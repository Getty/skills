# Development example. Pin a tested base digest/package version for deployment.
# This uses the DISTRIBUTION gearmand, not necessarily the 2.1 source baseline.
FROM debian:trixie-slim
RUN printf '#!/bin/sh\nexit 101\n' > /usr/sbin/policy-rc.d \
    && chmod +x /usr/sbin/policy-rc.d \
    && apt-get update \
    && apt-get install -y --no-install-recommends gearman-job-server python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 gearman-lab \
    && useradd --uid 10001 --gid 10001 --no-create-home gearman-lab \
    && mkdir -p /var/lib/gearman-skill \
    && chown 10001:10001 /var/lib/gearman-skill
COPY . /opt/gearman-skill/
ENV PYTHONDONTWRITEBYTECODE=1
USER 10001:10001
WORKDIR /opt/gearman-skill
EXPOSE 4730
CMD ["/usr/sbin/gearmand", "--listen=0.0.0.0", "--port=4730", "--queue-type=libsqlite3", "--libsqlite3-db=/var/lib/gearman-skill/queue.sqlite", "--job-retries=3", "--verbose=NOTICE", "--log-file=stderr"]
