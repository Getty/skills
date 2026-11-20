#!/usr/bin/env node
/** Run original fixtures through a caller-supplied feelin-compatible module.
 * No package installation, network request, or replacement FEEL evaluator.
 */
import { readFile, stat } from 'node:fs/promises';
import { isAbsolute } from 'node:path';
import { pathToFileURL } from 'node:url';
import { isDeepStrictEqual } from 'node:util';

async function main() {
  const argv = process.argv.slice(2);
  const options = {};
  for (let i = 0; i < argv.length; i += 2) {
    if (!['--engine', '--cases'].includes(argv[i]) || !argv[i + 1] || options[argv[i]]) {
      throw new Error('Usage: node run_cases.mjs --engine /absolute/module.js --cases cases.json');
    }
    options[argv[i]] = argv[i + 1];
  }
  if (!options['--engine'] || !options['--cases'] || !isAbsolute(options['--engine'])) {
    throw new Error('Provide an absolute existing engine module and a case file.');
  }
  if (!(await stat(options['--engine'])).isFile()) throw new Error('Engine must be a module file.');
  if ((await stat(options['--cases'])).size > 1024 * 1024) throw new Error('Case file exceeds 1 MiB helper limit.');
  const fixture = JSON.parse(await readFile(options['--cases'], 'utf8'));
  if (!Array.isArray(fixture.cases) || !fixture.cases.length) throw new Error('Expected nonempty cases array.');
  const ids = new Set();
  for (const c of fixture.cases) {
    if (!c || typeof c.id !== 'string' || ids.has(c.id) || typeof c.source !== 'string'
      || !['expression', 'unary-test'].includes(c.kind) || !Object.hasOwn(c, 'expected')
      || c.context === null || typeof c.context !== 'object' || Array.isArray(c.context)
      || (c.minWarnings !== undefined && (!Number.isInteger(c.minWarnings) || c.minWarnings < 0))) {
      throw new Error('Invalid or duplicate case: ' + String(c?.id));
    }
    ids.add(c.id);
  }
  const engine = await import(pathToFileURL(options['--engine']).href);
  if (typeof engine.evaluate !== 'function' || typeof engine.unaryTest !== 'function') {
    throw new Error('Module must export evaluate and unaryTest.');
  }
  const results = [];
  for (const c of fixture.cases) {
    try {
      const result = await (c.kind === 'unary-test' ? engine.unaryTest : engine.evaluate)(c.source, c.context);
      if (!result || !Object.hasOwn(result, 'value') || !Array.isArray(result.warnings)) {
        throw new Error('Engine result must contain value and warnings array.');
      }
      const pass = isDeepStrictEqual(result.value, c.expected)
        && result.warnings.length >= (c.minWarnings ?? 0);
      results.push({id:c.id, pass, expected:c.expected, actual:result.value, warnings:result.warnings});
    } catch (error) {
      results.push({id:c.id, pass:false, expected:c.expected, error:String(error.message ?? error)});
    }
  }
  const passed = results.filter(r => r.pass).length;
  console.log(JSON.stringify({engineModule:options['--engine'], profile:fixture.profile,
    passed, failed:results.length-passed, total:results.length, results}, null, 2));
  process.exitCode = passed === results.length ? 0 : 1;
}
main().catch(error => { console.error(JSON.stringify({error:String(error.message ?? error)})); process.exitCode=2; });
