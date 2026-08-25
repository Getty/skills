# Stream Design and Run of Show

The stream as a produced thing: what is on screen, what happens when, and what stops it going
wrong live.

## Visual identity

Three assets carry a channel's look: the **offline banner** (what non-followers see most),
the **waiting/BRB screen**, and the **in-stream overlay**. Keep them one system — same
typeface, same 2–3 colours, same corner radius.

Overlay rules that hold up:
- **The content is the picture.** Overlay is a frame, not a dashboard. If your webcam,
  alerts, chat box, recent-sub ticker, goal bar and sponsor banner all fight for space, the
  viewer looks at none of them.
- **A permanent "what is happening" line.** One text source, updated per segment. This is what
  converts a Discovery Feed passer-by.
- **Readable at 480p and on a phone.** Test by shrinking the OBS preview to postcard size.
- **Safe area for vertical.** With Dual Format, anything near the horizontal edges is gone in
  the 9:16 crop. Design the vertical layout separately — see `broadcasting-and-obs.md`.

## Run of show

Structure beats spontaneity for retention, and it is what lets you stream tired. A default
shape:

| Phase | Length | Scene | Purpose |
|---|---|---|---|
| Waiting | 2–5 min | `5 WAITING` | Lets notifications land and early arrivals gather; music, no mic |
| Welcome | 3–5 min | `4 CAM` | Who you are, what today is, why it matters |
| Main block A | 30–45 min | `1 MAIN` / `2 MAIN + CAM` | The actual thing |
| Break / chat | 5–10 min | `4 CAM` | Answer chat, ad break if you run one |
| Main block B | 30–45 min | `1 MAIN` | |
| Wrap + raid | 5–10 min | `4 CAM` / `6 ENDING` | Recap, what's next, raid out |

Full fillable version: `../templates/run-of-show.md`.

## Segment design

- Every segment needs a **statable goal** ("get the parser to compile", "beat this boss",
  "answer three chat questions"). Goals create tension; tension creates retention.
- **Announce the next segment before the break** — it is the reason someone stays through it.
- Keep a **parking lot**: chat questions you will answer at the next break. Saying "I'll get
  to that at the break" is better than ignoring or derailing.

## Failure drills

Practise these once, so they are muscle memory:

| Failure | Response |
|---|---|
| Something private appears on screen | Push-to-mute + switch to `4 CAM` in one motion; then fix; then say what happened |
| Stream drops | Scene `5 WAITING`, restart stream, post in Discord |
| Capture goes black | Re-select the window in `MAIN WINDOW`; keep talking on camera meanwhile |
| Hate raid | Shield Mode hotkey — see `moderation-and-safety.md` |
| Guest misbehaves | Remove from Stream Together; state the rule; move on |

## Ending

End on time, every time. The last 5 minutes should say what you did, what is next, and where
to find you between streams — then raid. An abrupt ending costs you the return visit.
