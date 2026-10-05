@echo off
REM Isaac + Elden Ring Mashup v0.1 launch script
REM This is the one-click project-side launcher for the local companion loop.

setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0
set PYTHON=%PYTHON%

if "%PYTHON%"=="" (
  where py >nul 2>nul
  if not errorlevel 1 (
    set PYTHON=py
  ) else (
    where python >nul 2>nul
    if not errorlevel 1 (
      set PYTHON=python
    ) else (
      echo [launcher] Python 3 is required and was not found on PATH.
      echo [launcher] Install Python 3 and rerun this script.
      pause
      exit /b 1
    )
  )
)

REM Make sure the bridge and mod directory are initialized in standard install locations
call "%PYTHON%" "%SCRIPT_DIR%scripts\install_release.py"
if errorlevel 1 (
  echo [launcher] Release setup failed.
  pause
  exit /b 1
)

echo [launcher] Starting Elden Ring bridge monitor...
start "ER Bridge Monitor" "%PYTHON%" "%SCRIPT_DIR%elden-ring\modengine2\er_bridge\bridge_monitor.py"

REM If the game directories are present, start the games next.
set ISAAC_DIR=
set ER_DIR=

for %%D in ("C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Repentance" "C:\Program Files\Steam\steamapps\common\The Binding of Isaac Repentance" "C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth" "C:\Program Files\Steam\steamapps\common\The Binding of Isaac Rebirth") do (
  if exist %%~D\isaac.exe (
    set "ISAAC_DIR=%%~D"
  )
)
for %%D in ("C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING" "C:\Program Files\Steam\steamapps\common\ELDEN RING") do (
  if exist %%~D\eldenring.exe (
    set "ER_DIR=%%~D"
  )
)

if not "%ISAAC_DIR%"=="" (
  echo [launcher] Launching Isaac: %ISAAC_DIR%\isaac.exe
  start "Isaac" "%ISAAC_DIR%\isaac.exe"
)

if not "%ER_DIR%"=="" (
  echo [launcher] Launching Elden Ring: %ER_DIR%\eldenring.exe
  start "Elden Ring" "%ER_DIR%\eldenring.exe"
)

if "%ISAAC_DIR%"=="" if "%ER_DIR%"=="" (
  echo [launcher] Could not auto-detect Steam installs for Isaac or Elden Ring.
  echo [launcher] Install both Steam games, then run this script again.
)

pause
