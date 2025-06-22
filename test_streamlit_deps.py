#!/usr/bin/env python3
"""
Test Streamlit app dependencies without running the full app
"""

def test_streamlit_dependencies():
    print("🧪 Testing Streamlit App Dependencies")
    print("=" * 50)
    
    try:
        print("1. Testing basic imports...")
        import streamlit as st
        import pandas as pd
        import requests
        import time
        from datetime import datetime
        import plotly.graph_objects as go
        import re
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        print("   ✅ Basic imports working")
        
        print("2. Testing API utilities...")
        try:
            from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
            print("   ✅ API utilities imported successfully")
            
            # Try to initialize without causing issues
            print("   Testing CryptoAPIs initialization...")
            api = CryptoAPIs()
            print("   ✅ CryptoAPIs initialized")
        except Exception as e:
            print(f"   ⚠️ API utilities error (but app can continue): {e}")
        
        print("3. Testing chatbot import...")
        try:
            from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
            print("   ✅ Chatbot imported successfully")
        except Exception as e:
            print(f"   ❌ Chatbot import failed: {e}")
            return False
        
        print("\n✅ All critical dependencies working!")
        print("🚀 Streamlit app should be deployable")
        return True
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_streamlit_dependencies()
