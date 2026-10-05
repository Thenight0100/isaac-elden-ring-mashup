#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-$(command -v python3 || command -v python || true)}"

if [ -z "$PYTHON_BIN" ]; then
  echo "[launcher] Python 3 is required and was not found on PATH."
  exit 1
fi

python3 "$SCRIPT_DIR/scripts/install_release.py"

echo "[launcher] Starting Elden Ring bridge monitor..."
python3 "$SCRIPT_DIR/elden-ring/modengine2/er_bridge/bridge_monitor.py" &

ISAAC_DIR=""
ER_DIR=""
for dir in \
  "$HOME/.steam/steam/steamapps/common/The Binding of Isaac Repentance" \
  "$HOME/.steam/steam/steamapps/common/The Binding of Isaac Rebirth" \
  "$HOME/.local/share/Steam/steamapps/common/The Binding of Isaac Repentance" \
  "$HOME/.local/share/Steam/steamapps/common/The Binding of Isaac Rebirth"; do
  if [ -f "$dir/isaac" ] || [ -f "$dir/isaac.exe" ]; then
    ISAAC_DIR="$dir"
  fi
done

for dir in \
  "$HOME/.steam/steam/steamapps/common/ELDEN RING" \
  "$HOME/.local/share/Steam/steamapps/common/ELDEN RING"; do
  if [ -f "$dir/eldenring" ] || [ -f "$dir/eldenring.exe" ]; then
    ER_DIR="$dir"
  fi
done

if [ -n "$ISAAC_DIR" ]; then
  echo "[launcher] Launching Isaac: $ISAAC_DIR"
  if [ -f "$ISAAC_DIR/isaac" ]; then
    "$ISAAC_DIR/isaac" &
  elif [ -f "$ISAAC_DIR/isaac.exe" ]; then
    "$ISAAC_DIR/isaac.exe" &
  fi
else
  echo "[launcher] Isaac install not found. Install The Binding of Isaac: Repentance, then run this launcher again."
fi

if [ -n "$ER_DIR" ]; then
  echo "[launcher] Launching Elden Ring: $ER_DIR"
  if [ -f "$ER_DIR/eldenring" ]; then
    "$ER_DIR/eldenring" &
  elif [ -f "$ER_DIR/eldenring.exe" ]; then
    "$ER_DIR/eldenring.exe" &
  fi
else
  echo "[launcher] Elden Ring install not found. Install Elden Ring, then run this launcher again."
fi

if [ -z "$ISAAC_DIR" ] && [ -z "$ER_DIR" ]; then
  echo "[launcher] The required Steam games are not installed on this machine."
  exit 1
fi

read -p "Press Enter to exit the launcher..."
