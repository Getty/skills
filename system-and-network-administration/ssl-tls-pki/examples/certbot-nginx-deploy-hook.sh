#!/bin/sh
# REVIEWED TEMPLATE: executes a real local configuration check and reload when run.
# Install only through an approved change; run as the intended privileged service.
# This intentionally contains no certificate copying, secret output or fallback.
set -eu
nginx -t
systemctl reload nginx
