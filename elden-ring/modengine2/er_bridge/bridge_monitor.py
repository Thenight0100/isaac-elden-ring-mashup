#!/usr/bin/env python3
import json
import time
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().with_name("config.json")


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_log_line(line: str):
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def main():
    config = load_config()
    log_path = Path(config["logPath"])
    state_path = Path(config["statePath"])
    state_path.parent.mkdir(parents=True, exist_ok=True)

    if not state_path.exists():
        state_path.write_text('{"seenEvents": []}\n', encoding="utf-8")

    while True:
        if log_path.exists():
            with log_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    event = parse_log_line(raw_line)
                    if not event:
                        continue

                    event_type = event.get("event")
                    payload = event.get("payload", {})

                    if event_type == "pickup":
                        source = payload.get("type", "unknown")
                        if source in {"coins", "bombs", "keys", "hearts"}:
                            print(f"[ER monitor] pickup event -> {source}")
                    elif event_type == "room_clear":
                        print("[ER monitor] room clear detected")
                    elif event_type == "bridge_start":
                        print("[ER monitor] bridge online")

        time.sleep(config.get("refreshSeconds", 1))


if __name__ == "__main__":
    main()
