# Elden Ring ModEngine2 Side

This folder contains the lightweight ER-side bridge runner intended to watch the Isaac exchange log and apply item injection or boss-reward plumbing in a clean offline ModEngine2 environment.

## Files

- `bridge_monitor.py` — Python process that polls the bridge log for Isaac state deltas.
- `config.json` — runtime settings for monitor refresh intervals and reward policies.

## Planned ER-side behavior

- Read pickup events from the Isaac bridge log
- Map those events to Elden Ring conversion actions (`runes`, `fire pots`, `Stone Sword Keys`, `scrap`)
- Watch for room-clear or boss-defeat markers
- Inject the relevant Isaac rewards after a boss kill or major ER victory
- Keep a local state file for idempotence and replay prevention

## Offline ModEngine2 environment

This is designed to run under the ModEngine2 offline profile with Easy Anti-Cheat disabled, keeping the flow local and self-contained.
