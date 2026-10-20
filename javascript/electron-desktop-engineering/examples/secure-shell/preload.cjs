'use strict';
// Intentionally self-contained: sandboxed preload cannot assume arbitrary relative require.
const { contextBridge, ipcRenderer } = require('electron');
const themes = new Set(['system', 'light', 'dark']);
function preferences(value) {
  if (!value || !themes.has(value.theme) || !Number.isSafeInteger(value.revision) || value.revision < 0) throw new TypeError('Invalid preference response');
  return Object.freeze({ theme: value.theme, revision: value.revision });
}
async function result(promise) {
  const reply = await promise;
  if (!reply || reply.ok !== true) throw new Error(reply?.error?.code === 'busy' ? 'Too many requests' : 'Desktop request failed');
  return reply.value;
}
contextBridge.exposeInMainWorld('desktop', Object.freeze({
  getPreferences: async () => preferences(await result(ipcRenderer.invoke('preferences:get'))),
  setTheme: async theme => {
    if (typeof theme !== 'string' || !themes.has(theme)) throw new TypeError('Invalid theme');
    return preferences(await result(ipcRenderer.invoke('preferences:set-theme', { theme })));
  },
  openDocumentation: async () => { await result(ipcRenderer.invoke('documentation:open')); },
  onPreferencesChanged: callback => {
    if (typeof callback !== 'function') throw new TypeError('Listener must be a function');
    const wrapped = (_event, payload) => { callback(preferences(payload)); };
    ipcRenderer.on('preferences:changed', wrapped);
    let active = true;
    return () => { if (active) { active = false; ipcRenderer.removeListener('preferences:changed', wrapped); } };
  }
}));
