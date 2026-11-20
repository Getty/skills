#!/usr/bin/env node
"use strict";
// Execute original fixtures against a caller-supplied trusted local evaluator.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 3 || args[0] !== "--engine") {
    throw new Error("Usage: node run_cases.cjs --engine /trusted/logic.js cases.json");
  }
  const enginePath = path.resolve(args[1]);
  const engine = require(enginePath);
  if (!engine || typeof engine.apply !== "function") {
    throw new Error("Evaluator must expose apply(rule, data)");
  }
  const raw = fs.readFileSync(path.resolve(args[2]), "utf8");
  if (Buffer.byteLength(raw) > 4 * 1024 * 1024) throw new Error("Corpus too large");
  const cases = JSON.parse(raw);
  if (!Array.isArray(cases) || !cases.length) throw new Error("Expected nonempty case array");
  const failures = [];
  let passed = 0;
  for (const test of cases) {
    try {
      const choices = ["expected", "expectedError", "expectedSpecial"]
        .filter(key => Object.hasOwn(test, key));
      assert.equal(choices.length, 1, "case must have exactly one expectation");
      let actual, thrown;
      try {
        actual = engine.apply(structuredClone(test.rule), structuredClone(test.data));
      } catch (error) {
        thrown = error;
      }
      if (Object.hasOwn(test, "expectedError")) {
        assert.ok(thrown, "expected an evaluation error");
        assert.ok(String(thrown.message || thrown).includes(test.expectedError),
          "error did not contain expected text");
      } else {
        if (thrown) throw thrown;
        if (Object.hasOwn(test, "expectedSpecial")) {
          const special = test.expectedSpecial;
          if (special === "positive-infinity") assert.equal(actual, Infinity);
          else if (special === "negative-infinity") assert.equal(actual, -Infinity);
          else if (special === "nan") assert.ok(Number.isNaN(actual));
          else throw new Error("Unknown expectedSpecial");
        } else {
          assert.deepStrictEqual(actual, test.expected);
        }
      }
      passed++;
    } catch (error) {
      failures.push({id: test.id || "(unnamed)", message: error.message});
    }
  }
  process.stdout.write(JSON.stringify({engine: enginePath, total: cases.length,
    passed, failed: failures.length, failures}, null, 2) + "\n");
  process.exitCode = failures.length ? 1 : 0;
}
try { main(); } catch (error) {
  process.stderr.write(String(error.message || error) + "\n");
  process.exitCode = 2;
}
