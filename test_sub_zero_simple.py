#!/usr/bin/env python3
"""Simple Sub-Zero test with explicit output"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🧊 Starting Sub-Zero Test...", flush=True)

try:
    from crypto_chatbot import CryptoChatbot
    print("✅ Successfully imported CryptoChatbot", flush=True)
    
    chatbot = CryptoChatbot()
    print("✅ Chatbot initialized successfully", flush=True)
    
    # Test dataset loading
    print(f"📊 Dataset stats:", flush=True)
    print(f"   Sub-Zero responses: {len(chatbot.chat_dataset.get('sub_zero_responses', []))}", flush=True)
    print(f"   Sub-Zero jokes: {len(chatbot.chat_dataset.get('sub_zero_jokes', []))}", flush=True)
    print(f"   Greetings: {len(chatbot.chat_dataset.get('greetings', []))}", flush=True)
    
    # Test a greeting
    print("\n🎭 Testing greeting...", flush=True)
    response = chatbot.generate_response("hello")
    print(f"Response type: {response.get('type', 'unknown')}", flush=True)
    print(f"Message: {response.get('message', 'No message')[:150]}...", flush=True)
    
    # Test a joke request
    print("\n😄 Testing joke request...", flush=True)
    response = chatbot.generate_response("tell me a joke")
    print(f"Response type: {response.get('type', 'unknown')}", flush=True)
    print(f"Joke: {response.get('message', 'No message')[:150]}...", flush=True)
    
    # Test crypto question
    print("\n💰 Testing crypto question...", flush=True)
    response = chatbot.generate_response("what is bitcoin")
    print(f"Response type: {response.get('type', 'unknown')}", flush=True)
    print(f"Bitcoin info: {response.get('message', 'No message')[:150]}...", flush=True)
    
    print("\n❄️ Sub-Zero integration test completed successfully!", flush=True)
    
except Exception as e:
    print(f"❌ Error occurred: {str(e)}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
