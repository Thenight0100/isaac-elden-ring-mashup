# Isaac + Elden Ring Mashup v0.1

A companion project pairing The Binding of Isaac: Repentance with Elden Ring through a local exchange bridge. This repository is the v0.1 design and scaffolding for a solo-companion loop where Isaac pickups and dungeon clears feed resources and rewards into Elden Ring, and major Elden Ring bosses trigger rewards back into Isaac.

## Core loop

- Isaac acts as the scavenger. Coins, bombs, and keys are recorded in the bridge log.
- Resource conversion rules translate those items into Elden Ring resources such as runes, fire pots, and Stone Sword Keys/scrap.
- Starting item pedestals and baseline buffs are synced from Isaac into Elden Ring.
- Defeating major Elden Ring bosses triggers Isaac item rewards and chest/pedestal drops.

## Requirements

- The Binding of Isaac: Repentance
- The Binding of Isaac Lua mod support
- Elden Ring
- ModEngine2 for Elden Ring offline launch
- Melty launcher or equivalent one-click desktop flow
- Easy Anti-Cheat disabled for offline play

## Repo structure

- `design/resource-conversion.json` — conversion matrix
- `design/boss-reward-matrix.json` — boss-to-reward mapping
- `isaac/repentance/mods/isaac_er_bridge/` — Isaac mod scaffold and bridge log writer
- `elden-ring/modengine2/er_bridge/` — ModEngine2-side monitor and item injection scaffold
- `melty/launch_recipe.json` — one-click Melty launch recipe draft
- `scripts/preflight.py` — design validation across conversion and boss sheets

## Design files

The design sheets are intentionally versioned as JSON so they can be validated, diffed, and extended without breaking the bridge layer.

## Preflight workflow

Run the validator before packaging:

```bash
python3 scripts/preflight.py
```

The script verifies:

- all resource conversion sources are defined
- no boss rewards are missing a target item ID
- all matrix categories are cross-referenced consistently
- config values remain aligned between Isaac and ER bridge files

## One-click Melty launch

The launch recipe in `melty/launch_recipe.json` is designed to bring the full offline loop online in a clean sequence:

1. Launch Elden Ring via ModEngine2 in offline mode
2. Start the ER bridge monitor
3. Launch Isaac with the companion mod enabled
4. Keep the exchange log active for pickup and room-cleared state deltas

## Notes

This repo represents the v0.1 blueprint. It is intentionally lightweight and modular so the bridge can be expanded once the first offline loop is working.

## Next steps

1. Wire the Lua mod into a real Isaac mod environment
2. Test the log schema against the actual game events
3. Add boss reward injection logic on the ER side
4. Validate the full Melty flow in the clean offline launch profile
