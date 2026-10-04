# Official Hermes Desktop SDK

Use the native [Desktop SDK](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk) for native app contributions. It is distinct from the web Dashboard SDK and Python agent plugins.

## Package and entry point

A disk plugin is plain ESM at the Desktop machine's resolved `desktop-plugins/<id>/plugin.js`. It default-exports an object with `id`, optional display/default fields, and `register(ctx)`. The folder and ID must agree.

This original example uses the documented basic contract:

```javascript
import { PANES_AREA } from '@hermes/plugin-sdk';
import { jsx } from 'react/jsx-runtime';

export default {
  id: 'text-metrics-panel',
  name: 'Text Metrics',
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'overview',
      area: PANES_AREA,
      title: 'Text Metrics',
      data: { placement: 'right', width: '260px' },
      render: () => jsx('div', {
        className: 'p-3 text-sm',
        children: 'Select a document to inspect its text metrics.'
      })
    });
  }
};
```

This only contributes static UI; it does not implement document selection or a backend. Literal JSX is not accepted by the disk loader. Use `jsx/jsxs` or `React.createElement`.

## Contribution and host APIs

The [pinned PluginContext](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/plugin.ts) provides registration, cleanup, timers, events, scoped REST/socket, storage, OS actions, and localization. The [export inventory](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/sdk/index.ts) is the contract for available constants/components.

Use supported areas for panes, routes, navigation, status/title bars, commands/keybindings, composer/session contributions, settings, and appearance. Each area has its own data shape. Read that shape rather than assuming all areas accept an arbitrary React component.

Use reactive host state through the SDK. In particular, gateway socket status is not the current agent turn's busy state. The [contribution type](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/types.ts) notes that `when()` is reevaluated when area snapshots rebuild; it is not a general reactive subscription.

## Loading and trust

Use the documented imports `@hermes/plugin-sdk`, `react`, and `react/jsx-runtime`. Other imports require explicit target-build support; do not assume arbitrary npm/URL/relative-module loading.

The [loader](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/runtime-loader.ts) provides error handling and lifecycle management, not a sandbox. ESM runs with renderer authority; storage namespaces are conventions.

Disabled plugins may still be evaluated for inventory, although `register()` is gated. Keep module scope free of side effects. Register timers/listeners through context and release external subscriptions with `onDispose`. Test save/reload, disable/re-enable, window close, and active-connection switching.

For optional newer exports, feature-detect through a namespace import. A missing named import can prevent the whole plugin loading before your fallback executes.

