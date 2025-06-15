#!/usr/bin/env python3
"""
Live test of the enhanced Sub-Zero chatbot
"""

from crypto_chatbot import CryptoChatbot

def test_enhanced_chatbot():
    print("Testing Enhanced Sub-Zero Chatbot with Natural Conversation Training")
    print("=" * 70)
    
    bot = CryptoChatbot()
    print()
    
    # Test various conversation types
    test_cases = [
        ("Hello!", "Basic greeting"),
        ("How are you doing today?", "Casual question"),
        ("What do you like to do for fun?", "Personal interest"),
        ("Tell me about Bitcoin", "Crypto expertise"),
        ("Should I invest in crypto?", "Investment advice"),
        ("Any plans for the weekend?", "Natural conversation"),
        ("Tell me a crypto joke", "Humor request"),
        ("What is your favorite food?", "Personal preference"),
        ("Goodbye", "Farewell")
    ]
    
    for query, test_type in test_cases:
        print(f"[{test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.generate_response(query)
        print(f"Sub-Zero: {response['message']}")
        print(f"(Response type: {response['type']})")
        print("-" * 50)
    
    print("Enhanced chatbot test completed!")

if __name__ == "__main__":
    test_enhanced_chatbot()
