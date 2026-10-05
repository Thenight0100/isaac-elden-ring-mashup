# Isaac ER Bridge Mod

This folder contains the Isaac-side companion mod for the v0.1 bridge. Its purpose is to emit a local JSONL log with structured room and pickup events for the Elden Ring monitor to consume.

## Included files

- `main.lua` — runtime bridge logic.
- `metadata.json` — mod metadata used to describe the plug-in and version.

## Event contract

The bridge emits data in JSONL form, one JSON object per line. Example event shapes:

```json
{"ts":"2026-10-05T16:57:00Z","event":"pickup","payload":{"type":"coins","variant":5,"roomIndex":2,"player":"unknown"}}
{"ts":"2026-10-05T16:57:04Z","event":"room_clear","payload":{"roomIndex":2,"status":"clear"}}
{"ts":"2026-10-05T16:57:09Z","event":"bridge_start","payload":{"status":"online","mod":"isaac_er_bridge","version":"0.1"}}
```

## Notes

The actual callback names and pickup APIs should be verified against the exact Isaac build and modloader version used on the host machine, but the structure is intentionally lightweight and easy to adapt.
