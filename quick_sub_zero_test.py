#!/usr/bin/env python3
"""Quick test of Sub-Zero functionality"""

try:
    from crypto_chatbot import CryptoChatbot
    
    print("🧊 QUICK SUB-ZERO TEST ❄️")
    print("Initializing chatbot...")
    
    chatbot = CryptoChatbot()
    
    print("Testing basic responses:")
    
    # Test greeting
    response1 = chatbot.generate_response("hello")
    print(f"Greeting: {response1.get('message', 'No response')[:100]}...")
    
    # Test joke
    response2 = chatbot.generate_response("tell me a joke")
    print(f"Joke: {response2.get('message', 'No response')[:100]}...")
    
    # Test crypto question
    response3 = chatbot.generate_response("what is bitcoin")
    print(f"Bitcoin: {response3.get('message', 'No response')[:100]}...")
    
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
