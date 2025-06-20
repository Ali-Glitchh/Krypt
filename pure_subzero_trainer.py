#!/usr/bin/env python3
"""
Pure Dataset-Trained Sub-Zero Trainer - Only uses training data, no hardcoded responses
"""

import json
import random
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PureSubZeroTrainer:
    def __init__(self, dataset_file: str = 'sub_zero_crypto_comprehensive_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_questions = []
        self.sub_zero_responses = []
        self.vectorizer = None
        self.question_vectors = None
        self.response_cache = {}
        
        # Load the dataset and build the model
        self.load_dataset()
        self.build_similarity_model()
    
    def load_dataset(self):
        """Load the Sub-Zero conversation dataset"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                self.conversations = json.load(f)
            
            # Extract questions and responses
            for conv in self.conversations:
                user_question = conv.get('user', '')
                sub_zero_response = conv.get('sub_zero', '')
                
                if user_question and sub_zero_response:
                    self.user_questions.append(user_question)
                    self.sub_zero_responses.append(sub_zero_response)
            
            print(f"✅ Loaded {len(self.conversations)} Sub-Zero conversation pairs")
            
        except Exception as e:
            print(f"❌ Error loading Sub-Zero dataset: {e}")
            self.conversations = []
    
    def build_similarity_model(self):
        """Build similarity matching model for questions"""
        if not self.user_questions:
            print("❌ No Sub-Zero training data available")
            return
        
        try:
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2),
                max_features=5000,
                min_df=1
            )
            
            self.question_vectors = self.vectorizer.fit_transform(self.user_questions)
            print(f"✅ Built similarity matching model")
            
        except Exception as e:
            print(f"❌ Error building similarity model: {e}")
    
    def get_response(self, user_input: str, threshold: float = 0.05) -> str:
        """Get Sub-Zero response using ONLY training data"""
        if not self.vectorizer or self.question_vectors is None:
            if self.sub_zero_responses:
                # Return a random response from training data
                return random.choice(self.sub_zero_responses)
            return "❄️ Sub-Zero is still mastering the ancient texts! Ask me something else, warrior! ❄️"
        
        # Clean input
        user_input = user_input.strip()
        if not user_input:
            if self.sub_zero_responses:
                return random.choice(self.sub_zero_responses)
            return "❄️ Speak clearly, warrior! ❄️"
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Vectorize the user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, self.question_vectors).flatten()
            
            # Get top matches above threshold
            valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) == 0:
                # Lower threshold if no matches
                threshold = 0.01
                valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) > 0:
                # Sort by similarity and get top matches
                sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
                
                # Select from top 3 matches for variety
                top_count = min(3, len(sorted_indices))
                selected_idx = sorted_indices[random.randint(0, top_count-1)]
                
                response = self.sub_zero_responses[selected_idx]
                
                # Cache the response
                self.response_cache[cache_key] = response
                return response
            else:
                # No good matches - use the most similar one anyway
                best_idx = np.argmax(similarities)
                response = self.sub_zero_responses[best_idx]
                self.response_cache[cache_key] = response
                return response
                
        except Exception as e:
            print(f"⚠️ Error in Sub-Zero similarity matching: {e}")
            # Return a random response from training data as ultimate fallback
            if self.sub_zero_responses:
                return random.choice(self.sub_zero_responses)
            return "❄️ The ice realm is temporarily clouded! ❄️"
    
    def get_training_stats(self) -> Dict:
        """Get statistics about the Sub-Zero training data"""
        if not self.conversations:
            return {}
        
        total_conversations = len(self.conversations)
        
        # Count crypto-related conversations
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'trading', 'defi', 'wallet', 'invest', 'coin', 'token']
        crypto_conversations = 0
        
        for conv in self.conversations:
            user_msg = conv.get('user', '').lower()
            if any(keyword in user_msg for keyword in crypto_keywords):
                crypto_conversations += 1
        
        avg_response_length = np.mean([len(conv.get('sub_zero', '')) for conv in self.conversations])
        
        return {
            'total_conversations': total_conversations,
            'crypto_conversations': crypto_conversations,
            'average_response_length': avg_response_length,
            'cache_size': len(self.response_cache)
        }

def test_pure_subzero_trainer():
    """Test the pure Sub-Zero trainer"""
    print("🧊 Testing Pure Sub-Zero Trainer")
    print("=" * 50)
    
    trainer = PureSubZeroTrainer()
    
    # Show stats
    stats = trainer.get_training_stats()
    print(f"📊 Sub-Zero Training Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test queries
    test_queries = [
        "Hello Sub-Zero!",
        "What is Bitcoin?",
        "How do I secure my crypto?",
        "What is Ethereum?",
        "Should I buy crypto now?",
        "What is DeFi?",
        "Tell me about blockchain",
        "How are you today?",
        "What are your powers?",
        "Goodbye!"
    ]
    
    print(f"\n❄️ Testing Sub-Zero Conversations:")
    for query in test_queries:
        response = trainer.get_response(query)
        print(f"User: {query}")
        print(f"Sub-Zero: {response}")
        print()

if __name__ == "__main__":
    test_pure_subzero_trainer()
