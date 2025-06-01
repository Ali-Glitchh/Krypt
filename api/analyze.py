from http.server import BaseHTTPRequestHandler
import json
from pycoingecko import CoinGeckoAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests

# Initialize APIs
cg = CoinGeckoAPI()
analyzer = SentimentIntensityAnalyzer()

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

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('query', '').lower()
            
            # Extract cryptocurrency name
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
                'chainlink': ['link', 'chainlink'],
                'uniswap': ['uni', 'uniswap']
            }

            coin_id = None
            for official_name, patterns in coin_patterns.items():
                if any(pattern in query for pattern in patterns):
                    coin_id = official_name
                    break

            if not coin_id:
                # Try to search
                try:
                    search_results = cg.search(query)
                    if search_results and search_results['coins']:
                        coin_id = search_results['coins'][0]['id']
                except:
                    pass

            if not coin_id:
                self.send_error(404, 'Cryptocurrency not found')
                return

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
                    for item in news_data.get('Data', [])[:5]:
                        text = item.get('title', '') + ' ' + item.get('body', '')
                        sentiment = analyze_sentiment(text, coin_id)
                        news_items.append({
                            'title': item.get('title'),
                            'source': item.get('source'),
                            'link': item.get('url'),
                            'sentiment': sentiment
                        })
            except:
                pass

            # Calculate overall sentiment
            overall_sentiment = 0
            if news_items:
                overall_sentiment = sum(item['sentiment'] for item in news_items) / len(news_items)
            
            sentiment_interpretation = 'Bullish' if overall_sentiment > 0.2 else 'Bearish' if overall_sentiment < -0.2 else 'Neutral'

            # Get investment sentiment
            price_change = market_data['market_data']['price_change_percentage_24h'] or 0
            volume_change = 0  # Would need historical data to calculate
            
            total_score = (
                0.4 * overall_sentiment +
                0.4 * (price_change / 10) +
                0.2 * (volume_change / 100)
            )

            if total_score > 0.5:
                sentiment_status = "Strong Positive"
                sentiment_message = "Market indicators suggest strong positive sentiment, but remember to do your own research."
            elif total_score > 0.2:
                sentiment_status = "Positive"
                sentiment_message = "Market indicators are positive, but cryptocurrency markets are highly volatile."
            elif total_score > -0.2:
                sentiment_status = "Neutral"
                sentiment_message = "Market indicators are mixed. Consider monitoring for clearer signals."
            elif total_score > -0.5:
                sentiment_status = "Negative"
                sentiment_message = "Market indicators show some concerning signals. Exercise caution."
            else:
                sentiment_status = "Strong Negative"
                sentiment_message = "Market indicators suggest strong negative sentiment. High risk environment."

            response = {
                'market_data': {
                    'name': market_data['name'],
                    'symbol': market_data['symbol'].upper(),
                    'current_price': market_data['market_data']['current_price']['usd'],
                    'price_change_24h': market_data['market_data']['price_change_percentage_24h'] or 0,
                    'total_volume': market_data['market_data']['total_volume']['usd'],
                    'market_cap': market_data['market_data']['market_cap']['usd']
                },
                'sentiment_analysis': {
                    'score': overall_sentiment,
                    'interpretation': sentiment_interpretation,
                    'status': sentiment_status,
                    'message': sentiment_message,
                    'confidence': {
                        'level': 'High' if len(news_items) >= 3 else 'Medium' if news_items else 'Low'
                    }
                },
                'news': news_items
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())