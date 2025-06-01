import json
import re
import random
import os

class CryptoChatbot:
    def __init__(self):
        self.crypto_patterns = self._load_crypto_patterns()
        self.conversation_patterns = self._load_conversation_patterns()
        self.chat_dataset = self._load_chat_dataset()
        self.market_data = None
        
    def _load_crypto_patterns(self):
        """Load cryptocurrency-specific conversation patterns"""
        return {
            'greetings': [
                'Hello! I can help you with cryptocurrency analysis and market insights.',
                'Hi there! Ready to explore the crypto market?',
                'Welcome to Krypt! How can I assist you with crypto today?'
            ],
            'price_inquiry': [
                'Let me check the current price for you.',
                'Fetching the latest market data...',
                'Getting real-time price information...'
            ],
            'analysis_request': [
                'I\'ll analyze the market sentiment and trends for you.',
                'Let me gather news and sentiment data...',
                'Performing comprehensive market analysis...'
            ],
            'investment_advice': [
                '⚠️ Remember: This is not financial advice. Always do your own research.',
                'Based on current market indicators, here\'s what I can tell you...',
                'Market analysis suggests... (Please invest responsibly)'
            ]
        }
    
    def _load_conversation_patterns(self):
        """Load general conversation patterns"""
        return {
            'greetings': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'farewells': ['bye', 'goodbye', 'see you', 'thanks', 'thank you'],
            'crypto_keywords': ['price', 'buy', 'sell', 'invest', 'analysis', 'chart', 'market', 'crypto', 'bitcoin', 'ethereum'],
            'help_keywords': ['help', 'how', 'what', 'explain', 'tell me'],
            'price_keywords': ['price', 'cost', 'value', 'worth', 'current', 'latest'],
            'trend_keywords': ['trend', 'analysis', 'forecast', 'prediction', 'outlook'],
            'comparison_keywords': ['compare', 'vs', 'versus', 'difference', 'better']
        }

    def _load_chat_dataset(self):
        """Load Sub-Zero crypto dataset for training and responses"""
        try:
            # Try current directory first, then the full path
            sub_zero_paths = [
                'sub_zero_crypto_dataset.json',
                os.path.join(os.path.dirname(__file__), 'sub_zero_crypto_dataset.json'),
                r'c:\Users\Dell\Desktop\Krypt\sub_zero_crypto_dataset.json'
            ]
            
            # Load Sub-Zero dataset
            sub_zero_dataset = None
            for path in sub_zero_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        sub_zero_dataset = json.load(f)
                    print(f"🧊 Successfully loaded Sub-Zero dataset from: {path}")
                    break
                except FileNotFoundError:
                    continue
            
            if not sub_zero_dataset:
                raise FileNotFoundError("Sub-Zero dataset not found in any expected location")
              
            # Process the Sub-Zero dataset into categories
            processed_dataset = {
                'greetings': [],
                'crypto_knowledge': [],
                'investment_advice': [],
                'security_tips': [],
                'general': [],
                'sub_zero_responses': [],
                'sub_zero_jokes': []
            }
            
            # Process Sub-Zero dataset and categorize into all response types
            for item in sub_zero_dataset:
                response = item['sub_zero']
                
                # Categorize Sub-Zero responses into different types
                if any(phrase in response.lower() for phrase in ['frozen', 'n-freeze-t', 'frost', 'ice', 'crypto traders throw parties', 'therapy', 'trust issues', 'joke', 'funny']):
                    processed_dataset['sub_zero_jokes'].append(response)
                elif any(word in response.lower() for word in ['hi', 'hello', 'meet', 'greetings', 'ice to meet']):
                    processed_dataset['greetings'].append(response)
                elif any(word in response.lower() for word in ['bitcoin', 'ethereum', 'blockchain', 'mining', 'wallet', 'defi', 'token', 'smart contract', 'dapp', 'nft', 'dao']):
                    processed_dataset['crypto_knowledge'].append(response)
                elif any(word in response.lower() for word in ['buying', 'selling', 'investment', 'market', 'bull', 'research', 'trading', 'hodl', 'fomo', 'fud']):
                    processed_dataset['investment_advice'].append(response)
                elif any(word in response.lower() for word in ['security', 'private key', 'seed', 'cold', 'hardware', 'backup', 'safe']):
                    processed_dataset['security_tips'].append(response)
                else:
                    processed_dataset['sub_zero_responses'].append(response)
            
            # Fill empty categories with Sub-Zero themed defaults
            if not processed_dataset['greetings']:
                processed_dataset['greetings'] = ["Ice to meet you! Sub-Zero here, ready to freeze out the competition in crypto!"]
            if not processed_dataset['crypto_knowledge']:
                processed_dataset['crypto_knowledge'] = ["What's Sub-Zero's favorite crypto? Any coin that can weather the frost!"]
            if not processed_dataset['investment_advice']:
                processed_dataset['investment_advice'] = ["Remember: Even in the coldest market, research is key!"]
            if not processed_dataset['security_tips']:
                processed_dataset['security_tips'] = ["Keep your crypto colder than Sub-Zero's finishing moves!"]
            if not processed_dataset['general']:
                processed_dataset['general'] = ["That's cool... ice cold, actually!"]
            
            return processed_dataset
            
        except FileNotFoundError:
            print("Warning: Sub-Zero dataset not found. Using default Sub-Zero responses.")
            return {
                'greetings': ["Ice to meet you! Sub-Zero here, ready to freeze out the competition in crypto!"],
                'crypto_knowledge': ["What's Sub-Zero's favorite crypto? Any coin that can weather the frost!"],
                'investment_advice': ["Remember: Even in the coldest market, research is key - Sub-Zero never makes hasty moves!"],
                'security_tips': ["Keep your crypto colder than Sub-Zero's finishing moves! Cold storage is key!"],
                'general': ["That's cool... ice cold, actually! How can Sub-Zero assist you further?"],
                'sub_zero_responses': ["Sure! Want me to break it down more? It's critical for understanding crypto - Sub-Zero style!"],
                'sub_zero_jokes': ["What do you call a frozen NFT? An N-Freeze-T, courtesy of Sub-Zero!"]
            }
        except Exception as e:
            print(f"Error loading Sub-Zero dataset: {e}")
            return {
                'greetings': ["Ice to meet you! Sub-Zero here for crypto assistance!"],
                'crypto_knowledge': ["I can help you with cryptocurrency information - Sub-Zero style!"],
                'investment_advice': ["Research is key before making any investment - even Sub-Zero studies his opponents!"],
                'security_tips': ["Always keep your private keys secure - colder than Sub-Zero's ice attacks!"],
                'general': ["That's Sub-Zero cool! How else can I help you with crypto?"],
                'sub_zero_responses': ["Absolutely! Let me break it down for you - Sub-Zero style!"],
                'sub_zero_jokes': ["What's the coldest crypto? Ice-coin, of course! ❄️"]
            }

    def detect_query_intent(self, user_input):
        """Detect the intent of user query"""
        text_lower = user_input.lower().strip()
        
        # Check for greetings
        if any(greeting in text_lower for greeting in self.conversation_patterns['greetings']):
            return 'greeting'
        
        # Check for name inquiries
        if any(phrase in text_lower for phrase in ['what is your name', 'who are you', 'tell me your name', 'what should i call you', 'what are you called']):
            return 'name_inquiry'
        
        # Check for farewells
        if any(farewell in text_lower for farewell in self.conversation_patterns['farewells']):
            return 'farewell'
        
        # Check for help requests
        if any(help_word in text_lower for help_word in self.conversation_patterns['help_keywords']):
            return 'help_request'
        
        # Check for crypto-related queries
        if any(crypto_word in text_lower for crypto_word in self.conversation_patterns['crypto_keywords']):
            return 'crypto_general'
        
        # Check for price inquiries
        if any(price_word in text_lower for price_word in self.conversation_patterns['price_keywords']):
            return 'price_inquiry'
        
        return 'general'

    def generate_response(self, user_input, market_data=None, selected_coin=None):
        """Generate appropriate response based on user input"""
        self.market_data = market_data
        
        # Detect intent first
        intent = self.detect_query_intent(user_input)
        
        if intent == 'greeting':
            # Use Sub-Zero dataset responses for greetings
            dataset_response = self.get_smart_response('greeting', user_input)
            if dataset_response and len(dataset_response) > 5:
                message = dataset_response
            else:
                # Fallback to Sub-Zero themed greetings instead of generic ones
                sub_zero_fallbacks = [
                    "Ice to meet you! Sub-Zero here, ready to help with crypto!",
                    "Freeze! Sub-Zero at your service for all things cryptocurrency!",
                    "Welcome, mortal! Let's explore the crypto world together!"
                ]
                message = random.choice(sub_zero_fallbacks)
            
            return {
                'type': 'greeting',
                'message': message,
                'action': 'show_welcome'
            }

        if intent == 'name_inquiry':
            # Sub-Zero identity responses
            name_responses = [
                "I am Sub-Zero, the Lin Kuei warrior who has mastered both ice and cryptocurrency! ❄️",
                "Sub-Zero is my name, and freezing crypto market fears is my game! 🧊",
                "I'm Sub-Zero! When I'm not throwing ice balls, I'm analyzing crypto markets!",
                "Call me Sub-Zero - your ice-cold guide to the crypto universe! ❄️"
            ]
            message = random.choice(name_responses)
            
            return {
                'type': 'name_response',
                'message': message,
                'action': 'show_welcome'
            }
        
        if intent == 'farewell':
            farewell_responses = [
                "Stay frosty, and may your crypto portfolio be as strong as ice! ❄️",
                "Until next time, keep your investments colder than Sub-Zero's heart!",
                "Farewell, mortal! Remember: HODL like ice - strong and unwavering!"
            ]
            message = random.choice(farewell_responses)
            
            return {
                'type': 'farewell',
                'message': message,
                'action': 'show_farewell'
            }
        
        # For other intents, use the smart response system
        dataset_response = self.get_smart_response(intent, user_input)
        if dataset_response and len(dataset_response) > 5:
            message = dataset_response
        else:
            message = "That's ice cold! Let me help you with that crypto question."
        
        return {
            'type': intent,
            'message': message,
            'action': 'show_response'
        }

    def get_smart_response(self, intent, context=""):
        """Get intelligent response based on intent and context using Sub-Zero dataset"""
        responses = []
        
        # Check if user wants a joke or fun response
        if any(word in context.lower() for word in ['joke', 'funny', 'laugh', 'humor', 'fun']):
            return random.choice(self.chat_dataset['sub_zero_jokes']) if self.chat_dataset['sub_zero_jokes'] else "What do you call a frozen NFT? An N-Freeze-T, courtesy of Sub-Zero!"
        
        if intent == 'greeting':
            responses = self.chat_dataset['greetings']
            # Add extra Sub-Zero greetings for variety
            sub_zero_greetings = [
                "Ice to meet you! Ready to explore the crypto world with Sub-Zero?",
                "Sub-Zero here! Let's freeze out the competition with some crypto knowledge!",
                "Welcome, mortal! I'm here to help you navigate the icy waters of cryptocurrency!",
                "Freeze! Sub-Zero at your service for all things crypto!"
            ]
            responses.extend(sub_zero_greetings)
            
        elif intent in ['crypto_general', 'price_inquiry']:
            # Check context for specific crypto topics and use appropriate Sub-Zero responses
            context_lower = context.lower()
            if any(word in context_lower for word in ['bitcoin', 'btc']):
                responses = [r for r in self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses'] if 'bitcoin' in r.lower()]
            elif any(word in context_lower for word in ['ethereum', 'eth']):
                responses = [r for r in self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses'] if 'ethereum' in r.lower()]
            elif any(word in context_lower for word in ['wallet', 'store']):
                responses = [r for r in self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses'] if 'wallet' in r.lower()]
            else:
                # Use all crypto knowledge and Sub-Zero responses
                responses = self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses']
                
        elif intent in ['help_request', 'investment']:
            responses = self.chat_dataset['investment_advice'] + self.chat_dataset['sub_zero_responses']
            
        else:
            # For general queries, use all available Sub-Zero responses
            responses = self.chat_dataset['general'] + self.chat_dataset['sub_zero_responses']
        
        # If no specific responses found, fall back to Sub-Zero general responses
        if not responses:
            responses = self.chat_dataset['sub_zero_responses'] or ["Ice to see you're interested in crypto! Let me break it down for you, mortal."]
        
        return random.choice(responses) if responses else "Ice to see you're interested in crypto! Let me break it down for you, mortal."

# Create a global chatbot instance for the Streamlit app
chatbot = CryptoChatbot()
