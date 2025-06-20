#!/usr/bin/env python3
"""
Pure Dataset-Trained Normal Trainer - Only uses training data, no hardcoded responses
"""

import json
import re
import random
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PureNormalTrainer:
    def __init__(self, dataset_file: str = 'normal_conversation_dataset.json'):
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
            # Check if it's a JSON file
            if self.dataset_file.endswith('.json'):
                self.load_json_dataset()
            else:
                self.load_text_dataset()
                
            print(f"✅ Loaded {len(self.conversations)} pure normal conversation pairs")
            
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
                self.conversations.append({
                    "user": user_msg,
                    "bot": bot_response
                })
                
                self.user_inputs.append(user_msg)
                self.bot_responses.append(bot_response)
    
    def load_text_dataset(self):
        """Load text format dataset (original human_chat.txt format)"""
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
                
                if len(current_conversation) >= 2:
                    user_msg = current_conversation[-2][1]
                    bot_response = current_conversation[-1][1]
                    
                    self.conversations.append({
                        "user": user_msg,
                        "bot": bot_response
                    })
                    
                    self.user_inputs.append(user_msg)
                    self.bot_responses.append(bot_response)
    
    def build_similarity_model(self):
        """Build TF-IDF similarity model for response matching"""
        if not self.user_inputs:
            print("❌ No training data available for similarity model")
            return
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10000,
            min_df=1
        )
        
        self.input_vectors = self.vectorizer.fit_transform(self.user_inputs)
        print(f"✅ Built similarity model with {len(self.user_inputs)} training examples")
    
    def find_best_response(self, user_input: str, threshold: float = 0.05) -> str:
        """Find the best response using similarity matching - ONLY from training data"""
        if not self.vectorizer or not self.input_vectors.size:
            return "I'm still learning from the conversations. Could you ask something else?"
        
        # Clean and normalize input
        user_input = user_input.strip()
        if not user_input:
            return "I'm here to chat! What would you like to talk about?"
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Vectorize user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, self.input_vectors).flatten()
            
            # Get top matches above threshold
            valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) == 0:
                # Lower threshold if no matches
                threshold = 0.01
                valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) > 0:
                # Sort by similarity and get top matches
                sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
                
                # Select from top 5 matches for variety
                top_count = min(5, len(sorted_indices))
                selected_idx = sorted_indices[random.randint(0, top_count-1)]
                
                response = self.bot_responses[selected_idx]
                
                # Cache the response
                self.response_cache[cache_key] = response
                return response
            else:
                # Absolutely no matches - use most similar anyway
                best_idx = np.argmax(similarities)
                response = self.bot_responses[best_idx]
                self.response_cache[cache_key] = response
                return response
                
        except Exception as e:
            print(f"⚠️ Error in similarity matching: {e}")
            # Return a random response from training data as fallback
            if self.bot_responses:
                return random.choice(self.bot_responses)
            return "I'm having trouble processing that right now."
    
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
            'cache_size': len(self.response_cache)
        }

def test_pure_trainer():
    """Test the pure trainer"""
    print("🧪 Testing Pure Normal Trainer")
    print("=" * 50)
    
    trainer = PureNormalTrainer()
    
    # Show stats
    stats = trainer.get_training_stats()
    print(f"📊 Training Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test queries
    test_queries = [
        "Hello there!",
        "How are you?", 
        "What's your name?",
        "Tell me about yourself",
        "What do you like to do?",
        "Where are you from?",
        "What's the weather like?",
        "Do you have any hobbies?",
        "Goodbye!",
        "See you later"
    ]
    
    print(f"\n💬 Testing Conversations:")
    for query in test_queries:
        response = trainer.find_best_response(query)
        print(f"User: {query}")
        print(f"Bot: {response}")
        print()

if __name__ == "__main__":
    test_pure_trainer()
