# Isaac + Elden Ring Mashup v0.1

A local, offline companion loop connecting The Binding of Isaac: Repentance with Elden Ring through a shared log bridge and a lightweight ModEngine2 monitor.

## Core architecture

- **Isaac side:** a Lua mod watches pickups, room clears, and dungeon events, then writes JSONL state deltas to a local bridge log.
- **ER side:** a Python monitor reads that log, watches for conversion events, and applies the matching Elden Ring reward or resource injection rules.
- **Design sheet contracts:** the conversion matrix and boss reward matrix remain the source of truth for cross-game actions.

## Quick start

**Windows:**
```bash
launch.bat
```

**macOS/Linux:**
```bash
chmod +x launch.sh
./launch.sh
```

Then launch Elden Ring via ModEngine2 (offline, EAC disabled) and Isaac with the `isaac_er_bridge` mod enabled.

For full setup instructions, see **[PLAYBOOK.md](PLAYBOOK.md)**.

## Current state

This is a v0.1 **play-ready scaffold** that includes:

- A JSON resource conversion matrix (coins → runes, bombs → fire pots, keys → Stone Sword Keys)
- A JSON boss reward matrix (Godrick → Heart Potion, Radahn → Bomb Pack, etc.)
- An Isaac Lua bridge mod that logs pickups and room clears
- A ModEngine2-side Python monitor that reads the bridge log and tracks events
- A Melty/desktop launcher recipe for one-click offline play
- Validation scripts to check design sheet integrity
- Comprehensive documentation and troubleshooting guides

## Flow

1. Isaac logs pickups (coins, bombs, keys, hearts) and room-clear events to a local JSONL file.
2. The ER bridge monitor polls that log and converts events:
   - Coins → Runes
   - Bombs → Fire Pots
   - Keys → Stone Sword Keys or Smithing Scrap (fallback)
   - Hearts → Crimson Tears
3. Elden Ring boss victories can trigger Isaac reward injections via the boss reward matrix.
4. The entire loop stays local and offline with no manual file moving or port forwarding.

## File structure

```
.
├── design/
│   ├── resource-conversion.json     # Pickup → ER resource matrix
│   └── boss-reward-matrix.json      # ER boss → Isaac reward matrix
├── isaac/
│   └── repentance/mods/isaac_er_bridge/
│       ├── main.lua                 # Bridge mod runtime
│       └── metadata.json            # Mod metadata
├── elden-ring/
│   └── modengine2/er_bridge/
│       ├── bridge_monitor.py        # Event monitor & log reader
│       └── config.json              # Monitor configuration
├── melty/
│   └── launch_recipe.json           # One-click launcher draft
├── scripts/
│   ├── preflight.py                 # Design validation
│   └── test_bridge.py               # Fake event generator for testing
├── launch.bat                       # Windows launcher
├── launch.sh                        # macOS/Linux launcher
├── README.md                        # This file
├── PLAYBOOK.md                      # Setup & troubleshooting guide
└── PUBLISHING.md                    # Release & extension guide
```

## Testing without games

Test the bridge and monitor without launching Isaac or Elden Ring:

```bash
python3 scripts/test_bridge.py        # Generate fake events
python3 scripts/preflight.py          # Validate design sheets
python3 elden-ring/modengine2/er_bridge/bridge_monitor.py  # Run monitor
```

The monitor will read and echo the fake events, confirming the full pipeline works.

## Design sheets

Both the resource conversion and boss reward matrices are JSON, making them:
- Easy to read and understand
- Simple to extend with new items or bosses
- Validated by `preflight.py` for consistency
- Sourceable as a database for UI dashboards or wiki pages

### Resource conversion example

```json
{
  "source": "coins",
  "sourceType": "isaac_pickup",
  "target": "runes",
  "targetType": "elden_ring_resource",
  "ratio": 100,
  "notes": "1 coin = 100 runes"
}
```

### Boss reward example

```json
{
  "erBossId": "godrick",
  "erBossName": "Godrick the Grafted",
  "rewardType": "pedestal",
  "isaacItemId": "ITEM_isaac_heart_potion",
  "isaacItemName": "Heart Potion"
}
```

## Extending the project

- **Add more bosses:** Edit `design/boss-reward-matrix.json` and run `preflight.py`
- **Tune conversion rates:** Edit `design/resource-conversion.json`
- **Add new resource types:** Extend both matrices and implement the conversion logic in `bridge_monitor.py`
- **Inject items into ER:** Replace the logging placeholders in `bridge_monitor.py` with actual ModEngine2 API calls
- **Add more games:** Create a new folder (e.g., `hades/`) and follow the same bridge pattern

## Troubleshooting

See **[PLAYBOOK.md](PLAYBOOK.md)** for setup, diagnostics, and common issues.

## Publishing

To tag a release, prepare the repo, and publish externally, see **[PUBLISHING.md](PUBLISHING.md)**.

## License

TBD — add a LICENSE file when publishing externally.

## Next steps

Once the bridge is live and working:
1. Implement actual item injection into Elden Ring
2. Add a visual dashboard to watch resource conversions in real-time
3. Expand to more bosses and items
4. Extend to other games (Hades, Hollow Knight, Celeste, etc.)
5. Create a community wiki for shared conversion matrices

Happy playing!
