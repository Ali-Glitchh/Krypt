#!/usr/bin/env python3
"""
Sub-Zero Conversation Trainer
Specialized trainer for Sub-Zero personality using adapted human conversation data
"""

import random
import re
from typing import List, Dict, Tuple, Optional

class SubZeroConversationTrainer:
    def __init__(self, conversation_file: str = 'human_chat_subzero_style.txt'):
        self.conversation_file = conversation_file
        self.conversation_pairs = []
        self.subzero_responses = {}
        self.conversation_contexts = {}
        
        # Sub-Zero specific response patterns
        self.ice_responses = [
            "As cold as winter's embrace.",
            "The frost reveals all truths.",
            "Ice flows through my veins.",
            "Winter's wisdom guides me.",
            "The chill brings clarity.",
            "Frozen thoughts crystallize into action.",
            "Cold steel, colder heart.",
            "Honor burns like ice - pure and unyielding."
        ]
        
        self.parse_training_data()
    
    def parse_training_data(self):
        """Parse the Sub-Zero style conversation data"""
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            current_conversation = []
            
            for line in lines:
                if line.startswith('Human 1:') or line.startswith('Human 2:'):
                    # Extract the message part
                    message = line.split(':', 1)[1].strip() if ':' in line else ""
                    speaker = line.split(':')[0]
                    
                    if message:
                        current_conversation.append((speaker, message))
                    
                    # If we have a pair, add it to conversation pairs
                    if len(current_conversation) >= 2:
                        human1_msg = current_conversation[-2][1]
                        human2_msg = current_conversation[-1][1]
                        
                        # Store as conversational pairs
                        self.conversation_pairs.append((human1_msg, human2_msg))
                        
                        # Also store reverse for bidirectional learning
                        self.conversation_pairs.append((human2_msg, human1_msg))
                else:
                    # End of conversation - reset
                    current_conversation = []
            
            self._build_response_mappings()
            print(f"✅ Sub-Zero trainer loaded {len(self.conversation_pairs)} conversation pairs")
            
        except Exception as e:
            print(f"❌ Error loading Sub-Zero conversation data: {e}")
            self.conversation_pairs = []
    
    def _build_response_mappings(self):
        """Build response mappings for better conversation flow"""
        # Group responses by context/topic
        for input_msg, response_msg in self.conversation_pairs:
            # Normalize input for better matching
            normalized_input = self._normalize_text(input_msg)
            
            # Store multiple possible responses for each input pattern
            if normalized_input not in self.subzero_responses:
                self.subzero_responses[normalized_input] = []
            
            self.subzero_responses[normalized_input].append(response_msg)
            
            # Also map by keywords for partial matching
            keywords = self._extract_keywords(input_msg)
            for keyword in keywords:
                if keyword not in self.conversation_contexts:
                    self.conversation_contexts[keyword] = []
                self.conversation_contexts[keyword].append(response_msg)
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better matching"""
        # Convert to lowercase and remove punctuation
        normalized = re.sub(r'[^\w\s]', '', text.lower())
        # Remove extra spaces
        normalized = ' '.join(normalized.split())
        return normalized
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common stop words
        stop_words = {'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'I', 'me', 'my', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'it', 'its', 'we', 'us', 'our', 'they', 'them', 'their'}
        
        # Extract words that are 3+ characters and not stop words
        words = re.findall(r'\b\w{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:5]  # Return top 5 keywords
    
    def get_subzero_response(self, user_input: str, context: str = None) -> Optional[str]:
        """Get a Sub-Zero style response based on user input"""
        if not self.conversation_pairs:
            return random.choice(self.ice_responses)
        
        # First try exact/similar pattern matching
        normalized_input = self._normalize_text(user_input)
        
        # Check for exact matches first
        if normalized_input in self.subzero_responses:
            return random.choice(self.subzero_responses[normalized_input])
        
        # Try partial matching with keywords
        user_keywords = self._extract_keywords(user_input)
        possible_responses = []
        
        for keyword in user_keywords:
            if keyword in self.conversation_contexts:
                possible_responses.extend(self.conversation_contexts[keyword])
        
        if possible_responses:
            return random.choice(possible_responses)
        
        # Try semantic similarity with existing patterns
        best_match = self._find_similar_pattern(user_input)
        if best_match:
            return best_match
        
        # Fallback to ice-themed responses
        return random.choice(self.ice_responses)
    
    def _find_similar_pattern(self, user_input: str) -> Optional[str]:
        """Find similar conversation patterns"""
        user_keywords = set(self._extract_keywords(user_input))
        
        best_score = 0
        best_response = None
        
        for input_msg, response_msg in self.conversation_pairs:
            input_keywords = set(self._extract_keywords(input_msg))
            
            # Calculate similarity based on common keywords
            if user_keywords and input_keywords:
                similarity = len(user_keywords.intersection(input_keywords)) / len(user_keywords.union(input_keywords))
                
                if similarity > best_score and similarity > 0.3:  # At least 30% similarity
                    best_score = similarity
                    best_response = response_msg
        
        return best_response
    
    def get_greeting_response(self) -> str:
        """Get a Sub-Zero style greeting"""
        greetings = [
            "Greetings.",
            "I acknowledge your presence.", 
            "You have my attention.",
            "Speak.",
            "What brings you before me?",
            "Honor guides our meeting.",
            "The ice recognizes your approach."
        ]
        return random.choice(greetings)
    
    def get_farewell_response(self) -> str:
        """Get a Sub-Zero style farewell"""
        farewells = [
            "Until we meet again.",
            "Our paths may cross once more.",
            "I take my leave.",
            "Farewell.",
            "Honor guides my steps.",
            "May the frost preserve your path.",
            "Winter's blessing upon you."
        ]
        return random.choice(farewells)
    
    def enhance_with_ice_theme(self, response: str) -> str:
        """Enhance response with additional ice themes if appropriate"""
        # Add ice-themed endings to some responses
        ice_endings = [
            " The cold truth has been spoken.",
            " As certain as winter's return.",
            " Frozen in time, this truth remains.",
            " The ice reveals all."
        ]
        
        # Randomly add ice themes to longer responses (20% chance)
        if len(response.split()) > 5 and random.random() < 0.2:
            return response + random.choice(ice_endings)
        
        return response
    
    def get_crypto_themed_response(self, crypto_topic: str) -> str:
        """Get responses that blend Sub-Zero personality with crypto knowledge"""
        crypto_ice_responses = {
            'price': [
                "The market's temperature runs cold today.",
                "These numbers freeze in place like ice crystals.",
                "The frost of volatility touches all prices."
            ],
            'analysis': [
                "My icy perception cuts through market illusions.",
                "Cold analysis reveals the hidden patterns.",
                "The frozen truth of the charts speaks clearly."
            ],
            'general': [
                "Cryptocurrency flows like winter wind - unpredictable yet powerful.",
                "Honor demands careful study of these digital realms.",
                "The discipline of ice guides wise investment choices."
            ]
        }
        
        topic_key = 'general'
        if 'price' in crypto_topic.lower():
            topic_key = 'price'
        elif any(word in crypto_topic.lower() for word in ['analysis', 'chart', 'technical']):
            topic_key = 'analysis'
        
        return random.choice(crypto_ice_responses[topic_key])

if __name__ == "__main__":
    # Test the Sub-Zero trainer
    trainer = SubZeroConversationTrainer()
    
    # Test some responses
    test_inputs = [
        "Hi there!",
        "How are you doing?",
        "What do you think about the weather?",
        "Any plans for the weekend?",
        "Tell me about cryptocurrency",
        "Goodbye!"
    ]
    
    print("\n🧊 Sub-Zero Conversation Trainer Test:")
    print("=" * 50)
    
    for test_input in test_inputs:
        response = trainer.get_subzero_response(test_input)
        print(f"Input: {test_input}")
        print(f"Sub-Zero: {response}")
        print("-" * 30)
