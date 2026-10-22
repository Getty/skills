# Firsthand experience and regression evidence

## How to use these reports

These are dated accounts by users or maintainers who describe an observed installation or fix. They establish that an outcome occurred in that context; they do not establish frequency, reliability rankings, or a universal defect. A closed issue is not automatically a confirmed fix. Separate the original reporter's observations, their causal hypothesis, and an independently verified resolution.

This research snapshot was checked on 2026-10-22. Reopen the original thread, linked PR, and installed release before using a workaround. Do not expose full support dumps or household identifiers when creating a new report.

## Control 440 through local webhooks

**Source:** [jhol-byte, 2026-02-01, Control 440 webhook blueprint](https://community.home-assistant.io/t/fritz-smart-control-440-blueprint-webhook/981706), with an [author-owned implementation](https://gist.github.com/jhol-byte/c9ee61b60337455622a7187871280321).

The author reports using FRITZ URL-call actions to invoke HA webhooks from Control 440 assignments and implementing click handling in HA. This is an actual workaround account for the native integration's button-event gap. The post does not establish a firmware-independent event API or compatibility with every 440/base combination.

**Application:** Verify the URL-call option on the user's firmware, prove one press with a harmless notification, then map additional buttons. Review imported blueprint code and current HA webhook method/local-access requirements. See [Buttons](buttons.md). Do not infer native push support from a webhook workaround.

## RolloTron unavailable in HA while native control worked

**Source:** [rolandsteinmeyer, issue #110335, 2024-02-12](https://github.com/home-assistant/core/issues/110335).

The reported setup was a 7530 AX on FRITZ!OS 7.57, two Rademacher RolloTron DECT devices, and HA Core 2024.2.1. The author described HA availability failures while control in the FRITZ interface still worked, and reported a Node-RED/fritzapi alternative. That alternate path is evidence that comparing clients can isolate a layer; it does not establish the root cause or a current recommendation to replace the native integration.

**Application:** Compare reachability and timestamps across native UI, a minimal read, and HA. Use a temporary read-only comparison client, not multiple uncontrolled writers. Verify the issue's current state before reusing an old workaround.

## A 7490 with multiple independent pollers

**Source:** [Elarion245, 2025-11-09, timeout discussion](https://community.home-assistant.io/t/fritzbox-option-to-change-default-timeout/949176).

The author described a 7490 used with both HA FRITZ integrations and additional curl polling, intermittent unavailability, authentication prompts, and a 10-second client timeout. They suspected router/API load. The account was not a controlled benchmark and does not establish that a given host/device count overloads all FRITZ!Boxes.

**Application:** Inventory pollers, measure latency, and reduce redundant requests before lengthening timeouts. A longer timeout can conceal congestion. Do not derive a universal maximum from this account or apply the 7490 result directly to another model.

## Apparent firmware breakage was changed DNS

**Source:** [rugk, issue #182103, 2026-09-13](https://github.com/home-assistant/core/issues/182103).

The report involved HA 2026.9.2 and laboratory firmware 8.40-136363. The reporter later corrected the initial firmware explanation: their DNS changes meant `fritz.box` no longer reached the intended router.

**Application:** Resolve the configured hostname from the HA runtime, verify the returned address, and compare a direct authorized IP connection. Record hostname, TLS-name, and discovery behavior separately. A coincident update is a lead to investigate, not sufficient evidence to downgrade firmware.

## October 2026 discovery regression and a linked fix

**Sources:** [ulik14, issue #185818, 2026-10-11](https://github.com/home-assistant/core/issues/185818); [fix PR #186029, merged 2026-10-14](https://github.com/home-assistant/core/pull/186029); [October release changelog](https://www.home-assistant.io/changelogs/core-2026.10/).

The issue reports a 7590 AX and a regression after moving from HA 2026.10.0 to 2026.10.1, with the previous release working. The linked fix changes FRITZ!SmartHome SSDP host selection to use the discovery location rather than the UPnP presentation URL, and restricts automatic host updates to IP-address configurations.

**Application:** Check whether the installed patch contains the fix, inspect the integration host and discovery data, and preserve intentional hostname configuration. Do not call this a general incompatibility with FRITZ!OS or assert that every symptom resembling it has the same cause. A PR merge date alone does not prove inclusion in a specific installed release.

## Energy 250 in an HA installation

**Source:** [Chris, original 2026-01-14, updated 2026-08-25, hands-on Energy 250 report](https://chrissmart.de/fritz-smart-energy-250-im-test-mit-home-assistant/).

The author reports seeing meter-related sensors in HA, including separate consumption/feed-in energy values, and describes initially similar names and duplicated electrical readings in their installation. Their explanation for the duplication is explicitly tentative. The article contains affiliate shopping links; treat the account as a commercially contextualized firsthand test, not independent prevalence data. The exact complete router/HA/meter version combination is not supplied clearly enough to generalize.

**Application:** Verify the actual meter and firmware, identify import/export registers by measured behavior and units, and configure energy statistics from cumulative energy rather than names alone. Use [official meter compatibility](https://fritz.com/pages/stromsensor) for eligibility. Do not carry over the review's broad compatibility wording or a firmware threshold as a universal requirement without primary confirmation.

## Add new evidence consistently

For each case, capture original URL, author/date, exact model/firmware/integration version when disclosed, observed behavior, measurement or log evidence, workaround, result, unresolved explanations, and relevant conflicts of interest. Prefer a direct reproducible issue or owner account to a retailer's aggregate stars. Search for successful and unsuccessful cases of the same SKU and integration path. If the model or firmware is missing, say so; do not fill it in from a different participant's installation.
