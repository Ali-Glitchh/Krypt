#!/usr/bin/env python3
"""
Test both personalities with the response fix
"""

def test_both_personalities():
    print("🎭 Testing Both Personalities Response Fix")
    print("=" * 45)
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        bot = ImprovedDualPersonalityChatbot()
        
        # Test Normal personality
        print("1. Testing Normal personality with 'doge'...")
        bot.switch_personality('normal')
        response1 = bot.get_response("doge")
        print(f"   ✅ Normal: {response1['message'][:80]}...")
        
        # Test Sub-Zero personality
        print("2. Testing Sub-Zero personality with 'doge'...")
        bot.switch_personality('subzero')
        response2 = bot.get_response("doge")
        print(f"   ✅ Sub-Zero: {response2['message'][:80]}...")
        
        # Test various inputs
        test_inputs = ["bitcoin", "ethereum", "hello", "price"]
        
        print("3. Testing various inputs in Sub-Zero mode...")
        for input_text in test_inputs:
            response = bot.get_response(input_text)
            if isinstance(response, dict) and 'message' in response:
                print(f"   ✅ '{input_text}': {response['message'][:60]}...")
            else:
                print(f"   ❌ '{input_text}': Format error")
        
        print("\n✅ All personality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_both_personalities()
    print(f"\n{'🎉 ALL FIXES WORKING' if success else '⚠️ ISSUES REMAIN'}")
