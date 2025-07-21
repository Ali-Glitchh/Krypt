@echo off
echo 🎓 Launching KoinToss AI - Educational Mode with MoonshotAI
echo ===================================================
echo.

REM Check Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if streamlit is available
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Streamlit not installed. Installing...
    pip install streamlit
)

echo ✅ Streamlit available

REM Check chatbot integration
python -c "from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot; bot = ImprovedSinglePersonalityChatbot(); print('✅ Educational chatbot ready'); print('🌙 MoonshotAI integrated:', bool(bot.moonshot_ai))" 2>nul

echo.
echo 🚀 Starting KoinToss AI - Educational Mode...
echo    • Friendly, educational cryptocurrency assistance
echo    • Enhanced with MoonshotAI Kimi K2 for complex queries
echo    • Real-time price data and market analysis
echo    • News sentiment analysis
echo    • Clean, beginner-friendly interface
echo.
echo 🌐 Opening in browser at: http://localhost:8501
echo 🔥 Press Ctrl+C to stop the server
echo.

REM Launch Streamlit app
streamlit run streamlit_app.py --server.port=8501 --server.headless=false

pause
