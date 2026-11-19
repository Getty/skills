<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Containers and integrity

Evidence: official RUML 1.0.0 (2026-11-15), commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. File `$specVersion` is `"1.0"`.
Normative requirements are summarized from the pinned sources. **Implementation recommendation** describes runtime policy; **Snapshot discrepancy/gap** marks a conflict or incomplete contract.

## Contents

- [Exact formats and extensions](#exact-formats-and-extensions)
- [Manifest and archive structure](#manifest-and-archive-structure)
- [Canonicalization and hash representations](#canonicalization-and-hash-representations)
- [Hash verification](#hash-verification)
- [Detached signatures and trust](#detached-signatures-and-trust)
- [Manifest self-protection](#manifest-self-protection)
- [Encryption](#encryption)
- [Ordered processing](#ordered-processing)
- [Versions and bundled references](#versions-and-bundled-references)
- [Limits and runtime controls](#limits-and-runtime-controls)
- [Evidence and coverage](#evidence-and-coverage)

## Exact formats and extensions

| Artifact | Extension | Representation | Discriminator |
| --- | --- | --- | --- |
| Rulemap | `.ruml` | UTF-8 JSON | `RUML` |
| Capability sidecar | `.ruml-ext` | UTF-8 JSON | `RUML-EXT` |
| Evaluation result | `.ruml-result` | UTF-8 JSON | `RUML-Result` |
| Container | `.rumlc` | ZIP archive | Manifest `$format: "RUML-Container"` |

Use `.rumlc`, not an invented `.ruml-container` extension. A bare JSON document is valid without a container; container layers add packaging and protection without changing its content model. Current MIME usage is `application/x-ruml`; `application/vnd.rulemapping.ruml+json` is described as future, contingent on IANA registration. [I1][I2]

Hash, signature, and encryption layers are optional and independent. A `.rumlc` can be a bundle without cryptography, and may contain only a sidecar or only a result as its RUML content. An asset-only archive is insufficient. [I2][I3]

Bare documents have no embedded file-wide integrity protection. Fields such as `metadata.hash` and `metadata.integrity` are not part of the current data model. This does not remove reference-specific hashes such as EXT `$base.hash`, result `rumlReference.hash`, or text `digest`. [I1][I10]

## Manifest and archive structure

A container requires exactly one root `manifest.json` and at least one content file of type `ruml`, `ruml-ext`, or `ruml-result`. The manifest is JSON and requires `$format`, `$specVersion`, `created`, and `files`. [I3]

`files` is a map from relative logical file path to its entry. Every content file has one entry. An encrypted entry is keyed by the plaintext's logical path even though plaintext is absent. Signature files and ciphertext files are referenced from that entry and have no separate content entries. [I3]

| Entry field | Requirement | Meaning |
| --- | --- | --- |
| `type` | Required except for manifest's own entry | `ruml`, `ruml-ext`, `ruml-result`, or `asset` |
| `uri` | Optional, only for type `ruml` | Immutable RUML version URI, required when a bundled file is an anchor target |
| `hash` | Optional object | `algorithm` plus lowercase-hex `value` |
| `signature` | Optional object or array | Detached signature locator(s) and format(s) |
| `encryption` | Optional object | Ciphertext locator and format, optional algorithm |

The documented directory conventions are root for rulemaps, `ext/`, `results/`, `assets/`, `signatures/`, and `encrypted/`. Signature and encryption paths must mirror the source path: `ext/review.json` corresponds to `signatures/ext/review.json.sig` or `encrypted/ext/review.json.enc`. [I3]

Container examples use `.json` for internal RUML documents. Dispatch using manifest type and document discriminator; do not assume every internal filename ends with its bare-file extension. [I3]

**Snapshot integration detail:** capability container paths have stricter prefixes: context uses `.context/`, and text uses `.texts/`. The general `assets/` convention does not override those payload requirements. Include such files in the manifest as assets at their actual required paths. [I11]

On opening, verify all listed/referenced files exist, using ciphertext rather than plaintext for encrypted entries. A parser must not process an archive member that is neither listed nor referenced; a warning is recommended for such members. [I3]

There is no published container-manifest JSON Schema among the three schemas at this pin. Implement the manifest obligations from Chapter 7 and do not claim that validating a `.ruml` payload validates its ZIP wrapper. [I12]

## Canonicalization and hash representations

JSON hashing and signing use RFC 8785 JCS over the document, not its original formatted bytes. JCS sorts object keys by UTF-16 code units, removes insignificant whitespace, and uses the specified ECMAScript/IEEE 754 number serialization. Array order remains intact. [I4]

Use a conforming canonicalization implementation. Sorting keys with a language's default comparator plus ordinary JSON serialization is not enough evidence of JCS conformance. Important boundaries include non-ASCII key ordering, number formatting, escaping, and rejection of inputs that cannot be represented under the JCS requirements.

Pretty printing or reordering object members does not change a canonical hash. Reordering an array, changing a number's actual value, or changing string whitespace does. Do not normalize Unicode, trim text, or reorder capability/child arrays as an undocumented preprocessing step.

Non-JSON assets use their raw bytes. A structured text entry's `digest` instead hashes only its `content` JSON tree in JCS form. The base-file hash hashes the base file, not its merged sidecars or an extracted subtree. [I4][I11]

| Location | Representation | Algorithm vocabulary at this pin |
| --- | --- | --- |
| Manifest file `hash` | `{ "algorithm": ..., "value": ... }` | SHA3-256 support mandatory; Chapter 7 allows others |
| EXT `$base.hash` | `<algorithm>:<64 lowercase hex>` | Schema permits `sha3-256`, `sha256`, `blake3` |
| Result `rumlReference.hash` | Same string form | Same three algorithms |
| Context `hash` | Same string form | Same three algorithms |
| Structured text `digest` | `sha3-256:<64 lowercase hex>` | SHA3-256 only |

Do not reuse the open manifest-algorithm policy to accept an unsupported name in the closed sidecar/result/context string pattern. Conversely, do not impose those three names as the complete Chapter 7 algorithm registry. [I4][I11][I12]

## Hash verification

A manifest hash requires `algorithm` and lowercase hexadecimal `value`. Every parser must support SHA3-256; its digest has 64 hexadecimal characters. `sha3-256` is the serialized identifier; do not substitute `sha-256` or confuse SHA3-256 with SHA-256. [I4]

If a manifest entry contains a supported hash, verify it regardless of document status. A draft flag does not bypass integrity checking. Mismatch is an error and the file is considered compromised. An unsupported hash algorithm requires a warning and skipping that integrity check. [I4]

**Snapshot discrepancy:** §3.2.4 says new containers must use SHA3-256, while §7.3 recommends it and allows any other algorithm. Author portable new containers with SHA3-256, which satisfies both statements; report the conflict instead of claiming the alternative-algorithm policy is unambiguous. [I4][I10]

Hash verification proves consistency with an expected digest, not publisher identity. A party able to replace both content and an unsigned manifest can replace the digest too. Separate `verified`, `mismatched`, and `not verified/unsupported` outcomes; the last is not a successful check. [I4]

**Implementation recommendation:** applications requiring verified integrity may refuse to use an unverified file under their local trust policy. Report that as application policy, not as the standard's required response to every unknown algorithm.

## Detached signatures and trust

Signatures are always detached: content and signature occupy different files. Sign canonical JSON bytes for JSON files and raw bytes for non-JSON assets. The signature descriptor needs `path` and `format`. [I5]

Reserved format identifiers are `jws-detached` and `cms-detached`. Other formats must use a reverse-domain identifier, such as a provider's `org.example/custom-signature`. RUML does not require every parser to implement JWS or CMS; supported formats are implementation-specific. [I5]

For multiple signatures, `signature` is an array. An optional `signer` is a display identifier; it is not a trusted assertion of identity. Derive cryptographic identity through the signature/key/certificate mechanism and the application's trust policy. [I5]

Unsupported signature format means explicitly not verified, and the file must not be treated as signed. A recognized but invalid signature is an error. Do not equate finding a `.sig` file with verification. [I5]

Key discovery and trust are outside the format. The specification recommends certificate-chain, timestamp, and revocation checking, and requires full chain/revocation verification for systems handling legally binding documents. Application acceptance still needs an explicit trusted-signer policy. [I5]

**Implementation recommendation:** distinguish mathematical signature validity, trusted signer identity, expected signing responsibility, certificate validity at the relevant time, and legal/domain review. A valid signature does not prove the rulemap is correct or that the source's statements are true.

Use the selected format's standard signing API correctly. Signing a digest, signing canonical content, and signing a digest twice are different operations; do not turn the illustrative qualified-signature workflow into an undocumented custom wire format.

## Manifest self-protection

The manifest may list itself as `files["manifest.json"]` to carry a hash/signature descriptor. Before hashing **or signing** it, remove that entire entry from `files`, then canonicalize the remaining manifest. Do not remove unrelated file entries or the `files` object. [I3][I5]

Insert the self-entry after computing the signature/hash. Verification repeats the same exclusion. Hashing the stored manifest with its self-entry still present creates a circular and incorrect calculation. [I5]

A verified manifest signature protects its other file descriptors and the hashes they contain. That binds the corresponding hashed content after those hashes are checked; it does not magically authenticate bytes of entries with no hash or separately verified signature. [I4][I5]

The specification recommends signing the manifest when any content file is signed. File signatures identify responsibility for individual content; manifest protection binds the package descriptions and prevents substitution of its hash declarations. [I3][I5]

**Implementation recommendation:** report a protection matrix for each logical file, including whether it is covered by a verified own signature, a trusted manifest plus verified content hash, neither, or an unsupported layer. Do not label the entire archive trusted because one unrelated file verified.

## Encryption

Encryption is file-level. Store ciphertext under the mirrored `encrypted/` path with `.enc`; the plaintext must not simultaneously be present in the container. Manifest entries still use the plaintext's logical path. Field-level encryption is a capability/runtime concern. [I6]

The descriptor requires `path` and `format`; `algorithm` is optional and interpreted by the named encryption format. Reserved formats are `jwe` and `cms-enveloped`; other formats require reverse-domain identifiers. Key acquisition/distribution is outside RUML. [I6]

Hash and signature always refer to plaintext, including when ciphertext is what the ZIP stores. Decrypt first, then verify the signature and hash against the recovered canonical JSON/raw content. Do not change those checks to cover ciphertext. [I6]

An unsupported encryption format or absent key makes that file unreadable and must be reported. Other readable files remain processable; one undecryptable member must not invalidate access to the whole container. A dependent evaluation may nevertheless lack a required input/file. [I6]

**Snapshot gap:** the overview describes layer independence even for the manifest, but the structure requires root `manifest.json` and consuming begins by reading it; no encrypted-manifest bootstrap is specified. For interoperable authoring, keep the manifest readable rather than inventing an encrypted-only index scheme. [I2][I3][I7]

**Implementation recommendation:** remove temporary plaintext securely according to the deployment's storage model, avoid logging decrypted sensitive data, and keep key material separate from documents. These controls are not serialized by a standard RUML encryption-policy object.

## Ordered processing

The fixed order applies to whichever layers are present. [I7]

| Creation | Consumption |
| --- | --- |
| Canonicalize plaintext and compute requested hash | Read and validate the manifest |
| Create detached plaintext signature | Verify a manifest signature first if present |
| Encrypt plaintext; remove its archive plaintext copy | For each file, decrypt if needed |
| Build manifest with descriptors | Verify its signature if present |
| Optionally hash/sign the manifest last | Verify its hash if present |

Manifest algorithm declarations cannot be treated as authenticated until its signature has been verified under the chosen trust policy. Even an unsigned manifest needs bounded parsing to identify its declarations; parsing it is not equivalent to trusting it. [I7]

| Condition | Standard response |
| --- | --- |
| Hash mismatch | Error |
| Invalid supported signature | Error |
| Unsupported hash | Warning; check skipped |
| Unsupported signature format | Report unverified; do not treat file as signed |
| Unsupported encryption / missing key | Report unreadable file; preserve access to other files |
| Unlisted and unreferenced member | Do not process; warning recommended |

Keep protection outcomes separate from document schema/semantic validity. A cryptographically intact file may contain invalid RUML, and a valid rulemap may have no authenticated publisher.

## Versions and bundled references

An archive may contain several versions, each as its own manifest file entry, with independent protection. Subdirectory labels such as `1.0/` are for people; parsers must take the normative version from the RUML file's `metadata.version`. `replaces` and `replacedBy` describe metadata version relationships. [I8]

When bundled files are targets of cross-file node anchors, each needs its immutable version `uri` in its manifest entry. URIs must be unique within the container and may appear only on `type: "ruml"` entries. Resolve a matching bundled URI before fetching remotely. [I3]

A multi-version container does not authorize silently selecting the latest file for a hash-bound result or sidecar. Select the precise requested version and apply its own validation and protection checks.

## Limits and runtime controls

Bare RUML has no inherent size maximum; implementations should handle files up to 100 MB. Containers should not exceed 1 GB of total uncompressed content. Parsers may enforce smaller container limits, but must document them. These are different statements, not a single mandatory global cap. [I1][I3]

**Implementation recommendation:** bound compressed and uncompressed bytes, entry counts, compression ratio, JSON depth, string size, expression work, signature attempts, network fetches, and elapsed time. Validate declared sizes against actual decompressed data rather than trusting archive headers alone.

**Implementation recommendation:** reject or quarantine ambiguous archive paths, traversal components, absolute paths, unsafe links, and duplicate member names. Resolve referenced members inside a controlled extraction root. These are archive-processing controls beyond the listed RUML validation rules.

Do not execute extracted assets or discover credentials from arbitrary archived files. Resolve included-document URIs with configured network policies and caching; preserve immutable identity and prevent a local path from escaping the archive's resource boundary.

Record lower limits and unsupported algorithms/formats in capability documentation. A resource limit or inaccessible key is an operational condition, not evidence that a document's underlying rule is false.

## Evidence and coverage

Chapter 7 supplies prose and manifest examples; the pinned repository has no `tests/07-container` suite or manifest schema. General-format tests cover UTF-8 and JSON. State separately whether work verified schema shape, canonical digest agreement, signatures with trusted keys, decryption, or merely reviewed examples. [I12]

[I1]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-1-general-properties.md
[I2]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-1-overview.md
[I3]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-2-structure.md
[I4]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-3-hashing.md
[I5]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-4-signatures.md
[I6]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-5-encryption.md
[I7]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-6-processing.md
[I8]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-7-versioning.md
[I10]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-2-data-types-and-formats.md
[I11]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities
[I12]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4
