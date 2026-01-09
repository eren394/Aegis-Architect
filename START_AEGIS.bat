@echo off
title AEGIS ARCHITECT - Master Control
color 0B

echo [0/3] Killing previous instances...
taskkill /F /IM aegis_core.exe /T >nul 2>&1

echo [1/3] Compiling C++ Core...
g++ core/src/main.cpp core/src/ResourceEmitter.cpp -Icore/include -o aegis_core.exe -lws2_32

if %errorlevel% neq 0 (
    echo [ERROR] C++ Compilation failed! Make sure the .exe is not running elsewhere.
    pause
    exit /b
)

echo [2/3] Starting Aegis Mind...
start "Aegis Mind" C:\msys64\ucrt64\bin\python.exe brain/analyzer.py

echo [WAIT] Waiting for Mind to initialize...
timeout /t 3 > nul

echo [3/3] Launching Aegis Core...
start "Aegis Core" aegis_core.exe

echo.
echo ============================================
echo   AEGIS ARCHITECT IS NOW LIVE 
echo ============================================
pause