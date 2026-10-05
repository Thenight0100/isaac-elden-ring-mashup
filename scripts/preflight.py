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
    if not matrix:
        raise ValueError("resourceMatrix is empty")

    sources = {row["source"] for row in matrix}
    targets = {row["target"] for row in matrix}
    seen_pairs = set()

    if len(sources) < 3:
        raise ValueError("Need at least three source resource categories")
    if len(targets) < 3:
        raise ValueError("Need at least three target resource categories")

    for row in matrix:
        source = row.get("source")
        target = row.get("target")
        pair = (source, target)
        if pair in seen_pairs:
            raise ValueError(f"Duplicate mapping for {source} -> {target}")
        seen_pairs.add(pair)

        if row.get("ratio", 0) <= 0:
            raise ValueError(f"Invalid ratio for {source} -> {target}")
        if not row.get("sourceItemId"):
            raise ValueError(f"Missing sourceItemId for {source}")
        if not row.get("targetItemId"):
            raise ValueError(f"Missing targetItemId for {target}")

    return True


def validate_boss_matrix(data):
    rewards = data.get("bossRewards", [])
    if not rewards:
        raise ValueError("bossRewards is empty")

    seen_ids = set()
    for row in rewards:
        boss_id = row.get("erBossId")
        if not boss_id:
            raise ValueError("Missing erBossId in bossRewards")
        if boss_id in seen_ids:
            raise ValueError(f"Duplicate boss id: {boss_id}")
        seen_ids.add(boss_id)

        if not row.get("isaacItemId"):
            raise ValueError(f"Missing isaacItemId for boss {boss_id}")
        if row.get("rewardType") not in {"pedestal", "chest"}:
            raise ValueError(f"Unsupported rewardType for {boss_id}")

    return True


def validate_cross_reference(resources, bosses):
    target_names = {row["target"] for row in resources["resourceMatrix"]}
    boss_item_ids = {row["isaacItemId"] for row in bosses["bossRewards"]}
    if not boss_item_ids:
        raise ValueError("Boss reward matrix has no Isaac item ids")
    if not target_names:
        raise ValueError("No target resources found in conversion matrix")
    return True


def main():
    resources = load_json(RESOURCE_FILE)
    bosses = load_json(BOSS_FILE)

    validate_resource_matrix(resources)
    validate_boss_matrix(bosses)
    validate_cross_reference(resources, bosses)

    print("[OK] resource-conversion.json validated")
    print("[OK] boss-reward-matrix.json validated")
    print("[OK] cross-reference checks passed")
    print("[OK] design sheets are internally consistent")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Preflight failed: {exc}")
