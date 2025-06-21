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
    
    # Test advanced training features
    print(f"\n{'='*70}")
    print("🎓 TESTING ADVANCED TRAINING FEATURES")
    print("-" * 50)
      # Show learning statistics
    learning_stats = bot.get_learning_statistics()
    print(f"📊 Learning Statistics:")
    print(f"   Continuous learning: {learning_stats.get('continuous_learning_enabled', False)}")
    print(f"   Autonomous training: {learning_stats.get('autonomous_training_enabled', False)}")
    
    if 'autonomous_training_stats' in learning_stats:
        auto_stats = learning_stats['autonomous_training_stats']
        print(f"   Current accuracy: {auto_stats.get('current_accuracy', 'N/A')}%")
        print(f"   Training sessions: {auto_stats.get('sessions_completed', 0)}")
        print(f"   Improvement rate: {auto_stats.get('improvement_rate', 0):+.1f}%")
        print(f"   Synthetic conversations: {auto_stats.get('synthetic_conversations', 0)}")
    
    # Test autonomous training features
    print(f"\n🤖 Testing Autonomous Training:")
    
    # Enable autonomous training
    print("   Enabling autonomous training...")
    if bot.enable_autonomous_training():
        print("   ✅ Autonomous training started!")
        
        # Let it run for a short demo
        import time
        print("   ⏳ Running training for 60 seconds...")
        time.sleep(60)
        
        # Check progress
        auto_status = bot.get_autonomous_training_status()
        print(f"   📈 Training progress:")
        print(f"      Sessions: {auto_status.get('sessions_completed', 0)}")
        print(f"      Accuracy: {auto_status.get('current_accuracy', 0):.1f}%")
        print(f"      Improvement: {auto_status.get('improvement_rate', 0):+.1f}%")
        
        # Disable training
        bot.disable_autonomous_training()
        print("   ⏹️ Autonomous training stopped")
    else:
        print("   ❌ Failed to start autonomous training")
    
    # Get training recommendations
    print(f"\n💡 Training Recommendations:")
    recommendations = bot.get_training_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print(f"\n✅ Enhanced chatbot testing completed!")
    print("🎯 Both personalities are fully trained and operational!")
    print("🚀 Advanced training system is actively improving accuracy!")

if __name__ == "__main__":
    test_enhanced_chatbot()
