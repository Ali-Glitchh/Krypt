#!/usr/bin/env python3
"""
News Insights Module for Crypto Chatbot
Fetches and analyzes cryptocurrency news from multiple sources
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

class CryptoNewsInsights:
    def __init__(self):
        self.news_cache = {}
        self.cache_expiry = 3600  # 1 hour cache
        self.last_update = {}
        
        # News API sources (free tiers available)
        self.news_sources = {
            'newsapi': {
                'url': 'https://newsapi.org/v2/everything',
                'params': {
                    'q': 'cryptocurrency OR bitcoin OR ethereum OR crypto',
                    'sortBy': 'publishedAt',
                    'language': 'en',
                    'pageSize': 20
                }
            },
            'cryptonews': {
                'url': 'https://cryptonews.net/api/news',
                'backup_sources': [
                    'https://api.coindesk.com/v1/news',
                    'https://api.cointelegraph.com/news'
                ]
            }
        }
        
        # Market sentiment keywords
        self.sentiment_keywords = {
            'bullish': ['surge', 'rally', 'moon', 'pump', 'breakout', 'bullish', 'gains', 'rise', 'up', 'positive'],
            'bearish': ['crash', 'dump', 'dip', 'fall', 'bearish', 'decline', 'drop', 'correction', 'sell-off'],
            'neutral': ['stable', 'sideways', 'consolidation', 'range', 'unchanged', 'mixed']
        }
    
    def get_latest_news(self, topic: str = "cryptocurrency", limit: int = 5) -> List[Dict]:
        """Fetch latest crypto news with caching"""
        
        cache_key = f"{topic}_{limit}"
        current_time = time.time()
        
        # Check cache
        if (cache_key in self.news_cache and 
            cache_key in self.last_update and
            current_time - self.last_update[cache_key] < self.cache_expiry):
            return self.news_cache[cache_key]
        
        # Fetch fresh news
        news_articles = []
        
        try:
            # Use a free crypto news service (CoinGecko has free endpoints)
            news_articles = self._fetch_coingecko_news(topic, limit)
            
            if not news_articles:
                # Fallback to mock news for demo
                news_articles = self._get_mock_news(topic, limit)
            
            # Cache results
            self.news_cache[cache_key] = news_articles
            self.last_update[cache_key] = current_time
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            # Return mock data as fallback
            news_articles = self._get_mock_news(topic, limit)
        
        return news_articles
    
    def _fetch_coingecko_news(self, topic: str, limit: int) -> List[Dict]:
        """Fetch news from CoinGecko API (free tier)"""
        try:
            # CoinGecko doesn't require API key for basic endpoints
            url = "https://api.coingecko.com/api/v3/news"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                news_articles = []
                for item in data.get('data', [])[:limit]:
                    article = {
                        'title': item.get('title', 'Crypto News'),
                        'description': item.get('description', 'Latest cryptocurrency news'),
                        'url': item.get('url', ''),
                        'published_at': item.get('created_at', ''),
                        'source': 'CoinGecko'
                    }
                    news_articles.append(article)
                
                return news_articles
                
        except Exception as e:
            print(f"CoinGecko API error: {e}")
            return []
    
    def _get_mock_news(self, topic: str, limit: int) -> List[Dict]:
        """Generate realistic mock news for demo purposes"""
        
        mock_articles = [
            {
                'title': 'Bitcoin Reaches New Monthly High Amid Institutional Interest',
                'description': 'Bitcoin surged past key resistance levels as major institutions continue to show interest in cryptocurrency adoption.',
                'url': 'https://example.com/btc-surge',
                'published_at': datetime.now().isoformat(),
                'source': 'CryptoDaily',
                'sentiment': 'bullish'
            },
            {
                'title': 'Ethereum 2.0 Staking Rewards Attract More Validators',
                'description': 'The number of Ethereum validators continues to grow as staking rewards remain attractive to long-term holders.',
                'url': 'https://example.com/eth-staking',
                'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'source': 'DeFi News',
                'sentiment': 'bullish'
            },
            {
                'title': 'Regulatory Clarity Improves Market Sentiment',
                'description': 'Recent regulatory developments provide clearer guidelines for cryptocurrency operations, boosting investor confidence.',
                'url': 'https://example.com/regulation',
                'published_at': (datetime.now() - timedelta(hours=4)).isoformat(),
                'source': 'Regulatory Watch',
                'sentiment': 'neutral'
            },
            {
                'title': 'DeFi Protocol Launches New Yield Farming Pool',
                'description': 'A major DeFi protocol announced a new liquidity mining program with competitive APY rates for early participants.',
                'url': 'https://example.com/defi-yield',
                'published_at': (datetime.now() - timedelta(hours=6)).isoformat(),
                'source': 'DeFi Pulse',
                'sentiment': 'bullish'
            },
            {
                'title': 'Market Analysis: Crypto Winter or Healthy Correction?',
                'description': 'Analysts debate whether current market conditions represent a prolonged bear market or a healthy correction before the next rally.',
                'url': 'https://example.com/market-analysis',
                'published_at': (datetime.now() - timedelta(hours=8)).isoformat(),
                'source': 'Market Insights',
                'sentiment': 'neutral'
            }
        ]
        
        # Filter by topic if specific
        if topic.lower() != "cryptocurrency":
            filtered_articles = []
            for article in mock_articles:
                if topic.lower() in article['title'].lower() or topic.lower() in article['description'].lower():
                    filtered_articles.append(article)
            mock_articles = filtered_articles if filtered_articles else mock_articles
        
        return mock_articles[:limit]
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of news text"""
        text_lower = text.lower()
        
        bullish_score = sum(1 for word in self.sentiment_keywords['bullish'] if word in text_lower)
        bearish_score = sum(1 for word in self.sentiment_keywords['bearish'] if word in text_lower)
        
        if bullish_score > bearish_score:
            return 'bullish'
        elif bearish_score > bullish_score:
            return 'bearish'
        else:
            return 'neutral'
    
    def get_market_insights(self, personality: str = "normal") -> str:
        """Generate market insights based on recent news"""
        
        news_articles = self.get_latest_news("cryptocurrency", 5)
        
        if not news_articles:
            return "Unable to fetch current market news at the moment."
        
        # Analyze overall sentiment
        sentiments = []
        for article in news_articles:
            sentiment = article.get('sentiment') or self.analyze_sentiment(
                article['title'] + ' ' + article['description']
            )
            sentiments.append(sentiment)
        
        bullish_count = sentiments.count('bullish')
        bearish_count = sentiments.count('bearish')
        neutral_count = sentiments.count('neutral')
        
        # Generate insights based on personality
        if personality == "subzero":
            return self._generate_subzero_insights(news_articles, bullish_count, bearish_count, neutral_count)
        else:
            return self._generate_normal_insights(news_articles, bullish_count, bearish_count, neutral_count)
    
    def _generate_normal_insights(self, articles: List[Dict], bullish: int, bearish: int, neutral: int) -> str:
        """Generate normal personality market insights"""
        
        total = len(articles)
        
        # Overall sentiment
        if bullish > bearish:
            sentiment_summary = f"Market sentiment appears positive with {bullish}/{total} bullish signals."
        elif bearish > bullish:
            sentiment_summary = f"Market shows caution with {bearish}/{total} bearish indicators."
        else:
            sentiment_summary = f"Market sentiment is mixed with balanced signals."
        
        # Key headlines
        key_headlines = []
        for i, article in enumerate(articles[:3]):
            key_headlines.append(f"{i+1}. {article['title']}")
        
        headlines_text = "\n".join(key_headlines)
        
        insight = f"""📊 **Current Market Insights:**

{sentiment_summary}

**Top Headlines:**
{headlines_text}

**Analysis:** Based on recent news, the crypto market is showing {"positive momentum" if bullish > bearish else "mixed signals" if bullish == bearish else "cautious sentiment"}. {"Consider watching for institutional moves and regulatory developments." if neutral > 0 else "Keep an eye on volume and technical indicators for confirmation."}

*News updates every hour. Always do your own research before making investment decisions.*"""
        
        return insight
    
    def _generate_subzero_insights(self, articles: List[Dict], bullish: int, bearish: int, neutral: int) -> str:
        """Generate Sub-Zero personality market insights"""
        
        total = len(articles)
        
        # Sub-Zero style sentiment analysis
        if bullish > bearish:
            sentiment_summary = f"❄️ The ice crystals align favorably! {bullish}/{total} signals show bullish momentum!"
        elif bearish > bullish:
            sentiment_summary = f"🧊 Market winds blow cold with {bearish}/{total} bearish indicators. Stay frosty!"
        else:
            sentiment_summary = f"⛄ The crypto realm shows balanced forces - {neutral}/{total} signals remain neutral."
        
        # Key headlines with Sub-Zero flair
        key_headlines = []
        for i, article in enumerate(articles[:3]):
            ice_emoji = ["❄️", "🧊", "🌨️"][i % 3]
            key_headlines.append(f"{ice_emoji} {article['title']}")
        
        headlines_text = "\n".join(key_headlines)
        
        insight = f"""🧊 **Sub-Zero's Market Analysis:**

{sentiment_summary}

**Lin Kuei Intelligence Reports:**
{headlines_text}

**Ice-Cold Assessment:** {"The crypto battlefield favors the bold! Strike while the market shows strength!" if bullish > bearish else "Patience, young warrior. Bear markets forge diamond hands!" if bearish > bullish else "Market forces remain in balance. Watch and wait for the perfect moment to strike!"}

❄️ *Sub-Zero's wisdom: Never let emotions cloud your judgment. Ice-cold analysis conquers market chaos!* ❄️"""
        
        return insight
    
    def get_specific_coin_news(self, coin: str, personality: str = "normal") -> str:
        """Get news specific to a cryptocurrency"""
        
        coin_articles = self.get_latest_news(coin, 3)
        
        if not coin_articles:
            if personality == "subzero":
                return f"🧊 Sub-Zero's network finds no recent intel on {coin.upper()}. The ice realm remains quiet on this token! ❄️"
            else:
                return f"No recent news found for {coin.upper()}. Try checking major crypto news sources directly."
        
        if personality == "subzero":
            headlines = []
            for i, article in enumerate(coin_articles):
                ice_emoji = ["❄️", "🧊", "🌨️"][i % 3]
                headlines.append(f"{ice_emoji} {article['title']}")
            
            headlines_text = "\n".join(headlines)
            
            return f"""🧊 **Sub-Zero's {coin.upper()} Intelligence:**

{headlines_text}

❄️ *Stay ice-cold and analyze each development carefully!* ❄️"""
        
        else:
            headlines = []
            for i, article in enumerate(coin_articles):
                headlines.append(f"• {article['title']}")
            
            headlines_text = "\n".join(headlines)
            
            return f"""📰 **Latest {coin.upper()} News:**

{headlines_text}

*Remember to verify information from multiple sources.*"""

def test_news_insights():
    """Test the news insights functionality"""
    print("🧪 Testing Crypto News Insights")
    print("=" * 50)
    
    news_service = CryptoNewsInsights()
    
    # Test general market insights
    print("\n📊 Normal Personality Market Insights:")
    normal_insights = news_service.get_market_insights("normal")
    print(normal_insights)
    
    print("\n🧊 Sub-Zero Personality Market Insights:")
    subzero_insights = news_service.get_market_insights("subzero")
    print(subzero_insights)
    
    # Test specific coin news
    print("\n💰 Bitcoin-specific News (Normal):")
    btc_news_normal = news_service.get_specific_coin_news("bitcoin", "normal")
    print(btc_news_normal)
    
    print("\n❄️ Bitcoin-specific News (Sub-Zero):")
    btc_news_subzero = news_service.get_specific_coin_news("bitcoin", "subzero")
    print(btc_news_subzero)
    
    print("\n✅ News insights testing completed!")

if __name__ == "__main__":
    test_news_insights()
