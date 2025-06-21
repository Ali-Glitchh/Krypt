#!/usr/bin/env python3
"""
Sub-Zero Personality Adapter
Transforms human conversation data to fit Sub-Zero's personality traits
"""

import re
import random
from typing import List, Dict, Tuple

class SubZeroPersonalityAdapter:
    def __init__(self):
        # Sub-Zero personality traits
        self.ice_metaphors = [
            "cold", "ice", "frost", "frozen", "chill", "arctic", "blizzard", 
            "freezing", "icy", "crystalline", "winter", "snow", "glacial"
        ]
        
        self.honor_terms = [
            "honor", "duty", "discipline", "loyalty", "respect", "code", 
            "tradition", "commitment", "integrity", "oath", "sacred"
        ]
        
        self.warrior_terms = [
            "training", "discipline", "focus", "meditate", "balance", "strength",
            "skill", "technique", "combat", "battle", "warrior", "fight"
        ]
        
        # Sub-Zero speech patterns
        self.speech_patterns = {
            # Replace casual expressions with formal ones
            "yeah": "indeed",
            "yep": "yes", 
            "yea": "yes",
            "ok": "understood",
            "okay": "very well",
            "cool": "acceptable",
            "awesome": "impressive",
            "great": "satisfactory",
            "nice": "adequate",
            "haha": "",
            "lol": "",
            "😂": "",
            "😛": "",
            "🙂": "",
            "😞": "",
            "😐": "",
            
            # Make responses more formal and cold
            "i'm": "I am",
            "you're": "you are", 
            "we're": "we are",
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "isn't": "is not",
            "aren't": "are not",
        }
        
        # Sub-Zero conversation starters and responses
        self.subzero_greetings = [
            "Greetings.",
            "I acknowledge your presence.",
            "You have my attention.",
            "Speak.",
            "What brings you before me?"
        ]
        
        self.subzero_farewells = [
            "Until we meet again.",
            "Our paths may cross once more.",
            "I take my leave.",
            "Farewell.",
            "Honor guides my steps."
        ]
        
        # Ice-themed replacements for common words
        self.ice_replacements = {
            "feel": "sense",
            "think": "perceive", 
            "hot": "warm",
            "excited": "focused",
            "fun": "engaging",
            "scary": "challenging",
            "happy": "content",
            "sad": "troubled",
            "tired": "weary",
            "busy": "occupied with duties",
            "relaxing": "meditative",
            "interesting": "intriguing",
            "boring": "mundane"
        }
    
    def apply_ice_metaphors(self, text: str) -> str:
        """Add ice-themed language to text"""
        # Add ice metaphors to emotional expressions
        ice_enhanced_text = text
        
        # Replace some common expressions with ice-themed ones
        replacements = {
            r'\bvery good\b': 'as solid as ice',
            r'\bexcellent\b': 'crystalline perfection',
            r'\bperfect\b': 'flawless as frozen steel',
            r'\bclear\b': 'crystal clear',
            r'\bstrong\b': 'hard as ice',
            r'\bquiet\b': 'silent as falling snow',
            r'\bcalm\b': 'still as frozen lake',
            r'\bfast\b': 'swift as arctic wind',
            r'\bslow\b': 'deliberate as forming frost'
        }
        
        for pattern, replacement in replacements.items():
            ice_enhanced_text = re.sub(pattern, replacement, ice_enhanced_text, flags=re.IGNORECASE)
        
        return ice_enhanced_text
    
    def add_honor_context(self, text: str) -> str:
        """Add honor and discipline themes to text"""
        # Add honor-based reasoning to decisions
        honor_patterns = {
            r'\bi should\b': 'honor demands I',
            r'\bi will\b': 'my duty requires I',
            r'\bi want to\b': 'I am compelled to',
            r'\bi like\b': 'I find honor in',
            r'\bi enjoy\b': 'there is discipline in',
            r'\bwe should\b': 'our code demands we',
            r'\byou should\b': 'wisdom suggests you'
        }
        
        enhanced_text = text
        for pattern, replacement in honor_patterns.items():
            enhanced_text = re.sub(pattern, replacement, enhanced_text, flags=re.IGNORECASE)
        
        return enhanced_text
    
    def apply_formal_speech(self, text: str) -> str:
        """Make speech more formal and measured"""
        formal_text = text
        
        # Apply speech pattern replacements
        for casual, formal in self.speech_patterns.items():
            formal_text = re.sub(r'\b' + re.escape(casual) + r'\b', formal, formal_text, flags=re.IGNORECASE)
        
        # Apply ice-themed word replacements
        for common, ice_themed in self.ice_replacements.items():
            formal_text = re.sub(r'\b' + re.escape(common) + r'\b', ice_themed, formal_text, flags=re.IGNORECASE)
        
        return formal_text
    
    def add_warrior_discipline(self, text: str) -> str:
        """Add martial arts and discipline themes"""
        # Replace casual activities with disciplined equivalents
        discipline_patterns = {
            r'\bexercise\b': 'training',
            r'\bwork out\b': 'condition my body',
            r'\blearn\b': 'study with discipline',
            r'\bpractice\b': 'refine my technique',
            r'\brelax\b': 'meditate',
            r'\brest\b': 'restore my energy',
            r'\bhang out\b': 'spend time in contemplation',
            r'\bparty\b': 'gather with fellow warriors'
        }
        
        enhanced_text = text
        for pattern, replacement in discipline_patterns.items():
            enhanced_text = re.sub(pattern, replacement, enhanced_text, flags=re.IGNORECASE)
        
        return enhanced_text
    
    def make_response_brief(self, text: str) -> str:
        """Make responses more brief and to the point (Sub-Zero doesn't waste words)"""
        # Remove unnecessary words and phrases
        brief_text = text
        
        # Remove filler words and excessive politeness
        filler_patterns = [
            r'\boh\s+',
            r'\bwell\s+',
            r'\bso\s+',
            r'\bactually\s+',
            r'\bbasically\s+',
            r'\breally\s+',
            r'\btotally\s+',
            r'\babsolutely\s+'
        ]
        
        for pattern in filler_patterns:
            brief_text = re.sub(pattern, '', brief_text, flags=re.IGNORECASE)
        
        # Trim excessive enthusiasm
        brief_text = re.sub(r'!+', '.', brief_text)
        brief_text = re.sub(r'\?+', '?', brief_text)
        
        return brief_text.strip()
    
    def transform_conversation_pair(self, human1: str, human2: str) -> Tuple[str, str]:
        """Transform a conversation pair to Sub-Zero style"""
        # Transform both sides of conversation
        subzero_human1 = self.transform_single_response(human1)
        subzero_human2 = self.transform_single_response(human2)
        
        return subzero_human1, subzero_human2
    
    def transform_single_response(self, text: str) -> str:
        """Transform a single response to Sub-Zero personality"""
        if not text or text.strip() == "":
            return text
        
        # Apply transformations in order
        transformed = text
        
        # 1. Make speech formal and replace casual terms
        transformed = self.apply_formal_speech(transformed)
        
        # 2. Add ice metaphors
        transformed = self.apply_ice_metaphors(transformed)
        
        # 3. Add honor and duty context
        transformed = self.add_honor_context(transformed)
        
        # 4. Add warrior discipline
        transformed = self.add_warrior_discipline(transformed)
        
        # 5. Make response brief and direct
        transformed = self.make_response_brief(transformed)
        
        # 6. Handle special cases for greetings and farewells
        transformed = self.handle_special_cases(transformed)
        
        return transformed
    
    def handle_special_cases(self, text: str) -> str:
        """Handle special cases like greetings and farewells"""
        text_lower = text.lower().strip()
        
        # Handle greetings
        if text_lower in ['hi!', 'hi', 'hello', 'hey', 'hello!', 'hey!']:
            return random.choice(self.subzero_greetings)
        
        # Handle simple farewells
        if text_lower in ['bye', 'goodbye', 'see you', 'ttyl!', 'talk to you later!']:
            return random.choice(self.subzero_farewells)
        
        # Handle questions with more formality
        if text.endswith('?') and len(text.split()) <= 5:
            # Short questions become more formal
            formal_questions = {
                'how are you?': 'How do you fare?',
                'what\'s up?': 'What occupies your thoughts?',
                'how\'s it going?': 'How do your endeavors progress?',
                'what are you doing?': 'What task commands your attention?'
            }
            
            for casual, formal in formal_questions.items():
                if text_lower == casual:
                    return formal
        
        return text
    
    def transform_conversation_file(self, input_file: str, output_file: str):
        """Transform entire conversation file to Sub-Zero personality"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            transformed_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    transformed_lines.append("")
                    continue
                
                # Parse the conversation format "Human X: message"
                if line.startswith('Human 1:') or line.startswith('Human 2:'):
                    prefix = line.split(':', 1)[0] + ':'
                    message = line.split(':', 1)[1].strip() if ':' in line else ""
                    
                    if message:
                        transformed_message = self.transform_single_response(message)
                        transformed_lines.append(f"{prefix} {transformed_message}")
                    else:
                        transformed_lines.append(line)
                else:
                    # Non-conversation lines pass through unchanged
                    transformed_lines.append(line)
            
            # Write transformed conversations
            with open(output_file, 'w', encoding='utf-8') as f:
                for line in transformed_lines:
                    f.write(line + '\n')
            
            print(f"✅ Sub-Zero personality transformation complete!")
            print(f"   Input: {input_file}")
            print(f"   Output: {output_file}")
            print(f"   Processed {len(lines)} lines")
            
        except Exception as e:
            print(f"❌ Error transforming conversation file: {e}")

if __name__ == "__main__":
    # Transform the human_chat.txt file to Sub-Zero style
    adapter = SubZeroPersonalityAdapter()
    adapter.transform_conversation_file(
        'human_chat.txt', 
        'human_chat_subzero_style.txt'
    )
