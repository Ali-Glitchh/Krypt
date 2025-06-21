#!/usr/bin/env python3
"""
Sub-Zero Personality Demo
Demonstrates the Sub-Zero counterpart trained on adapted human_chat.txt data
"""

from enhanced_crypto_chatbot import EnhancedCryptoChatbot
import time

def demo_subzero_personality():
    """Demonstrate Sub-Zero personality with adapted conversation training"""
    print("🧊" * 60)
    print("           SUB-ZERO PERSONALITY COUNTERPART DEMO")
    print("      Trained on adapted human_chat.txt conversations")
    print("🧊" * 60)
    
    # Initialize chatbot
    chatbot = EnhancedCryptoChatbot()
    
    print(f"\n📊 Training Data Summary:")
    print(f"   - Normal conversation pairs: {len(chatbot.trainer.conversation_pairs) if chatbot.trainer else 0}")
    print(f"   - Sub-Zero conversation pairs: {len(chatbot.subzero_trainer.conversation_pairs) if chatbot.subzero_trainer else 0}")
    print(f"   - Sub-Zero response mappings: {len(chatbot.subzero_trainer.subzero_responses) if chatbot.subzero_trainer else 0}")
    
    # Demo conversations
    demo_scenarios = [
        {
            "title": "🔄 Personality Switching",
            "interactions": [
                ("Switch to Sub-Zero mode", "Activating Sub-Zero personality"),
                ("Hi there!", "Sub-Zero greeting"),
                ("Switch to normal mode", "Switching back"),
                ("Hello again", "Normal greeting")
            ]
        },
        {
            "title": "❄️ Sub-Zero General Conversation (using adapted human_chat.txt)",
            "interactions": [
                ("subzero mode", "Ensuring Sub-Zero mode"),
                ("How are you doing today?", "Sub-Zero response using adapted training"),
                ("What are your plans for the weekend?", "Honor/discipline themed response"),
                ("Tell me about your hobbies", "Ice-cold personality with adapted data"),
                ("Do you like movies?", "Sub-Zero style with conversation training"),
                ("What's your favorite food?", "Cold wisdom from adapted dataset"),
                ("Are you feeling tired?", "Stoic Sub-Zero response"),
                ("Thanks for chatting", "Sub-Zero farewell")
            ]
        },
        {
            "title": "🚀 Sub-Zero + Crypto Knowledge",
            "interactions": [
                ("What's the price of Bitcoin?", "Ice-themed price response"),
                ("Tell me about crypto news", "Frozen intel delivery"),
                ("Analyze the crypto market", "Cold analysis"),
                ("What do you think about DeFi?", "Sub-Zero wisdom on DeFi")
            ]
        }
    ]
    
    for scenario in demo_scenarios:
        print(f"\n{'='*20} {scenario['title']} {'='*20}")
        
        for user_input, description in scenario['interactions']:
            print(f"\n👤 User: {user_input}")
            print(f"💭 Expected: {description}")
            
            # Get response
            response = chatbot.generate_response(user_input)
            message = response.get('message', 'No response')
            response_type = response.get('type', 'unknown')
            
            print(f"🤖 Type: {response_type}")
            print(f"🧊 Sub-Zero: {message}")
            print(f"🎯 Mode: {chatbot.personality_mode}")
            
            # Brief pause for readability
            time.sleep(0.5)
    
    # Show direct Sub-Zero trainer examples
    print(f"\n{'='*25} DIRECT SUB-ZERO TRAINING EXAMPLES {'='*25}")
    
    if chatbot.subzero_trainer:
        print("\n🗣️ Raw Sub-Zero responses from adapted human_chat.txt:")
        
        sample_queries = [
            "How's your week been?",
            "Any interesting plans?", 
            "What do you enjoy doing?",
            "How do you feel about travel?",
            "What's your opinion on technology?",
            "Do you have any advice?"
        ]
        
        for query in sample_queries:
            raw_response = chatbot.subzero_trainer.get_subzero_response(query)
            enhanced_response = chatbot.subzero_trainer.enhance_with_ice_theme(raw_response)
            
            print(f"\n❓ Query: {query}")
            print(f"🧊 Raw Sub-Zero: {raw_response}")
            print(f"❄️ Enhanced: {enhanced_response}")
    
    # Show comparison between modes
    print(f"\n{'='*30} MODE COMPARISON {'='*30}")
    
    comparison_queries = [
        "How are you?",
        "What's up?",
        "Tell me about yourself",
        "Goodbye!"
    ]
    
    for query in comparison_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Normal mode
        chatbot.switch_personality("normal")
        normal_response = chatbot.generate_response(query)
        
        # Sub-Zero mode  
        chatbot.switch_personality("subzero")
        subzero_response = chatbot.generate_response(query)
        
        print(f"😊 Normal: {normal_response.get('message', 'No response')}")
        print(f"🧊 Sub-Zero: {subzero_response.get('message', 'No response')}")
    
    print(f"\n{'🧊'*60}")
    print("           SUB-ZERO COUNTERPART DEMO COMPLETE")
    print("   Successfully trained on adapted human_chat.txt data!")
    print("🧊" * 60)

if __name__ == "__main__":
    demo_subzero_personality()
