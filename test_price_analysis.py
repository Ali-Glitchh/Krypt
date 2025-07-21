#!/usr/bin/env python3
"""
Test Enhanced Price Analysis System
"""

def test_price_analysis():
    print("Testing Enhanced Price Analysis with News Sentiment...")
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        bot = ImprovedDualPersonalityChatbot()
        print("Bot initialized successfully")
        
        # Test price queries
        test_queries = [
            "price of bitcoin",
            "what is bitcoin worth",
            "ethereum price",
            "BITCOIN PRICE NOW"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*50}")
            print(f"Test {i}: {query}")
            print(f"{'='*50}")
            
            response = bot.get_response(query)
            
            if isinstance(response, dict):
                print(f"Response Type: {response.get('type', 'unknown')}")
                print(f"Personality: {response.get('personality', 'unknown')}")
                
                # Check if it's a price analysis response
                if response.get('type') == 'price_analysis_with_news':
                    print("✅ PRICE ANALYSIS WITH NEWS SENTIMENT DETECTED!")
                    print(f"Crypto Symbol: {response.get('crypto_symbol', 'N/A')}")
                    
                    news_sentiment = response.get('news_sentiment', {})
                    print(f"News Sentiment: {news_sentiment.get('overall_sentiment', 'N/A')}")
                    print(f"Headlines Analyzed: {news_sentiment.get('headlines_analyzed', 0)}")
                    
                    # Show first part of message
                    message = response.get('message', '')
                    print(f"Response Preview: {message[:200]}...")
                else:
                    print("⚠️ Not recognized as price analysis")
                    message = response.get('message', '')
                    print(f"Response Preview: {message[:150]}...")
            else:
                print("❌ Invalid response format")
        
        # Test personality switching for price queries
        print(f"\n{'='*50}")
        print("Testing Warrior Mode Price Analysis")
        print(f"{'='*50}")
        
        bot.switch_personality('subzero')
        warrior_response = bot.get_response("bitcoin price")
        
        if isinstance(warrior_response, dict):
            if warrior_response.get('type') == 'price_analysis_with_news':
                print("✅ WARRIOR PRICE ANALYSIS WORKING!")
                message = warrior_response.get('message', '')
                print(f"Warrior Response Preview: {message[:200]}...")
            else:
                print("⚠️ Warrior price analysis not working as expected")
        
        print("\n🎉 Price analysis testing complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_price_analysis()
