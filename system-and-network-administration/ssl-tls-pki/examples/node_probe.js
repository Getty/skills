#!/usr/bin/env node
// Usage: node node_probe.js host port expected-name ca.pem
// Performs certificate/name verification and one HTTP/1.1 status check.
'use strict';
const tls = require('node:tls');
const fs = require('node:fs');
const [host, portText, name, caPath, ...extra] = process.argv.slice(2);
const port = Number(portText);
if (!host || !name || !caPath || extra.length || !Number.isInteger(port) || port < 1 || port > 65535 || /[\r\n /\\]/.test(name)) {
  console.error('usage: node node_probe.js host port expected-name ca.pem'); process.exit(2);
}
let ca;
try { ca = fs.readFileSync(caPath); } catch (err) { console.error(err.message); process.exit(2); }
let received = '', finished = false;
const socket = tls.connect({host, port, servername:name, ca, rejectUnauthorized:true, minVersion:'TLSv1.2', ALPNProtocols:['http/1.1']});
function finish(ok, message) {
  if (finished) return;
  finished = true;
  (ok ? console.log : console.error)(message);
  process.exitCode = ok ? 0 : 1;
  socket.destroy();
}
socket.setTimeout(5000, () => finish(false, 'timeout'));
socket.on('error', err => finish(false, err.message));
socket.on('secureConnect', () => socket.write(`GET / HTTP/1.1\r\nHost: ${name}\r\nConnection: close\r\n\r\n`));
socket.on('data', data => {
  received += data.toString('utf8');
  if (received.length > 16384) return finish(false, 'response header too large');
  const i = received.indexOf('\r\n');
  if (i >= 0) finish(received.startsWith('HTTP/1.1 200 '), received.slice(0, i));
});
socket.on('end', () => finish(false, 'connection ended before a complete status line'));
