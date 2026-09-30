# Local tests

From the skill directory: `python -m unittest discover -s tests -v`.

The suite requires Python 3.10+ and only the standard library. Integration tests
run a short-lived HTTP server on a randomly assigned **loopback address**.
No internet, model weights, or GPU are required. A temporary executable `vllm`
stub checks the benchmark wrapper; it does not measure model performance.
Temporary files are cleaned up. POSIX-specific Bash/executable-path tests are deliberately
skipped on other systems.

`last-run.txt` contains the documented successful run of this package version.
The [validation report](../VALIDATION.md) explicitly separates this evidence
from outstanding GPU, vLLM, quality, and service tests.
