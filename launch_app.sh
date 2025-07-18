#!/bin/bash
# KoinToss App Launch Script

echo "🚀 Launching KoinToss Streamlit App..."
echo "==========================================="

# Check if streamlit is available
if command -v streamlit &> /dev/null; then
    echo "✅ Streamlit is available"
else
    echo "❌ Streamlit not found"
    echo "Please install streamlit: pip install streamlit"
    exit 1
fi

# Check if the app file exists
if [ -f "streamlit_app.py" ]; then
    echo "✅ streamlit_app.py found"
else
    echo "❌ streamlit_app.py not found"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

# Launch the app
echo "🌟 Starting KoinToss app..."
echo "📱 The app will open in your default browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run streamlit_app.py
