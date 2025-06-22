#!/usr/bin/env python3
"""
Enhanced Pure Dataset-Trained Normal Trainer - Crypto-focused responses
"""

import json
import re
import random
import math
from typing import Dict, List, Optional
import numpy as np

class PureNormalTrainer:
    def __init__(self, dataset_file: str = 'crypto_normal_dataset.json'):
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
        """Load the conversation dataset"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data:
                user_msg = item.get('user', '')
                bot_response = item.get('bot', '')
                
                if user_msg and bot_response:
                    self.conversations.append({
                        "user": user_msg,
                        "bot": bot_response
                    })
                    
                    self.user_inputs.append(user_msg)
                    self.bot_responses.append(bot_response)
                    
            print(f"✅ Loaded {len(self.conversations)} crypto-focused conversation pairs")
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.conversations = []
            # Fallback basic responses
            self.user_inputs = ["hello", "what is bitcoin", "how are you"]
            self.bot_responses = [
                "Hello! I'm your crypto assistant.",
                "Bitcoin is the first cryptocurrency.",
                "I'm doing great! Ready to talk crypto?"
            ]
      def build_similarity_model(self):
        """Build simplified similarity model without scikit-learn"""
        if not self.user_inputs:
            print("❌ No training data available for similarity model")
            return
        
        try:
            # Use simple word-based similarity instead of TF-IDF
            self.word_vectors = []
            self.all_words = set()
            
            # Build vocabulary from all inputs
            for input_text in self.user_inputs:
                words = self.tokenize_text(input_text.lower())
                self.all_words.update(words)
            
            self.all_words = sorted(list(self.all_words))
            self.vocab_size = len(self.all_words)
            
            # Create word vectors for each input
            for input_text in self.user_inputs:
                vector = self.text_to_vector(input_text.lower())
                self.word_vectors.append(vector)
            
            print(f"✅ Built similarity model with {len(self.word_vectors)} conversations")
            print(f"📊 Vocabulary size: {self.vocab_size}")
            
        except Exception as e:
            print(f"❌ Error building similarity model: {e}")
            self.word_vectors = None
            self.vocab_size = 0

    def find_best_response(self, user_input: str, threshold: float = 0.1) -> str:
        """Find the best response using enhanced similarity matching"""
        if not self.user_inputs or not self.vectorizer:
            return "I'm still learning about cryptocurrency! Please ask me about Bitcoin, Ethereum, or blockchain."
        
        user_input = user_input.strip()
        if not user_input:
            return "I'm here to help with your crypto questions!"
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Enhanced preprocessing for better matching
            processed_input = self.preprocess_input(user_input)
            
            # Try keyword matching first for common patterns
            keyword_response = self.try_keyword_matching(user_input.lower())
            if keyword_response:
                self.response_cache[cache_key] = keyword_response
                return keyword_response
            
            # Vectorize user input
            user_vector = self.vectorizer.transform([processed_input])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, self.input_vectors).flatten()
            
            # Get top matches above threshold
            valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) == 0:
                # Lower threshold progressively
                for lower_threshold in [0.05, 0.02, 0.01]:
                    valid_indices = np.where(similarities >= lower_threshold)[0]
                    if len(valid_indices) > 0:
                        break
            
            if len(valid_indices) > 0:
                # Sort by similarity and get top matches
                sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
                
                # Select from top 3 matches for better quality
                top_count = min(3, len(sorted_indices))
                selected_idx = sorted_indices[random.randint(0, top_count-1)]
                
                response = self.bot_responses[selected_idx]
                
                # Cache the response
                self.response_cache[cache_key] = response
                return response
            else:
                # Absolutely no matches - use fallback
                return self.get_fallback_response(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in similarity matching: {e}")
            return self.get_fallback_response(user_input)
    
    def preprocess_input(self, user_input: str) -> str:
        """Enhanced preprocessing for better matching"""
        # Convert to lowercase
        text = user_input.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Expand common abbreviations
        expansions = {
            'btc': 'bitcoin',
            'eth': 'ethereum',
            'crypto': 'cryptocurrency',
            'defi': 'decentralized finance',
            'nft': 'non fungible token',
            'dao': 'decentralized autonomous organization'
        }
        
        for abbr, full in expansions.items():
            text = text.replace(abbr, full)
        
        return text
    
    def try_keyword_matching(self, user_input: str) -> Optional[str]:
        """Try to match based on keywords for common patterns"""
        user_input = user_input.lower()
        
        # Greeting patterns
        if any(greeting in user_input for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            greetings = [conv['bot'] for conv in self.conversations if any(g in conv['user'].lower() for g in ['hello', 'hi', 'hey', 'good morning'])]
            if greetings:
                return random.choice(greetings)
        
        # Name patterns
        if any(name_word in user_input for name_word in ['name', 'who are you', 'what are you']):
            name_responses = [conv['bot'] for conv in self.conversations if any(n in conv['user'].lower() for n in ['name', 'who', 'what'])]
            if name_responses:
                return random.choice(name_responses)
        
        # Goodbye patterns
        if any(goodbye in user_input for goodbye in ['goodbye', 'bye', 'see you', 'farewell', 'thanks', 'thank you']):
            goodbyes = [conv['bot'] for conv in self.conversations if any(g in conv['user'].lower() for g in ['goodbye', 'bye', 'thanks', 'thank you'])]
            if goodbyes:
                return random.choice(goodbyes)
        
        return None
    
    def get_fallback_response(self, user_input: str) -> str:
        """Get a contextual fallback response"""
        user_input = user_input.lower()
        
        # Crypto-related fallbacks
        if any(crypto_word in user_input for crypto_word in ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'trading', 'invest']):
            crypto_responses = [
                "That's an interesting crypto question! I'm always learning more about the cryptocurrency ecosystem.",
                "Cryptocurrency is a fascinating topic! While I might not have that specific information, I'm happy to discuss other crypto concepts.",
                "I love talking about crypto! While I don't have that exact answer, feel free to ask me about Bitcoin, Ethereum, or other cryptocurrencies."
            ]
            return random.choice(crypto_responses)
        
        # General fallbacks
        general_responses = [
            "I'm here to help with your cryptocurrency questions! What would you like to know about crypto?",
            "That's an interesting question! I specialize in cryptocurrency topics - feel free to ask me about Bitcoin, blockchain, or DeFi!",
            "I'm still learning! Could you ask me something about cryptocurrency or blockchain technology?"
        ]
        return random.choice(general_responses)
    
    def get_training_stats(self) -> Dict:
        """Get statistics about the training data"""
        if not self.conversations:
            return {}
        
        total_conversations = len(self.conversations)
        avg_user_length = np.mean([len(conv['user']) for conv in self.conversations])
        avg_bot_length = np.mean([len(conv['bot']) for conv in self.conversations])
        
        return {
            'total_conversations': total_conversations,
            'avg_user_length': avg_user_length,
            'avg_bot_length': avg_bot_length,
            'cache_size': len(self.response_cache),
            'features': ['crypto_focused', 'enhanced_matching', 'keyword_recognition']
        }

def test_pure_trainer():
    """Test the enhanced pure trainer"""
    print("🧪 Testing Enhanced Pure Normal Trainer")
    print("=" * 50)
    
    trainer = PureNormalTrainer()
    
    # Show stats
    stats = trainer.get_training_stats()
    print(f"📊 Training Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test crypto-focused queries
    test_queries = [
        "Hello",
        "Hi there",
        "What's your name?",
        "What is Bitcoin?",
        "How do I buy crypto?",
        "Is crypto safe?",
        "What is Ethereum?",
        "What is DeFi?",
        "How are you doing?",
        "Should I invest in crypto?",
        "What is blockchain?",
        "Thanks for your help",
        "Goodbye!"
    ]
    
    print(f"\n💬 Testing Crypto-Focused Conversations:")
    for query in test_queries:
        response = trainer.find_best_response(query)
        print(f"User: {query}")
        print(f"Bot: {response}")
        print()

if __name__ == "__main__":
    test_pure_trainer()
