#!/usr/bin/env python3
"""Small bounded Gearman protocol lab. Not a production connection pool.

One foreground request at a time. No transparent resubmission. Python >= 3.10.
See references/protocol-framing.md and references/protocol-client.md.
"""
from __future__ import annotations

import socket
import math
import ssl
import struct
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable

HEADER = struct.Struct("!4sII")
REQUEST = b"\x00REQ"
RESPONSE = b"\x00RES"
MAX_FRAME = 1024 * 1024  # Lab policy, not a Gearman protocol limit.


class Command(IntEnum):
    CAN_DO = 1
    CANT_DO = 2
    RESET_ABILITIES = 3
    PRE_SLEEP = 4
    NOOP = 6
    SUBMIT_JOB = 7
    JOB_CREATED = 8
    GRAB_JOB = 9
    NO_JOB = 10
    JOB_ASSIGN = 11
    WORK_STATUS = 12
    WORK_COMPLETE = 13
    WORK_FAIL = 14
    GET_STATUS = 15
    ECHO_REQ = 16
    ECHO_RES = 17
    SUBMIT_JOB_BG = 18
    ERROR = 19
    STATUS_RES = 20
    SUBMIT_JOB_HIGH = 21
    SET_CLIENT_ID = 22
    CAN_DO_TIMEOUT = 23
    WORK_EXCEPTION = 25
    OPTION_REQ = 26
    OPTION_RES = 27
    WORK_DATA = 28
    WORK_WARNING = 29
    GRAB_JOB_UNIQ = 30
    JOB_ASSIGN_UNIQ = 31
    SUBMIT_JOB_HIGH_BG = 32
    SUBMIT_JOB_LOW = 33
    SUBMIT_JOB_LOW_BG = 34
    SUBMIT_JOB_SCHED = 35
    SUBMIT_JOB_EPOCH = 36


class ProtocolError(RuntimeError):
    pass


class JobFailed(RuntimeError):
    """Terminal worker failure observed; details are not logged automatically."""


class OutcomeUnknown(RuntimeError):
    """The connection failed after a submission may have reached the server."""


@dataclass(frozen=True)
class Packet:
    command: int
    body: bytes


def remaining(deadline: float) -> float:
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise TimeoutError("operation deadline exceeded")
    return seconds


def recv_exact(sock: socket.socket, length: int, deadline: float) -> bytes:
    if length < 0:
        raise ValueError("negative read length")
    chunks = bytearray()
    while len(chunks) < length:
        sock.settimeout(remaining(deadline))
        part = sock.recv(length - len(chunks))
        if not part:
            raise EOFError(f"stream closed after {len(chunks)} of {length} expected bytes")
        chunks.extend(part)
    return bytes(chunks)


def encode_packet(command: int, body: bytes = b"", *, magic: bytes = REQUEST,
                  max_frame: int = MAX_FRAME) -> bytes:
    if magic not in (REQUEST, RESPONSE):
        raise ValueError("invalid magic")
    if not isinstance(body, bytes):
        raise TypeError("packet body must be bytes")
    if not 0 <= int(command) <= 0xFFFFFFFF:
        raise ValueError("command outside unsigned 32-bit range")
    if len(body) > max_frame:
        raise ValueError("frame exceeds configured limit")
    return HEADER.pack(magic, int(command), len(body)) + body


def read_packet(sock: socket.socket, deadline: float, *, magic: bytes = RESPONSE,
                max_frame: int = MAX_FRAME) -> Packet:
    wire_magic, command, size = HEADER.unpack(recv_exact(sock, HEADER.size, deadline))
    if wire_magic != magic:
        raise ProtocolError("wrong protocol magic; verify TLS mode and target service")
    if size > max_frame:
        raise ProtocolError("declared frame exceeds configured limit")
    return Packet(command, recv_exact(sock, size, deadline))


def field_bytes(value: str | bytes, name: str, *, maximum: int = 64,
                allow_empty: bool = False) -> bytes:
    raw = value.encode("ascii") if isinstance(value, str) else value
    if not isinstance(raw, bytes):
        raise TypeError(f"{name} must be ASCII text or bytes")
    if (not raw and not allow_empty) or len(raw) > maximum or b"\x00" in raw:
        raise ValueError(f"invalid {name}; maximum {maximum} bytes, no NUL")
    # Restrictive lab policy keeps metadata safe for logs/admin output.
    if any(byte < 33 or byte > 126 for byte in raw):
        raise ValueError(f"{name} must contain printable non-space ASCII")
    return raw


def make_tls_context(ca: str, cert: str | None = None,
                     key: str | None = None) -> ssl.SSLContext:
    if bool(cert) != bool(key):
        raise ValueError("client certificate and key must be supplied together")
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    if cert:
        context.load_cert_chain(cert, key)
    return context


