@echo off
REM Isaac + Elden Ring Mashup v0.1 launcher
REM This script installs the Isaac companion mod in the player's Steam install,
REM prepares the local bridge runtime, and launches the required games.

setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if not errorlevel 1 (
  set PYTHON=py
) else (
  where python >nul 2>nul
  if not errorlevel 1 (
    set PYTHON=python
  ) else (
    echo [launcher] Python 3 is required and was not found on PATH.
    echo [launcher] Install Python 3, then rerun this launcher.
    pause
    exit /b 1
  )
)

call "%PYTHON%" "%SCRIPT_DIR%scripts\install_release.py"
if errorlevel 1 (
  echo [launcher] Release setup failed.
  pause
  exit /b 1
)

echo [launcher] Starting Elden Ring bridge monitor...
start "ER Bridge Monitor" "%PYTHON%" "%SCRIPT_DIR%elden-ring\modengine2\er_bridge\bridge_monitor.py"

echo [launcher] Looking for Steam installs of Isaac and Elden Ring...

set ISAAC_DIR=
set ER_DIR=

for %%D in (
  "C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Repentance"
  "C:\Program Files\Steam\steamapps\common\The Binding of Isaac Repentance"
  "C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth"
  "C:\Program Files\Steam\steamapps\common\The Binding of Isaac Rebirth"
) do (
  if exist "%%~D\isaac.exe" (
    set "ISAAC_DIR=%%~D"
  )
)

for %%D in (
  "C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING"
  "C:\Program Files\Steam\steamapps\common\ELDEN RING"
) do (
  if exist "%%~D\eldenring.exe" (
    set "ER_DIR=%%~D"
  )
)

if not "%ISAAC_DIR%"=="" (
  echo [launcher] Launching Isaac: %ISAAC_DIR%\isaac.exe
  start "Isaac" "%ISAAC_DIR%\isaac.exe"
) else (
  echo [launcher] Isaac install not found. Install The Binding of Isaac: Repentance, then run this launcher again.
)

if not "%ER_DIR%"=="" (
  echo [launcher] Launching Elden Ring: %ER_DIR%\eldenring.exe
  start "Elden Ring" "%ER_DIR%\eldenring.exe"
) else (
  echo [launcher] Elden Ring install not found. Install Elden Ring, then run this launcher again.
)

if "%ISAAC_DIR%"=="" if "%ER_DIR%"=="" (
  echo [launcher] The required Steam games are not installed on this machine.
  pause
  exit /b 1
)

echo [launcher] Startup sequence complete.
pause
