from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pycoingecko import CoinGeckoAPI
import requests
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize APIs
cg = CoinGeckoAPI()
analyzer = SentimentIntensityAnalyzer()

# Cache for API responses
cache = {}
CACHE_DURATION = 300  # 5 minutes

def get_cached_or_fetch(key, fetch_func):
    if key in cache:
        cached_data, timestamp = cache[key]
        if time.time() - timestamp < CACHE_DURATION:
            return cached_data
    
    data = fetch_func()
    cache[key] = (data, time.time())
    return data

def analyze_sentiment(text, coin_name):
    relevant_terms = {
        'bullish': 2.0,
        'bearish': -2.0,
        'surge': 1.5,
        'plunge': -1.5,
        'gain': 1.0,
        'loss': -1.0,
        'high': 0.5,
        'low': -0.5,
        'up': 0.3,
        'down': -0.3,
    }
    base_sentiment = analyzer.polarity_scores(text)
    score = base_sentiment['compound']
    text_lower = text.lower()
    for term, weight in relevant_terms.items():
        if term in text_lower and coin_name in text_lower:
            score += weight
    return max(min(score, 1.0), -1.0)

@app.route('/api/markets', methods=['GET'])
def get_markets():
    """Get top cryptocurrencies by market cap"""
    try:
        def fetch_markets():
            return cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=100,
                sparkline=False,
                price_change_percentage='24h'
            )
        
        markets = get_cached_or_fetch('markets', fetch_markets)
        return jsonify(markets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a specific cryptocurrency"""
    try:
        data = request.get_json()
        
        if not data or 'coin_id' not in data:
            return jsonify({'error': 'No coin_id provided'}), 400

        coin_id = data['coin_id']
        
        # Get market data
        market_data = cg.get_coin_by_id(
            coin_id,
            localization=False,
            tickers=False,
            market_data=True,
            community_data=False,
            developer_data=False
        )

        # Get news
        news_items = []
        try:
            crypto_compare_url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={coin_id}"
            news_response = requests.get(crypto_compare_url, timeout=5)
            if news_response.status_code == 200:
                news_data = news_response.json()
                for item in news_data.get('Data', [])[:10]:
                    if item.get('title'):
                        text = item.get('title', '') + ' ' + item.get('body', '')
                        sentiment = analyze_sentiment(text, coin_id)
                        timestamp = datetime.fromtimestamp(item.get('published_on', 0))
                        news_items.append({
                            'title': item.get('title'),
                            'source': item.get('source'),
                            'url': item.get('url'),
                            'sentiment': sentiment,
                            'published': timestamp.isoformat()
                        })
        except Exception as e:
            print(f"Error fetching news: {e}")

        # Calculate overall sentiment
        overall_sentiment = 0
        if news_items:
            total_sentiment = sum(item['sentiment'] for item in news_items)
            overall_sentiment = total_sentiment / len(news_items)
        
        price_change = market_data['market_data']['price_change_percentage_24h']
        
        # Investment sentiment calculation
        total_score = (0.4 * overall_sentiment + 0.4 * (price_change / 10))
        
        if total_score > 0.5:
            sentiment_status = "Strong Positive"
            sentiment_message = "Market indicators suggest strong positive sentiment."
        elif total_score > 0.2:
            sentiment_status = "Positive"
            sentiment_message = "Market indicators are positive."
        elif total_score > -0.2:
            sentiment_status = "Neutral"
            sentiment_message = "Market indicators are mixed."
        elif total_score > -0.5:
            sentiment_status = "Negative"
            sentiment_message = "Market indicators show concerning signals."
        else:
            sentiment_status = "Strong Negative"
            sentiment_message = "Market indicators suggest strong negative sentiment."

        response = {
            'coin': {
                'id': market_data['id'],
                'name': market_data['name'],
                'symbol': market_data['symbol'].upper(),
                'image': market_data['image']['large']
            },
            'market_data': {
                'current_price': market_data['market_data']['current_price']['usd'],
                'price_change_24h': price_change,
                'market_cap': market_data['market_data']['market_cap']['usd'],
                'total_volume': market_data['market_data']['total_volume']['usd'],
                'market_cap_rank': market_data['market_cap_rank']
            },
            'sentiment': {
                'score': overall_sentiment,
                'status': sentiment_status,
                'message': sentiment_message
            },
            'news': news_items
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    """Search for cryptocurrencies"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        results = cg.search(query)
        coins = results.get('coins', [])[:10]
        return jsonify({
            'results': [
                {
                    'id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'thumb': coin['thumb']
                }
                for coin in coins
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

# Vercel requires the app to be exposed as 'app'
# for the serverless function to work
handler = app