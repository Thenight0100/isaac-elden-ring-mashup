# Elden Ring Bridge Monitor

This folder contains the ER-side state monitor. It polls the JSONL bridge log produced by the Isaac mod and translates Isaac events into Elden Ring-facing actions such as rune grants, fire pot drops, Stone Sword Key grants, and boss-triggered reward injection.

## Runtime behavior

- Watches `isaac_er_bridge.log` for JSONL events.
- Ignores duplicate events using a local `seen_events` state file.
- Maps item types and room-clear signals into known conversion actions.
- Keeps the loop idempotent so repeated reads do not re-trigger the same reward.

## Example event flow

```json
{"ts":"2026-10-05T16:57:00Z","event":"pickup","payload":{"type":"coins","variant":5,"roomIndex":2}}
{"ts":"2026-10-05T16:57:01Z","event":"room_clear","payload":{"roomIndex":2,"status":"clear"}}
```

The runner can then trigger actions such as:

- coins -> grant runes
- bombs -> grant fire pots
- keys -> grant Stone Sword Key or smithing scrap fallback
- room clear -> optionally grant a small reward or update state

## Notes

This implementation is intentionally lightweight and offline-focused so it can be expanded once the final ModEngine2 installation path and boss injection APIs are finalized.
