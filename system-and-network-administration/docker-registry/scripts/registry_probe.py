#!/usr/bin/env python3
"""Read-only unauthenticated registry header probe, Python 3.10+.

No redirects or credentials. HTTP requires explicit opt-in. This does not
validate blob integrity, successful authentication, or writable storage.
"""
from __future__ import annotations
import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

ACCEPT = ', '.join((
    'application/vnd.oci.image.index.v1+json',
    'application/vnd.oci.image.manifest.v1+json',
    'application/vnd.docker.distribution.manifest.list.v2+json',
    'application/vnd.docker.distribution.manifest.v2+json',
))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def inspect(opener, url: str, method: str, timeout: float) -> dict:
    req = urllib.request.Request(url, method=method, headers={'Accept': ACCEPT})
    try:
        response = opener.open(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        selected = {}
        for key in ('Content-Type', 'Content-Length', 'Docker-Content-Digest',
                    'Docker-Distribution-Api-Version', 'WWW-Authenticate'):
            if response.headers.get(key) is not None:
                selected[key] = response.headers.get(key)
        # Location is intentionally omitted: it can contain presigned credentials.
        return {'url': url, 'method': method, 'status': response.code, 'headers': selected}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', help='Registry origin, e.g. https://registry.example.com')
    parser.add_argument('--repository')
    parser.add_argument('--reference', help='Tag or digest; required with --repository')
    parser.add_argument('--ca-file')
    parser.add_argument('--allow-http', action='store_true', help='Explicit approval for an HTTP-only lab')
    parser.add_argument('--timeout', type=float, default=10.0)
    args = parser.parse_args()
    origin = urllib.parse.urlsplit(args.base)
    if origin.scheme not in ('http', 'https') or not origin.hostname:
        parser.error('base must be an HTTP(S) origin')
    if origin.username is not None or origin.password is not None or origin.query or origin.fragment or origin.path not in ('', '/'):
        parser.error('base must have no credentials, query, fragment, or path prefix')
    if origin.scheme == 'http' and not args.allow_http:
        parser.error('HTTP requires explicit --allow-http; prefer TLS')
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if bool(args.repository) != bool(args.reference):
        parser.error('--repository and --reference must be supplied together')
    if args.repository and (not re.fullmatch(r'[a-z0-9._/-]+', args.repository)
                            or any(part in ('', '.', '..') for part in args.repository.split('/'))):
        parser.error('repository is outside this probe\'s conservative supported name syntax')
    if args.reference and not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.:-]*', args.reference):
        parser.error('reference is outside this probe\'s supported tag/digest syntax')
    try:
        context = ssl.create_default_context(cafile=args.ca_file)
        opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=context))
        base = urllib.parse.urlunsplit((origin.scheme, origin.netloc, '', '', '')).rstrip('/')
        rows = [inspect(opener, base + '/v2/', 'GET', args.timeout)]
        if args.repository:
            path = '/v2/' + urllib.parse.quote(args.repository, safe='/') + '/manifests/' + urllib.parse.quote(args.reference, safe=':')
            rows.append(inspect(opener, base + path, 'HEAD', args.timeout))
        print(json.dumps({'observations': rows,
                          'note': '401 may be an expected authentication challenge; no credentials were attempted.'}, indent=2))
        # 2 means an authentication challenge was observed, not full validation.
        if any(row['status'] not in (200, 401) for row in rows):
            return 1
        return 2 if any(row['status'] == 401 for row in rows) else 0
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f'Probe failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
