@echo off
REM KoinToss iframe Deployment Script for Windows
echo 🚀 KoinToss iframe Deployment Script
echo ======================================

REM Create deployment directory
echo 📦 Creating deployment package...
mkdir kointoss-iframe-deploy 2>nul
cd kointoss-iframe-deploy

REM Copy essential files
copy ..\kointoss_iframe_app.py app.py >nul 2>&1
copy ..\requirements_iframe.txt requirements.txt >nul 2>&1
copy ..\README_iframe.md README.md >nul 2>&1

REM Copy chatbot files (try different options)
copy ..\improved_dual_personality_chatbot_fixed.py . >nul 2>&1
if not exist improved_dual_personality_chatbot_fixed.py (
    copy ..\crypto_chatbot_fixed.py . >nul 2>&1
)
if not exist crypto_chatbot_fixed.py (
    copy ..\crypto_chatbot.py . >nul 2>&1
)

REM Copy supporting files
copy ..\crypto_news_insights.py . >nul 2>&1
copy ..\*trainer*.py . >nul 2>&1

REM Create Streamlit config directory
mkdir .streamlit 2>nul

REM Create Streamlit config file
echo [server] > .streamlit\config.toml
echo headless = true >> .streamlit\config.toml
echo port = 8501 >> .streamlit\config.toml
echo. >> .streamlit\config.toml
echo [browser] >> .streamlit\config.toml
echo gatherUsageStats = false >> .streamlit\config.toml
echo showErrorDetails = false >> .streamlit\config.toml
echo. >> .streamlit\config.toml
echo [theme] >> .streamlit\config.toml
echo primaryColor = "#667eea" >> .streamlit\config.toml
echo backgroundColor = "#ffffff" >> .streamlit\config.toml
echo secondaryBackgroundColor = "#f0f2f6" >> .streamlit\config.toml
echo textColor = "#262730" >> .streamlit\config.toml

REM Create Procfile for Heroku
echo web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 > Procfile

REM Create gitignore
echo __pycache__/ > .gitignore
echo *.pyc >> .gitignore
echo .env >> .gitignore

echo.
echo ✅ Deployment package created in: kointoss-iframe-deploy\
echo.
echo 🎯 Next Steps:
echo 1. Push to GitHub: git add . ^&^& git commit -m "Initial commit"
echo 2. Deploy to Streamlit Cloud: https://share.streamlit.io
echo 3. Use the generated URL in your iframe
echo.
echo 📱 iframe Code Example:
echo ^<iframe src="https://your-app.streamlit.app" width="100%%" height="600px"^>^</iframe^>
echo.
echo 🎉 Ready for deployment!
pause
