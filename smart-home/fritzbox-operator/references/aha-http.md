# AHA HTTP compatibility and device interpretation

## Role and lifecycle

Use AHA when the deployed integration or firmware requires it. The [official interface index](https://fritz.com/pages/schnittstellen) marks AHA frozen while retaining it in FRITZ!OS and recommends a medium-term transition to REST. This is not a removal notice and does not mean current HA installations should be modified manually.

The [AHA specification](https://fritz.support/resources/AHA-HTTP-Interface.pdf) documents `/webservices/homeautoswitch.lua` with URL-encoded `switchcmd`, `sid`, and operation-specific parameters such as `ain`. Responses can be plain values or XML. Device IDs and HAN FUN/Zigbee unit IDs differ; discover them from device information. Treat AINs as opaque strings and preserve spaces/suffixes. A 200 response may contain `inval`; 403 can indicate an invalid session or insufficient rights.

## Read a coherent inventory

Start with `getdevicelistinfos`, then inspect templates and triggers only if the use case needs them. Keep device, unit, group, template, and routine identities distinct. Record product name, firmware, capability fields, availability, and field timestamps. A parent device can exist while its functional unit is absent or unsupported.

For a tiny read-only client using an already established SID, keep secrets in memory and restrict output to selected fields:

```python
from getpass import getpass
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

base = input("Router HTTPS origin: ").rstrip("/")
sid = getpass("Short-lived SID: ")
query = urllib.parse.urlencode({"switchcmd": "getdevicelistinfos", "sid": sid})
request = urllib.request.Request(base + "/webservices/homeautoswitch.lua?" + query)
with urllib.request.urlopen(request, timeout=10) as response:
    data = response.read(2_000_001)
declarations = data.replace(b"\x00", b"").upper()
if len(data) > 2_000_000 or any(
    token in declarations for token in (b"<!DOCTYPE", b"<!ENTITY")
):
    raise ValueError("Unexpected XML document")
root = ET.fromstring(data)
for device in root.findall("device"):
    print(device.get("productname"), device.findtext("present"))
```

Use a hostname with a validated certificate or an explicitly trusted local certificate. Do not globally disable verification. The sample is a request recipe, not a long-running SID manager; production code needs bounded input, origin validation, HTTP/XML errors, session renewal, and redacted logs. Do not run it with an untrusted URL that could receive the session credential.

## Normalize readings deliberately

Never infer a unit from magnitude. Existing AHA fields use specific representations, including mW for plug power, Wh for energy, tenths of a degree for temperature, and encoded thermostat setpoints with special on/off values. Check each command/field's specification before conversion. `unknown`, missing, invalid, and disconnected must remain distinguishable from zero.

Build normalization at the API boundary once. Downstream automations should consume validated SI values plus availability and age. Retain raw values only in restricted diagnostics. For energy, distinguish an accumulating counter from instantaneous power and handle counter reset explicitly; do not simply add a new cumulative reading to yesterday's total.

## Write through a capability-aware adapter

Map desired effects to documented commands, rather than arbitrary `switchcmd` strings supplied by external text. Check whether the target is a group or unit, whether device/API locks apply, and whether another controller will immediately change the value again. Prefer explicit on/off to toggle for retryable operations.

For a timed heating change, define the expiration and schedule interaction before sending it. For blinds, verify direction, end stops, and stop behavior before automation. For plugs, identify the load and startup behavior rather than assuming “switch” means a harmless lamp.

## Troubleshoot without increasing load

Compare one direct read, one FRITZ UI observation, and one HA update. If only HA is stale, inspect the coordinator, entity mapping, and integration logs. If both interfaces stall, stop duplicate scrapers and measure request duration. If the router sees a device unavailable, investigate radio/physical power before adding retries. Never create a new login session for every entity poll.

The [pyfritzhome upstream project](https://github.com/hthiery/python-fritzhome) is the implementation used by the inspected HA release. Its own source provides a useful comparison, but bind conclusions to the version in HA's manifest.
