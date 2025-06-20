#!/usr/bin/env python3
"""
Pure Dataset-Trained Dual-Personality Crypto Chatbot
Uses only training data - no hardcoded responses
"""

import json
import random
import re
from typing import Dict, Optional, List
from pure_normal_trainer import PureNormalTrainer
from pure_subzero_trainer import PureSubZeroTrainer
from crypto_news_insights import CryptoNewsInsights

class PureDualPersonalityChatbot:
    def __init__(self):
        self.personality_mode = "normal"  # "normal" or "subzero"
        self.normal_trainer = None
        self.subzero_trainer = None
        self.news_service = None
        
        # Initialize all services
        self.initialize_trainers()
        self.initialize_news_service()
        
        # Conversation history
        self.conversation_history = []
    
    def initialize_trainers(self):
        """Initialize both pure personality trainers"""
        print("🤖 Initializing Pure Dataset-Trained Dual-Personality Chatbot...")
        
        # Normal personality
        try:
            self.normal_trainer = PureNormalTrainer()
            print("✅ Pure normal personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load normal personality: {e}")
        
        # Sub-Zero personality
        try:
            self.subzero_trainer = PureSubZeroTrainer()
            print("✅ Pure Sub-Zero personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load Sub-Zero personality: {e}")
        
        print("🎯 Pure dual-personality chatbot ready!")
    
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
                return "🧊 Sub-Zero mode activated! Ready to share ice-cold crypto wisdom! ❄️"
            elif mode.lower() in ['normal', 'regular', 'default']:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready for natural conversation!"
        else:
            # Toggle mode
            if self.personality_mode == "normal":
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! Ready to share ice-cold crypto wisdom! ❄️"
            else:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready for natural conversation!"
        
        return f"Current personality: {self.personality_mode}"
    
    def get_response(self, user_input: str) -> Dict:
        """Get response from the current personality - PURE training data only"""
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
            }
        
        # Check for news-related queries
        if self._is_news_query(user_input):
            news_response = self._handle_news_query(user_input)
            if news_response:
                return {
                    "message": news_response,
                    "personality": self.personality_mode,
                    "type": "news_insights"
                }
        
        # Get response from appropriate PURE trainer
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
    
    def get_personality_info(self) -> Dict:
        """Get information about current personality and training"""
        info = {
            "current_personality": self.personality_mode,
        }
        
        # Add normal training info
        if self.normal_trainer:
            normal_stats = self.normal_trainer.get_training_stats()
            info["normal_training"] = normal_stats
        
        # Add Sub-Zero training info
        if self.subzero_trainer:
            subzero_stats = self.subzero_trainer.get_training_stats()
            info["subzero_training"] = subzero_stats
        
        return info
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history.copy()

# CLI Interface for testing
def main():
    print("🚀 Starting Pure Dataset-Trained Dual-Personality Crypto Chatbot")
    print("="*70)
    
    # Initialize chatbot
    chatbot = PureDualPersonalityChatbot()
    
    # Show personality info
    info = chatbot.get_personality_info()
    print(f"\n📊 Chatbot Information:")
    print(f"Current personality: {info['current_personality'].upper()}")
    
    if 'normal_training' in info:
        normal_stats = info['normal_training']
        print(f"Normal personality: {normal_stats['total_conversations']:,} pure conversations trained")
    
    if 'subzero_training' in info:
        subzero_stats = info['subzero_training']
        print(f"Sub-Zero personality: {subzero_stats['total_conversations']:,} pure conversations trained")
        print(f"  - Crypto coverage: {subzero_stats['crypto_conversations']:,} conversations")
    
    print(f"\n💡 This chatbot uses ONLY training data - no hardcoded responses!")
    print(f"🎯 Personality switching: 'switch to subzero' or 'normal mode'")
    print(f"📰 News queries: 'latest crypto news', 'bitcoin news', 'market insights'")
    print(f"💬 Type 'quit' to exit\n")
    
    # Chat loop
    while True:
        try:
            user_input = input(f"[{chatbot.personality_mode.upper()}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for chatting! Stay frosty! ❄️")
                break
            
            if not user_input:
                continue
            
            response = chatbot.get_response(user_input)
            personality_icon = "🧊" if response['personality'] == 'subzero' else "🤖"
            personality_name = "Sub-Zero" if response['personality'] == 'subzero' else "Bot"
            
            print(f"{personality_icon} {personality_name}: {response['message']}")
            
            # Show response type for debugging
            if response['type'] in ['news_insights', 'personality_switch']:
                print(f"   💭 [{response['type']}]")
            
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for chatting! Stay frosty! ❄️")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
