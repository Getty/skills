import type {} from '../examples/react-adapter/desktop.js';
const bridge = window.desktop;
if (bridge) {
  void bridge.setTheme('dark');
  // @ts-expect-error The bridge does not accept arbitrary theme payloads.
  void bridge.setTheme('execute');
  // @ts-expect-error A generic IPC transport must not appear in this contract.
  bridge.send('channel', {});
}
