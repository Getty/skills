'use strict';
/** Pure policy helpers. Tests do not claim an actual Electron sandbox test. */
const APP = Object.freeze({ scheme: 'app:', host: 'desktop', document: '/index.html' });
const ASSETS = Object.freeze({ '/index.html': ['index.html', 'text/html; charset=utf-8'], '/renderer.js': ['renderer.js', 'text/javascript; charset=utf-8'], '/styles.css': ['styles.css', 'text/css; charset=utf-8'] });
const THEMES = new Set(['system', 'light', 'dark']);
function appURL(raw) {
  if (typeof raw !== 'string' || raw.length > 2048 || /[\u0000-\u0020\u007f\\%]/.test(raw)) return null;
  if (/(?:^|\/)\.{1,2}(?:\/|$)/.test(raw)) return null;
  try {
    const url = new URL(raw);
    if (url.protocol !== APP.scheme || url.hostname !== APP.host || url.port || url.username || url.password || url.search) return null;
    return url;
  } catch { return null; }
}
function trustedDocumentURL(raw) {
  const url = appURL(raw);
  return !!url && url.pathname === APP.document;
}
function assetForURL(raw) {
  const url = appURL(raw);
  if (!url || url.hash || !Object.hasOwn(ASSETS, url.pathname)) return null;
  return Object.freeze({ file: ASSETS[url.pathname][0], mime: ASSETS[url.pathname][1] });
}
function authorizeSender(event, owner) {
  try {
    return !!owner && !owner.isDestroyed() && event.sender === owner && !!event.senderFrame && event.senderFrame === owner.mainFrame && trustedDocumentURL(event.senderFrame.url);
  } catch { return false; }
}
function parseTheme(payload) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload) || ![Object.prototype, null].includes(Object.getPrototypeOf(payload))) throw new TypeError('Invalid preference request');
  const keys = Object.keys(payload);
  if (keys.length !== 1 || keys[0] !== 'theme' || typeof payload.theme !== 'string' || !THEMES.has(payload.theme)) throw new TypeError('Invalid theme');
  return payload.theme;
}
function allowedExternalURL(raw) {
  if (typeof raw !== 'string' || raw.length > 2048 || /[\u0000-\u0020\u007f\\]/.test(raw)) return false;
  try {
    const url = new URL(raw);
    return url.protocol === 'https:' && url.hostname === 'www.electronjs.org' && !url.port && !url.username && !url.password && url.pathname.startsWith('/docs/') && !url.search && !url.hash;
  } catch { return false; }
}
function createTokenBucket({ capacity = 20, refillPerSecond = 5, clock = Date.now } = {}) {
  if (!Number.isFinite(capacity) || capacity < 1 || !Number.isFinite(refillPerSecond) || refillPerSecond <= 0 || typeof clock !== 'function') throw new TypeError('Invalid rate policy');
  let tokens = capacity, last = clock();
  if (!Number.isFinite(last)) throw new TypeError('Invalid clock');
  return Object.freeze({ take() {
    const now = clock(); if (!Number.isFinite(now)) return false;
    const elapsed = Math.max(0, now - last); last = Math.max(last, now);
    tokens = Math.min(capacity, tokens + elapsed * refillPerSecond / 1000);
    if (tokens < 1) return false;
    tokens -= 1; return true;
  } });
}
module.exports = { trustedDocumentURL, assetForURL, authorizeSender, parseTheme, allowedExternalURL, createTokenBucket };
