# Merge, remote denoise and calibration boundaries

**Read when:** processing HDR/panoramas, using a GPU service, or fitting camera profiles.

The CLI exposes `merge hdr`, `merge panorama` and `merge hdr-panorama`. Bracket grouping, alignment, deghosting, projection, boundary warp, cropping and edge filling are separate decisions. Confirm the input sequence before executing; grouping unrelated frames can produce a plausible but invalid result. Start with `--preview OUT.png` to inspect a bounded result without creating a derived file beside the originals. Full merges normally write an HDR/Pano DNG next to the first input.

`synth-merge` generates procedural input fixtures. That is useful for testing installation and pipeline behavior without disclosing a private shoot; it is not evidence that a difficult real-world bracket will merge well.

## Denoise service security

`denoise-serve` runs installed model inference. It defaults to loopback at port 7990, supports CPU/GPU selection, a models directory, a shared-token environment variable and a concurrency limit. The reviewed service uses plain TCP, not an automatically encrypted HTTPS API. Restrict it to a protected VPN/LAN or a narrowly firewalled interface; do not expose it publicly because it has a token. Client variables include `LIGHTCRAFT_DENOISE_URL` and `LIGHTCRAFT_DENOISE_TOKEN`.

Before enabling it, record model identity, installation source, accepted data exposure, execution device and failure behavior. Model installation/download, network listening and remote transmission are distinct approvals. GPU selection or a running listener does not prove useful inference throughput; test a small image and observe memory and result quality.

## Camera calibration

`calibrate` fits per-camera profiles from RAW files and embedded camera JPEGs, with bounded sampling options. By default it writes into the profile directory the current user subsequently consumes. Use an explicit output directory for experiments and do not silently replace production profiles. Store camera models, input hashes, count, profile output and before/after references. A fitted profile's success on its fitting images is not a validation on independent images.

## Evidence

- [light-cli](https://github.com/storytold/lightcraft/blob/main/apps/lightcraft-cli/src/main.rs)
