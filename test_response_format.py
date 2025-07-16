#!/usr/bin/env python3
"""
Quick test to check response format
"""

def test_response_format():
    print("Testing response format...")
    
    try:
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        bot = ImprovedDualPersonalityChatbot()
        response = bot.get_response("What is Bitcoin?")
        
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")
        
        if isinstance(response, dict):
            print("Response is dict format")
            if 'message' in response:
                print(f"Message: {response['message'][:100]}...")
            if 'response' in response:
                print(f"Response: {response['response'][:100]}...")
        else:
            print(f"Response is string format: {response[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_response_format()
