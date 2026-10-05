#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISAAC_MOD_SRC = ROOT / "isaac" / "repentance" / "mods" / "isaac_er_bridge"
LOG_DIR = Path.home() / ".IsaacERBridge"
LOG_FILE = LOG_DIR / "isaac_er_bridge.log"

WINDOWS_COMMON_DIRS = [
    Path(r"C:\Program Files (x86)\Steam\steamapps\common"),
    Path(r"C:\Program Files\Steam\steamapps\common"),
    Path.home() / "Program Files (x86)" / "Steam" / "steamapps" / "common",
    Path.home() / "Steam" / "steamapps" / "common",
]

POSIX_COMMON_DIRS = [
    Path.home() / ".steam" / "steam" / "steamapps" / "common",
    Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common",
    Path("/usr/local/games"),
]


def find_steam_game_dir(game_name_tokens):
    search_roots = WINDOWS_COMMON_DIRS + POSIX_COMMON_DIRS
    for root in search_roots:
        if not root.exists():
            continue
        for candidate in root.rglob("*"):
            if not candidate.is_dir():
                continue
            name = candidate.name.lower()
            if any(token.lower() in name for token in game_name_tokens):
                return candidate
    return None


def find_isaac_dir():
    # Common Steam folder names for the game; we prefer exact matches first.
    for dir_name in [
        "The Binding of Isaac Rebirth",
        "The Binding of Isaac: Rebirth",
        "The Binding of Isaac Repentance",
        "The Binding of Isaac: Repentance",
        "The Binding of Isaac",
    ]:
        for root in WINDOWS_COMMON_DIRS + POSIX_COMMON_DIRS:
            if not root.exists():
                continue
            candidate = root / dir_name
            if candidate.exists():
                return candidate
    return find_steam_game_dir(["binding of isaac", "isaac"])


def find_elden_ring_dir():
    for dir_name in ["ELDEN RING", "Elden Ring", "eldenring"]:
        for root in WINDOWS_COMMON_DIRS + POSIX_COMMON_DIRS:
            if not root.exists():
                continue
            candidate = root / dir_name
            if candidate.exists():
                return candidate
    return find_steam_game_dir(["elden ring", "eldenring"])


def install_mod_to_game(isaac_dir: Path):
    target_dir = isaac_dir / "repentance" / "mods" / "isaac_er_bridge"
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(ISAAC_MOD_SRC, target_dir)
    return target_dir


def start_monitor():
    script = ROOT / "elden-ring" / "modengine2" / "er_bridge" / "bridge_monitor.py"
    if not script.exists():
        raise FileNotFoundError(f"Monitor not found: {script}")

    log_dir.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        subprocess.Popen([sys.executable, str(script)], creationflags=subprocess.CREATE_NEW_CONSOLE)  # type: ignore[attr-defined]
    else:
        subprocess.Popen([sys.executable, str(script)])


def main():
    isaac_dir = find_isaac_dir()
    elden_ring_dir = find_elden_ring_dir()

    if isaac_dir is None:
        raise FileNotFoundError("Could not find The Binding of Isaac install. Install the Steam copy and re-run this script.")
    if elden_ring_dir is None:
        raise FileNotFoundError("Could not find Elden Ring install. Install the Steam copy and re-run this script.")

    target = install_mod_to_game(isaac_dir)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text("", encoding="utf-8")

    print("[install] Isaac mod installed to:", target)
    print("[install] Elden Ring install found at:", elden_ring_dir)
    print("[install] Bridge log ready at:", LOG_FILE)
    print("[install] Starting monitor...")
    start_monitor()

    print("\n[install] Ready to launch the games. Use the Isaac + Elden Ring offline launch flow.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Release prep failed: {exc}")
