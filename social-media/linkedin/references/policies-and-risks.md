# Policies and Risks

What gets accounts restricted, what gets posts suppressed, and what to never recommend.

## Account-level risks

| Behaviour | Risk |
|---|---|
| **Third-party automation** (auto-connect, auto-view, auto-message, scrapers) | Violates the User Agreement. Escalates from feature restriction to permanent loss. LinkedIn has litigated this aggressively |
| **Scraping** profile data | Same, plus GDPR exposure — see `germany-legal.md` |
| **Fake or embellished profile** (roles never held, invented employers) | Account action, and in DACH a potential Urkundenfälschung/fraud question in a hiring context |
| **Bulk identical DMs** | Spam classification; sender reputation drops silently before anything visible happens |
| **Multiple accounts** for one person | Prohibited |
| **Engagement pods** | Detected; posts get classified as low quality |
| **Buying followers or engagement** | Detected; contaminates your own analytics permanently |

There is no appeal path that reliably restores a permanently restricted account. **Treat the
account as rented, not owned**: export your data regularly, keep an email list or another
channel you control.

## Post-level suppression

Not bans — just quiet non-distribution:

- Engagement bait ("comment YES and I'll send it")
- Bare reposts with no commentary
- Repetitive templated content
- Edited immediately after publishing
- Mass mentions of uninvolved people
- Content classified as low-quality: no substance, obvious AI boilerplate, pure self-promotion

## Content that creates real-world liability

- **Confidential or customer information.** The most common serious error in build-in-public
  posting: a screenshot with a customer name, an internal metric, an unreleased feature.
  Screenshot discipline is a professional obligation.
- **Naming people you are arguing with.** Legally borderline (Persönlichkeitsrecht in DE),
  reputationally worse. Keep the example, drop the name.
- **Statements about your employer.** German employment law protects opinion but not
  disparagement or breach of confidentiality; see `germany-legal.md`.
- **Undisclosed advertising.** A labelling duty, not a courtesy — `germany-legal.md`.
- **Invented specifics.** A fabricated number in a professional post is a credibility failure
  and, in a commercial context, potentially an unfair-competition problem.

## Platform data practices worth knowing

- **AI training on member data**: LinkedIn began using EU member data (public posts, profile
  data, interactions) to train generative AI models on **2025-11-03**, opt-out rather than
  opt-in, with an objection mechanism in settings. Several European data protection
  authorities recommended objecting. If a client asks, tell them the setting exists and where.
- **Data export** exists and should be run periodically (see `analytics.md`).

## The honest disclaimers to give a client

1. Anything that promises to automate LinkedIn growth is offering to risk your account.
2. Reach fluctuates for reasons no one outside LinkedIn can see; a bad month is not proof of
   a penalty.
3. Advice older than about a year on limits, links or format performance should be re-verified
   before it is acted on.
