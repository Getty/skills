# Read-only registry probe

Python 3.10+, standard library only. It performs `/v2/` GET and optionally a manifest HEAD, without credentials or automatic redirects. HTTPS verification is on by default; supply `--ca-file` for a private CA. HTTP requires explicit `--allow-http` for a controlled lab.

```sh
python registry_probe.py https://registry.example.com
python registry_probe.py https://registry.example.com --repository team/app --reference APPROVED_TAG --ca-file /secure/registry-ca.crt
python registry_probe.py http://127.0.0.1:15000 --allow-http
```

Exit code 0 means the requested header probes returned 200, **not** that uploads or blob integrity passed. Exit code 2 means at least one expected-form 401 was observed and no other failing status was returned. Exit code 1 is a failed/unexpected probe. Review hostname/auth-realm information before sharing output. Location headers are omitted because redirects can contain presigned credentials.

No authentication exchange, pagination, OCI graph traversal, blob download, push, delete, GC, retry, or credential helper integration is implemented. Use the protocol references and a maintained registry client for those workflows. The conservative reference syntax can reject legitimate less-common inputs; expand it deliberately with tests rather than treating it as the entire OCI naming specification.
