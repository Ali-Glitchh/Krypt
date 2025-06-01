#!/usr/bin/env python3
"""
Quick test for the AI fixes
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ai_fixes():
    print("🤖 Testing AI Fixes...")
    print("=" * 40)
    
    try:
        from crypto_chatbot import chatbot
        print("✅ Chatbot imported successfully")
        
        # Test cases that were problematic
        test_cases = [
            ("hi", "greeting"),
            ("hello", "greeting"), 
            ("hey", "greeting"),
            ("bitcoin price", "crypto_info"),
            ("what is ethereum", "crypto_general"),
            ("shiba inu", "crypto_info")
        ]
        
        # Mock market data including Shiba Inu
        mock_market_data = [
            {
                'id': 'bitcoin',
                'symbol': 'btc',
                'name': 'Bitcoin',
                'current_price': 67500.45
            },
            {
                'id': 'shiba-inu',
                'symbol': 'shib',
                'name': 'Shiba Inu',
                'current_price': 0.000024
            }
        ]
        
        print("\n🔍 Testing responses...")
        for test_input, expected_type in test_cases:
            try:
                response = chatbot.generate_response(test_input, mock_market_data)
                actual_type = response.get('type', 'unknown')
                
                print(f"\nInput: '{test_input}'")
                print(f"Expected: {expected_type}")
                print(f"Actual: {actual_type}")
                
                if test_input == "hi":
                    if actual_type == "greeting":
                        print("✅ FIXED: 'hi' now correctly returns greeting!")
                    else:
                        print("❌ ISSUE: 'hi' still not working correctly")
                else:
                    print("✅ Response generated")
                    
            except Exception as e:
                print(f"❌ Error with '{test_input}': {e}")
        
        print("\n" + "=" * 40)
        print("🎯 Test complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_ai_fixes()
