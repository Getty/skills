'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { trustedDocumentURL, assetForURL, authorizeSender, parseTheme, allowedExternalURL, createTokenBucket } = require('../examples/secure-shell/policy.cjs');
test('trusted document', () => assert.equal(trustedDocumentURL('app://desktop/index.html'), true));
test('same-document hash', () => assert.equal(trustedDocumentURL('app://desktop/index.html#settings'), true));
for (const value of ['https://desktop/index.html','file:///index.html','app://desktop.evil/index.html','app://desktop@evil/index.html','app://user@desktop/index.html','app://desktop:123/index.html','app://desktop/other.html','app://desktop/index.html?admin=1','app://desktop/../index.html','app://desktop/%69ndex.html','app://desktop/%2e%2e/index.html','app://desktop/%252e%252e/index.html','app://desktop\\index.html',' app://desktop/index.html','app://desktop/index.html\n','javascript:alert(1)','not a url',null,'app://desktop/' + 'x'.repeat(2050)]) {
  test(`document rejects ${String(value).slice(0,85)}`, () => assert.equal(trustedDocumentURL(value), false));
}
test('asset map returns only known files', () => assert.deepEqual(assetForURL('app://desktop/renderer.js'), { file: 'renderer.js', mime: 'text/javascript; charset=utf-8' }));
test('HTML asset MIME', () => assert.match(assetForURL('app://desktop/index.html').mime, /^text\/html/));
test('stylesheet MIME', () => assert.match(assetForURL('app://desktop/styles.css').mime, /^text\/css/));
for (const value of ['app://desktop/secret.txt','app://desktop/constructor','app://desktop/renderer.js?x=1','app://desktop/renderer.js#x','app://desktop/../../etc/passwd','app://desktop/%2fetc/passwd','file:///etc/passwd']) test(`asset rejects ${value}`, () => assert.equal(assetForURL(value), null));
function caller() { const frame = { url: 'app://desktop/index.html' }; const owner = { mainFrame: frame, isDestroyed: () => false }; return { owner, event: { sender: owner, senderFrame: frame } }; }
test('authorized top frame', () => { const { owner,event }=caller(); assert.equal(authorizeSender(event,owner),true); });
test('other window denied', () => { const { owner,event }=caller(); event.sender={}; assert.equal(authorizeSender(event,owner),false); });
test('same URL in subframe denied', () => { const { owner,event }=caller(); event.senderFrame={url:'app://desktop/index.html'}; assert.equal(authorizeSender(event,owner),false); });
test('navigated main frame denied', () => { const { owner,event }=caller(); event.senderFrame.url='https://evil.test/'; assert.equal(authorizeSender(event,owner),false); });
test('destroyed owner denied', () => { const { owner,event }=caller(); owner.isDestroyed=()=>true; assert.equal(authorizeSender(event,owner),false); });
test('missing frame denied', () => { const { owner,event }=caller(); event.senderFrame=null; assert.equal(authorizeSender(event,owner),false); });
test('exception during sender inspection denied', () => { const { owner,event }=caller(); owner.isDestroyed=()=>{throw Error('gone');}; assert.equal(authorizeSender(event,owner),false); });
test('no owner denied', () => assert.equal(authorizeSender({},null),false));
for (const theme of ['system','light','dark']) test(`theme ${theme}`, () => assert.equal(parseTheme({theme}),theme));
for (const value of [null,[],{}, {theme:'remote'}, {theme:'dark',path:'/etc/passwd'}, {theme:1}, {theme:'x'.repeat(100_000)}, new Date()]) test(`invalid theme input ${JSON.stringify(value).slice(0,70)}`, () => assert.throws(()=>parseTheme(value),TypeError));
test('prototype field rejected', () => assert.throws(()=>parseTheme(JSON.parse('{"theme":"dark","__proto__":{}}')),TypeError));
test('fixed docs URL allowed', () => assert.equal(allowedExternalURL('https://www.electronjs.org/docs/latest/tutorial/security'),true));
for (const value of ['http://www.electronjs.org/docs/','https://www.electronjs.org.evil/docs/','https://www.electronjs.org@evil.test/docs/','https://user@www.electronjs.org/docs/','https://www.electronjs.org:444/docs/','https://www.electronjs.org/not-docs/','file:///tmp/a','javascript:alert(1)','https://www.electronjs.org/docs/?token=secret',null]) test(`external rejects ${value}`, () => assert.equal(allowedExternalURL(value),false));
test('rate bucket permits bounded burst', () => { const bucket=createTokenBucket({capacity:2,refillPerSecond:1,clock:()=>0}); assert.equal(bucket.take(),true); assert.equal(bucket.take(),true); assert.equal(bucket.take(),false); });
test('rate bucket refills by elapsed time', () => { let time=0; const b=createTokenBucket({capacity:1,refillPerSecond:2,clock:()=>time}); b.take(); time=499; assert.equal(b.take(),false); time=500; assert.equal(b.take(),true); });
test('refill does not exceed capacity', () => { let time=0; const b=createTokenBucket({capacity:1,clock:()=>time}); b.take(); time=1e6; assert.equal(b.take(),true); assert.equal(b.take(),false); });
test('clock rollback cannot create tokens', () => { let time=1000; const b=createTokenBucket({capacity:1,refillPerSecond:1,clock:()=>time}); b.take(); time=0; assert.equal(b.take(),false); time=1000; assert.equal(b.take(),false); });
test('invalid clock after start denies', () => { let time=0; const b=createTokenBucket({clock:()=>time}); time=NaN; assert.equal(b.take(),false); });
test('invalid rate policy rejects', () => assert.throws(()=>createTokenBucket({capacity:0}),TypeError));
test('invalid initial clock rejects', () => assert.throws(()=>createTokenBucket({clock:()=>NaN}),TypeError));
