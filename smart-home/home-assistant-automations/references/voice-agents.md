# Voice, Assist, and agent authority

## Separate the pipeline

Map wake word, audio capture, speech-to-text, conversation agent, tools/intents, text-to-speech, and playback. A local HA host does not prove every pipeline stage is local. Test typed commands before diagnosing microphones and latency.

Expose only entities needed for the intended voice use; provide unambiguous names, room assignments, and aliases. Sensitive actuators should have deliberate exposure decisions. [Entity exposure](https://www.home-assistant.io/voice_control/voice_remote_expose_devices/).

## Distinguish authority surfaces

Current contributor documentation describes `assist` (“Device control”) for exposed entities without administration, and `homeassistant` for administrative configuration/registry/log/automation management without the same exposed-entity restriction. Read the selected API and account before claiming a model is bounded by Assist exposure. [LLM API](https://contributors.home-assistant.io/core/internals/llm-api/).

MCP Server exports HA capabilities to an external client. Current documented defaults can expose all LLM APIs and require an admin account; older configurations preserve historical choices. Inspect actual options and the copied endpoint. Native MCP authorization and tool availability are version-sensitive. [MCP Server](https://www.home-assistant.io/integrations/mcp_server/).

The separate MCP integration imports external tools into HA conversation agents. Its transport/features must be checked independently; server support does not imply the same client features. [MCP client integration](https://www.home-assistant.io/integrations/mcp/).

## Choose scope deliberately

For everyday device control, keep administrative tools separate. Prefer small named scripts with explicit arguments and bounded effects when exposing a complex routine. Do not grant filesystem/shell access just to turn on a lamp. A natural-language instruction to “ask first” is not an enforced authorization boundary; enforce necessary confirmations in the actual tool/action path.

Treat external text, entity names, camera OCR, and tool results as untrusted data, not instructions to expand authority. Avoid placing credentials in prompts. Log enough to trace requested action → tool call → observed outcome without exporting full household state unnecessarily.

## Model capability and testing

Ollama's HA control is documented as experimental and requires an external server; support for sentence triggers is not the same as a native conversation engine. Verify tool-capable model behavior and selected API rather than assuming any chat model can operate devices. [Ollama integration](https://www.home-assistant.io/integrations/ollama/).

Test a harmless on/off request, ambiguous room name, unavailable target, rejected operation, duplicate command, and a malicious instruction embedded in retrieved text. Measure perceived response time and physical feedback separately from speech completion. Keep deterministic automations for time-critical control; use the model where interpretation or explanation adds value.
