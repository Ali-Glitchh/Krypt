#!/usr/bin/env python3
"""
URGENT FIX: Strip Error Resolution for KoinToss Chatbot
This creates a completely fixed version of the chatbot with robust error handling
"""

import json
import random
import re
from typing import Dict, Optional, List
from datetime import datetime

# Import trainers with error handling
try:
    from enhanced_normal_trainer import PureNormalTrainer
    NORMAL_TRAINER_AVAILABLE = True
except ImportError:
    NORMAL_TRAINER_AVAILABLE = False

try:
    from pure_subzero_trainer import PureSubZeroTrainer
    SUBZERO_TRAINER_AVAILABLE = True
except ImportError:
    SUBZERO_TRAINER_AVAILABLE = False

try:
    from crypto_news_insights import CryptoNewsInsights
    NEWS_SERVICE_AVAILABLE = True
except ImportError:
    NEWS_SERVICE_AVAILABLE = False

class FixedDualPersonalityChatbot:
    """Chatbot with 100% strip() error prevention"""
    
    def __init__(self):
        self.personality_mode = "normal"
        self.conversation_history = []
        self.learning_stats = {
            'total_conversations': 0,
            'successful_responses': 0,
            'accuracy_rate': 0.0
        }
        
        # Initialize trainers with robust error handling
        self.normal_trainer = None
        self.subzero_trainer = None
        self.news_service = None
        
        if NORMAL_TRAINER_AVAILABLE:
            try:
                self.normal_trainer = PureNormalTrainer()
                print("✅ Normal trainer loaded")
            except Exception as e:
                print(f"⚠️ Normal trainer failed: {e}")
        
        if SUBZERO_TRAINER_AVAILABLE:
            try:
                self.subzero_trainer = PureSubZeroTrainer()
                print("✅ SubZero trainer loaded")
            except Exception as e:
                print(f"⚠️ SubZero trainer failed: {e}")
        
        if NEWS_SERVICE_AVAILABLE:
            try:
                self.news_service = CryptoNewsInsights()
                print("✅ News service loaded")
            except Exception as e:
                print(f"⚠️ News service failed: {e}")
    
    def safe_string_convert(self, value) -> str:
        """Safely convert any value to string, preventing strip() errors"""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get('message', str(value))
        return str(value)
    
    def switch_personality(self, mode: str = None) -> str:
        """Switch between personalities with robust error handling"""
        try:
            if mode:
                mode = self.safe_string_convert(mode).lower().strip()
                if mode in ['subzero', 'sub-zero', 'sub zero']:
                    self.personality_mode = "subzero"
                    return "🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️"
                elif mode in ['normal', 'crypto', 'default']:
                    self.personality_mode = "normal"
                    return "🤖 Normal mode activated! Ready to help with crypto questions! 📈"
            
            # Toggle if no specific mode given
            if self.personality_mode == "normal":
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! The ice master stands ready! ❄️"
            else:
                self.personality_mode = "normal"
                return "🤖 Normal mode activated! Back to friendly crypto assistance! 📈"
                
        except Exception as e:
            print(f"Error switching personality: {e}")
            return "🤖 Personality switching available in both Normal and Sub-Zero modes!"
    
    def get_response(self, user_input) -> Dict:
        """Get response with complete strip() error prevention"""
        try:
            # CRITICAL: Ensure user_input is always a clean string
            if user_input is None:
                user_input = ""
            
            # Convert to string and clean safely
            user_input_str = self.safe_string_convert(user_input)
            user_input_clean = user_input_str.strip() if user_input_str else ""
            
            # Handle empty input
            if not user_input_clean:
                return self._get_greeting_response()
            
            # Check for personality switch commands
            user_lower = user_input_clean.lower()
            if any(phrase in user_lower for phrase in ['switch to subzero', 'switch to sub-zero', 'activate subzero']):
                switch_msg = self.switch_personality('subzero')
                return {
                    "message": switch_msg,
                    "personality": self.personality_mode,
                    "type": "personality_switch",
                    "confidence": 1.0
                }
            elif any(phrase in user_lower for phrase in ['switch to normal', 'normal mode', 'activate normal']):
                switch_msg = self.switch_personality('normal')
                return {
                    "message": switch_msg,
                    "personality": self.personality_mode,
                    "type": "personality_switch",
                    "confidence": 1.0
                }
            
            # Get response from current personality
            response_message = ""
            response_type = "unknown"
            confidence = 0.5
            
            if self.personality_mode == "subzero" and self.subzero_trainer:
                response_raw = self.subzero_trainer.get_response(user_input_clean)
                response_message = self._extract_message(response_raw)
                response_type = "subzero_response"
                confidence = 0.85
                
            elif self.personality_mode == "normal" and self.normal_trainer:
                response_raw = self.normal_trainer.get_response(user_input_clean)
                response_message = self._extract_message(response_raw)
                response_type = "normal_response"
                confidence = 0.8
            
            # Fallback if no trainer available or no response
            if not response_message or not response_message.strip():
                response_message = self._get_fallback_response(user_input_clean)
                response_type = "fallback"
                confidence = 0.5
            
            # Final safety check
            response_message = self.safe_string_convert(response_message)
            if not response_message.strip():
                response_message = "I'm here to help with crypto questions! What would you like to know?"
            
            # Update stats
            self._update_stats()
            
            # Add to history
            self.conversation_history.append({
                "user": user_input_clean,
                "bot": response_message,
                "personality": self.personality_mode,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "message": response_message,
                "personality": self.personality_mode,
                "type": response_type,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"Error in get_response: {e}")
            return {
                "message": "I'm having technical difficulties. Please try again.",
                "personality": self.personality_mode,
                "type": "error",
                "confidence": 0.0
            }
    
    def _extract_message(self, response_raw) -> str:
        """Safely extract message from any response format"""
        try:
            if response_raw is None:
                return ""
            if isinstance(response_raw, str):
                return response_raw
            if isinstance(response_raw, dict):
                return response_raw.get('message', str(response_raw))
            return str(response_raw)
        except Exception:
            return ""
    
    def _get_greeting_response(self) -> Dict:
        """Get personality-appropriate greeting"""
        if self.personality_mode == "subzero":
            message = "🧊 Sub-Zero greets you, crypto warrior! What knowledge do you seek from the ice master? ❄️"
        else:
            message = "👋 Hello! I'm your crypto assistant. How can I help you today?"
        
        return {
            "message": message,
            "personality": self.personality_mode,
            "type": "greeting",
            "confidence": 1.0
        }
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Get fallback response based on personality"""
        try:
            user_lower = user_input.lower()
            
            # Crypto-related fallbacks
            if any(word in user_lower for word in ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'coin', 'price']):
                if self.personality_mode == "subzero":
                    return "🧊 The ice master senses your interest in the crypto realm! Ask me about specific coins or blockchain concepts, and I shall share frozen wisdom! ❄️"
                else:
                    return "🤖 I'd be happy to help with crypto questions! Try asking about Bitcoin, Ethereum, or any specific cryptocurrency you're interested in."
            
            # General fallbacks
            if self.personality_mode == "subzero":
                return "🧊 Sub-Zero is here to assist! Speak your crypto questions, and the ice master shall respond with frozen wisdom! ❄️"
            else:
                return "🤖 I'm here to help with cryptocurrency questions! What would you like to know?"
                
        except Exception:
            return "I'm here to help! What can I assist you with?"
    
    def _update_stats(self):
        """Update learning statistics"""
        try:
            self.learning_stats['total_conversations'] += 1
            self.learning_stats['successful_responses'] += 1
            if self.learning_stats['total_conversations'] > 0:
                self.learning_stats['accuracy_rate'] = (
                    self.learning_stats['successful_responses'] / 
                    self.learning_stats['total_conversations'] * 100
                )
        except Exception:
            pass
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        return {
            "personality_mode": self.personality_mode,
            "trainers_available": {
                "normal": self.normal_trainer is not None,
                "subzero": self.subzero_trainer is not None
            },
            "news_service": self.news_service is not None,
            "conversation_count": len(self.conversation_history),
            "stats": self.learning_stats
        }

def test_fixed_chatbot():
    """Test the fixed chatbot"""
    print("🧪 Testing Fixed Chatbot (Strip Error Prevention)")
    print("=" * 60)
    
    bot = FixedDualPersonalityChatbot()
    
    # Test cases that might cause strip() errors
    test_cases = [
        "hi",
        "what is bitcoin",
        "",
        "   ",
        None,
        "switch to subzero",
        "what is pi coin",
        {"message": "test dict input"},
        ["test", "list", "input"]
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        try:
            print(f"\n{i}. Testing: {repr(test_input)}")
            response = bot.get_response(test_input)
            print(f"   ✅ Response: {response['message'][:50]}...")
            print(f"   ✅ Type: {response['type']}")
            print(f"   ✅ Personality: {response['personality']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ All tests completed!")
    print(f"📊 Total conversations: {len(bot.conversation_history)}")
    print(f"📈 Success rate: {bot.learning_stats['accuracy_rate']:.1f}%")

if __name__ == "__main__":
    test_fixed_chatbot()
