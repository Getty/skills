#!/usr/bin/env python3
"""Capture trusted Craft CLI catalogs and optional headless MCP metadata.

Python 3.10+, standard library only. No shell, installation, tools/call, or
resources/read. Running a native binary is still code execution, not a sandbox.
Reports/logs may contain local paths: keep the newly created directory private.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from typing import Any

class ProbeError(RuntimeError):
    pass

def strict_json(text: str) -> Any:
    def reject(value: str) -> None:
        raise ValueError(f"Non-finite JSON number: {value}")
    return json.loads(text, parse_constant=reject)

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def private_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)

def write_json(path: Path, value: Any) -> None:
    private_write(path, (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode())

def stop_process(proc: subprocess.Popen[bytes]) -> None:
    """Stop our process group on POSIX; Windows stops the direct process only."""
    try:
        if os.name == 'posix':
            os.killpg(proc.pid, signal.SIGKILL)
        elif proc.poll() is None:
            proc.kill()
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass

def validate_limits(timeout: float, max_bytes: int) -> None:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('timeout must be positive and finite')
    if max_bytes < 64 or max_bytes > 256 * 1024 * 1024:
        raise ValueError('max-bytes must be between 64 and 268435456')

def run_bounded(argv: list[str], *, timeout: float = 20, max_bytes: int = 16*1024*1024,
                cwd: Path | None = None) -> dict[str, Any]:
    """Capture both streams with a shared memory budget; never execute a shell."""
    validate_limits(timeout, max_bytes)
    if not argv or not all(isinstance(x, str) and '\x00' not in x for x in argv):
        raise ValueError('argv must be nonempty strings without NULs')
    started = time.monotonic()
    proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, cwd=cwd, shell=False, bufsize=0,
        start_new_session=(os.name == 'posix'))
    captured = {'stdout': bytearray(), 'stderr': bytearray()}
    lock = threading.Lock()
    overflow = threading.Event()
    def pump(stream: Any, key: str) -> None:
        try:
            while True:
                block = stream.read(8192)
                if not block:
                    break
                with lock:
                    remaining = max_bytes - sum(len(v) for v in captured.values())
                    captured[key].extend(block[:remaining])
                    if len(block) > remaining:
                        overflow.set()
        except (OSError, ValueError):
            pass
    threads = [threading.Thread(target=pump, args=(proc.stdout, 'stdout'), daemon=True),
               threading.Thread(target=pump, args=(proc.stderr, 'stderr'), daemon=True)]
    for thread in threads:
        thread.start()
    reason = None
    while proc.poll() is None:
        if overflow.is_set():
            reason = 'output_limit'
            stop_process(proc)
            break
        if time.monotonic() - started >= timeout:
            reason = 'timeout'
            stop_process(proc)
            break
        time.sleep(0.01)
    for thread in threads:
        thread.join(timeout=0.5)
    if any(thread.is_alive() for thread in threads):
        reason = reason or 'descendant_kept_pipe_open'
        stop_process(proc)
        for thread in threads:
            thread.join(timeout=0.5)
    if overflow.is_set():
        reason = reason or 'output_limit'
    with lock:
        raw = {key: bytes(value) for key, value in captured.items()}
    for stream in (proc.stdout, proc.stderr):
        if stream is not None:
            stream.close()
    return {'argv': argv, 'returncode': proc.poll(), 'reason': reason,
            'elapsed_seconds': round(time.monotonic()-started, 6), **raw}

class McpWire:
    """Serial JSON-lines MCP client limited to metadata discovery."""
    def __init__(self, argv: list[str], *, timeout: float, max_bytes: int):
        validate_limits(timeout, max_bytes)
        self.timeout, self.max_bytes = timeout, max_bytes
        self.proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False, bufsize=0,
            start_new_session=(os.name == 'posix'))
        self.events: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.raw = {'stdout': bytearray(), 'stderr': bytearray()}
        self.lock = threading.Lock()
        self.next_id = 0
        self.notification_count = 0
        self.closed = False
        def retain(key: str, data: bytes) -> bool:
            with self.lock:
                remaining = self.max_bytes - sum(len(v) for v in self.raw.values())
                self.raw[key].extend(data[:remaining])
                ok = len(data) <= remaining
            if not ok:
                self.events.put(('error', 'MCP capture output limit exceeded'))
            return ok
        def stdout_reader() -> None:
            try:
                frames = 0
                while True:
                    line = self.proc.stdout.readline(self.max_bytes + 1)
                    if not line:
                        self.events.put(('eof', None))
                        break
                    if not retain('stdout', line):
                        break
                    frames += 1
                    if frames > 4096:
                        self.events.put(('error', 'Too many MCP frames'))
                        break
                    if not line.endswith(b'\n'):
                        self.events.put(('error', 'Unterminated or oversized MCP JSON line'))
                        break
                    self.events.put(('line', line))
            except (OSError, ValueError) as exc:
                self.events.put(('error', str(exc)))
        def stderr_reader() -> None:
            try:
                while True:
                    chunk = self.proc.stderr.read(8192)
                    if not chunk or not retain('stderr', chunk):
                        break
            except (OSError, ValueError):
                pass
        self.threads = [threading.Thread(target=stdout_reader, daemon=True),
                        threading.Thread(target=stderr_reader, daemon=True)]
        for thread in self.threads:
            thread.start()
    def send(self, obj: dict[str, Any]) -> None:
        try:
            self.proc.stdin.write((json.dumps(obj, separators=(',', ':'), allow_nan=False)+'\n').encode())
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise ProbeError(f'MCP stdin unavailable: {exc}') from exc
    def request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        if method not in {'initialize', 'tools/list', 'resources/list', 'resources/templates/list'}:
            raise ProbeError('This client only permits metadata methods')
        self.next_id += 1
        ident = self.next_id
        self.send({'jsonrpc':'2.0', 'id':ident, 'method':method, 'params':params})
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ProbeError(f'MCP timeout waiting for {method}')
            try:
                kind, payload = self.events.get(timeout=remaining)
            except queue.Empty as exc:
                raise ProbeError(f'MCP timeout waiting for {method}') from exc
            if kind != 'line':
                raise ProbeError(f'MCP {kind}: {payload or "server closed stdout"}')
            try:
                obj = strict_json(payload.decode('utf-8'))
            except (ValueError, UnicodeError) as exc:
                raise ProbeError('Non-JSON or non-UTF-8 data on MCP stdout') from exc
            if not isinstance(obj, dict) or obj.get('jsonrpc') != '2.0':
                raise ProbeError('Invalid MCP JSON-RPC envelope')
            if 'method' in obj:
                if 'id' in obj:
                    self.send({'jsonrpc':'2.0','id':obj['id'], 'error':
                               {'code':-32601,'message':'Metadata probe offers no client-side tools'}})
                    raise ProbeError('Server requested an unoffered client capability')
                self.notification_count += 1
                if self.notification_count > 1000:
                    raise ProbeError('MCP notification limit exceeded')
                continue
            if obj.get('id') != ident:
                raise ProbeError('Unexpected response id; refusing to mix sessions/results')
            if 'error' in obj:
                raise ProbeError(f'MCP RPC error for {method}: {obj["error"]}')
            if not isinstance(obj.get('result'), dict):
                raise ProbeError('MCP result must be an object')
            return obj['result']
    def pages(self, method: str, field: str, *, max_pages: int = 32) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        seen_cursors: set[str] = set()
        cursor: str | None = None
        for _ in range(max_pages):
            result = self.request(method, {} if cursor is None else {'cursor':cursor})
            page = result.get(field)
            if not isinstance(page, list) or not all(isinstance(v, dict) for v in page):
                raise ProbeError(f'Invalid {field} list')
            items.extend(page)
            if len(items) > 20000:
                raise ProbeError('MCP item count limit exceeded')
            cursor = result.get('nextCursor')
            if cursor is None:
                return items
            if not isinstance(cursor, str) or not cursor or cursor in seen_cursors:
                raise ProbeError('Invalid or repeated pagination cursor')
            seen_cursors.add(cursor)
        raise ProbeError('MCP pagination limit exceeded')
    def close(self) -> bool:
        if self.closed:
            return False
        self.closed = True
        forced = False
        try:
            self.proc.stdin.close()
        except (OSError, BrokenPipeError):
            pass
        try:
            self.proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            forced = True
            stop_process(self.proc)
        for thread in self.threads:
            thread.join(timeout=0.5)
        if any(thread.is_alive() for thread in self.threads):
            forced = True
            stop_process(self.proc)
        for stream in (self.proc.stdout, self.proc.stderr):
            if stream is not None:
                stream.close()
        return forced

def probe_mcp(argv: list[str], *, timeout: float = 20, max_bytes: int = 16*1024*1024,
              include_resources: bool = False) -> dict[str, Any]:
    wire = McpWire(argv, timeout=timeout, max_bytes=max_bytes)
    report: dict[str, Any] = {'argv':argv, 'status':'failed', 'tools_call_sent':False,
                              'resources_read_sent':False}
    try:
        init = wire.request('initialize', {'protocolVersion':'2025-06-18',
            'capabilities':{}, 'clientInfo':{'name':'storytold-skill-metadata-probe','version':'0.1.0'}})
        version = init.get('protocolVersion')
        if version not in {'2025-06-18','2025-03-26','2024-11-05'}:
            raise ProbeError(f'Unimplemented negotiated protocol version: {version!r}')
        wire.send({'jsonrpc':'2.0','method':'notifications/initialized'})
        report['initialize'] = init
        capabilities = init.get('capabilities', {})
        if not isinstance(capabilities, dict) or 'tools' not in capabilities:
            raise ProbeError('Server did not advertise a tools capability')
        tools = wire.pages('tools/list', 'tools')
        names: set[str] = set()
        for tool in tools:
            name = tool.get('name')
            if not isinstance(name, str) or not name or name in names:
                raise ProbeError('Missing or duplicate MCP tool name')
            if not isinstance(tool.get('inputSchema'), dict):
                raise ProbeError(f'Tool {name} has no object inputSchema')
            names.add(name)
        report['tools'] = tools
        if include_resources and 'resources' in capabilities:
            report['resources'] = wire.pages('resources/list', 'resources')
            report['resourceTemplates'] = wire.pages('resources/templates/list', 'resourceTemplates')
        report['status'] = 'metadata_observed'
    except (ProbeError, OSError, ValueError) as exc:
        report['error'] = str(exc)
    finally:
        report['forced_shutdown'] = wire.close()
        with wire.lock:
            report['stdout'] = bytes(wire.raw['stdout'])
            report['stderr'] = bytes(wire.raw['stderr'])
        report['returncode'] = wire.proc.poll()
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True, help='Absolute path to a trusted native CLI')
    parser.add_argument('--out', type=Path, required=True, help='New private directory; existing paths refused')
    parser.add_argument('--profile', type=Path, default=Path(__file__).resolve().parents[1]/'assets/runtime-profile.json')
    parser.add_argument('--mcp', action='store_true', help='Also launch the profile\'s explicit headless MCP server')
    parser.add_argument('--include-resources', action='store_true', help='List metadata only; never read resources')
    parser.add_argument('--timeout', type=float, default=20)
    parser.add_argument('--max-bytes', type=int, default=16*1024*1024)
    parser.add_argument('--execute', action='store_true', help='Required to execute the binary; otherwise print plan only')
    args = parser.parse_args()
    try:
        validate_limits(args.timeout,args.max_bytes)
        profile = strict_json(args.profile.read_text(encoding='utf-8'))
        if not profile.get('operator_cli_verified'):
            raise ValueError('No verified operator CLI in this product profile')
        binary = args.binary.expanduser().resolve(strict=True)
        if not binary.is_file():
            raise ValueError('binary must be a file')
        cli_argv = profile['catalog_argv']
        if not isinstance(cli_argv,list) or not all(isinstance(a,list) and a and all(isinstance(x,str) for x in a) for a in cli_argv):
            raise ValueError('Invalid catalog argv in trusted profile')
        mcp_argv = profile.get('mcp_argv')
        if args.mcp and (not isinstance(mcp_argv,list) or not mcp_argv or not all(isinstance(x,str) for x in mcp_argv)):
            raise ValueError('No valid headless MCP argv in profile')
        plan = {'app':profile['app'], 'cli_commands':[[str(binary),*a] for a in cli_argv],
                'mcp_command':[str(binary),*mcp_argv] if args.mcp else None,
                'warning':'Native code execution; not an OS sandbox. No tools/call or resources/read.'}
        if not args.execute:
            print(json.dumps(plan,indent=2)); return 0
        out = args.out.expanduser().absolute()
        out.mkdir(mode=0o700,parents=True,exist_ok=False)
        report: dict[str,Any] = {'schema':'storytold-capability-capture/1', 'app':profile['app'],
            'captured_at':datetime.now(timezone.utc).isoformat(), 'binary':str(binary),
            'binary_sha256':digest(binary), 'profile_sha256':digest(args.profile),
            'execution_scope':'metadata discovery only; no creative operation tested', 'cli':[]}
        failed = False
        for i, command in enumerate(plan['cli_commands'], 1):
            entry = run_bounded(command, timeout=args.timeout, max_bytes=args.max_bytes)
            for stream in ('stdout','stderr'):
                filename=f'cli-{i:02}-{stream}.log'
                private_write(out/filename, entry.pop(stream))
                entry[stream+'_file']=filename
            entry['status'] = 'observed' if entry['returncode']==0 and entry['reason'] is None else 'failed'
            failed |= entry['status']=='failed'
            report['cli'].append(entry)
        if args.mcp:
            entry=probe_mcp(plan['mcp_command'], timeout=args.timeout,max_bytes=args.max_bytes,
                            include_resources=args.include_resources)
            for stream in ('stdout','stderr'):
                filename=f'mcp-{stream}.log'
                private_write(out/filename, entry.pop(stream))
                entry[stream+'_file']=filename
            failed |= entry['status']!='metadata_observed'
            report['mcp']=entry
        report['status']='failed_or_partial' if failed else 'metadata_observed'
        report['output_files_sha256']={p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file()}
        write_json(out/'report.json',report)
        print(str(out/'report.json'))
        return 1 if failed else 0
    except (OSError,ValueError,KeyError,TypeError,ProbeError) as exc:
        print(f'capture_capabilities: {exc}',file=sys.stderr)
        return 2
if __name__ == '__main__':
    raise SystemExit(main())
