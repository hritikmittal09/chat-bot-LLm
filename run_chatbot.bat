                                                                                                                   @echo off
title Chat-Bot LLM Launcher
cd /d "E:\chat-bot-LLm"

echo ==========================================
echo   Starting Chat-Bot LLM Assistant...
echo ==========================================
echo.

REM Activate virtual environment if it exists (.venv folder)
IF EXIST ".venv\Scripts\activate.bat" (
    echo [1/2] Activating virtual environment...
    call .venv\Scripts\activate.bat
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    echo [1/2] Activating virtual environment...
    call venv\Scripts\activate.bat
) ELSE (
    echo [INFO] No venv found, using system Python / uv directly...
)

echo [2/2] Launching assistant...
echo.

REM Run with uv (preferred)
uv run main.py

REM If uv fails, fallback to python
IF %ERRORLEVEL% NEQ 0 (
    echo [WARN] uv run failed, trying python directly...
    python main.py
)

echo.
echo ==========================================
echo   Assistant closed. Press any key to exit.
echo ==========================================
pause
