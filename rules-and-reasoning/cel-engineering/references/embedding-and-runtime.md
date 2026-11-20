# Embedding and runtime

## Separate configuration from requests

At configuration time, create the environment, parse the source, type-check it,
verify the expected result type, and prepare the executable program. At request
time, bind trusted values, evaluate, classify the result, and let the application
apply its decision. Keep source and profile metadata with checked artifacts.
[CEL overview](https://cel.dev/overview/cel-overview).

Build a cache key from source/revision, declarations, namespace/container, message
descriptors, extension versions, function overload definitions, and relevant options.
The same text checked under a different environment is not necessarily the same
program. Invalidate on contract changes rather than relying only on expression text.

## Match the implementation API

Current official Go examples use `cel.dev/cel-go/cel`; older code often uses
`github.com/google/cel-go/cel`. Select the module path for the pinned release and
avoid mixing imports and examples across versions. Prepared programs in the Go
implementation are designed for reuse, but verify concurrency assumptions for
custom host adapters and shared state.
[CEL Go README](https://github.com/cel-expr/cel-go/blob/master/README.md).

The Python example runner uses official `cel-expr-python` 0.1.3 with
`from cel_expr_python import cel`. This is a C++ wrapper, distinct from other
similarly named Python CEL packages. Its environment compiles expressions and
returns typed CEL values. Inspect `type()` and `value()` rather than Python
truthiness or equality alone.
[Python wrapper](https://github.com/cel-expr/cel-python/blob/main/README.md).

## Bind functions responsibly

Declare a custom function's overload signatures and bind a matching implementation.
Version its semantics. Keep it deterministic, side-effect-free, and bounded where
possible. If it uses external state, explicitly capture that state or document the
host extension's effects and replay limitations.

A safe expression grammar cannot make an arbitrary host function safe. Restrict
available functions for untrusted policy authors. Avoid exposing filesystem,
network, dynamic code execution, or broad object reflection merely for convenience.
Pre-fetch authoritative facts and pass a minimal evaluation context instead.

## Handle outcomes and lifecycle

Distinguish parse/check failure, runtime error, unknown, wrong type, and a valid
negative answer. A Boolean permission consumer must accept only a valid true
result. Preserve rich diagnostics internally without returning secrets to callers.

Manage memory/arena lifetime and compiled-program eviction under sustained load.
Keep request activations isolated. If serialized ASTs are accepted, validate their
origin, size, format/profile, and environment compatibility before executing them.
Serialization is interchange machinery, not a guarantee that arbitrary producers
share the same host functions or policy meaning.
