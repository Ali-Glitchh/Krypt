import time
from pycoingecko import CoinGeckoAPI
from kucoin.client import Market
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
                        try:
                            last_price = float(ticker.get('last', 0))
                            volume = float(ticker.get('vol', 0))
                            if last_price and volume:  # Only add if valid numbers
                                symbol = ticker['symbol'].replace('-USDT', '')
                                all_markets.append({
                                    'id': symbol.lower(),
                                    'symbol': symbol,
                                    'name': symbol,
                                    'current_price': last_price,
                                    'price_change_percentage_24h': float(ticker.get('changeRate', 0)) * 100,
                                    'market_cap': volume * last_price,
                                    'total_volume': volume
                                })
                        except (TypeError, ValueError) as e:
                            continue  # Skip this ticker if number conversion fails
        except Exception as e:
            st.warning(f"KuCoin API error: {str(e)}")

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
        try:
            time.sleep(RATE_LIMIT_DELAY)
            markets = self.apis['coingecko'].get_coins_markets(
                vs_currency='usd',
                ids=[coin_id],
                per_page=1
            )
            if markets:
                return markets[0]
        except Exception as e:
            st.warning(f"CoinGecko API error: {str(e)}")
        return None