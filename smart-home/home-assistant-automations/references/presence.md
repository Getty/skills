# Presence and occupancy

Distinguish network availability, a person's approximate location, room occupancy, and permission to act. None is a universal substitute for the others.

## Interpret router trackers

A long list of FRITZ! tracked devices can include infrastructure, stale hosts, guests, sleeping endpoints, and repeated randomized identities. Do not attach every tracker to a person or conclude “away” from one missed poll. Inventory actual carried devices and measure their disconnect/reconnect behavior.

Person entities combine selected trackers using documented precedence rules; connection trackers and position trackers can disagree for a while. Inspect the contributing source and update time rather than only the final label. [Person](https://www.home-assistant.io/integrations/person/).

## Build a confidence policy

Use strong positive observations for arrival where acceptable, delayed/multiple evidence for absence, and an explicit unknown state during outages. Different actions need different confidence: pausing music is easier to reverse than setting an alarm or changing all heating. Presence alone should not authorize door unlocking.

For room occupancy, combine motion, presence sensors, door state, and recent interaction only when those sensors exist. Motion silence does not prove an empty room; radar presence can see through some boundaries or retain false positives depending on installation. Treat device-specific behavior empirically.

## Handle phones and visitors

Document private-MAC behavior and the exact home SSID identity. Re-pairing or network reset may change identifiers. Keep guest mode and “someone remains home” controls that a person can understand. Do not force everyone to install tracking software when a simpler room-based rule meets the goal.

Avoid storing precise movement history when a current-home/away decision suffices. Decide which tracker history is necessary before enabling recorder coverage for all hosts.

## Acceptance

Test arrival, normal departure, phone sleep, airplane mode, Wi-Fi outage, router restart, guest presence, and two people leaving at different times. Observe latency rather than imposing a universal debounce value. For long absences, store/reconcile deadlines as described in the timing reference. Report the chosen tradeoff between false-away and delayed-away behavior.
