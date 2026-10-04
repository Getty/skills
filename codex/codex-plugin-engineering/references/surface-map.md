# Surface and capability map

Read this before choosing a package, protocol, or deployment. Separate the visible client, orchestration service, execution environment, and connected identity.

## Documented baseline

| Surface | Established capability | Design implication |
|---|---|---|
| Codex CLI | Native plugin browser and plugin commands | Test with the actual installed CLI and a fresh session. |
| Codex in the ChatGPT desktop app | Native plugins; desktop capabilities depend on environment | Include OS and local-versus-cloud execution in the test record. |
| Codex IDE extension | Standalone skills and directly configured MCP; native plugins are not supported in the current user guide | Offer a separately tested skill/MCP installation if IDE support is required. |
| ChatGPT web/mobile and desktop Chat/Work | Universal plugin directory, with capability restrictions | A catalog listing is insufficient evidence for local scripts or UI features. |
| Codex Cloud | A separate execution environment | Establish the particular cloud product and its package/runtime contract before promising plugin parity. |
| Cloud-orchestrated ChatGPT Work | Plugin tools and skills; plugin hooks are excluded | Connecting a computer does not move orchestration to that computer. |

Sources: [Plugins](https://learn.chatgpt.com/docs/plugins), [Build skills](https://learn.chatgpt.com/docs/build-skills), [MCP](https://learn.chatgpt.com/docs/extend/mcp), [configuration scope](https://learn.chatgpt.com/docs/config-file/config-reference).

The current SDK and user documentation should take precedence over a historical changelog entry when their host-support claims disagree. Record the discrepancy rather than presenting contradictory claims together.

## Ask the questions that change implementation

- Where will scripts execute, and which interpreters and filesystem paths exist there?
- Is the package locally installed, imported by a workspace admin, or published through the public directory?
- Is the service connected as the user, a managed account, or a service identity?
- Does the host support the required approval interaction, MCP authentication, UI, or event delivery?
- Is a fresh conversation required to discover the changed package?
- Which capability is essential, and what useful output remains if that capability is absent?

Use separate acceptance tests for execution and presentation. A plugin that returns a structured search result in CLI and an interactive browser in desktop may provide the same core workflow with different presentation. A plugin whose only useful behavior requires a local daemon needs an explicit deployment story.

## Avoid misleading product substitutions

Do not call all OpenAI integrations “Codex plugins.” A standalone skill, a ChatGPT plugin, a Codex SDK program, an Agents API session, an IDE extension, and a custom app-server client have different configuration and lifecycle contracts. Choose the actual requested host, and label optional adjacent integrations.
