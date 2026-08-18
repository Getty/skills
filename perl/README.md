# Perl skills

Shared Perl knowledge, split by what kind of knowledge it is:

- **`getty-` prefixed** — prescribes something: a house convention chosen over other
  valid options, or the API of software Getty itself wrote. Follow it as given.
- **No prefix** — a reference: how a public module or protocol actually behaves. True
  for anyone using that technology, Getty or not.

| Skill | Covers |
|---|---|
| [getty-perl-core](getty-perl-core/SKILL.md) | House rules for all Perl code — module loading, Moose patterns, cpanfile versioning for Getty-authored CPAN distributions, stylistic choices that differ from defaults. Load on any Perl edit in a Getty project. |
| [getty-perl-moose](getty-perl-moose/SKILL.md) | Moose classes — attributes, roles vs. inheritance, BUILD/BUILDARGS, type constraints, MooseX::Singleton, make_immutable, method modifiers. |
| [getty-perl-moo](getty-perl-moo/SKILL.md) | Moo object system — roles, attributes, inheritance patterns, and best practices. |
| [getty-perl-crawl4ai](getty-perl-crawl4ai/SKILL.md) | WWW::Crawl4AI + Net::Async::Crawl4AI — Getty's own Perl client and fallback orchestrator for the Crawl4AI Docker service, including the strategy chain, content classification, and error model. |
| [getty-perl-kubernetes-classes](getty-perl-kubernetes-classes/SKILL.md) | IO::K8s — Getty's own typed Kubernetes objects for Perl: creating, serializing, extending via CRD providers. |
| [getty-perl-release-author-getty](getty-perl-release-author-getty/SKILL.md) | For `dist.ini` files using Getty's own `[@Author::GETTY]` bundle — bundle options, POD conventions (`=attr`/`=method`/`=opt`), next-version semantics, the `dzil release` workflow. |
| [perl-io-async-future](perl-io-async-future/SKILL.md) | Async Perl with IO::Async, Future, Future::AsyncAwait — lifecycle, retention, cancellation, reconnect patterns from PEVANS modules and battle-tested fixes. |
| [perl-mcp](perl-mcp/SKILL.md) | MCP (Model Context Protocol) server development in Perl — tool definitions, server setup, common patterns. |
| [perl-release-dist-ini](perl-release-dist-ini/SKILL.md) | Reading, editing, or debugging any `dist.ini` — any plugin bundle (Author::GETTY, Author::ETHER, Author::KENTNL, …), version config, plugins, metadata, prereqs. |

`getty-perl-core` is the one to load first — it sets the conventions the others build on.
For a `dist.ini` under `[@Author::GETTY]`, load both `perl-release-dist-ini` (the generic
mechanics) and `getty-perl-release-author-getty` (what that bundle adds) together.
