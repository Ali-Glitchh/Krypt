#!/usr/bin/env python3
"""
Conversation Training Module for Sub-Zero Chatbot
Analyzes human_chat_subzero_full.txt to extract conversation patterns and responses
"""

import re
import random
from typing import List, Dict, Tuple

class ConversationTrainer:
    def __init__(self, training_file_path: str):
        self.training_file = training_file_path
        self.conversation_pairs = []
        self.response_patterns = {}
        self.greeting_patterns = []
        self.question_patterns = []
        self.casual_responses = []
        
    def parse_training_data(self):
        """Parse the training file to extract conversation patterns"""
        print("🧊 Parsing training data from human conversations...")
        
        with open(self.training_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_conversation = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse Human Echo and SubZero responses
            if line.startswith('🧊 Human Echo:'):
                human_msg = line.replace('🧊 Human Echo:', '').strip()
                current_conversation.append(('human', human_msg))
            elif line.startswith('❄️ SubZero:'):
                subzero_msg = line.replace('❄️ SubZero:', '').strip()
                current_conversation.append(('subzero', subzero_msg))
                
                # Create conversation pair (human input -> subzero response)
                if len(current_conversation) >= 2:
                    human_input = current_conversation[-2][1] if current_conversation[-2][0] == 'human' else None
                    if human_input:
                        self.conversation_pairs.append((human_input.lower(), subzero_msg))
        
        print(f"✅ Extracted {len(self.conversation_pairs)} conversation pairs")
        self._categorize_responses()
    
    def _categorize_responses(self):
        """Categorize responses by type for better matching"""
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon']
        questions_starters = ['what', 'how', 'where', 'when', 'why', 'do you', 'have you', 'are you']
        
        for human_input, subzero_response in self.conversation_pairs:
            # Categorize greetings
            if any(greeting in human_input for greeting in greetings):
                self.greeting_patterns.append(subzero_response)
            
            # Categorize questions
            elif any(human_input.startswith(q) for q in questions_starters):
                self.question_patterns.append((human_input, subzero_response))
            
            # Everything else as casual responses
            else:
                self.casual_responses.append((human_input, subzero_response))
    
    def get_natural_response(self, user_input: str) -> str:
        """Get a natural response based on training data"""
        user_input_lower = user_input.lower().strip()
        
        # Check for direct matches first
        for human_msg, subzero_response in self.conversation_pairs:
            if self._similarity_score(user_input_lower, human_msg) > 0.8:
                return self._subzerofy_response(subzero_response)
        
        # Check for greeting patterns
        if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey']):
            if self.greeting_patterns:
                response = random.choice(self.greeting_patterns)
                return self._subzerofy_response(response)
        
        # Check for question patterns
        question_starters = ['what', 'how', 'where', 'when', 'why', 'do you', 'have you', 'are you']
        if any(user_input_lower.startswith(q) for q in question_starters):
            if self.question_patterns:
                _, response = random.choice(self.question_patterns)
                return self._subzerofy_response(response)
        
        # Fallback to casual responses
        if self.casual_responses:
            _, response = random.choice(self.casual_responses)
            return self._subzerofy_response(response)
        
        return None
    
    def _similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _subzerofy_response(self, response: str) -> str:
        """Add Sub-Zero personality to natural responses"""
        # Add ice-themed elements to natural responses
        ice_additions = [
            " ❄️", " 🧊", ", ice cold!", ", frostily speaking!", 
            " - Sub-Zero style!", " *freezes the moment*"
        ]
        
        # Sometimes add Sub-Zero personality elements
        if random.random() < 0.3:  # 30% chance to add Sub-Zero flair
            response += random.choice(ice_additions)
        
        # Replace certain words with Sub-Zero equivalents
        replacements = {
            'cool': 'ice cold',
            'awesome': 'freezing awesome',
            'great': 'ice cold great',
            'nice': 'frosty nice'
        }
        
        for original, replacement in replacements.items():
            if original in response.lower() and random.random() < 0.2:  # 20% chance
                response = response.replace(original, replacement)
        
        return response

# Global trainer instance
trainer = ConversationTrainer('human_chat_subzero_full.txt')
