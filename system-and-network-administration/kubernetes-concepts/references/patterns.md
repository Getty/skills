# Kubernetes workload patterns

Read this when writing or reviewing a workload manifest — rollout, probes, shutdown,
init and sidecar containers, resources, placement, labels, exposure — or a CRD and the
controller behind it.

## Rolling updates (Deployment default)

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%   # How many can be down during update
    maxSurge: 25%          # How many extra Pods during update
```

A Deployment with a ReadWriteOnce claim uses `type: Recreate` instead (SKILL.md,
Storage).

## Health checks

```yaml
livenessProbe:    # Kill container if failing (restarts it)
  httpGet: { path: /healthz, port: 8080 }
  initialDelaySeconds: 10
  periodSeconds: 10
readinessProbe:   # Remove from Service if failing (no traffic)
  httpGet: { path: /ready, port: 8080 }
startupProbe:     # Protect slow-starting containers
  httpGet: { path: /healthz, port: 8080 }
  failureThreshold: 30
  periodSeconds: 10
```

## Graceful shutdown

1. Pod marked for deletion → removed from Service endpoints
2. `preStop` hook runs (e.g., `sleep 5` to drain connections)
3. `SIGTERM` sent to PID 1
4. `terminationGracePeriodSeconds` countdown (default 30s)
5. `SIGKILL` if still running

## Init and sidecar containers

Init containers run sequentially before the app containers start. Use them for waiting
on dependencies, database migrations, config generation, permission setup.

Sidecars (v1.29+): `restartPolicy: Always` on an init container makes it a sidecar. It
starts before and outlives the main container. Use for log shipping, proxies
(istio/envoy), metrics export.

## Resources and QoS

```yaml
resources:
  requests:    # Guaranteed. Used by scheduler for placement.
    cpu: "100m"      # 0.1 CPU core
    memory: "128Mi"
  limits:      # Maximum. OOM-killed if exceeded (memory). Throttled (CPU).
    cpu: "500m"
    memory: "256Mi"
```

QoS classes follow automatically from requests and limits:

- `Guaranteed`: requests == limits for all containers
- `Burstable`: at least one request set, not Guaranteed
- `BestEffort`: no requests/limits (first to be evicted)

## Placement

- `nodeSelector`: simple key-value match on Node labels.
- Affinity and anti-affinity: expressive rules, required or preferred, on Node or Pod
  level.
- Taints and tolerations: a Node repels every Pod that does not tolerate its taint.
- Topology spread: distribute Pods across zones or nodes.

## Recommended labels

The `app.kubernetes.io/*` set from the k8s.io conventions:

```yaml
app.kubernetes.io/name: myapp
app.kubernetes.io/instance: myapp-prod
app.kubernetes.io/component: frontend
app.kubernetes.io/part-of: platform
app.kubernetes.io/version: "1.2.3"
```

## Exposing traffic

```
Internet → Ingress/Gateway → Service → Pods
Internet → LoadBalancer Service → Pods
Internet → NodePort Service → Pods (not recommended for production)
```

Gateway API is the successor to Ingress. Ask the cluster which one it serves —
`kubectl get gatewayclass`, `kubectl get ingressclass` — before writing either.
Gateway API resources: `GatewayClass` → `Gateway` → `HTTPRoute`/`TCPRoute`/etc. A
LoadBalancer Service needs a cloud controller or, on bare metal, LB-IPAM; without one
its external IP stays `<pending>`. Cilium's Gateway and LB-IPAM: skill
`kubernetes-cilium-concepts`.

## CRDs and operators

A CustomResourceDefinition extends the API with a new resource type: OpenAPI v3
schema, versions, scope (Namespaced or Cluster). An operator is a CRD plus a controller
that reconciles it: watch → diff desired against actual → act → update status.

- `/status` is a separate update path: with the status subresource enabled, a
  controller writes `.status` through it, and status in a main-resource update is
  ignored. `/scale` is what the HPA reads.
- Applying a CRD and its first instances in one go fails with "no matches for kind".
  Wait first: `kubectl wait --for condition=established crd/<name>`.
