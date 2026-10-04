# In-process mod runtime

## Check the feature gate

Mods are supported from Claude Code v2.1.287 and are enabled by default subject to policy. They register JavaScript or TypeScript functions inside Claude Code. Treat this as a distinct API from classic JSON hooks. Do not rely on the obsolete early-access environment switch. [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview).

Start with a normal plugin manifest, then `hooks/hooks.json`:

```json
{
  "modules": ["./register.js"]
}
```

The module path is relative to `hooks.json`. The current contract accepts one module entry; combine handlers through that entry rather than inventing an arbitrary module loader. Export `register(on, options)`; `options` carries user configuration. Classic hooks can coexist under a separate `hooks` key. [Mod file contract](https://code.claude.com/docs/en/plugins/mods/reference#files).

## Example: bounded observation

Original `hooks/register.js` for a plugin named `read-meter`:

```javascript
let completed = 0;
let failed = 0;

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'read-meter-summary',
      description: 'Show the observed read outcomes since this mod loaded'
    });
    return next(e);
  });

  on('tool.call', { tool: 'Read' }, async ($, e, next) => {
    const outcome = await next(e);
    if (outcome.deny || outcome.isError) failed += 1;
    else completed += 1;
    return outcome;
  });

  on('command.run', { command: 'read-meter-summary' }, async () => ({
    text: `Completed reads: ${completed}; denied or failed reads: ${failed}`
  }));
}
```

The counts reset when the module reloads and include only events reaching this handler. This is observation, not billing or a security log. Keep that limitation in the command's description.

## Compile against the actual build

Loading a development mod causes Claude Code to write declarations under `.claude-plugin/types/`; use those declarations and generated TypeScript configuration for the installed version. The published [mod types](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts) can lag. `claude plugin validate` statically reports handled events and API calls without executing the mod. [Authoring and generated types](https://code.claude.com/docs/en/plugins/mods/create#get-type-definitions-for-your-version).

Write API calls in the form the static analyzer accepts, such as `$.fs.read(...)`. Do not hide access behind dynamic property names or assume arbitrary Node imports and globals. Keep pure parsing and transformation code separate from effects.

## Design for bounded execution

Ordinary mod handlers are async functions; streaming events such as `turn.step` have generator contracts. The current reference sets a 10-second own-execution budget per hook, excluding waits inside most API calls and `next`; `.catch` handlers have a shorter budget. A timeout can skip a handler. [Runtime limits](https://code.claude.com/docs/en/plugins/mods/reference#limits).

Forward `next.signal` to long-running operations that support cancellation. Keep timers, streams, and state bounded. Do not make an internal promise wait indefinitely for a UI response; use the supported API and define headless behavior. Make reload, disable, interruption, and partial completion explicit test cases.
