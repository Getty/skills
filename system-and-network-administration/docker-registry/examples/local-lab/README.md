# Loopback-only registry lab

This is an unauthenticated **local HTTP lab**, bound only to `127.0.0.1:15000`. Do not expose it to a network or put private images in it. The `registry:3.1.2` tag is a documented review-date snapshot; recheck/pin a digest before controlled deployment. Requires a local Linux-container Engine and Compose.

```sh
docker compose -f compose.yaml config -q
docker compose -f compose.yaml up -d
curl --fail http://127.0.0.1:15000/v2/
```

Expected API response is `{}` with status 200. A subsequent isolated smoke test can tag and push an already approved local image to `localhost:15000/lab/IMAGE:TAG`; substitute a real reviewed source image rather than copying an arbitrary internet image. Verify the digest after push and after pull from another disposable client.

Loopback handling of insecure registries depends on the actual Engine/platform policy. A remote daemon's `localhost` is not your laptop. Do not add broad insecure-registry exceptions or publish port 5000 publicly to make this lab work.

Stop with `docker compose -f compose.yaml down`. The named data volume is retained. Deletion is disabled in this configuration; destructive API/GC experiments require a separate disposable copy, explicit review, and the maintenance reference.
