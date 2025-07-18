#!/usr/bin/env python3
"""
Enhanced SubZero Trainer with Better Crypto Query Handling
Improves responses for price queries and crypto-specific questions
"""

import json
import random
import re
import math
from typing import Dict, List, Optional
import numpy as np

class EnhancedSubZeroTrainer:
    def __init__(self, dataset_file: str = 'sub_zero_crypto_comprehensive_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_questions = []
        self.sub_zero_responses = []
        
        # Enhanced crypto knowledge base
        self.crypto_knowledge = {
            'bitcoin': {
                'description': 'The legendary cryptocurrency, forged by the mysterious Satoshi Nakamoto',
                'subzero_response': '🧊 Bitcoin - the first and most powerful digital asset, as enduring as the eternal frost! Created by the shadow-warrior Satoshi, it blazes the path for all crypto that follows!'
            },
            'ethereum': {
                'description': 'The smart contract platform that enables DeFi',
                'subzero_response': '❄️ Ethereum - the ice kingdom of smart contracts! Where frozen logic meets liquid assets, enabling the decentralized finance revolution!'
            },
            'cardano': {
                'description': 'The academic blockchain with proof-of-stake consensus',
                'subzero_response': '🌨️ Cardano - methodical and precise like the Lin Kuei training! Built on academic research and sustainable proof-of-stake consensus!'
            },
            'solana': {
                'description': 'High-speed blockchain for DeFi and NFTs',
                'subzero_response': '🧊 Solana - swift as the north wind, processing transactions with ice-cold efficiency! The speed of lightning frozen in blockchain form!'
            },
            'dogecoin': {
                'description': 'The meme cryptocurrency that became serious',
                'subzero_response': '❄️ Dogecoin - born as jest but forged into legend! Like Sub-Zero, who started as an assassin but became a protector, DOGE evolved from meme to legitimate force!'
            }
        }
        
        # Custom similarity components
        self.word_vectors = []
        self.all_words = []
        self.vocab_size = 0
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()

    def detect_price_query(self, user_input: str) -> tuple:
        """Detect if user is asking for price information"""
        price_indicators = ['price', 'cost', 'value', 'worth', 'trading at', 'current', 'how much', 'what is the price']
        crypto_mentions = []
        
        user_lower = user_input.lower()
        is_price_query = any(indicator in user_lower for indicator in price_indicators)
        
        # Check for crypto mentions
        for crypto in self.crypto_knowledge.keys():
            if crypto in user_lower or crypto.upper() in user_input:
                crypto_mentions.append(crypto)
        
        return is_price_query, crypto_mentions

    def generate_subzero_price_response(self, crypto_name: str) -> str:
        """Generate SubZero-themed response for price queries"""
        base_responses = [
            f"🧊 The {crypto_name.title()} markets flow like ice through my veins! Real-time prices change faster than the winter winds - consult your trading platform for current values, young warrior!",
            f"❄️ Patience, mortal! The price of {crypto_name.title()} shifts like shadows in the frozen realm. Check your preferred exchange for the most current battlefield conditions!",
            f"🌨️ The Lin Kuei do not simply observe prices - we understand the forces that move them! {crypto_name.title()} dances to the rhythm of supply, demand, and market sentiment!",
            f"🔵 Like the ancient ice that never melts, {crypto_name.title()}'s true value lies not in momentary price, but in its underlying technology and adoption! Study the fundamentals, young one!"
        ]
        return random.choice(base_responses)

    def tokenize_text(self, text: str) -> List[str]:
        """Simple tokenization function"""
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        return [word for word in words if len(word) > 2]
    
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
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
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
                if 'user' in conv and 'sub_zero' in conv:
                    self.user_questions.append(conv['user'])
                    self.sub_zero_responses.append(conv['sub_zero'])
            
            print(f"✅ Enhanced SubZero loaded {len(self.conversations)} conversations from dataset")
            
        except FileNotFoundError:
            print(f"❌ Dataset file not found: {self.dataset_file}")
            self.conversations = []
            self._create_fallback_data()

    def _create_fallback_data(self):
        """Create fallback data if dataset not found"""
        self.user_questions = [
            "hello", "what is bitcoin", "tell me about ethereum", 
            "how does crypto work", "what is blockchain"
        ]
        self.sub_zero_responses = [
            "🧊 I am Sub-Zero, Grandmaster of the Lin Kuei. Ice to meet you, mortal.",
            "❄️ Bitcoin - the legendary cryptocurrency, forged by the mysterious Satoshi Nakamoto! Like Sub-Zero emerging from shadows, Bitcoin brought financial revolution!",
            "🌨️ Ethereum - the ice kingdom of smart contracts! Where frozen logic meets liquid assets!",
            "🔵 Cryptocurrency operates like the ancient Lin Kuei techniques - complex, precise, and requiring mastery!",
            "❄️ Blockchain - an unbreakable chain of ice-cold data, each block linked to the next in eternal sequence!"
        ]

    def build_similarity_model(self):
        """Build simplified similarity model"""
        if not self.user_questions:
            print("❌ No training questions available for similarity model")
            return
        
        try:
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
            
            print(f"✅ Enhanced SubZero similarity model: {len(self.word_vectors)} conversations, {self.vocab_size} vocab")
            
        except Exception as e:
            print(f"❌ Error building enhanced SubZero similarity model: {e}")
            self.word_vectors = None
            self.vocab_size = 0

    def find_best_response(self, user_input: str, threshold: float = 0.1) -> str:
        """Find the best Sub-Zero response with enhanced crypto handling"""
        
        # First, check for price queries
        is_price_query, crypto_mentions = self.detect_price_query(user_input)
        
        if is_price_query and crypto_mentions:
            # Generate price-specific SubZero response
            crypto_name = crypto_mentions[0]
            return self.generate_subzero_price_response(crypto_name)
        
        # Check for specific crypto knowledge
        for crypto_name, crypto_info in self.crypto_knowledge.items():
            if crypto_name in user_input.lower():
                return crypto_info['subzero_response']
        
        # Use similarity matching for dataset responses
        if not self.user_questions or not hasattr(self, 'word_vectors') or not self.word_vectors:
            return self.get_subzero_fallback(user_input)
        
        try:
            user_vector = self.text_to_vector(user_input.lower())
            similarities = []
            
            for i, training_vector in enumerate(self.word_vectors):
                similarity = self.cosine_similarity_custom(user_vector, training_vector)
                similarities.append(similarity)
            
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
                best_idx = valid_indices[np.argmax(similarities[valid_indices])]
                response = self.sub_zero_responses[best_idx]
                return response
            else:
                return self.get_subzero_fallback(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in enhanced SubZero similarity matching: {e}")
            return self.get_subzero_fallback(user_input)

    def get_subzero_fallback(self, user_input: str) -> str:
        """Enhanced Sub-Zero themed fallback responses"""
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'trading', 'mining', 'defi', 'nft']
        has_crypto_terms = any(keyword in user_input.lower() for keyword in crypto_keywords)
        
        if has_crypto_terms:
            crypto_fallbacks = [
                "🧊 The realm of cryptocurrency is as vast and cold as the frozen tundra. Patience and discipline will guide you to mastery, young warrior!",
                "❄️ Like the ancient arts of the Lin Kuei, crypto requires dedication and unwavering focus. Study the fundamentals before you strike!",
                "🌨️ In the world of digital assets, as in combat, only the prepared survive. Learn, practice, and master your craft!",
                "🔵 The crypto markets flow like ice through mountain streams - unpredictable yet following natural laws. Respect their power!",
                "❄️ Sub-Zero has witnessed many battles, but the cryptocurrency realm offers endless challenges for those brave enough to enter!"
            ]
            return random.choice(crypto_fallbacks)
        else:
            general_fallbacks = [
                "🧊 You speak in riddles, mortal. State your purpose clearly, and Sub-Zero shall guide you.",
                "❄️ The Lin Kuei do not waste words on trivial matters. Ask what truly concerns you about the crypto realm.",
                "🌨️ I am Sub-Zero, not a keeper of idle conversation. What knowledge do you seek from the frozen depths?",
                "🔵 Your words drift like snow in the wind. Speak with purpose about cryptocurrency, or remain silent."
            ]
            return random.choice(general_fallbacks)

    def get_response(self, user_input: str) -> Dict:
        """Get Sub-Zero response with metadata"""
        response_text = self.find_best_response(user_input)
        
        return {
            "message": response_text,
            "type": "enhanced_subzero_response",
            "personality": "subzero",
            "confidence": 0.90,
            "training_source": "enhanced_subzero_trainer"
        }

    def get_training_stats(self) -> Dict:
        """Get training statistics"""
        return {
            "total_conversations": len(self.conversations),
            "vocabulary_size": self.vocab_size,
            "crypto_knowledge_base": len(self.crypto_knowledge),
            "features": [
                "Enhanced crypto query detection",
                "Price query handling", 
                "Crypto-specific knowledge base",
                "SubZero personality responses",
                "Similarity-based matching"
            ]
        }

# Test function
def test_enhanced_subzero():
    trainer = EnhancedSubZeroTrainer()
    
    test_queries = [
        "What is the price of Bitcoin?",
        "Tell me about Ethereum",
        "How does blockchain work?",
        "What is Cardano?", 
        "Hello SubZero"
    ]
    
    print("🧊 Testing Enhanced SubZero Trainer:")
    for query in test_queries:
        response = trainer.get_response(query)
        print(f"\nUser: {query}")
        print(f"SubZero: {response['message']}")

if __name__ == "__main__":
    test_enhanced_subzero()
