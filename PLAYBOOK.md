# Isaac + Elden Ring Mashup v0.1 — Play Setup

## Pre-flight checklist

Before you launch, verify these files and paths:

- [ ] Elden Ring is installed and runs offline via ModEngine2
- [ ] Easy Anti-Cheat is disabled for your offline profile
- [ ] The Binding of Isaac: Repentance is installed with mod support enabled
- [ ] `C:/Games/IsaacERBridge/` directory exists (or adjust `launch.bat` to your log path)
- [ ] You have `python3` installed and available in your PATH

## Installing the Isaac bridge mod

1. Copy the contents of `isaac/repentance/mods/isaac_er_bridge/` into your Isaac mods folder:
   ```
   <Isaac Install>/repentance/mods/isaac_er_bridge/
   ```
2. Verify these files are in place:
   - `main.lua` — the bridge runtime
   - `metadata.json` — mod metadata

## Launching the companion loop

### Windows

1. Run `launch.bat` (or double-click it):
   ```bash
   launch.bat
   ```
   - This starts the Elden Ring bridge monitor in the background
   - Follow the on-screen prompts

2. The prompt will tell you when to launch Elden Ring and Isaac manually

3. Once both games are running with the mod enabled, the bridge log will start filling with pickup and room-clear events

### macOS / Linux

1. Make the launch script executable:
   ```bash
   chmod +x launch.sh
   ```

2. Run it:
   ```bash
   ./launch.sh
   ```

3. Follow the same flow as Windows (launch ER and Isaac manually)

## Verifying the bridge is working

While playing Isaac, check the bridge log at:
- **Windows:** `C:/Games/IsaacERBridge/isaac_er_bridge.log`
- **macOS/Linux:** `~/.IsaacERBridge/isaac_er_bridge.log`

You should see JSONL events like:
```json
{"ts":"2026-10-05T16:57:00Z","event":"bridge_start","payload":{"status":"online","mod":"isaac_er_bridge","version":"0.1"}}
{"ts":"2026-10-05T16:57:05Z","event":"pickup","payload":{"type":"coins","variant":5,"roomIndex":2,"player":"unknown"}}
{"ts":"2026-10-05T16:57:10Z","event":"room_clear","payload":{"roomIndex":2,"status":"clear"}}
```

The ER monitor will also print these events to its console:
```
[ER monitor] bridge online
[ER monitor] pickup: coins
[ER monitor] room clear detected
```

## Troubleshooting

### Bridge log not appearing
- Verify the Isaac mod is loaded (check Isaac's mod menu)
- Check that `C:/Games/IsaacERBridge/` exists and is writable
- Make sure the `logPath` in `isaac/repentance/mods/isaac_er_bridge/metadata.json` matches your setup

### Monitor not starting
- Verify Python 3 is installed: `python3 --version`
- Check that the monitor config path is correct in `launch.bat` or `launch.sh`
- Run the monitor manually to see error output:
  ```bash
  python3 elden-ring/modengine2/er_bridge/bridge_monitor.py
  ```

### Duplicate events or missing events
- The monitor keeps a local `state.json` to prevent re-triggering the same event
- If events seem stuck, delete `elden-ring/modengine2/er_bridge/state.json` and restart

## Design sheets

The conversion and reward rules are defined in JSON so you can edit them:

- **Resource conversion:** `design/resource-conversion.json`
  - Controls how Isaac pickups map to ER resources
  - Edit the `ratio` field to change conversion rates

- **Boss rewards:** `design/boss-reward-matrix.json`
  - Controls what Isaac item you get for each ER boss defeat
  - Add new bosses or adjust reward types (`pedestal` or `chest`)

After editing, validate your changes:
```bash
python3 scripts/preflight.py
```

## Next steps

Once the bridge is working, you can:
- Adjust conversion rates in the design sheets
- Add more boss/reward mappings
- Expand the monitor to actually inject items into Elden Ring (currently just logs events)
- Create a visual dashboard to watch the sync in real-time

## Questions?

Check the README for architecture details, or inspect the JSONL log to debug event flow.

Happy playing!
