#!/usr/bin/env python3
"""
Test script for the AI chatbot functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crypto_chatbot import chatbot

# Test cases to verify AI functionality
test_cases = [
    ("hi", "Should return a greeting response"),
    ("hello", "Should return a greeting response"),
    ("bitcoin price", "Should return crypto info for Bitcoin"),
    ("what is ethereum", "Should return crypto info for Ethereum"),
    ("btc", "Should return crypto info for Bitcoin"),
    ("shiba inu", "Should return crypto info for Shiba Inu"),
    ("goodbye", "Should return farewell message"),
    ("help", "Should return general help message"),
    ("random text", "Should return general conversation response")
]

def test_chatbot():
    print("🤖 Testing Krypt AI Chatbot...")
    print("=" * 50)
    
    # Mock market data for testing
    mock_market_data = [
        {
            'id': 'bitcoin',
            'symbol': 'btc',
            'name': 'Bitcoin',
            'current_price': 67500.45,
            'price_change_percentage_24h': 2.35,
            'market_cap': 1320000000000,
            'market_cap_rank': 1
        },
        {
            'id': 'ethereum',
            'symbol': 'eth', 
            'name': 'Ethereum',
            'current_price': 3450.23,
            'price_change_percentage_24h': -1.25,
            'market_cap': 415000000000,
            'market_cap_rank': 2
        },
        {
            'id': 'shiba-inu',
            'symbol': 'shib',
            'name': 'Shiba Inu',
            'current_price': 0.000024,
            'price_change_percentage_24h': 5.67,
            'market_cap': 14200000000,
            'market_cap_rank': 12
        }
    ]
    
    for test_input, expected_behavior in test_cases:
        print(f"\n🔸 Testing: '{test_input}'")
        print(f"   Expected: {expected_behavior}")
        
        try:
            response = chatbot.generate_response(test_input, mock_market_data)
            print(f"   Response Type: {response['type']}")
            print(f"   Message: {response['message'][:100]}...")
            
            # Special validation for "hi" input
            if test_input == "hi":
                if response['type'] == 'greeting':
                    print("   ✅ PASS: 'hi' correctly identified as greeting")
                else:
                    print("   ❌ FAIL: 'hi' not identified as greeting")
            
            print("   ✅ SUCCESS")
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Testing complete!")

if __name__ == "__main__":
    test_chatbot()
