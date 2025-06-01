#!/usr/bin/env python3
"""
Live test of Sub-Zero integration features
Tests the actual user experience with Sub-Zero responses
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from crypto_chatbot import CryptoChatbot

def test_sub_zero_personality():
    """Test Sub-Zero personality in live responses"""
    print("🧊 LIVE SUB-ZERO INTEGRATION TEST ❄️")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = CryptoChatbot()
    
    # Test various user inputs that should trigger Sub-Zero responses
    test_inputs = [
        "hi",
        "hello",
        "what's your favorite crypto?",
        "tell me a joke",
        "what is bitcoin?",
        "explain ethereum",
        "what's blockchain?", 
        "what are NFTs?",
        "what is DeFi?",
        "explain staking",
        "what's mining?",
        "tell me about wallets",
        "what's your name?",
        "who are you?",
        "help me with crypto"
    ]
    
    print("\n🎭 Testing Sub-Zero Personality Responses:")
    print("-" * 45)
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{i}. User: '{user_input}'")
        
        # Get response from chatbot
        response = chatbot.generate_response(user_input)
        
        # Display the response
        message = response.get('message', 'No response')
        response_type = response.get('type', 'unknown')
        
        print(f"   Type: {response_type}")
        print(f"   Sub-Zero: {message[:200]}{'...' if len(message) > 200 else ''}")
        
        # Check for Sub-Zero personality indicators
        sub_zero_indicators = ['ice', 'frost', 'freeze', 'sub-zero', 'frozen', 'cold', 'mortal']
        has_personality = any(indicator in message.lower() for indicator in sub_zero_indicators)
        
        if has_personality:
            print("   ✅ Sub-Zero personality detected!")
        else:
            print("   ⚠️  Generic response (no Sub-Zero personality)")
    
    print("\n" + "=" * 50)
    print("🧊 DATASET SUMMARY:")
    print(f"   Sub-Zero responses: {len(chatbot.chat_dataset.get('sub_zero_responses', []))}")
    print(f"   Sub-Zero jokes: {len(chatbot.chat_dataset.get('sub_zero_jokes', []))}")
    print(f"   General greetings: {len(chatbot.chat_dataset.get('greetings', []))}")
    print(f"   Crypto knowledge: {len(chatbot.chat_dataset.get('crypto_knowledge', []))}")
    
    print("\n❄️ Test Complete! Sub-Zero is ready to freeze out the competition! ❄️")

if __name__ == "__main__":
    test_sub_zero_personality()
