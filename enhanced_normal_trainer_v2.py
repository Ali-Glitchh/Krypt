#!/usr/bin/env python3
"""
Enhanced Normal Conversation Trainer with better crypto knowledge and DailyDialog dataset support
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
                'description': "Crypto trading involves buying and selling cryptocurrencies to profit from price movements.",
                'key_points': ["Technical analysis", "Risk management", "Dollar-cost averaging", "Market timing"]
            },
            'security': {
                'description': "Crypto security involves protecting your digital assets from theft, scams, and technical failures.",
                'key_points': ["Hardware wallets", "Seed phrases", "2FA", "Cold storage"]
            }
        }
    
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
            # Add natural crypto knowledge to response
            crypto_info = self.crypto_knowledge[detected_topic]
            enhanced = f"{original_response} {crypto_info['description']}"
            return enhanced
        
        return original_response
    
    def add_crypto_conversations(self):
        """Add specific crypto conversation pairs for better coverage"""
        crypto_conversations = [
            {
                "user": "What do you think about cryptocurrency?",
                "bot": "I find cryptocurrency fascinating! It represents a new way of thinking about money and financial systems. The technology behind it, like blockchain, has potential applications beyond just digital currency."
            },
            {
                "user": "Should I invest in Bitcoin?",
                "bot": "That's a personal decision that depends on your risk tolerance and financial situation. Bitcoin can be quite volatile, so it's important to only invest what you can afford to lose and do your own research first."
            },
            {
                "user": "How does blockchain work?",
                "bot": "Blockchain is like a digital ledger that's shared across many computers. Each 'block' contains transaction data, and they're linked together in a 'chain' that's very difficult to alter. This creates transparency and security without needing a central authority."
            },
            {
                "user": "What's the difference between Bitcoin and Ethereum?",
                "bot": "Great question! Bitcoin is primarily digital money - like digital gold. Ethereum is more like a platform where people can build applications and smart contracts. Both use blockchain technology but serve different purposes."
            },
            {
                "user": "Is crypto safe?",
                "bot": "Crypto security depends on how you handle it. The blockchain technology itself is very secure, but you need to protect your private keys and use reputable exchanges. Think of it like digital cash - if you lose it, it's gone."
            }
        ]
        
        for conv in crypto_conversations:
            self.conversations.append(conv)
            self.user_inputs.append(conv["user"])
            self.bot_responses.append(conv["bot"])
    
    def build_similarity_model(self):
        """Build TF-IDF vectorizer for finding similar inputs"""
        if not self.user_inputs:
            return
        
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        self.input_vectors = self.vectorizer.fit_transform(self.user_inputs)
        print(f"✅ Built similarity model with {len(self.user_inputs)} training examples")
    
    def find_best_response(self, user_input: str) -> str:
        """Find the best response using similarity matching"""
        if not self.vectorizer or not self.input_vectors.size:
            return "I'm still learning! Could you tell me more?"
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Vectorize user input
        user_vector = self.vectorizer.transform([user_input])
        
        # Calculate similarities
        similarities = cosine_similarity(user_vector, self.input_vectors).flatten()
        
        # Get top matches
        top_indices = np.argsort(similarities)[-5:][::-1]
        
        # Select best response with some randomness
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                response = self.bot_responses[idx]
                
                # Add some variation to avoid repetitive responses
                if random.random() < 0.3:  # 30% chance to add variation
                    response = self.add_response_variation(response)
                
                # Cache the response
                self.response_cache[cache_key] = response
                return response
        
        # Fallback for low similarity
        return self.generate_fallback_response(user_input)
    
    def add_response_variation(self, response: str) -> str:
        """Add slight variations to responses to make them feel more natural"""
        variations = {
            "That's": ["That's", "That is", "This is"],
            "I think": ["I think", "I believe", "In my opinion"],
            "Great": ["Great", "Excellent", "Awesome", "Nice"],
            "Yes": ["Yes", "Absolutely", "Definitely", "For sure"],
            "No": ["No", "Not really", "I don't think so"],
        }
        
        for original, replacements in variations.items():
            if original in response:
                replacement = random.choice(replacements)
                response = response.replace(original, replacement, 1)
                break
        
        return response
    
    def generate_fallback_response(self, user_input: str) -> str:
        """Generate appropriate fallback responses"""
        user_lower = user_input.lower()
        
        # Check for question words
        if any(word in user_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            return "That's an interesting question! I'd love to know more about what specifically interests you about that topic."
        
        # Check for greetings
        if any(word in user_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
            return random.choice([
                "Hello! How are you doing today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to chat with you."
            ])
        
        # Check for crypto-related terms
        crypto_terms = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'defi', 'trading']
        if any(term in user_lower for term in crypto_terms):
            return "Cryptocurrency is such a fascinating topic! What aspect interests you most - the technology, investing, or something else?"
        
        # Default responses
        return random.choice([
            "That's interesting! Can you tell me more about that?",
            "I'd love to hear your thoughts on that.",
            "What made you think about that?",
            "That sounds intriguing. Could you elaborate?",
            "I'm curious to know more about your perspective on this."
        ])
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about the loaded conversations"""
        return {
            "total_conversations": len(self.conversations),
            "avg_user_length": np.mean([len(inp) for inp in self.user_inputs]) if self.user_inputs else 0,
            "avg_bot_length": np.mean([len(resp) for resp in self.bot_responses]) if self.bot_responses else 0,
            "crypto_knowledge_topics": len(self.crypto_knowledge),
            "cache_size": len(self.response_cache)
        }

def test_enhanced_normal_trainer():
    """Test the enhanced normal trainer"""
    print("🤖 Testing Enhanced Normal Trainer")
    print("=" * 50)
    
    trainer = EnhancedNormalTrainer()
    
    # Test conversation stats
    stats = trainer.get_conversation_stats()
    print(f"📊 Conversation Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Test various inputs
    test_inputs = [
        "Hi there!",
        "What do you think about Bitcoin?",
        "How does blockchain work?",
        "Should I invest in cryptocurrency?",
        "What's your favorite movie?",
        "How's the weather today?",
        "Tell me about Ethereum",
        "Is crypto trading risky?",
        "What are your hobbies?",
        "Goodbye!"
    ]
    
    print("💬 Testing Conversations:")
    for inp in test_inputs:
        response = trainer.find_best_response(inp)
        print(f"User: {inp}")
        print(f"Bot:  {response}")
        print()

if __name__ == "__main__":
    test_enhanced_normal_trainer()
