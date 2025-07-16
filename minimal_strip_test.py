#!/usr/bin/env python3
"""
Simple test to isolate the strip error
"""

def minimal_test():
    """Test just the essential parts"""
    print("🔍 Minimal Strip Error Test")
    print("=" * 40)
    
    try:
        # Test 1: Direct import
        print("1. Testing import...")
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("   ✅ Import successful")
        
        # Test 2: Create instance
        print("2. Creating chatbot...")
        chatbot = ImprovedDualPersonalityChatbot()
        print("   ✅ Chatbot created")
        
        # Test 3: Simple response
        print("3. Testing simple response...")
        try:
            response = chatbot.get_response("hi")
            print(f"   ✅ Response: {type(response)}")
            if isinstance(response, dict) and 'message' in response:
                print(f"   ✅ Message: {response['message'][:30]}...")
            else:
                print(f"   ⚠️ Unexpected response format: {response}")
        except Exception as e:
            print(f"   ❌ Response error: {e}")
            import traceback
            traceback.print_exc()
            
        # Test 4: Personality switch
        print("4. Testing personality switch...")
        try:
            chatbot.switch_personality('subzero')
            response = chatbot.get_response("hi")
            print(f"   ✅ SubZero response: {type(response)}")
            if isinstance(response, dict) and 'message' in response:
                print(f"   ✅ Message: {response['message'][:30]}...")
        except Exception as e:
            print(f"   ❌ SubZero error: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Minimal test completed")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_test()
