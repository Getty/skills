# Marketplaces, dependencies, and distribution

## Package and catalog are separate deliverables

A plugin contains behavior. A marketplace tells Claude Code where to obtain plugins and how to identify them. Keep their names, versions, ownership, and release processes distinct. A repository may host one plugin, many plugins, only a catalog, or all of these. [Marketplace authoring](https://code.claude.com/docs/en/plugins/create-marketplace).

Original minimal `.claude-plugin/marketplace.json` for a repository containing `plugins/change-companion/`:

```json
{
  "name": "example-tools",
  "owner": {"name": "Example maintainers"},
  "plugins": [
    {
      "name": "change-companion",
      "source": "./plugins/change-companion",
      "description": "Evidence-based review assistance"
    }
  ]
}
```

The source is relative to the marketplace root. Test both the catalog and the plugin directory. Make ownership and support expectations explicit; an entry in a catalog does not establish who maintains its code.

## Choose a source intentionally

| Distribution need | Candidate | Main design check |
|---|---|---|
| Local development or managed directory deployment | Relative plugin directory | Does the target receive the whole directory? |
| Version-controlled release | `github`, Git `url`, or `git-subdir` | Which ref/commit is selected, and can authentication run noninteractively? |
| Registry distribution | `npm` | Is the published package complete, including its appropriate lockfile? |
| Immutable downloadable package | `archive` | Is the ZIP rooted correctly and its digest pinned? |
| Existing enterprise provisioning process | `command` | Is execution necessary, reviewable, bounded, and supported by policy? |

These are different marketplace source schemas. In particular, a plugin source with `source: "url"` denotes Git; downloadable ZIPs use `archive`. A marketplace fetched as one JSON URL does not fetch neighboring plugin files, so relative sources require a directory/Git-hosted catalog or a different plugin source. Read the exact field names instead of guessing from a URL extension. [Source schemas](https://code.claude.com/docs/en/plugins/marketplace-reference), [hosting and private access](https://code.claude.com/docs/en/plugins/host-marketplace).

## Model two kinds of dependency

**Plugin dependencies** supply other plugins. **Runtime dependencies** supply code or executables used by this plugin. A dependency on a plugin does not install arbitrary Python packages or an LSP binary. Design the failure message for each independently.

Plugin dependency entries can name the current marketplace, qualify another marketplace, and express a version range. Git-backed range resolution uses release tags with the documented plugin-specific naming convention, such as `change-companion--v1.2.0`. Multiple constraints must intersect. Cross-marketplace auto-installation additionally depends on the catalog's `allowCrossMarketplaceDependenciesOn` setting; do not quietly add a new marketplace to satisfy it. Local `--plugin-dir` development does not check dependency versions. [Dependency resolution](https://code.claude.com/docs/en/plugins/dependencies).

For each dependency, record why it is needed, acceptable versions, who obtains it, behavior when absent, and whether a degraded mode is useful. Prefer an explicit error to invoking an unrelated tool with a coincidentally similar name. See [loading and runtime packages](loading-versioning-development.md).

## Exercise the real install route

After reviewing the package in an authorized disposable project, a local catalog exercise is:

```bash
claude plugin validate ./example-marketplace --strict
claude plugin marketplace add ./example-marketplace
claude plugin install change-companion@example-tools --scope local
claude plugin list --json
```

The last three commands change or inspect the selected installation; they are a workflow example, not instructions to install an unknown catalog. The scope names are `user`, `project`, and `local`; use `--scope`, not an invented `--project` flag. Inspect the loaded components in a session after installation. [CLI contract](https://code.claude.com/docs/en/plugins/cli-reference).

## Prepare a release and rollback

Keep the technical plugin name stable. A rename changes identity and requires migration; changing a display label is a different operation. Choose explicit semantic versions with a release bump, or the documented source-derived version strategy. Reusing an explicit version while changing code can leave cached users on old content. [Publishing guidance](https://code.claude.com/docs/en/plugins/publish).

Before release, check the actual install artifact, runtime requirements, supported Claude Code builds, permission effects, configuration migration, cancellation, and one upgrade from the preceding version. Keep the previous source/version and state backup strategy available. Preview tags with `claude plugin tag --dry-run` before creating or pushing them. Publishing a catalog, uploading a package, and pushing a tag are separate external actions; carry out only the authorized ones.

Use the [official plugin repository](https://github.com/anthropics/claude-plugins-official) as a locator for real packages. Its `plugins` and `external_plugins` sections have different maintainers; inspect the individual manifest, source, license, and current documentation before adapting an example.
