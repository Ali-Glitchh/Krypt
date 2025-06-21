#!/usr/bin/env python3
"""
Test script to verify Streamlit integration with improved chatbot
"""

from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot

def test_streamlit_integration():
    print("🧪 Testing Streamlit Integration with Improved Chatbot")
    print("=" * 60)
    
    # Initialize the chatbot (same as Streamlit does)
    try:
        chatbot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return
    
    # Test basic functionality
    test_queries = [
        "Hello!",
        "What is Bitcoin?",
        "switch to subzero",
        "What is your trading strategy?",
        "switch to normal",
        "Tell me about Ethereum"
    ]
    
    print(f"\n🔍 Testing chatbot responses:")
    print("-" * 40)
    
    for query in test_queries:
        print(f"\n>>> {query}")
        try:
            response = chatbot.get_response(query)
            print(f"Response: {response['message'][:100]}{'...' if len(response['message']) > 100 else ''}")
            print(f"Type: {response['type']}, Personality: {response['personality']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test personality info (used by Streamlit)
    print(f"\n📊 Testing personality info:")
    print("-" * 40)
    try:
        info = chatbot.get_personality_info()
        print(f"Current personality: {info['current_personality']}")
        print(f"Available personalities: {info['available_personalities']}")
        print(f"Features: {info['features']}")
    except Exception as e:
        print(f"❌ Error getting personality info: {e}")
    
    print(f"\n✅ Streamlit integration test completed!")
    print("🚀 Ready to run: streamlit run streamlit_app.py")

if __name__ == "__main__":
    test_streamlit_integration()
