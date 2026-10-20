'use strict';
const { app, BrowserWindow, protocol, session, ipcMain, shell } = require('electron');
const path = require('node:path');
const fs = require('node:fs/promises');
const { trustedDocumentURL, assetForURL, authorizeSender, parseTheme, allowedExternalURL, createTokenBucket } = require('./policy.cjs');
// Scheme privileges must be declared before ready. Never bypass CSP.
protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } }]);
const DOCUMENT = 'app://desktop/index.html';
const DOCS = 'https://www.electronjs.org/docs/latest/tutorial/security';
const CSP = "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; font-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'";
let window = null;
let preferences = { theme: 'system', revision: 0 }; // In-memory example, intentionally not durable storage.
const rate = createTokenBucket();
let inFlight = 0;
const failure = (code, message) => ({ ok: false, error: { code, message } });
function registerOperation(channel, validate, operation) {
  ipcMain.handle(channel, async (event, payload) => {
    if (!authorizeSender(event, window?.webContents)) return failure('denied', 'Request denied');
    if (!rate.take() || inFlight >= 4) return failure('busy', 'Too many requests');
    let input;
    try { input = validate(payload); } catch { return failure('invalid_input', 'Invalid request'); }
    inFlight++;
    try { return { ok: true, value: await operation(input) }; }
    catch { return failure('operation_failed', 'Operation failed'); }
    finally { inFlight--; }
  });
}
function noPayload(payload) { if (payload !== undefined) throw new TypeError('No payload expected'); }
registerOperation('preferences:get', noPayload, () => ({ ...preferences }));
registerOperation('preferences:set-theme', parseTheme, theme => {
  preferences = { theme, revision: preferences.revision + 1 };
  if (window && !window.isDestroyed()) window.webContents.send('preferences:changed', { ...preferences });
  return { ...preferences };
});
registerOperation('documentation:open', noPayload, async () => {
  if (!allowedExternalURL(DOCS)) throw new Error('Invalid configured documentation URL');
  await shell.openExternal(DOCS); return null;
});
function createWindow(appSession) {
  window = new BrowserWindow({ width: 900, height: 640, show: false,
    webPreferences: { preload: path.join(__dirname, 'preload.cjs'), session: appSession, contextIsolation: true, sandbox: true, nodeIntegration: false, webSecurity: true, webviewTag: false } });
  const contents = window.webContents;
  contents.setWindowOpenHandler(() => ({ action: 'deny' }));
  contents.on('will-navigate', event => event.preventDefault());
  contents.on('will-frame-navigate', event => event.preventDefault());
  contents.on('will-redirect', event => event.preventDefault());
  window.once('ready-to-show', () => { if (window && !window.isDestroyed()) window.show(); });
  window.on('closed', () => { window = null; });
  // Explicit load is application-owned; renderer-initiated navigations above are denied.
  if (!trustedDocumentURL(DOCUMENT)) throw new Error('Invalid application document');
  window.loadURL(DOCUMENT).catch(() => { console.error('Application document failed to load'); app.quit(); });
}
app.on('web-contents-created', (_event, contents) => {
  contents.on('will-attach-webview', event => event.preventDefault());
});
app.whenReady().then(async () => {
  const appSession = session.fromPartition('persist:secure-shell-example');
  appSession.setPermissionCheckHandler(() => false);
  appSession.setPermissionRequestHandler((_contents, _permission, callback) => callback(false));
  appSession.on('will-download', (_event, item) => item.cancel());
  // Fixed immutable packaged files: no user URL ever becomes an arbitrary filesystem path.
  const assets = new Map();
  for (const name of ['index.html', 'renderer.js', 'styles.css']) {
    const bytes = await fs.readFile(path.join(__dirname, 'renderer', name));
    if (bytes.byteLength > 2_000_000) throw new Error('Packaged asset exceeds example limit');
    assets.set(name, bytes);
  }
  appSession.protocol.handle('app', request => {
    if (request.method !== 'GET') return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET' } });
    const asset = assetForURL(request.url);
    if (!asset) return new Response('Not found', { status: 404 });
    return new Response(assets.get(asset.file), { headers: { 'Content-Type': asset.mime, 'Content-Security-Policy': CSP, 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-store' } });
  });
  createWindow(appSession);
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(appSession); });
}).catch(() => { console.error('Application startup failed'); app.quit(); });
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
