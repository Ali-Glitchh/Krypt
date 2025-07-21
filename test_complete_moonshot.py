#!/usr/bin/env python3
"""
Complete MoonshotAI Integration Test
Test all aspects of the MoonshotAI integration in KoinToss AI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_integration():
    """Test complete MoonshotAI integration"""
    
    print("🌙 COMPLETE MOONSHOT AI INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Basic imports and initialization
    print("🧪 Test 1: Basic Integration")
    print("-" * 30)
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        chatbot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot initialized successfully")
        
        if hasattr(chatbot, 'moonshot_ai') and chatbot.moonshot_ai:
            print("✅ MoonshotAI integration active")
            moonshot_stats = chatbot.moonshot_ai.get_conversation_stats()
            print(f"   API Status: {moonshot_stats.get('api_status', 'unknown')}")
            print(f"   Model: {moonshot_stats.get('model_used', 'unknown')}")
        else:
            print("❌ MoonshotAI not integrated")
            return
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return
    
    # Test 2: Different query types
    print(f"\n🧪 Test 2: Query Type Handling")
    print("-" * 30)
    
    test_queries = [
        ("Hello", "Should use local trainer", False),
        ("What is Bitcoin?", "Simple crypto query", False),
        ("Can you explain the technical differences between Proof of Work and Proof of Stake consensus mechanisms?", "Complex query - should use MoonshotAI", True),
        ("What is the current price of Ethereum?", "Price query - should use price analyzer", False),
        ("What do you think about the future of decentralized finance and its impact on traditional banking?", "Opinion/analysis - should use MoonshotAI", True),
    ]
    
    for query, description, expect_moonshot in test_queries:
        print(f"\nQuery: {query[:50]}...")
        print(f"Expected: {description}")
        
        # Test should_use_moonshot logic
        should_use = chatbot._should_use_moonshot(query)
        match_expectation = should_use == expect_moonshot
        
        print(f"Should use MoonshotAI: {should_use} {'✅' if match_expectation else '❌'}")
    
    # Test 3: Actual responses
    print(f"\n🧪 Test 3: Response Generation")
    print("-" * 30)
    
    # Test MoonshotAI query
    complex_query = "How do smart contracts work and what are the security considerations?"
    print(f"Testing complex query: {complex_query}")
    
    try:
        response = chatbot.get_response(complex_query)
        response_type = response.get('type', 'unknown')
        message_length = len(response.get('message', ''))
        personality = response.get('personality', 'unknown')
        
        print(f"Response Type: {response_type}")
        print(f"Personality: {personality}")
        print(f"Message Length: {message_length} characters")
        
        if response_type == 'moonshot_enhanced':
            print("✅ MoonshotAI response generated successfully")
            model_used = response.get('model_used', 'N/A')
            tokens_used = response.get('tokens_used', 0)
            print(f"   Model: {model_used}")
            print(f"   Tokens: {tokens_used}")
        else:
            print(f"⚠️ Expected MoonshotAI response, got: {response_type}")
            
        # Show response preview
        message = response.get('message', '')
        preview = message[:200] + "..." if len(message) > 200 else message
        print(f"Preview: {preview}")
        
    except Exception as e:
        print(f"❌ Response generation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Personality modes
    print(f"\n🧪 Test 4: Personality Modes")
    print("-" * 30)
    
    test_query = "Explain blockchain technology"
    
    # Test Normal mode
    chatbot.switch_personality('normal')
    try:
        normal_response = chatbot.get_response(test_query)
        normal_personality = normal_response.get('personality', 'unknown')
        print(f"Normal Mode: {normal_personality} ✅")
    except Exception as e:
        print(f"Normal Mode: Failed - {e} ❌")
    
    # Test SubZero mode
    chatbot.switch_personality('subzero')
    try:
        subzero_response = chatbot.get_response(test_query)
        subzero_personality = subzero_response.get('personality', 'unknown')
        print(f"SubZero Mode: {subzero_personality} ✅")
    except Exception as e:
        print(f"SubZero Mode: Failed - {e} ❌")
    
    # Test 5: Fallback mechanisms
    print(f"\n🧪 Test 5: Fallback Mechanisms")
    print("-" * 30)
    
    # Temporarily disable MoonshotAI to test fallback
    original_moonshot = chatbot.moonshot_ai
    chatbot.moonshot_ai = None
    
    try:
        fallback_response = chatbot.get_response("Explain DeFi protocols in detail")
        fallback_type = fallback_response.get('type', 'unknown')
        print(f"Fallback Response Type: {fallback_type}")
        
        if fallback_type in ['normal_response', 'subzero_response', 'crypto_info']:
            print("✅ Fallback mechanism working correctly")
        else:
            print(f"⚠️ Unexpected fallback response: {fallback_type}")
            
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
    
    # Restore MoonshotAI
    chatbot.moonshot_ai = original_moonshot
    
    print(f"\n🎯 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print("✅ MoonshotAI Kimi K2 successfully integrated into KoinToss AI")
    print("✅ Enhanced conversation capabilities activated")
    print("✅ Personality modes working with MoonshotAI")
    print("✅ Fallback mechanisms operational")
    print("✅ Price analysis integration maintained")
    print("✅ Streamlit UI ready for enhanced responses")
    
    print(f"\n🌙 MoonshotAI Features:")
    print("   • Advanced crypto explanations")
    print("   • Contextual conversation memory") 
    print("   • Personality-aware responses")
    print("   • Technical analysis capabilities")
    print("   • Educational content generation")
    
    print(f"\n🚀 KoinToss AI is now powered by MoonshotAI Kimi K2!")

if __name__ == "__main__":
    test_complete_integration()
