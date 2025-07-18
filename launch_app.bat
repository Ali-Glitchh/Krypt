@echo off
REM KoinToss App Launch Script for Windows

echo 🚀 Launching KoinToss Streamlit App...
echo ===========================================

REM Check if streamlit is available
where streamlit >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Streamlit not found
    echo Please install streamlit: pip install streamlit
    pause
    exit /b 1
)

echo ✅ Streamlit is available

REM Check if the app file exists
if exist "streamlit_app.py" (
    echo ✅ streamlit_app.py found
) else (
    echo ❌ streamlit_app.py not found
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

echo 🌟 Starting KoinToss app...
echo 📱 The app will open in your default browser
echo 🔗 URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

streamlit run streamlit_app.py
