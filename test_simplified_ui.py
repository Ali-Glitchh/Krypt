#!/usr/bin/env python3
"""
Test Simplified KoinToss UI
"""

def test_simplified_ui():
    print("Testing simplified UI components...")
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("Chatbot import OK")
        
        bot = ImprovedDualPersonalityChatbot()
        print("Bot initialization OK")
        
        # Test response
        response = bot.get_response('hello')
        print("Response generation OK")
        if isinstance(response, dict):
            print("Response keys:", list(response.keys()))
        
        # Test personality switch
        result = bot.switch_personality('subzero')
        print("Personality switch OK")
        
        print("\nAll simplified UI components working!")
        return True
        
    except Exception as e:
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    success = test_simplified_ui()
    if success:
        print("\nSimplified KoinToss UI is ready!")
    else:
        print("\nThere are issues to fix.")
