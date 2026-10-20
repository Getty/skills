# Dates, calendars, time zones, and internationalization

**Read when:** localizing an application, scheduling events, or adding calendar/date controls.

## Domain representation

Distinguish an instant, a calendar date, a local wall-clock time, a duration, and a recurring schedule. They are not interchangeable strings. Decide which values require an IANA time zone and which must not shift across zones, such as a birthday. Keep canonical data separate from localized display and parsing.

react-i18next and React Intl have different message/workflow models. Choose the existing project convention, extract messages consistently, and avoid constructing sentences by concatenating fragments that cannot be translated correctly. Keep accessible labels and error messages in the same localization workflow. Calendar/date-picker libraries and date utilities are catalog discovery routes requiring version-specific checks.

## UI integration

Document locale selection, fallback language, pluralization, number/currency formatting, calendar conventions, first weekday, and right-to-left layout. A date field should make its expected input clear and preserve an invalid draft for correction. For range selection, define inclusive/exclusive boundaries and what happens when the end precedes the start.

For recurring events, specify behavior during daylight-saving gaps/overlaps and when a user changes time zone. Never approximate calendar months as a fixed number of milliseconds. Server and first client render must use compatible locale/time assumptions to avoid hydration mismatches.

## Acceptance

Test long translations, plural cases, bidirectional text, non-Latin input, leap days, month-end, DST transitions, and users in different zones opening the same event. Verify keyboard date selection and screen-reader announcements. Review calendar advanced-feature licensing and locale-data bundle size. Snapshot formatted dates only with an explicit locale/time zone so tests remain deterministic across machines.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R66: react-i18next](https://react.i18next.com/)
- [R67: React Intl](https://formatjs.github.io/docs/react-intl/)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
