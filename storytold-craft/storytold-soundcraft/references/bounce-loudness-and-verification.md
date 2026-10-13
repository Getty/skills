# Bounce completion, loudness metrics and final checks

**Read when:** delivering audio or deciding whether a mix is actually valid.

The documented MCP `bounce_mix` exports WAV/AIFF/FLAC and returns peak dBFS plus integrated LUFS. Do not relabel peak dBFS as true peak unless that specific measurement is actually exposed. Loudness requirements depend on the delivery brief; do not force a universal LUFS target onto every mix.

Specify output range, format, bit depth/sample rate where supported, and channel policy. A bounce with the wrong start/end or muted routing can still be a valid audio file. Verify duration, channel layout, sample rate, non-silence where expected, level metrics and a listening sample when tools/hardware allow it.

Headless operation has no audio device. Its output file is the evidence of rendered audio, not a successful transport command. A waveform/level summary is not a substitute for listening when perceptual defects such as clicks, distortion or unwanted processing are material; report when no listening check was performed.

`save_session` refuses to replace another existing file unless `replace:true` is explicit. Do not automatically add that override on error. Use a new working path, retain associated media and reopen the session to verify persistence independently from the bounced file.

For final handoff, provide the rendered mix, editable session/media package if requested, signal/format specification, and measured—not guessed—peak/loudness information. Record missing-media, plugin, routing or listening checks that remain unresolved.

## Evidence

- [sound-mcp](https://github.com/storytold/soundcraft/blob/main/docs/mcp.md)
- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
- [soundcraft-readme](https://github.com/storytold/soundcraft/blob/main/README.md)
