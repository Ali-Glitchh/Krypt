#!/usr/bin/env python3
"""
Enhanced Pure Dataset-Trained Normal Trainer - Crypto-focused responses with API integration
Uses custom similarity matching without scikit-learn dependencies
"""

import json
import re
import random
import math
from typing import Dict, List, Optional
import numpy as np

# Import API utilities for real-time data
try:
    from api_utils import get_crypto_price, get_crypto_info, get_static_crypto_info
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False
    print("⚠️ API utilities not available - using static responses only")

class PureNormalTrainer:
    def __init__(self, dataset_file: str = 'crypto_normal_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_inputs = []
        self.bot_responses = []
        self.response_cache = {}
        
        # Custom similarity components
        self.word_vectors = []
        self.all_words = []
        self.vocab_size = 0
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
    
    def load_dataset(self):
        """Load the conversation dataset"""
        try:
            with open(self.dataset_file, 'r') as f:
                data = json.load(f)
                
            if isinstance(data, dict) and 'conversations' in data:
                self.conversations = data['conversations']
            elif isinstance(data, list):
                self.conversations = data
            else:
                print(f"❌ Invalid dataset format in {self.dataset_file}")
                self.conversations = []
            
            # Extract user inputs and bot responses
            for conv in self.conversations:
                if 'user' in conv and 'bot' in conv:
                    self.user_inputs.append(conv['user'])
                    self.bot_responses.append(conv['bot'])
            
            print(f"✅ Loaded {len(self.conversations)} crypto conversations from dataset")
            
        except FileNotFoundError:
            print(f"❌ Dataset file not found: {self.dataset_file}")
            self.conversations = []
            # Fallback basic responses
            self.user_inputs = ["hello", "what is bitcoin", "how are you"]
            self.bot_responses = [
                "Hello! I'm your crypto assistant.",
                "Bitcoin is the first cryptocurrency.",
                "I'm doing great! Ready to talk crypto?"
            ]

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

    def try_keyword_matching(self, user_input: str) -> Optional[str]:
        """Try to match using crypto-specific keywords with real-time data"""
        
        # Check for specific coin requests with flexible patterns
        if API_AVAILABLE:
            coin_patterns = [
                r'\b(\w+)(?:\s+coin)?\s*(?:price|cost|value)\b',  # "pi price", "pi coin price"
                r'\b(?:price|cost|value).*(?:of\s+)?(\w+)(?:\s+coin)?\b',  # "price of pi"
                r'\b(\w+)(?:\s+coin)\b',  # "pi coin", "bitcoin coin"
                r'\b(?:what.*is|about|info.*on|tell.*about)\s+(\w+)(?:\s+coin)?\b'  # "what is pi"
            ]
            
            for pattern in coin_patterns:
                match = re.search(pattern, user_input.lower())
                if match:
                    coin_name = match.group(1)
                    # Check if it's a known cryptocurrency
                    known_coins = ['bitcoin', 'btc', 'ethereum', 'eth', 'pi', 'doge', 'dogecoin', 'litecoin', 'ltc']
                    if coin_name in known_coins:
                        # Determine if they want price or general info
                        if re.search(r'\b(?:price|cost|value)\b', user_input.lower()):
                            return self.get_real_time_price(coin_name)
                        else:
                            return self.get_coin_information(coin_name)
        
        # Static keyword patterns for general responses
        keyword_patterns = {
            r'\b(hello|hi|hey)\b': [
                "Hello! I'm here to help with all your crypto questions!",
                "Hi there! Ready to explore the world of cryptocurrency?",
                "Hey! I'm your crypto assistant. What would you like to know?"
            ],
            r'\b(bye|goodbye|see you)\b': [
                "Goodbye! Keep HODLing and happy trading!",
                "See you later! May your portfolio be ever green!",
                "Bye! Remember to always DYOR (Do Your Own Research)!"
            ]
        }
        
        for pattern, responses in keyword_patterns.items():
            if re.search(pattern, user_input):
                return random.choice(responses)
        
        return None
    
    def get_real_time_price(self, coin_name: str) -> str:
        """Get real-time price for a cryptocurrency"""
        try:
            # Normalize coin names
            coin_map = {
                'btc': 'bitcoin',
                'eth': 'ethereum', 
                'doge': 'dogecoin',
                'pi': 'pi-network'
            }
            
            coin_id = coin_map.get(coin_name.lower(), coin_name.lower())
            
            # Try API first
            if API_AVAILABLE:
                price = get_crypto_price(coin_id)
                if price:
                    return f"The current price of {coin_name.upper()} is ${price:,.4f} USD. Please note that crypto prices are highly volatile and change rapidly!"
            
            # Fallback to static info
            static_info = get_static_crypto_info(coin_id) if API_AVAILABLE else None
            if static_info:
                return f"I couldn't fetch live price data for {coin_name.upper()} right now. {static_info['description']}"
            else:
                return f"I couldn't fetch the current price for {coin_name}. You can check live prices on CoinGecko, CoinMarketCap, or your preferred crypto exchange."
                
        except Exception as e:
            return f"I'm having trouble fetching real-time data for {coin_name}. Please try again later or check a reliable crypto price tracker."
    
    def get_coin_information(self, coin_name: str) -> str:
        """Get detailed information about a cryptocurrency"""
        try:
            # Normalize coin names
            coin_map = {
                'btc': 'bitcoin',
                'eth': 'ethereum',
                'doge': 'dogecoin', 
                'pi': 'pi-network'
            }
            
            coin_id = coin_map.get(coin_name.lower(), coin_name.lower())
            
            # Try API first
            if API_AVAILABLE:
                coin_info = get_crypto_info(coin_id)
                if coin_info and coin_info.get('current_price', 0) > 0:
                    return f"""**{coin_info['name']} ({coin_info['symbol']})**
Current Price: ${coin_info['current_price']:,.4f}
24h Change: {coin_info['price_change_24h']:.2f}%
Market Cap: ${coin_info['market_cap']:,}

{coin_info['description']}

Remember to always do your own research before making investment decisions!"""
            
            # Fallback to static information
            static_info_map = {
                'pi': "Pi Network is a cryptocurrency project that allows users to mine Pi coins on their mobile phones. However, Pi is still in development phase and not yet tradeable on major exchanges.",
                'bitcoin': "Bitcoin (BTC) is the world's first cryptocurrency, created by Satoshi Nakamoto in 2009. It operates on a decentralized blockchain network.",
                'ethereum': "Ethereum (ETH) is a blockchain platform that enables smart contracts and decentralized applications (dApps).",
                'doge': "Dogecoin (DOGE) started as a meme cryptocurrency but has gained significant popularity and community support."
            }
            
            return static_info_map.get(coin_name.lower(), f"I don't have specific information about {coin_name} right now. You can research it on CoinGecko or CoinMarketCap for detailed information.")
                
        except Exception as e:
            return f"I'm having trouble fetching information about {coin_name}. Please try again later or check a reliable crypto information source."

    def find_best_response(self, user_input: str, threshold: float = 0.1) -> str:
        """Find the best response using enhanced similarity matching"""
        if not self.user_inputs or not hasattr(self, 'word_vectors') or not self.word_vectors:
            return "I'm still learning about cryptocurrency! Please ask me about Bitcoin, Ethereum, or blockchain."
        
        # Check cache first
        cache_key = user_input.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Try keyword matching first for common patterns
            keyword_response = self.try_keyword_matching(user_input.lower())
            if keyword_response:
                self.response_cache[cache_key] = keyword_response
                return keyword_response
            
            # Create vector for user input
            user_vector = self.text_to_vector(user_input.lower())
            
            # Calculate similarities with all training inputs
            similarities = []
            for i, training_vector in enumerate(self.word_vectors):
                similarity = self.cosine_similarity_custom(user_vector, training_vector)
                similarities.append(similarity)
            
            # Convert to numpy array for easier processing
            similarities = np.array(similarities)
            
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
                # Enhanced fallback with context-aware responses
                fallback_response = self.get_smart_fallback(user_input)
                self.response_cache[cache_key] = fallback_response
                return fallback_response
                
        except Exception as e:
            print(f"⚠️ Error in similarity matching: {e}")
            return self.get_smart_fallback(user_input)

    def get_smart_fallback(self, user_input: str) -> str:
        """Enhanced fallback responses based on input context"""
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'trading', 'mining', 'wallet', 'pi', 'coin']
        
        # Check if input contains crypto terms
        has_crypto_terms = any(keyword in user_input.lower() for keyword in crypto_keywords)
        
        if has_crypto_terms:
            crypto_fallbacks = [
                "That's an interesting crypto question! While I don't have specific data on that, I'd recommend checking reputable sources like CoinDesk or CoinTelegraph.",
                "I'm still learning about that aspect of cryptocurrency. Could you rephrase your question or ask about something more specific?",
                "That's a great crypto topic! For the most accurate and up-to-date information, I'd suggest consulting multiple reliable crypto resources."
            ]
            return random.choice(crypto_fallbacks)
        else:
            general_fallbacks = [
                "I'm focused on cryptocurrency topics. Feel free to ask me about Bitcoin, Ethereum, blockchain, or other crypto-related questions!",
                "I specialize in crypto discussions. What would you like to know about cryptocurrency or blockchain technology?",
                "Let's talk crypto! I'm here to help with questions about digital currencies, trading, and blockchain technology."
            ]
            return random.choice(general_fallbacks)

    def get_response(self, user_input: str) -> Dict:
        """Get response with enhanced metadata"""
        response_text = self.find_best_response(user_input)
        
        # Determine response type based on matching method
        if user_input.lower().strip() in self.response_cache:
            response_type = "cached"
        elif self.try_keyword_matching(user_input.lower()):
            response_type = "keyword_match"
        else:
            response_type = "similarity_match"
        
        return {
            "message": response_text,
            "type": f"normal_{response_type}",
            "personality": "normal",
            "confidence": 0.8,
            "training_source": "enhanced_crypto_dataset"
        }

    def get_training_info(self) -> Dict:
        """Get information about the training status"""
        return {
            "type": "enhanced_dataset_training",
            "conversations_loaded": len(self.conversations),
            "vocab_size": self.vocab_size,
            "cache_size": len(self.response_cache),
            "features": [
                "Crypto-focused responses",
                "Enhanced similarity matching",
                "Keyword pattern recognition",
                "Smart fallback responses",
                "Response caching",
                "Real-time API integration",
                "Static info fallback"
            ]
        }

if __name__ == "__main__":
    print("🧪 Testing Enhanced Normal Trainer with API Integration")
    trainer = PureNormalTrainer()
    
    test_inputs = [
        "Hello!",
        "pi coin",
        "pi",
        "What is Bitcoin?",
        "bitcoin price",
        "Tell me about pi coin",
        "Goodbye!"
    ]
    
    for test_input in test_inputs:
        response = trainer.get_response(test_input)
        print(f"\n👤 User: {test_input}")
        print(f"🤖 Bot: {response['message']}")
        print(f"📊 Type: {response['type']}")
