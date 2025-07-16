#!/bin/bash
# KoinToss iframe Deployment Automation Script
# Deploys your app to multiple free hosting platforms

echo "🚀 KoinToss iframe Deployment Script"
echo "======================================"

# Create deployment package
echo "📦 Creating deployment package..."

# Create deployment directory
mkdir -p kointoss-iframe-deploy
cd kointoss-iframe-deploy

# Copy essential files
cp ../kointoss_iframe_app.py ./app.py
cp ../requirements_iframe.txt ./requirements.txt
cp ../README_iframe.md ./README.md

# Copy chatbot files (try different options)
if [ -f ../improved_dual_personality_chatbot_fixed.py ]; then
    cp ../improved_dual_personality_chatbot_fixed.py ./
elif [ -f ../crypto_chatbot_fixed.py ]; then
    cp ../crypto_chatbot_fixed.py ./
elif [ -f ../crypto_chatbot.py ]; then
    cp ../crypto_chatbot.py ./
fi

# Copy supporting files
cp ../crypto_news_insights.py ./ 2>/dev/null || echo "Note: crypto_news_insights.py not found"
cp ../*trainer*.py ./ 2>/dev/null || echo "Note: trainer files not found"

# Create Streamlit config
mkdir -p .streamlit
cat > .streamlit/config.toml << EOF
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
showErrorDetails = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

# Create Procfile for Heroku
cat > Procfile << EOF
web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
EOF

# Create railway.json for Railway
cat > railway.json << EOF
{
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
EOF

# Create render.yaml for Render
cat > render.yaml << EOF
services:
  - type: web
    name: kointoss-iframe
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
    healthCheckPath: /
EOF

# Initialize git repository
git init
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore

echo "✅ Deployment package created in: kointoss-iframe-deploy/"
echo ""
echo "🎯 Next Steps:"
echo "1. Push to GitHub: cd kointoss-iframe-deploy && git add . && git commit -m 'Initial commit'"
echo "2. Deploy to Streamlit Cloud: https://share.streamlit.io"
echo "3. Use the generated URL in your iframe"
echo ""
echo "📱 iframe Code Example:"
echo '<iframe src="https://your-app.streamlit.app" width="100%" height="600px"></iframe>'
echo ""
echo "🎉 Ready for deployment!"
