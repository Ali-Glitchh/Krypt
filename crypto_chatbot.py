import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import re
import random
import os
from datetime import datetime
import requests

class Seq2SeqModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(Seq2SeqModel, self).__init__()
        self.encoder = nn.Sequential(
            nn.Embedding(input_dim, hidden_dim),
            nn.GRU(hidden_dim, hidden_dim, num_layers=1, batch_first=True)
        )
        self.decoder = nn.Sequential(
            nn.Embedding(input_dim, hidden_dim),
            nn.GRU(hidden_dim, hidden_dim, num_layers=1, batch_first=True)
        )
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, input_seq):
        encoder_output, _ = self.encoder(input_seq)
        decoder_output, _ = self.decoder(encoder_output)
        output = self.fc(decoder_output[:, -1, :])
        return output

class CryptoChatbot:
    def __init__(self):
        self.model = None
        self.vocab = {}
        self.reverse_vocab = {}
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
            'crypto_keywords': ['price', 'buy', 'sell', 'invest', 'analysis', 'chart', 'market', 'crypto', 'bitcoin', 'ethereum'],            'help_keywords': ['help', 'how', 'what', 'explain', 'tell me'],
            'price_keywords': ['price', 'cost', 'value', 'worth', 'current', 'latest'],
            'trend_keywords': ['trend', 'analysis', 'forecast', 'prediction', 'outlook'],            'comparison_keywords': ['compare', 'vs', 'versus', 'difference', 'better']
        }

    def _load_chat_dataset(self):
        """Load Sub-Zero crypto dataset for training and responses"""
        try:
            import os
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
                'general': ["That's interesting! Tell me more, mortal."],
                'sub_zero_responses': ["Let me break that down for you - Sub-Zero style!"],
                'sub_zero_jokes': ["Ice to meet you in the crypto world!"]
            }

    def detect_query_intent(self, text):
        """Detect the intent of the user query"""
        text_lower = text.lower()
        
        if self.is_greeting(text):
            return 'greeting'
        
        if self.is_farewell(text):
            return 'farewell'
            
        # Check for price inquiries
        if any(keyword in text_lower for keyword in self.conversation_patterns['price_keywords']):
            return 'price_inquiry'
            
        # Check for trend analysis
        if any(keyword in text_lower for keyword in self.conversation_patterns['trend_keywords']):
            return 'trend_analysis'
            
        # Check for comparisons
        if any(keyword in text_lower for keyword in self.conversation_patterns['comparison_keywords']):
            return 'comparison'
            
        # Check for help requests
        if any(keyword in text_lower for keyword in self.conversation_patterns['help_keywords']):
            return 'help_request'
            
        # Check if it contains crypto keywords
        if self.is_crypto_query(text):
            return 'crypto_general'
            
        return 'general_conversation'
    
    def is_crypto_query(self, text):
        """Determine if the user input is crypto-related"""
        text_lower = text.lower()
        
        # Check for specific crypto names or symbols
        crypto_terms = ['btc', 'eth', 'bitcoin', 'ethereum', 'crypto', 'price', 'market', 'coin']
        if any(term in text_lower for term in crypto_terms):
            return True
            
        # Check for price-related queries
        price_terms = ['price', 'cost', 'value', 'worth', '$']
        if any(term in text_lower for term in price_terms):
            return True
            
        return False
    
    def is_greeting(self, text):
        """Check if the input is a greeting"""
        text_lower = text.lower().strip()
        greetings = self.conversation_patterns['greetings']
        # Check for exact matches or very close matches to avoid false positives
        return (text_lower in greetings or 
                any(greeting == text_lower for greeting in greetings) or
                any(text_lower.startswith(greeting + ' ') for greeting in greetings[:3]))
    
    def is_farewell(self, text):
        """Check if the input is a farewell"""
        text_lower = text.lower().strip()
        farewells = self.conversation_patterns['farewells']
        return any(farewell in text_lower for farewell in farewells)
    
    def extract_crypto_name(self, text):
        """Extract cryptocurrency name from user input"""
        text_lower = text.lower().strip()
        
        # First check if it's a greeting to avoid false matches
        if self.is_greeting(text):
            return None
            
        # Common crypto mappings
        crypto_mappings = {
            'btc': 'bitcoin',
            'eth': 'ethereum',
            'ada': 'cardano',
            'dot': 'polkadot',
            'link': 'chainlink',
            'bnb': 'binancecoin',
            'sol': 'solana',
            'avax': 'avalanche-2',
            'matic': 'matic-network',
            'shib': 'shiba-inu'
        }
        
        # Check for exact symbol matches first
        words = text_lower.split()
        for word in words:
            if word in crypto_mappings:
                return crypto_mappings[word]
        
        # Check for direct name matches
        for symbol, name in crypto_mappings.items():
            if name in text_lower and len(name) > 3:
                return name
                
        # Extract potential crypto names (words that might be cryptocurrencies)
        # Exclude common words and greetings
        excluded_words = {'the', 'and', 'for', 'with', 'price', 'what', 'how', 'is', 'hi', 'hello', 'hey', 'good', 'morning', 'afternoon', 'evening'}
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        for word in words:
            word_lower = word.lower()
            if len(word) > 2 and word_lower not in excluded_words:
                return word_lower
                
        return None
    
    def generate_response(self, user_input, market_data=None, selected_coin=None):
        """Generate appropriate response based on user input"""
        self.market_data = market_data
          # Detect intent first
        intent = self.detect_query_intent(user_input)
        
        if intent == 'greeting':
            # Use dataset responses for greetings
            dataset_response = self.get_smart_response('greeting', user_input)
            return {
                'type': 'greeting',
                'message': dataset_response if dataset_response and len(dataset_response) > 5 else random.choice(self.crypto_patterns['greetings']),
                'action': 'show_welcome'
            }
        
        if intent == 'farewell':
            return {
                'type': 'farewell',
                'message': 'Thanks for using Krypt! Stay safe in the crypto world! 🚀',
                'action': 'none'
            }

        if intent == 'help_request':
            return {
                'type': 'help',
                'message': "I can help you with:\n• Cryptocurrency prices and market data\n• Market analysis and trends\n• News sentiment analysis\n• Investment insights (not financial advice)\n\nTry asking: 'Bitcoin price', 'Ethereum trends', or just type a coin name!",                'action': 'show_help'
            }
        
        if self.is_crypto_query(user_input) or intent in ['price_inquiry', 'trend_analysis', 'crypto_general']:
            crypto_name = self.extract_crypto_name(user_input)
            
            # First check if we have a relevant dataset response for this query
            dataset_response = self.get_smart_response(intent, user_input)
            
            if crypto_name:
                # Find matching coin in market data
                if market_data:
                    matching_coins = [
                        coin for coin in market_data 
                        if (crypto_name.lower() in coin['symbol'].lower() or 
                            crypto_name.lower() in coin['name'].lower() or
                            coin['id'].lower() == crypto_name.lower())
                    ]
                    
                    if matching_coins:
                        coin = matching_coins[0]
                        price = coin.get('current_price', 'N/A')
                        change = coin.get('price_change_percentage_24h', 0) or 0
                        
                        # Customize response based on intent
                        if intent == 'price_inquiry':
                            message = f"💰 {coin['name']} ({coin['symbol'].upper()}) is currently ${price:,.2f}"
                            if change != 0:
                                direction = "📈" if change > 0 else "📉"
                                message += f"\n{direction} 24h Change: {change:+.2f}%"
                        else:
                            message = f"Here's the latest info for {coin['name']} ({coin['symbol'].upper()}):\n"
                            message += f"💰 Price: ${price:,.2f}\n"
                            message += f"📈 24h Change: {change:+.2f}%\n"
                            message += f"Click below for detailed analysis!"
                            
                            # Add dataset knowledge if relevant
                            if dataset_response and len(dataset_response) > 10:
                                message += f"\n\n💡 Did you know: {dataset_response}"
                        
                        return {
                            'type': 'crypto_info',
                            'message': message,
                            'action': 'show_coin',
                            'coin_data': coin
                        }
                    else:
                        # No coin found, but provide educational response from dataset
                        educational_response = dataset_response if dataset_response and len(dataset_response) > 10 else f"I couldn't find '{crypto_name}' in the market data."
                        return {
                            'type': 'crypto_not_found',
                            'message': f"{educational_response}\n\nTry searching for popular coins like Bitcoin, Ethereum, or browse the coin list!",
                            'action': 'show_search_help'
                        }
            else:
                # No specific crypto mentioned, provide general crypto education
                educational_response = dataset_response if dataset_response and len(dataset_response) > 10 else "I can help you with cryptocurrency information!"
                return {
                    'type': 'crypto_general',
                    'message': f"{educational_response}\n\nTry asking about specific coins like 'Bitcoin price' or 'What is Ethereum worth?'",
                    'action': 'show_search_help'                }
        
        # General conversation - use dataset responses
        dataset_response = self.get_smart_response('general', user_input)
        fallback_message = "I'm Krypt's AI assistant! I specialize in cryptocurrency analysis. Ask me about coin prices, market trends, or type a coin name to get started! 🪙"
        
        return {
            'type': 'general',            'message': dataset_response if dataset_response and len(dataset_response) > 5 else fallback_message,
            'action': 'show_help'
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
            elif any(word in context_lower for word in ['mining', 'mine']):
                responses = [r for r in self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses'] if 'mining' in r.lower()]
            elif any(word in context_lower for word in ['blockchain']):
                responses = [r for r in self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses'] if 'blockchain' in r.lower()]
            elif any(word in context_lower for word in ['defi', 'staking', 'yield']):
                responses = [r for r in self.chat_dataset['sub_zero_responses'] if any(term in r.lower() for term in ['defi', 'staking', 'yield'])]
            elif any(word in context_lower for word in ['nft', 'token']):
                responses = [r for r in self.chat_dataset['sub_zero_responses'] if any(term in r.lower() for term in ['nft', 'token'])]
            elif any(word in context_lower for word in ['hodl', 'fomo', 'fud']):
                responses = [r for r in self.chat_dataset['sub_zero_responses'] if any(term in r.lower() for term in ['hodl', 'fomo', 'fud'])]
            else:
                # Use all crypto knowledge and Sub-Zero responses
                responses = self.chat_dataset['crypto_knowledge'] + self.chat_dataset['sub_zero_responses']
                
        elif intent in ['help_request', 'investment']:
            responses = self.chat_dataset['investment_advice'] + self.chat_dataset['sub_zero_responses']
            
        elif 'security' in context.lower():
            responses = self.chat_dataset['security_tips'] + self.chat_dataset['sub_zero_responses']
            
        else:
            # For general queries, use all available Sub-Zero responses
            responses = self.chat_dataset['general'] + self.chat_dataset['sub_zero_responses']
        
        # If no specific responses found, fall back to Sub-Zero general responses
        if not responses:
            responses = self.chat_dataset['sub_zero_responses'] or ["Ice to see you're interested in crypto! Let me break it down for you, mortal."]
        
        return random.choice(responses) if responses else "Ice to see you're interested in crypto! Let me break it down for you, mortal."

    def get_crypto_education(self, topic):
        """Get educational content about specific crypto topics"""
        topic_lower = topic.lower()
        
        # Search for relevant educational responses in the dataset
        relevant_responses = []
        
        for category in self.chat_dataset.values():
            for response in category:
                if any(word in response.lower() for word in topic_lower.split()):
                    relevant_responses.append(response)
        
        if relevant_responses:
            return random.choice(relevant_responses)
        
        # Fallback educational responses
        education_map = {
            'bitcoin': "Bitcoin is a decentralized digital currency that operates on a peer-to-peer network.",
            'ethereum': "Ethereum is a blockchain platform that enables smart contracts and decentralized applications (DApps).",
            'blockchain': "Blockchain is a distributed ledger technology that maintains a continuously growing list of records.",
            'wallet': "Crypto wallets store your private keys and allow you to send, receive, and manage your cryptocurrencies.",
            'mining': "Mining is the process of validating transactions and adding them to the blockchain.",
            'defi': "DeFi (Decentralized Finance) refers to financial services built on blockchain technology.",
        }
        
        for key, value in education_map.items():
            if key in topic_lower:
                return value
        
        return "I'd be happy to help you learn about cryptocurrency topics!"

# Global chatbot instance
chatbot = CryptoChatbot()