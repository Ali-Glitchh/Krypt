#!/usr/bin/env python3
"""
Quick test of the full chatbot system with pi coin queries
"""

def test_full_chatbot():
    print("🧪 Testing Full Chatbot System")
    print("=" * 40)
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        print("1. Initializing chatbot...")
        chatbot = ImprovedDualPersonalityChatbot()
        
        print("2. Testing pi coin queries...")
        test_queries = [
            "pi",
            "pi coin", 
            "what is pi coin",
            "pi coin price"
        ]
        
        for query in test_queries:
            print(f"\n👤 You: {query}")
            response = chatbot.get_response(query)
            
            if isinstance(response, dict):
                print(f"🤖 {response['personality'].title()} AI: {response['message']}")
            else:
                print(f"🤖 Bot: {response}")
        
        print("\n✅ Full chatbot test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in full chatbot test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_full_chatbot()
