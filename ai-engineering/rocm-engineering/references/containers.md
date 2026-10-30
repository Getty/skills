# Containers, device injection and reproducible images

Evidence baseline: 2026-10-30. Validate the selected ROCm and container-toolkit versions against the actual host. This file concerns native Linux containers; WSL and Windows require their own supported integration paths.

## Contents

- [Separate host and image responsibilities](#separate-host-and-image-responsibilities)
- [Choose a device-injection method](#choose-a-device-injection-method)
- [Use a minimal launch](#use-a-minimal-launch)
- [Handle identity and rootless execution](#handle-identity-and-rootless-execution)
- [Add resources only for a demonstrated need](#add-resources-only-for-a-demonstrated-need)
- [Build and validate an image](#build-and-validate-an-image)
- [Diagnose container-only failures](#diagnose-container-only-failures)

## Separate host and image responsibilities

| Host supplies | Image supplies | Joint contract |
| --- | --- | --- |
| Kernel, GPU driver, device nodes, hardware/firmware | ROCm userspace, framework, application and extensions | Driver/runtime compatibility and architecture coverage |
| Container runtime and device policy | User/group execution context | Permission to open the selected devices |
| Storage, CPU, RAM, network and topology | Workload configuration | Sufficient resources and measured performance |

A container cannot repair an uninitialized host GPU or change its ISA. Conversely, installing a new SDK on the host need not update the runtime loaded inside an image. Diagnose those independently.

Choose an AMD or framework-published image whose documented hardware, framework and ROCm tuple matches the task. Record the repository, tag and resolved digest. Tags are convenient selectors; a digest identifies the bytes used. Pin application dependencies as well, because an unbounded package install at container startup defeats image reproducibility.

## Choose a device-injection method

AMD documents both [manual device passthrough and the Container Runtime Toolkit](https://rocm.docs.amd.com/en/latest/install/docker-containers.html). For manual Linux access, `/dev/kfd` supplies the compute interface and selected DRM render nodes identify the exposed GPUs. Passing all of `/dev/dri` grants broader device access. The documented `seccomp=unconfined` option is optional; assess it only when the workload needs blocked operations.

For a managed runtime that supports CDI, use the [AMD CDI guide](https://instinct.docs.amd.com/projects/container-toolkit/en/latest/container-runtime/cdi-guide.html). Install the toolkit using its own versioned instructions, generate the device specification during host setup, and validate it against the actual hardware. Regenerate it after changing devices or partition configuration. Inspect available entries with:

```bash
amd-ctk cdi list
```

Use an entry returned on that system, such as `amd.com/gpu=0`, rather than assuming numbering. CDI injection does not require `--runtime=amd`. The separate `amd-container-runtime` route has its own configuration and `AMD_VISIBLE_DEVICES` convention. Do not mix the two mechanisms merely because both appear in examples.

The [toolkit workload guide](https://instinct.docs.amd.com/projects/container-toolkit/en/latest/container-runtime/running-workloads.html) documents current Docker, Podman and containerd integrations. Support for shorthand `--gpus` flags is runtime/version dependent; the presence of NVIDIA-oriented examples elsewhere does not establish AMD support in an installed runtime.

## Use a minimal launch

After choosing a digest-pinned image containing `rocminfo` and an observed CDI entry:

```bash
: "${ROCM_IMAGE:?Set a verified digest-pinned image}"
: "${AMD_CDI_DEVICE:?Set a device returned by amd-ctk cdi list}"
docker run --rm --device "$AMD_CDI_DEVICE" "$ROCM_IMAGE" rocminfo
```

For manual passthrough, first map the desired PCI device to its render node. Then set `AMD_RENDER_NODE` to that observed path. This discovery-only example uses the current user's identity and the device-node groups:

```bash
: "${ROCM_IMAGE:?Set a verified digest-pinned image}"
: "${AMD_RENDER_NODE:?Set the observed render-node path}"
test -c /dev/kfd
test -c "$AMD_RENDER_NODE"
docker run --rm \
  --device /dev/kfd \
  --device "$AMD_RENDER_NODE" \
  --user "$(id -u):$(id -g)" \
  --group-add "$(stat -c %g /dev/kfd)" \
  --group-add "$(stat -c %g "$AMD_RENDER_NODE")" \
  "$ROCM_IMAGE" rocminfo
```

This is a Linux template, not a universal image command. If the selected image lacks `rocminfo`, use its documented device query. Do not label the image unsupported merely because a diagnostic executable is absent.

For an application launch, replace the final query with its explicit command and add only required mounts, ports and resource settings. Mount input models read-only when the application only reads them. Use a separate writable cache/output directory with deliberate ownership. Bind a local service to a local endpoint unless remote exposure is requested.

## Handle identity and rootless execution

The process inside the container needs actual device access, not merely a group with the same name. Compare numeric group IDs and effective supplementary groups. On rootless runtimes, also inspect user namespaces and device policy; root inside the namespace is not host root.

AMD's workload guide describes Podman's `--group-add keep-groups` approach for passing host supplementary groups in rootless operation. Check the selected Podman/OCI-runtime combination and verify permissions from inside the actual process. Do not “fix” rootless access by globally changing device modes or running every application as privileged.

A visibility environment variable selects devices for a cooperative process. It is not an access-control boundary against code that can open other exposed devices. For tenant isolation, enforce device exposure and the appropriate VM/container security design. Passing only selected render nodes is a concrete access decision, while runtime-level scheduling and hardware partitioning require separate evaluation.

## Add resources only for a demonstrated need

| Setting | Reason to consider it | Verify |
| --- | --- | --- |
| Shared memory size | Data-loader multiprocessing or collectives exhaust `/dev/shm` | Actual usage, process failures and peak workload |
| IPC sharing | A documented cross-process communication requirement | Scope of sharing and whether a private enlarged segment suffices |
| Memory-lock limits | Registered/pinned memory path requires it | Error and library requirement, host capacity |
| NUMA-related permissions | Affinity calls are blocked | Exact denied syscall and measured benefit |
| Debug capabilities | An authorized profiler/debugger requires them | Tool requirements; remove for normal operation |
| Host networking | A measured networking or rendezvous requirement | Necessary ports and interference with other services |

Do not inherit `--privileged`, host PID namespace, host networking, unconfined seccomp and unlimited limits from a benchmark command without understanding each one. A small isolated reproduction should establish whether a permission or resource is the cause.

## Build and validate an image

Keep the Dockerfile, base-image digest, dependency lock, target architectures and application commit together. Use a build stage for compilers when possible. Preserve all runtime libraries required by compiled extensions; a successful builder-stage import does not prove the final image contains them.

Architecture-specific packages reduce size but constrain deployment. If an image is intended for several GPU families, include the required targets and test them individually. An OCI CPU-platform label such as `linux/amd64` describes the CPU platform, not AMD GPU ISA coverage.

Separate build-time and run-time validation:

1. Build-time: dependency resolution, imports that do not require a GPU, wheel metadata and executable/library presence.
2. GPU canary: enumeration and numerical smoke test on each supported target.
3. Application: representative model, precision and extension paths.
4. Operational: startup/shutdown, concurrent requests, memory cleanup, restart and health checks.

Store the result against the image digest and host tuple. A GPU-less CI build is useful but cannot claim hardware correctness. Use independent small deployment canaries before replacing a working fleet image.

## Diagnose container-only failures

Compare host and container observations side by side: driver/runtime versions, visible devices, effective identity, library search paths, mounted directories and resource limits. Start from the same image without optional extensions. If host execution works but the image fails, investigate missing devices, numeric groups, unsupported image architecture or conflicting bundled libraries before replacing the host driver.

If a framework update unexpectedly removes HIP support, inspect package provenance and dependency resolution. If only the application fails, reduce to its first failing custom operator. If all containers lose the GPU after a host update, revalidate host driver loading and any stale CDI specification. Keep each diagnosis tied to a reproducible layer.
