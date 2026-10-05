#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    ROOT / "design" / "resource-conversion.json",
    ROOT / "design" / "boss-reward-matrix.json",
    ROOT / "isaac" / "repentance" / "mods" / "isaac_er_bridge" / "main.lua",
    ROOT / "elden-ring" / "modengine2" / "er_bridge" / "bridge_monitor.py",
    ROOT / "launch.bat",
    ROOT / "melty.json",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main():
    missing = [str(path) for path in REQUIRED if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    for path in [ROOT / "design" / "resource-conversion.json", ROOT / "design" / "boss-reward-matrix.json"]:
        load_json(path)

    melty = load_json(ROOT / "melty.json")
    if not melty.get("requiredGames"):
        raise SystemExit("melty.json is missing requiredGames")

    print("[validate] All required repo files are present.")
    print("[validate] JSON design sheets parse successfully.")
    print("[validate] Melty recipe contains required game metadata.")
    print("[validate] The project is ready for the next live Steam/ModEngine2 verification step.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Validation failed: {exc}")
