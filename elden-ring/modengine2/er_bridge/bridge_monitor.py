#!/usr/bin/env python3
import json
import time
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().with_name("config.json")
STATE_PATH = Path(__file__).resolve().parent / "state.json"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_state():
    if not STATE_PATH.exists():
        STATE_PATH.write_text('{"seenEvents": []}\n', encoding="utf-8")
    with STATE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state):
    with STATE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def parse_log_line(line: str):
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def handle_event(event, state):
    event_key = event.get("event")
    payload = event.get("payload", {})
    seen = state.setdefault("seenEvents", [])

    marker = (event_key, json.dumps(payload, sort_keys=True))
    if marker in seen:
        return

    seen.append(marker)
    if len(seen) > 500:
        del seen[:-250]

    if event_key == "pickup":
        item_type = payload.get("type", "unknown")
        print(f"[ER monitor] pickup: {item_type}")
    elif event_key == "room_clear":
        print("[ER monitor] room clear detected")
    elif event_key == "bridge_start":
        print("[ER monitor] bridge online")
    else:
        print(f"[ER monitor] unhandled event: {event_key}")


def main():
    config = load_config()
    state = load_state()
    log_path = Path(config["logPath"])

    while True:
        if log_path.exists():
            with log_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    event = parse_log_line(raw_line)
                    if not event:
                        continue
                    handle_event(event, state)
            save_state(state)

        time.sleep(config.get("refreshSeconds", 1))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[ER monitor] stopping")
    except Exception as exc:
        raise SystemExit(f"Bridge monitor failed: {exc}")
