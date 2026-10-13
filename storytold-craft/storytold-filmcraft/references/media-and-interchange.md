# Media identity, offline assets and project interchange

**Read when:** importing media, relinking a project, or transferring an edit between applications.

Probe each unfamiliar source before import. Record path, size/hash, stream types, dimensions, frame rate, duration, sample rate and channel layout as available. A familiar extension does not prove codec/profile support. Image-sequence import is explicit: a numbered still can be treated as a sequence only under the intended mode.

Import produces project items; placing an item on a track creates timeline clips. Preserve that distinction when selecting targets. Keep source files immutable during an agent job and deliver a manifest of dependencies, not only a `.fcproj` file. Relative-path behavior and relinking rules must be established for the actual project before moving its directory.

Offline, missing and unreadable media can be rendered as placeholders. Reopening a project successfully therefore does not establish that all dependencies are available. Inspect media state and the `offlineMedia` field in exports/jobs; verify a few representative frames and audio segments from each important source.

## Native versus interchange deliverables

Use `.fcproj` for the native editable working project. Upstream describes interchange through formats such as FCP XML/FCPXML, OTIO, EDL, AAF and OMF; do not infer support for a Premiere `.prproj` project. Choose a format based on the target application's accepted semantics, not a similar filename.

Compare a transfer manifest: sequence rate and duration, track count/order, clip boundaries, source offsets, speed/reverse, effects, transitions, captions and audio gain. A transfer that preserves cuts but drops effect parameters is a partial transfer, even when both applications open it normally. Keep a rendered reference and list known losses. Never present upstream feature-parity percentages as a guarantee about a specific professional project.

## Evidence

- [film-agents](https://github.com/storytold/filmcraft/blob/main/docs/agents.md)
- [filmcraft-readme](https://github.com/storytold/filmcraft/blob/main/README.md)
- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
