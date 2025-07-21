@echo off
echo ==========================================
echo   KoinToss AI - Price Analysis Enhanced
echo ==========================================
echo.
echo New Features:
echo  - Real-time price data with news sentiment
echo  - Comprehensive crypto market analysis  
echo  - News headline sentiment analysis
echo  - Enhanced price query responses
echo.

cd /d "c:\Users\Dell\Desktop\Krypt"

if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo.
echo Testing price analysis system...
python -c "print('Testing price analysis...'); from advanced_price_news_analyzer import AdvancedPriceNewsAnalyzer; analyzer = AdvancedPriceNewsAnalyzer(); result = analyzer.generate_price_analysis_response('price of bitcoin', 'normal'); print('✅ Price analysis working!' if result else '❌ Price analysis failed')"

echo.
echo Launching KoinToss AI with Enhanced Price Analysis...
echo.
echo Now when you ask "price of bitcoin" you will get:
echo  - Current price and market data
echo  - News sentiment analysis
echo  - Recent headlines impact
echo  - Comprehensive market insight
echo.
echo App available at: http://localhost:8501
echo.

streamlit run streamlit_app.py

echo.
pause
