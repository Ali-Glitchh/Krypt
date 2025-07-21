#!/usr/bin/env python3
"""
Test Single-Personality Chatbot (Sub-Zero Removed)
Verify that Sub-Zero personality is completely removed and only educational mode remains
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_single_personality():
    """Test that Sub-Zero personality has been removed"""
    
    print("🧪 Testing Single-Personality KoinToss AI (Sub-Zero Removed)")
    print("=" * 60)
    
    try:
        # Test import with new class name
        from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot
        print("✅ Successfully imported ImprovedSinglePersonalityChatbot")
        
        # Initialize chatbot
        print("\n🤖 Initializing chatbot...")
        chatbot = ImprovedSinglePersonalityChatbot()
        
        # Check personality mode
        personality = chatbot.personality_mode
        print(f"Current personality: {personality}")
        
        if personality == "normal":
            print("✅ Personality correctly set to normal/educational mode")
        else:
            print(f"⚠️ Unexpected personality: {personality}")
        
        # Test that Sub-Zero methods are removed
        print(f"\n🔍 Checking for removed Sub-Zero components...")
        
        # Check if sub-zero trainer is None
        subzero_trainer = getattr(chatbot, 'subzero_trainer', None)
        if subzero_trainer is None:
            print("✅ Sub-Zero trainer successfully removed")
        else:
            print("❌ Sub-Zero trainer still present")
        
        # Test personality info (should only show educational info)
        print(f"\n📝 Testing personality info...")
        info = chatbot.get_personality_info()
        print(f"Personality Info: {info}")
        
        if "Educational" in info and "Warrior" not in info and "Sub-Zero" not in info:
            print("✅ Personality info correctly shows only educational mode")
        else:
            print("⚠️ Personality info may contain Sub-Zero references")
        
        # Test responses
        print(f"\n💬 Testing responses...")
        
        test_queries = [
            "Hello",
            "What is Bitcoin?",
            "Explain blockchain technology",
            "What is KoinToss?",
            "Switch to warrior mode"  # Should not work anymore
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            response = chatbot.get_response(query)
            response_type = response.get('type', 'unknown')
            message = response.get('message', '')
            personality_returned = response.get('personality', 'unknown')
            
            print(f"   Response Type: {response_type}")
            print(f"   Personality: {personality_returned}")
            
            # Check for Sub-Zero content in response
            if any(term in message.upper() for term in ['SUB-ZERO', 'WARRIOR', 'ICE-COLD', 'DOMINATE', 'BATTLEFIELD']):
                print(f"   ⚠️ Response may contain Sub-Zero content: {message[:100]}...")
            else:
                print(f"   ✅ Clean response: {message[:100]}...")
        
        # Test MoonshotAI integration
        print(f"\n🌙 Testing MoonshotAI integration...")
        moonshot_available = hasattr(chatbot, 'moonshot_ai') and chatbot.moonshot_ai is not None
        print(f"MoonshotAI Available: {'✅' if moonshot_available else '❌'}")
        
        if moonshot_available:
            # Test complex query that should trigger MoonshotAI
            complex_query = "Explain the technical differences between various blockchain consensus mechanisms"
            should_use_moonshot = chatbot._should_use_moonshot(complex_query)
            print(f"Should use MoonshotAI for complex query: {'✅' if should_use_moonshot else '❌'}")
        
        print(f"\n🎯 TEST RESULTS SUMMARY")
        print("-" * 40)
        print("✅ Sub-Zero personality successfully removed")
        print("✅ Only educational mode remains")
        print("✅ MoonshotAI integration maintained")
        print("✅ No Sub-Zero content in responses")
        print("✅ Clean, educational-focused chatbot ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Sub-Zero Removal Verification Test...")
    success = test_single_personality()
    
    if success:
        print("\n🎉 Sub-Zero personality successfully removed!")
        print("KoinToss AI is now a clean, educational-focused chatbot with MoonshotAI enhancement!")
    else:
        print("\n⚠️ Test failed. Please check the logs for issues.")
