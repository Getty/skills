#!/usr/bin/env python3
"""Read-only protocol probe/admin utility. Never submits jobs or mutates queues."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import time
from gearman_wire import Session, ProtocolError, remaining

ALLOWED = {"version": False, "status": True, "workers": True}


def parse_status(text: str) -> list[dict[str, object]]:
    result = []
    seen = set()
    for line in text.splitlines():
        if line == ".":
            continue
        parts = line.split("\t")
        if len(parts) != 4 or not parts[0] or parts[0] in seen:
            raise ProtocolError("invalid/duplicate status row")
        if not all(value.isascii() and value.isdigit() for value in parts[1:]):
            raise ProtocolError("non-negative integer status counts required")
        total, running, capable = map(int, parts[1:])
        if running > total:
            raise ProtocolError("running exceeds total in one status snapshot")
        seen.add(parts[0])
        result.append({"function": parts[0], "total": total, "running": running,
                       "waiting": total - running, "capable_registrations": capable})
    return result


def admin_query(session: Session, command: str, *, max_bytes: int = 1024 * 1024) -> str:
    if command not in ALLOWED:
        raise ValueError("command not in read-only allowlist")
    deadline = time.monotonic() + session.timeout
    session.sock.settimeout(remaining(deadline))
    session.sock.sendall(command.encode("ascii") + b"\n")
    data = bytearray()
    # Read whole lines without assuming socket closure terminates the response.
    while True:
        session.sock.settimeout(remaining(deadline))
        chunk = session.sock.recv(min(4096, max_bytes + 1 - len(data)))
        if not chunk:
            raise EOFError("admin response ended without its terminator")
        data.extend(chunk)
        if len(data) > max_bytes:
            raise ProtocolError("admin response exceeds byte budget")
        lines = bytes(data).split(b"\n")
        completed = [line.rstrip(b"\r") for line in lines[:-1]]
        if completed and (not ALLOWED[command] or b"." in completed):
            terminal = completed.index(b".") if ALLOWED[command] else 0
            return b"\n".join(completed[:terminal + 1]).decode("utf-8", errors="strict")


def inventory() -> dict[str, object]:
    result = {}
    for name, options in {"gearmand": ["--version", "--help"],
                          "gearman": ["-H"], "gearadmin": ["--help"]}.items():
        path = shutil.which(name)
        if not path:
            result[name] = {"available": False}
            continue
        captures = []
        for option in options:
            try:
                process = subprocess.run([path, option], capture_output=True, text=True,
                                         timeout=10, check=False)
                captures.append({"option": option, "returncode": process.returncode,
                                 "stdout": process.stdout[:100000],
                                 "stderr": process.stderr[:100000]})
            except subprocess.TimeoutExpired:
                captures.append({"option": option, "error": "timeout"})
        result[name] = {"available": True, "path": path, "captures": captures}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("inventory", help="only execute installed tools' help/version commands")
    for action in ("probe", "admin"):
        p = sub.add_parser(action)
        p.add_argument("--host", default="127.0.0.1")
        p.add_argument("--port", type=int, default=4730)
        p.add_argument("--timeout", type=float, default=3.0)
        p.add_argument("--ca")
        p.add_argument("--cert")
        p.add_argument("--key")
        p.add_argument("--server-name")
        if action == "admin":
            p.add_argument("command", choices=sorted(ALLOWED))
    args = parser.parse_args()
    try:
        if args.action == "inventory":
            output = inventory()
        else:
            start = time.monotonic()
            with Session.connect(args.host, args.port, timeout=args.timeout, ca=args.ca,
                                 cert=args.cert, key=args.key, server_name=args.server_name) as session:
                if args.action == "probe":
                    session.echo()
                    output = {"ok": True, "kind": "binary_echo_only",
                              "elapsed_ms": round((time.monotonic() - start) * 1000, 3)}
                else:
                    text = admin_query(session, args.command)
                    output = {"command": args.command, "server": f"{args.host}:{args.port}",
                              "data": parse_status(text) if args.command == "status" else text}
        print(json.dumps(output, ensure_ascii=True, indent=2))
        return 0
    except (OSError, EOFError, ValueError, RuntimeError, UnicodeError) as error:
        print(json.dumps({"ok": False, "error_type": type(error).__name__,
                          "error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
