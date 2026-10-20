"""Safety gates for helper tools; never starts a daemon."""
import contextlib
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_lab

class ToolGateTests(unittest.TestCase):
    def test_default_is_plan_without_process_or_lookup(self):
        output=io.StringIO()
        with patch.object(sys,'argv',['run_lab.py']), patch('run_lab.subprocess.Popen') as popen, \
             patch('run_lab.shutil.which') as which, contextlib.redirect_stdout(output):
            self.assertEqual(run_lab.main(),0)
        popen.assert_not_called();which.assert_not_called()
        self.assertFalse(json.loads(output.getvalue())['executed'])
    def test_missing_daemon_is_failure_not_passing_skip(self):
        output=io.StringIO()
        with patch.object(sys,'argv',['run_lab.py','--execute']), patch('run_lab.shutil.which',return_value=None), \
             patch('run_lab.subprocess.Popen') as popen, contextlib.redirect_stdout(output):
            self.assertEqual(run_lab.main(),2)
        popen.assert_not_called();self.assertFalse(json.loads(output.getvalue())['ok'])
    def test_unverified_listener_blocks_connection(self):
        lab=run_lab.Lab.__new__(run_lab.Lab)
        lab.server=Mock();lab.server.poll.return_value=None;lab.server.pid=123;lab.port=12345
        with patch('run_lab.listener_owned',return_value=False), patch('run_lab.Session.connect') as connect:
            with self.assertRaises(RuntimeError):lab.connect()
        connect.assert_not_called()
    def test_stop_does_not_signal_exited_process(self):
        p=Mock();p.poll.return_value=0
        run_lab.stop_process(p)
        p.terminate.assert_not_called();p.kill.assert_not_called()
    def test_stop_owned_process_escalates_only_on_timeout(self):
        p=Mock();p.poll.return_value=None
        p.wait.side_effect=[subprocess.TimeoutExpired('owned',5),0]
        run_lab.stop_process(p)
        p.terminate.assert_called_once();p.kill.assert_called_once()
        self.assertEqual(p.wait.call_count,2)
    def test_agent_rubrics_reference_existing_chapters(self):
        obj=json.loads((ROOT/'tests/evaluation-cases.json').read_text())
        ids=set()
        for case in obj['cases']:
            self.assertNotIn(case['id'],ids);ids.add(case['id'])
            self.assertTrue(case['expected']);self.assertTrue(case['reject'])
            for ref in case['read']:self.assertTrue((ROOT/ref).is_file(),ref)
        self.assertGreaterEqual(len(ids),20)
