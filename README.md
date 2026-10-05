# Isaac + Elden Ring Mashup v0.1

A local, offline companion loop connecting The Binding of Isaac: Repentance with Elden Ring through a shared log bridge and a lightweight ModEngine2 monitor.

## Core architecture

- Isaac side: a Lua mod watches pickups, room clears, and dungeon events, then writes JSONL state deltas to a local bridge log.
- ER side: a Python monitor reads that log, watches for conversion events, and applies the matching Elden Ring reward or resource injection rules.
- Design sheet contracts: the conversion matrix and boss reward matrix remain the source of truth for cross-game actions.

## Current state

This repo currently contains the v0.1 blueprint plus working starter code for:

- a JSON resource conversion matrix
- a JSON boss reward matrix
- an Isaac Lua bridge mod scaffold
- a ModEngine2-side Python monitor scaffold
- a Melty launch recipe draft
- a validation script to check the design sheet contracts

## Flow

1. Isaac logs pickups such as coins, bombs, keys, and hearts.
2. The bridge monitor converts those events into Elden Ring actions:
   - coins -> runes
   - bombs -> fire pots
   - keys -> Stone Sword Keys or smithing scrap fallback
   - hearts -> Crimson Tear or equivalent sustain resource
3. Elden Ring boss victories trigger Isaac reward injections via the boss reward matrix.
4. The process stays local and offline, with no manual file moving or port forwarding.

## Quick start

Validate the design sheets:

```bash
python3 scripts/preflight.py
```

Launch the ER side monitor:

```bash
python3 elden-ring/modengine2/er_bridge/bridge_monitor.py
```

Then run Isaac with the companion mod loaded and keep the shared log path live.

## File map

- `design/resource-conversion.json` — resource conversion matrix
- `design/boss-reward-matrix.json` — boss reward mapping
- `isaac/repentance/mods/isaac_er_bridge/main.lua` — Isaac bridge mod
- `isaac/repentance/mods/isaac_er_bridge/metadata.json` — mod metadata
- `elden-ring/modengine2/er_bridge/bridge_monitor.py` — ER-side monitor
- `elden-ring/modengine2/er_bridge/config.json` — monitor config
- `melty/launch_recipe.json` — one-click launch recipe draft
- `scripts/preflight.py` — validation script

## Notes

This is intentionally a v0.1 implementation. The goal is a clean, testable loop that can be expanded after the first offline run proves the bridge contract end-to-end.
