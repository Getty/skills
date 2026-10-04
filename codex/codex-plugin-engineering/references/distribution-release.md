# Distribution, publication, and upgrades

Select the distribution route independently from the implementation.

| Route | Appropriate goal | Release owner |
|---|---|---|
| Local marketplace | Individual development and testing | Local user |
| Repository marketplace | Team/project distribution | Repository maintainer |
| Workspace import | Managed organizational access | Workspace administrator |
| Universal public directory | Public discoverability | Verified publisher |

Workspace import currently treats bundled MCP declarations as Desktop only, including HTTPS declarations. A `.app.json` reference points to an existing app; it does not create the integration or grant account access. [Workspace plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management)

## Public submission baseline

The portal has a separate validation/review contract. It currently connects one MCP server per plugin, even if a package declares several, and does not support adding MCP to an existing skills-only plugin. Package/skill updates and hosted tool updates follow different review paths. [Submission](https://developers.openai.com/plugins/deploy/submission)

Remote MCP review currently requires production HTTPS, domain verification, explicit annotation justifications, five positive and three negative test cases, and review materials. Upload validation is weaker than final directory validation. Recheck the exact limits when publishing. [Submission errors and requirements](https://developers.openai.com/plugins/deploy/submission-errors)

These are public distribution constraints, not general limits on local MCP client configuration.

## Release procedure

1. Assign a version to the exact package contents.
2. Validate the archive as extracted into a clean directory.
3. Test the installed release candidate against supported hosts.
4. Review metadata, screenshots, privacy claims, and examples against actual behavior.
5. Keep credentials and reviewer access outside the archive.
6. Publish only through the authorized route.
7. Verify the installed/published revision after completion.

Keep backend changes compatible with still-installed skill versions. If a tool schema must break, plan a migration window or versioned operation rather than silently reinterpreting old arguments.

## Rollback and retirement

Retain the last working package and compatible service version. Document how to disable the plugin, revert a marketplace revision, and reconnect only if needed. Uninstalling a bundle and revoking external credentials are distinct operational tasks.

For workspace catalogs, removing source content is not automatically equivalent to deleting imported plugins. Inspect the admin-managed state before claiming removal succeeded.
