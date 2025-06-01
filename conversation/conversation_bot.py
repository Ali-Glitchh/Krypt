import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import random

class ConversationBot:
    """
    A simple rule-based conversational bot for Krypt.
    This doesn't require external APIs and works well for crypto-specific conversations.
    """
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        
        # Define intents and patterns
        self.intents = {
            'greeting': {
                'patterns': [
                    r'\b(hi|hello|hey|greetings|good morning|good evening|good afternoon)\b',
                    r'\b(what\'s up|sup|howdy)\b'
                ],
                'responses': [
                    "Hey there! I'm Krypt, your crypto analysis assistant. How can I help you today?",
                    "Hello! Ready to explore the crypto markets together?",
                    "Hi! I'm here to help you with cryptocurrency analysis and market insights. What would you like to know?"
                ]
            },
            'crypto_price': {
                'patterns': [
                    r'\b(price|cost|worth|value)\b.*\b(bitcoin|btc|ethereum|eth|crypto|coin)\b',
                    r'\b(bitcoin|btc|ethereum|eth|crypto|coin)\b.*\b(price|cost|worth|value)\b',
                    r'\b(how much is|what\'s the price of|current price)\b'
                ],
                'responses': [
                    "I'll check the current price of {crypto} for you right away!",
                    "Let me fetch the latest {crypto} price data for you.",
                    "Looking up {crypto} market data now..."
                ]
            },
            'crypto_sentiment': {
                'patterns': [
                    r'\b(sentiment|feeling|mood|outlook)\b.*\b(bitcoin|btc|ethereum|eth|crypto|market)\b',
                    r'\b(bullish|bearish)\b.*\b(bitcoin|btc|ethereum|eth|crypto)\b',
                    r'\b(should i buy|good time to invest|market analysis)\b'
                ],
                'responses': [
                    "I'll analyze the current market sentiment for {crypto}.",
                    "Let me check the sentiment indicators and news for {crypto}.",
                    "I'll provide you with a sentiment analysis, but remember this isn't financial advice!"
                ]
            },
            'help': {
                'patterns': [
                    r'\b(help|what can you do|features|capabilities|how to use)\b',
                    r'\b(tell me about yourself|who are you|what are you)\b'
                ],
                'responses': [
                    "I'm Krypt, your crypto analysis assistant! I can help you with:\n🔍 Real-time cryptocurrency prices\n📊 Market sentiment analysis\n📰 Latest crypto news\n💡 Market insights and trends\n\nJust ask me about any cryptocurrency!",
                    "I can help you analyze cryptocurrencies! Try asking:\n• 'What's the price of Bitcoin?'\n• 'Show me Ethereum sentiment'\n• 'Is it a good time to invest in crypto?'\n• 'What's happening with Solana?'"
                ]
            },
            'market_analysis': {
                'patterns': [
                    r'\b(market|analysis|trend|what\'s happening)\b',
                    r'\b(crypto market|overall market|market conditions)\b',
                    r'\b(bull|bear|sideways)\b.*\bmarket\b'
                ],
                'responses': [
                    "Let me analyze the current crypto market conditions for you.",
                    "I'll provide an overview of the market trends and key indicators.",
                    "Here's what's happening in the crypto markets right now..."
                ]
            },
            'investment_advice': {
                'patterns': [
                    r'\b(should i invest|good investment|buy or sell)\b',
                    r'\b(investment advice|financial advice|what do you recommend)\b',
                    r'\b(is it safe|risky|good time)\b.*\b(invest|buy)\b'
                ],
                'responses': [
                    "⚠️ I can provide market analysis, but I'm not a financial advisor. Cryptocurrency investments are highly volatile and risky. Always do your own research and consider consulting with a financial professional before making investment decisions.\n\nThat said, I can show you the current market data and sentiment analysis to help inform your decision.",
                    "While I can't give financial advice, I can provide you with market data, sentiment analysis, and news to help you make informed decisions. Remember: only invest what you can afford to lose in crypto!",
                ]
            },
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|take care|thanks|thank you)\b',
                    r'\b(that\'s all|i\'m done|exit|quit)\b'
                ],
                'responses': [
                    "Goodbye! Feel free to come back anytime for crypto analysis!",
                    "Take care! Happy crypto trading, and remember to invest responsibly!",
                    "See you later! May the markets be in your favor! 🚀"
                ]
            },
            'crypto_news': {
                'patterns': [
                    r'\b(news|latest|recent|what\'s new)\b.*\b(bitcoin|btc|ethereum|eth|crypto)\b',
                    r'\b(tell me about|update me on|what happened)\b.*\b(bitcoin|btc|ethereum|eth|crypto)\b'
                ],
                'responses': [
                    "I'll fetch the latest news about {crypto} for you.",
                    "Let me check recent {crypto} news and updates.",
                    "Here's what's been happening with {crypto} recently..."
                ]
            },
            'general_question': {
                'patterns': [
                    r'\b(what is|explain|tell me about)\b.*\b(bitcoin|blockchain|crypto|defi|nft)\b',
                    r'\b(how does|how do)\b.*\b(bitcoin|blockchain|crypto|mining)\b.*\bwork\b'
                ],
                'responses': [
                    "Great question! Let me explain {topic} for you.",
                    "I'd be happy to help you understand {topic} better.",
                    "{topic} is a fascinating subject! Here's what you need to know..."
                ]
            }
        }
        
        # Crypto name patterns
        self.crypto_patterns = {
            'bitcoin': ['bitcoin', 'btc', 'xbt'],
            'ethereum': ['ethereum', 'eth', 'ether'],
            'cardano': ['cardano', 'ada'],
            'binancecoin': ['bnb', 'binance coin', 'binance'],
            'solana': ['solana', 'sol'],
            'ripple': ['ripple', 'xrp'],
            'dogecoin': ['dogecoin', 'doge'],
            'polkadot': ['polkadot', 'dot'],
            'polygon': ['polygon', 'matic'],
            'avalanche': ['avalanche', 'avax'],
            'chainlink': ['chainlink', 'link'],
            'uniswap': ['uniswap', 'uni']
        }
        
        # Small talk responses
        self.small_talk = {
            'how are you': [
                "I'm doing great, thanks for asking! Ready to analyze some crypto markets!",
                "I'm functioning perfectly! How can I help you with crypto today?",
                "All systems operational! What cryptocurrency interests you today?"
            ],
            'what\'s your name': [
                "I'm Krypt, your friendly cryptocurrency analysis assistant!",
                "My name is Krypt! I'm here to help you navigate the crypto markets."
            ],
            'who created you': [
                "I was created to help people understand and analyze cryptocurrency markets!",
                "I'm a crypto analysis bot designed to make market insights accessible to everyone."
            ],
            'are you a robot': [
                "I'm an AI assistant specialized in cryptocurrency analysis. Think of me as your crypto-savvy friend!",
                "Yes, I'm an AI bot, but I'm here to provide real insights about the crypto market!"
            ]
        }
    
    def extract_crypto(self, text: str) -> Optional[str]:
        """Extract cryptocurrency name from text"""
        text_lower = text.lower()
        for crypto_id, patterns in self.crypto_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return crypto_id
        return None
    
    def classify_intent(self, text: str) -> Tuple[str, Dict]:
        """Classify the intent of user input"""
        text_lower = text.lower()
        
        # Check each intent
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    # Extract entities
                    entities = {}
                    
                    # Extract cryptocurrency if mentioned
                    crypto = self.extract_crypto(text)
                    if crypto:
                        entities['crypto'] = crypto
                    
                    # Extract topic for general questions
                    if intent_name == 'general_question':
                        topics = ['bitcoin', 'blockchain', 'crypto', 'defi', 'nft', 'mining']
                        for topic in topics:
                            if topic in text_lower:
                                entities['topic'] = topic
                                break
                    
                    return intent_name, entities
        
        # Check small talk
        for phrase, responses in self.small_talk.items():
            if phrase in text_lower:
                return 'small_talk', {'phrase': phrase}
        
        # Default to general chat
        return 'general_chat', {}
    
    def generate_response(self, text: str, session_id: str = None) -> Dict:
        """Generate a response based on user input"""
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': text,
            'session_id': session_id
        })
        
        # Classify intent
        intent, entities = self.classify_intent(text)
        
        # Handle different intents
        if intent in self.intents:
            responses = self.intents[intent]['responses']
            response = random.choice(responses)
            
            # Format response with entities
            if entities.get('crypto'):
                response = response.replace('{crypto}', entities['crypto'].upper())
            if entities.get('topic'):
                response = response.replace('{topic}', entities['topic'])
            
            # Return appropriate response type
            if intent in ['crypto_price', 'crypto_sentiment', 'crypto_news']:
                return {
                    'type': 'crypto_analysis',
                    'message': response,
                    'crypto': entities.get('crypto'),
                    'intent': intent
                }
            else:
                return {
                    'type': 'conversation',
                    'message': response,
                    'intent': intent
                }
        
        elif intent == 'small_talk':
            phrase = entities.get('phrase', '')
            responses = self.small_talk.get(phrase, ["I'm here to help with crypto analysis!"])
            return {
                'type': 'conversation',
                'message': random.choice(responses),
                'intent': intent
            }
        
        else:
            # Default response
            return {
                'type': 'conversation',
                'message': "I'm not sure I understand. I'm best at helping with cryptocurrency analysis! Try asking about Bitcoin, Ethereum, or any other crypto.",
                'intent': 'unknown'
            }
    
    def get_conversation_context(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return [
            conv for conv in self.conversation_history 
            if conv.get('session_id') == session_id
        ][-5:]  # Last 5 messages
    
    def learn_from_feedback(self, session_id: str, message_id: str, feedback: str):
        """Store feedback for improving responses"""
        # In a real implementation, this would save to a database
        # For now, we'll just log it
        feedback_data = {
            'session_id': session_id,
            'message_id': message_id,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        print(f"Feedback received: {feedback_data}")


# Conversation templates for more natural responses
CONVERSATION_TEMPLATES = {
    'market_insight': [
        "Based on my analysis, {crypto} is showing {sentiment} signals with a {percentage}% change in the last 24 hours.",
        "The {crypto} market is quite {sentiment} today. We're seeing {volume} in trading volume and {news_count} news articles discussing it.",
        "Interesting times for {crypto}! The sentiment analysis shows {sentiment} indicators, though remember that crypto markets are highly volatile."
    ],
    'educational': [
        "{topic} is one of the fundamental concepts in cryptocurrency. Would you like me to explain how it works?",
        "Great question about {topic}! This is actually a common area of interest for many crypto enthusiasts.",
        "Understanding {topic} is crucial for anyone interested in cryptocurrency. Let me break it down for you."
    ],
    'risk_warning': [
        "⚠️ Remember: Cryptocurrency investments carry significant risk. Prices can be extremely volatile.",
        "⚠️ Please note: This is analysis, not financial advice. Always do your own research.",
        "⚠️ Important: Never invest more than you can afford to lose in cryptocurrency."
    ]
}

# Example usage
if __name__ == "__main__":
    bot = ConversationBot()
    
    # Test conversations
    test_inputs = [
        "Hi there!",
        "What's the price of Bitcoin?",
        "How's the sentiment for Ethereum?",
        "Should I invest in crypto?",
        "What can you do?",
        "Tell me about blockchain",
        "Thanks, bye!"
    ]
    
    print("Testing Krypt Conversation Bot:\n")
    for user_input in test_inputs:
        print(f"User: {user_input}")
        response = bot.generate_response(user_input, "test_session")
        print(f"Bot: {response['message']}")
        print(f"Intent: {response['intent']}")
        print("-" * 50)
