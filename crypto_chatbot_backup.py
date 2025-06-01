import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import re
import random
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
    
    def generate_response(self, user_input, market_data=None, selected_coin=None):
        """Generate appropriate response based on user input"""
        self.market_data = market_data
        
        if self.is_greeting(user_input):
            return {
                'type': 'greeting',
                'message': random.choice(self.crypto_patterns['greetings']),
                'action': 'show_welcome'
            }
        
        if self.is_farewell(user_input):
            return {
                'type': 'farewell',
                'message': 'Thanks for using Krypt! Stay safe in the crypto world! 🚀',
                'action': 'none'
            }
        
        if self.is_crypto_query(user_input):
            crypto_name = self.extract_crypto_name(user_input)
            
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
                        
                        return {
                            'type': 'crypto_info',
                            'message': f"Here's the latest info for {coin['name']} ({coin['symbol'].upper()}):\n"
                                     f"💰 Price: ${price:,.2f}\n"
                                     f"📈 24h Change: {change:+.2f}%\n"
                                     f"Click below for detailed analysis!",
                            'action': 'show_coin',
                            'coin_data': coin
                        }
                    else:
                        return {
                            'type': 'crypto_not_found',
                            'message': f"I couldn't find '{crypto_name}' in the market data. Try searching for popular coins like Bitcoin, Ethereum, or browse the coin list!",
                            'action': 'show_search_help'
                        }
            
            return {
                'type': 'crypto_general',
                'message': "I can help you with cryptocurrency information! Try asking about specific coins like 'Bitcoin price' or 'What is Ethereum worth?'",
                'action': 'show_search_help'
            }
        
        # General conversation
        return {
            'type': 'general',
            'message': "I'm Krypt's AI assistant! I specialize in cryptocurrency analysis. Ask me about coin prices, market trends, or type a coin name to get started! 🪙",
            'action': 'show_help'
        }

# Global chatbot instance
chatbot = CryptoChatbot()
