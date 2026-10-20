'use strict';
const theme = document.getElementById('theme');
const status = document.getElementById('status');
const save = document.getElementById('save');
const docs = document.getElementById('docs');
let appliedRevision = -1;
function apply(value) {
  if (value.revision < appliedRevision) return;
  appliedRevision = value.revision;
  theme.value = value.theme;
  document.documentElement.dataset.theme = value.theme;
  status.textContent = `Theme: ${value.theme}; revision ${value.revision}.`;
}
async function run(action) {
  save.disabled = true;
  try { await action(); } catch { status.textContent = 'The desktop operation failed.'; }
  finally { save.disabled = false; }
}
if (!window.desktop) {
  status.textContent = 'Desktop bridge is unavailable. Launch through Electron.';
  save.disabled = true; docs.disabled = true;
} else {
  const unsubscribe = window.desktop.onPreferencesChanged(apply);
  window.addEventListener('pagehide', unsubscribe, { once: true });
  void run(async () => apply(await window.desktop.getPreferences()));
  save.addEventListener('click', () => { void run(async () => apply(await window.desktop.setTheme(theme.value))); });
  docs.addEventListener('click', () => { void run(() => window.desktop.openDocumentation()); });
}
