# Executable examples and integration guide

Read [validation](../VALIDATION.md) first. Commands below are explicit operator actions;
do not point them at production or an unapproved existing service.

## Offline contract examples

From the skill root, no Gearman server or binding is needed:

```sh
perl examples/perl/contract_cli.pl < assets/contracts/sample-request.json
php examples/php/contract_cli.php < assets/contracts/sample-request.json
python3 -B -m unittest discover -s tests -v
```

The successful result has sum **27**. Python, Perl and PHP use the same small request
contract and success envelope. Python rejects duplicate JSON keys; the standard Perl/PHP
decoders do not. Their parser depth/number representation policies can also differ.
The schema documents structural rules; byte budgets and lexical integer-token rules are
additional runtime checks. This is not an all-inputs parser-equivalence claim.

## Isolated automated server lab

```sh
python3 -B scripts/run_lab.py
python3 -B scripts/run_lab.py --execute
python3 -B scripts/run_lab.py --execute --persistence
```

The first command only prints a plan. Execution requires installed `gearmand`; the
persistence mode additionally requires its SQLite backend. The runner creates and stops
its own server and uses temporary storage. It never installs dependencies.

## Manual local integration

On an explicitly prepared private test server, use separate terminals:

```sh
python3 -B examples/python/worker.py --host 127.0.0.1 --port 4730
python3 -B examples/python/client.py --host 127.0.0.1 --port 4730 < assets/contracts/sample-request.json
```

Replace the worker with `perl examples/perl/worker.pl` or `php examples/php/worker.php`
after installing and validating the appropriate native binding. Perl's endpoint variable
is `GEARMAN_SERVER=127.0.0.1:4730`; PHP uses `GEARMAN_HOST` and `GEARMAN_PORT`.
Their clients are `examples/perl/client.pl` and `examples/php/client.php`, with optional
`--background`. Native adapters are plaintext/private-network examples; they do not
pretend to configure TLS across incompatible binding versions.

Python and Perl reject bad jobs through a native failure path. The PHP callback instead
returns a completed domain-error envelope with `ok: false`. Successful interoperation
therefore does not imply identical failure signaling. The simple sum has no remote effects.

For a **local-only** transaction/idempotency demo, give the Python worker
`--result-db /a/private/local/path/results.sqlite`. A counter increment and result are
committed together. Concurrent repeats of the same request return the stored result;
a different business payload under the same ID is rejected. This does not make an HTTP
call, email delivery or another database transaction exactly-once. Do not share this SQLite
file over a network filesystem as a distributed result service.

## C/libgearman example

The C pair handles opaque bytes using `gearman_skill.bytes.v1`, not JSON sum jobs.
With matching installed development headers and library:

```sh
cc -std=c11 -Wall -Wextra -Wpedantic examples/c/client.c -lgearman -o /tmp/gearman-client-example
cc -std=c11 -Wall -Wextra -Wpedantic examples/c/worker.c -lgearman -o /tmp/gearman-worker-example
/tmp/gearman-worker-example 127.0.0.1 4730
printf 'example' | /tmp/gearman-client-example 127.0.0.1 4730 request-001
```

Adjust include/library paths to the actual development package. These files were not
compiled locally because the headers/library were absent. The client expects its echo
worker's final-only response; it is not a general intermediate-event client.

## Deployment examples

The [Compose file](../assets/containers/compose.yaml) builds from the package root and
uses distribution packages, not an asserted 2.1 binary. Review it before an explicit
`docker compose -f assets/containers/compose.yaml up --build` in an isolated environment.
The [systemd](../references/systemd-containers.md) and [Kubernetes](../references/kubernetes.md)
chapters explain the unapplied templates, ownership constraints and missing deployment gates.
