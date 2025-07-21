#!/usr/bin/env python3
"""
Enhanced Response Generator for KoinToss AI
Improves answering capabilities and adds sentiment analysis integration
"""

import json
import re
import random
from typing import Dict, List, Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EnhancedResponseGenerator:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.crypto_keywords = self._load_crypto_keywords()
        self.enhanced_responses = self._load_enhanced_responses()
        
    def _load_crypto_keywords(self) -> Dict:
        """Load crypto-specific keywords for better context understanding"""
        return {
            'price_queries': ['price', 'cost', 'value', 'worth', 'trading', 'market cap'],
            'technical_queries': ['how', 'what', 'explain', 'define', 'meaning', 'work'],
            'investment_queries': ['buy', 'sell', 'invest', 'trade', 'portfolio', 'hodl'],
            'sentiment_queries': ['opinion', 'think', 'predict', 'future', 'forecast'],
            'bullish_terms': ['moon', 'rocket', 'hodl', 'diamond hands', 'bullish', 'pump', 'surge', 'rally', 'bull run'],
            'bearish_terms': ['dump', 'crash', 'bear', 'dip', 'fud', 'panic', 'sell off', 'decline', 'bear market'],
            'crypto_coins': ['bitcoin', 'btc', 'ethereum', 'eth', 'dogecoin', 'doge', 'ada', 'cardano', 'solana', 'sol']
        }
    
    def _load_enhanced_responses(self) -> List[Dict]:
        """Load enhanced response templates"""
        return [
            {
                "pattern": r"price of (bitcoin|btc)",
                "response_template": "💰 **Bitcoin Price Analysis**\n\nBitcoin is currently trading around ${price}. Here's what you need to know:\n\n🔹 **Market Position**: Bitcoin remains the dominant cryptocurrency\n🔹 **Volatility**: Prices can change rapidly - always DYOR\n🔹 **Investment Tip**: Consider dollar-cost averaging for long-term positions\n\n*Remember: Crypto is highly volatile. Never invest more than you can afford to lose!*",
                "personality": "educational"
            },
            {
                "pattern": r"what is (bitcoin|btc)",
                "response_template": "🪙 **Bitcoin - The Digital Gold**\n\nBitcoin (BTC) is the world's first cryptocurrency, created in 2009 by Satoshi Nakamoto. Here's why it matters:\n\n✨ **Key Features**:\n• Limited supply: Only 21 million coins ever\n• Decentralized: No government or bank control\n• Secure: Protected by blockchain technology\n• Global: 24/7 trading worldwide\n\n🎯 **Why it's called 'Digital Gold'**:\n• Store of value properties\n• Hedge against inflation\n• Growing institutional adoption\n\n*Bitcoin started the entire crypto revolution and remains the most trusted digital asset!*",
                "personality": "educational"
            }
        ]
    
    def analyze_user_sentiment(self, user_input: str) -> Dict:
        """Analyze sentiment of user input with crypto-specific context"""
        scores = self.sentiment_analyzer.polarity_scores(user_input)
        
        # Add crypto-specific sentiment analysis
        user_lower = user_input.lower()
        crypto_sentiment_bonus = 0
        
        for term in self.crypto_keywords['bullish_terms']:
            if term in user_lower:
                crypto_sentiment_bonus += 0.1
                
        for term in self.crypto_keywords['bearish_terms']:
            if term in user_lower:
                crypto_sentiment_bonus -= 0.1
        
        final_compound = max(-1, min(1, scores['compound'] + crypto_sentiment_bonus))
        
        return {
            'compound': final_compound,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'crypto_sentiment': crypto_sentiment_bonus,
            'sentiment_label': self._get_sentiment_label(final_compound)
        }
    
    def _get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to readable sentiment label"""
        if compound_score >= 0.05:
            return "bullish"
        elif compound_score <= -0.05:
            return "bearish"
        else:
            return "neutral"
    
    def detect_query_type(self, user_input: str) -> str:
        """Detect the type of query to provide more targeted responses"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in self.crypto_keywords['price_queries']):
            return "price_query"
        elif any(word in user_lower for word in self.crypto_keywords['technical_queries']):
            return "technical_query"
        elif any(word in user_lower for word in self.crypto_keywords['investment_queries']):
            return "investment_query"
        elif any(word in user_lower for word in self.crypto_keywords['sentiment_queries']):
            return "sentiment_query"
        else:
            return "general_query"
    
    def enhance_response(self, base_response: str, user_input: str, personality: str = "normal") -> Dict:
        """Enhance a base response with sentiment analysis and additional context"""
        
        # Analyze user sentiment
        sentiment_analysis = self.analyze_user_sentiment(user_input)
        query_type = self.detect_query_type(user_input)
        
        # Enhance response based on personality and sentiment
        if personality == "normal":
            enhanced_response = self._enhance_educational_response(
                base_response, sentiment_analysis, query_type, user_input
            )
        else:  # subzero personality
            enhanced_response = self._enhance_warrior_response(
                base_response, sentiment_analysis, query_type, user_input
            )
        
        return {
            'message': enhanced_response,
            'personality': personality,
            'type': f'{personality}_enhanced',
            'confidence': 0.9,
            'sentiment_analysis': sentiment_analysis,
            'query_type': query_type,
            'enhancements_applied': True
        }
    
    def _enhance_educational_response(self, base_response: str, sentiment: Dict, query_type: str, user_input: str) -> str:
        """Enhance response for educational personality"""
        
        # Add sentiment-aware introduction
        if sentiment['sentiment_label'] == 'bullish':
            intro = "🚀 I can sense your enthusiasm for crypto! "
        elif sentiment['sentiment_label'] == 'bearish':
            intro = "📉 I understand your concerns about the market. "
        else:
            intro = "💡 Great question! "
        
        # Add query-type specific enhancements
        if query_type == "price_query":
            footer = "\n\n💡 **Pro Tip**: Remember that crypto prices are highly volatile. Always do your own research and never invest more than you can afford to lose!"
        elif query_type == "investment_query":
            footer = "\n\n⚠️ **Investment Disclaimer**: This is educational information, not financial advice. Please consult with a financial advisor before making investment decisions."
        elif query_type == "technical_query":
            footer = "\n\n🔍 **Want to Learn More?** Feel free to ask follow-up questions - I'm here to help you understand crypto better!"
        else:
            footer = "\n\n🎯 **KoinToss Tip**: Switch to Warrior mode (type 'switch to subzero') for more aggressive market analysis!"
        
        return f"{intro}{base_response}{footer}"
    
    def _enhance_warrior_response(self, base_response: str, sentiment: Dict, query_type: str, user_input: str) -> str:
        """Enhance response for warrior (subzero) personality"""
        
        # Add aggressive sentiment-aware introduction
        if sentiment['sentiment_label'] == 'bullish':
            intro = "⚔️ YOUR BULLISH ENERGY IS DETECTED! "
        elif sentiment['sentiment_label'] == 'bearish':
            intro = "🧊 FEELING THE MARKET FREEZE? "
        else:
            intro = "❄️ COLD ANALYSIS INCOMING! "
        
        # Add warrior-style enhancements
        if query_type == "price_query":
            footer = "\n\n💎 **WARRIOR CODE**: Prices are for the WEAK! True warriors HODL through the storms and emerge VICTORIOUS!"
        elif query_type == "investment_query":
            footer = "\n\n⚔️ **BATTLE STRATEGY**: Only invest what you can afford to LOSE in BATTLE! The crypto realm shows NO MERCY to the unprepared!"
        elif query_type == "technical_query":
            footer = "\n\n🧊 **ICE-COLD TRUTH**: Knowledge is POWER! Master the fundamentals and you'll DOMINATE the markets!"
        else:
            footer = "\n\n❄️ **SUB-ZERO'S WISDOM**: Switch to Educational mode if you need gentler guidance, but WARRIORS learn through ICE and FIRE!"
        
        return f"{intro}{base_response.upper()}{footer}"

# Test the enhanced response generator
if __name__ == "__main__":
    generator = EnhancedResponseGenerator()
    
    test_queries = [
        ("price of bitcoin", "normal"),
        ("WHAT IS BITCOIN?", "subzero"),
        ("I'm worried about my crypto investments", "normal"),
        ("Bitcoin is going to the moon!", "subzero")
    ]
    
    for query, personality in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"Personality: {personality}")
        
        base_response = "Bitcoin is a cryptocurrency created in 2009."
        enhanced = generator.enhance_response(base_response, query, personality)
        
        print(f"Enhanced Response:\n{enhanced['message']}")
        print(f"Sentiment: {enhanced['sentiment_analysis']['sentiment_label']}")
        print(f"Query Type: {enhanced['query_type']}")
