"""Pure local unit/integration tests. No vLLM/GPU or external network needed."""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import _common
import audit_env
import bench_sweep
import capacity
import cost
import metrics_inventory
import stream_probe
import validate_skill


class CommonTests(unittest.TestCase):
    def test_https_remote_is_allowed(self):
        self.assertEqual(_common.validate_url("https://example.org/", base=True), "https://example.org")

    def test_loopback_http_is_allowed(self):
        for url in ("http://localhost:8000", "http://127.0.0.1:8000", "http://[::1]:8000"):
            self.assertEqual(_common.validate_url(url, base=True), url)

    def test_remote_http_needs_opt_in(self):
        with self.assertRaises(ValueError):
            _common.validate_url("http://192.0.2.1:8000")
        self.assertEqual(_common.validate_url("http://192.0.2.1:8000", allow_insecure_http=True), "http://192.0.2.1:8000")

    def test_invalid_urls(self):
        for url in ("https://u:secret@example.org", "http://localhost:8000/v1", "https://x/?key=secret", "https://x/#a", "file:///tmp/x", "http://x:999999", "http://local host"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                _common.validate_url(url, base=True)

    def test_numeric_validators(self):
        for value in ("nan", "inf", "-inf", "bad"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                _common.positive_float(value)
        for value in ("0", "-1", "1.5"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                _common.positive_int(value)

    def test_no_overwrite_and_no_nan_files(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "result.json"
            _common.write_json(p, {"ok": True})
            with self.assertRaises(FileExistsError):
                _common.write_json(p, {"ok": False})
            self.assertEqual(json.loads(p.read_text()), {"ok": True})
            bad = Path(d) / "bad.json"
            with self.assertRaises(ValueError):
                _common.write_json(bad, {"bad": float("nan")})
            self.assertFalse(bad.exists())

    def test_json_size_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text('{"n": NaN}')
            with self.assertRaises(ValueError):
                _common.read_json(p)
            p.write_text('[1,2,3]')
            with self.assertRaises(ValueError):
                _common.read_json(p, max_bytes=2)

    def test_api_key_newline_rejected(self):
        with patch.dict(os.environ, {"VLLM_API_KEY": "secret\r\ninjected"}):
            with self.assertRaises(ValueError):
                _common.api_key()


class CapacityTests(unittest.TestCase):
    def args(self):
        return dict(gpu_gib=24, utilization=.85, parameters_b=8,
                    weight_bits=4, weight_overhead=1.15, runtime_gib=3,
                    reserve_gib=1, layers=32, kv_heads=8, head_dim=128,
                    kv_bits=16, context_tokens=8192, block_size=16)

    def test_known_synthetic_gqa(self):
        r = capacity.estimate(**self.args())
        self.assertEqual(r["kv_bytes_per_token_with_assumed_overhead"], 131072)
        self.assertEqual(r["kv_gib_per_full_length_sequence"], 1)
        self.assertEqual(r["estimated_full_length_sequence_capacity"], 12)

    def test_raw_weights_units(self):
        r = capacity.estimate(**self.args())
        self.assertAlmostEqual(r["raw_weights_gib"], 4e9 / 2**30)

    def test_block_rounding(self):
        args = self.args(); args["context_tokens"] = 8193
        self.assertEqual(capacity.estimate(**args)["context_tokens_rounded_to_blocks"], 8208)

    def test_fp8_halves_raw_kv(self):
        args = self.args(); args["kv_bits"] = 8
        self.assertEqual(capacity.estimate(**args)["kv_gib_per_full_length_sequence"], .5)

    def test_no_fit_is_zero_not_negative_capacity(self):
        args = self.args(); args["parameters_b"] = 70
        r = capacity.estimate(**args)
        self.assertEqual(r["estimated_full_length_sequence_capacity"], 0)
        self.assertFalse(r["estimated_memory_fit_for_one_sequence"])
        self.assertLess(r["remaining_kv_gib"], 0)

    def test_invalid_capacity_inputs(self):
        for key, value in (("utilization", 1.1), ("weight_overhead", .9), ("layers", 0),
                           ("runtime_gib", -1), ("gpu_gib", float("nan")), ("head_dim", 12.5)):
            args = self.args(); args[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                capacity.estimate(**args)


class CostTests(unittest.TestCase):
    def test_sample_arithmetic(self):
        r = cost.calculate(.8, 3, .15, 900000, 600, "EUR")
        self.assertAlmostEqual(r["total_cost"], 2.55)
        self.assertAlmostEqual(r["cost_per_million_useful_tokens"], 2.55 / .9)
        self.assertAlmostEqual(r["cost_per_accepted_request"], 2.55 / 600)

    def test_zero_denominators_are_unknown(self):
        r = cost.calculate(1, 1, 0, 0, 0, "EUR")
        self.assertIsNone(r["cost_per_million_useful_tokens"])
        self.assertIsNone(r["cost_per_accepted_request"])

    def test_invalid_cost_inputs(self):
        with self.assertRaises(ValueError):
            cost.calculate(-1, 1, 0, 1, 1, "EUR")
        with self.assertRaises(ValueError):
            cost.calculate(1, 1, 0, -1, 1, "EUR")


class MetricsTests(unittest.TestCase):
    def test_counter_suffix_and_label_redaction(self):
        text = '# HELP vllm:prefix_cache_hits Cache hit tokens\n# TYPE vllm:prefix_cache_hits counter\nvllm:prefix_cache_hits_total{model_name="PRIVATE-MODEL"} 42\n'
        r = metrics_inventory.parse_metrics(text)
        self.assertEqual(r["families"][0]["sample_names"], ["vllm:prefix_cache_hits_total"])
        self.assertNotIn("PRIVATE-MODEL", json.dumps(r))
        self.assertNotIn('"42"', json.dumps(r))

    def test_histogram_and_unknown(self):
        text = '# TYPE latency histogram\nlatency_bucket{le="1"} 3\nlatency_count 3\nlatency_sum .5\nunknown_metric 1\n'
        r = metrics_inventory.parse_metrics(text)
        self.assertEqual(len(r["families"][0]["sample_names"]), 3)
        self.assertEqual(r["untyped_or_unassigned_sample_names"], ["unknown_metric"])

    def test_unparsed_new_metric_syntax_is_not_hidden(self):
        r = metrics_inventory.parse_metrics('{"some unicode metric"} 1\n')
        self.assertEqual(r["unparsed_noncomment_line_count"], 1)


class SSETests(unittest.TestCase):
    def test_comments_crlf_and_multiline_data(self):
        raw = b': heartbeat\r\nevent: message\r\ndata: {"choices": [],\r\ndata: "usage": {"completion_tokens": 1}}\r\n\r\ndata: [DONE]\r\n\r\n'
        events = list(stream_probe.sse_data(io.BytesIO(raw)))
        self.assertEqual(len(events), 2)
        self.assertEqual(json.loads(events[0])["usage"]["completion_tokens"], 1)
        self.assertEqual(events[1], "[DONE]")

    def test_unfinished_record_rejected(self):
        with self.assertRaises(stream_probe.StreamProtocolError):
            list(stream_probe.sse_data(io.BytesIO(b'data: {"choices": []}\n')))

    def test_utf8_bom(self):
        raw = '\ufeffdata: {"text":"Hello 🌍"}\n\n'.encode()
        self.assertIn("Hello 🌍", list(stream_probe.sse_data(io.BytesIO(raw)))[0])

    def test_size_limit(self):
        with patch.object(stream_probe, "MAX_LINE_BYTES", 10):
            with self.assertRaises(stream_probe.StreamProtocolError):
                list(stream_probe.sse_data(io.BytesIO(b'data: ' + b'x' * 20 + b'\n\n')))

    def test_role_usage_not_tokens_reasoning_not_answer(self):
        o = stream_probe.Observation()
        o.consume('{"choices":[{"delta":{"role":"assistant"}}]}', 1)
        o.consume('{"choices":[],"usage":{"completion_tokens":3}}', 2)
        self.assertIsNone(o.summary()["client_first_model_delta_ms"])
        o.consume('{"choices":[{"delta":{"reasoning_content":"private"}}]}', 10)
        o.consume('{"choices":[{"delta":{"content":"Hi"}}]}', 20)
        o.consume('{"choices":[{"delta":{"content":"!"}}]}', 30)
        o.consume('[DONE]', 31)
        r = o.summary()
        self.assertEqual(r["client_first_model_delta_ms"], 10)
        self.assertEqual(r["client_first_visible_content_ms"], 20)
        self.assertEqual(r["model_delta_gaps_ms"], [10, 10])
        self.assertIsNone(r["usage"]["cached_prompt_tokens"])
        self.assertNotIn("private", json.dumps(r))

    def test_tool_fields_and_refusal(self):
        counts = stream_probe.classify_delta({"tool_calls":[{"id":"metadata-only","function":{"name":"lookup","arguments":"{}"}}]})
        self.assertEqual(counts["tool_argument_chars"], 2)
        self.assertEqual(counts["tool_name_chars"], 6)
        self.assertEqual(sum(stream_probe.classify_delta({"tool_calls":[{"id":"metadata-only"}]}).values()), 0)
        self.assertEqual(stream_probe.classify_delta({"refusal":"no"})["refusal_chars"], 2)

    def test_usage_and_server_metrics(self):
        u = stream_probe.usage_fields({"prompt_tokens": 8, "prompt_tokens_details":{"cached_tokens":0},
                                      "completion_tokens_details":{"reasoning_tokens":2}})
        self.assertEqual(u["cached_prompt_tokens"], 0)
        self.assertIsNone(u["completion_tokens"])
        self.assertEqual(stream_probe.metrics_fields({"queue_time_ms": 100, "private_prompt":"secret", "mean_itl_ms":None}),
                         {"queue_time_ms":100,"mean_itl_ms":None})

    def test_invalid_json_and_apierror(self):
        o = stream_probe.Observation()
        with self.assertRaises(stream_probe.StreamProtocolError):
            o.consume('not json', 1)
        with self.assertRaises(stream_probe.APIStreamError):
            o.consume('{"error":{"message":"PRIVATE"}}', 1)

    def test_payload_requires_bounded_single_output(self):
        base = {"messages":[{"role":"user","content":"test"}], "max_tokens":10}
        r = stream_probe.prepare_payload(base, "alias")
        self.assertTrue(r["stream_options"]["include_usage"])
        self.assertEqual(r["model"], "alias")
        for changed in (dict(base, n=2), {"messages":base["messages"]}, dict(base, max_tokens=0), dict(base, max_completion_tokens=5)):
            with self.assertRaises(ValueError):
                stream_probe.prepare_payload(changed, "alias")


class FakeSSEHandler(BaseHTTPRequestHandler):
    seen_authorization = None
    seen_traceparent = None
    redirect_target_calls = 0

    def log_message(self, *args):
        pass

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        type(self).seen_authorization = self.headers.get("Authorization")
        type(self).seen_traceparent = self.headers.get("traceparent")
        if self.path == "/redirect":
            self.send_response(307); self.send_header("Location", "/redirect-target"); self.end_headers(); return
        if self.path == "/redirect-target":
            type(self).redirect_target_calls += 1
        if self.path == "/unauthorized":
            self.send_response(401); self.end_headers(); self.wfile.write(b"DO-NOT-LOG-THIS-SECRET"); return
        self.send_response(200)
        self.send_header("Content-Type", "application/json" if self.path == "/json" else "text/event-stream")
        self.end_headers()
        if self.path == "/json":
            self.wfile.write(b'{}'); return
        if self.path == "/stall":
            time.sleep(.15)
            return
        records = [
            ': heartbeat\n\n',
            'data: {"choices":[{"index":0,"delta":{"role":"assistant"}}]}\n\n',
            'data: {"choices":[{"index":0,"delta":{"reasoning":"PRIVATE-REASONING"}}]}\n\n',
            'data: {"choices":[{"index":0,"delta":{"content":"PRIVATE-ANSWER"}}]}\n\n',
            'data: {"choices":[{"index":0,"delta":{},"finish_reason":"stop"}],"usage":{"prompt_tokens":100,"completion_tokens":5,"prompt_tokens_details":{"cached_tokens":64}},"metrics":{"queue_time_ms":10,"time_to_first_token_ms":3}}\n\n'
        ]
        if self.path != "/truncated":
            records.append('data: [DONE]\n\n')
        try:
            for record in records:
                self.wfile.write(record.encode()); self.wfile.flush()
                time.sleep(.001)
        except (BrokenPipeError, ConnectionResetError):
            pass


class HTTPIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeSSEHandler)
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        cls.payload = stream_probe.prepare_payload({"messages":[{"role":"user","content":"PRIVATE-PROMPT"}],"max_tokens":8}, "fixture")

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=2)

    def test_real_local_sse_consumption(self):
        result = stream_probe.probe_once(self.base + "/ok", self.payload, key="TEST-KEY", trace=True)
        self.assertTrue(result["success"])
        self.assertEqual(result["usage"]["cached_prompt_tokens"], 64)
        self.assertGreaterEqual(result["client_first_visible_content_ms"], result["client_first_model_delta_ms"])
        self.assertGreaterEqual(result["client_stream_complete_ms"], result["client_last_model_delta_ms"])
        for private in ("PRIVATE-PROMPT", "PRIVATE-REASONING", "PRIVATE-ANSWER", "TEST-KEY"):
            self.assertNotIn(private, json.dumps(result))
        self.assertEqual(FakeSSEHandler.seen_authorization, "Bearer TEST-KEY")
        self.assertRegex(FakeSSEHandler.seen_traceparent, r"^00-[0-9a-f]{32}-[0-9a-f]{16}-01$")

    def test_missing_done_is_failed(self):
        result = stream_probe.probe_once(self.base + "/truncated", self.payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "MissingDone")

    def test_http_error_redacts_body(self):
        result = stream_probe.probe_once(self.base + "/unauthorized", self.payload)
        self.assertEqual(result["http_status"], 401)
        self.assertNotIn("DO-NOT-LOG", json.dumps(result))

    def test_redirect_does_not_leak_auth(self):
        FakeSSEHandler.redirect_target_calls = 0
        result = stream_probe.probe_once(self.base + "/redirect", self.payload, key="TEST-KEY")
        self.assertEqual(result["http_status"], 307)
        self.assertEqual(FakeSSEHandler.redirect_target_calls, 0)

    def test_wrong_content_type_is_failed(self):
        result = stream_probe.probe_once(self.base + "/json", self.payload)
        self.assertEqual(result["error_type"], "StreamProtocolError")

    def test_socket_timeout_is_failed(self):
        result = stream_probe.probe_once(self.base + "/stall", self.payload, timeout=.02)
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error_type"])

    def test_probe_cli_writes_redacted_report(self):
        with tempfile.TemporaryDirectory() as d:
            payload_path = Path(d) / "payload.json"; payload_path.write_text(json.dumps(self.payload))
            output_path = Path(d) / "probe.json"
            cp = subprocess.run([sys.executable, str(ROOT / "scripts/stream_probe.py"),
                                 "--base-url", self.base, "--model", "fixture", "--payload", str(payload_path),
                                 "--repeat", "2", "--out", str(output_path)], capture_output=True, text=True, timeout=10)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            data = json.loads(output_path.read_text())
            self.assertEqual(data["completed_attempts"], 2)
            self.assertNotIn("PRIVATE-ANSWER", output_path.read_text())


class BenchTests(unittest.TestCase):
    def args(self, *extra):
        return bench_sweep.parser().parse_args(["--model","ORG/PINNED-TOKENIZER","--served-model-name","alias","--out","experiment", *extra])

    def test_saturation_has_cap_and_infinite_rate(self):
        r = bench_sweep.make_runs(self.args("--concurrency", "1,2"))
        self.assertEqual(len(r), 2)
        argv = r[1]["argv"]
        self.assertEqual(argv[argv.index("--max-concurrency") + 1], "2")
        self.assertEqual(argv[argv.index("--request-rate") + 1], "inf")

    def test_arrival_has_no_client_cap(self):
        r = bench_sweep.make_runs(self.args("--mode", "arrival", "--rates", ".5,1"))
        self.assertNotIn("--max-concurrency", r[0]["argv"])
        self.assertEqual(r[0]["argv"][r[0]["argv"].index("--request-rate") + 1], "0.5")

    def test_tokenizer_and_alias_not_confused(self):
        argv = bench_sweep.make_runs(self.args())[0]["argv"]
        self.assertEqual(argv[argv.index("--model") + 1], "ORG/PINNED-TOKENIZER")
        self.assertEqual(argv[argv.index("--served-model-name") + 1], "alias")
        self.assertNotIn("--save-detailed", argv)

    def test_prefix_dataset_uses_correct_family(self):
        argv = bench_sweep.make_runs(self.args("--dataset", "prefix_repetition"))[0]["argv"]
        self.assertIn("--prefix-repetition-prefix-len", argv)
        self.assertNotIn("--random-input-len", argv)

    def test_exact_flag_preflight(self):
        runs = [{"argv":["vllm","bench","serve","--model","x","--max-concurrency","2"]}]
        self.assertEqual(bench_sweep.missing_flags(runs, "--model-extra --max-concurrency-extra"), ["--max-concurrency","--model"])
        self.assertEqual(bench_sweep.missing_flags(runs, "options: --model MODEL, --max-concurrency N"), [])

    def test_prevent_accidental_cloud_key_forwarding(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY":"CLOUD-KEY"}, clear=True):
            self.assertNotIn("OPENAI_API_KEY", bench_sweep.child_environment())
        with patch.dict(os.environ, {"OPENAI_API_KEY":"CLOUD-KEY","VLLM_API_KEY":"LOCAL-KEY"}, clear=True):
            self.assertEqual(bench_sweep.child_environment()["OPENAI_API_KEY"], "LOCAL-KEY")

    def test_run_count_guard(self):
        with self.assertRaises(ValueError):
            bench_sweep.make_runs(self.args("--repeats", "100"))

    def test_default_dry_run_without_vllm(self):
        with tempfile.TemporaryDirectory() as d:
            cp = subprocess.run([sys.executable, str(ROOT / "scripts/bench_sweep.py"),
                                 "--model","NOT/DOWNLOADED","--served-model-name","alias", "--out", d,
                                 "--concurrency","1"], capture_output=True, text=True, timeout=10)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertTrue((Path(d)/"plan.json").is_file())
            self.assertFalse((Path(d)/"execution.json").exists())
            self.assertIn("No requests sent", cp.stdout)

    @unittest.skipUnless(os.name == "posix", "local executable fixture uses POSIX permissions")
    def test_execute_with_stub_cli_not_a_gpu_benchmark(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); bindir=root/"bin"; bindir.mkdir(); out=root/"results"
            args = self.args("--concurrency","1","--num-prompts","2")
            runs = bench_sweep.make_runs(args)
            flags = sorted({arg for r in runs for arg in r["argv"][3:] if arg.startswith("--")})
            fixture = bindir/"vllm"
            fixture.write_text(f'#!{sys.executable}\n' +
                'import sys,json,os\nfrom pathlib import Path\na=sys.argv[1:]\n' +
                f'if "--help" in a:\n print({" ".join(flags)!r}); sys.exit(0)\n' +
                'p=Path(a[a.index("--result-dir")+1])/a[a.index("--result-filename")+1]\n' +
                'p.write_text(json.dumps({"synthetic_test_fixture":True,"expected_key":os.environ.get("OPENAI_API_KEY")=="LOCAL-KEY"}))\n')
            fixture.chmod(0o700)
            env=dict(os.environ, PATH=str(bindir)+os.pathsep+os.environ.get("PATH",""),
                     VLLM_API_KEY="LOCAL-KEY", OPENAI_API_KEY="DO-NOT-FORWARD")
            command=[sys.executable, str(ROOT/"scripts/bench_sweep.py"), "--model","FIXTURE", "--served-model-name","alias",
                     "--out",str(out),"--concurrency","1","--num-prompts","2"]
            dry=subprocess.run(command, capture_output=True, text=True, env=env, timeout=10)
            self.assertEqual(dry.returncode,0,dry.stderr)
            cp=subprocess.run(command+["--execute"], capture_output=True, text=True, env=env, timeout=10)
            self.assertEqual(cp.returncode,0,cp.stderr)
            self.assertEqual(json.loads((out/"execution.json").read_text())["runs"][0]["status"],"cli_completed")
            self.assertTrue(json.loads((out/"run-01.json").read_text())["expected_key"])
            self.assertNotIn("LOCAL-KEY", (out/"plan.json").read_text())
            duplicate=subprocess.run(command+["--execute"],capture_output=True,text=True,env=env,timeout=10)
            self.assertNotEqual(duplicate.returncode,0)

    def test_cli_run_timeout(self):
        with tempfile.TemporaryDirectory() as d:
            result=bench_sweep.run_cli([sys.executable,"-c","import time; time.sleep(2)"],Path(d)/"log.txt",.05,dict(os.environ))
            self.assertEqual(result["status"],"timeout")


class AuditAndPackageTests(unittest.TestCase):
    def test_missing_audit_command_is_nonfatal(self):
        self.assertEqual(audit_env.run_readonly(["THIS_COMMAND_DOES_NOT_EXIST_TEST_999"],1)["status"],"not_installed")

    def test_package_structure(self):
        result=validate_skill.validate(ROOT)
        self.assertTrue(result["ok"],result["errors"])

    @unittest.skipUnless(os.name == "posix", "Bash launcher is POSIX-only")
    def test_launcher_only_plans_by_default(self):
        env=dict(os.environ,MODEL="FIXTURE/NO-DOWNLOAD",MODEL_REVISION="0123456789abcdef")
        cp=subprocess.run(["bash",str(ROOT/"scripts/serve_single.sh")],env=env,capture_output=True,text=True,timeout=5)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertIn("No server started",cp.stdout)


    @unittest.skipUnless(os.name == "posix", "Bash launcher is POSIX-only")
    def test_launcher_rejects_english_documentation_placeholders(self):
        # Translation must preserve the guard against executing example values.
        for model, revision in (
            ("ORG/EXACT-MODEL", "0123456789abcdef"),
            ("FIXTURE/NO-DOWNLOAD", "EXACT-COMMIT"),
        ):
            with self.subTest(model=model, revision=revision):
                env = dict(os.environ, MODEL=model, MODEL_REVISION=revision)
                result = subprocess.run(
                    ["bash", str(ROOT / "scripts/serve_single.sh")],
                    env=env, capture_output=True, text=True, timeout=5,
                )
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("Replace example placeholders", result.stderr)
                self.assertNotIn("Planned command", result.stdout)



if __name__ == "__main__":
    unittest.main()
