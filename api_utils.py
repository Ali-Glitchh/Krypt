import time
from pycoingecko import CoinGeckoAPI
from kucoin.client import Market
from binance.client import Client
import streamlit as st

RATE_LIMIT_DELAY = 1.5  # seconds between API calls

class CryptoAPIs:
    def __init__(self):
        self.apis = {}
        self.initialize_apis()

    def initialize_apis(self):
        try:
            # CoinGecko API
            self.apis['coingecko'] = CoinGeckoAPI()
            
            # KuCoin API
            self.apis['kucoin'] = Market()
            
            # Binance API
            self.apis['binance'] = Client(None, None)
            
            return True
        except Exception as e:
            st.error(f"Error initializing APIs: {str(e)}")
            return False

    def get_markets_data(self):
        all_markets = []
        
        # Try CoinGecko
        try:
            time.sleep(RATE_LIMIT_DELAY)
            markets = self.apis['coingecko'].get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=250,
                sparkline=False,
                price_change_percentage='24h'
            )
            if markets:
                all_markets.extend(markets)
        except Exception as e:
            st.warning(f"CoinGecko API error: {str(e)}")

        # Try KuCoin
        try:
            time.sleep(RATE_LIMIT_DELAY)
            kucoin_markets = self.apis['kucoin'].get_all_tickers()
            if kucoin_markets and 'ticker' in kucoin_markets:
                for ticker in kucoin_markets['ticker']:
                    if ticker['symbol'].endswith('USDT'):
                        symbol = ticker['symbol'].replace('-USDT', '')
                        all_markets.append({
                            'id': symbol.lower(),
                            'symbol': symbol,
                            'name': symbol,
                            'current_price': float(ticker['last']),
                            'price_change_percentage_24h': float(ticker['changeRate']) * 100,
                            'market_cap': float(ticker['vol']) * float(ticker['last']),
                            'total_volume': float(ticker['vol'])
                        })
        except Exception as e:
            st.warning(f"KuCoin API error: {str(e)}")

        # Try Binance
        try:
            time.sleep(RATE_LIMIT_DELAY)
            binance_markets = self.apis['binance'].get_ticker()
            for ticker in binance_markets:
                if ticker['symbol'].endswith('USDT'):
                    symbol = ticker['symbol'].replace('USDT', '')
                    all_markets.append({
                        'id': symbol.lower(),
                        'symbol': symbol,
                        'name': symbol,
                        'current_price': float(ticker['lastPrice']),
                        'price_change_percentage_24h': float(ticker['priceChangePercent']),
                        'market_cap': float(ticker['volume']) * float(ticker['lastPrice']),
                        'total_volume': float(ticker['volume'])
                    })
        except Exception as e:
            st.warning(f"Binance API error: {str(e)}")

        # Deduplicate and sort by market cap
        if all_markets:
            seen = set()
            unique_markets = []
            for market in all_markets:
                if market['id'] not in seen:
                    seen.add(market['id'])
                    unique_markets.append(market)
            return sorted(unique_markets, key=lambda x: x.get('market_cap', 0), reverse=True)
        
        return []

    def get_coin_price(self, coin_id):
        for api_name, api in self.apis.items():
            try:
                time.sleep(RATE_LIMIT_DELAY)
                if api_name == 'coingecko':
                    markets = api.get_coins_markets(
                        vs_currency='usd',
                        ids=[coin_id],
                        per_page=1
                    )
                    if markets:
                        return markets[0]
            except Exception as e:
                st.warning(f"{api_name} API error: {str(e)}")
                continue
        return None