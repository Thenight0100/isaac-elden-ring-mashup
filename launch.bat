@echo off
REM Isaac + Elden Ring Mashup v0.1 Launcher
REM One-click launch for the offline companion loop.

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set LOG_DIR=C:\Games\IsaacERBridge
set ISAAC_LOG=%LOG_DIR%\isaac_er_bridge.log
set ER_MONITOR_PY=%SCRIPT_DIR%elden-ring\modengine2\er_bridge\bridge_monitor.py

echo.
echo [Mashup] Preparing offline companion loop...
echo.

REM Create bridge log directory if missing
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
    echo [Mashup] Created bridge log directory: %LOG_DIR%
)

REM Clear old log if requested
if "%1"=="--fresh" (
    del "%ISAAC_LOG%" /f /q 2>nul
    echo [Mashup] Cleared old bridge log
)

REM Start ER bridge monitor in background
echo [Mashup] Starting Elden Ring bridge monitor...
start "ER Bridge Monitor" python "%ER_MONITOR_PY%"
echo [Mashup] Monitor started
echo.

echo [Mashup] Ready to launch games:
echo   1. Launch Elden Ring via ModEngine2 (offline, EAC disabled)
echo   2. Launch Isaac with isaac_er_bridge mod enabled
echo.
echo [Mashup] The bridge log will sync pickups and room clears in real-time.
echo.
pause
