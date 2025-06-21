#!/usr/bin/env python3
"""
Interactive Demo of Enhanced Crypto Chatbot
Demonstrates real-time price data, news, personality switching, and conversation
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot

def interactive_demo():
    print("🚀 ENHANCED CRYPTO CHATBOT - INTERACTIVE DEMO")
    print("=" * 60)
    print("Features:")
    print("🔸 Real-time crypto price data")
    print("🔸 Personality switching (Normal ↔ Sub-Zero)")
    print("🔸 Natural conversation with training data")
    print("🔸 Crypto news queries")
    print("🔸 Context-aware responses")
    print("-" * 60)
    
    bot = EnhancedCryptoChatbot()
    
    print(f"🤖 Bot initialized in {bot.personality_mode} mode")
    print("💡 Try these commands:")
    print("   • 'What is the price of Bitcoin?'")
    print("   • 'Switch to Sub-Zero mode'")
    print("   • 'Latest Bitcoin news'")
    print("   • 'How are you doing?'")
    print("   • 'quit' to exit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                farewell_response = bot.generate_response("goodbye")
                print(f"🤖 Bot: {farewell_response['message']}")
                break
            
            if not user_input:
                continue
            
            response = bot.generate_response(user_input)
            print(f"🤖 Bot: {response['message']}")
            
            # Show additional info for special response types
            if response['type'] == 'price_query' and response.get('data'):
                data = response['data']
                print(f"   📊 Live Data: ${data['current_price']:,.2f} ({data['price_change_24h']:+.2f}%)")
            
            elif response['type'] == 'personality_switch':
                print(f"   🎭 Current mode: {bot.personality_mode}")
            
            elif response['type'] == 'news_query' and response.get('data'):
                print(f"   📰 News articles found: {len(response['data'])}")
                
        except KeyboardInterrupt:
            print("\\n\\n👋 Demo ended by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def quick_feature_demo():
    """Quick demonstration of key features"""
    print("\\n🎯 QUICK FEATURE DEMONSTRATION")
    print("=" * 50)
    
    bot = EnhancedCryptoChatbot()
    
    demos = [
        ("Hello!", "Basic greeting"),
        ("What's the price of Bitcoin?", "Real-time price data"),
        ("Switch to Sub-Zero mode", "Personality switching"),
        ("Tell me the price of Ethereum", "Price in Sub-Zero mode"),
        ("What's the latest crypto news?", "News query"),
        ("How are you doing?", "Natural conversation"),
        ("Normal mode", "Switch back to normal"),
        ("Goodbye", "Farewell")
    ]
    
    for query, description in demos:
        print(f"\\n[{description.upper()}]")
        print(f"👤 You: {query}")
        
        response = bot.generate_response(query)
        print(f"🤖 Bot: {response['message']}")
        
        # Show metadata
        if response.get('data') and response['type'] == 'price_query':
            data = response['data']
            print(f"   💰 Price: ${data['current_price']:,.2f}")
        
        print(f"   🏷️ Type: {response['type']}")

if __name__ == "__main__":
    # Run quick demo first
    quick_feature_demo()
    
    # Ask if user wants interactive demo
    print("\\n" + "="*60)
    choice = input("🎮 Start interactive demo? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        interactive_demo()
    else:
        print("👋 Demo completed! The enhanced chatbot is ready to use.")
