# Templates and helpers

## Preserve meaning before conversion

Read values with supported state helpers, check availability/type, and only then convert. Decide the invalid-data policy explicitly: skip, retain a bounded previous decision, alert, or fall back to local device behavior. Do not turn unavailable heating input into `0 °C` through an indiscriminate `float(0)`.

```jinja2
{% set raw = states('sensor.study_temperature') %}
{{ is_number(raw) and (raw | float) < 19 }}
```

This is a guard for an example threshold, not a thermostat implementation. Check stale data separately; a valid number can be old. Use the developer template tool with unavailable, unknown, numeric, and unexpected string inputs. [Templating guide](https://www.home-assistant.io/docs/templating/).

## Model state explicitly

Use helpers for user mode, pending operation, deadline, selected scene, target value, or schedule. Name them after semantics, not the current code's intermediate variable. Avoid using one boolean as both “automation enabled” and “someone manually overrode it.” Those are different states with different reset rules.

Template sensors need correct device class, state class, unit, and availability. State-based and trigger-based templates update differently; pick the one matching the required dependencies and restoration behavior. Do not assume a trigger-based template recalculates on every referenced entity change. [Template integration](https://www.home-assistant.io/integrations/template/).

## Time

Use aware timestamps for elapsed-time comparisons and local scheduled times for household routines. Document DST behavior for clock-based schedules. Use a date-and-time helper for an absolute deadline; a time-only value loses which day is intended. An `initial` value can reset restored state, so do not set it casually on a durable deadline helper. [Input Datetime](https://www.home-assistant.io/integrations/input_datetime/).

## Avoid subtle template errors

Check units before comparing numbers. Distinguish `hvac_mode` from actual `hvac_action`, target temperature from measured temperature, and desired state from last command. Strings such as `"off"` and booleans are not interchangeable.

Keep costly all-entity loops out of high-frequency calculations when a bounded explicit group suffices. Resolve lists before calling actions; an empty target should not accidentally broaden intent. Guard against attribute absence when an integration is starting.

Test rendered output and actual action validation separately. Valid Jinja can produce the wrong data shape for a service. Preserve native numeric/boolean types where the installed action expects them; quote YAML strings deliberately.
