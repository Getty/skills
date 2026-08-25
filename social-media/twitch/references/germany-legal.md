# Germany/DACH — Broadcasting Licence, Legal Notice (Impressum), Data Protection

**Not legal advice.** This states the law and the authorities' published guidance as verified
2026-08, so an agent stops giving US-default answers. Anything with money or a deadline
attached belongs to a Rechtsanwalt/Steuerberater or the competent Landesmedienanstalt.

## 1. Do you need a broadcasting licence? (Germany, MStV)

A regular, scheduled livestream is legally **Rundfunk** (broadcasting) in Germany — not a
website. That is the fact most non-German guides get wrong.

**§ 54 Abs. 1 MStV** (in force since 2020-11-07) makes a programme **licence-free** if it

- reaches **fewer than 20,000 simultaneous users on average over six months**, **or**
- has only minor significance for individual and public opinion-forming, **or**
- is broadcast for a period of less than 72 hours (event broadcasting rules aside).

So: virtually every normal streamer is licence-free. The threshold is **simultaneous**
viewers averaged over six months — not followers, not total views, not peak.

- The competent **Landesmedienanstalt** can confirm licence-free status on request by issuing
  an **Unbedenklichkeitsbescheinigung** (certificate of no objection). Worth having once a
  channel is anywhere near the threshold or is doing brand work.
- Operating a licensable programme without a licence can be fined up to **€500,000** under the
  MStV.
- Which authority: the Landesmedienanstalt of the state where the provider is established
  (e.g. LfM NRW, BLM Bayern, mabb Berlin-Brandenburg, NLM Niedersachsen). Nationwide
  programmes are decided by the **ZAK**.
- On-demand offerings (podcasts, VOD libraries) are **not** Rundfunk and never need a licence.

Sources: § 54 MStV; NLM, *Zulassung/Zuweisung*; die-medienanstalten, *Zulassung*.

**Consequence people miss:** being licensed is not only a permission, it is a *duty regime*.
A licensed livestream must meet broadcasting-grade youth-protection rules — see
`germany-youth-protection.md` and the VG Köln decision cited there.

## 2. Legal notice (Impressum)

Two overlapping duties, both of which apply to a monetizing streamer:

- **§ 5 DDG** (Digitale-Dienste-Gesetz, successor to the TMG since 2024) — for
  *geschäftsmäßige, in der Regel gegen Entgelt angebotene* digital services.
- **§ 18 MStV** — for providers of digital services that are **not exclusively personal or
  family** in purpose, with journalistic-editorial content additionally naming a responsible
  person (V.i.S.d.P.).

Practically: **as soon as a channel earns anything or is used to promote a business —
subs, Bits, donations, affiliate links, sponsorships — it needs an legal notice.** "Hobby" stops
being a defence at the first euro or the first affiliate link.

Required content (§ 5 DDG): full name (and legal form/authorised representative if a company),
a **ladungsfähige Anschrift** — a real postal address, no P.O. box —, email address, a second
fast contact channel, plus VAT ID (USt-IdNr.) if you have one, register and register number
if registered, and supervisory authority where applicable.

Placement on Twitch: the legal notice must be **leicht erkennbar, unmittelbar erreichbar und
ständig verfügbar**. Twitch has no legal notice field, so:

- a **panel labelled "Impressum"** on the channel page (not buried in an "About me" essay),
  linking to a page whose URL is recognisable as an legal notice, **and**
- the same in the "About" section.

A link labelled "Impressum" or "Anbieterkennzeichnung" pointing at your own site is the
accepted route. The two-click rule is satisfied if the label is unambiguous.

**Address problem:** streamers who do not want their home address public use a
*ladungsfähige* business address service or a Gewerbe address. Omitting the address is not an
option — a missing legal notice is a classic Abmahnung trigger.

## 3. Data protection (DSGVO) on a stream

The parts that actually bite:

- **Chat messages and usernames are personal data.** If you store, analyse or feed them
  anywhere (a bot database, analytics, an LLM), you need a legal basis (usually
  Art. 6(1)(f) legitimate interest, documented) and a privacy notice reachable from the
  channel, next to the legal notice.
- **Pseudonymise before processing.** If chat text goes into an AI system, strip usernames
  first. This is the cheapest compliance win available.
- **Giveaways** collect personal data — state purpose, retention and legal basis in the
  conditions.
- **Filming other people** (IRL streams, events, guests) needs its own basis: consent, or in
  narrow cases KUG §§ 22–23 for images of people. Bystanders in a public place are not
  automatically fair game in Germany.
- **AI transparency:** if an AI system talks to viewers (a chat bot answering in natural
  language, an AI co-host), EU **AI Act Art. 50** requires that people can tell they are
  interacting with a machine. GPAI obligations began applying 2025-08-02, with further steps
  through 2026–2027. Disclose it in a panel and in the bot's own messages.
- Twitch itself is the controller for the platform's own processing; that does not cover what
  *you* do with the data you take off it.

## 4. Austria and Switzerland

**Austria.** No 20,000-viewer MStV threshold. Instead, providers of audiovisual media
services (including commercial video/streaming channels) must **notify KommAustria via RTR**
under the AMD-G — the anzeigepflicht applies where the video offering is the main purpose and
has a commercial background, and the notification is due **at least two weeks before starting**.
Registration is online at rtr.at. Legal notice duties follow ECG/MedienG rather than DDG.

**Switzerland.** No licence for ordinary streaming; broadcasting rules (RTVG) target
radio/TV. Data protection is the **revDSG** (in force since 2023-09-01), similar in shape to
the GDPR but not identical — do not copy a German privacy notice unchanged. Advertising rules
follow the UWG (CH) and lauterkeit.swiss guidance.

For all three: state the jurisdiction you are answering for, and say plainly when a question
needs a lawyer.
