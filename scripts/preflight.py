#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCE_FILE = ROOT / "design" / "resource-conversion.json"
BOSS_FILE = ROOT / "design" / "boss-reward-matrix.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_resource_matrix(data):
    matrix = data.get("resourceMatrix", [])
    sources = {row["source"] for row in matrix}
    targets = {row["target"] for row in matrix}
    if not matrix:
        raise ValueError("resourceMatrix is empty")
    if len(sources) < 3:
        raise ValueError("Need at least three source resource categories")
    if len(targets) < 3:
        raise ValueError("Need at least three target resource categories")
    for row in matrix:
        if row.get("ratio", 0) <= 0:
            raise ValueError(f"Invalid ratio for {row.get('source')} -> {row.get('target')}")
        if not row.get("sourceItemId"):
            raise ValueError(f"Missing sourceItemId for {row.get('source')}")
        if not row.get("targetItemId"):
            raise ValueError(f"Missing targetItemId for {row.get('target')}")
    return True


def validate_boss_matrix(data):
    rewards = data.get("bossRewards", [])
    if not rewards:
        raise ValueError("bossRewards is empty")
    for row in rewards:
        if not row.get("erBossId"):
            raise ValueError("Missing erBossId in bossRewards")
        if not row.get("isaacItemId"):
            raise ValueError(f"Missing isaacItemId for boss {row.get('erBossId')}")
        if row.get("rewardType") not in {"pedestal", "chest"}:
            raise ValueError(f"Unsupported rewardType for {row.get('erBossId')}")
    return True


def main():
    resources = load_json(RESOURCE_FILE)
    bosses = load_json(BOSS_FILE)

    validate_resource_matrix(resources)
    validate_boss_matrix(bosses)

    print("[OK] resource-conversion.json validated")
    print("[OK] boss-reward-matrix.json validated")
    print("[OK] design sheets are internally consistent")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Preflight failed: {exc}")
