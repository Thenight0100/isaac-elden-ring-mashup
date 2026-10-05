#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISAAC_MOD_SRC = ROOT / "isaac" / "repentance" / "mods" / "isaac_er_bridge"
ER_MONITOR_SRC = ROOT / "elden-ring" / "modengine2" / "er_bridge"
LOG_DIR = Path.home() / "AppData" / "Local" / "IsaacERBridge"
LOG_FILE = LOG_DIR / "isaac_er_bridge.log"
STATE_FILE = LOG_DIR / "bridge_state.json"
RUNTIME_MANIFEST = LOG_DIR / "runtime_manifest.json"

STEAM_COMMON_DIRS = [
    Path(r"C:\Program Files (x86)\Steam\steamapps\common"),
    Path(r"C:\Program Files\Steam\steamapps\common"),
    Path.home() / "Program Files (x86)" / "Steam" / "steamapps" / "common",
    Path.home() / "Steam" / "steamapps" / "common",
    Path.home() / ".steam" / "steam" / "steamapps" / "common",
    Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common",
]


def find_game_dir(names):
    for name in names:
        for root in STEAM_COMMON_DIRS:
            if not root.exists():
                continue
            candidate = root / name
            if candidate.exists():
                return candidate
    return None


def find_isaac_dir():
    return find_game_dir([
        "The Binding of Isaac Repentance",
        "The Binding of Isaac: Repentance",
        "The Binding of Isaac Rebirth",
        "The Binding of Isaac: Rebirth",
        "The Binding of Isaac",
    ])


def find_elden_ring_dir():
    return find_game_dir([
        "ELDEN RING",
        "Elden Ring",
        "eldenring",
    ])


def find_modengine2_dir():
    return find_game_dir([
        "ModEngine2",
        "modengine2",
    ])


def install_mod_to_game(isaac_dir: Path):
    target = isaac_dir / "repentance" / "mods" / "isaac_er_bridge"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ISAAC_MOD_SRC, target)
    return target


def install_monitor_bundle():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = LOG_DIR / "er_bridge"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ER_MONITOR_SRC, target)

    if not LOG_FILE.exists():
        LOG_FILE.write_text("", encoding="utf-8")
    if not STATE_FILE.exists():
        STATE_FILE.write_text('{"seenEvents": []}\n', encoding="utf-8")
    return target


def write_runtime_manifest(isaac_dir: Path, er_dir: Path, modengine_dir: Path | None):
    manifest = {
        "isaacDir": str(isaac_dir),
        "eldenRingDir": str(er_dir),
        "modengine2Dir": str(modengine_dir) if modengine_dir else None,
        "logDir": str(LOG_DIR),
        "logFile": str(LOG_FILE),
        "stateFile": str(STATE_FILE),
        "version": "0.1",
    }
    RUNTIME_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return RUNTIME_MANIFEST


def start_monitor():
    script = ER_MONITOR_SRC / "bridge_monitor.py"
    if not script.exists():
        raise FileNotFoundError(f"Monitor script not found: {script}")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        subprocess.Popen([sys.executable, str(script)], creationflags=subprocess.CREATE_NEW_CONSOLE)  # type: ignore[attr-defined]
    else:
        subprocess.Popen([sys.executable, str(script)])


def main():
    isaac_dir = find_isaac_dir()
    er_dir = find_elden_ring_dir()
    modengine_dir = find_modengine2_dir()

    if isaac_dir is None:
        raise FileNotFoundError("Could not find The Binding of Isaac install. Install the Steam copy and re-run this script.")
    if er_dir is None:
        raise FileNotFoundError("Could not find Elden Ring install. Install the Steam copy and re-run this script.")

    install_mod_to_game(isaac_dir)
    install_monitor_bundle()
    write_runtime_manifest(isaac_dir, er_dir, modengine_dir)

    print("[install] Isaac mod installed to:", isaac_dir / "repentance" / "mods" / "isaac_er_bridge")
    print("[install] Local monitor bundle installed to:", LOG_DIR / "er_bridge")
    print("[install] Elden Ring install found at:", er_dir)
    print("[install] ModEngine2 install found at:", modengine_dir if modengine_dir else "not found")
    print("[install] Bridge log ready at:", LOG_FILE)
    print("[install] Runtime manifest:", RUNTIME_MANIFEST)

    start_monitor()
    print("\n[install] Ready for launch. Launch Elden Ring through ModEngine2 offline mode, then launch Isaac with the companion mod enabled.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Release prep failed: {exc}")
