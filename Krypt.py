from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from pycoingecko import CoinGeckoAPI
import feedparser
import praw
import requests
import re
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins with additional options
CORS(app, resources={
    r"/*": {
        "origins": ["*", "file://", "null"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
        "supports_credentials": True
    }
})

# Initialize APIs
try:
    cg = CoinGeckoAPI()
    analyzer = SentimentIntensityAnalyzer()
    logger.info("APIs initialized successfully")
except Exception as e:
    logger.error(f"Error initializing APIs: {str(e)}")
    raise

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:
        logger.debug("Received analyze request")
        data = request.get_json()
        
        if not data or 'query' not in data:
            logger.error("No query provided in request")
            return jsonify({'error': 'No query provided'}), 400

        query = data['query'].lower()
        logger.debug(f"Processing query: {query}")

        try:
            # Extract cryptocurrency name from query
            crypto_name = query.lower()
            coin_patterns = {
                'bitcoin': ['bitcoin', 'btc', 'xbt'],
                'ethereum': ['ethereum', 'eth', 'ether'],
                'cardano': ['cardano', 'ada'],
                'binancecoin': ['bnb', 'binance coin'],
                'solana': ['solana', 'sol'],
                'ripple': ['ripple', 'xrp'],
                'dogecoin': ['dogecoin', 'doge'],
                'polkadot': ['polkadot', 'dot'],
                'matic-network': ['polygon', 'matic'],
                'avalanche-2': ['avalanche', 'avax'],
                'sui': ['sui', 'sui coin', 'sui token'],
                'uniswap': ['uni', 'uniswap'],
                'chainlink': ['link', 'chainlink'],
                'near': ['near', 'near protocol'],
                'internet-computer': ['icp', 'internet computer'],
                'optimism': ['op', 'optimism'],
                'arbitrum': ['arb', 'arbitrum']
            }

            coin_id = None
            for official_name, patterns in coin_patterns.items():
                if any(pattern in crypto_name for pattern in patterns):
                    coin_id = official_name
                    break

            if not coin_id:
                # Try to search CoinGecko API for the coin
                try:
                    # First try an exact search
                    search_results = cg.search(crypto_name)
                    if search_results and search_results['coins']:
                        # Try to find exact match first
                        for coin in search_results['coins']:
                            if coin['name'].lower() == crypto_name or coin['symbol'].lower() == crypto_name:
                                coin_id = coin['id']
                                break
                        # If no exact match, use the first result
                        if not coin_id and search_results['coins']:
                            coin_id = search_results['coins'][0]['id']
                            logger.info(f"Using best match for '{crypto_name}': {coin_id}")
                except Exception as e:
                    logger.error(f"Error searching for coin: {str(e)}")

            if not coin_id:
                suggestions = []
                try:
                    search_results = cg.search(crypto_name)
                    if search_results and search_results['coins']:
                        suggestions = [f"{coin['name']} ({coin['symbol'].upper()})"
                                     for coin in search_results['coins'][:3]]
                except:
                    pass
                
                error_msg = f"Could not find cryptocurrency: {query}"
                if suggestions:
                    error_msg += f"\n\nDid you mean one of these?\n- " + "\n- ".join(suggestions)
                return jsonify({
                    'error': error_msg,
                    'suggestions': suggestions
                }), 404

            # Track news fetch success
            news_sources_attempted = 0
            news_sources_successful = 0

            # Get market data from CoinGecko
            market_data = cg.get_coin_by_id(
                coin_id,
                localization=False,
                tickers=False,
                market_data=True,
                community_data=False,
                developer_data=False
            )

            # Initialize news items list
            news_items = []
            
            # Function to analyze sentiment with context
            def analyze_sentiment(text, coin_name):
                # Add more context for better sentiment analysis
                relevant_terms = {
                    'bullish': 2.0,
                    'bearish': -2.0,
                    'surge': 1.5,
                    'plunge': -1.5,
                    'gain': 1.0,
                    'loss': -1.0,
                    'high': 0.5,
                    'low': -0.5
                }
                
                base_sentiment = analyzer.polarity_scores(text)
                score = base_sentiment['compound']
                
                # Adjust score based on relevant terms
                text_lower = text.lower()
                for term, weight in relevant_terms.items():
                    if term in text_lower and coin_name in text_lower:
                        score += weight
                
                return max(min(score, 1.0), -1.0)  # Normalize between -1 and 1

            # Define source credibility ratings
            source_ratings = {
                'CryptoCompare': {'weight': 1.5, 'type': 'Primary Data Provider'},
                'CoinDesk': {'weight': 1.3, 'type': 'Major Publication'},
                'Cointelegraph': {'weight': 1.2, 'type': 'Major Publication'}
            }

            # CryptoCompare News API (free)
            news_sources_attempted += 1
            try:
                crypto_compare_url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={coin_id}"
                news_response = requests.get(crypto_compare_url, timeout=5)
                if news_response.status_code == 200:
                    news_data = news_response.json()
                    for item in news_data.get('Data', [])[:5]:
                        if item.get('title') and item.get('source'):
                            text = item.get('title', '') + ' ' + item.get('body', '')
                            sentiment = analyze_sentiment(text, coin_id)
                            timestamp = datetime.fromtimestamp(item.get('published_on', 0))
                            news_items.append({
                                'title': item.get('title'),
                                'source': item.get('source'),
                                'link': item.get('url'),
                                'sentiment': sentiment,
                                'published': timestamp.isoformat(),
                                'sourceRating': 'Primary Data Provider',
                                'weight': source_ratings['CryptoCompare']['weight']
                            })
                    news_sources_successful += 1
            except Exception as e:
                logger.error(f"Error fetching CryptoCompare news: {str(e)}")

            # Coindesk RSS Feed
            news_sources_attempted += 1
            try:
                feed_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
                feed = feedparser.parse(feed_url)
                relevant_count = 0
                for item in feed.entries:
                    if relevant_count >= 5:
                        break
                    if coin_id.lower() in item.title.lower() or coin_id.lower() in item.description.lower():
                        text = item.title + ' ' + item.description
                        sentiment = analyze_sentiment(text, coin_id)
                        try:
                            timestamp = datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z")
                        except:
                            timestamp = datetime.now()
                        news_items.append({
                            'title': item.title,
                            'source': 'CoinDesk',
                            'link': item.link,
                            'sentiment': sentiment,
                            'published': timestamp.isoformat(),
                            'sourceRating': 'Major Publication',
                            'weight': source_ratings['CoinDesk']['weight']
                        })
                        relevant_count += 1
                if relevant_count > 0:
                    news_sources_successful += 1
            except Exception as e:
                logger.error(f"Error fetching Coindesk news: {str(e)}")

            # Cointelegraph RSS Feed
            news_sources_attempted += 1
            try:
                feed_url = "https://cointelegraph.com/rss"
                feed = feedparser.parse(feed_url)
                relevant_count = 0
                for item in feed.entries:
                    if relevant_count >= 5:
                        break
                    if coin_id.lower() in item.title.lower() or coin_id.lower() in item.description.lower():
                        text = item.title + ' ' + item.description
                        sentiment = analyze_sentiment(text, coin_id)
                        try:
                            timestamp = datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z")
                        except:
                            timestamp = datetime.now()
                        news_items.append({
                            'title': item.title,
                            'source': 'Cointelegraph',
                            'link': item.link,
                            'sentiment': sentiment,
                            'published': timestamp.isoformat(),
                            'sourceRating': 'Major Publication',
                            'weight': source_ratings['Cointelegraph']['weight']
                        })
                        relevant_count += 1
                if relevant_count > 0:
                    news_sources_successful += 1
            except Exception as e:
                logger.error(f"Error fetching Cointelegraph news: {str(e)}")

            # Prepare metrics and final response
            if news_items:
                # Sort by published date
                news_items = sorted(news_items, key=lambda x: x.get('published', ''), reverse=True)[:10]  # Keep only 10 most recent

                # Calculate weighted sentiment
                total_weighted_sentiment = 0
                
                # Prepare analysis quality metrics
                analysis_quality = "High" if news_sources_successful >= 2 else "Medium" if news_sources_successful == 1 else "Low"
                data_freshness = "Recent" if any(
                    item.get('published', '') > (datetime.now() - timedelta(hours=24)).isoformat()
                    for item in news_items
                ) else "Older"
                total_weight = 0
                for item in news_items:
                    weight = item.get('weight', 1.0)
                    total_weighted_sentiment += item['sentiment'] * weight
                    total_weight += weight
                
                overall_sentiment = total_weighted_sentiment / total_weight
                sentiment_interpretation = 'Bullish' if overall_sentiment > 0.2 else 'Bearish' if overall_sentiment < -0.2 else 'Neutral'
            else:
                overall_sentiment = 0
                sentiment_interpretation = 'Neutral'

            response = {
                'market_data': {
                    'name': market_data['name'],
                    'symbol': market_data['symbol'].upper(),
                    'current_price': market_data['market_data']['current_price']['usd'],
                    'price_change_24h': market_data['market_data']['price_change_percentage_24h'],
                    'total_volume': market_data['market_data']['total_volume']['usd'],
                    'market_cap': market_data['market_data']['market_cap']['usd'],
                    'last_updated': market_data['market_data']['last_updated']
                },
                'sentiment_analysis': {
                    'score': overall_sentiment,
                    'interpretation': sentiment_interpretation,
                    'strength': abs(overall_sentiment),
                    'confidence': {
                        'level': analysis_quality,
                        'sources_attempted': news_sources_attempted,
                        'sources_successful': news_sources_successful,
                        'data_freshness': data_freshness
                    }
                },
                'news': news_items
            }

            logger.debug("Returning real market data and news")
            return jsonify(response)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({'error': f'Error processing request: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def index():
    """Serve the main application page."""
    return send_file('example.html')

# Create app instance for Vercel
app.debug = False

# Handler for Vercel serverless function
def handler(request):
    with app.request_context(request):
        return app.full_dispatch_request()

if __name__ == '__main__':
    logger.info(" * Starting Crypto Sentiment Analysis Server...")
    app.run(host='0.0.0.0', port=5000)
