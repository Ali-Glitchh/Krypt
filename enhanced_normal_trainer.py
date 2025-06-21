#!/usr/bin/env python3
"""
Enhanced Normal Conversation Trainer with better crypto knowledge
"""

import json
import re
import random
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EnhancedNormalTrainer:
    def __init__(self, dataset_file: str = 'normal_conversation_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_inputs = []
        self.bot_responses = []
        self.vectorizer = None
        self.input_vectors = None
        self.response_cache = {}
        
        # Enhanced crypto knowledge base
        self.crypto_knowledge = self._build_crypto_knowledge()
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
    
    def _build_crypto_knowledge(self) -> Dict:
        """Build comprehensive crypto knowledge base for normal personality"""
        return {
            'bitcoin': {
                'description': "Bitcoin is the world's first cryptocurrency, created by Satoshi Nakamoto in 2009. It's digital money that operates without central control.",
                'key_points': ["Decentralized", "Limited supply (21M)", "Store of value", "Digital gold"]
            },
            'ethereum': {
                'description': "Ethereum is a blockchain platform that enables smart contracts and decentralized applications (dApps).",
                'key_points': ["Smart contracts", "DeFi ecosystem", "NFT platform", "Programmable money"]
            },
            'blockchain': {
                'description': "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks.",
                'key_points': ["Transparency", "Immutability", "Decentralization", "Security"]
            },
            'defi': {
                'description': "DeFi (Decentralized Finance) refers to financial services built on blockchain technology without traditional intermediaries.",
                'key_points': ["No banks needed", "Yield farming", "Liquidity pools", "Smart contracts"]
            },
            'trading': {
                'description': "Crypto trading involves buying and selling digital assets on exchanges to profit from price movements.",
                'key_points': ["Technical analysis", "Risk management", "Dollar-cost averaging", "HODL strategy"]
            },
            'security': {
                'description': "Crypto security involves protecting your digital assets from theft, scams, and technical failures.",
                'key_points': ["Hardware wallets", "Seed phrases", "2FA", "Cold storage"]
            }        }
    
    def load_dataset(self):
        """Load and enhance the conversation dataset"""
        try:
            # Check if it's a JSON file
            if self.dataset_file.endswith('.json'):
                self.load_json_dataset()
            else:
                self.load_text_dataset()
                
            # Add specific crypto conversation pairs
            self.add_crypto_conversations()
            
            print(f"✅ Loaded {len(self.conversations)} enhanced normal conversation pairs")
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.conversations = []
    
    def load_json_dataset(self):
        """Load JSON format dataset (DailyDialog format)"""
        with open(self.dataset_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            user_msg = item.get('user', '')
            bot_response = item.get('bot', '')
            
            if user_msg and bot_response:
                # Create enhanced response
                enhanced_response = self.create_enhanced_response(user_msg, bot_response)
                
                self.conversations.append({
                    "user": user_msg,
                    "bot": enhanced_response
                })
                
                self.user_inputs.append(user_msg)
                self.bot_responses.append(enhanced_response)
    
    def load_text_dataset(self):
        """Load text format dataset (original human_chat.txt format)"""
        with open(self.dataset_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse human chat format and create enhanced responses
        lines = content.strip().split('\n')
        current_conversation = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Human 1:') or line.startswith('Human 2:'):
                speaker = line.split(':', 1)[0]
                message = line.split(':', 1)[1].strip()
                current_conversation.append((speaker, message))
                
                if len(current_conversation) >= 2:
                    user_msg = current_conversation[-2][1]
                    original_response = current_conversation[-1][1]
                    
                    # Create enhanced response
                    enhanced_response = self.create_enhanced_response(user_msg, original_response)
                    
                    self.conversations.append({
                        "user": user_msg,
                        "bot": enhanced_response
                    })
                      self.user_inputs.append(user_msg)
                    self.bot_responses.append(enhanced_response)
    
    def create_enhanced_response(self, user_input: str, original_response: str) -> str:
        """Create enhanced responses that maintain natural conversation but add crypto knowledge"""
        user_lower = user_input.lower()
        
        # Check for crypto-related content
        crypto_keywords = {
            'bitcoin': ['bitcoin', 'btc'],
            'ethereum': ['ethereum', 'eth'],
            'blockchain': ['blockchain', 'block chain'],
            'trading': ['trade', 'trading', 'buy', 'sell', 'invest'],
            'defi': ['defi', 'decentralized finance'],
            'security': ['secure', 'safety', 'protect', 'wallet']
        }
        
        detected_topic = None
        for topic, keywords in crypto_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_topic = topic
                break
        
        if detected_topic and detected_topic in self.crypto_knowledge:
            # Enhance response with crypto knowledge while keeping natural tone
            knowledge = self.crypto_knowledge[detected_topic]
            
            if len(original_response) < 50:  # Short original response
                return f"{knowledge['description']} {random.choice(knowledge['key_points'])} are particularly important to understand."
            else:
                # Add crypto context to longer responses
                return f"{original_response} Speaking of which, {knowledge['description']}"
        
        return original_response
    
    def add_crypto_conversations(self):
        """Add specific crypto conversation pairs for better coverage"""
        crypto_pairs = [
            {
                "user": "What is cryptocurrency?",
                "bot": "Cryptocurrency is digital money that uses cryptography for security. Unlike traditional money, it's decentralized and operates on blockchain technology. Bitcoin was the first, but now there are thousands of different cryptocurrencies."
            },
            {
                "user": "How do I start with crypto?",
                "bot": "Starting with crypto can be exciting! First, educate yourself about blockchain technology and different cryptocurrencies. Then choose a reputable exchange, start small, and consider dollar-cost averaging. Always use secure storage methods!"
            },
            {
                "user": "Is crypto safe?",
                "bot": "Crypto can be safe when proper security measures are used. Use hardware wallets, enable two-factor authentication, never share private keys, and be aware of scams. The technology itself is secure, but user practices matter most."
            },
            {
                "user": "Should I invest in crypto?",
                "bot": "Investment decisions depend on your financial situation and risk tolerance. Crypto is volatile and high-risk. Only invest what you can afford to lose, do thorough research, and consider consulting financial advisors."
            },
            {
                "user": "What's the difference between Bitcoin and Ethereum?",
                "bot": "Bitcoin is primarily digital money and a store of value, like digital gold. Ethereum is a platform for smart contracts and decentralized applications. Both are valuable but serve different purposes in the crypto ecosystem."
            },
            {
                "user": "What are the risks of crypto?",
                "bot": "Crypto risks include price volatility, regulatory changes, security breaches, scams, and technical issues. The market is highly speculative and can change rapidly. Always research thoroughly and invest responsibly."
            }
        ]
        
        for pair in crypto_pairs:
            self.conversations.append(pair)
            self.user_inputs.append(pair['user'])
            self.bot_responses.append(pair['bot'])
    
    def build_similarity_model(self):
        """Build TF-IDF model for finding similar inputs"""
        if not self.user_inputs:
            return
        
        try:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=3000,
                lowercase=True,
                ngram_range=(1, 2)
            )
            
            self.input_vectors = self.vectorizer.fit_transform(self.user_inputs)
            print("✅ Built enhanced normal conversation model")
            
        except Exception as e:
            print(f"⚠️ Could not build similarity model: {e}")
    
    def get_response(self, user_input: str) -> str:
        """Get enhanced normal personality response"""
        if not user_input.strip():
            return "I'm here to chat! What would you like to talk about?"
        
        # First check for direct crypto knowledge
        crypto_response = self.get_crypto_response(user_input)
        if crypto_response:
            return crypto_response
        
        # Then use similarity matching
        if self.vectorizer and self.input_vectors is not None:
            try:
                user_vector = self.vectorizer.transform([user_input])
                similarities = cosine_similarity(user_vector, self.input_vectors).flatten()
                
                best_match_idx = np.argmax(similarities)
                best_similarity = similarities[best_match_idx]
                
                if best_similarity >= 0.2:
                    return self.bot_responses[best_match_idx]
            except Exception as e:
                print(f"⚠️ Error in similarity matching: {e}")
        
        # Fallback to general responses
        return self.get_fallback_response(user_input)
    
    def get_crypto_response(self, user_input: str) -> Optional[str]:
        """Get specific crypto-related responses"""
        user_lower = user_input.lower()
        
        # Bitcoin responses
        if any(word in user_lower for word in ['bitcoin', 'btc']):
            return random.choice([
                "Bitcoin is fascinating! It's the first and most well-known cryptocurrency. What specific aspect interests you?",
                "Bitcoin has really changed how we think about money. Are you curious about the technology or the investment side?",
                "I find Bitcoin's decentralized nature really interesting. It operates without any central authority!"
            ])
        
        # Ethereum responses
        if any(word in user_lower for word in ['ethereum', 'eth']):
            return random.choice([
                "Ethereum is amazing because it's not just currency - it's a whole platform for building applications!",
                "I love how Ethereum enables smart contracts. It's like programmable money!",
                "Ethereum has created so many opportunities with DeFi and NFTs. What draws you to it?"
            ])
        
        # General crypto responses
        if any(word in user_lower for word in ['crypto', 'cryptocurrency', 'blockchain']):
            return random.choice([
                "Cryptocurrency is such an exciting field! The technology behind it is revolutionary.",
                "I find the crypto space really interesting. There's always something new happening!",
                "Blockchain technology has so many potential applications beyond just currency.",
                "The crypto market is definitely volatile, but the underlying technology is fascinating."
            ])
        
        # Trading/Investment responses
        if any(word in user_lower for word in ['invest', 'trading', 'buy crypto']):
            return random.choice([
                "Investment in crypto requires careful research. What's your risk tolerance like?",
                "Trading can be exciting but risky. Have you considered a long-term investment approach?",
                "I always recommend starting small and learning as you go. Education is key in crypto!",
                "The crypto market is very volatile. It's important to only invest what you can afford to lose."
            ])
        
        return None
    
    def get_fallback_response(self, user_input: str) -> str:
        """Generate fallback responses for normal personality"""
        user_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice([
                "Hello! Great to meet you! What's on your mind today?",
                "Hi there! I'm excited to chat. What would you like to discuss?",
                "Hey! Nice to meet you. I love talking about all sorts of topics, especially crypto!",
                "Greetings! I'm here and ready to chat about whatever interests you."
            ])
        
        # How are you responses
        if any(phrase in user_lower for phrase in ['how are you', 'how you doing', 'how have you been']):
            return random.choice([
                "I'm doing great, thanks for asking! I've been learning a lot about crypto lately. How about you?",
                "I'm wonderful! Always excited to chat about interesting topics. What's new with you?",
                "Doing well! I love having conversations about technology and finance. How are you doing?",
                "I'm fantastic! Been following some interesting developments in the crypto space. How about yourself?"
            ])
        
        # Question responses
        if '?' in user_input:
            return random.choice([
                "That's a great question! I'd love to help you think through that.",
                "Interesting question! What's your take on it so far?",
                "I'm curious about that too! What made you think of this?",
                "Good question! Let me think about that with you."
            ])
        
        # Default responses
        return random.choice([
            "That's really interesting! Tell me more about your thoughts on that.",
            "I'd love to hear more about what you're thinking. Can you elaborate?",
            "That sounds fascinating! What's your perspective on it?",
            "Interesting point! I'm curious to hear more about your experience with that.",
            "That's a good topic! What specifically interests you about it?"
        ])
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about the loaded conversations"""
        if not self.conversations:
            return {"total_conversations": 0}
        
        crypto_count = sum(1 for conv in self.conversations 
                         if any(word in conv['user'].lower() 
                              for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'investment']))
        
        greeting_count = sum(1 for conv in self.conversations 
                           if any(word in conv['user'].lower() 
                                for word in ['hello', 'hi', 'hey', 'greetings']))
        
        question_count = sum(1 for conv in self.conversations 
                           if '?' in conv['user'])
        
        return {
            "total_conversations": len(self.conversations),
            "crypto_conversations": crypto_count,
            "greeting_conversations": greeting_count,
            "question_conversations": question_count,
            "average_response_length": np.mean([len(conv['bot']) for conv in self.conversations]) if self.conversations else 0
        }

# Test the enhanced trainer
if __name__ == "__main__":
    trainer = EnhancedNormalTrainer()
    
    stats = trainer.get_conversation_stats()
    print("\n📊 Enhanced Normal Trainer Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    test_inputs = [
        "Hello!",
        "What is Bitcoin?",
        "How do I invest in crypto?",
        "Is Ethereum better than Bitcoin?",
        "How are you doing?",
        "What do you think about blockchain?"
    ]
    
    print("\n🧪 Testing Enhanced Normal Responses:")
    for test_input in test_inputs:
        response = trainer.get_response(test_input)
        print(f"\nUser: {test_input}")
        print(f"Bot: {response}")
