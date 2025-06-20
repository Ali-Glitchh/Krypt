#!/usr/bin/env python3
"""
Comprehensive Test Suite for Improved Dual-Personality Crypto Chatbot
"""

import json
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot

def test_normal_personality():
    """Test normal personality responses"""
    print("🔥 TESTING NORMAL PERSONALITY")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    
    test_cases = [
        "Hello, how are you?",
        "What do you think about Bitcoin?",
        "Can you explain Ethereum to me?",
        "What should I invest in?",
        "How does blockchain work?",
        "Tell me about DeFi",
        "What's the latest crypto news?",
        "Is now a good time to buy crypto?"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{i}. Question: {question}")
        response = bot.get_response(question)
        print(f"   Answer: {response['message'][:200]}{'...' if len(response['message']) > 200 else ''}")
        print(f"   Type: {response['type']}")
        print(f"   Personality: {response['personality']}")

def test_subzero_personality():
    """Test Sub-Zero personality responses"""
    print("\n\n❄️ TESTING SUB-ZERO PERSONALITY")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    bot.switch_personality('subzero')
    
    test_cases = [
        "Hello Sub-Zero",
        "What do you think about Bitcoin?",
        "Tell me about Ethereum",
        "Should I buy crypto now?",
        "What's your trading strategy?",
        "How do you analyze the market?",
        "What's the latest crypto news?",
        "Who are you?"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{i}. Question: {question}")
        response = bot.get_response(question)
        print(f"   Answer: {response['message'][:200]}{'...' if len(response['message']) > 200 else ''}")
        print(f"   Type: {response['type']}")
        print(f"   Personality: {response['personality']}")

def test_personality_switching():
    """Test personality switching functionality"""
    print("\n\n🔄 TESTING PERSONALITY SWITCHING")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    
    # Test switching commands
    switch_tests = [
        "switch to subzero",
        "What do you think about Bitcoin?",
        "switch to normal", 
        "What do you think about Bitcoin?",
        "activate subzero",
        "Tell me about yourself"
    ]
    
    for i, command in enumerate(switch_tests, 1):
        print(f"\n{i}. Command: {command}")
        response = bot.get_response(command)
        print(f"   Response: {response['message'][:150]}{'...' if len(response['message']) > 150 else ''}")
        print(f"   Current Personality: {response['personality']}")
        print(f"   Type: {response['type']}")

def test_news_integration():
    """Test news insights integration"""
    print("\n\n📰 TESTING NEWS INTEGRATION")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    
    news_queries = [
        "What's the latest Bitcoin news?",
        "Give me crypto market updates",
        "What's happening with Ethereum today?",
        "Show me recent crypto trends"
    ]
    
    for i, query in enumerate(news_queries, 1):
        print(f"\n{i}. Query: {query}")
        response = bot.get_response(query)
        print(f"   Response: {response['message'][:200]}{'...' if len(response['message']) > 200 else ''}")
        print(f"   Type: {response['type']}")
    
    # Test Sub-Zero news style
    print(f"\n--- Testing Sub-Zero News Style ---")
    bot.switch_personality('subzero')
    response = bot.get_response("What's the latest crypto news?")
    print(f"Sub-Zero News: {response['message'][:200]}{'...' if len(response['message']) > 200 else ''}")

def test_response_quality():
    """Test response quality and relevance"""
    print("\n\n🎯 TESTING RESPONSE QUALITY")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    
    quality_tests = [
        {
            "input": "Explain Bitcoin in simple terms",
            "expected_keywords": ["bitcoin", "cryptocurrency", "digital", "decentralized"],
            "personality": "normal"
        },
        {
            "input": "What's your trading philosophy?",
            "expected_keywords": ["freeze", "ice", "mortal", "sub-zero", "combat"],
            "personality": "subzero"
        }
    ]
    
    for test in quality_tests:
        bot.switch_personality(test["personality"])
        print(f"\nTesting {test['personality']} personality:")
        print(f"Input: {test['input']}")
        
        response = bot.get_response(test["input"])
        response_text = response['message'].lower()
        
        print(f"Response: {response['message'][:200]}{'...' if len(response['message']) > 200 else ''}")
        
        # Check for expected keywords
        found_keywords = [kw for kw in test["expected_keywords"] if kw in response_text]
        print(f"Found keywords: {found_keywords}")
        print(f"Quality score: {len(found_keywords)}/{len(test['expected_keywords'])}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n\n⚠️ TESTING EDGE CASES")
    print("=" * 50)
    
    bot = ImprovedDualPersonalityChatbot()
    
    edge_cases = [
        "",  # Empty input
        "   ",  # Whitespace only
        "asdfghjklqwertyuiop",  # Random text
        "What is the meaning of life, universe, and everything?",  # Non-crypto question
        "Tell me a joke",  # Entertainment request
        "How do I cook pasta?"  # Completely unrelated
    ]
    
    for i, test_input in enumerate(edge_cases, 1):
        print(f"\n{i}. Input: '{test_input}'")
        response = bot.get_response(test_input)
        print(f"   Response: {response['message'][:150]}{'...' if len(response['message']) > 150 else ''}")
        print(f"   Type: {response['type']}")
        print(f"   Handled gracefully: {'✅' if response['message'] else '❌'}")

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE TEST SUITE FOR IMPROVED DUAL-PERSONALITY CHATBOT")
    print("🎯 Verifying dataset-driven responses, personality accuracy, and functionality")
    print("=" * 80)
    
    try:
        test_normal_personality()
        test_subzero_personality()
        test_personality_switching()
        test_news_integration()
        test_response_quality()
        test_edge_cases()
        
        print("\n\n✅ ALL TESTS COMPLETED!")
        print("📊 Check the results above to verify:")
        print("  - Normal personality gives relevant, helpful responses")
        print("  - Sub-Zero personality maintains authentic character")
        print("  - Personality switching works correctly")
        print("  - News integration functions properly")
        print("  - Edge cases are handled gracefully")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
