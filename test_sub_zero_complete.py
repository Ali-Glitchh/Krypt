#!/usr/bin/env python3
"""
Complete test for Sub-Zero crypto chatbot integration
Tests both datasets and Sub-Zero personality features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crypto_chatbot import CryptoChatbot

def test_sub_zero_integration():
    """Test Sub-Zero dataset integration and personality"""
    print("🧊 Testing Sub-Zero Crypto Chatbot Integration")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = CryptoChatbot()
    
    # Test 1: Dataset Loading
    print("\n1. Testing Dataset Loading:")
    print(f"   Greetings loaded: {len(chatbot.chat_dataset.get('greetings', []))}")
    print(f"   Crypto knowledge loaded: {len(chatbot.chat_dataset.get('crypto_knowledge', []))}")
    print(f"   Sub-Zero responses loaded: {len(chatbot.chat_dataset.get('sub_zero_responses', []))}")
    print(f"   Sub-Zero jokes loaded: {len(chatbot.chat_dataset.get('sub_zero_jokes', []))}")
    
    # Test 2: Sub-Zero Greetings
    print("\n2. Testing Sub-Zero Greetings:")
    greeting_response = chatbot.generate_response("hello")
    print(f"   Response: {greeting_response['message']}")
    
    # Test 3: Sub-Zero Jokes
    print("\n3. Testing Sub-Zero Jokes:")
    joke_response = chatbot.get_smart_response('general', 'tell me a joke')
    print(f"   Joke: {joke_response}")
    
    # Test 4: Crypto Knowledge with Sub-Zero Style
    print("\n4. Testing Crypto Knowledge:")
    crypto_tests = [
        "What is Bitcoin?",
        "Tell me about Ethereum",
        "What's blockchain?",
        "Explain DeFi",
        "What is HODL?",
        "What are NFTs?"
    ]
    
    for query in crypto_tests:
        response = chatbot.generate_response(query)
        print(f"   Q: {query}")
        print(f"   A: {response['message'][:100]}...")
        print()
    
    # Test 5: Sub-Zero Specific Responses
    print("\n5. Testing Sub-Zero Specific Responses:")
    sub_zero_tests = [
        "What's your favorite crypto?",
        "Tell me about staking",
        "What are gas fees?",
        "Explain mining"
    ]
    
    for query in sub_zero_tests:
        response = chatbot.get_smart_response('crypto_general', query)
        print(f"   Q: {query}")
        print(f"   A: {response}")
        print()
    
    # Test 6: Verify "hi" doesn't return Shiba Inu
    print("\n6. Testing 'Hi' Issue Fix:")
    hi_response = chatbot.generate_response("hi")
    print(f"   'hi' response: {hi_response['message']}")
    print(f"   Should NOT mention Shiba Inu: {'shiba' not in hi_response['message'].lower()}")
    
    print("\n🎉 Sub-Zero Integration Test Complete!")
    print("The chatbot now has Sub-Zero's icy personality with crypto expertise!")

if __name__ == "__main__":
    test_sub_zero_integration()
