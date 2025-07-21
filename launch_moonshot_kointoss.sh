#!/bin/bash
echo "🌙 Launching KoinToss AI with MoonshotAI Integration..."
echo "=============================================="
echo ""

# Check Python availability
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python."
    exit 1
fi

echo "✅ Python found"

# Check if streamlit is available
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Streamlit not installed. Installing..."
    pip install streamlit
fi

echo "✅ Streamlit available"

# Check MoonshotAI integration
python -c "from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot; bot = ImprovedDualPersonalityChatbot(); print('✅ MoonshotAI integrated:', bool(bot.moonshot_ai))" 2>/dev/null

echo ""
echo "🚀 Starting KoinToss AI with MoonshotAI Kimi K2..."
echo "   • Enhanced conversation capabilities"
echo "   • Advanced crypto analysis"
echo "   • Dual personality modes"
echo "   • Real-time price data"
echo "   • News sentiment analysis"
echo ""
echo "🌐 Opening in browser at: http://localhost:8501"
echo "🔥 Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit app
streamlit run streamlit_app.py --server.port=8501 --server.headless=false
