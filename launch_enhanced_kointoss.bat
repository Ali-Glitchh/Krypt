@echo off
echo ========================================
echo   KoinToss Enhanced AI Assistant
echo ========================================
echo.
echo Starting the enhanced KoinToss AI with:
echo  - Sentiment analysis integration
echo  - Enhanced response generation
echo  - Improved answering capabilities
echo.

cd /d "c:\Users\Dell\Desktop\Krypt"

if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo.
echo Launching KoinToss Enhanced AI Assistant...
echo.
echo Features:
echo  - Dual personality modes (Educational/Warrior)
echo  - Real-time sentiment analysis
echo  - Enhanced crypto knowledge base
echo  - Market data integration
echo.
echo App will be available at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

echo.
echo App stopped. Press any key to exit...
pause > nul
