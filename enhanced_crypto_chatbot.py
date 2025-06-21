#!/usr/bin/env python3
"""
Enhanced Crypto Chatbot with Real-time Data, News Insights, Article Analysis, and Personality Modes
"""

import json
import re
import random
import os
from datetime import datetime
import requests
from typing import Dict, List, Optional
from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
import time

class EnhancedCryptoChatbot:
    def __init__(self):
        # Initialize APIs
        self.crypto_apis = CryptoAPIs()
        
        # Initialize article manager for custom insights
        try:
            from article_manager import ArticleManager
            self.article_manager = ArticleManager()
            # Load sample articles if none exist
            if not self.article_manager.articles:
                self.article_manager.load_sample_articles()
            self.use_articles = True
            print("✅ Article manager loaded with custom insights")
        except Exception as e:
            print(f"⚠️ Article manager not available: {e}")
            self.article_manager = None
            self.use_articles = False
        
        # Initialize conversation training
        self.conversation_patterns = self._load_conversation_patterns()
        self.personality_mode = "normal"  # "normal" or "subzero"          # Load training data
        try:
            from normal_conversation_trainer import NormalConversationTrainer
            self.trainer = NormalConversationTrainer('human_chat.txt')
            self.use_natural_responses = True
            print("✅ Normal conversation training loaded")
        except Exception as e:
            print(f"⚠️ Normal conversation training not available: {e}")
            self.trainer = None
            self.use_natural_responses = False
          # Load Sub-Zero specific conversation training
        try:
            from advanced_subzero_trainer_fixed import AdvancedSubZeroTrainer
            self.subzero_trainer = AdvancedSubZeroTrainer()
            self.use_subzero_responses = True
            print("✅ Advanced Sub-Zero conversation training loaded")
        except Exception as e:
            print(f"⚠️ Advanced Sub-Zero conversation training not available: {e}")
            self.subzero_trainer = None
            self.use_subzero_responses = False
        
        # Sub-Zero personality responses
        self.subzero_responses = self._load_subzero_responses()
        
        # News API setup (you can add your news API key here)
        self.news_api_key = os.getenv('NEWS_API_KEY', None)
        
    def _load_conversation_patterns(self):
        """Load general conversation patterns"""
        return {
            'greetings': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'farewells': ['bye', 'goodbye', 'see you', 'thanks', 'thank you'],
            'crypto_keywords': ['price', 'buy', 'sell', 'invest', 'analysis', 'chart', 'market', 'crypto', 'bitcoin', 'ethereum'],
            'price_keywords': ['price', 'cost', 'value', 'worth', 'current', 'latest'],
            'news_keywords': ['news', 'update', 'what happened', 'latest', 'recent'],
            'personality_switch': ['subzero', 'sub-zero', 'switch personality', 'change mode', 'normal mode'],
            'insight_keywords': ['insight', 'analysis', 'research', 'article', 'explain', 'tell me about', 'what do you know'],
            'article_keywords': ['your article', 'your content', 'your analysis', 'your insight', 'from your knowledge'],
        }
    
    def _load_subzero_responses(self):
        """Load Sub-Zero themed responses"""
        return {
            'greetings': [
                "Ice to meet you! Sub-Zero here, ready to freeze out the competition in crypto! ❄️",
                "Greetings, mortal! I am Sub-Zero, your ice-cold guide to cryptocurrency! 🧊",
                "Welcome! Sub-Zero has arrived to help you master the crypto realm!",
                "Freeze! Sub-Zero at your service for all things cryptocurrency! ❄️"
            ],
            'price_responses': [
                "The price is as cold as my ice daggers! Let me check the frozen markets for you! ❄️",
                "Sub-Zero will unveil the current price with icy precision! 🧊",
                "Time to freeze the market data and reveal the truth! ❄️"
            ],
            'analysis': [
                "Sub-Zero's market analysis cuts through the noise like ice through steel! ❄️",
                "Let me freeze this market data and give you the cold, hard truth! 🧊",
                "With the power of ice and data, Sub-Zero sees all market movements! ❄️"
            ]
        }
    
    def switch_personality(self, mode: str = None):
        """Switch between normal and Sub-Zero personality modes"""
        if mode:
            if mode.lower() in ['subzero', 'sub-zero', 'sub zero']:
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️"
            elif mode.lower() in ['normal', 'regular', 'default']:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready to help with crypto insights!"
        else:
            # Toggle mode
            if self.personality_mode == "normal":
                self.personality_mode = "subzero"
                return "🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️"
            else:
                self.personality_mode = "normal"
                return "✅ Normal mode activated! Ready to help with crypto insights!"
    
    def get_crypto_price(self, crypto_name: str) -> Dict:
        """Get real-time crypto price data"""
        try:
            # Clean up the crypto name
            crypto_name = crypto_name.lower().strip()
            
            # Common crypto mappings
            crypto_mapping = {
                'bitcoin': 'bitcoin',
                'btc': 'bitcoin',
                'ethereum': 'ethereum', 
                'eth': 'ethereum',
                'dogecoin': 'dogecoin',
                'doge': 'dogecoin',
                'cardano': 'cardano',
                'ada': 'cardano',
                'solana': 'solana',
                'sol': 'solana',
                'polkadot': 'polkadot',
                'dot': 'polkadot',
                'chainlink': 'chainlink',
                'link': 'chainlink'
            }
            
            coin_id = crypto_mapping.get(crypto_name, crypto_name)
            
            # Get price data from APIs
            price_data = self.crypto_apis.get_coin_price(coin_id)
            
            if price_data:
                return {
                    'name': price_data.get('name', crypto_name.title()),
                    'symbol': price_data.get('symbol', '').upper(),
                    'current_price': price_data.get('current_price', 0),
                    'price_change_24h': price_data.get('price_change_percentage_24h', 0),
                    'market_cap': price_data.get('market_cap', 0),
                    'volume': price_data.get('total_volume', 0),
                    'last_updated': price_data.get('last_updated', datetime.now().isoformat())
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return None
    
    def get_crypto_news(self, crypto_name: str = "cryptocurrency") -> List[Dict]:
        """Get latest crypto news"""
        try:
            if not self.news_api_key:
                # Fallback to a simple news response
                return [{
                    'title': f"Latest {crypto_name} market updates",
                    'description': "Real-time news requires API key configuration. Check recent market movements and trends.",
                    'url': '#',
                    'publishedAt': datetime.now().isoformat()
                }]
            
            # Use News API (requires API key)
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': f"{crypto_name} cryptocurrency",
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 3,
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return articles[:3]  # Return top 3 articles            
        except Exception as e:
            print(f"Error fetching news: {e}")
            
        return []
    
    def detect_query_intent(self, user_input: str) -> str:
        """Detect the intent of user query"""
        text_lower = user_input.lower().strip()
        
        # Check for personality switching
        if any(phrase in text_lower for phrase in self.conversation_patterns['personality_switch']):
            return 'personality_switch'
        
        # Check for article insights (specific to your content)
        if any(phrase in text_lower for phrase in self.conversation_patterns['article_keywords']):
            return 'article_insight'
        
        # Check for general insights
        if any(word in text_lower for word in self.conversation_patterns['insight_keywords']):
            return 'insight_query'
        
        # Check for price queries
        if any(word in text_lower for word in self.conversation_patterns['price_keywords']) and any(word in text_lower for word in self.conversation_patterns['crypto_keywords']):
            return 'price_query'
        
        # Check for news queries
        if any(word in text_lower for word in self.conversation_patterns['news_keywords']) and any(word in text_lower for word in self.conversation_patterns['crypto_keywords']):
            return 'news_query'
        
        # Check for greetings
        if any(greeting in text_lower for greeting in self.conversation_patterns['greetings']):
            return 'greeting'
        
        # Check for farewells
        if any(farewell in text_lower for farewell in self.conversation_patterns['farewells']):
            return 'farewell'
        
        # Check for crypto general
        if any(crypto_word in text_lower for crypto_word in self.conversation_patterns['crypto_keywords']):
            return 'crypto_general'        
        return 'general'
    
    def _extract_search_terms(self, user_input: str) -> str:
        """Extract search terms from user input for article insights"""
        text_lower = user_input.lower()
        
        # Common crypto terms that should be prioritized
        crypto_terms = ['bitcoin', 'ethereum', 'defi', 'nft', 'staking', 'yield', 'farming', 'mining']
        
        # Find crypto terms in the input
        found_terms = []
        for term in crypto_terms:
            if term in text_lower:
                found_terms.append(term)
        
        # If crypto terms found, use them
        if found_terms:
            return ' '.join(found_terms)
        
        # Otherwise, remove common query words and extract meaningful terms
        stop_words = ['what', 'is', 'the', 'about', 'tell', 'me', 'explain', 'your', 'article', 'insight', 'analysis', 'from', 'do', 'you', 'have', 'say', 'on']
        words = text_lower.split()
        
        # Keep meaningful words
        meaningful_words = []
        for word in words:
            if word not in stop_words and len(word) > 2:
                meaningful_words.append(word)
        
        # Default to cryptocurrency if nothing meaningful found
        result = ' '.join(meaningful_words) if meaningful_words else 'cryptocurrency'
        
        # Clean up common patterns
        result = result.replace('articles', '').replace('insights', '').strip()
        
        return result if result else 'cryptocurrency'
    
    def extract_crypto_name(self, user_input: str) -> str:
        """Extract cryptocurrency name from user input"""
        text_lower = user_input.lower()
        
        # Common crypto patterns
        crypto_patterns = [
            r'\b(bitcoin|btc)\b',
            r'\b(ethereum|eth)\b', 
            r'\b(dogecoin|doge)\b',
            r'\b(cardano|ada)\b',
            r'\b(solana|sol)\b',
            r'\b(polkadot|dot)\b',
            r'\b(chainlink|link)\b',
            r'\b(ripple|xrp)\b',
            r'\b(litecoin|ltc)\b',
            r'\b(binance coin|bnb)\b'
        ]
        
        for pattern in crypto_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)
        
        # Default to bitcoin if no specific crypto mentioned
        return 'bitcoin'
    
    def format_price_response(self, crypto_data: Dict, crypto_name: str) -> str:
        """Format price data into a readable response"""
        if not crypto_data:
            if self.personality_mode == "subzero":
                return f"❄️ Even Sub-Zero's ice powers couldn't freeze the data for {crypto_name}! The markets seem to be moving too fast! 🧊"
            else:
                return f"Sorry, I couldn't fetch the current price data for {crypto_name}. Please try again later."
        
        price = crypto_data['current_price']
        change_24h = crypto_data['price_change_24h']
        symbol = crypto_data['symbol']
        name = crypto_data['name']
        
        # Format change indicator
        change_indicator = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
        change_text = f"+{change_24h:.2f}%" if change_24h > 0 else f"{change_24h:.2f}%"
        
        if self.personality_mode == "subzero":
            if change_24h > 0:
                trend_comment = "The price rises like ice spikes! ❄️"
            elif change_24h < 0:
                trend_comment = "A cold drop, but Sub-Zero sees opportunity in frozen markets! 🧊"
            else:
                trend_comment = "Steady as ice, mortal! ❄️"
            
            return f"""🧊 **Sub-Zero's Market Analysis** ❄️
            
**{name} ({symbol})**
💰 Current Price: ${price:,.2f}
{change_indicator} 24h Change: {change_text}
            
{trend_comment}
            
*Sub-Zero's wisdom: Keep your investments colder than my heart!* ❄️"""
        else:
            return f"""📊 **Crypto Price Update**
            
**{name} ({symbol})**
💰 Current Price: ${price:,.2f}
{change_indicator} 24h Change: {change_text}
📊 Market Cap: ${crypto_data.get('market_cap', 0):,.0f}
📈 Volume: ${crypto_data.get('volume', 0):,.0f}
            
*Data updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""
    
    def generate_response(self, user_input: str) -> Dict:
        """Generate appropriate response based on user input"""
        intent = self.detect_query_intent(user_input)
        
        if intent == 'personality_switch':
            # Extract mode from input
            text_lower = user_input.lower()
            if 'subzero' in text_lower or 'sub-zero' in text_lower:
                message = self.switch_personality('subzero')
            elif 'normal' in text_lower:
                message = self.switch_personality('normal')
            else:
                message = self.switch_personality()  # Toggle
            
            return {
                'type': 'personality_switch',
                'message': message,
                'action': 'show_response'
            }
        
        elif intent == 'price_query':
            crypto_name = self.extract_crypto_name(user_input)
            crypto_data = self.get_crypto_price(crypto_name)
            message = self.format_price_response(crypto_data, crypto_name)
            
            return {
                'type': 'price_query',
                'message': message,
                'action': 'show_price_data',
                'data': crypto_data
            }
        
        elif intent == 'news_query':
            crypto_name = self.extract_crypto_name(user_input)
            news_data = self.get_crypto_news(crypto_name)
            
            if self.personality_mode == "subzero":
                news_intro = f"🧊 Sub-Zero's frozen intel on {crypto_name}! ❄️\\n\\n"
            else:
                news_intro = f"📰 Latest news about {crypto_name}:\\n\\n"
            
            if news_data:
                news_text = news_intro
                for article in news_data:
                    news_text += f"• {article.get('title', 'News Update')}\\n"
                    if article.get('description'):
                        news_text += f"  {article['description'][:100]}...\\n\\n"
            else:
                news_text = "No recent news found. Check back later for updates!"
            
            return {
                'type': 'news_query',
                'message': news_text,
                'action': 'show_news',
                'data': news_data
            }
        
        elif intent == 'article_insight' or intent == 'insight_query':
            # Extract search terms from the query
            search_terms = self._extract_search_terms(user_input)
            
            if self.use_articles and self.article_manager:
                insights = self.article_manager.get_insights_from_articles(search_terms)
                
                if insights['found_articles']:
                    if self.personality_mode == "subzero":
                        intro = f"🧊 Sub-Zero's frozen knowledge reveals insights about {search_terms}! ❄️\\n\\n"
                    else:
                        intro = f"📚 **Insights from our knowledge base about {search_terms}:**\\n\\n"
                    
                    message = intro
                    message += f"📊 Found {insights['total_articles']} relevant articles\\n"
                    message += f"🎯 Overall sentiment: {insights['overall_sentiment']}\\n\\n"
                    
                    for i, article in enumerate(insights['articles'][:3], 1):  # Show top 3
                        message += f"**{i}. {article['title']}**\\n"
                        message += f"📝 {article['summary']}\\n"
                        if article['tags']:
                            message += f"🏷️ Tags: {', '.join(article['tags'])}\\n"
                        message += f"💭 Sentiment: {article['sentiment']['overall']}\\n\\n"
                    
                    if insights['key_themes']:
                        message += f"🔍 **Key themes:** {', '.join(insights['key_themes'])}\\n"
                    
                    return {
                        'type': 'article_insight',
                        'message': message,
                        'action': 'show_insights',
                        'data': insights
                    }
                else:
                    if self.personality_mode == "subzero":
                        message = f"❄️ Even Sub-Zero's frozen archives don't contain specific insights about {search_terms}! Try asking about Bitcoin, Ethereum, DeFi, or NFTs! 🧊"
                    else:
                        message = f"I don't have specific articles about {search_terms} in our knowledge base. Try asking about Bitcoin, Ethereum, DeFi, or NFT analysis!"
                    
                    return {
                        'type': 'article_insight',
                        'message': message,
                        'action': 'show_response'
                    }
            else:
                message = "Article insights are not available right now. Please try price queries or news instead!"
                return {
                    'type': 'general',
                    'message': message,
                    'action': 'show_response'
                }
        
        elif intent == 'greeting':
            if self.personality_mode == "subzero":
                message = random.choice(self.subzero_responses['greetings'])
            else:
                greetings = [
                    "Hello! I'm your crypto assistant. Ask me about prices, news, or switch to Sub-Zero mode!",
                    "Hi there! Ready to explore crypto markets? I can get real-time prices and news!",
                    "Welcome! I can help with crypto prices, market news, and insights. Try 'Sub-Zero mode' for a cool experience!"
                ]
                message = random.choice(greetings)
            
            return {
                'type': 'greeting',
                'message': message,
                'action': 'show_welcome'
            }
        
        elif intent == 'farewell':
            if self.personality_mode == "subzero":
                farewells = [
                    "Stay frosty, and may your crypto portfolio be as strong as ice! ❄️",
                    "Until next time, keep your investments colder than Sub-Zero's heart! 🧊",
                    "Farewell, mortal! Remember: HODL like ice - strong and unwavering! ❄️"
                ]
                message = random.choice(farewells)
            else:
                farewells = [
                    "Goodbye! Keep an eye on those crypto markets!",
                    "See you later! Remember to DYOR (Do Your Own Research)!",
                    "Take care! May your portfolio always be green! 📈"
                ]
                message = random.choice(farewells)            
            return {
                'type': 'farewell',
                'message': message,
                'action': 'show_farewell'
            }
        
        else:            # General conversation using training data
            if self.personality_mode == "subzero" and self.use_subzero_responses and self.subzero_trainer:                # Use Sub-Zero specific conversation training
                subzero_response = self.subzero_trainer.get_response(user_input)
                if subzero_response:
                    return {
                        'type': 'general',
                        'message': subzero_response,
                        'action': 'show_response'
                    }
            elif self.use_natural_responses and self.trainer:
                # Use regular conversation training for normal mode
                natural_response = self.trainer.get_response(user_input)
                if natural_response:
                    return {
                        'type': 'general',
                        'message': natural_response,
                        'action': 'show_response'
                    }
            
            # Fallback responses
            if self.personality_mode == "subzero":
                # Use Sub-Zero trainer for all responses
                if self.use_subzero_responses and self.subzero_trainer:
                    message = self.subzero_trainer.get_response(user_input)
                else:
                    fallbacks = [
                        "That's ice cold! How else can Sub-Zero assist you in the crypto realm? ❄️",
                        "Interesting question! Sub-Zero is here to help freeze your doubts! 🧊",
                        "Sub-Zero appreciates your curiosity - knowledge is power, like mastering ice! ❄️"
                    ]
                    message = random.choice(fallbacks)
            else:
                fallbacks = [
                    "I can help you with crypto prices, news, and market insights! Try asking 'What's the price of Bitcoin?'",
                    "Ask me about cryptocurrency prices, latest news, or switch to Sub-Zero mode for a cooler experience!",
                    "I'm here to help with crypto questions! You can also say 'Sub-Zero mode' to activate a special personality!"
                ]
                message = random.choice(fallbacks)
            
            return {
                'type': 'general',
                'message': message,
                'action': 'show_response'
            }

# Create a global chatbot instance
chatbot = EnhancedCryptoChatbot()
