@echo off
echo ========================================================
echo Starting Smriti Car Rental System
echo ========================================================

echo.
echo Initializing database and seed data...
call .venv\Scripts\python scripts\seed_data.py

echo.
echo Starting Customer Application (Port 5000)...
start "Customer App" cmd /k "call .venv\Scripts\activate && python customer_server.py"

echo Starting Admin Application (Port 5001)...
start "Admin App" cmd /k "call .venv\Scripts\activate && python admin_server.py"

echo.
echo Servers are starting in separate windows.
echo - Customer Interface: http://127.0.0.1:5000
echo - Admin Interface:    http://127.0.0.1:5001
echo.
echo Close this window or press any key to exit.
pause > nul
