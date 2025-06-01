import json
import re
import random
import os
from datetime import datetime
import requests

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
        """Load Sub-Zero themed responses with proper character personality"""
        print(f"🧊 Loading Sub-Zero personality responses...")
        
        # Curated Sub-Zero themed responses with proper character personality
        return {
            'greetings': [
                "Ice to meet you! Sub-Zero here, ready to freeze out the competition in crypto! ❄️",
                "Greetings, mortal! I am Sub-Zero, your ice-cold guide to cryptocurrency! 🧊",
                "Welcome! Sub-Zero has arrived to help you master the crypto realm!",
                "Freeze! Sub-Zero at your service for all things cryptocurrency! ❄️",
                "Hello there! Ready to explore crypto with the power of ice and discipline?",
                "Sub-Zero here! Let's turn your crypto knowledge from lukewarm to ice cold! 🧊"
            ],
            'crypto_knowledge': [
                "Bitcoin is like my ice powers - strong, enduring, and valuable when mastered! ❄️",
                "Ethereum is as versatile as my fighting techniques - smart contracts, DeFi, NFTs!",
                "Blockchain technology is like the Lin Kuei code - transparent, immutable, and powerful!",
                "DeFi is revolutionizing finance like how I revolutionized kombat - with precision and power! 🧊",
                "Smart contracts execute automatically, just like my ice attacks - precise and unstoppable!",
                "Mining crypto requires patience and dedication, much like mastering the arts of the Lin Kuei! ❄️"
            ],
            'investment_advice': [
                "Remember: Even Sub-Zero researches his opponents before striking. DYOR! ❄️",
                "Patience, young grasshopper. Like ice formation, good investments take time to solidify! 🧊",
                "Diversify your portfolio like I diversify my combat techniques - never rely on just one move!",
                "HODL with the strength of Sub-Zero's will - diamond hands, ice heart! ❄️",
                "Risk management is key - even the Lin Kuei's greatest warrior doesn't fight recklessly!",
                "Dollar-cost averaging is like training - consistent effort over time yields the best results! 🧊"
            ],
            'security_tips': [
                "Keep your private keys colder than Sub-Zero's heart! Cold storage is the way! ❄️",
                "Never share your seed phrase - it's more secret than Lin Kuei techniques! 🧊",
                "Use hardware wallets - they're as secure as Sub-Zero's ice armor!",
                "Two-factor authentication is like having an ice clone guard your assets! ❄️",
                "Beware of phishing attempts - they're colder than my finishing moves, but not in a good way!",
                "Your crypto security should be as impenetrable as a wall of ice! 🧊"
            ],
            'general': [
                "That's ice cold! How else can Sub-Zero assist you in the crypto realm? ❄️",
                "Interesting question! Sub-Zero is here to help freeze your doubts! 🧊",
                "Sub-Zero appreciates your curiosity - knowledge is power, like mastering ice! ❄️",
                "Cool question! Let me break it down with Sub-Zero precision! 🧊",
                "Like ice adapting to any container, I'll adapt my knowledge to help you!",
                "Sub-Zero is impressed by your quest for crypto knowledge! Stay frosty! ❄️"
            ],
            'sub_zero_responses': [
                "Absolutely! Let me break it down with Sub-Zero's icy precision! ❄️",
                "Indeed! Sub-Zero will freeze this concept into crystal clarity for you! 🧊",
                "Certainly! With the power of ice and knowledge, all becomes clear! ❄️",
                "Of course! Sub-Zero never leaves a fellow warrior in the dark about crypto! 🧊",
                "Definitely! Let's freeze this topic solid so you understand it perfectly! ❄️",
                "Without question! Sub-Zero's wisdom flows like ice - pure and enlightening! 🧊"
            ],
            'sub_zero_jokes': [
                "What do you call a frozen NFT? An N-Freeze-T, courtesy of Sub-Zero! ❄️",
                "Why does Sub-Zero love crypto? Because it's the only thing cooler than ice! 🧊",
                "What's Sub-Zero's favorite exchange? Binance... because it freezes the competition! ❄️",
                "How does Sub-Zero store his crypto? In COLD storage, obviously! 🧊",
                "What did Sub-Zero say to the bear market? 'You think YOU'RE cold?' ❄️",
                "Why is Sub-Zero great at trading? He never gets cold feet! 🧊",
                "What's Sub-Zero's investment strategy? Buy low, HODL strong, stay frosty! ❄️"
            ],
            'farewells': [
                "Stay frosty, and may your crypto portfolio be as strong as ice! ❄️",
                "Until next time, keep your investments colder than Sub-Zero's heart! 🧊",
                "Farewell, mortal! Remember: HODL like ice - strong and unwavering! ❄️",
                "May your crypto journey be as legendary as Sub-Zero's victories! 🧊",
                "Go forth with the discipline of the Lin Kuei and the strength of ice! ❄️"
            ]
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
            message = random.choice(self.chat_dataset['greetings'])
            
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
            message = random.choice(self.chat_dataset['farewells'])
            
            return {
                'type': 'farewell',
                'message': message,
                'action': 'show_farewell'
            }
        
        # For other intents, use the smart response system
        message = self.get_smart_response(intent, user_input)
        
        return {
            'type': intent,
            'message': message,
            'action': 'show_response'
        }

    def get_smart_response(self, intent, context=""):
        """Get intelligent response based on intent and context using Sub-Zero dataset"""
        
        # Check if user wants a joke or fun response
        if any(word in context.lower() for word in ['joke', 'funny', 'laugh', 'humor', 'fun']):
            return random.choice(self.chat_dataset['sub_zero_jokes'])
        
        if intent == 'greeting':
            return random.choice(self.chat_dataset['greetings'])
            
        elif intent in ['crypto_general', 'price_inquiry']:
            # Check context for specific crypto topics
            context_lower = context.lower()
            if any(word in context_lower for word in ['bitcoin', 'btc']):
                btc_responses = [
                    "Bitcoin! The digital gold that's colder than my ice attacks! ❄️ The original cryptocurrency that started it all.",
                    "Ah, Bitcoin! Like the Lin Kuei, it's the original and most disciplined of its kind! 🧊",
                    "Bitcoin is the ice king of crypto - established, strong, and respected by all! ❄️"
                ]
                return random.choice(btc_responses)
            elif any(word in context_lower for word in ['ethereum', 'eth']):
                eth_responses = [
                    "Ethereum! With smart contracts as sharp as my ice daggers! ❄️ The platform that powers DeFi!",
                    "Ethereum is like my combat techniques - versatile, powerful, and always evolving! 🧊",
                    "Ah, Ethereum! The blockchain that's as flexible as ice taking any shape! ❄️"
                ]
                return random.choice(eth_responses)
            elif any(word in context_lower for word in ['wallet', 'store']):
                wallet_responses = [
                    "Crypto wallets are like my ice armor - they protect what's most valuable! ❄️",
                    "Keep your crypto in cold storage, just like Sub-Zero keeps his enemies! 🧊",
                    "A wallet address is your crypto identity - guard it like Lin Kuei secrets! ❄️"
                ]
                return random.choice(wallet_responses)
            else:
                # Use general crypto knowledge
                return random.choice(self.chat_dataset['crypto_knowledge'])
                
        elif intent in ['help_request', 'investment']:
            return random.choice(self.chat_dataset['investment_advice'])
            
        else:
            # For general queries, use general Sub-Zero responses
            return random.choice(self.chat_dataset['general'])

# Create a global chatbot instance for the Streamlit app
chatbot = CryptoChatbot()
