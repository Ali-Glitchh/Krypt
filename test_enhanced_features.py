#!/usr/bin/env python3
"""
Comprehensive test for the Enhanced Crypto Chatbot
Tests real-time data, news, personality switching, and natural conversation
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot

def test_enhanced_features():
    print("🚀 Testing Enhanced Crypto Chatbot with Real-time Data & Personality Modes")
    print("=" * 80)
    
    bot = EnhancedCryptoChatbot()
    print()
    
    # Test cases covering all new features
    test_cases = [
        # Basic greeting
        ("Hello!", "Basic greeting"),
        
        # Personality switching
        ("Switch to Sub-Zero mode", "Personality switching"),
        
        # Price queries in Sub-Zero mode
        ("What is the current price of Bitcoin?", "Bitcoin price query (Sub-Zero mode)"),
        ("Tell me the price of Ethereum", "Ethereum price query (Sub-Zero mode)"),
        
        # Switch back to normal mode
        ("Switch to normal mode", "Switch to normal personality"),
        
        # Price queries in normal mode  
        ("What's the current price of Bitcoin?", "Bitcoin price query (normal mode)"),
        ("How much is Dogecoin worth?", "Dogecoin price query (normal mode)"),
        
        # News queries
        ("What's the latest Bitcoin news?", "Bitcoin news query"),
        ("Any recent Ethereum updates?", "Ethereum news query"),
        
        # Natural conversation
        ("How are you doing today?", "Natural conversation"),
        ("What do you think about the market?", "Market opinion"),
        
        # Switch back to Sub-Zero for farewell
        ("Sub-Zero mode", "Switch to Sub-Zero for farewell"),
        ("Goodbye", "Farewell (Sub-Zero mode)")
    ]
    
    print("🧪 Running comprehensive test scenarios...")
    print("-" * 60)
    
    for i, (query, test_type) in enumerate(test_cases, 1):
        print(f"\\n[TEST {i}: {test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.generate_response(query)
        print(f"Bot: {response['message']}")
        print(f"(Type: {response['type']}, Action: {response['action']})")
        
        # Show additional data if available
        if 'data' in response and response['data']:
            if response['type'] == 'price_query':
                data = response['data']
                print(f"📊 Price Data: ${data['current_price']:,.2f} ({data['price_change_24h']:+.2f}%)")
            elif response['type'] == 'news_query':
                print(f"📰 News Articles: {len(response['data'])} found")
        
        print("-" * 60)
    
    print("\\n🎉 Enhanced chatbot test completed!")
    print("\\n✅ Features tested:")
    print("  • Real-time crypto price data")
    print("  • Personality switching (Normal ↔ Sub-Zero)")
    print("  • Natural conversation with training data")
    print("  • News queries (with fallback)")
    print("  • Context-aware responses")
    
    print(f"\\n🤖 Current personality mode: {bot.personality_mode}")

def test_specific_crypto_prices():
    """Test price queries for different cryptocurrencies"""
    print("\\n💰 Testing specific cryptocurrency price queries...")
    print("-" * 50)
    
    bot = EnhancedCryptoChatbot()
    
    cryptos_to_test = [
        "Bitcoin",
        "Ethereum", 
        "Dogecoin",
        "Cardano",
        "Solana"
    ]
    
    for crypto in cryptos_to_test:
        query = f"What's the current price of {crypto}?"
        print(f"\\nTesting: {query}")
        response = bot.generate_response(query)
        print(f"Response type: {response['type']}")
        if 'data' in response and response['data']:
            data = response['data']
            print(f"✅ Got price data: ${data['current_price']:,.2f}")
        else:
            print("⚠️ No price data returned")

if __name__ == "__main__":
    test_enhanced_features()
    test_specific_crypto_prices()
