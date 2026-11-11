# Publication lifecycle and reported claims

## Preserve item history

Identify an item through its source identity contract, retaining provider context, managed identifier, version, and representation. Keep receipt attempts separate from item revisions. A repeated transmission of the same item/version is not a new editorial revision; a translated or syndicated story can be a distinct publication with related provenance.

Store immutable received revisions and derive the current applicable state. Do not let an older late-arriving revision replace a newer one. Compare versions according to the format/provider contract: NewsML-G2 numeric version rules differ from a generic string in ninjs. A content hash detects byte equality but does not replace publisher identity or editorial version metadata.

Keep first creation, version creation, content creation, transmission, receipt, publication, embargo, and event times separate. Do not sort a story's editorial history solely by receipt time. Preserve timezone and precision, and treat missing values as unknown.

## Apply status, correction, and embargo behavior

| Condition | Processing implication |
| --- | --- |
| Usable | Eligible under editorial status, subject to embargo and applicable rights |
| Withheld | Do not publish until the provider releases it; withdraw already published content according to the contract |
| Canceled | Treat as terminal in the NewsML-G2 item lifecycle; prevent further use and handle prior publication accordingly |
| Timed embargo | Do not release before the specified time |
| Empty NewsML-G2 embargo element | Read the editorial condition or indefinite-embargo meaning; it does not mean no embargo |
| Correction/update signal | Preserve the signal and notes; determine affected revisions from available evidence |

For NewsML-G2, prioritize the authoritative identity/version and publication-status fields in withheld/canceled updates; do not assume the rest of the content remains reliable. A cancellation may carry little useful body content while still requiring state changes. The precise recipient behavior comes from the selected specification and provider agreement.

Apply changes to user-visible text, search, summaries, extracted claims, and derived datasets. Retain the earlier record under the applicable audit/retention policy while marking its status; an archive should not accidentally republish a canceled story as current. Do not automatically infer that every individual world assertion in the earlier item is false; preserve what the correction actually says.

## Distinguish events from coverage

A real-world event, planned editorial coverage, a produced news item, and a reported claim are different objects. A conference can be canceled while planned coverage continues as a cancellation story. A story can be withdrawn while the underlying event remains scheduled. Use event status and coverage status for their declared objects; do not propagate one blindly to the other.

Keep prospective, announced, approved, started, and completed states distinct when extracting events from text. “The organization plans to open a venue” does not establish an opening already occurred. A quote attributing a claim to a spokesperson does not automatically make the publisher the originator of the asserted fact.

## Extract claims with reviewable evidence

For each candidate claim record the item/revision, exact span or structural locator, extraction method and version, participant mentions and candidate identifiers, relation/event type, participant roles, negation, modality, attribution, temporal scope, original numbers/units, and normalization rules. Preserve contradictory or ambiguous interpretations when the text does not resolve them.

Keep mention detection separate from identity resolution. A name match, shared brand, or ticker without context can be ambiguous. Co-occurrence of two organizations does not establish a partnership, acquisition, or dispute. Use evidence in the text and cited sources before asserting a relationship.

Separate classification confidence, extraction confidence, source reliability, and acceptance of the substantive claim. An item subject label says what it is about; a high extraction score says something about a method's output, under that method's calibration. Neither independently establishes truth.

## Verify lifecycle effects end to end

Use representative cases: correction after publication, cancellation after indexing, embargo with a timezone, conditional embargo, retransmission, out-of-order delivery, nested package/association, multilingual content, unresolved vocabulary code, negation, and an event whose coverage status differs from its event status. Verify the derived state and retained evidence, not just parser acceptance.

Record actual validation scope and conversion losses. The [NewsML-G2 processing model](https://www.iptc.org/std/NewsML-G2/2.35/specification/NewsML-G2-2.35-specification.html) and [ninjs guide](https://www.iptc.org/std/ninjs/userguide/) define format behavior; the claim-record and recovery recommendations here are implementation choices.
