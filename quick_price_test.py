#!/usr/bin/env python3
"""
Quick Test - Enhanced Price Response System
"""
import sys
sys.path.append('.')

def quick_test():
    try:
        print("Quick test of price analysis system...")
        
        from advanced_price_news_analyzer import AdvancedPriceNewsAnalyzer
        analyzer = AdvancedPriceNewsAnalyzer()
        
        # Test basic functionality
        result = analyzer.generate_price_analysis_response("price of bitcoin", "normal")
        
        if result:
            print("\n✅ Price Analysis Working!")
            print(f"Crypto: {result['crypto_symbol']}")
            print(f"Sentiment: {result['news_sentiment']['overall_sentiment']}")
            print(f"Message length: {len(result['message'])} characters")
            print("\nFirst 200 characters of response:")
            print(result['message'][:200] + "...")
            return True
        else:
            print("❌ No result generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Enhanced price analysis system is working!")
        print("Launch the Streamlit app to test the full integration.")
    else:
        print("\n⚠️ There are issues with the price analysis system.")
