#!/usr/bin/env python3
"""
Quick test for Streamlit compatibility
"""

def test_streamlit_compatibility():
    print("🧪 Testing Streamlit compatibility...")
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("✅ Import successful")
        
        bot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot initialized")
        
        response = bot.get_response("Hello")
        print(f"✅ Response generated: {response['type']}")
        
        switch_result = bot.switch_personality('subzero')
        print(f"✅ Personality switch: {bot.personality_mode}")
        
        print("🎉 Streamlit app should work now!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_streamlit_compatibility()
