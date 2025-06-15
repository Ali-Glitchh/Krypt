#!/usr/bin/env python3
"""
Quick compatibility test for Streamlit and enhanced chatbot
"""

def test_compatibility():
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} loaded successfully")
        
        from crypto_chatbot import CryptoChatbot
        print("✅ Enhanced Sub-Zero chatbot imported")
        
        bot = CryptoChatbot()
        print("✅ Chatbot instance created with training data")
        
        # Test response
        response = bot.generate_response("Hello!")
        print(f"✅ Sample response: {response['message'][:60]}...")
        
        print("\n🎉 Everything is compatible and ready!")
        print("💡 You can now run: python -m streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_compatibility()
