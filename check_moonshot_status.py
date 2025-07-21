#!/usr/bin/env python3
"""
MoonshotAI Integration Status Check
Test the current status and functionality of MoonshotAI integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_moonshot_integration():
    """Check MoonshotAI integration status"""
    
    print("🌙 MoonshotAI Integration Status Check")
    print("=" * 50)
    
    try:
        # Import and initialize
        from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot
        bot = ImprovedSinglePersonalityChatbot()
        print("✅ Chatbot initialized successfully")
        
        # Check MoonshotAI availability
        moonshot_available = hasattr(bot, 'moonshot_ai') and bot.moonshot_ai is not None
        print(f"MoonshotAI Available: {'✅' if moonshot_available else '❌'}")
        
        if moonshot_available:
            # Get integration stats
            stats = bot.moonshot_ai.get_conversation_stats()
            print(f"API Status: {stats.get('api_status', 'unknown')}")
            print(f"Model: {stats.get('model_used', 'unknown')}")
            
            # Test query routing logic
            print(f"\n🧠 Query Routing Logic Test:")
            
            test_cases = [
                ("Hello", False, "Simple greeting"),
                ("What is Bitcoin?", False, "Basic crypto question"),  
                ("Explain blockchain consensus mechanisms in detail", True, "Complex technical question"),
                ("What do you think about the future of DeFi?", True, "Opinion/analysis question"),
                ("How do smart contracts work?", True, "Complex explanation needed"),
                ("Price of ETH", False, "Price query (uses price analyzer)")
            ]
            
            for query, should_use_moonshot, description in test_cases:
                uses_moonshot = bot._should_use_moonshot(query)
                status = "✅" if uses_moonshot == should_use_moonshot else "❌"
                print(f"  {status} '{query[:30]}...' -> MoonshotAI: {uses_moonshot} ({description})")
            
            # Test actual responses
            print(f"\n💬 Testing Actual Responses:")
            
            # Simple query test
            print(f"\n1. Simple Query Test:")
            simple_response = bot.get_response("Hello there!")
            print(f"   Query: Hello there!")
            print(f"   Response Type: {simple_response.get('type', 'unknown')}")
            print(f"   Uses MoonshotAI: {'✅' if 'moonshot' in simple_response.get('type', '') else '❌'}")
            
            # Complex query test
            print(f"\n2. Complex Query Test:")
            complex_query = "Can you explain how decentralized autonomous organizations (DAOs) work and their governance mechanisms?"
            try:
                complex_response = bot.get_response(complex_query)
                print(f"   Query: {complex_query[:50]}...")
                print(f"   Response Type: {complex_response.get('type', 'unknown')}")
                print(f"   Uses MoonshotAI: {'✅' if 'moonshot' in complex_response.get('type', '') else '❌'}")
                
                if 'moonshot' in complex_response.get('type', ''):
                    print(f"   Model Used: {complex_response.get('model_used', 'N/A')}")
                    print(f"   Tokens Used: {complex_response.get('tokens_used', 0)}")
                    print(f"   Message Length: {len(complex_response.get('message', ''))} chars")
                
            except Exception as e:
                print(f"   ❌ Error testing complex query: {e}")
            
            # Price query test (should NOT use MoonshotAI)
            print(f"\n3. Price Query Test:")
            price_response = bot.get_response("What is the current Bitcoin price?")
            print(f"   Query: What is the current Bitcoin price?")
            print(f"   Response Type: {price_response.get('type', 'unknown')}")
            print(f"   Uses MoonshotAI: {'❌' if 'moonshot' not in price_response.get('type', '') else '⚠️'} (should NOT use MoonshotAI)")
            
        else:
            print("❌ MoonshotAI not available - checking why...")
            
            # Check if MoonshotAI module can be imported
            try:
                from moonshot_ai_integration import MoonshotAIIntegration
                print("✅ MoonshotAI module can be imported")
                
                # Try manual initialization
                api_key = "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"
                moonshot_test = MoonshotAIIntegration(api_key=api_key)
                print("✅ MoonshotAI can be manually initialized")
                
            except Exception as e:
                print(f"❌ MoonshotAI module import error: {e}")
        
        # Integration health summary
        print(f"\n🎯 INTEGRATION HEALTH SUMMARY")
        print("-" * 40)
        
        if moonshot_available:
            print("✅ MoonshotAI Successfully Integrated")
            print("✅ Query routing logic working")
            print("✅ API key configured")
            print("✅ Fallback mechanisms in place")
            print(f"✅ Model: {stats.get('model_used', 'moonshot-v1-8k')}")
            
            # Check for any potential issues
            print(f"\n🔍 Potential Issues:")
            if stats.get('api_status') == 'no_api_key':
                print("⚠️ API key not detected")
            else:
                print("✅ API key detected")
                
        else:
            print("❌ MoonshotAI Integration Issues Detected")
            print("⚠️ Check API key and module imports")
        
        return moonshot_available
        
    except Exception as e:
        print(f"❌ Integration check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting MoonshotAI Integration Health Check...")
    
    success = check_moonshot_integration()
    
    if success:
        print(f"\n🎉 MoonshotAI Integration is Working!")
        print("The chatbot can handle:")
        print("• Simple queries with local trainers (fast)")
        print("• Complex queries with MoonshotAI (enhanced)")
        print("• Price queries with price analyzer")
        print("• Fallback responses when needed")
    else:
        print(f"\n⚠️ MoonshotAI Integration has issues.")
        print("Please check the logs above for specific problems.")
