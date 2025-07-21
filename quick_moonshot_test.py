#!/usr/bin/env python3
"""
Quick MoonshotAI Integration Test
Simple test to verify the integration is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_integration():
    """Test basic MoonshotAI integration"""
    
    print("🧪 Quick MoonshotAI Integration Test...")
    
    # Test import
    try:
        from moonshot_ai_integration import MoonshotAIIntegration
        print("✅ MoonshotAI module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import MoonshotAI module: {e}")
        return False
    
    # Test initialization
    try:
        api_key = "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"
        moonshot = MoonshotAIIntegration(api_key=api_key)
        print("✅ MoonshotAI initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize MoonshotAI: {e}")
        return False
    
    # Test chatbot import
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("✅ Chatbot module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import chatbot module: {e}")
        return False
    
    # Test chatbot initialization
    try:
        chatbot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot initialized successfully")
        
        # Check if MoonshotAI is available in chatbot
        if hasattr(chatbot, 'moonshot_ai') and chatbot.moonshot_ai:
            print("✅ MoonshotAI integrated into chatbot")
        else:
            print("❌ MoonshotAI not available in chatbot")
            
        # Test simple query
        print("\n🧪 Testing simple query...")
        response = chatbot.get_response("Hello")
        print(f"Response type: {response.get('type', 'unknown')}")
        print(f"Message preview: {response.get('message', '')[:100]}...")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("🎉 Basic integration test completed!")
    return True

if __name__ == "__main__":
    test_basic_integration()
