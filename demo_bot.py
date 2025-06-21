#!/usr/bin/env python3
"""
Demo script showing the Enhanced Crypto Chatbot capabilities
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot
import time

def main():
    print("🚀 Enhanced Crypto Chatbot Demo")
    print("=" * 50)
    
    # Initialize the bot
    bot = EnhancedCryptoChatbot()
    
    # Demo queries
    demo_queries = [
        "Hello there!",
        "What is the current price of bitcoin?",
        "Can you give me news about ethereum?", 
        "Switch to Sub-Zero mode",
        "What's the price of dogecoin?",
        "Tell me about recent crypto news",
        "Switch to normal mode",
        "What do you think about the market today?",
        "Thanks, goodbye!"
    ]
    
    print(f"Current personality mode: {bot.personality_mode}")
    print("\nStarting demo conversation...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"👤 User: {query}")
        
        # Get bot response
        response = bot.generate_response(query)
        
        # Show response with type info
        print(f"🤖 Bot ({response['type']}): {response['message']}")
        print(f"   [Personality: {bot.personality_mode}]")
        print("-" * 50)
        
        # Small delay for readability
        time.sleep(1)
    
    print("\n✅ Demo completed!")
    print("\n🎯 Key Features Demonstrated:")
    print("✓ Real-time crypto price queries")
    print("✓ Crypto news and insights")
    print("✓ Personality switching (Normal ↔ Sub-Zero)")
    print("✓ Natural conversation abilities")
    print("✓ Intent detection and appropriate responses")

if __name__ == "__main__":
    main()
