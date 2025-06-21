#!/usr/bin/env python3
"""
Normal Conversation Trainer for the human_chat.txt dataset
"""

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
        self.questions = []
        self.responses = []
        self.vectorizer = None
        self.question_vectors = None
        self.response_cache = {}
        
        # Load and process the dataset
        self.load_dataset()
        self.build_similarity_model()
    
    def load_dataset(self):
        """Load the human chat dataset and parse conversations"""
        try:
            with open(self.dataset_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the conversations
            self.parse_conversations(content)
            print(f"✅ Loaded {len(self.conversations)} normal conversation pairs")
            
        except FileNotFoundError:
            print(f"❌ Dataset file {self.dataset_file} not found!")
            self.conversations = []
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.conversations = []
    
    def parse_conversations(self, content: str):
        """Parse conversations from human_chat.txt format"""
        lines = content.split('\n')
        current_conversation = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_conversation and len(current_conversation) >= 2:
                    # Process the conversation to extract Q&A pairs
                    self.extract_qa_pairs(current_conversation)
                current_conversation = []
            else:
                # Parse speaker and message
                if ':' in line:
                    speaker, message = line.split(':', 1)
                    speaker = speaker.strip()
                    message = message.strip()
                    current_conversation.append((speaker, message))
        
        # Process the last conversation if it exists
        if current_conversation and len(current_conversation) >= 2:
            self.extract_qa_pairs(current_conversation)
        
        # Extract questions and responses for similarity matching
        if self.conversations:
            self.questions = [conv['user'] for conv in self.conversations]
            self.responses = [conv['normal'] for conv in self.conversations]
    
    def extract_qa_pairs(self, conversation_turns: List[tuple]):
        """Extract question-answer pairs from conversation turns"""
        for i in range(len(conversation_turns) - 1):
            speaker1, message1 = conversation_turns[i]
            speaker2, message2 = conversation_turns[i + 1]
            
            # If different speakers, create a Q&A pair
            if speaker1 != speaker2:
                # Clean and validate messages
                question = self.clean_message(message1)
                answer = self.clean_message(message2)
                
                if question and answer and len(question) > 3 and len(answer) > 3:
                    self.conversations.append({
                        'user': question,
                        'normal': answer
                    })
    
    def clean_message(self, message: str) -> str:
        """Clean and validate a message"""
        if not message:
            return ""
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', message.strip())
        
        # Filter out very short or low-quality responses
        if len(cleaned) < 3:
            return ""
        
        # Add crypto context to responses when appropriate
        crypto_terms = ['bitcoin', 'crypto', 'ethereum', 'blockchain', 'trading', 'investment']
        if any(term in cleaned.lower() for term in crypto_terms):
            return cleaned
        
        # For non-crypto conversations, add helpful context
        return cleaned
    
    def build_similarity_model(self):
        """Build TF-IDF model for finding similar questions"""
        if not self.questions:
            return
        
        try:
            # Create TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=3000,
                lowercase=True,
                ngram_range=(1, 2)
            )
            
            # Fit and transform the questions
            self.question_vectors = self.vectorizer.fit_transform(self.questions)
            print("✅ Built normal conversation similarity model")
            
        except Exception as e:
            print(f"⚠️ Could not build normal conversation similarity model: {e}")
            self.vectorizer = None
    
    def find_best_response(self, user_input: str, threshold: float = 0.2) -> Optional[str]:
        """Find the best normal response using similarity matching"""
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
                response = self.responses[best_match_idx]
                # Add crypto context if needed
                response = self.add_crypto_context(response, user_input)
                # Cache the response
                self.response_cache[cache_key] = response
                return response
            else:
                # No good match found, use fallback
                return self.get_fallback_response(user_input)
                
        except Exception as e:
            print(f"⚠️ Error in normal conversation similarity matching: {e}")
            return self.get_fallback_response(user_input)
    
    def add_crypto_context(self, response: str, user_input: str) -> str:
        """Add crypto context to responses when relevant"""
        user_lower = user_input.lower()
        
        # If user asks about crypto topics, enhance the response
        crypto_keywords = ['bitcoin', 'crypto', 'ethereum', 'blockchain', 'trading', 'investment', 'price']
        
        if any(keyword in user_lower for keyword in crypto_keywords):
            crypto_enhancers = [
                " Here's what I know about crypto: ",
                " From a cryptocurrency perspective: ",
                " In the crypto space: ",
                " Speaking of digital assets: "
            ]
            
            # Avoid double enhancement
            if not any(enhancer in response for enhancer in crypto_enhancers):
                if random.random() < 0.3:  # 30% chance to enhance
                    response += random.choice(crypto_enhancers) + "feel free to ask me more specific crypto questions!"
        
        return response
    
    def get_fallback_response(self, user_input: str) -> str:
        """Generate a fallback normal response when no good match is found"""
        user_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            greetings = [
                "Hello! I'm here to help with crypto insights and general conversation. What's on your mind?",
                "Hi there! Ready to explore the world of cryptocurrency together?",
                "Hey! I'm your friendly crypto assistant. How can I help you today?",
                "Greetings! I'm here for all your crypto questions and more. What would you like to know?"
            ]
            return random.choice(greetings)
        
        # Crypto-related responses
        if any(word in user_lower for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']):
            crypto_responses = [
                "That's a great crypto question! I'd love to help you understand more about digital assets.",
                "Cryptocurrency is fascinating! What specific aspect interests you most?",
                "I'm here to help with all things crypto. Can you be more specific about what you'd like to know?",
                "The crypto world is vast and exciting! What particular area would you like to explore?"
            ]
            return random.choice(crypto_responses)
        
        # Trading responses
        if any(word in user_lower for word in ['trade', 'buy', 'sell', 'invest']):
            trading_responses = [
                "Trading and investing require careful consideration. What specific guidance are you looking for?",
                "I can help with trading insights! What aspect of cryptocurrency trading interests you?",
                "Investment decisions are important. What crypto investment questions do you have?",
                "Smart trading starts with good information. How can I help with your crypto strategy?"
            ]
            return random.choice(trading_responses)
        
        # General responses
        general_responses = [
            "That's interesting! Can you tell me more about what you're looking for?",
            "I'd love to help! Could you provide a bit more detail about your question?",
            "Great question! Can you elaborate so I can give you the best answer?",
            "I'm here to help! What specific information are you seeking?",
            "Thanks for asking! Could you be more specific about what you'd like to know?"
        ]
        return random.choice(general_responses)
    
    def get_response(self, user_input: str) -> str:
        """Main method to get normal response"""
        if not user_input.strip():
            return "I'm here to help! What would you like to know about crypto or anything else?"
        
        # Preprocess input
        processed_input = re.sub(r'\s+', ' ', user_input.strip())
        
        # Find best response
        response = self.find_best_response(processed_input)
        
        return response or self.get_fallback_response(user_input)
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about the loaded conversations"""
        if not self.conversations:
            return {"total_conversations": 0}
        
        return {
            "total_conversations": len(self.conversations),
            "average_question_length": np.mean([len(conv['user']) for conv in self.conversations]),
            "average_response_length": np.mean([len(conv['normal']) for conv in self.conversations])
        }

# Example usage and testing
if __name__ == "__main__":
    trainer = NormalConversationTrainer()
    
    # Display stats
    stats = trainer.get_conversation_stats()
    print("\n💬 Normal Conversation Training Dataset Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test some responses
    test_questions = [
        "Hello!",
        "What is Bitcoin?",
        "How are you doing?",
        "Tell me about crypto",
        "What's your favorite holiday?",
        "Do you like trading?"
    ]
    
    print("\n💬 Testing Normal Responses:")
    for question in test_questions:
        response = trainer.get_response(question)
        print(f"\nUser: {question}")
        print(f"Normal: {response}")
