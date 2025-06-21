#!/usr/bin/env python3
"""
Article Manager for Crypto Chatbot
Manages custom articles for insights and analysis
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import requests
from pathlib import Path

class ArticleManager:
    def __init__(self, articles_directory: str = "articles"):
        """Initialize article manager with articles directory"""
        self.articles_dir = Path(articles_directory)
        self.articles_dir.mkdir(exist_ok=True)
        self.articles_file = self.articles_dir / "articles.json"
        self.articles = self._load_articles()
        
    def _load_articles(self) -> List[Dict]:
        """Load articles from JSON file"""
        if self.articles_file.exists():
            try:
                with open(self.articles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading articles: {e}")
                return []
        return []
    
    def _save_articles(self):
        """Save articles to JSON file"""
        try:
            with open(self.articles_file, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving articles: {e}")
    
    def add_article(self, title: str, content: str, category: str = "general", 
                   tags: List[str] = None, url: str = None) -> str:
        """Add a new article"""
        article_id = f"article_{len(self.articles) + 1}_{int(datetime.now().timestamp())}"
        
        article = {
            "id": article_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "url": url,
            "created_at": datetime.now().isoformat(),
            "word_count": len(content.split())
        }
        
        self.articles.append(article)
        self._save_articles()
        return article_id
    
    def get_article(self, article_id: str) -> Optional[Dict]:
        """Get article by ID"""
        for article in self.articles:
            if article["id"] == article_id:
                return article
        return None
    
    def search_articles(self, query: str, category: str = None) -> List[Dict]:
        """Search articles by content, title, or tags"""
        query_lower = query.lower()
        results = []
        
        for article in self.articles:
            # Check category filter
            if category and article.get("category", "").lower() != category.lower():
                continue
                
            # Search in title, content, and tags
            title_match = query_lower in article.get("title", "").lower()
            content_match = query_lower in article.get("content", "").lower()
            tag_match = any(query_lower in tag.lower() for tag in article.get("tags", []))
            
            if title_match or content_match or tag_match:
                # Calculate relevance score
                score = 0
                if title_match:
                    score += 3
                if content_match:
                    score += 1
                if tag_match:
                    score += 2
                    
                article_copy = article.copy()
                article_copy["relevance_score"] = score
                results.append(article_copy)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:5]  # Return top 5 results
    
    def get_articles_by_category(self, category: str) -> List[Dict]:
        """Get all articles in a category"""
        return [article for article in self.articles 
                if article.get("category", "").lower() == category.lower()]
    
    def get_recent_articles(self, limit: int = 5) -> List[Dict]:
        """Get most recent articles"""
        sorted_articles = sorted(self.articles, 
                               key=lambda x: x.get("created_at", ""), 
                               reverse=True)
        return sorted_articles[:limit]
    
    def get_article_summary(self, article: Dict) -> str:
        """Generate a summary of an article"""
        content = article.get("content", "")
        
        # Simple extractive summary - get first few sentences
        sentences = re.split(r'[.!?]+', content)
        summary_sentences = []
        word_count = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and word_count < 50:  # Limit to ~50 words
                summary_sentences.append(sentence)
                word_count += len(sentence.split())
            else:
                break
        
        summary = ". ".join(summary_sentences)
        if len(summary) > 200:
            summary = summary[:200] + "..."
            
        return summary
    
    def analyze_article_sentiment(self, article: Dict) -> Dict:
        """Analyze sentiment of article content"""
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            analyzer = SentimentIntensityAnalyzer()
            
            content = article.get("content", "")
            sentiment = analyzer.polarity_scores(content)
            
            # Determine overall sentiment
            compound = sentiment['compound']
            if compound >= 0.05:
                overall = "Positive"
            elif compound <= -0.05:
                overall = "Negative"
            else:
                overall = "Neutral"
            
            return {
                "overall": overall,
                "positive": sentiment['pos'],
                "negative": sentiment['neg'],
                "neutral": sentiment['neu'],
                "compound": compound
            }
        except ImportError:
            return {"overall": "Unknown", "error": "Sentiment analysis not available"}
    
    def get_insights_from_articles(self, query: str) -> Dict:
        """Get insights based on query from your articles"""
        relevant_articles = self.search_articles(query)
        
        if not relevant_articles:
            return {
                "found_articles": False,
                "message": "No relevant articles found in your knowledge base.",
                "suggestions": "Try different keywords or add more articles to expand insights."
            }
        
        insights = {
            "found_articles": True,
            "total_articles": len(relevant_articles),
            "articles": [],
            "key_themes": [],
            "overall_sentiment": "Neutral"
        }
        
        sentiments = []
        themes = set()
        
        for article in relevant_articles:
            article_insight = {
                "title": article.get("title", ""),
                "summary": self.get_article_summary(article),
                "category": article.get("category", ""),
                "tags": article.get("tags", []),
                "relevance_score": article.get("relevance_score", 0),
                "sentiment": self.analyze_article_sentiment(article)
            }
            
            insights["articles"].append(article_insight)
            
            # Collect sentiments and themes
            sentiment_data = article_insight["sentiment"]
            if "compound" in sentiment_data:
                sentiments.append(sentiment_data["compound"])
            
            themes.update(article.get("tags", []))
        
        # Calculate overall sentiment
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            if avg_sentiment >= 0.05:
                insights["overall_sentiment"] = "Positive"
            elif avg_sentiment <= -0.05:
                insights["overall_sentiment"] = "Negative"
            else:
                insights["overall_sentiment"] = "Neutral"
        
        insights["key_themes"] = list(themes)[:5]  # Top 5 themes
        
        return insights
    
    def load_sample_articles(self):
        """Load some sample crypto articles for demonstration"""
        sample_articles = [
            {
                "title": "Bitcoin's Market Dynamics: Understanding Price Volatility",
                "content": "Bitcoin continues to show significant price volatility, driven by various market factors including institutional adoption, regulatory news, and macroeconomic trends. Recent analysis shows that Bitcoin's correlation with traditional markets has increased, suggesting it's becoming more integrated into the broader financial ecosystem. Technical indicators suggest support levels around $60,000 with resistance near $110,000. Market sentiment remains cautiously optimistic as long-term holders continue to accumulate during price dips.",
                "category": "analysis",
                "tags": ["bitcoin", "volatility", "market-analysis", "technical-analysis"]
            },
            {
                "title": "Ethereum 2.0 Staking: A Comprehensive Guide",
                "content": "Ethereum's transition to Proof of Stake has opened new opportunities for passive income through staking. With current staking rewards around 4-6% annually, many investors are considering this as a long-term investment strategy. However, staking comes with risks including slashing penalties and liquidity constraints. This guide covers the technical requirements, risks, and potential rewards of Ethereum staking for both individual and institutional investors.",
                "category": "education",
                "tags": ["ethereum", "staking", "proof-of-stake", "passive-income"]
            },
            {
                "title": "DeFi Market Trends: Yield Farming and Liquidity Mining",
                "content": "Decentralized Finance continues to evolve with new yield farming opportunities and liquidity mining programs. Current yields in major protocols range from 5-15% APY, though higher yields often come with increased smart contract risks. The total value locked (TVL) in DeFi protocols has stabilized around $100 billion, indicating market maturation. New innovations in cross-chain protocols are creating opportunities for arbitrage and diversified yield strategies.",
                "category": "defi",
                "tags": ["defi", "yield-farming", "liquidity-mining", "tvl"]
            },
            {
                "title": "Regulatory Landscape: Global Crypto Adoption",
                "content": "Cryptocurrency regulation continues to evolve globally, with some countries embracing digital assets while others impose restrictions. The United States is working on comprehensive crypto legislation, while the European Union's MiCA regulation provides a framework for crypto operations. Regulatory clarity is generally positive for institutional adoption, though compliance costs may impact smaller projects. Market participants should stay informed about regulatory developments in their jurisdictions.",
                "category": "regulation",
                "tags": ["regulation", "compliance", "institutional-adoption", "policy"]
            },
            {
                "title": "NFT Market Analysis: Trends and Future Outlook",
                "content": "The NFT market has experienced significant consolidation, with trading volumes down from 2021 peaks but showing signs of stabilization. Utility-focused NFTs are gaining traction over speculative collections, with gaming and metaverse applications driving adoption. Price floors for major collections have stabilized, and the market is showing signs of maturation. New developments in NFT technology, including dynamic NFTs and improved marketplaces, are expected to drive future growth.",
                "category": "nft",
                "tags": ["nft", "digital-assets", "gaming", "metaverse"]
            }
        ]
        
        for article_data in sample_articles:
            self.add_article(
                title=article_data["title"],
                content=article_data["content"],
                category=article_data["category"],
                tags=article_data["tags"]
            )
        
        print(f"✅ Loaded {len(sample_articles)} sample articles")

# Example usage
if __name__ == "__main__":
    manager = ArticleManager()
    
    # Load sample articles if none exist
    if not manager.articles:
        manager.load_sample_articles()
    
    # Test search
    results = manager.search_articles("bitcoin price")
    print(f"Found {len(results)} articles about bitcoin price")
    
    # Test insights
    insights = manager.get_insights_from_articles("ethereum staking")
    print(f"Insights: {insights}")
