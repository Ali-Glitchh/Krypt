#!/usr/bin/env python3
"""
Quick Demo: Dual-Personality Crypto Chatbot
Test both personalities and response handling
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    
    print("🚀 DUAL-PERSONALITY CRYPTO CHATBOT DEMO")
    print("=" * 50)
    
    # Initialize chatbot
    print("🤖 Initializing chatbot...")
    bot = ImprovedDualPersonalityChatbot()
    
    print("\n📋 Testing Normal Personality:")
    print("-" * 30)
    
    # Test normal personality
    response = bot.get_response("What is Bitcoin?")
    print(f"User: What is Bitcoin?")
    print(f"Bot: {response['message']}")
    print(f"Personality: {response['personality']}")
    
    print("\n🧊 Switching to Sub-Zero:")
    print("-" * 30)
      # Switch to Sub-Zero
    switch_response = bot.switch_personality()
    print(f"Switch: {switch_response}")  # switch_personality returns a string, not dict
      # Test Sub-Zero personality
    response = bot.get_response("Tell me about crypto")
    print(f"User: Tell me about crypto")
    print(f"Bot: {response['message']}")
    print(f"Personality: {response['personality']}")
    
    print("\n📊 System Info:")
    print("-" * 30)
    personality_info = bot.get_personality_info()
    print(f"Current Personality: {personality_info['current_personality']}")
    print(f"Available Personalities: {', '.join(personality_info['available_personalities'])}")
    print(f"Features: {', '.join(personality_info['features'])}")
    
    if 'normal_training' in personality_info:
        print(f"Normal Training: {personality_info['normal_training']['type']}")
        
    if 'subzero_training' in personality_info:
        print(f"Sub-Zero Training: {personality_info['subzero_training']['type']}")
    
    print("\n✅ Demo completed successfully!")
    print("🚀 System is ready for production deployment!")
    
except Exception as e:
    print(f"❌ Error during demo: {e}")
    import traceback
    traceback.print_exc()
