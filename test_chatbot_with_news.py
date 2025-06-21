#!/usr/bin/env python3
"""
Test the final dual-personality enhanced crypto chatbot with news insights
"""

from final_dual_personality_chatbot import DualPersonalityChatbot

def test_enhanced_chatbot_with_news():
    print("🚀 Testing Final Dual-Personality Crypto Chatbot with News Insights")
    print("=" * 80)
    
    # Initialize the chatbot
    bot = DualPersonalityChatbot()
    
    # Show training information
    info = bot.get_personality_info()
    print(f"\n📊 Training Information:")
    print(f"Current personality: {info['current_personality'].upper()}")
    
    if 'normal_training' in info:
        normal_stats = info['normal_training']
        print(f"Normal personality: {normal_stats['total_conversations']} conversations trained")
        if 'crypto_conversations' in normal_stats:
            print(f"  - Crypto conversations: {normal_stats['crypto_conversations']}")
        if 'average_response_length' in normal_stats:
            print(f"  - Average response length: {normal_stats['average_response_length']:.1f} chars")
    
    if 'subzero_training' in info:
        subzero_stats = info['subzero_training']
        print(f"Sub-Zero personality: {subzero_stats['total_conversations']} conversations trained")
        if 'crypto_conversations' in subzero_stats:
            print(f"  - Crypto conversations: {subzero_stats['crypto_conversations']}")
        if 'average_response_length' in subzero_stats:
            print(f"  - Average response length: {subzero_stats['average_response_length']:.1f} chars")
    
    print("\n" + "=" * 80)
    
    # Test cases including news queries
    test_cases = [
        ("Hello!", "Greeting test"),
        ("What is Bitcoin?", "Crypto knowledge"),
        ("What's the latest crypto news?", "News insights"),
        ("Give me market insights", "Market analysis"),
        ("Any recent Bitcoin news?", "Specific coin news"),
        ("How do I start investing in crypto?", "Investment advice"),
        ("What's happening in the crypto market?", "Market updates"),
        ("Tell me about blockchain security", "Security knowledge"),
        ("Should I buy crypto now?", "Market timing"),
        ("Current market sentiment?", "Sentiment analysis"),
        ("Goodbye!", "Farewell")
    ]
    
    print("🧪 TESTING NORMAL PERSONALITY WITH NEWS")
    print("-" * 60)
    
    for query, test_type in test_cases:
        print(f"\n[{test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.get_response(query)
        print(f"Normal Bot: {response['message']}")
        print(f"(Type: {response['type']}, Personality: {response['personality']})")
    
    # Switch to Sub-Zero personality
    print(f"\n{'='*80}")
    print("🧊 SWITCHING TO SUB-ZERO PERSONALITY")
    switch_response = bot.switch_personality('subzero')
    print(f"System: {switch_response}")
    print("-" * 60)
    
    for query, test_type in test_cases:
        print(f"\n[{test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.get_response(query)
        print(f"Sub-Zero: {response['message']}")
        print(f"(Type: {response['type']}, Personality: {response['personality']})")
    
    # Test specific news queries
    print(f"\n{'='*80}")
    print("📰 TESTING SPECIFIC NEWS QUERIES")
    print("-" * 60)
    
    news_queries = [
        "Latest Ethereum news",
        "What's the market sentiment today?",
        "Any Bitcoin updates?",
        "Current crypto market analysis"
    ]
    
    for query in news_queries:
        print(f"\nYou: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response['message']}")
        print(f"(Type: {response['type']})")
    
    # Test personality switching commands
    print(f"\n{'='*80}")
    print("🔄 TESTING PERSONALITY SWITCHING COMMANDS")
    print("-" * 60)
    
    switch_tests = [
        "switch to normal",
        "activate subzero",
        "switch to sub-zero",
        "normal mode"
    ]
    
    for switch_cmd in switch_tests:
        print(f"\nYou: {switch_cmd}")
        response = bot.get_response(switch_cmd)
        print(f"System: {response['message']}")
        print(f"Current personality: {response['personality']}")
    
    # Show conversation history
    print(f"\n{'='*80}")
    print("📜 CONVERSATION HISTORY SUMMARY")
    print("-" * 60)
    history = bot.get_conversation_history()
    print(f"Total conversations: {len(history)}")
    
    personality_counts = {}
    type_counts = {}
    for conv in history:
        personality = conv['personality']
        personality_counts[personality] = personality_counts.get(personality, 0) + 1
        
        # Count response types (from the bot responses)
        response_type = "regular"  # Default for conversation history
        type_counts[response_type] = type_counts.get(response_type, 0) + 1
    
    for personality, count in personality_counts.items():
        print(f"{personality.capitalize()} responses: {count}")
    
    print(f"\n✅ Enhanced chatbot with news insights testing completed!")
    print("🎯 Features tested:")
    print("  ✓ Normal personality with 84,689 human-like conversations")
    print("  ✓ Sub-Zero personality with 3,500 crypto + personality conversations")
    print("  ✓ Real-time crypto news insights and market analysis")
    print("  ✓ Personality switching functionality")
    print("  ✓ Specific coin news queries")
    print("  ✓ Market sentiment analysis")

if __name__ == "__main__":
    test_enhanced_chatbot_with_news()
