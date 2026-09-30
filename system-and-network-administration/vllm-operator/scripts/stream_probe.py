#!/usr/bin/env python3
"""Sequential Chat-Completions SSE probe; measures deltas, NOT exact token ITL.

Sends real inference requests. Saves timing/count metadata, not prompts or output
text. Timeout is socket inactivity, not a hard end-to-end deadline. There are no
retries, implicit proxies, redirect following, or disabled TLS verification.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.client import HTTPException
import json
import math
from pathlib import Path
import secrets
import statistics
import time
from typing import BinaryIO, Iterator, Any
from urllib.error import HTTPError, URLError
from urllib.request import Request
from _common import (api_key, http_opener, positive_float, positive_int,
                     read_json, validate_url, write_json)

MAX_LINE_BYTES = 1024 * 1024
MAX_EVENT_BYTES = 2 * 1024 * 1024
MAX_STREAM_BYTES = 32 * 1024 * 1024


class StreamProtocolError(ValueError):
    pass


class MissingDone(StreamProtocolError):
    pass


class APIStreamError(StreamProtocolError):
    pass


def sse_data(stream: BinaryIO) -> Iterator[str]:
    """Parse UTF-8 SSE data records. Comments/IDs/events do not become tokens.

    Strictly require a blank line to terminate a data record. CRLF is supported.
    An unfinished final data record is rejected instead of silently accepted.
    """
    lines: list[str] = []
    event_bytes = total_bytes = 0
    first = True
    while True:
        raw = stream.readline(MAX_LINE_BYTES + 1)
        if not raw:
            if lines:
                raise StreamProtocolError("unfinished SSE record")
            return
        total_bytes += len(raw)
        event_bytes += len(raw)
        if len(raw) > MAX_LINE_BYTES or event_bytes > MAX_EVENT_BYTES or total_bytes > MAX_STREAM_BYTES:
            raise StreamProtocolError("SSE size limit exceeded")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise StreamProtocolError("invalid UTF-8") from exc
        if first:
            text = text.removeprefix("\ufeff")
            first = False
        text = text.rstrip("\r\n")
        if not text:
            if lines:
                yield "\n".join(lines)
            lines = []
            event_bytes = 0
            continue
        if text.startswith(":"):
            continue
        field, sep, value = text.partition(":")
        if sep and value.startswith(" "):
            value = value[1:]
        if field == "data":
            lines.append(value if sep else "")


def text_chars(value: Any) -> int:
    if isinstance(value, str):
        return len(value)
    if isinstance(value, list):
        # Only recognized textual content parts. Audio/image chunks are out of scope.
        return sum(len(item["text"]) for item in value
                   if isinstance(item, dict) and isinstance(item.get("text"), str))
    return 0


def classify_delta(delta: dict) -> dict[str, int]:
    content = text_chars(delta.get("content"))
    reasoning = text_chars(delta.get("reasoning_content")) + text_chars(delta.get("reasoning"))
    refusal = text_chars(delta.get("refusal"))
    tool_args = tool_names = 0
    calls = delta.get("tool_calls")
    if calls is not None and not isinstance(calls, list):
        raise StreamProtocolError("invalid tool_calls shape")
    functions = []
    for call in calls or []:
        if isinstance(call, dict) and isinstance(call.get("function"), dict):
            functions.append(call["function"])
    if isinstance(delta.get("function_call"), dict):
        functions.append(delta["function_call"])
    for function in functions:
        tool_args += text_chars(function.get("arguments"))
        tool_names += text_chars(function.get("name"))
    return {"content_chars": content, "reasoning_chars": reasoning,
            "refusal_chars": refusal, "tool_argument_chars": tool_args,
            "tool_name_chars": tool_names}


def valid_count(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def usage_fields(usage: dict) -> dict:
    prompt_details = usage.get("prompt_tokens_details")
    completion_details = usage.get("completion_tokens_details")
    return {
        "prompt_tokens": valid_count(usage.get("prompt_tokens")),
        "completion_tokens": valid_count(usage.get("completion_tokens")),
        "total_tokens": valid_count(usage.get("total_tokens")),
        "cached_prompt_tokens": valid_count(prompt_details.get("cached_tokens")) if isinstance(prompt_details, dict) else None,
        "reasoning_tokens": valid_count(completion_details.get("reasoning_tokens")) if isinstance(completion_details, dict) else None,
    }


def metrics_fields(metrics: dict) -> dict:
    allowed = ("time_to_first_token_ms", "generation_time_ms", "queue_time_ms",
               "mean_itl_ms", "tokens_per_second")
    selected = {}
    for name in allowed:
        value = metrics.get(name)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0:
            selected[name] = value
        elif name in metrics:
            selected[name] = None
    return selected


class Observation:
    def __init__(self) -> None:
        self.saw_done = False
        self.data_events = 0
        self.delta_times: list[float] = []
        self.content_times: list[float] = []
        self.char_counts = {name: 0 for name in classify_delta({})}
        self.usage = usage_fields({})
        self.server_metrics: dict = {}
        self.finish_reason: str | None = None

    def consume(self, data: str, elapsed_ms: float) -> None:
        self.data_events += 1
        if data.strip() == "[DONE]":
            self.saw_done = True
            return
        try:
            event = json.loads(data)
        except (json.JSONDecodeError, ValueError) as exc:
            raise StreamProtocolError("invalid JSON data record") from exc
        if not isinstance(event, dict):
            raise StreamProtocolError("SSE JSON must be an object")
        if event.get("error") is not None:
            raise APIStreamError("API returned a stream error; body omitted")
        if isinstance(event.get("usage"), dict):
            for key, value in usage_fields(event["usage"]).items():
                if value is not None:
                    self.usage[key] = value
        if isinstance(event.get("metrics"), dict):
            self.server_metrics.update(metrics_fields(event["metrics"]))
        choices = event.get("choices", [])
        if not isinstance(choices, list):
            raise StreamProtocolError("invalid choices shape")
        # The request is constrained to n == 1, so a single stream is measured.
        for choice in choices:
            if not isinstance(choice, dict) or choice.get("index", 0) != 0:
                continue
            reason = choice.get("finish_reason")
            if isinstance(reason, str):
                self.finish_reason = reason if reason in {"stop", "length", "tool_calls", "function_call", "content_filter"} else "other"
            delta = choice.get("delta", {})
            if not isinstance(delta, dict):
                raise StreamProtocolError("invalid delta shape")
            counts = classify_delta(delta)
            if sum(counts.values()) > 0:
                self.delta_times.append(elapsed_ms)
            if counts["content_chars"] > 0:
                self.content_times.append(elapsed_ms)
            for name, count in counts.items():
                self.char_counts[name] += count

    def summary(self) -> dict:
        gaps = [b - a for a, b in zip(self.delta_times, self.delta_times[1:])]
        return {
            "saw_done": self.saw_done,
            "data_event_count": self.data_events,
            "meaningful_delta_count": len(self.delta_times),
            "visible_content_delta_count": len(self.content_times),
            "client_first_model_delta_ms": self.delta_times[0] if self.delta_times else None,
            "client_first_visible_content_ms": self.content_times[0] if self.content_times else None,
            "client_last_model_delta_ms": self.delta_times[-1] if self.delta_times else None,
            "model_delta_gaps_ms": gaps,
            "mean_model_delta_gap_ms": statistics.fmean(gaps) if gaps else None,
            "max_model_delta_gap_ms": max(gaps) if gaps else None,
            "observed_character_counts": self.char_counts,
            "usage": self.usage,
            "server_metrics_if_present": self.server_metrics,
            "finish_reason": self.finish_reason,
        }


def prepare_payload(payload: Any, model: str) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("messages"), list) or not payload["messages"]:
        raise ValueError("payload needs a nonempty messages array")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model alias must not be empty")
    if payload.get("n", 1) != 1 or isinstance(payload.get("n", 1), bool):
        raise ValueError("probe only supports n=1")
    caps = [payload.get(k) for k in ("max_tokens", "max_completion_tokens") if k in payload]
    if len(caps) != 1 or valid_count(caps[0]) in {None, 0}:
        raise ValueError("specify exactly one positive max_tokens or max_completion_tokens budget")
    options = payload.get("stream_options", {})
    if not isinstance(options, dict):
        raise ValueError("stream_options must be an object")
    result = dict(payload)
    result.update(model=model, stream=True, n=1)
    result["stream_options"] = dict(options, include_usage=True)
    # Reject NaN, infinity or unserializable values before making a request.
    json.dumps(result, allow_nan=False)
    return result


def probe_once(url: str, payload: dict, *, key: str | None = None,
               timeout: float = 60, trace: bool = False, max_events: int = 100000) -> dict:
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}
    if key:
        headers["Authorization"] = "Bearer " + key
    traceparent = None
    if trace:
        traceparent = "00-" + secrets.token_hex(16) + "-" + secrets.token_hex(8) + "-01"
        headers["traceparent"] = traceparent
    body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    request = Request(url, data=body, headers=headers, method="POST")
    obs = Observation()
    status = error = header_ms = None
    start = time.perf_counter()
    try:
        with http_opener().open(request, timeout=timeout) as response:
            header_ms = (time.perf_counter() - start) * 1000
            status = response.status
            if response.headers.get_content_type() != "text/event-stream":
                raise StreamProtocolError("expected text/event-stream")
            for data in sse_data(response):
                obs.consume(data, (time.perf_counter() - start) * 1000)
                if obs.data_events > max_events:
                    raise StreamProtocolError("event count limit exceeded")
                if obs.saw_done:
                    break
            if not obs.saw_done:
                raise MissingDone("stream ended before [DONE]")
    except HTTPError as exc:
        status = exc.code
        error = "HTTPError"
        exc.close()
    except (OSError, URLError, ValueError, HTTPException) as exc:
        # No server body or exception message is logged: it may contain prompts or credentials.
        error = type(exc).__name__
    end_ms = (time.perf_counter() - start) * 1000
    result = obs.summary()
    result.update(
        http_status=status, error_type=error,
        protocol_ok=error is None and obs.saw_done,
        success=error is None and obs.saw_done and bool(obs.delta_times),
        client_headers_ms=header_ms, client_stream_complete_ms=end_ms,
        traceparent=traceparent,
    )
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-url", default="http://127.0.0.1:8000")
    p.add_argument("--model", required=True, help="served API alias, not necessarily tokenizer repo")
    p.add_argument("--payload", type=Path, required=True)
    p.add_argument("--repeat", type=positive_int, default=1)
    p.add_argument("--timeout", type=positive_float, default=60, help="socket inactivity seconds, not an absolute deadline")
    p.add_argument("--max-events", type=positive_int, default=100000)
    p.add_argument("--trace", action="store_true", help="send correlation traceparent; does not export a client span")
    p.add_argument("--allow-insecure-http", action="store_true")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    try:
        if a.repeat > 100:
            raise ValueError("repeat is capped at 100; use the official benchmark for load")
        if a.out.exists():
            raise ValueError("output already exists; choose a fresh result path")
        base = validate_url(a.base_url, base=True, allow_insecure_http=a.allow_insecure_http)
        payload = prepare_payload(read_json(a.payload), a.model)
        key = api_key()
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    results = []
    for i in range(a.repeat):
        result = probe_once(base + "/v1/chat/completions", payload, key=key,
                            timeout=a.timeout, trace=a.trace, max_events=a.max_events)
        result["sequence_number"] = i + 1
        results.append(result)
        if not result["success"]:
            break  # No automatic retry and no continued spend after an error.
    report = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "model_alias": a.model, "base_url": base,
        "requested_repeats": a.repeat, "completed_attempts": len(results),
        "measurements": results,
        "notes": [
            "Real requests, sequential only. First run is not guaranteed cold; cache is never reset here.",
            "Client timer starts immediately before HTTP request, including connect/send/wait/stream.",
            "Meaningful delta includes text, reasoning, refusal or tool name/arguments; role/usage/IDs alone are excluded.",
            "First-visible metric counts content only; actual UI rendering and reasoning-in-content need application-level validation.",
            "Delta gaps are NOT token ITLs; token counts and streaming chunk boundaries differ.",
            "Stream-complete is receipt/consumption through DONE, not TCP disconnect or only last generated token.",
            "No prompt, output text, key, or raw error body retained. Count fields missing from API remain null.",
            "Per-request server TTFT may exclude queue; do not conflate it with client timing.",
            "A traceparent correlates requests but this script exports no OpenTelemetry client span.",
            "Timeout is socket inactivity, not a hard total-duration limit. Outputs are explicitly token-budgeted."
        ]
    }
    try:
        write_json(a.out, report)
    except OSError:
        p.exit(1, "Requests completed but result file could not be created; no retries performed.\n")
    print(f"Wrote {len(results)} request observations to {a.out}; no prompt/output text stored.")
    return 0 if all(r["success"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
