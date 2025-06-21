#!/usr/bin/env python3
"""
Continuous Training Demo
Demonstrates the chatbot learning and improving in real-time
"""

import time
import random
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot as DualPersonalityChatbot

def demonstrate_continuous_training():
    print("🚀 Continuous Training & Improvement Demo")
    print("=" * 60)
    
    # Initialize the chatbot
    bot = DualPersonalityChatbot()
    
    print("\n📊 Initial Training State:")
    initial_stats = bot.get_learning_statistics()
    print(f"   Continuous learning: {initial_stats.get('continuous_learning_enabled', False)}")
    print(f"   Training conversations: {initial_stats.get('total_training_conversations', 0)}")
    if 'advanced_training_stats' in initial_stats:
        adv_stats = initial_stats['advanced_training_stats']
        print(f"   Success rate: {adv_stats.get('success_rate', 'N/A')}%")
        print(f"   Total interactions: {adv_stats.get('total_interactions', 0)}")
    
    # Demonstrate learning over multiple conversation rounds
    conversation_rounds = [
        {
            "title": "Round 1: Basic Crypto Questions",
            "questions": [
                "What is Bitcoin?",
                "How does blockchain work?",
                "What is cryptocurrency mining?",
                "Is Bitcoin safe to invest in?",
                "How do I buy Bitcoin?"
            ]
        },
        {
            "title": "Round 2: Advanced Topics",
            "questions": [
                "What is DeFi and how does it work?",
                "Explain smart contracts",
                "What are NFTs?",
                "How does staking work?",
                "What is the difference between Proof of Work and Proof of Stake?"
            ]
        },
        {
            "title": "Round 3: Investment & Strategy",
            "questions": [
                "Should I diversify my crypto portfolio?",
                "What is dollar-cost averaging?",
                "How do I analyze crypto market trends?",
                "What are the risks of crypto investing?",
                "When should I take profits?"
            ]
        }
    ]
    
    total_interactions = 0
    
    for round_num, round_data in enumerate(conversation_rounds, 1):
        print(f"\n{'='*60}")
        print(f"🎯 {round_data['title']}")
        print("-" * 50)
        
        round_start_time = time.time()
        
        for i, question in enumerate(round_data['questions'], 1):
            print(f"\n[Question {i}/5] {question}")
            
            # Get response
            response = bot.get_response(question)
            print(f"Bot: {response['message'][:100]}{'...' if len(response['message']) > 100 else ''}")
            print(f"     [Type: {response['type']}, Confidence tracked for learning]")
            
            # Simulate user feedback (realistic ratings)
            if response['type'] in ['normal_trained_data', 'subzero_response']:
                satisfaction = random.uniform(0.7, 1.0)  # Good responses
            elif response['type'] in ['normal_pattern_match', 'news_insights']:
                satisfaction = random.uniform(0.6, 0.9)  # Decent responses
            else:
                satisfaction = random.uniform(0.4, 0.7)  # Fair responses
            
            # Provide feedback
            bot.provide_feedback(total_interactions, satisfaction)
            total_interactions += 1
            
            # Small delay to show real-time learning
            time.sleep(0.5)
        
        round_time = time.time() - round_start_time
        print(f"\n📈 Round {round_num} completed in {round_time:.1f} seconds")
        
        # Show learning progress after each round
        current_stats = bot.get_learning_statistics()
        if 'advanced_training_stats' in current_stats:
            adv_stats = current_stats['advanced_training_stats']
            print(f"   Current success rate: {adv_stats.get('success_rate', 'N/A')}%")
            print(f"   Total interactions: {adv_stats.get('total_interactions', 0)}")
            print(f"   User satisfaction: {adv_stats.get('avg_user_satisfaction', 'N/A')}")
        
        # Trigger training after each round
        if round_num % 2 == 0:  # Train after rounds 2 and 4
            print(f"\n🎓 Triggering training cycle...")
            training_result = bot.trigger_training_cycle()
            print(f"   {training_result}")
    
    # Final assessment
    print(f"\n{'='*60}")
    print("📊 FINAL TRAINING ASSESSMENT")
    print("-" * 50)
    
    final_stats = bot.get_learning_statistics()
    print(f"Final learning statistics:")
    
    if 'normal_trainer_stats' in final_stats:
        normal_stats = final_stats['normal_trainer_stats']
        print(f"   Normal trainer accuracy: {normal_stats.get('accuracy_rate', 'N/A')}%")
        print(f"   Dynamic conversations added: {normal_stats.get('dynamic_conversations', 0)}")
        print(f"   Total vocabulary size: {normal_stats.get('vocabulary_size', 0)}")
    
    if 'advanced_training_stats' in final_stats:
        adv_stats = final_stats['advanced_training_stats']
        print(f"   Overall success rate: {adv_stats.get('success_rate', 'N/A')}%")
        print(f"   Total interactions processed: {adv_stats.get('total_interactions', 0)}")
        print(f"   Learning iterations: {adv_stats.get('learning_iterations', 0)}")
        print(f"   Model updates: {adv_stats.get('model_updates', 0)}")
        print(f"   Average user satisfaction: {adv_stats.get('avg_user_satisfaction', 'N/A')}")
    
    # Get improvement recommendations
    print(f"\n💡 Current recommendations:")
    recommendations = bot.get_training_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Test both personalities with learned improvements
    print(f"\n{'='*60}")
    print("🧪 TESTING BOTH PERSONALITIES AFTER TRAINING")
    print("-" * 50)
    
    test_question = "What's the best way to get started with cryptocurrency?"
    
    # Normal personality
    print(f"\n[NORMAL] {test_question}")
    normal_response = bot.get_response(test_question)
    print(f"Normal: {normal_response['message']}")
    
    # Switch to Sub-Zero
    bot.switch_personality('subzero')
    print(f"\n[SUB-ZERO] {test_question}")
    subzero_response = bot.get_response(test_question)
    print(f"Sub-Zero: {subzero_response['message']}")
    
    print(f"\n✅ Continuous training demonstration completed!")
    print("🎯 The chatbot has learned and improved from user interactions!")
    print("🚀 Training system continues to run in the background for ongoing improvement!")

