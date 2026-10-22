![skills](assets/github.png)

# Getty/skills

**The skills that don't belong to any one project.**

Skills installed with [skilletor](https://github.com/Getty/skilletor) live in
whichever repo owns them — a Perl module keeps its Perl skill, a Kubernetes cluster repo
keeps its cluster skill. This repo holds the rest: knowledge that applies across many
projects and has no single home of its own.

**The rule: a skill lives here only as long as nothing else claims it.** The moment a
skill belongs to one specific project, it moves there and this repo drops the link.

## The groups

| Group | Skills | What it holds |
|---|---|---|
| [authoring](authoring/README.md) | 5 | Skills about skills — writing them, mining them out of existing code, compressing them, the library's own rules, and the agent team that consumes them |
| [claude](claude/README.md) | 4 | Working with Claude itself — headless spawning, talking across running sessions, routing work across model tiers, building plugins for Claude Code |
| [codex](codex/README.md) | 3 | Working with Codex — non-interactive runs, reaching threads that already exist, building plugins |
| [compliance-and-governance](compliance-and-governance/README.md) | 14 | EU law for an AI platform as engineering work — GDPR, AI Act, data and IP, consumer and B2B contracts, billing and tax, accessibility, content safety, cybersecurity, with German overlays |
| [databases](databases/README.md) | 1 | Data stores themselves — PostgreSQL with pgvector and Apache AGE: schema, indexes, retrieval, consistency, recovery |
| [development](development/README.md) | 2 | Engineering practice independent of language — debugging discipline, project scaffolding |
| [git](git/README.md) | 2 | How repositories are used, and how commit messages are written |
| [hermes-agent](hermes-agent/README.md) | 1 | NousResearch Hermes Agent — extending the agent, its messaging gateway, and the Desktop and Dashboard surfaces |
| [javascript](javascript/README.md) | 2 | React and Electron — renderer, library choice and React Flow; main/preload boundary, security, packaging and updates |
| [perl](perl/README.md) | 12 | House style, object systems including Mojo::Base, typing, DSL sugar, async, MCP, XS and Alien, release tooling |
| [smart-home](smart-home/README.md) | 9 | Home Assistant with its automations and extensions, FRITZ!Box, radio networks, device families, ESPHome and MQTT, cameras and media |
| [social-media](social-media/README.md) | 2 | LinkedIn and Twitch — platform mechanics, content practice, and the DACH legal duties that have no US equivalent |
| [storytold-craft](storytold-craft/README.md) | 16 | Operating the Storytold Craft editors as an agent — one skill per application, its CLI and MCP server, plus an overview that routes between them |
| [system-and-network-administration](system-and-network-administration/README.md) | 13 | Machines, networks, hosting, storage, containers, Kubernetes, TLS and PKI, job queues, admin automation |

Each group README describes every skill in it: what it covers, and when to load it.

## Every skill

### [authoring](authoring/README.md)

| Skill | What it is |
|---|---|
| [getty-agent-team](authoring/getty-agent-team/SKILL.md) | A whole multi-agent setup for a project: subagents, briefing-preloaded skills, karr wiring |
| [getty-skill-library](authoring/getty-skill-library/SKILL.md) | Where a skill lives, what it is named, and how an edit reaches its consumers |
| [skill-authoring](authoring/skill-authoring/SKILL.md) | Writing a SKILL.md that fires from its description and then gets followed |
| [skill-compressor](authoring/skill-compressor/SKILL.md) | Shrinking or merging skills without losing the rules that drive behaviour |
| [skill-mining](authoring/skill-mining/SKILL.md) | Deriving skill content from a codebase instead of inventing conventions |

### [claude](claude/README.md)

| Skill | What it is |
|---|---|
| [claude-code-plugin-engineering](claude/claude-code-plugin-engineering/SKILL.md) | Building a Claude Code plugin: picking the mechanism, hooks and mods, loading, distribution |
| [claude-cross-session](claude/claude-cross-session/SKILL.md) | One Claude session starting, watching and messaging another |
| [claude-headless](claude/claude-headless/SKILL.md) | Driving Claude Code as a subprocess: `-p`, JSON, permissions, the multi-turn channel |
| [model-routing](claude/model-routing/SKILL.md) | Choosing a model tier by the hardest dimension the work routinely hits |

### [codex](codex/README.md)

| Skill | What it is |
|---|---|
| [codex-cross-session](codex/codex-cross-session/SKILL.md) | Reaching an existing Codex thread: the queue, the daemon, `--remote` |
| [codex-headless](codex/codex-headless/SKILL.md) | `codex exec` non-interactively: JSONL events, sandboxes, resuming a thread |
| [codex-plugin-engineering](codex/codex-plugin-engineering/SKILL.md) | Building a Codex plugin: package formats, hooks, MCP, and what each host actually runs |

### [compliance-and-governance](compliance-and-governance/README.md)

| Skill | What it is |
|---|---|
| [eu-ai-act](compliance-and-governance/eu-ai-act/SKILL.md) | AI Act classification and duties per feature, actor and model version, on the 2026-amended timeline |
| [eu-ai-data-ip](compliance-and-governance/eu-ai-data-ip/SKILL.md) | Rights for training data, RAG sources, scraping, model weights and outputs, with German copyright overlay |
| [eu-platform-accessibility](compliance-and-governance/eu-platform-accessibility/SKILL.md) | EAA and BFSG scope, then complete user journeys tested with keyboard and screen reader |
| [eu-platform-agent-assurance](compliance-and-governance/eu-platform-agent-assurance/SKILL.md) | Compliance evidence, release gates and agent permissions for agent-built software |
| [eu-platform-billing-tax](compliance-and-governance/eu-platform-billing-tax/SKILL.md) | Metering, VAT and OSS, German e-invoicing, retention, credits and payment-regulation screening |
| [eu-platform-business-contracts](compliance-and-governance/eu-platform-business-contracts/SKILL.md) | B2B contracts in both directions: DPAs, SLAs, vendor terms, Data Act switching, promises as controls |
| [eu-platform-compliance](compliance-and-governance/eu-platform-compliance/SKILL.md) | The entry point: platform profile, applicability register, routing to the specialists |
| [eu-platform-consumer-commerce](compliance-and-governance/eu-platform-consumer-commerce/SKILL.md) | B2C checkout, pricing, withdrawal, cancellation and digital-product remedies, German adapter |
| [eu-platform-content-safety](compliance-and-governance/eu-platform-content-safety/SKILL.md) | DSA classification, notices and appeals, minors, government orders, German DDG and youth law |
| [eu-platform-cybersecurity](compliance-and-governance/eu-platform-cybersecurity/SKILL.md) | Security controls and evidence, NIS2/BSIG and CRA scope, incident reporting clocks |
| [eu-platform-data-governance](compliance-and-governance/eu-platform-data-governance/SKILL.md) | Data lifecycle: inventory, retention, deletion, RAG and training provenance, vendors and transfers |
| [eu-platform-privacy](compliance-and-governance/eu-platform-privacy/SKILL.md) | GDPR roles, lawful bases, DPIA, rights, automated decisions and breaches, BDSG overlay |
| [eu-platform-regulatory-watch](compliance-and-governance/eu-platform-regulatory-watch/SKILL.md) | Versioned legal source register and change-impact review, without self-installed monitoring |
| [eu-platform-tracking-marketing](compliance-and-governance/eu-platform-tracking-marketing/SKILL.md) | Cookies, SDKs, consent and direct marketing — device access, processing and contact kept apart |

### [databases](databases/README.md)

| Skill | What it is |
|---|---|
| [postgres-vector-graph](databases/postgres-vector-graph/SKILL.md) | PostgreSQL 18 with pgvector and Apache AGE: relational, vector and graph in one system |

### [development](development/README.md)

| Skill | What it is |
|---|---|
| [feedback-loop-debugging](development/feedback-loop-debugging/SKILL.md) | A six-phase discipline for hard bugs, built on a fast pass/fail signal |
| [getty-create-software](development/getty-create-software/SKILL.md) | Scaffolding a new project from the signals that reveal its type |

### [git](git/README.md)

| Skill | What it is |
|---|---|
| [getty-git-commit-style](git/getty-git-commit-style/SKILL.md) | Imperative summary, one body line per change, and the `Changes` file every repo keeps: format, entries, version line |
| [getty-git-usage](git/getty-git-usage/SKILL.md) | Linear history: rebase over merge, and `--force-with-lease` after it |

### [hermes-agent](hermes-agent/README.md)

| Skill | What it is |
|---|---|
| [hermes-plugin-engineering](hermes-agent/hermes-plugin-engineering/SKILL.md) | Extending Hermes Agent: tools, hooks, middleware, providers, gateway adapters, Desktop |

### [javascript](javascript/README.md)

| Skill | What it is |
|---|---|
| [electron-desktop-engineering](javascript/electron-desktop-engineering/SKILL.md) | Electron apps: process and trust boundaries, validated IPC, packaging, signing and updates |
| [react-ecosystem-engineering](javascript/react-ecosystem-engineering/SKILL.md) | React and its library ecosystem: state, SSR/RSC, forms, UI systems, React Flow, testing |

### [perl](perl/README.md)

| Skill | What it is |
|---|---|
| [getty-perl-core](perl/getty-perl-core/SKILL.md) | The base layer: module loading, object-system choice, errors, subroutine shape |
| [getty-perl-distribution](perl/getty-perl-distribution/SKILL.md) | Creating a CPAN distribution, or bringing an existing one to house standard |
| [getty-perl-moo](perl/getty-perl-moo/SKILL.md) | Moo classes and roles — roles for reuse, inheritance only for a stable is-a |
| [getty-perl-moose](perl/getty-perl-moose/SKILL.md) | The same shape in Moose, plus `make_immutable` on every class |
| [getty-perl-sugar](perl/getty-perl-sugar/SKILL.md) | Designing a new DSL: registering keywords, a metadata registry, one shared runner |
| [getty-perl-typing](perl/getty-perl-typing/SKILL.md) | Whether a project needs a type system at all, and which one is cheap here |
| [perl-alien](perl/perl-alien/SKILL.md) | `Alien::Build`: providing a C library or tool through CPAN |
| [perl-io-async-future](perl/perl-io-async-future/SKILL.md) | PEVANS-style async Perl, and its unforgiving lifetime rules |
| [perl-mcp](perl/perl-mcp/SKILL.md) | Building an MCP server in Perl with `MCP::Server` |
| [perl-mojo](perl/perl-mojo/SKILL.md) | `Mojo::Base` as an object system, plus the `Mojo::*` toolkit around it |
| [perl-release-dist-ini](perl/perl-release-dist-ini/SKILL.md) | Dist::Zilla for any distribution, independent of the author bundle |
| [perl-xs](perl/perl-xs/SKILL.md) | The Perl/C boundary, and why an `.xs` file is C behind a preprocessor |

### [smart-home](smart-home/README.md)

| Skill | What it is |
|---|---|
| [fritzbox-operator](smart-home/fritzbox-operator/SKILL.md) | FRITZ!Box APIs, HA integrations, DECT heating and buttons, presence, provider firmware, recovery |
| [home-assistant-automations](smart-home/home-assistant-automations/SKILL.md) | Automations as behaviour contracts: triggers, restart-safe timing, manual override, presence, Assist and MCP |
| [home-assistant-hacs](smart-home/home-assistant-hacs/SKILL.md) | HACS and community extensions: when to install, frontend debugging, updates and recovery |
| [home-assistant-operator](smart-home/home-assistant-operator/SKILL.md) | Running Home Assistant: install types, backups, registries, APIs, recorder, performance, integration development |
| [smart-home-architecture](smart-home/smart-home-architecture/SKILL.md) | The whole home: subsystems and control ownership, protocol and hub choice, purchasing, migration |
| [smart-home-devices](smart-home/smart-home-devices/SKILL.md) | Exact-model integration decisions for Hue, Shelly, Tuya, SONOFF, Aqara and other device families |
| [smart-home-esphome-mqtt](smart-home/smart-home-esphome-mqtt/SKILL.md) | ESPHome firmware and MQTT: boards, API and OTA, broker design, discovery, availability |
| [smart-home-radio](smart-home/smart-home-radio/SKILL.md) | Zigbee, ZHA, Zigbee2MQTT, Matter and Thread, BLE, Z-Wave — commissioning, diagnosis, migration |
| [smart-home-video-media](smart-home/smart-home-video-media/SKILL.md) | Cameras, NVRs, doorbells, go2rtc and Frigate, TVs and media players in Home Assistant |

### [social-media](social-media/README.md)

| Skill | What it is |
|---|---|
| [linkedin](social-media/linkedin/SKILL.md) | Formats, how distribution actually works, and the DACH legal duties |
| [twitch](social-media/twitch/SKILL.md) | Channel operation end to end: encoder, growth, chat, monetization, moderation |

### [storytold-craft](storytold-craft/README.md)

| Skill | What it is |
|---|---|
| [storytold-artcraft](storytold-craft/storytold-artcraft/SKILL.md) | ArtCraft's generative workflow and Rust client — an integration boundary, no operator CLI |
| [storytold-artcraftx](storytold-craft/storytold-artcraftx/SKILL.md) | The experimental ArtCraft-X Tauri app: its IPC boundary and development lifecycle |
| [storytold-cadcraft](storytold-craft/storytold-cadcraft/SKILL.md) | CADCraft drawings: geometry commands, units and layouts, DXF/DWG interchange |
| [storytold-craft](storytold-craft/storytold-craft/SKILL.md) | The overview: which product owns which task, and where the twelve CLIs differ |
| [storytold-craft-launcher](storytold-craft/storytold-craft-launcher/SKILL.md) | Installing, updating and locating the Craft applications |
| [storytold-deckcraft](storytold-craft/storytold-deckcraft/SKILL.md) | DeckCraft presentations: slides, shapes, layouts, export coverage |
| [storytold-designcraft](storytold-craft/storytold-designcraft/SKILL.md) | DesignCraft page layout: spreads, frames, threaded stories, publication export |
| [storytold-effectcraft](storytold-craft/storytold-effectcraft/SKILL.md) | EffectCraft motion graphics: compositions, keyframes, expressions, render jobs |
| [storytold-filmcraft](storytold-craft/storytold-filmcraft/SKILL.md) | FilmCraft timelines: media health, tick-based timing, export jobs |
| [storytold-gridcraft](storytold-craft/storytold-gridcraft/SKILL.md) | GridCraft spreadsheets: formulas, calculation oracles, round-trip fidelity |
| [storytold-lightcraft](storytold-craft/storytold-lightcraft/SKILL.md) | LightCraft photo catalogs: RAW development, originals and sidecars, exports |
| [storytold-pdfcraft](storytold-craft/storytold-pdfcraft/SKILL.md) | PdfCraft: reading, organizing, annotating, editing and securing existing PDFs |
| [storytold-photocraft](storytold-craft/storytold-photocraft/SKILL.md) | PhotoCraft layered raster images: PSD/PSB, masks, smart objects, exports |
| [storytold-soundcraft](storytold-craft/storytold-soundcraft/SKILL.md) | SoundCraft multitrack sessions: media, routing, automation, offline bounces |
| [storytold-vectorcraft](storytold-craft/storytold-vectorcraft/SKILL.md) | VectorCraft documents: object queries, live appearance, artboard export |
| [storytold-wordcraft](storytold-craft/storytold-wordcraft/SKILL.md) | WordCraft documents: styles, sections, tracked changes, export |

### [system-and-network-administration](system-and-network-administration/README.md)

| Skill | What it is |
|---|---|
| [docker](system-and-network-administration/docker/SKILL.md) | Docker images and Compose stacks: build, wiring, operation, recovery — routed by task |
| [docker-engine-api](system-and-network-administration/docker-engine-api/SKILL.md) | Writing a client that speaks the Engine HTTP API instead of shelling out to `docker` |
| [docker-registry](system-and-network-administration/docker-registry/SKILL.md) | Registries and pull-through caches: protocol, clients, mirror fallback, retention |
| [gearman](system-and-network-administration/gearman/SKILL.md) | Gearman job queues: server, clients and workers, persistence, protocol, retries and idempotency |
| [hetzner-operator](system-and-network-administration/hetzner-operator/SKILL.md) | Hetzner Cloud, Robot and managed hosting: networking, VPN access, storage, recovery, cost |
| [kubernetes-cilium-concepts](system-and-network-administration/kubernetes-cilium-concepts/SKILL.md) | Cilium replacing CNI, kube-proxy, policy, encryption and ingress at once |
| [kubernetes-concepts](system-and-network-administration/kubernetes-concepts/SKILL.md) | Control plane, resource hierarchy, and how ownership and selectors tie it together |
| [kubernetes-gpu](system-and-network-administration/kubernetes-gpu/SKILL.md) | The four layers that must line up before a pod can use a GPU |
| [kubernetes-rke2](system-and-network-administration/kubernetes-rke2/SKILL.md) | RKE2 and K3s as one topic, with the differences named where they exist |
| [rex](system-and-network-administration/rex/SKILL.md) | Perl Rex automation: Rexfiles, transports, idempotency, and operating it safely |
| [storage-engineering](system-and-network-administration/storage-engineering/SKILL.md) | Storage from the access contract and failure model: block, file, object, HA, DR, backup, Kubernetes, sizing |
| [ssl-tls-pki](system-and-network-administration/ssl-tls-pki/SKILL.md) | TLS, public Web PKI, private CAs, ACME and mTLS — design, operation, debugging |
| [vllm-operator](system-and-network-administration/vllm-operator/SKILL.md) | Running vLLM on small GPU hardware: capacity, caching, benchmarking, tuning (German) |

## Using this repo

An owner name on its own is enough — it resolves to that owner's `skills` repo:

```bash
skilletor add Getty --project       # github.com/Getty/skills, as source `getty`
skilletor available getty           # see what's on offer
skilletor install getty-perl-moo@getty getty-git-usage@getty --project
```

With a local checkout, point the same source name at it in your user config
(`~/.claude/skilletor.json`); it then overrides the git source and is read
directly on every sync:

```json
{ "sources": { "getty": { "local": "<checkout>" } } }
```

The same files also ship as a plugin for Claude Code (`.claude-plugin/`) and for
Codex (`.codex-plugin/`) — three distribution routes, one source of truth.

## Naming

`getty-` prefixed skills **prescribe** — a house convention chosen over other valid
options, or the API of Getty's own software. Unprefixed skills are **reference** —
documentation of how a public tool or protocol behaves, equally true for anyone.
The full naming and placement rules are themselves a skill:
[getty-skill-library](authoring/getty-skill-library/SKILL.md).

## Adding a skill

Write it where it's used first. Only pull it in here once a second, unrelated project
needs the same knowledge — that's the signal it has outgrown a single home. The
workbench for that is the [authoring group](authoring/README.md): `skill-authoring`
for the content, `getty-skill-library` for placement, naming, and the way an edit
reaches its consumers.

A skill has to be listed in four places — its group README, the group table and the
skill table above, and both plugin manifests. `bin/check-listings` holds them against
the directories and names what is missing; it exits non-zero, so it fits a hook or CI.

Consumers hold installed copies, not these files. Edit a skill here, and a consuming
project picks the change up at its next `skilletor sync`; an edit made to the installed
copy is overwritten by that same sync. `getty-skill-library` has the details.

## Licence

Copyright (c) 2026 Torsten Raudssus.

This is free software; you can redistribute it and/or modify it under the terms of the
[Artistic License 2.0](LICENSE) — the Perl licence, because that is where most of this
came from.
