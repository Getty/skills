#!/usr/bin/env python3
"""Run bounded ROCm PyTorch correctness checks; never silently pass on CPU/CUDA.

Exit 0: requested checks passed; 1: execution/correctness failure; 2: missing
prerequisite or invalid invocation. A pass is a narrow smoke test, not model
qualification, a performance benchmark, or official support certification.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def emit(status: str, **fields) -> None:
    print(json.dumps({"schema_version": 1, "status": status, **fields}, indent=2, default=str))


def worker(args: argparse.Namespace) -> int:
    try:
        import torch
        import torch.nn.functional as functional
    except ImportError as error:
        emit("prerequisite_missing", reason="PyTorch cannot be imported", error=str(error)[:1500])
        return 2
    hip_version = getattr(torch.version, "hip", None)
    if not hip_version:
        emit("wrong_backend", torch_version=torch.__version__, hip_version=hip_version,
             reason="This test requires a ROCm/HIP PyTorch build; CPU and NVIDIA CUDA do not qualify.")
        return 2
    if not torch.cuda.is_available():
        emit("device_unavailable", torch_version=torch.__version__, hip_version=hip_version)
        return 2
    count = torch.cuda.device_count()
    if args.device >= count:
        emit("invalid_device", requested=args.device, visible_devices=count)
        return 2
    torch.cuda.set_device(args.device)
    device = torch.device("cuda", args.device)
    dtype = getattr(torch, args.dtype)
    torch.manual_seed(17)
    n = args.size
    a_cpu = torch.randn(n, n + 3, dtype=torch.float32)
    b_cpu = torch.randn(n + 3, n - 1, dtype=torch.float32)
    # Reference uses the same rounded inputs, with higher-precision CPU accumulation.
    a = a_cpu.to(device=device, dtype=dtype)
    b = b_cpu.to(device=device, dtype=dtype)
    reference = a.cpu().double() @ b.cpu().double()
    result = a @ b
    torch.cuda.synchronize(device)
    tolerances = {"float32": (1e-3, 2e-3), "float16": (5e-3, 2e-2), "bfloat16": (5e-2, 2e-1)}
    rtol, atol = tolerances[args.dtype]
    if not bool(torch.isfinite(result).all().item()):
        raise RuntimeError("Matmul produced nonfinite values")
    torch.testing.assert_close(result.cpu().double(), reference, rtol=rtol, atol=atol)
    checks = ["selected_dtype_matmul_matches_cpu_reference"]
    # Basic FP32 autograd check. This does not validate a mixed-precision optimizer.
    x = a_cpu.to(device).detach().requires_grad_(True)
    loss = x.square().mean()
    loss.backward()
    torch.cuda.synchronize(device)
    expected_gradient = 2 * a_cpu / a_cpu.numel()
    torch.testing.assert_close(x.grad.cpu(), expected_gradient, rtol=1e-5, atol=1e-6)
    checks.append("fp32_autograd_matches_analytic_gradient")
    if args.sdpa:
        q_cpu, k_cpu, v_cpu = [torch.randn(1, 2, 17, 32) for _ in range(3)]
        q, k, v = [t.to(device=device, dtype=dtype) for t in (q_cpu, k_cpu, v_cpu)]
        attention = functional.scaled_dot_product_attention(q, k, v, dropout_p=0.0, is_causal=False)
        qr, kr, vr = [t.cpu().double() for t in (q, k, v)]
        expected_attention = torch.softmax((qr @ kr.transpose(-2, -1)) / (32 ** 0.5), dim=-1) @ vr
        torch.cuda.synchronize(device)
        torch.testing.assert_close(attention.cpu().double(), expected_attention, rtol=rtol, atol=atol)
        checks.append("sdpa_matches_cpu_math_reference_backend_not_forced")
    properties = torch.cuda.get_device_properties(device)
    emit("passed", torch_version=torch.__version__, hip_version=hip_version,
         device_index=args.device, device_name=properties.name,
         gfx_target=getattr(properties, "gcnArchName", None),
         dtype=args.dtype, matrix_shape=[n, n + 3, n - 1], checks=checks,
         rtol=rtol, atol=atol,
         limits="No model, torch.compile, graph, quantization, fused-kernel, mixed-precision-training or scaling certification.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--dtype", choices=("float32", "float16", "bfloat16"), default="float32")
    parser.add_argument("--size", type=int, default=127, help="Base matrix size (16..1024)")
    parser.add_argument("--sdpa", action="store_true", help="Also compare a tiny default SDPA operation with CPU math")
    parser.add_argument("--timeout", type=float, default=45, help="Worker wall-clock limit in seconds (0 < value <= 60)")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.device < 0 or not 16 <= args.size <= 1024 or not 0 < args.timeout <= 60:
        parser.error("Require device >= 0, 16 <= size <= 1024, and 0 < timeout <= 60")
    if args.worker:
        try:
            return worker(args)
        except Exception as error:
            emit("failed", error_type=type(error).__name__, error=str(error)[:3000])
            return 1
    command = [sys.executable, __file__, *sys.argv[1:], "--worker"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        emit("timeout", seconds=args.timeout, reason="Worker terminated; inspect driver and process state before retrying. This does not reset the GPU.")
        return 1
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode < 0 or not result.stdout.strip():
        emit("worker_failed", returncode=result.returncode)
        return 1
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
