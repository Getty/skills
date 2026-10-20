#!/usr/bin/env python3
"""Submit a validated example job. This command writes to the selected server."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from gearman_wire import Session, JobFailed, OutcomeUnknown, ProtocolError
from contract import MAX_BYTES, parse


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4730)
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--function", default="gearman_skill.sum.v1")
    parser.add_argument("--background", action="store_true")
    parser.add_argument("--priority", choices=("normal", "high", "low"), default="normal")
    parser.add_argument("--unique", help="transport identity; defaults to envelope request_id")
    parser.add_argument("--ca")
    parser.add_argument("--cert")
    parser.add_argument("--key")
    parser.add_argument("--server-name")
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        obj = parse(raw)
        with Session.connect(args.host, args.port, timeout=args.timeout, ca=args.ca,
                             cert=args.cert, key=args.key, server_name=args.server_name) as session:
            if not args.background:
                session.enable_exceptions()
            done = session.submit(args.function, raw, args.unique or obj["request_id"],
                                  background=args.background, priority=args.priority)
            if args.background:
                print(json.dumps({"accepted": True, "completed": False,
                                  "server": f"{args.host}:{args.port}",
                                  "handle": done.handle.decode("ascii"),
                                  "request_id": obj["request_id"]}))
            else:
                sys.stdout.buffer.write((done.result or b"") + b"\n")
        return 0
    except OutcomeUnknown as error:
        print(str(error), file=sys.stderr)
        return 3
    except (OSError, ValueError, JobFailed, ProtocolError, EOFError) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
