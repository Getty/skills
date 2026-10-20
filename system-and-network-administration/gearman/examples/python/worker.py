#!/usr/bin/env python3
"""Single-connection, one-job-at-a-time lab worker. No automatic reconnect/retry."""
from __future__ import annotations
import argparse
import json
import select
import signal
import sqlite3
import sys
import threading
import time
from pathlib import Path
from typing import Callable
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from gearman_wire import Session, Command, ProtocolError, field_bytes
from contract import parse, execute, encode, ContractError
from result_store import ResultStore


def serve(session: Session, function: str, *, stop: threading.Event | None = None,
          max_jobs: int = 0, handler: Callable[[bytes], bytes] | None = None) -> int:
    stop = stop or threading.Event()
    name = field_bytes(function, "function")
    if max_jobs < 0:
        raise ValueError("max_jobs must be nonnegative")
    handler = handler or (lambda raw: encode(execute(parse(raw))))
    session.send(Command.CAN_DO, name)
    completed = 0
    while not stop.is_set() and (max_jobs == 0 or completed < max_jobs):
        session.send(Command.GRAB_JOB_UNIQ)
        deadline = time.monotonic() + session.timeout
        packet = session.recv(deadline=deadline)
        while packet.command == Command.NOOP:
            # Already have an outstanding GRAB; repeated wakeups do not reset its budget.
            packet = session.recv(deadline=deadline)
        if packet.command == Command.NO_JOB:
            session.send(Command.PRE_SLEEP)
            while not stop.is_set():
                pending = getattr(session.sock, "pending", lambda: 0)()
                if not pending and not select.select([session.sock], [], [], 0.25)[0]:
                    continue
                wake = session.recv()
                if wake.command != Command.NOOP:
                    raise ProtocolError("expected NOOP while sleeping")
                break
            continue
        if packet.command != Command.JOB_ASSIGN_UNIQ:
            raise ProtocolError("expected JOB_ASSIGN_UNIQ")
        parts = packet.body.split(b"\0", 3)
        if len(parts) != 4 or not parts[0] or parts[1] != name:
            raise ProtocolError("invalid job assignment")
        handle, _, _transport_unique, raw = parts
        # On SIGTERM after assignment, finish this small pure task before leaving.
        try:
            result = handler(raw)
        except (ContractError, ValueError):
            session.send(Command.WORK_FAIL, handle)
        else:
            session.send(Command.WORK_COMPLETE, handle + b"\0" + result)
        completed += 1
    return completed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4730)
    parser.add_argument("--function", default="gearman_skill.sum.v1")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--result-db", help="single-host demo only; never share SQLite over a network filesystem")
    parser.add_argument("--ca")
    parser.add_argument("--cert")
    parser.add_argument("--key")
    parser.add_argument("--server-name")
    args = parser.parse_args()
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    store = None
    try:
        store = ResultStore(args.result_db) if args.result_db else None
        handler = (lambda raw: encode(store.apply(parse(raw)))) if store else None
        with Session.connect(args.host, args.port, timeout=args.timeout, ca=args.ca,
                             cert=args.cert, key=args.key, server_name=args.server_name) as session:
            count = serve(session, args.function, stop=stop, max_jobs=args.max_jobs, handler=handler)
        print(json.dumps({"worker_stopped": True, "jobs_handled": count}), file=sys.stderr)
        return 0
    except (OSError, EOFError, RuntimeError, ValueError, sqlite3.Error) as error:
        print(json.dumps({"worker_stopped": True, "error_type": type(error).__name__}), file=sys.stderr)
        return 1
    finally:
        if store:
            store.close()

if __name__ == "__main__":
    raise SystemExit(main())
