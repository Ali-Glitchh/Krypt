import json
import os

# Test if the datasets can be loaded directly
print("Testing dataset loading...")

# Test Sub-Zero dataset
try:
    with open('sub_zero_crypto_dataset.json', 'r', encoding='utf-8') as f:
        sub_zero_data = json.load(f)
    print(f"✅ Sub-Zero dataset loaded: {len(sub_zero_data)} entries")
    print(f"First entry: {sub_zero_data[0]['sub_zero'][:100]}...")
except Exception as e:
    print(f"❌ Error loading Sub-Zero dataset: {e}")

# Test original crypto dataset
try:
    with open('crypto_chat_dataset.json', 'r', encoding='utf-8') as f:
        crypto_data = json.load(f)
    print(f"✅ Crypto dataset loaded: {len(crypto_data)} entries")
    print(f"First entry: {crypto_data[0]['output'][:100]}...")
except Exception as e:
    print(f"❌ Error loading crypto dataset: {e}")

print("\nTesting basic chatbot import...")
try:
    import sys
    sys.path.append('.')
    from crypto_chatbot import CryptoChatbot
    print("✅ Chatbot imported successfully")
    
    bot = CryptoChatbot()
    print("✅ Chatbot initialized")
    
    # Test basic response
    response = bot.generate_response("hello")
    print(f"✅ Hello response: {response['message'][:100]}...")
    
except Exception as e:
    print(f"❌ Error with chatbot: {e}")
    import traceback
    traceback.print_exc()
