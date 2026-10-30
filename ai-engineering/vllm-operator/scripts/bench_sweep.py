#!/usr/bin/env python3
"""Plan safe vLLM bench serve sweeps. Only --execute sends requests or loads tokenizers.

Separate saturation (fixed concurrency, infinite offered rate) from arrival
(finite rate, no client concurrency cap). This wrapper does not claim to measure
application quality, reset caches, provision instances, or tune a server itself.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import shlex
import signal
import shutil
import subprocess
import time
from typing import Sequence
from _common import (api_key, positive_int, positive_float, nonnegative_int,
                     private_text_file, read_json, validate_url, write_json)


def csv_positive_ints(text: str) -> list[int]:
    values = [positive_int(value.strip()) for value in text.split(",")]
    if len(set(values)) != len(values):
        raise argparse.ArgumentTypeError("duplicate concurrency values")
    return values


def csv_positive_floats(text: str) -> list[float]:
    values = [positive_float(value.strip()) for value in text.split(",")]
    if len(set(values)) != len(values):
        raise argparse.ArgumentTypeError("duplicate request rates")
    return values


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", required=True, help="model repo/local tokenizer source; NOT just an arbitrary API alias")
    p.add_argument("--served-model-name", required=True, help="model name accepted by the server API")
    p.add_argument("--base-url", default="http://127.0.0.1:8000")
    p.add_argument("--mode", choices=("saturation", "arrival"), default="saturation")
    p.add_argument("--concurrency", type=csv_positive_ints, default=[1, 2, 4, 8])
    p.add_argument("--rates", type=csv_positive_floats, default=[.5, 1, 2])
    p.add_argument("--dataset", choices=("random", "prefix_repetition"), default="random")
    p.add_argument("--input-len", type=positive_int, default=1024)
    p.add_argument("--output-len", type=positive_int, default=128)
    p.add_argument("--prefix-len", type=positive_int, default=1024)
    p.add_argument("--suffix-len", type=positive_int, default=128)
    p.add_argument("--prefix-count", type=positive_int, default=4)
    p.add_argument("--num-prompts", type=positive_int, default=200)
    p.add_argument("--warmups", type=nonnegative_int, default=5)
    p.add_argument("--repeats", type=positive_int, default=1)
    p.add_argument("--seed", type=nonnegative_int, default=42)
    p.add_argument("--ttft-ms", type=positive_float, default=1500)
    p.add_argument("--tpot-ms", type=positive_float, default=80)
    p.add_argument("--e2e-ms", type=positive_float, default=20000)
    p.add_argument("--timeout-seconds", type=positive_float, default=1800,
                   help="maximum wall time per CLI run; on POSIX timeout kills its process group")
    p.add_argument("--save-detailed", action="store_true", help="SENSITIVE: official result may contain response/error text")
    p.add_argument("--allow-insecure-http", action="store_true")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--execute", action="store_true", help="explicitly authorize real load and possible billed GPU/tokenizer activity")
    return p


def make_runs(a: argparse.Namespace) -> list[dict]:
    settings: Sequence[int | float] = a.concurrency if a.mode == "saturation" else a.rates
    if len(settings) * a.repeats > 32:
        raise ValueError("more than 32 runs; split the experiment into deliberate smaller batches")
    root = a.out.resolve()
    runs = []
    for repetition in range(a.repeats):
        for setting in settings:
            name = f"run-{len(runs) + 1:02d}"
            filename = name + ".json"
            argv = ["vllm", "bench", "serve", "--backend", "openai-chat",
                    "--base-url", a.base_url, "--endpoint", "/v1/chat/completions",
                    "--model", a.model, "--served-model-name", a.served_model_name,
                    "--dataset-name", a.dataset, "--num-prompts", str(a.num_prompts),
                    "--seed", str(a.seed + repetition), "--num-warmups", str(a.warmups),
                    "--ignore-eos", "--percentile-metrics", "ttft,tpot,itl,e2el",
                    "--metric-percentiles", "50,90,95,99",
                    "--goodput", f"ttft:{a.ttft_ms:g}", f"tpot:{a.tpot_ms:g}", f"e2el:{a.e2e_ms:g}",
                    "--save-result", "--result-dir", str(root),
                    "--result-filename", filename, "--request-id-prefix", name + "-"]
            if a.dataset == "random":
                argv += ["--random-input-len", str(a.input_len),
                         "--random-output-len", str(a.output_len), "--random-prefix-len", "0"]
            else:
                argv += ["--prefix-repetition-prefix-len", str(a.prefix_len),
                         "--prefix-repetition-suffix-len", str(a.suffix_len),
                         "--prefix-repetition-num-prefixes", str(a.prefix_count),
                         "--prefix-repetition-output-len", str(a.output_len)]
            if a.mode == "saturation":
                argv += ["--request-rate", "inf", "--max-concurrency", str(setting)]
            else:
                argv += ["--request-rate", str(setting)]
            if a.save_detailed:
                argv += ["--save-detailed"]
            runs.append({"name": name, "repeat_index": repetition + 1,
                         "mode": a.mode, "setting": setting, "argv": argv,
                         "result_filename": filename, "log_filename": name + ".log"})
    return runs


def missing_flags(runs: list[dict], help_text: str) -> list[str]:
    available = set(re.findall(r"--[A-Za-z0-9][A-Za-z0-9_-]*", help_text))
    required = {part for run in runs for part in run["argv"][3:] if part.startswith("--")}
    return sorted(required - available)


def child_environment() -> dict[str, str]:
    env = dict(os.environ)
    # Do NOT accidentally send a cloud-provider key to a new vLLM host.
    env.pop("OPENAI_API_KEY", None)
    key = api_key()
    if key:
        env["OPENAI_API_KEY"] = key
    return env


def run_cli(argv: list[str], log_path: Path, timeout: float, env: dict[str, str]) -> dict:
    start = time.monotonic()
    with private_text_file(log_path) as log:
        process = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT,
                                   text=True, env=env, start_new_session=(os.name == "posix"))
        def stop(force: bool) -> None:
            try:
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGKILL if force else signal.SIGTERM)
                elif force:
                    process.kill()
                else:
                    process.terminate()
            except ProcessLookupError:
                pass
        try:
            code = process.wait(timeout=timeout)
            status = "cli_completed" if code == 0 else "cli_failed"
        except subprocess.TimeoutExpired:
            stop(force=True)
            code = process.wait()
            status = "timeout"
        except KeyboardInterrupt:
            stop(force=False)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                stop(force=True)
                process.wait()
            raise
    return {"status": status, "returncode": code, "wall_seconds": time.monotonic() - start}


def main() -> int:
    p = parser()
    a = p.parse_args()
    try:
        a.base_url = validate_url(a.base_url, base=True, allow_insecure_http=a.allow_insecure_http)
        if a.model.startswith("-") or a.served_model_name.startswith("-"):
            raise ValueError("model identifiers must not look like CLI flags")
        runs = make_runs(a)
        plan = {
            "schema": 1, "runs": runs,
            "run_timeout_seconds": a.timeout_seconds,
            "scheduled_benchmark_prompts": len(runs) * a.num_prompts,
            "nominal_requested_output_tokens_excluding_warmups": len(runs) * a.num_prompts * a.output_len,
            "notes": [
                "Plan only until --execute. No server is started, stopped, reset or reconfigured.",
                "Warmup/readiness/validation may issue additional requests beyond num-prompts.",
                "Synthetic text, fixed requested output with ignore_eos: NOT application quality or natural output distribution.",
                "Saturation limits active clients; arrival mode deliberately has no client concurrency cap.",
                "Cache state is NOT reset; equal seeds and warmups may produce reuse across runs. Control/cache-label it explicitly.",
                "Default SLO thresholds are EXAMPLE hypotheses in milliseconds, not measured recommendations.",
                "Actual offered rate, errors and client queue behavior must be checked in the versioned official results.",
                "Only VLLM_API_KEY is mapped to the benchmark child's OPENAI_API_KEY; keys are not in argv/plan.",
                "The wrapper does not alter official benchmark HTTP/redirect/proxy behavior; use a trusted direct endpoint.",
                "CLI success is not a passed SLO/quality gate. Review raw JSON and logs.",
                "Logs may contain internal paths/errors; --save-detailed additionally retains responses."
            ]
        }
        a.out.mkdir(parents=True, exist_ok=True, mode=0o700)
        plan_path = a.out / "plan.json"
        if plan_path.exists():
            if read_json(plan_path) != plan:
                raise ValueError("existing plan differs; use a new experiment directory")
        else:
            write_json(plan_path, plan)
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    print(f"Plan: {len(runs)} runs, {plan['scheduled_benchmark_prompts']} benchmark prompts plus possible warmups/tests.")
    for run in runs:
        print(shlex.join(run["argv"]))
    if not a.execute:
        print(f"No requests sent. Review {plan_path}; add --execute with identical parameters to run.")
        return 0
    if shutil.which("vllm") is None:
        p.exit(1, "vllm CLI is not installed. Plan retained; no requests sent.\n")
    occupied = [a.out / name for name in ("execution.json", "local-bench-help.txt")]
    occupied += [a.out / r[key] for r in runs for key in ("result_filename", "log_filename")]
    if any(path.exists() for path in occupied):
        p.exit(1, "Execution artifacts already exist; use a new experiment directory, no overwrite or automatic resume.\n")
    try:
        env = child_environment()
        help_result = subprocess.run(["vllm", "bench", "serve", "--help"],
                                     capture_output=True, text=True, encoding="utf-8",
                                     errors="replace", timeout=45, check=False, env=env)
        help_text = help_result.stdout + "\n" + help_result.stderr
        if help_result.returncode != 0:
            p.exit(1, "Local benchmark help failed; no load sent. Check the vLLM environment.\n")
        missing = missing_flags(runs, help_text)
        if missing:
            p.exit(1, "Unsupported or unavailable local flags: " + ", ".join(missing) + ". No load sent.\n")
        with private_text_file(a.out / "local-bench-help.txt") as f:
            f.write(help_text)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        p.exit(1, f"Preflight failed ({type(exc).__name__}); no load sent.\n")
    execution = {"utc": datetime.now(timezone.utc).isoformat(), "flag_check": "passed against local CLI help", "runs": []}
    interrupted = False
    try:
        for run in runs:
            outcome = run_cli(run["argv"], a.out / run["log_filename"], a.timeout_seconds, env)
            outcome["name"] = run["name"]
            outcome["result_file_exists"] = (a.out / run["result_filename"]).is_file()
            if outcome["status"] == "cli_completed" and not outcome["result_file_exists"]:
                outcome["status"] = "result_missing"
            execution["runs"].append(outcome)
            if outcome["status"] != "cli_completed":
                break
    except KeyboardInterrupt:
        interrupted = True
        execution["interrupted"] = True
    except OSError as exc:
        execution["error_type"] = type(exc).__name__
    finally:
        write_json(a.out / "execution.json", execution)
    ok = (not interrupted and len(execution["runs"]) == len(runs)
          and all(r["status"] == "cli_completed" for r in execution["runs"]))
    print("Execution finished; inspect actual JSON results, errors and quality gates. No SLO pass is inferred.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