def interactive_training_session():
    """Interactive session where users can train the bot in real-time"""
    print("\n" + "="*60)
    print("🤖 INTERACTIVE TRAINING SESSION")
    print("=" + "="*60)
    print("Train the chatbot by asking questions and providing feedback!")
    print("Commands:")
    print("  'stats' - Show learning statistics")
    print("  'train' - Trigger manual training cycle")
    print("  'recommendations' - Get improvement suggestions")
    print("  'switch' - Switch personality")
    print("  'quit' - Exit training session")
    print("-" * 60)
    
    bot = DualPersonalityChatbot()
    interaction_count = 0
    
    while True:
        try:
            user_input = input(f"\n[{bot.personality_mode.upper()}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Training session ended. Thanks for helping improve the bot!")
                break
            
            elif user_input.lower() == 'stats':
                stats = bot.get_learning_statistics()
                print("\n📊 Current Learning Statistics:")
                if 'advanced_training_stats' in stats:
                    adv_stats = stats['advanced_training_stats']
                    for key, value in adv_stats.items():
                        print(f"   {key}: {value}")
                continue
            
            elif user_input.lower() == 'train':
                result = bot.trigger_training_cycle()
                print(f"🎓 {result}")
                continue
            
            elif user_input.lower() == 'recommendations':
                recs = bot.get_training_recommendations()
                print("\n💡 Current Recommendations:")
                for i, rec in enumerate(recs, 1):
                    print(f"   {i}. {rec}")
                continue
            
            elif user_input.lower() == 'switch':
                switch_result = bot.switch_personality()
                print(f"🔄 {switch_result}")
                continue
            
            # Get bot response
            response = bot.get_response(user_input)
            print(f"\n🤖 {response['message']}")
            print(f"    [Type: {response['type']}]")
            
            # Ask for feedback
            while True:
                feedback_input = input("Rate this response (1-5, or press Enter to skip): ").strip()
                if not feedback_input:
                    break
                try:
                    rating = int(feedback_input)
                    if 1 <= rating <= 5:
                        satisfaction = rating / 5.0  # Convert to 0-1 scale
                        bot.provide_feedback(interaction_count, satisfaction)
                        break
                    else:
                        print("Please enter a number between 1 and 5")
                except ValueError:
                    print("Please enter a valid number")
            
            interaction_count += 1
            
        except KeyboardInterrupt:
            print("\n👋 Training session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    demonstrate_continuous_training()
    
    # Ask if user wants interactive session
    while True:
        choice = input("\nWould you like to try the interactive training session? (y/n): ").lower()
        if choice in ['y', 'yes']:
            interactive_training_session()
            break
        elif choice in ['n', 'no']:
            print("👋 Thanks for trying the training demo!")
            break
        else:
            print("Please enter 'y' or 'n'")
