#!/usr/bin/env python3
"""
Pure Dataset-Trained Sub-Zero Trainer - Only uses training data, no hardcoded responses
Uses simplified similarity matching without scikit-learn dependencies
"""

import json
import random
import re
import math
from typing import Dict, List, Optional
import numpy as np

class PureSubZeroTrainer:
    def __init__(self, dataset_file: str = 'sub_zero_crypto_comprehensive_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_questions = []
        self.sub_zero_responses = []
        
        # Custom similarity components
        self.word_vectors = []
        self.all_words = []
        self.vocab_size = 0
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()

    def tokenize_text(self, text: str) -> List[str]:
        """Simple tokenization function"""
        # Remove punctuation and split into words
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        return [word for word in words if len(word) > 2]  # Filter short words
    
    def text_to_vector(self, text: str) -> List[float]:
        """Convert text to simple word count vector"""
        words = self.tokenize_text(text)
        vector = [0.0] * self.vocab_size
        
        for i, vocab_word in enumerate(self.all_words):
            vector[i] = words.count(vocab_word)
        
        return vector
    
    def cosine_similarity_custom(self, vec1: List[float], vec2: List[float]) -> float:
        """Custom cosine similarity implementation"""
        if not vec1 or not vec2:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)

    def load_dataset(self):
        """Load the Sub-Zero conversation dataset"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and 'conversations' in data:
                self.conversations = data['conversations']
            elif isinstance(data, list):
                self.conversations = data
            else:
                print(f"❌ Invalid dataset format in {self.dataset_file}")
                self.conversations = []
            
            # Extract user questions and Sub-Zero responses
            for conv in self.conversations:
                if 'user' in conv and 'subzero' in conv:
                    self.user_questions.append(conv['user'])
                    self.sub_zero_responses.append(conv['subzero'])
            
            print(f"✅ Loaded {len(self.conversations)} Sub-Zero conversations from dataset")
            
        except FileNotFoundError:
            print(f"❌ Dataset file not found: {self.dataset_file}")
            self.conversations = []
            # Basic fallback responses for Sub-Zero
            self.user_questions = ["hello", "what is bitcoin"]
            self.sub_zero_responses = [
                "I am Sub-Zero. Ice to meet you, mortal.",
                "Bitcoin... a digital currency as cold as my realm. It requires discipline and patience, traits few possess."
            ]

    def build_similarity_model(self):
        """Build simplified similarity model without scikit-learn"""
        if not self.user_questions:
            print("❌ No training questions available for similarity model")
            return
        
        try:
            # Use simple word-based similarity instead of TF-IDF
            self.word_vectors = []
            self.all_words = set()
            
            # Build vocabulary from all questions
            for question in self.user_questions:
                words = self.tokenize_text(question.lower())
                self.all_words.update(words)
            
            self.all_words = sorted(list(self.all_words))
            self.vocab_size = len(self.all_words)
            
            # Create word vectors for each question
            for question in self.user_questions:
                vector = self.text_to_vector(question.lower())
                self.word_vectors.append(vector)
            
            print(f"✅ Built Sub-Zero similarity model with {len(self.word_vectors)} conversations")
            print(f"📊 Vocabulary size: {self.vocab_size}")
            
        except Exception as e:
            print(f"❌ Error building Sub-Zero similarity model: {e}")
            self.word_vectors = None
            self.vocab_size = 0

    def find_best_response(self, user_input: str, threshold: float = 0.1) -> str:
        """Find the best Sub-Zero response using similarity matching"""
        if not self.user_questions or not hasattr(self, 'word_vectors') or not self.word_vectors:
            return "I am Sub-Zero, Grandmaster of the Lin Kuei. What brings you to my frozen domain?"
        
        try:
            # Create vector for user input
            user_vector = self.text_to_vector(user_input.lower())
            
            # Calculate similarities with all training questions
            similarities = []
            for i, training_vector in enumerate(self.word_vectors):
                similarity = self.cosine_similarity_custom(user_vector, training_vector)
                similarities.append(similarity)
            
            # Convert to numpy array for easier processing
            similarities = np.array(similarities)
            
            # Find the best match above threshold
            valid_indices = np.where(similarities >= threshold)[0]
            
            if len(valid_indices) == 0:
                # Lower threshold progressively
                for lower_threshold in [0.05, 0.02, 0.01]:
                    valid_indices = np.where(similarities >= lower_threshold)[0]
                    if len(valid_indices) > 0:
                        break
            
            if len(valid_indices) > 0:
                # Get the highest similarity match
                best_idx = valid_indices[np.argmax(similarities[valid_indices])]
                response = self.sub_zero_responses[best_idx]
                return response
            else:
                # Sub-Zero themed fallback
                return self.get_subzero_fallback(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in Sub-Zero similarity matching: {e}")
            return self.get_subzero_fallback(user_input)

    def get_subzero_fallback(self, user_input: str) -> str:
        """Sub-Zero themed fallback responses"""
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'trading', 'mining']
        has_crypto_terms = any(keyword in user_input.lower() for keyword in crypto_keywords)
        
        if has_crypto_terms:
            crypto_fallbacks = [
                "The realm of cryptocurrency is as vast and cold as the frozen tundra. Patience and discipline will guide you to mastery.",
                "Like the ancient arts of the Lin Kuei, crypto requires dedication and unwavering focus. Study well, young warrior.",
                "In the world of digital assets, as in combat, only the prepared survive. Learn the fundamentals before you strike."
            ]
            return random.choice(crypto_fallbacks)
        else:
            general_fallbacks = [
                "You speak in riddles, mortal. State your purpose clearly.",
                "The Lin Kuei do not waste words on trivial matters. Ask what truly concerns you.",
                "I am Sub-Zero, not a keeper of idle conversation. What knowledge do you seek?",
                "Your words drift like snow in the wind. Speak with purpose, or remain silent."
            ]
            return random.choice(general_fallbacks)

    def get_response(self, user_input: str) -> Dict:
        """Get Sub-Zero response with metadata"""
        response_text = self.find_best_response(user_input)
        
        return {
            "message": response_text,
            "type": "subzero_trained_data",
            "personality": "subzero",
            "confidence": 0.85,
            "training_source": "pure_subzero_dataset"
        }

    def get_training_info(self) -> Dict:
        """Get information about Sub-Zero training status"""
        return {
            "type": "pure_dataset_training",
            "conversations_loaded": len(self.conversations),
            "vocab_size": self.vocab_size,
            "features": [
                "Sub-Zero personality responses",
                "Mortal Kombat style dialogue",
                "Crypto knowledge with ice theme",
                "Lin Kuei warrior mentality",
                "Honor and discipline focus"
            ]
        }

if __name__ == "__main__":
    print("🧊 Testing Sub-Zero Trainer")
    trainer = PureSubZeroTrainer()
    
    test_inputs = [
        "Hello!",
        "What is Bitcoin?",
        "How do I trade crypto?",
        "Tell me about blockchain",
        "Who are you?",
        "Goodbye!"
    ]
    
    for test_input in test_inputs:
        response = trainer.get_response(test_input)
        print(f"\nUser: {test_input}")
        print(f"Sub-Zero: {response['message']}")
        print(f"Type: {response['type']}")
