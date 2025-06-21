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
          # Market sentiment keywords with more nuanced analysis
        self.sentiment_keywords = {
            'bullish': {
                'strong': ['surge', 'rally', 'moon', 'breakout', 'explosion', 'skyrocket', 'soar'],
                'moderate': ['rise', 'gains', 'positive', 'bullish', 'optimistic', 'green', 'pump'],
                'weak': ['slight increase', 'modest gains', 'recovery', 'bounce']
            },
            'bearish': {
                'strong': ['crash', 'plummet', 'collapse', 'bloodbath', 'catastrophic', 'devastating'],
                'moderate': ['fall', 'decline', 'bearish', 'correction', 'sell-off', 'dump', 'red'],
                'weak': ['dip', 'pullback', 'slight decline', 'cooling']
            },
            'neutral': ['stable', 'sideways', 'consolidation', 'range', 'unchanged', 'mixed', 'flat']
        }
        
        # Technical analysis keywords
        self.technical_keywords = {
            'support': ['support', 'floor', 'buying interest', 'held above'],
            'resistance': ['resistance', 'ceiling', 'rejected at', 'struggle above'],
            'volume': ['volume', 'trading activity', 'liquidity', 'market participation'],
            'trend': ['trend', 'direction', 'momentum', 'moving average'],
            'pattern': ['pattern', 'formation', 'triangle', 'flag', 'head and shoulders']
        }
        
        # Fundamental analysis keywords
        self.fundamental_keywords = {
            'adoption': ['adoption', 'partnership', 'integration', 'mainstream', 'institutional'],
            'regulation': ['regulation', 'SEC', 'government', 'legal', 'compliance', 'policy'],
            'technology': ['upgrade', 'hard fork', 'scalability', 'consensus', 'blockchain'],
            'market_structure': ['ETF', 'derivatives', 'futures', 'options', 'custody']
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
    def analyze_sentiment(self, text: str) -> Dict:
        """Enhanced sentiment analysis with intensity and reasoning"""
        text_lower = text.lower()
        
        # Calculate sentiment scores with weights
        bullish_strong = sum(2 for word in self.sentiment_keywords['bullish']['strong'] if word in text_lower)
        bullish_moderate = sum(1 for word in self.sentiment_keywords['bullish']['moderate'] if word in text_lower)
        bullish_weak = sum(0.5 for word in self.sentiment_keywords['bullish']['weak'] if word in text_lower)
        
        bearish_strong = sum(2 for word in self.sentiment_keywords['bearish']['strong'] if word in text_lower)
        bearish_moderate = sum(1 for word in self.sentiment_keywords['bearish']['moderate'] if word in text_lower)
        bearish_weak = sum(0.5 for word in self.sentiment_keywords['bearish']['weak'] if word in text_lower)
        
        neutral_score = sum(1 for word in self.sentiment_keywords['neutral'] if word in text_lower)
        
        total_bullish = bullish_strong + bullish_moderate + bullish_weak
        total_bearish = bearish_strong + bearish_moderate + bearish_weak
        
        # Determine sentiment and intensity
        if total_bullish > total_bearish + neutral_score:
            if bullish_strong > 0:
                sentiment, intensity = 'bullish', 'strong'
            elif bullish_moderate > bullish_weak:
                sentiment, intensity = 'bullish', 'moderate'
            else:
                sentiment, intensity = 'bullish', 'weak'
        elif total_bearish > total_bullish + neutral_score:
            if bearish_strong > 0:
                sentiment, intensity = 'bearish', 'strong'
            elif bearish_moderate > bearish_weak:
                sentiment, intensity = 'bearish', 'moderate'
            else:
                sentiment, intensity = 'bearish', 'weak'
        else:
            sentiment, intensity = 'neutral', 'balanced'
        
        # Analyze technical and fundamental factors
        technical_factors = []
        for category, keywords in self.technical_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                technical_factors.append(category)
        
        fundamental_factors = []
        for category, keywords in self.fundamental_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                fundamental_factors.append(category)
        
        return {
            'sentiment': sentiment,
            'intensity': intensity,
            'bullish_score': total_bullish,
            'bearish_score': total_bearish,
            'technical_factors': technical_factors,
            'fundamental_factors': fundamental_factors
        }
    def get_market_insights(self, personality: str = "normal") -> str:
        """Generate enhanced market insights with deep analysis"""
        
        news_articles = self.get_latest_news("cryptocurrency", 5)
        
        if not news_articles:
            return "Unable to fetch current market news at the moment."
        
        # Enhanced sentiment analysis
        sentiment_analyses = []
        technical_factors = []
        fundamental_factors = []
        
        for article in news_articles:
            text = article['title'] + ' ' + article['description']
            analysis = self.analyze_sentiment(text)
            sentiment_analyses.append(analysis)
            technical_factors.extend(analysis['technical_factors'])
            fundamental_factors.extend(analysis['fundamental_factors'])
        
        # Aggregate analysis
        strong_bullish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bullish' and a['intensity'] == 'strong')
        moderate_bullish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bullish' and a['intensity'] == 'moderate')
        weak_bullish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bullish' and a['intensity'] == 'weak')
        
        strong_bearish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bearish' and a['intensity'] == 'strong')
        moderate_bearish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bearish' and a['intensity'] == 'moderate')
        weak_bearish = sum(1 for a in sentiment_analyses if a['sentiment'] == 'bearish' and a['intensity'] == 'weak')
        
        neutral_count = sum(1 for a in sentiment_analyses if a['sentiment'] == 'neutral')
        
        # Count factor occurrences
        tech_factor_counts = {factor: technical_factors.count(factor) for factor in set(technical_factors)}
        fund_factor_counts = {factor: fundamental_factors.count(factor) for factor in set(fundamental_factors)}
        
        # Generate personality-specific insights
        if personality == "subzero":
            return self._generate_enhanced_subzero_insights(
                news_articles, strong_bullish, moderate_bullish, weak_bullish,
                strong_bearish, moderate_bearish, weak_bearish, neutral_count,
                tech_factor_counts, fund_factor_counts
            )
        else:
            return self._generate_enhanced_normal_insights(
                news_articles, strong_bullish, moderate_bullish, weak_bullish,
                strong_bearish, moderate_bearish, weak_bearish, neutral_count,
                tech_factor_counts, fund_factor_counts
            )
    def _generate_enhanced_normal_insights(self, articles: List[Dict], strong_bull: int, mod_bull: int, weak_bull: int,
                                         strong_bear: int, mod_bear: int, weak_bear: int, neutral: int,
                                         tech_factors: Dict, fund_factors: Dict) -> str:
        """Generate enhanced normal personality market insights with deep analysis"""
        
        total = len(articles)
        total_bullish = strong_bull + mod_bull + weak_bull
        total_bearish = strong_bear + mod_bear + weak_bear
        
        # Overall sentiment with intensity
        if strong_bull > 0:
            sentiment_summary = f"📈 **STRONG BULLISH MOMENTUM** detected with {strong_bull} high-confidence signals!"
        elif total_bullish > total_bearish:
            intensity = "moderate" if mod_bull > weak_bull else "cautious"
            sentiment_summary = f"📊 Market shows {intensity} bullish sentiment ({total_bullish}/{total} positive signals)."
        elif strong_bear > 0:
            sentiment_summary = f"📉 **STRONG BEARISH PRESSURE** identified with {strong_bear} significant warning signals!"
        elif total_bearish > total_bullish:
            intensity = "moderate" if mod_bear > weak_bear else "mild"
            sentiment_summary = f"⚠️ Market displays {intensity} bearish sentiment ({total_bearish}/{total} negative indicators)."
        else:
            sentiment_summary = f"⚖️ Market sentiment is **BALANCED** with mixed signals across {total} data points."
        
        # Technical analysis insights
        tech_insights = []
        if 'support' in tech_factors and tech_factors['support'] > 1:
            tech_insights.append(f"🛡️ **Support levels** are being tested across multiple assets")
        if 'resistance' in tech_factors and tech_factors['resistance'] > 1:
            tech_insights.append(f"🚧 **Resistance zones** are limiting upward movement")
        if 'volume' in tech_factors and tech_factors['volume'] > 1:
            tech_insights.append(f"📊 **Volume analysis** suggests significant market participation")
        if 'trend' in tech_factors and tech_factors['trend'] > 1:
            tech_insights.append(f"📈 **Trend analysis** indicates directional momentum shifts")
        
        # Fundamental analysis insights
        fund_insights = []
        if 'adoption' in fund_factors and fund_factors['adoption'] > 0:
            fund_insights.append(f"🏢 **Institutional adoption** continues driving long-term value")
        if 'regulation' in fund_factors and fund_factors['regulation'] > 0:
            fund_insights.append(f"⚖️ **Regulatory developments** are shaping market structure")
        if 'technology' in fund_factors and fund_factors['technology'] > 0:
            fund_insights.append(f"🔧 **Technology upgrades** are enhancing network capabilities")
        if 'market_structure' in fund_factors and fund_factors['market_structure'] > 0:
            fund_insights.append(f"🏗️ **Market infrastructure** improvements support ecosystem growth")
        
        # Key headlines with analysis
        key_headlines = []
        for i, article in enumerate(articles[:3]):
            key_headlines.append(f"{i+1}. **{article['title']}**")
        
        headlines_text = "\n".join(key_headlines)
        
        # Strategic recommendations
        if total_bullish > total_bearish and strong_bull > 0:
            strategy = "🎯 **Strategic Outlook:** Strong momentum suggests potential continuation. Consider DCA strategies and risk management."
        elif total_bearish > total_bullish and strong_bear > 0:
            strategy = "🛡️ **Strategic Outlook:** High volatility expected. Focus on risk management and potential accumulation zones."
        else:
            strategy = "⚖️ **Strategic Outlook:** Mixed signals suggest range-bound action. Wait for clearer directional confirmation."
        
        # Technical factors summary
        tech_summary = f"**Technical Factors:** {', '.join(tech_insights) if tech_insights else 'Limited technical signals in current news cycle'}"
        
        # Fundamental factors summary  
        fund_summary = f"**Fundamental Drivers:** {', '.join(fund_insights) if fund_insights else 'Focus on price action and technical levels'}"
        
        insight = f"""📊 **COMPREHENSIVE MARKET ANALYSIS**

{sentiment_summary}

**📰 Key Market Headlines:**
{headlines_text}

{tech_summary}

{fund_summary}

{strategy}

**⏰ Analysis Timeframe:** Last hour • **🔄 Next Update:** 60 minutes
**📋 Disclaimer:** This analysis is for educational purposes. Always conduct your own research and manage risk appropriately."""
        
        return insight
    def _generate_enhanced_subzero_insights(self, articles: List[Dict], strong_bull: int, mod_bull: int, weak_bull: int,
                                          strong_bear: int, mod_bear: int, weak_bear: int, neutral: int,
                                          tech_factors: Dict, fund_factors: Dict) -> str:
        """Generate enhanced Sub-Zero personality market insights with ice-cold analysis"""
        
        total = len(articles)
        total_bullish = strong_bull + mod_bull + weak_bull
        total_bearish = strong_bear + mod_bear + weak_bear
        
        # Sub-Zero style sentiment analysis
        if strong_bull > 0:
            sentiment_summary = f"🧊 **THE ICE CRYSTALS SURGE WITH POWER!** {strong_bull} mighty bullish forces dominate the battlefield!"
        elif total_bullish > total_bearish:
            intensity = "moderate" if mod_bull > weak_bull else "patient"
            sentiment_summary = f"❄️ The frozen winds favor our advance! {total_bullish}/{total} signals show {intensity} bullish momentum!"
        elif strong_bear > 0:
            sentiment_summary = f"🌨️ **WINTER'S WRATH DESCENDS!** {strong_bear} powerful bearish storms threaten the realm!"
        elif total_bearish > total_bullish:
            intensity = "fierce" if mod_bear > weak_bear else "subtle"
            sentiment_summary = f"⛄ Cold winds blow against us with {intensity} bearish pressure ({total_bearish}/{total} warning signs)!"
        else:
            sentiment_summary = f"🧊 The realm stands in perfect balance - {neutral}/{total} forces remain neutral. The calm before the storm!"
        
        # Technical analysis with Sub-Zero flair
        ice_tech_insights = []
        if 'support' in tech_factors and tech_factors['support'] > 1:
            ice_tech_insights.append(f"🛡️ **Ice barriers hold strong** - support levels defend our positions!")
        if 'resistance' in tech_factors and tech_factors['resistance'] > 1:
            ice_tech_insights.append(f"⚔️ **Enemy fortifications** - resistance zones block our advance!")
        if 'volume' in tech_factors and tech_factors['volume'] > 1:
            ice_tech_insights.append(f"🌪️ **Battle intensity increases** - massive volume signals epic conflicts!")
        if 'trend' in tech_factors and tech_factors['trend'] > 1:
            ice_tech_insights.append(f"🧭 **The tide of war shifts** - trend momentum reveals the victor!")
        
        # Fundamental analysis with Lin Kuei intelligence
        lin_kuei_intel = []
        if 'adoption' in fund_factors and fund_factors['adoption'] > 0:
            lin_kuei_intel.append(f"🏰 **New allies join our cause** - institutional adoption strengthens our forces!")
        if 'regulation' in fund_factors and fund_factors['regulation'] > 0:
            lin_kuei_intel.append(f"⚖️ **Elder gods speak** - regulatory changes reshape the battlefield!")
        if 'technology' in fund_factors and fund_factors['technology'] > 0:
            lin_kuei_intel.append(f"🔨 **Ancient weapons upgraded** - technology advances grant new powers!")
        if 'market_structure' in fund_factors and fund_factors['market_structure'] > 0:
            lin_kuei_intel.append(f"🏗️ **The arena transforms** - market structure evolution favors the prepared!")
        
        # Key headlines with ice-cold analysis
        ice_headlines = []
        ice_emojis = ["❄️", "🧊", "🌨️"]
        for i, article in enumerate(articles[:3]):
            emoji = ice_emojis[i % 3]
            ice_headlines.append(f"{emoji} **{article['title']}**")
        
        headlines_text = "\n".join(ice_headlines)
        
        # Sub-Zero's strategic wisdom
        if total_bullish > total_bearish and strong_bull > 0:
            strategy = f"⚔️ **SUB-ZERO'S BATTLE PLAN:** The frozen currents surge with power! Strike decisively while momentum favors the bold!"
        elif total_bearish > total_bullish and strong_bear > 0:
            strategy = f"🛡️ **SUB-ZERO'S DEFENSE:** Winter's storm approaches! Fortify positions and prepare for the ice to crack!"
        else:
            strategy = f"🧊 **SUB-ZERO'S PATIENCE:** The wise warrior waits in the shadows. Let the weak reveal themselves before we strike!"
        
        # Lin Kuei intelligence summary
        tech_summary = f"**🥷 Lin Kuei Technical Analysis:** {' | '.join(ice_tech_insights) if ice_tech_insights else 'The shadows reveal no clear patterns - watch and wait!'}"
        
        # Elder intelligence summary
        fund_summary = f"**👤 Elder Gods' Wisdom:** {' | '.join(lin_kuei_intel) if lin_kuei_intel else 'Focus on the battle at hand - let combat skills decide victory!'}"
        
        insight = f"""🧊 **SUB-ZERO'S COMPREHENSIVE BATTLEFIELD ANALYSIS**

{sentiment_summary}

**❄️ Lin Kuei Intelligence Reports:**
{headlines_text}

{tech_summary}

{fund_summary}

{strategy}

**⏰ Intelligence Update:** Hourly surveillance • **🕵️ Next Report:** 60 minutes
**❄️ Sub-Zero's Code:** "Patience and precision conquer market chaos. Never let emotion cloud your frozen judgment!" ❄️"""
        
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
