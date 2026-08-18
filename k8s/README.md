# Kubernetes skills

Cluster and resource knowledge that isn't tied to any one language's client library —
plain reference, no Getty opinion baked in, so it carries no `getty-` prefix.

| Skill | Covers |
|---|---|
| [kubernetes-concepts](kubernetes-concepts/SKILL.md) | Kubernetes concepts, architecture, resource relationships, networking, storage, RBAC — the big picture without language-specific typing. |

Language-specific typed clients live next to their language, e.g. `getty-perl-kubernetes-classes`
under [perl/](../perl/README.md) — that one keeps the prefix because it documents Getty's
own `IO::K8s` module, not a public API. Load both when writing Kubernetes code in that
language.
