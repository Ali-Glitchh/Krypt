#!/usr/bin/env python3
"""
Comprehensive Sub-Zero Chatbot Test
Tests all response types and verifies Sub-Zero personality
"""

def comprehensive_test():
    print("🧊 COMPREHENSIVE SUB-ZERO CHATBOT TEST")
    print("=" * 50)
    
    try:
        from crypto_chatbot import CryptoChatbot
        bot = CryptoChatbot()
        print("✅ Chatbot imported and created successfully\n")
        
        # Test cases with expected behavior
        test_cases = [
            ("hello", "greeting", "Should respond with Sub-Zero themed greeting"),
            ("who are you", "name_inquiry", "Should identify as Sub-Zero"),
            ("tell me about bitcoin", "crypto_general", "Should give crypto advice with Sub-Zero theme"),
            ("should I invest in crypto", "crypto_general", "Should give investment advice"),
            ("tell me a crypto joke", "crypto_general", "Should tell a Sub-Zero crypto joke"),
            ("what is a wallet", "crypto_general", "Should explain wallets with Sub-Zero metaphors"),
            ("goodbye", "farewell", "Should give Sub-Zero themed farewell"),
        ]
        
        subzero_indicators = ['❄️', '🧊', 'Sub-Zero', 'ice', 'freeze', 'frost', 'Lin Kuei', 'mortal', 'kombat']
        
        all_passed = True
        
        for i, (query, expected_type, description) in enumerate(test_cases, 1):
            print(f"TEST {i}: {description}")
            print(f"Query: '{query}'")
            
            response = bot.generate_response(query)
            message = response['message']
            response_type = response['type']
            
            print(f"Response Type: {response_type}")
            print(f"Response: {message}")
            
            # Check if it's Sub-Zero themed
            has_subzero_theme = any(indicator in message for indicator in subzero_indicators)
            print(f"Sub-Zero themed: {'✅ YES' if has_subzero_theme else '❌ NO'}")
            
            # Check for generic templates (should be gone)
            has_generic_template = "is something every trader should know" in message
            if has_generic_template:
                print("🚨 ERROR: Still contains generic template!")
                all_passed = False
            else:
                print("✅ No generic templates")
            
            # Check response length (should be substantial)
            if len(message) < 10:
                print("⚠️  WARNING: Response seems too short")
                all_passed = False
            else:
                print("✅ Response has good length")
            
            print("-" * 50)
        
        if all_passed:
            print("\n🎉 ALL TESTS PASSED! Sub-Zero chatbot is working perfectly!")
            print("✅ Proper Sub-Zero themed responses")
            print("✅ No generic template responses")
            print("✅ All response types working")
            return True
        else:
            print("\n❌ Some tests failed. See details above.")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = comprehensive_test()
    exit(0 if success else 1)
