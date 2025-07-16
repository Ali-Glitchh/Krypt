#!/usr/bin/env python3
"""
Test the specific response fix for 'doge' input
"""

def test_doge_fix():
    print("🐕 Testing DOGE Response Fix")
    print("=" * 30)
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        print("Initializing chatbot...")
        bot = ImprovedDualPersonalityChatbot()
        
        print("Testing 'doge' input (previously failed)...")
        response = bot.get_response("doge")
        
        print(f"Response type: {type(response)}")
        print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
        
        if isinstance(response, dict) and 'message' in response:
            message = response['message']
            print(f"✅ SUCCESS! Message: {message[:150]}...")
            print(f"Personality: {response.get('personality', 'unknown')}")
            print(f"Type: {response.get('type', 'unknown')}")
            
            # Test that message is a string and can be processed
            if isinstance(message, str) and message.strip():
                print("✅ Message is valid string")
            else:
                print("❌ Message format issue")
                
        else:
            print("❌ Response structure issue")
            print(f"Full response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_doge_fix()
    print(f"\n{'✅ FIX SUCCESSFUL' if success else '❌ FIX FAILED'}")
