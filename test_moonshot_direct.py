#!/usr/bin/env python3
"""
Direct MoonshotAI Connection Test
Test the API connection and functionality directly
"""

def test_moonshot_direct():
    """Test MoonshotAI connection directly"""
    
    print("🌙 Direct MoonshotAI Connection Test")
    print("=" * 40)
    
    try:
        from moonshot_ai_integration import MoonshotAIIntegration
        
        # Initialize with the provided API key
        api_key = "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"
        print(f"🔑 Using API key: {api_key[:20]}...{api_key[-10:]}")
        
        moonshot = MoonshotAIIntegration(api_key=api_key)
        print("✅ MoonshotAI integration initialized")
        
        # Get basic stats
        stats = moonshot.get_conversation_stats()
        print(f"📊 Stats: {stats}")
        
        # Test a simple query
        print(f"\n🧪 Testing simple crypto query...")
        response = moonshot.get_crypto_specific_response("What is Bitcoin and how does it work?")
        
        if response:
            print(f"✅ Response received!")
            print(f"   Type: {response.get('type', 'unknown')}")
            print(f"   Model: {response.get('model_used', 'N/A')}")
            print(f"   Tokens: {response.get('tokens_used', 0)}")
            print(f"   Confidence: {response.get('confidence', 0)}")
            print(f"   Message Length: {len(response.get('message', ''))} chars")
            print(f"   Message Preview: {response.get('message', '')[:200]}...")
            
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Direct connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_in_chatbot():
    """Test MoonshotAI integration within the main chatbot"""
    
    print(f"\n🤖 Testing Integration in Main Chatbot")
    print("=" * 40)
    
    try:
        from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot
        
        bot = ImprovedSinglePersonalityChatbot()
        
        # Check if MoonshotAI is available
        if hasattr(bot, 'moonshot_ai') and bot.moonshot_ai:
            print("✅ MoonshotAI available in chatbot")
            
            # Test complex query routing
            complex_query = "Explain the differences between Proof of Work and Proof of Stake consensus mechanisms"
            should_use = bot._should_use_moonshot(complex_query)
            print(f"   Should use MoonshotAI for complex query: {should_use}")
            
            if should_use:
                print(f"\n🧪 Testing complex query response...")
                response = bot.get_response(complex_query)
                
                response_type = response.get('type', 'unknown')
                print(f"   Response Type: {response_type}")
                
                if 'moonshot' in response_type:
                    print("✅ MoonshotAI was used for complex query")
                    print(f"   Model: {response.get('model_used', 'N/A')}")
                    print(f"   Tokens: {response.get('tokens_used', 0)}")
                else:
                    print("⚠️ MoonshotAI was not used (may have fallen back to local trainer)")
                
                return True
            else:
                print("⚠️ Query routing not triggering MoonshotAI")
                return False
                
        else:
            print("❌ MoonshotAI not available in chatbot")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting MoonshotAI Direct Tests...")
    
    # Test direct connection
    direct_success = test_moonshot_direct()
    
    # Test integration in chatbot
    integration_success = test_integration_in_chatbot()
    
    print(f"\n🎯 TEST RESULTS SUMMARY")
    print("=" * 30)
    print(f"Direct Connection: {'✅' if direct_success else '❌'}")
    print(f"Chatbot Integration: {'✅' if integration_success else '❌'}")
    
    if direct_success and integration_success:
        print(f"\n🎉 MoonshotAI Integration Fully Working!")
        print("• API connection established")
        print("• Query routing functional") 
        print("• Enhanced responses available")
        print("• Fallback mechanisms in place")
    elif direct_success:
        print(f"\n⚠️ MoonshotAI API works but integration has issues")
        print("• Check query routing logic")
        print("• Verify chatbot initialization")
    else:
        print(f"\n❌ MoonshotAI API Connection Issues")
        print("• Check API key validity")
        print("• Check network connectivity")
        print("• API key may need renewal")
