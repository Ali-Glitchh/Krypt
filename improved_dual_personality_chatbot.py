#!/usr/bin/env python3
"""
Improved Dual-Personality Crypto Chatbot
- Dataset-driven responses (no hardcoded fallbacks)
- Enhanced normal personality with crypto knowledge
- Sub-Zero personality with authentic style
- Real-time news insights integration
"""

import json
import random
import re
from typing import Dict, Optional, List
from enhanced_normal_trainer import PureNormalTrainer
from pure_subzero_trainer import PureSubZeroTrainer
from crypto_news_insights import CryptoNewsInsights

class ImprovedDualPersonalityChatbot:
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
        """Initialize both personality trainers with optimal configurations"""
        print("🤖 Initializing Improved Dual-Personality Chatbot...")
          # Enhanced normal personality (crypto-aware + conversational)
        try:
            self.normal_trainer = PureNormalTrainer()
            print("✅ Pure normal personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load normal personality: {e}")
        
        # Pure Sub-Zero personality (dataset-only)
        try:
            self.subzero_trainer = PureSubZeroTrainer()
            print("✅ Pure Sub-Zero personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load Sub-Zero personality: {e}")
        
        print("🎯 Improved dual-personality chatbot ready!")
    
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
    def _is_news_query(self, user_input: str) -> bool:
        """Check if the user is asking for news or market information"""
        news_keywords = [
            'news', 'latest', 'updates', 'market', 'price', 'today',
            'recent', 'current', 'happening', 'trend', 'analysis'
        ]
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in news_keywords)
    
    def _handle_news_query(self, user_input: str) -> Optional[str]:
        """Handle news-related queries with personality adaptation"""
        if not self.news_service:
            return None
        
        try:
            # Use the correct method name
            news_response = self.news_service.get_market_insights(self.personality_mode)
            
            # Add Sub-Zero style if needed (already handled in the method)
            return news_response
            
        except Exception as e:
            print(f"Error getting news: {e}")
            return None
    
    def _subzero_style_news(self, news_content: str) -> str:
        """Add Sub-Zero personality style to news content"""
        intros = [
            "❄️ The markets tremble before this intelligence...",
            "🧊 Mortal, witness the frozen truth of the crypto realm:",
            "❄️ Sub-Zero reveals the icy reality of the markets:",
            "🧊 From the depths of the frozen markets, this knowledge emerges:"
        ]
        
        outros = [
            "The crypto realm yields its secrets to Sub-Zero! ❄️",
            "Such is the way of the frozen markets, mortal. 🧊",
            "The ice-cold truth has been revealed! ❄️"
        ]
        
        intro = random.choice(intros)
        outro = random.choice(outros)
        
        return f"{intro}\n\n{news_content}\n\n{outro}"
    
    def get_response(self, user_input: str) -> Dict:
        """Get response from the current personality"""
        if not user_input.strip():
            # Use personality-appropriate prompts
            if self.personality_mode == "subzero":
                if self.subzero_trainer:
                    prompt_response = self.subzero_trainer.get_response("hello")
                    return {
                        "message": prompt_response,
                        "personality": self.personality_mode,
                        "type": "greeting"
                    }
            else:
                if self.normal_trainer:
                    prompt_response = self.normal_trainer.find_best_response("hello how are you")
                    return {
                        "message": prompt_response,
                        "personality": self.personality_mode,
                        "type": "greeting"
                    }
            
            return {
                "message": "How can I help you today?",
                "personality": self.personality_mode,
                "type": "fallback"
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
        
        # Get response from appropriate trainer
        response = None
        response_type = "unknown"
        
        if self.personality_mode == "subzero" and self.subzero_trainer:
            response = self.subzero_trainer.get_response(user_input)
            response_type = "subzero_response"
        elif self.personality_mode == "normal" and self.normal_trainer:
            response = self.normal_trainer.find_best_response(user_input)
            response_type = "normal_response"
        
        # If no response found, try to get a contextual response
        if not response or response.strip() == "":
            if self.personality_mode == "subzero" and self.subzero_trainer:
                # Try a more general Sub-Zero response
                response = self.subzero_trainer.get_response("crypto")
                response_type = "subzero_fallback"
            elif self.personality_mode == "normal" and self.normal_trainer:
                # Try a more general normal response
                response = self.normal_trainer.find_best_response("help")
                response_type = "normal_fallback"
        
        # Final fallback - should rarely be reached
        if not response or response.strip() == "":
            response = "I'm processing that information. Could you rephrase your question?"
            response_type = "system_fallback"
        
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
            "available_personalities": ["normal", "subzero"],
            "features": [
                "Dataset-driven responses",
                "Real-time crypto news",
                "Personality switching",
                "Contextual conversations"
            ]
        }
        
        if self.normal_trainer:
            info["normal_training"] = {
                "type": "Enhanced Normal",
                "features": ["DailyDialog dataset", "Crypto knowledge integration", "Natural conversations"]
            }
        
        if self.subzero_trainer:
            info["subzero_training"] = {
                "type": "Pure Sub-Zero",
                "features": ["3500+ Sub-Zero pairs", "Authentic personality", "Crypto expertise"]
            }
        
        return info
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

def main():
    """Interactive demo of the improved chatbot"""
    print("🚀 Improved Dual-Personality Crypto Chatbot Demo")
    print("=" * 60)
    
    bot = ImprovedDualPersonalityChatbot()
    
    print("\n📋 Available commands:")
    print("- 'switch to subzero' or 'switch to normal' - Change personality")
    print("- 'news' or 'market updates' - Get crypto news")
    print("- 'info' - Show personality information")
    print("- 'quit' - Exit")
    print("\n💬 Start chatting:")
    
    while True:
        try:
            user_input = input(f"\n[{bot.personality_mode.upper()}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for chatting!")
                break
            
            if user_input.lower() == 'info':
                info = bot.get_personality_info()
                print(f"\n📊 Chatbot Info:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                continue
            
            response = bot.get_response(user_input)
            print(f"\n🤖 Bot: {response['message']}")
            print(f"    [Type: {response['type']} | Personality: {response['personality']}]")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
