#!/usr/bin/env python3
"""
Test script to verify the crypto chat dataset integration
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from crypto_chatbot import chatbot

def test_dataset_integration():
    """Test that the dataset is properly loaded and responses are enhanced"""
    print("🧪 Testing Crypto Chat Dataset Integration")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        "hi",
        "hello",
        "what is bitcoin?",
        "tell me about ethereum",
        "what is blockchain?",
        "how does mining work?",
        "what are wallets?",
        "explain defi",
        "bitcoin price",
        "help me with crypto"
    ]
    
    print("📊 Dataset Statistics:")
    print(f"   Greetings: {len(chatbot.chat_dataset['greetings'])}")
    print(f"   Crypto Knowledge: {len(chatbot.chat_dataset['crypto_knowledge'])}")
    print(f"   Investment Advice: {len(chatbot.chat_dataset['investment_advice'])}")
    print(f"   Security Tips: {len(chatbot.chat_dataset['security_tips'])}")
    print(f"   General: {len(chatbot.chat_dataset['general'])}")
    print()
    
    print("🤖 Testing Responses:")
    print("-" * 30)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. User: {test_input}")
        
        # Get intent
        intent = chatbot.detect_query_intent(test_input)
        print(f"   Intent: {intent}")
        
        # Get smart response from dataset
        dataset_response = chatbot.get_smart_response(intent, test_input)
        print(f"   Dataset Response: {dataset_response}")
        
        # Get full response
        response = chatbot.generate_response(test_input)
        print(f"   Full Response: {response['message']}")
        print(f"   Type: {response['type']}")
        
        print("-" * 30)
    
    print("\n✅ Dataset integration test completed!")

if __name__ == "__main__":
    test_dataset_integration()
