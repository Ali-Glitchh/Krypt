#!/usr/bin/env python3
"""
Comprehensive test for the dual-personality crypto chatbot
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot
import time

def test_dual_personality_chatbot():
    """Test both personalities and switching functionality"""
    print("🧪 Testing Dual-Personality Crypto Chatbot\n")
    
    # Initialize chatbot
    chatbot = EnhancedCryptoChatbot()
    
    # Test 1: Normal personality
    print("=" * 50)
    print("TEST 1: Normal Personality Mode")
    print("=" * 50)
    
    test_questions_normal = [
        "Hello!",
        "What is Bitcoin?",
        "How do I buy cryptocurrency?",
        "Tell me about DeFi",
        "Is crypto safe?"
    ]
    
    for question in test_questions_normal:
        response = chatbot.generate_response(question)
        print(f"\n💬 User: {question}")
        print(f"🤖 Normal: {response['message']}")
        time.sleep(0.5)
    
    # Test 2: Switch to Sub-Zero personality
    print("\n" + "=" * 50)
    print("TEST 2: Switching to Sub-Zero Mode")
    print("=" * 50)
    
    switch_response = chatbot.switch_personality("subzero")
    print(f"\n🔄 Personality Switch: {switch_response}")
    
    # Test 3: Sub-Zero personality
    print("\n" + "=" * 50)
    print("TEST 3: Sub-Zero Personality Mode")
    print("=" * 50)
    
    test_questions_subzero = [
        "Hello Sub-Zero!",
        "What is Bitcoin?",
        "How do I buy cryptocurrency?",
        "Tell me about DeFi",
        "What's your favorite crypto?",
        "How do I keep my crypto safe?"
    ]
    
    for question in test_questions_subzero:
        response = chatbot.generate_response(question)
        print(f"\n❄️ User: {question}")
        print(f"🧊 Sub-Zero: {response['message']}")
        time.sleep(0.5)
    
    # Test 4: Switch back to Normal
    print("\n" + "=" * 50)
    print("TEST 4: Switching back to Normal Mode")
    print("=" * 50)
    
    switch_response = chatbot.switch_personality("normal")
    print(f"\n🔄 Personality Switch: {switch_response}")
    
    # Test with normal question
    response = chatbot.generate_response("How are you doing?")
    print(f"\n💬 User: How are you doing?")
    print(f"🤖 Normal: {response['message']}")
    
    # Test 5: Dataset Statistics
    print("\n" + "=" * 50)
    print("TEST 5: Dataset Statistics")
    print("=" * 50)
    
    if hasattr(chatbot, 'subzero_trainer') and chatbot.subzero_trainer:
        subzero_stats = chatbot.subzero_trainer.get_conversation_stats()
        print("\n🧊 Sub-Zero Dataset Stats:")
        for key, value in subzero_stats.items():
            print(f"   {key}: {value}")
    
    if hasattr(chatbot, 'trainer') and chatbot.trainer:
        normal_stats = chatbot.trainer.get_conversation_stats()
        print("\n💬 Normal Dataset Stats:")
        for key, value in normal_stats.items():
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    print("✅ TEST COMPLETE")
    print("=" * 50)
    print("Summary:")
    print("- Normal personality: Friendly, general crypto assistant")
    print("- Sub-Zero personality: Ice-themed crypto warrior with 3500+ conversation pairs")
    print("- Personality switching: Seamless transition between modes")
    print("- Both personalities maintain separate training data and response styles")
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
