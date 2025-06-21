#!/usr/bin/env python3
"""
Test Sub-Zero Personality Integration
Tests the enhanced chatbot with Sub-Zero conversation training from human_chat.txt
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_crypto_chatbot import EnhancedCryptoChatbot

def test_subzero_integration():
    """Test the Sub-Zero personality integration"""
    print("🧊 Testing Sub-Zero Personality Integration")
    print("=" * 60)
    
    # Initialize the enhanced chatbot
    try:
        chatbot = EnhancedCryptoChatbot()
        print("✅ Enhanced chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return
    
    # Test cases to validate Sub-Zero personality
    test_cases = [
        # Basic personality switching
        ("Switch to Sub-Zero mode", "Should activate Sub-Zero personality"),
        ("Hi there!", "Should give Sub-Zero greeting"),
        ("How are you doing?", "Should respond in Sub-Zero style"),
        ("What do you think about today?", "Should use adapted conversation training"),
        ("Any plans for the weekend?", "Should respond with honor/discipline theme"),
        ("Tell me about yourself", "Should blend Sub-Zero personality with crypto knowledge"),
        ("What's the weather like?", "Should use ice/cold metaphors"),
        ("I'm feeling sad", "Should respond with stoic wisdom"),
        ("Thanks for the help", "Should give Sub-Zero farewell"),
        ("Switch to normal mode", "Should switch back to normal mode"),
        ("Hi again!", "Should give normal greeting"),
    ]
    
    print("\n🔥 Testing Personality Modes:")
    print("-" * 40)
    
    for i, (user_input, expected_behavior) in enumerate(test_cases, 1):
        print(f"\n{i}. Test: '{user_input}'")
        print(f"   Expected: {expected_behavior}")
        
        try:
            response = chatbot.generate_response(user_input)
            message = response.get('message', 'No message')
            response_type = response.get('type', 'unknown')
            
            print(f"   Response Type: {response_type}")
            print(f"   Bot: {message}")
            print(f"   Current Mode: {chatbot.personality_mode}")
            
            # Validate response contains appropriate elements
            if chatbot.personality_mode == "subzero":
                ice_indicators = ['❄️', '🧊', 'ice', 'cold', 'frost', 'honor', 'duty', 'Sub-Zero']
                has_ice_theme = any(indicator in message.lower() for indicator in ice_indicators)
                if has_ice_theme:
                    print("   ✅ Contains Sub-Zero elements")
                else:
                    print("   ⚠️ Missing Sub-Zero personality indicators")
            else:
                print("   ✅ Normal mode response")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 40)
    
    # Test crypto-specific queries in Sub-Zero mode
    print("\n❄️ Testing Sub-Zero Mode with Crypto Queries:")
    print("-" * 50)
    
    # Ensure we're in Sub-Zero mode
    chatbot.switch_personality("subzero")
    
    crypto_tests = [
        ("What's the price of Bitcoin?", "Should blend ice theme with price data"),
        ("Tell me about cryptocurrency news", "Should provide frozen intel"),
        ("Analyze the crypto market", "Should give cold analysis"),
        ("What do you think about DeFi?", "Should use Sub-Zero wisdom"),
    ]
    
    for i, (query, expected) in enumerate(crypto_tests, 1):
        print(f"\n{i}. Query: '{query}'")
        print(f"   Expected: {expected}")
        
        try:
            response = chatbot.generate_response(query)
            message = response.get('message', 'No message')
            print(f"   Sub-Zero: {message}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test Sub-Zero conversation training specifically
    print("\n🗣️ Testing Sub-Zero Conversation Training:")
    print("-" * 45)
    
    if chatbot.use_subzero_responses and chatbot.subzero_trainer:
        print("✅ Sub-Zero conversation trainer is available")
        
        # Test direct trainer responses
        conversation_tests = [
            "How's your day going?",
            "What are your hobbies?",
            "Do you like movies?",
            "Tell me about your weekend",
            "What's your favorite food?"
        ]
        
        for query in conversation_tests:
            subzero_response = chatbot.subzero_trainer.get_subzero_response(query)
            enhanced_response = chatbot.subzero_trainer.enhance_with_ice_theme(subzero_response)
            print(f"Query: {query}")
            print(f"Sub-Zero: {enhanced_response}")
            print("-" * 30)
    else:
        print("❌ Sub-Zero conversation trainer not available")
    
    print("\n🎯 Integration Test Summary:")
    print("=" * 40)
    print(f"✅ Chatbot initialized: {'Yes' if chatbot else 'No'}")
    print(f"✅ Normal conversation training: {'Yes' if chatbot.use_natural_responses else 'No'}")
    print(f"✅ Sub-Zero conversation training: {'Yes' if chatbot.use_subzero_responses else 'No'}")
    print(f"✅ Article manager: {'Yes' if chatbot.use_articles else 'No'}")
    print(f"✅ Personality switching: {'Yes' if hasattr(chatbot, 'personality_mode') else 'No'}")
    
    # Performance metrics
    if chatbot.use_subzero_responses and chatbot.subzero_trainer:
        total_pairs = len(chatbot.subzero_trainer.conversation_pairs)
        response_mappings = len(chatbot.subzero_trainer.subzero_responses)
        context_mappings = len(chatbot.subzero_trainer.conversation_contexts)
        
        print(f"📊 Sub-Zero training data:")
        print(f"   - Conversation pairs: {total_pairs}")
        print(f"   - Response mappings: {response_mappings}")
        print(f"   - Context mappings: {context_mappings}")
    
    print("\n🧊 Sub-Zero Personality Integration Test Complete! ❄️")

if __name__ == "__main__":
    test_subzero_integration()
