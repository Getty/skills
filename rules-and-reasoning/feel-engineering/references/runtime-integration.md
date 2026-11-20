# Runtime integration

## Define a narrow boundary

Separate source text, parser mode, typed input context, dialect, runtime options,
and output/diagnostic handling. Compile/cache expression plans only when the engine
supports that safely. Include source, dialect, function provider, and parser/runtime
version in compilation cache keys.

Bind application values through the engine API. Do not create expressions by
concatenating names, strings, or numeric literals from untrusted data. Input binding
avoids quote/escape mistakes and keeps logic versioning separate from case data.
Apply a deliberate size/depth limit for expressions and collection inputs when
execution is exposed to arbitrary users.

## Handle the result envelope

Distinguish parse failure, evaluation failure, returned null, returned false, and
a valid value with warnings. Preserve warning severity/type/location if the engine
provides them. Decide at the host level which diagnostics make a decision unusable;
do not rely on a generic truthiness test.

For a Boolean policy check, require a Boolean true when the application contract
means that only an explicitly satisfied condition allows continuation. Keep the
separate diagnostic reason so that an invalid expression is not mislabeled as an
ordinary failed condition.

## Integrate one documented engine at a time

[feelin](https://github.com/nikku/feelin) documents `evaluate` and `unaryTest`
returning `{value, warnings}`. Its unary-test example binds the implicit operand
as `?`. The bundled helper targets that interface, not every FEEL package.
Other engines may expose compiled expressions, typed result classes, or separate
error collections. Write an explicit adapter for them.

Pass an existing absolute module file to the bundled helper; it does not install
or download an engine. A Node module is executable code, so use the package/version
already chosen for the task. The helper runs local fixtures and serializable
results; it is not a sandbox for arbitrary third-party engine code.

## Preserve execution limits and purity

FEEL is suited to expressions, but the host controls resource use and extensions.
Bound expensive nested iterations, regex operations, and external function calls.
Do not advertise general sandbox guarantees just because the language lacks ordinary
assignment syntax. Running a custom function can escape any assumptions about pure
calculation if the host permits it.

Use supplied reference time and data snapshots for reproducibility. Keep downstream
actions outside expression evaluation. Record engine options and extensions with
stored results, and test the actual input conversion layer rather than only a
playground expression with hand-built values.
