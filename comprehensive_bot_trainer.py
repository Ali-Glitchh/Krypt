#!/usr/bin/env python3
"""
Comprehensive Bot Training and Testing Script
"""

import json
import re
import random
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NormalConversationTrainer:
    def __init__(self, dataset_file: str = 'human_chat.txt'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_inputs = []
        self.bot_responses = []
        self.vectorizer = None
        self.input_vectors = None
        self.response_cache = {}
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
    
    def load_dataset(self):
        """Load the human chat dataset and convert to conversation pairs"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse human chat format
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
                    
                    # Create conversation pairs when we have exchanges
                    if len(current_conversation) >= 2:
                        # Take the last two messages as a pair
                        user_msg = current_conversation[-2][1]
                        bot_response = current_conversation[-1][1]
                        
                        # Add natural conversation responses with crypto knowledge
                        enhanced_response = self.enhance_with_crypto_knowledge(user_msg, bot_response)
                        
                        self.conversations.append({
                            "user": user_msg,
                            "bot": enhanced_response
                        })
                        
                        self.user_inputs.append(user_msg)
                        self.bot_responses.append(enhanced_response)
            
            print(f"✅ Loaded {len(self.conversations)} normal conversation pairs")
            
        except FileNotFoundError:
            print(f"❌ Dataset file {self.dataset_file} not found!")
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
    
    def enhance_with_crypto_knowledge(self, user_input: str, original_response: str) -> str:
        """Enhance responses with crypto knowledge when relevant"""
        user_lower = user_input.lower()
        
        # Check if crypto-related
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'investment', 'money', 'trading', 'finance']
        
        if any(keyword in user_lower for keyword in crypto_keywords):
            # Add crypto knowledge to the response
            crypto_additions = [
                " Speaking of investments, cryptocurrency has been quite revolutionary in the financial space.",
                " You know, this reminds me of how blockchain technology is changing many industries.",
                " It's interesting how digital assets like Bitcoin have created new opportunities.",
                " The crypto market has definitely brought new perspectives to traditional finance.",
                " Have you explored any cryptocurrency investments? The space is quite fascinating."
            ]
            
            if not any(keyword in original_response.lower() for keyword in crypto_keywords):
                original_response += random.choice(crypto_additions)
        
        return original_response
    
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
            print("✅ Built normal conversation similarity model")
            
        except Exception as e:
            print(f"⚠️ Could not build similarity model: {e}")
    
    def get_response(self, user_input: str) -> str:
        """Get normal personality response"""
        if not self.vectorizer or self.input_vectors is None:
            return self.get_fallback_response(user_input)
        
        # Check cache
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Find similar input
            user_vector = self.vectorizer.transform([user_input])
            similarities = cosine_similarity(user_vector, self.input_vectors).flatten()
            
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity >= 0.2:
                response = self.bot_responses[best_match_idx]
                self.response_cache[cache_key] = response
                return response
            else:
                return self.get_fallback_response(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in normal conversation matching: {e}")
            return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input: str) -> str:
        """Generate fallback responses for normal personality"""
        user_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice([
                "Hello! Great to meet you! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to chat with you. What would you like to discuss?",
                "Greetings! I'm here to help with crypto insights and general conversation."
            ])
        
        # Crypto responses
        if any(word in user_lower for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']):
            return random.choice([
                "Cryptocurrency is a fascinating topic! What specific aspect interests you?",
                "I'd love to discuss crypto with you. Are you interested in trading, technology, or investment?",
                "The blockchain space is evolving rapidly. What would you like to know?",
                "Crypto markets are always interesting to analyze. What's your question?"
            ])
        
        # Investment responses
        if any(word in user_lower for word in ['invest', 'investment', 'money', 'financial']):
            return random.choice([
                "Investment decisions are important! I can share some insights, but always do your own research.",
                "Financial planning is crucial. What specific area are you looking at?",
                "Investment strategies vary by person. What's your risk tolerance and goals?",
                "I can provide some general guidance, but please consult with financial professionals for advice."
            ])
        
        # Default responses
        return random.choice([
            "That's an interesting question! Can you tell me more about what you're thinking?",
            "I'd like to help you with that. Could you provide a bit more context?",
            "Interesting perspective! What specifically would you like to explore?",
            "Tell me more about that - I'm curious to hear your thoughts.",
            "That's a good point. What's your take on it?"
        ])
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about the loaded conversations"""
        if not self.conversations:
            return {"total_conversations": 0}
        
        # Count different types of conversations
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

class BotTrainingManager:
    def __init__(self):
        self.normal_trainer = None
        self.subzero_trainer = None
        
        # Initialize trainers
        self.initialize_trainers()
    
    def initialize_trainers(self):
        """Initialize both personality trainers"""
        print("🤖 Initializing Bot Training Manager...")
        
        # Normal personality trainer
        try:
            self.normal_trainer = NormalConversationTrainer()
            print("✅ Normal personality trainer loaded")
        except Exception as e:
            print(f"❌ Failed to load normal trainer: {e}")
        
        # Sub-Zero personality trainer
        try:
            from advanced_subzero_trainer_fixed import AdvancedSubZeroTrainer
            self.subzero_trainer = AdvancedSubZeroTrainer()
            print("✅ Sub-Zero personality trainer loaded")
        except Exception as e:
            print(f"❌ Failed to load Sub-Zero trainer: {e}")
    
    def train_models(self):
        """Train both personality models"""
        print("\n🔥 Starting Bot Training Process...")
        
        if self.normal_trainer:
            print("\n📚 Training Normal Personality...")
            normal_stats = self.normal_trainer.get_conversation_stats() if hasattr(self.normal_trainer, 'get_conversation_stats') else {}
            print(f"   Normal conversations: {len(self.normal_trainer.conversations)}")
            
        if self.subzero_trainer:
            print("\n❄️ Training Sub-Zero Personality...")
            subzero_stats = self.subzero_trainer.get_conversation_stats()
            print(f"   Sub-Zero conversations: {subzero_stats.get('total_conversations', 0)}")
            print(f"   Average response length: {subzero_stats.get('average_response_length', 0):.1f} characters")
        
        print("\n✅ Bot training completed!")
    
    def test_personalities(self):
        """Test both personalities with various inputs"""
        print("\n🧪 Testing Both Personalities...")
        
        test_cases = [
            "Hello!",
            "What is Bitcoin?",
            "How do I start investing?",
            "Tell me about cryptocurrency security",
            "What's your favorite crypto?",
            "Should I buy crypto now?",
            "What is DeFi?",
            "How are you doing?",
            "What do you think about the market?"
        ]
        
        for test_input in test_cases:
            print(f"\n{'='*60}")
            print(f"Input: {test_input}")
            print("-" * 40)
            
            # Normal personality response
            if self.normal_trainer:
                normal_response = self.normal_trainer.get_response(test_input)
                print(f"Normal: {normal_response}")
            
            # Sub-Zero personality response
            if self.subzero_trainer:
                subzero_response = self.subzero_trainer.get_response(test_input)
                print(f"Sub-Zero: {subzero_response}")
        
        print(f"\n{'='*60}")
        print("🎉 Personality testing completed!")
    
    def get_response(self, user_input: str, personality: str = "normal") -> str:
        """Get response from specified personality"""
        if personality.lower() in ['subzero', 'sub-zero', 'sub zero']:
            if self.subzero_trainer:
                return self.subzero_trainer.get_response(user_input)
            else:
                return "❄️ Sub-Zero personality not available!"
        else:
            if self.normal_trainer:
                return self.normal_trainer.get_response(user_input)
            else:
                return "Normal personality not available!"

# Main training execution
if __name__ == "__main__":
    print("🚀 Starting Comprehensive Bot Training...")
    
    # Initialize training manager
    manager = BotTrainingManager()
    
    # Train the models
    manager.train_models()
    
    # Test personalities
    manager.test_personalities()
    
    # Interactive testing
    print("\n💬 Interactive Testing (type 'quit' to exit, 'switch' to change personality)")
    current_personality = "normal"
    
    while True:
        user_input = input(f"\n[{current_personality.upper()}] You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'switch':
            current_personality = "subzero" if current_personality == "normal" else "normal"
            print(f"Switched to {current_personality.upper()} personality")
            continue
        elif not user_input:
            continue
        
        response = manager.get_response(user_input, current_personality)
        print(f"Bot: {response}")
    
    print("\n🎯 Training and testing session completed!")
