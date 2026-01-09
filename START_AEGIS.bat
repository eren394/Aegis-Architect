@echo off
:: 1. Önce Python'ı (Zihin) başlatıyoruz
echo [STEP 1] Starting Aegis Mind (Python)...
start "" python brain/analyzer.py

:: 2. Python'ın portu dinlemeye başlaması için kısa bir es veriyoruz
echo [WAIT] Waiting for Mind to wake up...
timeout /t 4 > nul

:: 3. Python hazır olduğunda C++ (Core) veri göndermeye başlayabilir
echo [STEP 2] Launching Aegis Core (C++)...
start "" aegis_core.exe