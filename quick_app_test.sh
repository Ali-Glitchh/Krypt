#!/bin/bash
# KoinToss Streamlit App Quick Launch Test
echo "🚀 Testing KoinToss Streamlit App Launch..."

cd "c:\Users\Dell\Desktop\Krypt"

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️ Activating virtual environment..."
    source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null
fi

# Test basic imports
echo "📦 Testing imports..."
python -c "
import streamlit as st
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
print('✅ All imports successful')
bot = ImprovedDualPersonalityChatbot()
print('✅ Chatbot initialized')
response = bot.get_response('Hello KoinToss')
if isinstance(response, dict) and 'message' in response:
    print('✅ Chatbot responding correctly')
else:
    print('❌ Chatbot response issue')
    print('Response type:', type(response))
"

if [ $? -eq 0 ]; then
    echo "🎉 All components working! Ready to launch Streamlit app."
    echo "💡 To launch the app, run: streamlit run streamlit_app.py"
    echo "🌐 The app will be available at: http://localhost:8501"
else
    echo "❌ Component test failed. Check error messages above."
fi
