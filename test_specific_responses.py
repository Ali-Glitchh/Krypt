#!/usr/bin/env python3
"""Test specific responses: greeting and name inquiry"""

from crypto_chatbot import CryptoChatbot

print("🧊 TESTING SPECIFIC SUB-ZERO RESPONSES ❄️")
print("=" * 50)

try:
    chatbot = CryptoChatbot()
    print("✅ Chatbot initialized successfully")
    
    print("\n🎭 Testing Specific Responses:")
    print("-" * 30)
    
    # Test 1: "hi" greeting
    print("\n1️⃣ Testing: 'hi'")
    response1 = chatbot.generate_response("hi")
    print(f"   Type: {response1.get('type', 'unknown')}")
    print(f"   Message: {response1.get('message', 'No response')}")
    
    # Test 2: Asking for name
    print("\n2️⃣ Testing: 'what is your name'")
    response2 = chatbot.generate_response("what is your name")
    print(f"   Type: {response2.get('type', 'unknown')}")
    print(f"   Message: {response2.get('message', 'No response')}")
    
    # Test 3: Alternative name question
    print("\n3️⃣ Testing: 'who are you'")
    response3 = chatbot.generate_response("who are you")
    print(f"   Type: {response3.get('type', 'unknown')}")
    print(f"   Message: {response3.get('message', 'No response')}")
    
    # Test 4: Another greeting variation
    print("\n4️⃣ Testing: 'hello'")
    response4 = chatbot.generate_response("hello")
    print(f"   Type: {response4.get('type', 'unknown')}")
    print(f"   Message: {response4.get('message', 'No response')}")
    
    print("\n" + "=" * 50)
    print("❄️ Response testing complete!")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
