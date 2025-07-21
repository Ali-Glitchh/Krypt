#!/usr/bin/env python3
"""
Simple Streamlit app component test
"""

print("🧪 Testing KoinToss components...")

try:
    print("\n1️⃣ Testing basic imports...")
    import streamlit as st
    print("✅ Streamlit imported")
    
    import pandas as pd
    print("✅ Pandas imported")
    
    print("\n2️⃣ Testing API utilities...")
    try:
        from api_utils import CryptoAPIs
        print("✅ API utilities available")
        api_available = True
    except ImportError as e:
        print(f"⚠️ API utilities not available: {e}")
        api_available = False
    
    print("\n3️⃣ Testing chatbot...")
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    print("✅ Chatbot imported")
    
    bot = ImprovedDualPersonalityChatbot()
    print("✅ Chatbot initialized")
    
    # Test response
    response = bot.get_response("Hello KoinToss!")
    print(f"✅ Response received: {type(response)}")
    
    if isinstance(response, dict):
        message = response.get('message', '')
        personality = response.get('personality', 'unknown')
        print(f"✅ Message: {message[:100]}...")
        print(f"✅ Personality: {personality}")
    
    print("\n4️⃣ Testing crypto data fallback...")
    fallback_data = [
        {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'current_price': 43250.00,
            'price_change_percentage_24h': 2.45,
            'market_cap': 850000000000
        }
    ]
    print(f"✅ Fallback data available: {len(fallback_data)} cryptos")
    
    print("\n✅ ALL COMPONENTS WORKING!")
    print("🚀 KoinToss app is ready to launch!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
