# Verification scope and migration boundaries

**Read when:** comparing ArtCraft-X with ArtCraft or validating an experimental integration.

Do not infer compatibility of project files, preferences, credentials, model options or backend requests merely from the similar names. Compare the relevant manifests/types/callers at pinned revisions and test a small authorized task before migrating real work.

A useful verification ladder is: repository source inspected; development build completed; native app launched; IPC operation observed; authenticated job accepted; result retrieved; output inspected; restart/recovery tested. Record each level separately. None of the earlier levels implies the later ones.

When the integration uses a GUI, capture semantic application/job state where available as well as visual evidence. A screenshot of a completed thumbnail does not prove the full-resolution output was saved or can be reopened. When it uses native/SDK calls, validate the exact argument and result types rather than translating a UI label into guessed JSON.

For delivery, identify which product actually performed the work and which specialized editor subsequently processed the result. Do not label another tool's output as ArtCraft-X output. Keep limitations tied to the actual reviewed/installed version and update this skill's evidence ledger when the project publishes a supported operator interface.

## Evidence

- [artcraftx-readme](https://github.com/storytold/artcraftx/blob/main/README.md)
- [artcraftx-ipc](https://github.com/storytold/artcraftx/blob/98c2a48940aa0a54604637f665ee539c122fa707/crates/artcraftx/src/lib.rs)
