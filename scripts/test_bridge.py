#!/usr/bin/env python3
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# Test mode: simulate Isaac bridge events without needing the game running.

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "elden-ring" / "modengine2" / "er_bridge" / "config.json"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def generate_fake_events(count=10):
    events = []
    base_time = datetime.utcnow() - timedelta(seconds=count * 5)

    # Bridge start event
    events.append({
        "ts": base_time.isoformat() + "Z",
        "event": "bridge_start",
        "payload": {"status": "online", "mod": "isaac_er_bridge", "version": "0.1"},
    })

    # Random pickup events
    item_types = ["coins", "bombs", "keys", "hearts"]
    for i in range(count - 2):
        ts = (base_time + timedelta(seconds=(i + 1) * 5)).isoformat() + "Z"
        item_type = random.choice(item_types)
        events.append({
            "ts": ts,
            "event": "pickup",
            "payload": {
                "type": item_type,
                "variant": random.randint(0, 5),
                "roomIndex": random.randint(0, 10),
                "player": "testPlayer",
            },
        })

    # Room clear event
    events.append({
        "ts": (base_time + timedelta(seconds=count * 5)).isoformat() + "Z",
        "event": "room_clear",
        "payload": {"roomIndex": random.randint(0, 10), "status": "clear"},
    })

    return events


def write_fake_log(log_path: Path, events: list):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")
    print(f"[Test] Wrote {len(events)} fake events to {log_path}")


def main():
    config = load_config()
    log_path = Path(config["logPath"])

    events = generate_fake_events(count=10)
    write_fake_log(log_path, events)

    print("[Test] Fake bridge log ready. Run the monitor with:")
    print(f"       python3 elden-ring/modengine2/er_bridge/bridge_monitor.py")
    print()
    print("[Test] The monitor should read and echo these events without needing Isaac or ER running.")


if __name__ == "__main__":
    main()
