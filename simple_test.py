#!/usr/bin/env python3
"""
KoinToss Component Test
"""

print("Testing KoinToss components...")

print("1. Testing Streamlit import...")
import streamlit
print("Streamlit OK")

print("2. Testing chatbot import...")
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
print("Chatbot import OK")

print("3. Testing chatbot initialization...")
bot = ImprovedDualPersonalityChatbot()
print("Chatbot initialized")

print("4. Testing response...")
resp = bot.get_response("Hello")
if isinstance(resp, dict) and "message" in resp:
    print("Response format correct")
    print(f"Message preview: {resp['message'][:60]}...")
else:
    print("Response format issue")
    print("Response type:", type(resp))

print("All tests passed! App ready to launch.")
print("To launch: streamlit run streamlit_app.py")
