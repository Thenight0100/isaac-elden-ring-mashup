#!/bin/bash
# Isaac + Elden Ring Mashup v0.1 Launcher
# One-click launch for the offline companion loop.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$HOME/.IsaacERBridge"
ISAAC_LOG="$LOG_DIR/isaac_er_bridge.log"
ER_MONITOR_PY="$SCRIPT_DIR/elden-ring/modengine2/er_bridge/bridge_monitor.py"

echo ""
echo "[Mashup] Preparing offline companion loop..."
echo ""

# Create bridge log directory if missing
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo "[Mashup] Created bridge log directory: $LOG_DIR"
fi

# Clear old log if requested
if [ "$1" = "--fresh" ]; then
    rm -f "$ISAAC_LOG"
    echo "[Mashup] Cleared old bridge log"
fi

# Start ER bridge monitor in background
echo "[Mashup] Starting Elden Ring bridge monitor..."
python3 "$ER_MONITOR_PY" &
MONITOR_PID=$!
echo "[Mashup] Monitor started (PID: $MONITOR_PID)"
echo ""

echo "[Mashup] Ready to launch games:"
echo "  1. Launch Elden Ring via ModEngine2 (offline, EAC disabled)"
echo "  2. Launch Isaac with isaac_er_bridge mod enabled"
echo ""
echo "[Mashup] The bridge log will sync pickups and room clears in real-time."
echo ""
echo "Press Enter to continue..."
read
