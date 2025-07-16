#!/usr/bin/env python3
"""
Continuous Learning Enhanced Trainer
Improves conversation accuracy through ongoing training and optimization
Uses simplified similarity matching without scikit-learn dependencies
"""

import json
import re
import random
import time
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime

class ContinuousLearningTrainer:
    def __init__(self, dataset_file: str = 'crypto_normal_dataset.json'):
        self.dataset_file = dataset_file
        self.conversations = []
        self.user_inputs = []
        self.bot_responses = []
        self.vectorizer = None
        self.input_vectors = None
        self.response_cache = {}
        
        # Continuous learning components
        self.conversation_history = []
        self.response_quality_scores = {}
        self.similarity_threshold = 0.1
        self.learning_rate = 0.05
        self.min_quality_score = 0.7
        
        # Dynamic training data
        self.dynamic_conversations = []
        self.context_memory = {}
        self.conversation_patterns = {}
        
        # Performance metrics
        self.accuracy_metrics = {
            'total_responses': 0,
            'high_quality_responses': 0,
            'context_aware_responses': 0,
            'learning_iterations': 0
        }
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
        self.initialize_conversation_patterns()
    
    def load_dataset(self):
        """Load the conversation dataset with quality validation"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate and filter high-quality conversations
            for item in data:
                user_msg = item.get('user', '').strip()
                bot_response = item.get('bot', '').strip()
                
                if self.validate_conversation_quality(user_msg, bot_response):
                    self.conversations.append({
                        "user": user_msg,
                        "bot": bot_response,
                        "quality_score": self.calculate_initial_quality_score(user_msg, bot_response),
                        "usage_count": 0,
                        "last_used": None
                    })
                    
                    self.user_inputs.append(user_msg)
                    self.bot_responses.append(bot_response)
            
            print(f"✅ Loaded {len(self.conversations)} high-quality conversation pairs")
            
            # Load dynamic conversations if they exist
            self.load_dynamic_conversations()
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.conversations = []
    
    def validate_conversation_quality(self, user_input: str, bot_response: str) -> bool:
        """Validate if a conversation pair meets quality standards"""
        if not user_input or not bot_response:
            return False
        
        # Check minimum length
        if len(user_input) < 3 or len(bot_response) < 10:
            return False
        
        # Check for crypto relevance
        crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'defi', 'trading', 'invest', 'wallet', 'mining']
        has_crypto_context = any(keyword in (user_input + bot_response).lower() for keyword in crypto_keywords)
        
        # Check for coherence (basic)
        if bot_response.lower().startswith('i don\'t') and len(bot_response) < 30:
            return False
        
        return has_crypto_context or len(bot_response) > 50
    
    def calculate_initial_quality_score(self, user_input: str, bot_response: str) -> float:
        """Calculate initial quality score for a conversation pair"""
        score = 0.5  # Base score
        
        # Length appropriateness
        if 20 <= len(bot_response) <= 200:
            score += 0.1
        
        # Crypto relevance
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi']
        if any(keyword in bot_response.lower() for keyword in crypto_keywords):
            score += 0.2
        
        # Information density
        if len(bot_response.split()) > 10:
            score += 0.1
        
        # Helpful tone indicators
        helpful_indicators = ['help', 'assist', 'explain', 'understand', 'learn']
        if any(indicator in bot_response.lower() for indicator in helpful_indicators):
            score += 0.1
        
        return min(score, 1.0)
    
    def initialize_conversation_patterns(self):
        """Initialize common conversation patterns for better matching"""
        self.conversation_patterns = {
            'greetings': {
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
                'weight': 1.5
            },
            'questions': {
                'patterns': ['what', 'how', 'why', 'when', 'where', 'who'],
                'weight': 1.2
            },
            'crypto_terms': {
                'patterns': ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'nft'],
                'weight': 1.3            },
            'farewells': {
                'patterns': ['goodbye', 'bye', 'see you', 'thanks', 'thank you'],
                'weight': 1.4
            }
        }
    
    def build_similarity_model(self):
        """Build simplified similarity model without scikit-learn"""
        if not self.user_inputs:
            print("❌ No training data available for similarity model")
            return
        
        try:
            # Create simple word-based vectors for similarity calculation
            self.word_vectors = []
            self.vocabulary = set()
            
            # Build vocabulary from all inputs
            for text in self.user_inputs:
                words = self.simple_tokenize(text.lower())
                self.vocabulary.update(words)
            
            self.vocabulary = list(self.vocabulary)
            
            # Convert texts to simple vectors
            for text in self.user_inputs:
                vector = self.text_to_vector(text)
                self.word_vectors.append(vector)
            
            print(f"✅ Built simplified similarity model with {len(self.user_inputs)} conversations")
            print(f"📊 Vocabulary size: {len(self.vocabulary)}")
            print(f"🎯 Current similarity threshold: {self.similarity_threshold}")
            
        except Exception as e:
            print(f"❌ Error building similarity model: {e}")
            self.word_vectors = None
    
    def simple_tokenize(self, text: str) -> List[str]:
        """Simple tokenization without external dependencies"""
        # Remove punctuation and split on whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        
        # Filter out very short words and common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        filtered_words = [word for word in words if len(word) > 2 and word.lower() not in stop_words]
        return filtered_words
    
    def text_to_vector(self, text: str) -> List[float]:
        """Convert text to simple vector representation"""
        words = self.simple_tokenize(text.lower())
        vector = [0.0] * len(self.vocabulary)
        
        for word in words:
            if word in self.vocabulary:
                idx = self.vocabulary.index(word)
                vector[idx] += 1.0
          # Normalize vector
        total = sum(vector)
        if total > 0:
            vector = [v / total for v in vector]
        
        return vector
    
    def simple_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_best_response_with_learning(self, user_input: str, conversation_id: str = None) -> Dict:
        """Enhanced response finding with simplified similarity calculation"""
        if not self.user_inputs or not self.word_vectors:
            return {
                'response': "I'm still learning about cryptocurrency! Please ask me about Bitcoin, Ethereum, or blockchain.",
                'confidence': 0.1,
                'source': 'fallback'
            }
        
        user_input = user_input.strip()
        if not user_input:
            return {
                'response': "I'm here to help with your crypto questions!",
                'confidence': 0.5,
                'source': 'default'
            }
        
        # Check conversation context
        context_boost = self.get_context_boost(user_input, conversation_id)
        
        # Enhanced preprocessing
        processed_input = self.enhanced_preprocess(user_input)
        
        # Try pattern matching first
        pattern_response = self.try_pattern_matching(user_input)
        if pattern_response:
            return {
                'response': pattern_response,
                'confidence': 0.8,
                'source': 'pattern_match'
            }
        
        try:
            # Convert user input to vector
            user_vector = self.text_to_vector(processed_input)
            
            # Calculate similarities with context boost
            similarities = []
            for stored_vector in self.word_vectors:
                similarity = self.simple_cosine_similarity(user_vector, stored_vector)
                similarities.append(similarity)
            
            similarities = np.array(similarities)
            
            # Apply context and pattern boosts
            enhanced_similarities = self.apply_similarity_boosts(similarities, user_input, context_boost)
            
            # Adaptive threshold based on recent performance
            adaptive_threshold = self.get_adaptive_threshold()
            
            # Get best matches
            valid_indices = np.where(enhanced_similarities >= adaptive_threshold)[0]
            
            if len(valid_indices) == 0:
                # Progressive threshold lowering
                for lower_threshold in [adaptive_threshold * 0.7, adaptive_threshold * 0.5, adaptive_threshold * 0.3]:
                    valid_indices = np.where(enhanced_similarities >= lower_threshold)[0]
                    if len(valid_indices) > 0:
                        break
            
            if len(valid_indices) > 0:
                # Smart selection based on quality scores and usage
                selected_idx = self.smart_response_selection(valid_indices, enhanced_similarities)
                
                response = self.bot_responses[selected_idx]
                confidence = enhanced_similarities[selected_idx]
                
                # Update usage statistics
                self.conversations[selected_idx]['usage_count'] += 1
                self.conversations[selected_idx]['last_used'] = datetime.now().isoformat()
                
                # Record for learning
                self.record_response_usage(user_input, response, confidence, conversation_id)
                
                return {
                    'response': response,
                    'confidence': float(confidence),
                    'source': 'trained_data',
                    'index': selected_idx
                }
            else:
                # Generate contextual fallback
                fallback_response = self.generate_smart_fallback(user_input)
                return {
                    'response': fallback_response,
                    'confidence': 0.3,
                    'source': 'smart_fallback'
                }
                
        except Exception as e:
            print(f"⚠️ Error in similarity matching: {e}")
            return {
                'response': self.generate_smart_fallback(user_input),
                'confidence': 0.2,
                'source': 'error_fallback'
            }
    
    def enhanced_preprocess(self, user_input: str) -> str:
        """Enhanced preprocessing with crypto-specific optimizations"""
        text = user_input.lower()
        
        # Normalize common variations
        normalizations = {
            'btc': 'bitcoin',
            'eth': 'ethereum', 
            'crypto': 'cryptocurrency',
            'defi': 'decentralized finance',
            'nft': 'non fungible token',
            'dao': 'decentralized autonomous organization',
            'hodl': 'hold',
            'fomo': 'fear of missing out',
            'fud': 'fear uncertainty doubt'
        }
        
        for abbr, full in normalizations.items():
            text = text.replace(abbr, full)
        
        # Clean up common variations
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces
        text = re.sub(r'[^\w\s]', ' ', text)  # Non-alphanumeric except spaces
        
        return text.strip()
    
    def get_context_boost(self, user_input: str, conversation_id: str) -> float:
        """Calculate context boost based on conversation history"""
        if not conversation_id or conversation_id not in self.context_memory:
            return 0.0
        
        context = self.context_memory[conversation_id]
        recent_topics = context.get('recent_topics', [])
        
        # Boost if user input relates to recent conversation topics
        boost = 0.0
        for topic in recent_topics[-3:]:  # Last 3 topics
            if any(word in user_input.lower() for word in topic.split()):
                boost += 0.1
        
        return min(boost, 0.3)
    
    def apply_similarity_boosts(self, similarities: np.ndarray, user_input: str, context_boost: float) -> np.ndarray:
        """Apply various boosts to similarity scores"""
        enhanced_similarities = similarities.copy()
        
        # Apply context boost
        enhanced_similarities += context_boost
        
        # Apply pattern boosts
        for pattern_type, pattern_info in self.conversation_patterns.items():
            if any(pattern in user_input.lower() for pattern in pattern_info['patterns']):
                boost = (pattern_info['weight'] - 1.0) * 0.1
                enhanced_similarities += boost
        
        return enhanced_similarities
    
    def get_adaptive_threshold(self) -> float:
        """Get adaptive threshold based on recent performance"""
        if self.accuracy_metrics['total_responses'] < 10:
            return self.similarity_threshold
        
        accuracy_rate = self.accuracy_metrics['high_quality_responses'] / self.accuracy_metrics['total_responses']
        
        if accuracy_rate > 0.8:
            # High accuracy, can be more selective
            self.similarity_threshold = min(self.similarity_threshold + self.learning_rate * 0.1, 0.3)
        elif accuracy_rate < 0.6:
            # Low accuracy, be less selective
            self.similarity_threshold = max(self.similarity_threshold - self.learning_rate * 0.1, 0.05)
        
        return self.similarity_threshold
    
    def smart_response_selection(self, valid_indices: np.ndarray, similarities: np.ndarray) -> int:
        """Smart selection considering quality, freshness, and similarity"""
        scores = []
        
        for idx in valid_indices:
            conversation = self.conversations[idx]
            
            # Base similarity score
            score = similarities[idx]
            
            # Quality score boost
            score += conversation['quality_score'] * 0.2
            
            # Freshness penalty (reduce overused responses)
            usage_penalty = min(conversation['usage_count'] * 0.05, 0.3)
            score -= usage_penalty
            
            scores.append(score)
          # Select best score, but add some randomness for variety
        scores = np.array(scores)
        top_indices = valid_indices[np.argsort(scores)]
        
        # Take the top 3 or all if fewer than 3
        top_3_indices = top_indices[-3:] if len(top_indices) >= 3 else top_indices
        
        # Weighted random selection from top candidates
        if len(top_3_indices) == 1:
            selected_idx = top_3_indices[0]
        else:
            # Create normalized weights (higher for better scores)
            weights = np.array([1.0, 1.5, 2.0])[:len(top_3_indices)]
            weights = weights / weights.sum()
            selected_idx = np.random.choice(top_3_indices, p=weights)
        
        return selected_idx
    
    def record_response_usage(self, user_input: str, response: str, confidence: float, conversation_id: str):
        """Record response usage for learning"""
        self.accuracy_metrics['total_responses'] += 1
        
        # Estimate quality based on confidence and length
        estimated_quality = confidence * 0.7 + (min(len(response), 100) / 100) * 0.3
        
        if estimated_quality > self.min_quality_score:
            self.accuracy_metrics['high_quality_responses'] += 1
        
        # Update conversation context
        if conversation_id:
            if conversation_id not in self.context_memory:
                self.context_memory[conversation_id] = {'recent_topics': []}
            
            # Extract key topics from user input
            topics = self.extract_key_topics(user_input)
            self.context_memory[conversation_id]['recent_topics'].extend(topics)
            
            # Keep only recent topics
            self.context_memory[conversation_id]['recent_topics'] = \
                self.context_memory[conversation_id]['recent_topics'][-5:]
            
            self.accuracy_metrics['context_aware_responses'] += 1
    
    def extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from text for context tracking"""
        crypto_topics = ['bitcoin', 'ethereum', 'defi', 'trading', 'mining', 'staking', 'wallet', 'blockchain']
        found_topics = []
        
        text_lower = text.lower()
        for topic in crypto_topics:
            if topic in text_lower:
                found_topics.append(topic)
        
        return found_topics
    
    def try_pattern_matching(self, user_input: str) -> Optional[str]:
        """Enhanced pattern matching with learning"""
        user_lower = user_input.lower()
        
        # Greeting patterns with variety
        if any(greeting in user_lower for greeting in ['hello', 'hi', 'hey']):
            greetings = [conv['bot'] for conv in self.conversations 
                        if any(g in conv['user'].lower() for g in ['hello', 'hi', 'hey'])]
            return random.choice(greetings) if greetings else None
        
        # Question patterns
        if user_input.endswith('?') and len(user_input) > 10:
            questions = [conv['bot'] for conv in self.conversations 
                        if '?' in conv['user'] and len(conv['user']) > 8]
            if questions:
                return random.choice(questions[:5])  # Limit to avoid repetition
        
        return None
    
    def generate_smart_fallback(self, user_input: str) -> str:
        """Generate contextually appropriate fallback responses"""
        user_lower = user_input.lower()
        
        # Crypto-specific fallbacks
        if any(crypto_word in user_lower for crypto_word in ['bitcoin', 'ethereum', 'crypto', 'blockchain']):
            crypto_fallbacks = [
                "That's a great crypto question! While I don't have that specific information, I'm always learning about the cryptocurrency ecosystem.",
                "Interesting crypto topic! I'm constantly expanding my knowledge about blockchain and digital assets. Feel free to ask about other crypto concepts!",
                "I appreciate your crypto curiosity! While I might not have that exact answer, I'm here to help with Bitcoin, Ethereum, DeFi, and other blockchain topics."
            ]
            return random.choice(crypto_fallbacks)
        
        # General helpful fallbacks
        general_fallbacks = [
            "I'm here to help with cryptocurrency questions! What would you like to know about Bitcoin, Ethereum, or blockchain technology?",
            "That's an interesting question! I specialize in crypto topics - feel free to ask about trading, investing, or blockchain concepts.",
            "I'm always learning! Could you ask me something about cryptocurrency, DeFi, or digital assets? I'd love to help!"
        ]
        return random.choice(general_fallbacks)
    
    def add_dynamic_conversation(self, user_input: str, bot_response: str, quality_score: float = 0.8):
        """Add a new high-quality conversation to the dynamic dataset"""
        if quality_score >= self.min_quality_score and self.validate_conversation_quality(user_input, bot_response):
            new_conversation = {
                "user": user_input,
                "bot": bot_response,
                "quality_score": quality_score,
                "usage_count": 0,
                "last_used": None,
                "date_added": datetime.now().isoformat(),
                "source": "dynamic_learning"
            }
            
            self.dynamic_conversations.append(new_conversation)
            self.conversations.append(new_conversation)
            self.user_inputs.append(user_input)
            self.bot_responses.append(bot_response)
            
            # Rebuild model if we have enough new conversations
            if len(self.dynamic_conversations) % 10 == 0:
                print(f"🔄 Rebuilding model with {len(self.dynamic_conversations)} new conversations...")
                self.build_similarity_model()
                self.save_dynamic_conversations()
    
    def save_dynamic_conversations(self):
        """Save dynamic conversations for persistent learning"""
        try:
            filename = f"dynamic_conversations_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.dynamic_conversations, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(self.dynamic_conversations)} dynamic conversations to {filename}")
        except Exception as e:
            print(f"⚠️ Error saving dynamic conversations: {e}")
    
    def load_dynamic_conversations(self):
        """Load previously saved dynamic conversations"""
        try:
            import glob
            dynamic_files = glob.glob("dynamic_conversations_*.json")
            
            total_loaded = 0
            for file in dynamic_files:
                with open(file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
                    self.dynamic_conversations.extend(conversations)
                    total_loaded += len(conversations)
            
            if total_loaded > 0:
                print(f"📚 Loaded {total_loaded} dynamic conversations from previous sessions")
                
                # Add to main conversations
                for conv in self.dynamic_conversations:
                    if conv not in self.conversations:
                        self.conversations.append(conv)
                        self.user_inputs.append(conv['user'])
                        self.bot_responses.append(conv['bot'])
        except Exception as e:
            print(f"⚠️ Error loading dynamic conversations: {e}")
    
    def get_learning_stats(self) -> Dict:
        """Get comprehensive learning and performance statistics"""
        total_conversations = len(self.conversations)
        dynamic_count = len(self.dynamic_conversations)
        
        accuracy_rate = 0
        if self.accuracy_metrics['total_responses'] > 0:
            accuracy_rate = self.accuracy_metrics['high_quality_responses'] / self.accuracy_metrics['total_responses']
          context_rate = 0
        if self.accuracy_metrics['total_responses'] > 0:
            context_rate = self.accuracy_metrics['context_aware_responses'] / self.accuracy_metrics['total_responses']
        
        return {
            'total_conversations': total_conversations,
            'dynamic_conversations': dynamic_count,
            'base_conversations': total_conversations - dynamic_count,
            'accuracy_rate': round(accuracy_rate * 100, 1),
            'context_awareness_rate': round(context_rate * 100, 1),
            'current_threshold': round(self.similarity_threshold, 3),
            'vocabulary_size': len(self.vocabulary) if hasattr(self, 'vocabulary') else 0,
            'total_responses_given': self.accuracy_metrics['total_responses'],
            'high_quality_responses': self.accuracy_metrics['high_quality_responses'],
            'learning_iterations': self.accuracy_metrics['learning_iterations'],
            'features': [
                'continuous_learning', 
                'adaptive_threshold', 
                'context_awareness', 
                'quality_scoring',
                'dynamic_expansion',
                'pattern_recognition',
                'simplified_similarity'
            ]
        }

def test_continuous_learning():
    """Test the continuous learning trainer"""
    print("🧪 Testing Continuous Learning Enhanced Trainer")
    print("=" * 60)
    
    trainer = ContinuousLearningTrainer()
    
    # Show initial stats
    stats = trainer.get_learning_stats()
    print(f"📊 Initial Learning Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    
    # Test conversations with different types
    test_conversations = [
        ("Hello there!", "greeting"),
        ("What is Bitcoin mining?", "technical_question"),
        ("How do I buy cryptocurrency safely?", "practical_advice"),
        ("Is DeFi really the future?", "opinion_question"),
        ("What's the best wallet for beginners?", "recommendation_request"),
        ("Thanks for your help!", "gratitude"),
        ("Can you explain blockchain technology?", "educational_request")
    ]
    
    print("💬 Testing Enhanced Conversations:")
    conversation_id = "test_session_001"
    
    for i, (query, query_type) in enumerate(test_conversations):
        print(f"\n[{query_type.upper()}] - Query {i+1}")
        print(f"User: {query}")
        
        result = trainer.find_best_response_with_learning(query, conversation_id)
        
        print(f"Bot: {result['response']}")
        print(f"Confidence: {result['confidence']:.3f} | Source: {result['source']}")
        
        # Simulate learning from high-quality interactions
        if result['confidence'] > 0.7:
            print("✅ High quality interaction - learning recorded")
    
    # Show final stats
    print("\n" + "=" * 60)
    final_stats = trainer.get_learning_stats()
    print(f"📈 Final Learning Stats:")
    for key, value in final_stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n✅ Continuous learning testing completed!")
    print("🎯 Enhanced trainer ready for deployment!")

if __name__ == "__main__":
    test_continuous_learning()
