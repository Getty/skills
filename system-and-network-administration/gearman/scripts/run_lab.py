#!/usr/bin/env python3
"""Opt-in isolated gearmand smoke lab. Default is plan-only; no installation.

Execution requires Linux /proc so the harness can check that the native listener
belongs to the daemon it created, rather than probing a possibly unrelated port.
See references/testing.md. This is not a production acceptance suite.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import uuid
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'examples/python'))
from gearman_wire import Session, Command, JobFailed
from contract import encode
from result_store import ResultStore


def listener_owned(pid: int, port: int) -> bool:
    """Linux-only ownership check; failure to inspect is a closed gate."""
    try:
        inodes = set()
        for fd in (Path('/proc') / str(pid) / 'fd').iterdir():
            try:
                link = os.readlink(fd)
            except OSError:
                continue
            if link.startswith('socket:['):
                inodes.add(link[8:-1])
        for line in Path('/proc/net/tcp').read_text().splitlines()[1:]:
            fields = line.split()
            if (fields[1] == f'0100007F:{port:04X}' and fields[3] == '0A'
                    and fields[9] in inodes):
                return True
    except (OSError, IndexError):
        return False
    return False


def stop_process(process: subprocess.Popen) -> None:
    """Only accept an owned Popen instance; never kill by name or arbitrary PID."""
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


class Lab:
    def __init__(self, executable: str, directory: Path, persistence: bool):
        self.directory = directory
        self.executable = executable
        self.persistence = persistence
        self.server: subprocess.Popen | None = None
        self.workers: list[subprocess.Popen] = []
        self.logs = []
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            self.port = reservation.getsockname()[1]

    def start(self) -> None:
        command = [self.executable, '--listen=127.0.0.1', f'--port={self.port}',
                   '--job-retries=3', '--verbose=NOTICE',
                   f'--pid-file={self.directory / "server.pid"}',
                   f'--log-file={self.directory / "gearmand.log"}']
        if os.geteuid() == 0:
            import pwd
            command.append(f'--user={pwd.getpwuid(os.getuid()).pw_name}')
        if self.persistence:
            command += ['--queue-type=libsqlite3', f'--libsqlite3-db={self.directory / "queue.sqlite"}']
        log = open(self.directory / 'process.log', 'ab')
        self.logs.append(log)
        self.server = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if self.server.poll() is not None:
                raise RuntimeError('owned daemon exited before readiness; inspect captured logs')
            if listener_owned(self.server.pid, self.port):
                with self.connect() as session:
                    session.echo()
                return
            time.sleep(.05)
        raise RuntimeError('no verified owned listener became ready; no unrelated endpoint was probed')

    def connect(self) -> Session:
        if self.server is None or self.server.poll() is not None or not listener_owned(self.server.pid, self.port):
            raise RuntimeError('daemon listener ownership not verified')
        return Session.connect('127.0.0.1', self.port, timeout=5)

    def worker(self, *, result_db: bool = False) -> subprocess.Popen:
        # Check ownership before starting an adapter configured for this endpoint.
        with self.connect() as session:
            session.echo()
        command = [sys.executable, '-B', str(ROOT / 'examples/python/worker.py'),
                   '--host', '127.0.0.1', '--port', str(self.port), '--max-jobs', '1', '--timeout', '5']
        if result_db:
            command += ['--result-db', str(self.directory / 'results.sqlite')]
        p = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.workers.append(p)
        return p

    @staticmethod
    def wait_worker(p: subprocess.Popen) -> None:
        stdout, stderr = p.communicate(timeout=10)
        if p.returncode:
            raise RuntimeError(f'owned Python worker failed: {stderr.decode(errors="replace")[:1000]}')

    def close(self) -> None:
        for p in self.workers:
            stop_process(p)
            if p.stdout: p.stdout.close()
            if p.stderr: p.stderr.close()
        if self.server:
            stop_process(self.server)
        for log in self.logs:
            log.close()


def request() -> dict:
    return {'schema_version': 1, 'request_id': str(uuid.uuid4()), 'operation': 'sum.v1',
            'payload': {'numbers': [10, 20, -3]}}


def run(executable: str, persistence: bool) -> dict:
    checks = []
    with tempfile.TemporaryDirectory(prefix='gearman-skill-') as temp:
        lab = Lab(executable, Path(temp), persistence)
        try:
            lab.start()
            checks.append('owned_loopback_listener_and_echo')
            obj = request()
            worker = lab.worker()
            with lab.connect() as s:
                out = s.submit('gearman_skill.sum.v1', encode(obj), obj['request_id'])
            if json.loads(out.result)['result']['sum'] != 27:
                raise AssertionError('foreground result mismatch')
            lab.wait_worker(worker)
            checks.append('foreground_sum')
            obj = request()
            with lab.connect() as s:
                first = s.submit('gearman_skill.sum.v1', encode(obj), obj['request_id'], background=True)
            with lab.connect() as s:
                duplicate = s.submit('gearman_skill.sum.v1', encode(obj), obj['request_id'], background=True)
            if first.handle != duplicate.handle:
                raise AssertionError('active queued unique did not coalesce')
            worker = lab.worker(result_db=True)
            lab.wait_worker(worker)
            store = ResultStore(lab.directory / 'results.sqlite')
            try:
                if store.lookup(obj['request_id'])['result']['sum'] != 27:
                    raise AssertionError('background outcome missing')
            finally:
                store.close()
            checks += ['background_acceptance_and_external_result', 'active_unique_coalescing']
            worker = lab.worker()
            with lab.connect() as s:
                try:
                    s.submit('gearman_skill.sum.v1', b'not JSON', str(uuid.uuid4()))
                except JobFailed:
                    pass
                else:
                    raise AssertionError('invalid job did not produce WORK_FAIL')
            lab.wait_worker(worker)
            checks.append('explicit_worker_failure')
            obj = request()
            with lab.connect() as s:
                s.submit('gearman_skill.sum.v1', encode(obj), obj['request_id'], background=True)
            with lab.connect() as abandoned:
                abandoned.send(Command.CAN_DO, b'gearman_skill.sum.v1')
                abandoned.send(Command.GRAB_JOB_UNIQ)
                assignment = abandoned.recv()
                if assignment.command != Command.JOB_ASSIGN_UNIQ:
                    raise AssertionError('interruption fixture did not get an assignment')
                # Close without completion; only the test's pure operation was assigned.
            worker = lab.worker(result_db=True)
            lab.wait_worker(worker)
            store = ResultStore(lab.directory / 'results.sqlite')
            try:
                if not store.lookup(obj['request_id']):
                    raise AssertionError('disconnected assignment was not recovered')
            finally:
                store.close()
            checks.append('worker_disconnect_redelivery_with_configured_threshold')
            if persistence:
                obj = request()
                with lab.connect() as s:
                    s.submit('gearman_skill.sum.v1', encode(obj), obj['request_id'], background=True)
                stop_process(lab.server)
                lab.start()
                worker = lab.worker(result_db=True)
                lab.wait_worker(worker)
                store = ResultStore(lab.directory / 'results.sqlite')
                try:
                    if not store.lookup(obj['request_id']):
                        raise AssertionError('SQLite pending-job replay failed')
                finally:
                    store.close()
                checks.append('sqlite_pending_job_restart_replay')
            return {'ok': True, 'executed': True, 'checks': checks,
                    'scope': 'isolated smoke tests; not a production or all-backend certification'}
        except Exception as error:
            tails = {}
            for name in ('gearmand.log', 'process.log'):
                p = lab.directory / name
                if p.exists():
                    tails[name] = p.read_bytes()[-8000:].decode(errors='replace')
            return {'ok': False, 'executed': True, 'passed_checks': checks,
                    'error_type': type(error).__name__, 'error': str(error), 'owned_daemon_log_tails': tails}
        finally:
            lab.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--persistence', action='store_true')
    parser.add_argument('--gearmand', default='gearmand', help='locally installed executable, never downloaded')
    args = parser.parse_args()
    plan = {'executed': False, 'mode': 'plan_only', 'requires': ['Linux /proc ownership inspection', 'installed gearmand'],
            'actions': ['start owned foreground daemon on loopback with temporary state',
                        'ECHO, foreground, background/result, active unique, failure, interruption smoke tests',
                        'optional SQLite restart/replay', 'stop only owned processes and delete temporary state'],
            'persistence_requested': args.persistence,
            'not_covered': ['all backends', 'native C/Perl/PHP integration', 'live TLS', 'multi-server failover',
                            'container/Kubernetes deployment', 'crash after external side effect']}
    if not args.execute:
        print(json.dumps(plan, indent=2)); return 0
    executable = shutil.which(args.gearmand)
    if not executable or not Path('/proc/net/tcp').exists():
        print(json.dumps({'ok': False, 'executed': False, 'error': 'installed gearmand and Linux /proc required'}, indent=2))
        return 2
    version = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=5, check=False)
    result = run(executable, args.persistence)
    result['binary_version_output'] = (version.stdout + version.stderr)[:4000]
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
