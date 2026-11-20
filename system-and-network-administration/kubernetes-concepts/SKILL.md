---
name: kubernetes-concepts
description: Use when reasoning about Kubernetes itself — control plane, resource relationships, networking, storage, RBAC — independent of any client library.
user-invocable: true
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
model: sonnet
---

# Kubernetes — Concepts and Traps

Kubernetes itself, independent of client library and distribution. The resource model
is assumed known; this holds where agents get it wrong. Typed objects in Perl: skill
`perl-io-k8s-kubernetes-classes` on top. A project that talks to the API or builds
images keeps its own skill for that.

## Ownership and selectors

- Selectors are the only wiring: Deployment → ReplicaSet → Pod via
  `.spec.selector.matchLabels`, Service → Pod via `.spec.selector`, NetworkPolicy →
  Pod via `podSelector`. A label typo raises no error, it matches nothing — prove the
  match with `kubectl get pods -l <key>=<value>`.
- A workload's `.spec.selector` is immutable and must match its Pod template labels;
  changing it means recreating the Deployment, StatefulSet or DaemonSet.
- Owner references are the deletion chain: deleting a Deployment garbage-collects its
  ReplicaSets and their Pods. Change the owner, never the owned object — edits to an
  owned object are lost at the next rollout, and a deleted Pod comes straight back from
  the template. Find the owner:
  `kubectl get pod <name> -o jsonpath='{.metadata.ownerReferences}'`.

## Networking

A short Service name resolves only in the caller's own namespace:

```
my-svc                          → my-svc.<current-ns>.svc.cluster.local
my-svc.other-ns                 → my-svc.other-ns.svc.cluster.local
my-svc.other-ns.svc.cluster.local  → full FQDN
```

- Per-Pod DNS (`pod-0.my-svc.ns.svc.cluster.local`) exists only for a StatefulSet whose
  `serviceName` names a headless Service (`clusterIP: None`, DNS returns all Pod IPs).
- A Service without endpoints is a selector or readiness fault — a Pod failing its
  readinessProbe leaves the endpoints. Check
  `kubectl get endpointslices -l kubernetes.io/service-name=<svc>` and that
  `targetPort` is the container's listening port before suspecting the CNI.
- Once a NetworkPolicy selects a Pod for a direction, everything it does not allow
  there is dropped. Egress policies must allow DNS (UDP and TCP 53 to CoreDNS).

## Storage

- ReadWriteOnce (RWO, most block storage) is a single node. A Deployment with an RWO
  claim needs `strategy.type: Recreate`: RollingUpdate starts the new Pod first, and on
  another node it hangs on a Multi-Attach error. RWX (NFS, CephFS) spans nodes; ROX
  spans nodes read-only.
- Replicas that each need their own disk: a StatefulSet with `volumeClaimTemplates`,
  never a Deployment sharing one claim.
- Reclaim `Delete` destroys the volume with its PVC; dynamic PVs inherit the
  StorageClass's policy (default `Delete`). Before deleting a claim whose data
  matters, switch the PV to `Retain`:
  `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'`.
- `hostPath` is one Node's directory — avoid it in production. `emptyDir` dies with
  the Pod.

## RBAC

- Test as the subject — your own kubeconfig is usually cluster-admin. ServiceAccounts
  are namespaced:
  `kubectl auth can-i <verb> <resource> -n <ns> --as=system:serviceaccount:<ns>:<name>`.
- `apiGroups` takes the group without version: `""` for core, then `apps`, `batch`,
  `networking.k8s.io`. Read groups, scope and served versions from
  `kubectl api-resources`, never from memory.
- `get` grants neither `list` nor `watch`; listing or an informer needs all three.
  Subresources need their own rule: `pods/log`, `pods/exec`, `pods/portforward`,
  `<resource>/scale`, `<resource>/status`.
- A RoleBinding grants only in its namespace, even to a ClusterRole. Cluster-scoped
  objects (Nodes, PVs, StorageClasses, CRDs) need a ClusterRoleBinding.
- Set `automountServiceAccountToken: false` where a Pod never calls the API; the
  token is mounted otherwise.

## Debugging order

Status, then `describe` and events, then logs, then a shell:

```bash
kubectl get pods -o wide                    # Pod status + Node + IP
kubectl describe pod <name>                 # Events, conditions, scheduling
kubectl logs <pod> [-c container] [-f]      # Container logs
kubectl logs <pod> --previous               # Logs from crashed container
kubectl exec -it <pod> -- /bin/sh           # Shell into container
kubectl port-forward svc/<name> 8080:80     # Local access to Service
kubectl get events --sort-by=.lastTimestamp  # Cluster events
kubectl top pods                            # Resource usage (requires metrics-server)
kubectl auth can-i <verb> <resource>        # RBAC check
```

- `Pending` (not scheduled): resource requests, node capacity, taints, PVC binding.
- `CrashLoopBackOff`: `kubectl logs --previous`, probe config.
- `ImagePullBackOff`: image name, registry auth, `imagePullSecrets`.
- `Evicted` (Node under pressure): resource limits, node conditions.
- `Terminating` stuck: finalizers block deletion —
  `kubectl get pod <name> -o json | jq .metadata.finalizers`. Fix the controller the
  finalizer waits for; stripping it by hand skips that cleanup.

## References

- Writing a workload spec — rollout, probes, shutdown, init and sidecar containers,
  resources and QoS, placement, labels, exposing traffic (Ingress vs Gateway API),
  CRDs and operators: [references/patterns.md](references/patterns.md).

## Related

`kubernetes-rke2` (the distribution), `kubernetes-cilium-concepts` (CNI, kube-proxy
replacement, Gateway API, LB-IPAM, CiliumNetworkPolicy, Hubble), `kubernetes-gpu`,
`storage-engineering` (storage choice, CSI, recovery, etcd backups).
