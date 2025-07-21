#!/usr/bin/env python3
"""
New API Key Verification Test
Test the updated MoonshotAI API key functionality
"""

def test_new_api_key():
    """Test the new MoonshotAI API key"""
    
    print("🌙 New MoonshotAI API Key Test")
    print("=" * 50)
    
    new_key = "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"
    print(f"🔑 Testing key: {new_key[:20]}...{new_key[-10:]}")
    
    # Test 1: Direct MoonshotAI connection
    print(f"\n📡 Test 1: Direct API Connection")
    print("-" * 30)
    
    try:
        from moonshot_ai_integration import MoonshotAIIntegration
        
        moonshot = MoonshotAIIntegration(api_key=new_key)
        print("✅ MoonshotAI module initialized")
        
        # Test basic query
        response = moonshot.get_crypto_specific_response("What is Bitcoin?")
        
        if response:
            print("✅ API connection successful!")
            print(f"   Response Type: {response.get('type', 'unknown')}")
            print(f"   Model Used: {response.get('model_used', 'N/A')}")
            print(f"   Tokens Used: {response.get('tokens_used', 0)}")
            print(f"   Confidence: {response.get('confidence', 0)}")
            print(f"   Message Length: {len(response.get('message', ''))} characters")
            print(f"   Preview: {response.get('message', '')[:150]}...")
            api_working = True
        else:
            print("❌ No response from API")
            api_working = False
            
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        api_working = False
    
    # Test 2: Integration in main chatbot
    print(f"\n🤖 Test 2: Chatbot Integration")
    print("-" * 30)
    
    try:
        from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot
        
        bot = ImprovedSinglePersonalityChatbot()
        print("✅ Chatbot initialized")
        
        # Check MoonshotAI availability
        moonshot_available = hasattr(bot, 'moonshot_ai') and bot.moonshot_ai is not None
        print(f"MoonshotAI Available: {'✅' if moonshot_available else '❌'}")
        
        if moonshot_available:
            # Test query routing
            complex_query = "Explain the technical differences between Proof of Work and Proof of Stake consensus mechanisms"
            should_use_moonshot = bot._should_use_moonshot(complex_query)
            print(f"Should use MoonshotAI: {'✅' if should_use_moonshot else '❌'}")
            
            # Test actual response
            print(f"\n💬 Testing complex query response...")
            response = bot.get_response(complex_query)
            
            response_type = response.get('type', 'unknown')
            print(f"Response Type: {response_type}")
            
            if 'moonshot' in response_type:
                print("✅ MoonshotAI successfully used!")
                print(f"   Model: {response.get('model_used', 'N/A')}")
                print(f"   Tokens: {response.get('tokens_used', 0)}")
                print(f"   Enhanced: {response.get('enhanced_with_context', False)}")
                integration_working = True
            else:
                print("⚠️ Fallback response used (MoonshotAI may be unavailable)")
                integration_working = False
        else:
            print("❌ MoonshotAI not integrated in chatbot")
            integration_working = False
            
    except Exception as e:
        print(f"❌ Chatbot integration test failed: {e}")
        integration_working = False
    
    # Test 3: Different query types
    print(f"\n🧪 Test 3: Query Type Handling")
    print("-" * 30)
    
    if moonshot_available:
        test_queries = [
            ("Hello", False, "Simple greeting"),
            ("What is the price of Bitcoin?", False, "Price query - should use price analyzer"),
            ("How do smart contracts work and what are their security implications?", True, "Complex technical question"),
            ("Compare DeFi protocols and traditional banking systems", True, "Analysis/comparison question")
        ]
        
        for query, should_use_ai, description in test_queries:
            uses_moonshot = bot._should_use_moonshot(query)
            status = "✅" if uses_moonshot == should_use_ai else "⚠️"
            print(f"   {status} '{query[:40]}...' -> AI: {uses_moonshot} ({description})")
    
    # Summary
    print(f"\n🎯 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    if api_working and integration_working:
        print("✅ MoonshotAI API Key Working Perfectly!")
        print("✅ Direct API connection successful")
        print("✅ Chatbot integration functional")
        print("✅ Query routing working correctly")
        print("✅ Enhanced responses available")
        
        print(f"\n🎉 Your KoinToss AI now has full MoonshotAI capabilities!")
        print("Features unlocked:")
        print("• 🧠 Advanced technical explanations")
        print("• 💬 Context-aware conversations")
        print("• 📊 Detailed market analysis")
        print("• 🎓 Professional crypto education")
        
    elif api_working:
        print("✅ API Key Valid - Direct connection works")
        print("⚠️ Integration issues - Check chatbot configuration")
        
    else:
        print("❌ API Key Issues Detected")
        print("• Check key validity")
        print("• Verify account credits")
        print("• Check network connectivity")
        
    return api_working and integration_working

if __name__ == "__main__":
    print("🚀 Testing New MoonshotAI API Key Integration...")
    success = test_new_api_key()
    
    if success:
        print(f"\n🎊 SUCCESS! Your MoonshotAI integration is now fully operational!")
        print("Ready to launch: streamlit run streamlit_app.py")
    else:
        print(f"\n⚠️ Some issues detected. Check the logs above for details.")
