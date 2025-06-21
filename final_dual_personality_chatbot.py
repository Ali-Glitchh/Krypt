#!/usr/bin/env python3
"""
Final Dual-Personality Crypto Chatbot with Complete Training and News Insights
"""

import json
import random
import re
from typing import Dict, Optional, List
from enhanced_normal_trainer_v2 import EnhancedNormalTrainer
from advanced_subzero_trainer_fixed import AdvancedSubZeroTrainer
from crypto_news_insights import CryptoNewsInsights

class DualPersonalityChatbot:
    def __init__(self):
        self.personality_mode = "normal"  # "normal" or "subzero"
        self.normal_trainer = None
        self.subzero_trainer = None
        self.news_service = None
        
        # Initialize both trainers and news service
        self.initialize_trainers()
        self.initialize_news_service()
        
        # Conversation history
        self.conversation_history = []
    
    def initialize_trainers(self):
        """Initialize both personality trainers"""
        print("🤖 Initializing Dual-Personality Chatbot...")
        
        # Normal personality
        try:
            self.normal_trainer = EnhancedNormalTrainer()
            print("✅ Normal personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load normal personality: {e}")
        
        # Sub-Zero personality
        try:
            self.subzero_trainer = AdvancedSubZeroTrainer()
            print("✅ Sub-Zero personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load Sub-Zero personality: {e}")
        
        print("🎯 Dual-personality chatbot ready!")
    
    def initialize_news_service(self):
        """Initialize the crypto news insights service"""
        try:
            self.news_service = CryptoNewsInsights()
            print("📰 News insights service loaded")
        except Exception as e:
            print(f"⚠️ News service failed to load: {e}")
            self.news_service = None
    
    def switch_personality(self, mode: str = None) -> str:
        """Switch between normal and Sub-Zero personality modes"""
        if mode:
            if mode.lower() in ['subzero', 'sub-zero', 'sub zero']:
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️"
            elif mode.lower() in ['normal', 'regular', 'default']:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready to help with crypto insights!"
        else:
            # Toggle mode
            if self.personality_mode == "normal":
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️"
            else:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready to help with crypto insights!"
        
        return f"Current personality: {self.personality_mode}"
    
    def get_response(self, user_input: str) -> Dict:
        """Get response from the current personality"""
        if not user_input.strip():
            return {
                "message": "I'm here to chat! What would you like to discuss?",
                "personality": self.personality_mode,
                "type": "prompt"
            }
        
        # Check for personality switch commands
        user_lower = user_input.lower()
        if any(phrase in user_lower for phrase in ['switch to subzero', 'switch to sub-zero', 'activate subzero']):
            switch_msg = self.switch_personality('subzero')
            return {
                "message": switch_msg,
                "personality": self.personality_mode,
                "type": "personality_switch"
            }
        elif any(phrase in user_lower for phrase in ['switch to normal', 'activate normal', 'normal mode']):
            switch_msg = self.switch_personality('normal')
            return {
                "message": switch_msg,
                "personality": self.personality_mode,
                "type": "personality_switch"
            }        # Check for news-related queries
        if self._is_news_query(user_input):
            news_response = self._handle_news_query(user_input)
            if news_response:
                return {
                    "message": news_response,
                    "personality": self.personality_mode,
                    "type": "news_insights"
                }
        
        # Get response from appropriate trainer
        if self.personality_mode == "subzero" and self.subzero_trainer:
            response = self.subzero_trainer.get_response(user_input)
            response_type = "subzero_response"
        elif self.personality_mode == "normal" and self.normal_trainer:
            response = self.normal_trainer.find_best_response(user_input)
            response_type = "normal_response"
        else:
            response = "Sorry, the requested personality is not available right now."
            response_type = "error"
        
        # Add to conversation history
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "personality": self.personality_mode
        })
        
        return {
            "message": response,
            "personality": self.personality_mode,
            "type": response_type
        }
    
    def get_personality_info(self) -> Dict:
        """Get information about current personality and training data"""
        info = {
            "current_personality": self.personality_mode,
            "available_personalities": ["normal", "subzero"]
        }
        
        if self.normal_trainer:
            normal_stats = self.normal_trainer.get_conversation_stats()
            info["normal_training"] = normal_stats
        
        if self.subzero_trainer:
            subzero_stats = self.subzero_trainer.get_conversation_stats()
            info["subzero_training"] = subzero_stats
        
        return info
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _is_news_query(self, user_input: str) -> bool:
        """Check if user is asking for news or market insights"""
        user_lower = user_input.lower()
        news_keywords = [
            'news', 'latest', 'recent', 'updates', 'headlines', 'market insights',
            'market news', 'crypto news', 'what\'s happening', 'current events',
            'market sentiment', 'market analysis', 'price movement', 'market update'
        ]
        
        return any(keyword in user_lower for keyword in news_keywords)
    
    def _handle_news_query(self, user_input: str) -> Optional[str]:
        """Handle news-related queries"""
        if not self.news_service:
            if self.personality_mode == "subzero":
                return "🧊 Sub-Zero's intelligence network is temporarily offline! The ice realm cannot access current market data right now. ❄️"
            else:
                return "Sorry, news insights are currently unavailable. Please try again later."
        
        user_lower = user_input.lower()
        
        # Check for specific coin news
        coins = ['bitcoin', 'btc', 'ethereum', 'eth', 'dogecoin', 'doge', 'cardano', 'ada', 'solana', 'sol']
        for coin in coins:
            if coin in user_lower:
                return self.news_service.get_specific_coin_news(coin, self.personality_mode)
        
        # General market insights
        return self.news_service.get_market_insights(self.personality_mode)

