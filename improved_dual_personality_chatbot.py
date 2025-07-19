#!/usr/bin/env python3
"""
Simplified Dual-Personality Crypto Chatbot (Strip Error Fixed)
- Fixed all strip() errors with proper type checking
- Disabled autonomous training to prevent hanging
- Core functionality maintained
"""

import json
import random
import re
from typing import Dict, Optional, List
from enhanced_normal_trainer import PureNormalTrainer
from enhanced_subzero_trainer import EnhancedSubZeroTrainer as PureSubZeroTrainer
from crypto_news_insights import CryptoNewsInsights
from datetime import datetime

class ImprovedDualPersonalityChatbot:
    def __init__(self):
        self.personality_mode = "normal"  # "normal" or "subzero"
        self.normal_trainer = None
        self.subzero_trainer = None
        self.news_service = None
        
        # Disable autonomous training for now
        self.autonomous_trainer = None
        self.auto_training_enabled = False
        
        # Initialize core services
        self.initialize_trainers()
        self.initialize_news_service()
        
        # Conversation history
        self.conversation_history = []
        self.learning_stats = {
            'total_conversations': 0,
            'successful_responses': 0,
            'accuracy_rate': 0.0
        }
    
    def initialize_trainers(self):
        """Initialize both personality trainers with optimal configurations"""
        print("🤖 Initializing Simplified Dual-Personality Chatbot...")
        
        # Enhanced normal personality
        try:
            self.normal_trainer = PureNormalTrainer()
            print("✅ Enhanced normal personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load enhanced trainer: {e}")
            self.normal_trainer = None
        
        # Pure Sub-Zero personality
        try:
            self.subzero_trainer = PureSubZeroTrainer()
            print("✅ Pure Sub-Zero personality loaded and trained")
        except Exception as e:
            print(f"❌ Failed to load Sub-Zero personality: {e}")
        
        print("🎯 Simplified dual-personality chatbot ready!")
    
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
            elif mode.lower() in ['normal', 'crypto', 'default']:
                self.personality_mode = "normal"
                return "🤖 Normal mode activated! Ready to help with crypto questions! 📈"
        
        # Toggle if no specific mode given
        if self.personality_mode == "normal":
            self.personality_mode = "subzero"
            return "🧊 Sub-Zero mode activated! The Lin Kuei shall dominate the crypto realm! ❄️"
        else:
            self.personality_mode = "normal"
            return "🤖 Normal mode activated! Back to friendly crypto assistance! 📈"
    
    def get_crypto_news_context(self, user_input: str) -> str:
        """Get relevant crypto news context (Sub-Zero style)"""
        if not self.news_service:
            return ""
        
        # Extract potential crypto symbols from user input
        crypto_words = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'defi', 'nft']
        found_crypto = None
        
        for word in crypto_words:
            if word in user_input.lower():
                found_crypto = word
                break
        
        if not found_crypto:
            return ""
        
        # Get news content (placeholder for now)
        news_content = f"Recent developments in {found_crypto.upper()} markets show continued volatility and institutional interest."
        
        # Sub-Zero themed intro/outro
        intros = [
            "The frost reveals market truths hidden from mortal eyes...",
            "Ice-cold analysis of the current market conditions:",
            "The Lin Kuei intelligence network reports:",
            "From the frozen realm of market data:"
        ]
        
        outros = [
            "Such is the way of the frozen markets, mortal. 🧊",
            "The ice-cold truth has been revealed! ❄️"
        ]
        
        intro = random.choice(intros)
        outro = random.choice(outros)
        
        return f"{intro}\n\n{news_content}\n\n{outro}"
    
    def get_response(self, user_input: str) -> Dict:
        """Get response from the current personality with fixed strip() handling"""
        
        # CRITICAL FIX: Ensure user_input is always a string
        if not isinstance(user_input, str):
            user_input = str(user_input)
            
        if not user_input.strip():
            # Use personality-appropriate prompts
            if self.personality_mode == "subzero":
                if self.subzero_trainer:
                    prompt_response = self.subzero_trainer.get_response("hello")
                    # Handle both dict and string responses
                    if isinstance(prompt_response, dict):
                        message = prompt_response.get('message', str(prompt_response))
                    else:
                        message = str(prompt_response)
                    return {
                        "message": message,
                        "personality": self.personality_mode,
                        "type": "greeting"
                    }
            else:
                if self.normal_trainer:
                    prompt_response = self.normal_trainer.find_best_response("hello how are you")
                    # Handle both dict and string responses
                    if isinstance(prompt_response, dict):
                        message = prompt_response.get('message', str(prompt_response))
                    else:
                        message = str(prompt_response)
                    return {
                        "message": message,
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
        elif any(phrase in user_lower for phrase in ['switch to normal', 'normal mode', 'activate normal']):
            switch_msg = self.switch_personality('normal')
            return {
                "message": switch_msg,
                "personality": self.personality_mode,
                "type": "personality_switch"
            }
        
        # Check for project-specific questions first
        project_response = self.get_project_info(user_input)
        if project_response:
            return project_response
        
        # Check for enhanced crypto knowledge
        crypto_response = self.get_enhanced_crypto_knowledge(user_input)
        if crypto_response:
            return crypto_response
        
        # Initialize response variables
        response_message = ""
        response_type = "unknown"
        confidence = 0.0
        
        # Get response based on current personality
        if self.personality_mode == "subzero" and self.subzero_trainer:
            # Sub-Zero personality response
            response_raw = self.subzero_trainer.get_response(user_input)
            if isinstance(response_raw, dict):
                response_message = response_raw.get('message', str(response_raw))
                confidence = response_raw.get('confidence', 0.8)
            else:
                response_message = str(response_raw)
                confidence = 0.8
            response_type = "subzero_response"
            
        elif self.personality_mode == "normal" and self.normal_trainer:
            # Normal personality response
            response_raw = self.normal_trainer.get_response(user_input)
            if isinstance(response_raw, dict):
                response_message = response_raw.get('message', str(response_raw))
                confidence = response_raw.get('confidence', 0.7)
            else:
                response_message = str(response_raw)
                confidence = 0.7
            response_type = "normal_response"
        else:
            # Fallback if no trainer available
            response_raw = self.normal_trainer.find_best_response(user_input) if self.normal_trainer else None
            if response_raw:
                if isinstance(response_raw, dict):
                    response_message = response_raw.get('message', str(response_raw))
                else:
                    response_message = str(response_raw)
                response_type = "normal_response"
                confidence = 0.6
        
        # CRITICAL FIX: Ensure response_message is a string before strip() operations
        if not isinstance(response_message, str):
            response_message = str(response_message)
        
        # If no response found, try to get a contextual response
        if not response_message or response_message.strip() == "":
            if self.personality_mode == "subzero" and self.subzero_trainer:
                # Try a more general Sub-Zero response
                fallback_response = self.subzero_trainer.get_response("crypto")
                if isinstance(fallback_response, dict):
                    response_message = fallback_response.get('message', str(fallback_response))
                else:
                    response_message = str(fallback_response)
                response_type = "subzero_fallback"
            elif self.personality_mode == "normal" and self.normal_trainer:
                # Try a more general normal response
                fallback_response = self.normal_trainer.find_best_response("help")
                if isinstance(fallback_response, dict):
                    response_message = fallback_response.get('message', str(fallback_response))
                else:
                    response_message = str(fallback_response)
                response_type = "normal_fallback"
        
        # CRITICAL FIX: Final type check before strip()
        if not isinstance(response_message, str):
            response_message = str(response_message)
            
        # Final fallback - should rarely be reached
        if not response_message or response_message.strip() == "":
            response_message = "I'm processing that information. Could you rephrase your question?"
            response_type = "system_fallback"
            
        # Add to conversation history
        self.conversation_history.append({
            "user": user_input,
            "bot": response_message,
            "personality": self.personality_mode
        })
        
        # Update learning stats
        self.learning_stats['total_conversations'] += 1
        if response_type != "system_fallback":
            self.learning_stats['successful_responses'] += 1
        
        if self.learning_stats['total_conversations'] > 0:
            self.learning_stats['accuracy_rate'] = (
                self.learning_stats['successful_responses'] / 
                self.learning_stats['total_conversations'] * 100
            )
        
        return {
            "message": response_message,
            "personality": self.personality_mode,
            "type": response_type,
            "confidence": confidence
        }
    
    def get_project_info(self, user_input: str) -> Optional[Dict]:
        """Handle questions about the KoinToss project specifically"""
        user_lower = user_input.lower()
        
        # KoinToss project questions
        kointoss_keywords = ['kointoss', 'koin toss', 'coin toss', 'this project', 'your project', 'about you']
        if any(keyword in user_lower for keyword in kointoss_keywords):
            if self.personality_mode == "subzero":
                return {
                    "message": "🧊 KOINTOSS IS THE ULTIMATE CRYPTO WEAPON! A dual-personality AI assistant forged in the ice of digital warfare! I am your WARRIOR mode - providing COLD, calculated market insights and aggressive trading wisdom! The educational mode teaches, but I DOMINATE! Together we conquer the crypto realm with UNSTOPPABLE POWER! This project combines advanced AI, real-time market data, and pure DETERMINATION! ❄️⚔️💎",
                    "personality": self.personality_mode,
                    "type": "project_info",
                    "confidence": 0.95
                }
            else:
                return {
                    "message": "KoinToss is an advanced AI-powered cryptocurrency assistant designed to help users navigate the complex world of digital assets. Our unique dual-personality system offers two distinct modes: 🎓 Educational Mode (that's me!) provides friendly, informative guidance perfect for learning, and ⚔️ Warrior Mode offers bold, aggressive market insights. The project integrates real-time market data, sentiment analysis, and continuous learning capabilities to deliver comprehensive crypto assistance. Whether you're a beginner or experienced trader, KoinToss adapts to your needs!",
                    "personality": self.personality_mode,
                    "type": "project_info",
                    "confidence": 0.95
                }
        
        return None

    def get_enhanced_crypto_knowledge(self, user_input: str) -> Optional[Dict]:
        """Provide enhanced crypto knowledge responses"""
        user_lower = user_input.lower()
        
        # Bitcoin questions
        if any(word in user_lower for word in ['bitcoin', 'btc']):
            if self.personality_mode == "subzero":
                return {
                    "message": "🧊 BITCOIN - THE APEX PREDATOR OF CRYPTO! Created by the legendary Satoshi Nakamoto in 2009, this digital beast commands RESPECT! 💎 21 million coins maximum - SCARCITY breeds POWER! No banks, no government control - PURE DECENTRALIZATION! When institutions tremble, you know it's UNSTOPPABLE! Bitcoin doesn't ask permission - it TAKES what it deserves! The blockchain fortress is UNBREAKABLE! This is the KING of all cryptocurrencies! ❄️⚔️👑",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
            else:
                return {
                    "message": "Bitcoin (BTC) is the world's first and most well-known cryptocurrency, created in 2009 by the pseudonymous Satoshi Nakamoto. Often called 'digital gold,' Bitcoin features: 📊 Limited supply of 21 million coins, 🔒 Decentralized network with no central authority, 💫 Peer-to-peer transactions without banks, 🛡️ Secured by blockchain technology and mining. Bitcoin's value comes from its scarcity, utility as a store of value, and growing institutional adoption. It's the foundation of the entire cryptocurrency ecosystem!",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
        
        # Ethereum questions
        if any(word in user_lower for word in ['ethereum', 'eth']):
            if self.personality_mode == "subzero":
                return {
                    "message": "🧊 ETHEREUM - THE PROGRAMMABLE ICE FORTRESS! Created by the brilliant Vitalik Buterin in 2015, this platform is BUILT FOR WAR! 💪 Smart contracts = UNSTOPPABLE automation! DeFi kingdoms run on Ethereum's FROZEN rails! After 'The Merge' upgrade, ETH became a STAKING POWERHOUSE! 🔥 Supply burns while stakers earn - DEFLATIONARY DOMINANCE! This is where innovation meets PURE POWER! ❄️⚔️🚀",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
            else:
                return {
                    "message": "Ethereum (ETH) is a decentralized blockchain platform that enables smart contracts and decentralized applications (DApps). Created by Vitalik Buterin in 2015, Ethereum features: 🔧 Smart contracts (self-executing contracts), 🏗️ Platform for thousands of DApps, 💰 Native currency (Ether/ETH), ⚡ Proof-of-Stake consensus (after The Merge), 🔥 Deflationary tokenomics through EIP-1559. Ethereum is often called the 'world computer' and hosts the majority of DeFi protocols, NFTs, and Web3 applications!",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
        
        # General crypto questions
        if any(word in user_lower for word in ['crypto', 'cryptocurrency', 'what is crypto']):
            if self.personality_mode == "subzero":
                return {
                    "message": "🧊 CRYPTOCURRENCY IS DIGITAL WARFARE! Decentralized money that CRUSHES traditional banking! Built on unbreakable blockchain technology, crypto offers TOTAL FREEDOM from government control! 💀 No central authority can stop the crypto revolution! Bitcoin leads the charge, Ethereum powers innovation, and thousands of altcoins follow! This is the future of money - COLD, CALCULATED, and UNSTOPPABLE! Join the revolution or get left in the ice! ❄️⚔️💎",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
            else:
                return {
                    "message": "Cryptocurrency is digital money secured by cryptography and operating on decentralized networks, typically using blockchain technology. Key features include: 🔐 Cryptographic security (nearly impossible to counterfeit), 🌐 Decentralization (no central authority), 📊 Transparency (public transaction ledgers), 🚀 Global accessibility (24/7 trading), 💸 Peer-to-peer transactions. Since Bitcoin's creation in 2009, thousands of cryptocurrencies have emerged, each serving different purposes from payments to smart contracts to digital collectibles!",
                    "personality": self.personality_mode,
                    "type": "crypto_info",
                    "confidence": 0.9
                }
        
        return None
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        info = {
            "personality_mode": self.personality_mode,
            "trainers_available": {
                "normal": self.normal_trainer is not None,
                "subzero": self.subzero_trainer is not None
            },
            "news_service": self.news_service is not None,
            "autonomous_training": False,  # Disabled for stability
            "conversation_count": len(self.conversation_history)
        }
        
        # Normal trainer info
        if self.normal_trainer:
            if hasattr(self.normal_trainer, 'get_training_stats'):
                normal_stats = self.normal_trainer.get_training_stats()
                info["normal_training"] = {
                    "type": "Enhanced training",
                    "features": normal_stats.get('features', ["Dataset-driven responses", "Crypto expertise"])
                }
        
        # Sub-Zero trainer info
        if self.subzero_trainer:
            if hasattr(self.subzero_trainer, 'get_training_stats'):
                subzero_stats = self.subzero_trainer.get_training_stats()
                info["subzero_training"] = {
                    "type": "Pure Sub-Zero training",
                    "features": subzero_stats.get('features', ["Authentic Sub-Zero personality", "Crypto expertise"])
                }
        
        return info
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_learning_statistics(self) -> Dict:
        """Get learning statistics"""
        return {
            'continuous_learning_enabled': False,
            'autonomous_training_enabled': self.auto_training_enabled,
            'total_conversations': self.learning_stats['total_conversations'],
            'successful_responses': self.learning_stats['successful_responses'],
            'accuracy_rate': f"{self.learning_stats['accuracy_rate']:.1f}%",
            'personality_mode': self.personality_mode,
            'features': [
                "Dual personality system",
                "Enhanced normal trainer",
                "Pure Sub-Zero personality",
                "Fixed strip() error handling"
            ]
        }

# Test function
def test_chatbot():
    """Test the chatbot to ensure it works"""
    print("🧪 Testing Fixed Chatbot...")
    
    bot = ImprovedDualPersonalityChatbot()
    
    # Test normal mode
    print("\n1. Testing normal mode...")
    response1 = bot.get_response("hi")
    print(f"Response: {response1}")
    
    # Test subzero mode
    print("\n2. Testing subzero mode...")
    bot.switch_personality('subzero')
    response2 = bot.get_response("hi")
    print(f"Response: {response2}")
    
    print("\n✅ Chatbot test completed!")

if __name__ == "__main__":
    test_chatbot()
