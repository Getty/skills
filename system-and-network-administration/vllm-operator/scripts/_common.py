"""Small stdlib-only helpers. No installs, implicit proxies, or redirects."""
from __future__ import annotations

import argparse
import ipaddress
import json
import math
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener


def positive_int(value: str) -> int:
    try:
        n = int(value)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if n <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return n


def nonnegative_int(value: str) -> int:
    try:
        n = int(value)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if n < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return n


def finite_float(value: str) -> float:
    try:
        n = float(value)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if not math.isfinite(n):
        raise argparse.ArgumentTypeError("must be finite, not NaN or infinity")
    return n


def positive_float(value: str) -> float:
    n = finite_float(value)
    if n <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return n


def nonnegative_float(value: str) -> float:
    n = finite_float(value)
    if n < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return n


def validate_url(url: str, *, base: bool = False,
                 allow_insecure_http: bool = False) -> str:
    """Allow HTTPS or loopback HTTP. Reject credentials, fragments, and queries."""
    if not isinstance(url, str) or any(ord(c) < 33 for c in url):
        raise ValueError("URL must not contain whitespace or control characters")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must be an absolute http(s) URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URL credentials are forbidden; use VLLM_API_KEY")
    if parsed.query or parsed.fragment:
        raise ValueError("URL query strings/fragments are not supported")
    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError("invalid URL port") from exc
    host = parsed.hostname.lower()
    try:
        local = ipaddress.ip_address(host).is_loopback
    except ValueError:
        local = host == "localhost"
    if parsed.scheme == "http" and not local and not allow_insecure_http:
        raise ValueError("remote HTTP needs --allow-insecure-http; prefer HTTPS or a local tunnel")
    if base and parsed.path not in {"", "/"}:
        raise ValueError("base URL must contain only scheme/host/port, not /v1 or an API path")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/") if base else parsed.path, "", ""))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def http_opener():
    # Default HTTPS handler keeps certificate verification enabled.
    return build_opener(ProxyHandler({}), NoRedirect())


def api_key() -> str | None:
    value = os.environ.get("VLLM_API_KEY")
    if value and any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError("VLLM_API_KEY contains invalid control characters")
    return value or None


def read_json(path: Path, max_bytes: int = 8 * 1024 * 1024) -> Any:
    with path.open("rb") as f:
        data = f.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("JSON input exceeds the configured size limit")
    def reject_nonfinite(value: str):
        raise ValueError("non-finite JSON number")
    return json.loads(data.decode("utf-8"), parse_constant=reject_nonfinite)


def private_text_file(path: Path):
    """Exclusive create; never overwrite an experiment or follow a target symlink."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    return os.fdopen(fd, "w", encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    # Serialize before creating a file, so invalid values leave no partial output.
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with private_text_file(path) as f:
        f.write(text)
