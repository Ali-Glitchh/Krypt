from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from pycoingecko import CoinGeckoAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from datetime import datetime

# Initialize APIs
cg = CoinGeckoAPI()
analyzer = SentimentIntensityAnalyzer()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Get market data
        try:
            markets = cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=250,
                sparkline=False,
                price_change_percentage='24h'
            )
            self.wfile.write(json.dumps(markets).encode())
        except Exception as e:
            self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        return