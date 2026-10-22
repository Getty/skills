# External components and reproducible firmware

## Evaluate the component boundary

Use a built-in component when it implements the needed device contract. An [external component](https://esphome.io/components/external_components/) adds or replaces build/runtime code; a YAML package composes configuration. Both can change behavior, but their review surfaces differ. Neither is made trustworthy by being linked from a forum.

Record repository owner, component path, supported ESPHome/platform versions, license, update history and unresolved issues affecting the exact hardware. Inspect code and configuration before running validation: external sources can be fetched and imported during configuration processing. Treat arbitrary build code with the same care as other executable dependencies.

## Make a repeatable dependency set

Pin the ESPHome release and a supported immutable external-source revision or reviewed release tag. Record the resolved commit even when the declared ref is a tag. Avoid using a moving development branch as an unrecorded production dependency. Limit the `components` list to what is required, and verify the source path and refresh behavior against the current schema.

For packages, inspect substitutions, merged sections, on-boot actions, network services, hidden control entities and any remote includes. Two individually reasonable packages can collide on IDs, pins or timing. Keep local secrets out of distributed examples and commit only the intended non-secret configuration.

Maintain a build record:

- ESPHome release, platform/framework and resolved dependency revisions.
- Board/chip/flash identity and the intended device identifier.
- Non-secret source configuration plus secret-name requirements.
- Build artifact digest and successful validation/compile output.
- Actual flashed version, acceptance observations and recovery image location.

This is a reproducibility checklist, not a requirement to expose private credentials or binary images publicly.

## Add a component incrementally

Compile the baseline without the new component, then add one capability. Separate a schema/import failure from compiler failure, link-size overflow, boot failure and incorrect physical behavior. Keep a minimal reproducible configuration and sanitized logs for an upstream issue.

Exercise reconnect, unavailable-device behavior, invalid payloads and malformed input where applicable. Do not validate a parser solely with one happy-path capture. For custom actuators, review bounds and command ownership before connecting a real load.

If a dependency breaks on upgrade, reproduce with the recorded known-good versions and check current upstream resolution. A temporary version pin needs a reason and an exit condition. Do not keep a whole fleet on an old release indefinitely because one historical issue once existed.
