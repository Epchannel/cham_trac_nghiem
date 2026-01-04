@echo off
REM Khởi động Streamlit OMR App

cd /d "%~dp0"

echo.
echo ========================================
echo   OMR Sheet Evaluation System
echo   Streamlit + Webcam + Remote Access
echo ========================================
echo.

python run_with_tunnel.py

pause