@dataclass
class Session:
    sock: socket.socket
    timeout: float = 10.0
    max_frame: int = MAX_FRAME

    @classmethod
    def connect(cls, host: str, port: int = 4730, *, timeout: float = 10.0,
                ca: str | None = None, cert: str | None = None,
                key: str | None = None, server_name: str | None = None) -> "Session":
        if not math.isfinite(timeout) or timeout <= 0 or not 1 <= port <= 65535:
            raise ValueError("positive timeout and valid TCP port required")
        if (cert or key or server_name) and not ca:
            raise ValueError("TLS certificate/name options require --ca")
        context = make_tls_context(ca, cert, key) if ca else None
        sock = socket.create_connection((host, port), timeout=timeout)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if context:
                sock = context.wrap_socket(sock, server_hostname=server_name or host)
            return cls(sock, timeout)
        except BaseException:
            sock.close()
            raise

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self.sock.close()

    def send(self, command: int, body: bytes = b"", *, deadline: float | None = None) -> None:
        deadline = deadline if deadline is not None else time.monotonic() + self.timeout
        self.sock.settimeout(remaining(deadline))
        self.sock.sendall(encode_packet(command, body, max_frame=self.max_frame))

    def recv(self, *, deadline: float | None = None) -> Packet:
        deadline = deadline if deadline is not None else time.monotonic() + self.timeout
        return read_packet(self.sock, deadline, max_frame=self.max_frame)

    def echo(self, value: bytes = b"gearman-skill-probe") -> None:
        deadline = time.monotonic() + self.timeout
        self.send(Command.ECHO_REQ, value, deadline=deadline)
        packet = self.recv(deadline=deadline)
        if packet.command != Command.ECHO_RES or packet.body != value:
            raise ProtocolError("unexpected echo response")

    def enable_exceptions(self) -> None:
        deadline = time.monotonic() + self.timeout
        self.send(Command.OPTION_REQ, b"exceptions", deadline=deadline)
        response = self.recv(deadline=deadline)
        if response.command != Command.OPTION_RES or response.body != b"exceptions":
            raise ProtocolError("exceptions option not acknowledged")

    def submit(self, function: str, payload: bytes, unique: str, *, background: bool = False,
               priority: str = "normal", on_event: Callable[[Packet], None] | None = None,
               max_event_bytes: int = 4 * MAX_FRAME) -> "Completion":
        """One request per call/connection; caller closes on any error.

        A send/read failure is outcome-unknown, never grounds for blind retry.
        timeout is a total submit-to-terminal budget, not a worker time limit.
        """
        function_raw = field_bytes(function, "function")
        unique_raw = field_bytes(unique, "unique")
        commands = {
            (False, "normal"): Command.SUBMIT_JOB,
            (False, "high"): Command.SUBMIT_JOB_HIGH,
            (False, "low"): Command.SUBMIT_JOB_LOW,
            (True, "normal"): Command.SUBMIT_JOB_BG,
            (True, "high"): Command.SUBMIT_JOB_HIGH_BG,
            (True, "low"): Command.SUBMIT_JOB_LOW_BG,
        }
        if (background, priority) not in commands:
            raise ValueError("priority must be normal, high, or low")
        body = function_raw + b"\0" + unique_raw + b"\0" + payload
        # Validate before entering the ambiguous network section.
        encode_packet(commands[(background, priority)], body, max_frame=self.max_frame)
        deadline = time.monotonic() + self.timeout
        handle: bytes | None = None
        event_bytes = 0
        events: list[Packet] = []
        try:
            self.send(commands[(background, priority)], body, deadline=deadline)
            while True:
                packet = self.recv(deadline=deadline)
                if packet.command == Command.ERROR:
                    # A server error is preserved as a protocol failure; do not infer
                    # retry safety for every extension/plugin error code.
                    raise ProtocolError("server returned ERROR; inspect sanitized server logs")
                if packet.command == Command.JOB_CREATED:
                    if handle is not None or not packet.body or b"\0" in packet.body:
                        raise ProtocolError("invalid or repeated JOB_CREATED")
                    handle = packet.body
                    if background:
                        return Completion(handle, None, [])
                    continue
                if handle is None:
                    raise ProtocolError("work event arrived before JOB_CREATED")
                if packet.command == Command.WORK_FAIL:
                    if packet.body != handle:
                        raise ProtocolError("WORK_FAIL handle mismatch")
                    raise JobFailed("worker reported WORK_FAIL")
                if packet.command not in (Command.WORK_COMPLETE, Command.WORK_EXCEPTION,
                                          Command.WORK_DATA, Command.WORK_WARNING,
                                          Command.WORK_STATUS):
                    raise ProtocolError(f"unexpected response type {packet.command}")
                event_handle, sep, data = packet.body.partition(b"\0")
                if not sep or event_handle != handle:
                    raise ProtocolError("work event handle mismatch or missing delimiter")
                if packet.command == Command.WORK_COMPLETE:
                    return Completion(handle, data, events)
                if packet.command == Command.WORK_EXCEPTION:
                    # gearmand 2.1.0 treats this as terminal. Do not log raw data.
                    raise JobFailed("worker reported WORK_EXCEPTION")
                event_bytes += len(packet.body)
                if event_bytes > max_event_bytes or len(events) >= 10000:
                    raise ProtocolError("work event budget exceeded")
                if packet.command == Command.WORK_STATUS:
                    parts = data.split(b"\0")
                    if len(parts) != 2 or not all(x.isdigit() for x in parts):
                        raise ProtocolError("malformed WORK_STATUS")
                if on_event:
                    on_event(packet)
                events.append(packet)
        except (OSError, EOFError, TimeoutError) as error:
            raise OutcomeUnknown("submission may have been accepted; reconcile request_id") from error


@dataclass(frozen=True)
class Completion:
    handle: bytes
    result: bytes | None
    events: list[Packet] = field(default_factory=list)
