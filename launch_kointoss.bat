@echo off
echo ====================================
echo   KoinToss AI Assistant Launcher
echo ====================================

cd /d "c:\Users\Dell\Desktop\Krypt"

echo Checking virtual environment...
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
)

echo.
echo Launching KoinToss AI Assistant...
echo App will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

pause
