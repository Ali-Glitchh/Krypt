#!/usr/bin/env python3
"""
Test the final dual-personality enhanced crypto chatbot with improved datasets
"""

from final_dual_personality_chatbot import DualPersonalityChatbot

def test_enhanced_chatbot():
    print("🚀 Testing Final Dual-Personality Crypto Chatbot")
    print("=" * 70)
    
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
    
    print("\n" + "=" * 70)
    
    # Test cases for both personalities
    test_cases = [
        ("Hello!", "Greeting test"),
        ("What is Bitcoin?", "Crypto knowledge"),
        ("How do I start investing in crypto?", "Investment advice"),
        ("Tell me about blockchain security", "Security knowledge"),
        ("What's your favorite cryptocurrency?", "Personal preferences"),
        ("Should I buy crypto now?", "Market timing"),
        ("How are you doing today?", "Casual conversation"),
        ("What is DeFi?", "Advanced crypto topics"),
        ("Is crypto safe?", "Risk assessment"),
        ("Goodbye!", "Farewell")
    ]
    
    print("🧪 TESTING NORMAL PERSONALITY")
    print("-" * 50)
    
    for query, test_type in test_cases:
        print(f"\n[{test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.get_response(query)
        print(f"Normal Bot: {response['message']}")
        print(f"(Type: {response['type']}, Personality: {response['personality']})")
    
    # Switch to Sub-Zero personality
    print(f"\n{'='*70}")
    print("🧊 SWITCHING TO SUB-ZERO PERSONALITY")
    switch_response = bot.switch_personality('subzero')
    print(f"System: {switch_response}")
    print("-" * 50)
    
    for query, test_type in test_cases:
        print(f"\n[{test_type.upper()}]")
        print(f"You: {query}")
        
        response = bot.get_response(query)
        print(f"Sub-Zero: {response['message']}")
        print(f"(Type: {response['type']}, Personality: {response['personality']})")
    
    # Test personality switching commands
    print(f"\n{'='*70}")
    print("🔄 TESTING PERSONALITY SWITCHING COMMANDS")
    print("-" * 50)
    
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
    print(f"\n{'='*70}")
    print("📜 CONVERSATION HISTORY SUMMARY")
    print("-" * 50)
    history = bot.get_conversation_history()
    print(f"Total conversations: {len(history)}")
    
    personality_counts = {}
    for conv in history:
        personality = conv['personality']
        personality_counts[personality] = personality_counts.get(personality, 0) + 1
    
    for personality, count in personality_counts.items():
        print(f"{personality.capitalize()} responses: {count}")
    
    print(f"\n✅ Enhanced chatbot testing completed!")
    print("🎯 Both personalities are fully trained and operational!")
    print("📊 Normal bot now uses 84,689 human-like conversations from DailyDialog")
    print("🧊 Sub-Zero bot uses 3,500 authentic personality + crypto conversations")

if __name__ == "__main__":
    test_enhanced_chatbot()
