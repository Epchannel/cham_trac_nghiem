@echo off
REM Script để mở VS Code Dev Tunnel cho Streamlit app

echo ========================================
echo  VS Code Dev Tunnel Setup
echo ========================================
echo.

REM Kiểm tra VS Code CLI có được cài không
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] VS Code CLI không được tìm thấy!
    echo.
    echo Hãy cài đặt VS Code Dev Tunnel:
    echo 1. Mở VS Code
    echo 2. Nhấn Ctrl+Shift+P
    echo 3. Gõ "Dev Tunnels" và chọn "Dev Tunnel: Open Tunnel in Current Folder"
    echo 4. Hoặc cài code CLI: https://code.visualstudio.com/docs/remote/tunnels
    echo.
    pause
    exit /b 1
)

echo [INFO] Bắt đầu dev tunnel...
echo.

code tunnel

echo.
echo [SUCCESS] Dev tunnel đã được mở!
echo Bạn có thể truy cập qua link được cung cấp trên điện thoại hoặc máy khác.
echo.
pause
