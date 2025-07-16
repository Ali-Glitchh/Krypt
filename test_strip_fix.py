#!/usr/bin/env python3
"""
Simple test script to verify the strip() error fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    
    print("🚀 Testing KoinToss Chatbot Response Handling")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = ImprovedDualPersonalityChatbot()
    
    # Test messages that might cause the strip() error
    test_messages = [
        "hi",
        "what is bitcoin",
        "switch to subzero",
        "tell me about ethereum"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{message}'")
        
        try:
            # Get response
            response = chatbot.get_response(message)
            
            # Check response type and handle appropriately
            if isinstance(response, dict):
                print(f"   ✅ Dict response: {response.get('message', 'No message key')}")
                print(f"   📝 Type: {response.get('type', 'unknown')}")
                print(f"   🎭 Personality: {response.get('personality', 'unknown')}")
                
                # Test that we can safely extract the message
                message_text = response.get('message', '')
                if isinstance(message_text, str):
                    safe_message = message_text.strip()
                    print(f"   🔧 Stripped safely: '{safe_message[:50]}...'")
                else:
                    print(f"   ⚠️ Message is not string: {type(message_text)}")
                    
            elif isinstance(response, str):
                print(f"   ✅ String response: {response[:100]}...")
                safe_response = response.strip()
                print(f"   🔧 Stripped safely: '{safe_response[:50]}...'")
            else:
                print(f"   ❓ Unexpected response type: {type(response)}")
                print(f"   📄 Content: {response}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print(f"   🔍 Error type: {type(e).__name__}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed! Check results above.")
    
    # Test personality switching
    print("\n🎭 Testing personality switching...")
    try:
        chatbot.switch_personality('subzero')
        subzero_response = chatbot.get_response("hello")
        print(f"   🧊 SubZero response type: {type(subzero_response)}")
        if isinstance(subzero_response, dict):
            print(f"   🧊 SubZero message: {subzero_response.get('message', 'No message')}")
        
        chatbot.switch_personality('normal')
        normal_response = chatbot.get_response("hello")
        print(f"   💬 Normal response type: {type(normal_response)}")
        if isinstance(normal_response, dict):
            print(f"   💬 Normal message: {normal_response.get('message', 'No message')}")
            
    except Exception as e:
        print(f"   ❌ Personality switch error: {e}")
    
except ImportError as e:
    print(f"❌ Could not import chatbot: {e}")
    print("Make sure improved_dual_personality_chatbot.py is available and working.")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n💡 If this test runs without 'dict' object has no attribute 'strip' errors,")
print("   then the Streamlit app should work correctly too!")
