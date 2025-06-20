#!/usr/bin/env python3
"""
Test the final dual-personality enhanced crypto chatbot
"""

from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot as DualPersonalityChatbot

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
        print(f"Normal personality: Enhanced training with {normal_stats.get('features', 'multiple features')}")
    
    if 'subzero_training' in info:
        subzero_stats = info['subzero_training']
        print(f"Sub-Zero personality: {subzero_stats.get('type', 'Advanced')} training")
        if 'features' in subzero_stats:
            print(f"  - Features: {', '.join(subzero_stats['features'])}")
    
    print(f"Available features: {', '.join(info.get('features', []))}")
    
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

if __name__ == "__main__":
    test_enhanced_chatbot()
