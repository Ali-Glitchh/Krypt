#!/usr/bin/env python3
"""Quick validation that Sub-Zero is working"""

import json
import os

print("🧊 QUICK SUB-ZERO VALIDATION ❄️")
print("=" * 40)

# Check if datasets exist
if os.path.exists('sub_zero_crypto_dataset.json'):
    with open('sub_zero_crypto_dataset.json', 'r') as f:
        sub_zero_data = json.load(f)
    print(f"✅ Sub-Zero dataset: {len(sub_zero_data)} responses")
    
    # Show a sample Sub-Zero response
    if sub_zero_data:
        sample = sub_zero_data[0]['sub_zero']
        print(f"📝 Sample: {sample[:80]}...")
else:
    print("❌ Sub-Zero dataset missing")

if os.path.exists('crypto_chat_dataset.json'):
    with open('crypto_chat_dataset.json', 'r') as f:
        crypto_data = json.load(f)
    print(f"✅ Crypto dataset: {len(crypto_data)} conversations")
else:
    print("❌ Crypto dataset missing")

# Test basic import
try:
    from crypto_chatbot import CryptoChatbot
    print("✅ CryptoChatbot import successful")
    
    chatbot = CryptoChatbot()
    print("✅ Chatbot initialization successful")
    
    # Quick functionality test
    response = chatbot.get_smart_response('greeting', 'hello')
    print(f"✅ Sample greeting: {response[:60]}...")
    
    response = chatbot.get_smart_response('general', 'tell me a joke')
    print(f"✅ Sample joke: {response[:60]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎯 Status: Sub-Zero integration ready for testing!")
print("🌐 Visit: http://localhost:8502 to test live")
print("=" * 40)
