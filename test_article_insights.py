#!/usr/bin/env python3
"""
Test script for enhanced chatbot with article insights
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot

def test_enhanced_chatbot():
    print("🚀 Testing Enhanced Chatbot with Article Insights")
    print("=" * 55)
    
    bot = EnhancedCryptoChatbot()
    
    # Test queries
    test_queries = [
        "Tell me about DeFi from your articles",
        "What insights do you have about Bitcoin?", 
        "Explain Ethereum staking from your analysis",
        "What do your articles say about NFTs?",
        "Switch to Sub-Zero mode",
        "Tell me about your insights on DeFi",
        "What's the price of Bitcoin?",
        "Switch to normal mode"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = bot.generate_response(query)
        print(f"🤖 Bot ({response['type']}): {response['message'][:200]}...")
        print(f"   [Personality: {bot.personality_mode}]")
        print("-" * 50)
    
    print("\n✅ Test completed!")
    print("\n🎯 Features Demonstrated:")
    print("✓ Article insights from knowledge base")
    print("✓ Real-time crypto price queries")
    print("✓ Personality switching (Normal ↔ Sub-Zero)")
    print("✓ Intent detection for different query types")

if __name__ == "__main__":
    test_enhanced_chatbot()
