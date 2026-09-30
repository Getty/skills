# Validation Report

**Validation date: September 30, 2026. Package: 1.0.1, English.** Tested in a
Linux container with **Python 3.13.5**. Neither `vllm` nor `nvidia-smi` was
available. **No model was loaded and no GPU inference was executed.**

The original technical research date remains **September 21, 2026**.
This report records local checks rerun for the English localization; it does
not claim that external documentation, release status, or hardware performance
was reverified on the translation date.

## Checks actually performed

| Check | Result | What it does and does not establish |
|---|---|---|
| `python -m unittest discover -s tests -v` | **50 tests passed** | Local unit/integration tests, not model quality or GPU performance |
| `python scripts/validate_skill.py` | Passed | Package structure, local links, JSON, and Python syntax |
| `--help` for all seven Python CLI tools | Passed | CLIs load and argument parsers work |
| `bash -n scripts/serve_single.sh` | Passed | Shell syntax, not a vLLM server startup |
| Launcher without `--execute` | Passed | Plan only; no weight download or server startup |
| Benchmark sweep without `--execute` | Passed | Plan without vLLM installed; no network/load test |
| Benchmark execution against a synthetic CLI stub | Passed | Flag checks, argument lists, results/logs, key forwarding, and overwrite protection |
| Local HTTP/SSE test server | Passed | Streaming parser, actual local HTTP transport, cancellation, headers, errors, and redaction |
| Audit without vLLM/NVIDIA tools | Passed | Missing programs are documented, not presented as GPU evidence |
| SKILL front matter and three YAML configurations with PyYAML 6.0.3 | Syntax passed | Parsing, not complete semantic schema validation |
| `nginx -t` with a test parent configuration and the included server block | Passed | NGINX configuration check, not a running proxy/load test |
| English example-placeholder rejection | Passed | Launcher rejects the translated model and revision placeholders before planning or execution |
| Reference structure compared with the original | Passed | All 28 chapter section counts, table-row counts, original link targets, and inline CLI flags retained |
| Source registry compared with the original | Passed | All 57 source IDs, titles, URLs, their order, and the research date retained |

The last complete test run is in [tests/last-run.txt](tests/last-run.txt).
A rerun may take a different amount of time; suite duration is explicitly
**not a vLLM latency measurement**. The 50 tests consist of the 49 original
tests plus one regression test for the English documentation placeholders.

## What the tests cover

Memory calculations are checked against a synthetic GQA example: 128 KiB of
KV per token and one GiB for 8,192 tokens at the specified layer/head dimensions.
Tests include block rounding, raw-weight units, KV bit width, impossible fit,
and invalid inputs. The cost calculator checks arithmetic and missing
denominators; it does not fetch a price list.

Streaming tests cover role-only and usage-only events, reasoning versus visible
content, tools, refusal, UTF-8/CRLF, multiline SSE data, size limits, missing
`[DONE]`, invalid JSON events, incorrect content type, HTTP 401, redirect
rejection, socket timeouts, and an actual local CLI probe. They also check that
test prompts, answers, reasoning, and keys do not appear in emitted observation
data. The UTF-8/BOM fixture uses an English greeting with a non-ASCII character,
retaining the original Unicode test purpose.

Benchmark tests check saturation versus arrival mode, model alias versus
tokenizer source, prefix-repetition flags, exact flag detection, deliberate
key assignment, run limits, dry runs, stub execution, existing artifacts,
and process timeouts. The stub produces only files marked as synthetic tests,
**not purported benchmark results**. Those temporary files are not included
as measurement evidence.

The additional launcher test checks each English placeholder independently.
It requires an error before command planning, preserving the original safety
intent after translating the command examples.

## English localization scope and checks

The complete package is in English: `SKILL.md`, all 28 reference chapters,
README files, six templates, configuration guidance, example request text,
source annotations, and this report. The skill's explicit response-language
instruction is English. Tool messages were already English; the launcher
placeholder checks and Unicode fixture were updated where necessary.

Reference sections, table rows, original link destinations, and inline CLI
flags were compared against the original. Source IDs/titles/URLs were preserved
rather than silently replaced. A residual-language scan supplemented the
translation review; it is not a formal proof of linguistic or technical
correctness. File checksums are regenerated in [MANIFEST.json](MANIFEST.json).

Translated sample prompts can produce different token sequences and lengths.
Use a fresh baseline for prompt-based timing and cache tests; do not compare
them directly with runs using the earlier German-language fixtures.

## Still to be checked on target hardware

vLLM installation; specific flag/backend/checkpoint compatibility; actual KV,
graph, and activation peaks; quality; cache hits/isolation; TTFT/TTFA/ITL;
E2E/SLO goodput; sustained load/thermals; consumer/Spark/rented-instance
performance; multi-GPU P2P; and offload/store-failure behavior were **not**
measured here.

Prometheus `promtool` and the OpenTelemetry Collector were unavailable.
Their YAML files were parsed but not validated by the respective service tools
or through a running metrics/trace pipeline. NGINX was checked only with `-t`;
proxy buffering and cancellation propagation still need tests with an actual
upstream. Formal agent-import schema/application compatibility also depends
on the selected agent.

## Reproduce

```bash
cd vllm-operator
python scripts/validate_skill.py
python -m unittest discover -s tests -v
bash -n scripts/serve_single.sh
```

The scripts need only the Python standard library; PyYAML is not a runtime
dependency of these tools. For service validation, use the installed tools
described in [configs/README.md](configs/README.md). Load tests and server
startup require the explicit execution option.
