@echo off
REM Chạy Streamlit với tất cả host (0.0.0.0)
REM Cho phép truy cập từ bất kỳ máy nào trên mạng

cd /d "%~dp0"

echo.
echo ========================================
echo   OMR App - Network Mode (0.0.0.0)
echo ========================================
echo.
echo Streamlit sẽ lắng nghe trên tất cả host
echo Truy cập từ:
echo   - Local: http://localhost:8501
echo   - Network: http://<IP>:8501
echo.

python -m streamlit run main.py --server.address=0.0.0.0

pause
