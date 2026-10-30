# Kubernetes, schedulers, virtualization, and isolation

Evidence checked: 2026-10-30. AMD GPU Operator release documentation currently identifies version 1.5.1. Its `main` documentation is explicitly a development branch; use a release-matched chart, CRD, operand images, and support matrix.

## Contents

- [Choose the isolation and allocation model](#choose-the-isolation-and-allocation-model)
- [Deploy Kubernetes GPU support](#deploy-kubernetes-gpu-support)
- [Use DRA deliberately](#use-dra-deliberately)
- [Manage partitioning](#manage-partitioning)
- [Qualify virtual machines](#qualify-virtual-machines)
- [Integrate Slurm](#integrate-slurm)
- [Validate the complete service](#validate-the-complete-service)

## Choose the isolation and allocation model

| Mechanism | Purpose | What it does not establish |
| --- | --- | --- |
| `ROCR_VISIBLE_DEVICES` / `HIP_VISIBLE_DEVICES` | Select devices for cooperating processes | A boundary against an application that changes its environment |
| Device-node access and container policy | Restrict which GPU devices a container can open | A separate kernel or automatic fair scheduling |
| Whole-GPU allocation | Assign a device exclusively under scheduler policy | Enforcement if broad host device access bypasses the scheduler |
| Compute/memory partitioning | Expose supported logical GPU configurations | Universal tenant isolation, every partition combination, or extra physical VRAM |
| PCIe passthrough | Give a VM an assigned device | Sharing a single physical function among arbitrary guests |
| Supported SR-IOV | Expose vendor-supported virtual functions | Support on every Radeon/Instinct board or every hypervisor |

AMD explicitly warns that environment visibility masks do not isolate untrusted applications. Use the device-access and virtualization mechanisms appropriate to the threat model, and test the resulting access from inside the workload. [GPU isolation techniques](https://rocm.docs.amd.com/en/latest/reference/system-optimization/gpu-isolation.html).

## Deploy Kubernetes GPU support

Establish a working native Linux node first. Then choose who owns the kernel driver: the operating-system image or the operator. Avoid two controllers independently upgrading the same driver. Record the compatible GPU, OS/kernel, container runtime, Kubernetes/OpenShift, operator, driver, and ROCm userspace versions.

The operator can manage driver deployment, device allocation components, node labels, metrics, and health functions. Individual features have narrower support than the operator's general hardware list; for example, the 1.5.1 compatibility table lists Debian 12 without driver management. Verify the selected row instead of extrapolating from a supported Ubuntu deployment. [AMD GPU Operator release documentation](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/).

For traditional device-plugin allocation, request the resource actually advertised by the node. This fragment belongs under a container in an existing Pod template:

```yaml
resources:
  requests:
    cpu: "4"
    memory: 8Gi
  limits:
    cpu: "4"
    memory: 8Gi
    amd.com/gpu: 1
```

CPU/memory values are illustrative workload limits, not ROCm requirements. Kubernetes derives the extended-resource request from its limit when omitted. A claim for one advertised GPU resource can mean a logical partition, depending on device-plugin configuration; it does not necessarily mean an entire board. Inspect node capacity/allocatable and the operator's resource-naming strategy. [Device Plugin](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/device_plugin/device-plugin.html).

Use node labels/affinity to constrain architecture and capacity, tolerations for the intended GPU pool, and quotas to prevent accidental exhaustion. Pin workload images by digest. Supply CPU cores, memory, shared memory, model storage, and networking suitable for the application rather than assuming a GPU resource request configures them.

Read-only checks:

```bash
kubectl get nodes -o wide
kubectl get deviceconfigs -A
kubectl get pods -n kube-amd-gpu -o wide
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

Adapt the namespace to the actual installation. Inspect the chosen node and pending Pod using `kubectl describe`; distinguish missing resources, taints, image failures, and runtime device failures before changing the operator.

## Use DRA deliberately

Operator 1.5.1 documents Dynamic Resource Allocation as an alternative to the device plugin. It requires appropriate Kubernetes DRA support, an installed host driver, and a CDI-capable container runtime. The same `DeviceConfig` cannot enable both allocation paths. Workloads move from extended-resource limits to `ResourceClaim`/`ResourceClaimTemplate`; that is an application deployment migration, not merely an operator toggle. [Released DRA guide](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/dra/dra-driver.html).

Verify the release's exact Kubernetes API versions and feature-gate requirements; 1.32/1.33-era examples must not be copied unchanged into every later cluster. Inspect published `ResourceSlices`, claim allocation, and node preparation. Test claim deletion, Pod rescheduling, and node failure. Sharing must have an explicit fairness, memory, and failure-isolation policy; DRA's ability to represent sharing does not create hardware-enforced isolation by itself.

## Manage partitioning

Compute partition modes and memory partition modes are separate dimensions. Supported combinations depend on GPU, firmware, driver, and virtualization mode. Query available profiles on the target and retain the existing profile before making a change. For supported hardware, a physical GPU may enumerate as several logical devices; re-count resources and update mappings after partition changes. [AMD SMI partition model](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/conceptual/partition.html).

Plan partition changes as maintenance: drain affected workloads, account for GPU-consuming system agents, apply the selected profile, restart/reconcile enumeration components, validate resource counts and smoke workloads, then return the node to service. The operator's Device Config Manager documents such a workflow. Do not blanket-replace system Pod tolerations from a copied command; preserve existing policy and apply only the reviewed additions needed by this cluster. [DCM partition workflow](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/dcm/applying-partition-profiles.html).

Test whether a supposedly exclusive logical resource shares HBM domains, cache, reset behavior, or bandwidth with another resource. Choose partition sizes against observed per-job peak allocations, including workspaces and communication, and measure interference before offering capacity guarantees.

## Qualify virtual machines

Record the exact host and guest OS/kernel, hypervisor version, GPU SKU, physical-function and guest driver, firmware bundle, VF count, and partition mode. Confirm the combination in the selected [ROCm compatibility matrix](https://rocm.docs.amd.com/en/docs-10.1.0/compatibility/compatibility-matrix.html). Verify any required GPU Virtualization/GIM package and distribution/licensing terms for the selected product; never infer entitlement or support from the availability of SR-IOV in PCI configuration space.

Test IOMMU grouping and device assignment using the hypervisor's supported method. Preserve a management path if the only display GPU is assigned away. Inside the guest, validate device identity, memory size, framework support, and collective topology. A guest may intentionally omit host partition details. Do not promise VM live migration, suspend/resume, peer access, or GPU reset recovery unless that combination explicitly supports them and has been validated.

Cloud instances require the provider's guest image and driver contract as well as AMD compatibility. A provider's advertised aggregate GPU memory still needs application sharding and topology checks.

## Integrate Slurm

Use the installed Slurm release's GRES documentation, GPU autodetection plugin, cgroup/device enforcement, and accounting support. Map GPUs to CPUs/NUMA nodes, validate `slurmd -G`, and test an allocated job's visible devices. Bind one rank per assigned device deliberately; do not overwrite scheduler visibility masks with physical host indices.

**Migration trap:** the retrieved stable Slurm `gres.conf` documentation still describes `AutoDetect=rsmi` as requiring the ROCm SMI library, while current ROCm packaging has moved to AMD SMI. Installing `amd-smi` does not prove that an older Slurm binary can load its autodetection/accounting dependency. Check Slurm build options, loaded libraries, and release-specific AMD support before migrating the node image. A feature seen only on Slurm `master` is not an installed-release capability. [Slurm GRES configuration](https://slurm.schedmd.com/gres.conf.html); [GRES verification](https://slurm.schedmd.com/gres.html).

## Validate the complete service

Require evidence for allocation, computation, isolation, recovery, and telemetry separately. Test a job that requests one device, one that requests several, and a job that should be denied GPU access. Verify resource release after cancellation. Confirm the intended devices return healthy after a controlled restart, and avoid injecting hardware faults into active shared service nodes.

Document the rollout unit and rollback: driver/image, operator configuration, scheduler configuration, and partition profile. A successful Pod launch is only the first acceptance criterion.
