#!/usr/bin/env python3
"""
Test script for Sub-Zero crypto dataset integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crypto_chatbot import chatbot

def test_sub_zero_responses():
    """Test Sub-Zero personality responses"""
    print("🧊 Testing Sub-Zero Crypto Chatbot Integration 🧊")
    print("=" * 60)
    
    # Test different types of queries
    test_queries = [
        ("hi", "greeting"),
        ("hello", "greeting"),
        ("what is bitcoin?", "crypto knowledge"),
        ("tell me about ethereum", "crypto knowledge"),
        ("what is blockchain?", "blockchain explanation"),
        ("explain defi", "defi explanation"),
        ("what is staking?", "staking info"),
        ("tell me a joke", "humor request"),
        ("what is hodl?", "crypto slang"),
        ("what are gas fees?", "technical question"),
        ("explain nft", "nft explanation"),
        ("what is a dao?", "dao explanation"),
        ("help me understand wallets", "wallet info"),
        ("bye", "farewell")
    ]
    
    for query, description in test_queries:
        print(f"\n🔹 Query: '{query}' ({description})")
        print("-" * 40)
        
        try:
            response = chatbot.generate_response(query)
            print(f"Response Type: {response.get('type', 'unknown')}")
            print(f"Message: {response.get('message', 'No message')}")
            
            # Also test direct smart response
            smart_response = chatbot.get_smart_response('crypto_general', query)
            if smart_response:
                print(f"Smart Response: {smart_response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Sub-Zero Integration Test Complete! ❄️")
    
    # Test dataset loading
    print(f"\nDataset Categories Loaded:")
    for category, responses in chatbot.chat_dataset.items():
        print(f"  📂 {category}: {len(responses)} responses")
    
    # Test Sub-Zero specific responses
    print(f"\n🧊 Sub-Zero Jokes Available: {len(chatbot.chat_dataset.get('sub_zero_jokes', []))}")
    print(f"🧊 Sub-Zero Responses Available: {len(chatbot.chat_dataset.get('sub_zero_responses', []))}")
    
    if chatbot.chat_dataset.get('sub_zero_jokes'):
        print(f"\nSample Sub-Zero Joke:")
        print(f"  {chatbot.chat_dataset['sub_zero_jokes'][0]}")

if __name__ == "__main__":
    test_sub_zero_responses()
