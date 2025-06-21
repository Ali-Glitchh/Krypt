#!/usr/bin/env python3
"""
Advanced Sub-Zero Conversation Trainer for the comprehensive dataset
"""

import json
import re
import random
from typing import Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AdvancedSubZeroTrainer:
    def __init__(self, dataset_file: str = 'sub_zero_crypto_comprehensive_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_questions = []
        self.sub_zero_responses = []
        self.vectorizer = None
        self.question_vectors = None
        self.response_cache = {}
        
        # Sub-Zero personality enhancers
        self.ice_emojis = ["❄️", "🧊", "⛄", "🌨️", "🗻"]
        self.ice_words = ["freeze", "ice", "cold", "frost", "frozen", "chill", "arctic", "glacier", "blizzard"]
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
    
    def load_dataset(self):
        """Load the comprehensive Sub-Zero dataset"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                self.conversations = json.load(f)
            
            # Extract questions and responses for similarity matching
            self.user_questions = [conv['user'] for conv in self.conversations]
            self.sub_zero_responses = [conv['sub_zero'] for conv in self.conversations]
            
            print(f"✅ Loaded {len(self.conversations)} Sub-Zero conversation pairs")
            
        except FileNotFoundError:
            print(f"❌ Dataset file {self.dataset_file} not found!")
            self.conversations = []
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.conversations = []
    
    def build_similarity_model(self):
        """Build TF-IDF model for finding similar questions"""
        if not self.user_questions:
            return
        
        try:
            # Create TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=5000,
                lowercase=True,
                ngram_range=(1, 2)
            )
            
            # Fit and transform the questions
            self.question_vectors = self.vectorizer.fit_transform(self.user_questions)
            print("✅ Built similarity matching model")
            
        except Exception as e:
            print(f"⚠️ Could not build similarity model: {e}")
            self.vectorizer = None
      def preprocess_user_input(self, user_input: str) -> str:
        """Clean and preprocess user input"""
        # Remove extra whitespace and convert to lowercase for processing
        cleaned = re.sub(r'\s+', ' ', user_input.strip())
        return cleaned
    
    def find_best_response(self, user_input: str, threshold: float = 0.3) -> Optional[str]:
        """Find the best Sub-Zero response using similarity matching"""
        if not self.vectorizer or self.question_vectors is None:
            return self.get_fallback_response(user_input)
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Vectorize the user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, self.question_vectors).flatten()
            
            # Find the best match
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity >= threshold:
                response = self.sub_zero_responses[best_match_idx]
                # Cache the response
                self.response_cache[cache_key] = response
                return response
            else:
                # No good match found, use fallback
                return self.get_fallback_response(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in similarity matching: {e}")
            return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input: str) -> str:
        """Generate a fallback Sub-Zero response when no good match is found"""
        user_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            greetings = [
                "❄️ Ice to meet you! Sub-Zero here, ready to freeze out the crypto competition!",
                "🧊 Greetings, mortal! I am Sub-Zero, your ice-cold guide through cryptocurrency!",
                "❄️ Welcome! Sub-Zero has arrived to help you master the frozen crypto realm!"
            ]
            return random.choice(greetings)
        
        # Price-related responses
        if any(word in user_lower for word in ['price', 'cost', 'value', 'worth']):
            price_responses = [
                "❄️ The price is as cold as my ice daggers! Let me check the frozen markets for you!",
                "🧊 Sub-Zero will unveil the current price with icy precision!",
                "❄️ Time to freeze the market data and reveal the truth!"
            ]
            return random.choice(price_responses)
        
        # Analysis responses
        if any(word in user_lower for word in ['analyze', 'analysis', 'predict', 'forecast']):
            analysis_responses = [
                "❄️ Sub-Zero's market analysis cuts through the noise like ice through steel!",
                "🧊 Let me freeze this market data and give you the cold, hard truth!",
                "❄️ With the power of ice and data, Sub-Zero sees all market movements!"
            ]
            return random.choice(analysis_responses)
        
        # Trading responses
        if any(word in user_lower for word in ['buy', 'sell', 'trade', 'invest']):
            trading_responses = [
                "❄️ Sub-Zero's trading wisdom: Keep emotions frozen, let strategy guide you!",
                "🧊 Honor demands patience in trading - strike when the moment is ice-cold perfect!",
                "❄️ Like mastering ice techniques, successful trading requires discipline!"
            ]
            return random.choice(trading_responses)
        
        # Security responses
        if any(word in user_lower for word in ['safe', 'secure', 'protection', 'wallet']):
            security_responses = [
                "❄️ Guard your crypto like Sub-Zero guards clan secrets - with ice-cold vigilance!",
                "🧊 Security is paramount! Keep your keys colder than the arctic winds!",
                "❄️ Trust no one with your frozen assets - Lin Kuei wisdom applies to crypto!"
            ]
            return random.choice(security_responses)
        
        # General crypto responses
        if any(word in user_lower for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']):
            crypto_responses = [
                "❄️ Cryptocurrency knowledge flows through me like glacial streams! What specific aspect interests you?",
                "🧊 Sub-Zero masters both ice techniques and crypto wisdom! Ask me anything!",
                "❄️ The blockchain is like unbreakable ice - transparent, immutable, powerful!"
            ]
            return random.choice(crypto_responses)
        
        # Default fallback
        default_responses = [
            "❄️ Sub-Zero senses your question but needs more clarity! Can you elaborate?",
            "🧊 Like reading ancient Lin Kuei scrolls, your meaning requires deeper study. Please clarify!",
            "❄️ Sub-Zero's wisdom is vast as frozen seas, but your question needs refinement!",
            "🧊 Honor demands I understand fully before responding. Could you be more specific?",
            "❄️ The ice speaks to me, but your words need clearer focus. What exactly do you seek?"
        ]
        return random.choice(default_responses)
    
    def enhance_response_with_personality(self, response: str) -> str:
        """Add extra Sub-Zero personality elements to responses"""
        # Ensure ice emojis are present
        if not any(emoji in response for emoji in self.ice_emojis):
            response = random.choice(self.ice_emojis) + " " + response
        
        # Occasionally add ice-themed ending phrases
        if random.random() < 0.3:
            ice_endings = [
                " Stay frosty!",
                " May your portfolio freeze profits!",
                " Ice-cold wisdom prevails!",
                " The Lin Kuei way brings success!",
                " Honor guides the frozen path!"
            ]
            response += random.choice(ice_endings)
        
        return response
    
    def get_response(self, user_input: str) -> str:
        """Main method to get Sub-Zero response"""
        if not user_input.strip():
            return "❄️ Sub-Zero awaits your question... What wisdom do you seek?"
        
        # Preprocess input
        processed_input = self.preprocess_user_input(user_input)
        
        # Find best response
        response = self.find_best_response(processed_input)
        
        # Enhance with personality
        if response:
            response = self.enhance_response_with_personality(response)
        
        return response or self.get_fallback_response(user_input)
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about the loaded conversations"""
        if not self.conversations:
            return {"total_conversations": 0}
        
        # Count different types of conversations
        greeting_count = sum(1 for conv in self.conversations 
                           if any(word in conv['user'].lower() 
                                for word in ['hello', 'hi', 'hey', 'greetings']))
        
        crypto_count = sum(1 for conv in self.conversations 
                         if any(word in conv['user'].lower() 
                              for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']))
        
        trading_count = sum(1 for conv in self.conversations 
                          if any(word in conv['user'].lower() 
                               for word in ['trade', 'buy', 'sell', 'invest']))
        
        defi_count = sum(1 for conv in self.conversations 
                       if any(word in conv['user'].lower() 
                            for word in ['defi', 'yield', 'staking', 'liquidity']))
        
        return {
            "total_conversations": len(self.conversations),
            "greeting_conversations": greeting_count,
            "crypto_conversations": crypto_count,
            "trading_conversations": trading_count,
            "defi_conversations": defi_count,
            "average_response_length": np.mean([len(conv['sub_zero']) for conv in self.conversations])
        }

# Example usage and testing
if __name__ == "__main__":
    trainer = AdvancedSubZeroTrainer()
    
    # Display stats
    stats = trainer.get_conversation_stats()
    print("\n🧊 Sub-Zero Training Dataset Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test some responses
    test_questions = [
        "Hello Sub-Zero!",
        "What is Bitcoin?",
        "How do I buy cryptocurrency?",
        "Is crypto safe?",
        "What's your favorite coin?",
        "Tell me about DeFi"
    ]
    
    print("\n❄️ Testing Sub-Zero Responses:")
    for question in test_questions:
        response = trainer.get_response(question)
        print(f"\nUser: {question}")
        print(f"Sub-Zero: {response}")
