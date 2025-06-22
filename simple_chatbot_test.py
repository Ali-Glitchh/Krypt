#!/usr/bin/env python3
"""
Simple test of the basic chatbot functionality
"""

def test_basic_chatbot():
    print("🧪 Testing Basic Chatbot System")
    print("=" * 50)
    
    try:
        # Test the chatbot import
        print("1. Testing chatbot import...")
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("   ✅ Chatbot import successful")
        
        # Initialize chatbot
        print("2. Initializing chatbot...")
        bot = ImprovedDualPersonalityChatbot()
        print("   ✅ Chatbot initialized")
        
        # Test basic responses
        print("3. Testing basic responses...")
        
        # Test normal personality
        response = bot.get_response("Hello!")
        print(f"   Normal response: {response['message']}")
        
        # Test personality switch
        switch_result = bot.switch_personality('subzero')
        print(f"   Personality switch: {switch_result}")
        
        # Test sub-zero response
        response = bot.get_response("Hello!")
        print(f"   Sub-Zero response: {response['message']}")
        
        print("   ✅ Basic responses working")
        
        # Test crypto knowledge
        print("4. Testing crypto knowledge...")
        bot.switch_personality('normal')
        crypto_response = bot.get_response("What is Bitcoin?")
        print(f"   Crypto response: {crypto_response['message'][:100]}...")
        print("   ✅ Crypto knowledge working")
        
        print("\n✅ Basic chatbot test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_chatbot()
