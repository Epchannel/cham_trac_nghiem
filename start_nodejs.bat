@echo off
echo ============================================================
echo   OMR SHEET EVALUATION SYSTEM - NODE.JS VERSION
echo ============================================================
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [1/3] Installing Node.js dependencies...
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please make sure Node.js and npm are installed.
        pause
        exit /b 1
    )
    echo.
) else (
    echo [1/3] Dependencies already installed
    echo.
)

REM Check if uploads directory exists
if not exist "uploads\" (
    echo [2/3] Creating uploads directory...
    mkdir uploads
    echo.
) else (
    echo [2/3] Uploads directory exists
    echo.
)

echo [3/3] Starting server...
echo.
echo ============================================================
echo   Server will start on: http://localhost:3000
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start the server
node server.js

pause

