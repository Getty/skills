# Source map

Research baseline: **2026-10-22**. A household inventory the user provides is a report, not a scan. Architecture, purchasing worksheets and acceptance criteria are original engineering procedures; product capabilities require the primary sources below and the relevant vendor references.

| Source | Use |
|---|---|
| [HA integrations](https://www.home-assistant.io/integrations/) | Resolve native integration names and supported functions |
| [Certified products](https://works-with.home-assistant.io/certified-products/) | Exact certified variant; not blanket brand compatibility |
| [Network](https://www.home-assistant.io/integrations/network/), [Zeroconf](https://www.home-assistant.io/integrations/zeroconf/), [SSDP](https://www.home-assistant.io/integrations/ssdp/) | Interface selection and discovery mechanisms |
| [Matter](https://www.home-assistant.io/integrations/matter/), [Thread](https://www.home-assistant.io/integrations/thread/) | Controller, transport, commissioning and networking |
| [Matter server OS requirements](https://github.com/home-assistant-libs/python-matter-server/blob/main/docs/os_requirements.md) | Host kernel and IPv6 prerequisites; match installed server version |
| [ZHA](https://www.home-assistant.io/integrations/zha/), [Zigbee2MQTT](https://www.zigbee2mqtt.io/) | Coordinator and device support |
| [Z-Wave](https://www.home-assistant.io/integrations/zwave_js/) | Regional radio, integration and backup path |
| [HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/), [HomeKit Bridge](https://www.home-assistant.io/integrations/homekit/) | Import versus export |
| [EnOcean](https://www.home-assistant.io/integrations/enocean/), [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/) | Legacy radio support boundaries |
| [KNX](https://www.home-assistant.io/integrations/knx/), [Modbus](https://www.home-assistant.io/integrations/modbus/) | Building-system interface paths |
| [Backup](https://www.home-assistant.io/integrations/backup/) | Current HA backup behavior |
| [LLM API](https://contributors.home-assistant.io/core/internals/llm-api/), [MCP Server](https://www.home-assistant.io/integrations/mcp_server/) | Different AI API privilege surfaces |
| [core #161398](https://github.com/home-assistant/core/issues/161398) | Firsthand IPv6-only initialization problem; not a universal network verdict |

Recheck URLs, versions and release status before making a concrete purchase or applying a change. A product listed in another skill's family table is a candidate for investigation, not a guarantee about every regional SKU.
