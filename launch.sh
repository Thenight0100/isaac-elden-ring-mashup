#!/bin/bash
# Isaac + Elden Ring Mashup v0.1 launch script
# This is the one-click project-side launcher for the local companion loop.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-$(command -v python3 || command -v python || true)}"

if [ -z "$PYTHON_BIN" ]; then
    echo "[launcher] Python 3 is required and was not found on PATH."
    echo "[launcher] Install Python 3 and rerun this script."
    exit 1
fi

python3 "$SCRIPT_DIR/scripts/install_release.py"

echo "[launcher] Starting Elden Ring bridge monitor..."
python3 "$SCRIPT_DIR/elden-ring/modengine2/er_bridge/bridge_monitor.py" &

# Try common Steam install locations
ISAAC_DIR=""
ER_DIR=""

for dir in \
  "$HOME/.steam/steam/steamapps/common/The Binding of Isaac Repentance" \
  "$HOME/.steam/steam/steamapps/common/The Binding of Isaac Rebirth" \
  "$HOME/.local/share/Steam/steamapps/common/The Binding of Isaac Repentance" \
  "$HOME/.local/share/Steam/steamapps/common/The Binding of Isaac Rebirth" ; do
  if [ -f "$dir/isaac" ] || [ -f "$dir/isaac.exe" ]; then
    ISAAC_DIR="$dir"
  fi
done

for dir in \
  "$HOME/.steam/steam/steamapps/common/ELDEN RING" \
  "$HOME/.local/share/Steam/steamapps/common/ELDEN RING" ; do
  if [ -f "$dir/eldenring.exe" ] || [ -f "$dir/eldenring" ]; then
    ER_DIR="$dir"
  fi
done

if [ -n "$ISAAC_DIR" ]; then
  echo "[launcher] Launching Isaac: $ISAAC_DIR"
  if [ -f "$ISAAC_DIR/isaac" ]; then
    "$ISAAC_DIR/isaac" &
  elif [ -f "$ISAAC_DIR/isaac.exe" ]; then
    cmd.exe /c start "" "$ISAAC_DIR/isaac.exe" >/dev/null 2>&1 || "${ISAAC_DIR}/isaac.exe" &
  fi
fi

if [ -n "$ER_DIR" ]; then
  echo "[launcher] Launching Elden Ring: $ER_DIR"
  if [ -f "$ER_DIR/eldenring" ]; then
    "$ER_DIR/eldenring" &
  elif [ -f "$ER_DIR/eldenring.exe" ]; then
    cmd.exe /c start "" "$ER_DIR/eldenring.exe" >/dev/null 2>&1 || "${ER_DIR}/eldenring.exe" &
  fi
fi

if [ -z "$ISAAC_DIR" ] && [ -z "$ER_DIR" ]; then
  echo "[launcher] Could not auto-detect Steam installs for Isaac or Elden Ring."
  echo "[launcher] Install both Steam games, then run this script again."
fi

read -p "Press Enter to exit the launcher..."