# CLI Interface for testing
def main():
    print("🚀 Starting Dual-Personality Crypto Chatbot")
    print("="*60)
    
    # Initialize chatbot
    chatbot = DualPersonalityChatbot()
    
    # Show personality info
    info = chatbot.get_personality_info()
    print(f"\n📊 Chatbot Information:")
    print(f"Current personality: {info['current_personality'].upper()}")
    
    if 'normal_training' in info:
        normal_stats = info['normal_training']
        print(f"Normal personality: {normal_stats['total_conversations']} conversations trained")
    
    if 'subzero_training' in info:
        subzero_stats = info['subzero_training']
        print(f"Sub-Zero personality: {subzero_stats['total_conversations']} conversations trained")
    
    print("\n💬 Chat Interface")
    print("Commands:")
    print("  'switch' - Toggle between personalities")
    print("  'info' - Show personality information")
    print("  'history' - Show conversation history")
    print("  'clear' - Clear conversation history")
    print("  'quit' - Exit")
    print("-" * 60)
    
    while True:
        # Show current personality
        personality_indicator = "🧊 SUB-ZERO" if chatbot.personality_mode == "subzero" else "😊 NORMAL"
        user_input = input(f"\n[{personality_indicator}] You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Thanks for chatting! Goodbye!")
            break
        elif user_input.lower() == 'switch':
            switch_msg = chatbot.switch_personality()
            print(f"System: {switch_msg}")
            continue
        elif user_input.lower() == 'info':
            info = chatbot.get_personality_info()
            print(f"\nPersonality Info:")
            print(f"Current: {info['current_personality']}")
            if 'normal_training' in info:
                print(f"Normal: {info['normal_training']['total_conversations']} conversations")
            if 'subzero_training' in info:
                print(f"Sub-Zero: {info['subzero_training']['total_conversations']} conversations")
            continue
        elif user_input.lower() == 'history':
            history = chatbot.get_conversation_history()
            print(f"\nConversation History ({len(history)} messages):")
            for i, conv in enumerate(history[-5:], 1):  # Show last 5
                print(f"{i}. [{conv['personality'].upper()}] You: {conv['user']}")
                print(f"   Bot: {conv['bot'][:100]}...")
            continue
        elif user_input.lower() == 'clear':
            chatbot.clear_history()
            print("System: Conversation history cleared!")
            continue
        elif not user_input:
            continue
        
        # Get bot response
        response = chatbot.get_response(user_input)
        print(f"Bot: {response['message']}")

if __name__ == "__main__":
    main()
