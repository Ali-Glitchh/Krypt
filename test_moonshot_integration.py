#!/usr/bin/env python3
"""
Test MoonshotAI Integration in KoinToss AI Chatbot
Verify enhanced conversation capabilities and fallback mechanisms
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
import time
import json

def test_moonshot_integration():
    """Test MoonshotAI integration with various query types"""
    
    print("🌙 Testing MoonshotAI Integration in KoinToss AI...")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = ImprovedDualPersonalityChatbot()
    
    # Test queries designed to trigger MoonshotAI
    test_queries = [
        # Complex crypto questions
        {
            "query": "Can you explain the difference between DeFi and traditional banking?",
            "personality": "normal",
            "expected_type": "moonshot_enhanced"
        },
        
        # Sub-Zero personality complex query
        {
            "query": "What are the best strategies for dominating the crypto market?",
            "personality": "subzero", 
            "expected_type": "moonshot_enhanced"
        },
        
        # Price query (should use price analyzer, not MoonshotAI)
        {
            "query": "What is the current Bitcoin price?",
            "personality": "normal",
            "expected_type": "price_analysis_with_news"
        },
        
        # Simple query (should use local trainers)
        {
            "query": "Hello",
            "personality": "normal",
            "expected_type": "normal_response"
        },
        
        # Conversational query
        {
            "query": "What do you think about the future of cryptocurrency adoption?",
            "personality": "normal",
            "expected_type": "moonshot_enhanced"
        },
        
        # Technical analysis
        {
            "query": "How does blockchain consensus mechanisms work in proof of stake?",
            "personality": "subzero",
            "expected_type": "moonshot_enhanced"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: {test_case['query'][:50]}...")
        print(f"Personality: {test_case['personality']}")
        print(f"Expected Response Type: {test_case['expected_type']}")
        print("-" * 40)
        
        # Set personality
        if test_case['personality'] != chatbot.personality_mode:
            chatbot.switch_personality(test_case['personality'])
        
        # Get response
        start_time = time.time()
        response = chatbot.get_response(test_case['query'])
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Analyze response
        response_type = response.get('type', 'unknown')
        message = response.get('message', '')
        personality = response.get('personality', 'unknown')
        confidence = response.get('confidence', 0.0)
        
        print(f"✅ Response received!")
        print(f"   Type: {response_type}")
        print(f"   Personality: {personality}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Response Time: {response_time:.2f}s")
        print(f"   Message Length: {len(message)} chars")
        
        # Show first part of message
        preview = message[:150] + "..." if len(message) > 150 else message
        print(f"   Preview: {preview}")
        
        # Check if it matches expected type
        matches_expected = response_type == test_case['expected_type']
        print(f"   Matches Expected: {'✅' if matches_expected else '❌'}")
        
        # Special checks for MoonshotAI responses
        if response_type == "moonshot_enhanced":
            model_used = response.get('model_used', 'N/A')
            tokens_used = response.get('tokens_used', 0)
            enhanced_with_context = response.get('enhanced_with_context', False)
            
            print(f"   🌙 MoonshotAI Details:")
            print(f"      Model: {model_used}")
            print(f"      Tokens: {tokens_used}")
            print(f"      Enhanced with Context: {enhanced_with_context}")
        
        results.append({
            'test_case': test_case,
            'response': response,
            'response_time': response_time,
            'matches_expected': matches_expected
        })
        
        # Rate limiting
        time.sleep(1)
    
    # Summary
    print(f"\n{'='*60}")
    print("🎯 INTEGRATION TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    moonshot_responses = sum(1 for r in results if r['response'].get('type') == 'moonshot_enhanced')
    expected_matches = sum(1 for r in results if r['matches_expected'])
    avg_response_time = sum(r['response_time'] for r in results) / total_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"MoonshotAI Responses: {moonshot_responses}")
    print(f"Expected Type Matches: {expected_matches}/{total_tests}")
    print(f"Average Response Time: {avg_response_time:.2f}s")
    print(f"Success Rate: {(expected_matches/total_tests)*100:.1f}%")
    
    # Check MoonshotAI availability
    moonshot_available = chatbot.moonshot_ai is not None
    print(f"MoonshotAI Available: {'✅' if moonshot_available else '❌'}")
    
    if moonshot_available:
        stats = chatbot.moonshot_ai.get_conversation_stats()
        print(f"MoonshotAI Stats: {stats}")
    
    # Show learning stats
    learning_stats = chatbot.learning_stats
    print(f"Chatbot Learning Stats: {learning_stats}")
    
    return results

if __name__ == "__main__":
    print("🚀 Starting MoonshotAI Integration Test for KoinToss AI...")
    
    try:
        results = test_moonshot_integration()
        
        print(f"\n🎉 Integration test completed!")
        print("The KoinToss AI chatbot now has enhanced MoonshotAI capabilities!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
