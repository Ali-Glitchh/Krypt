import time
from pycoingecko import CoinGeckoAPI
import logging
import requests

# Optional KuCoin import with graceful fallback
try:
    from kucoin.client import Market
    KUCOIN_AVAILABLE = True
except (ImportError, ModuleNotFoundError, Exception) as e:
    Market = None
    KUCOIN_AVAILABLE = False
    print(f"⚠️ KuCoin API not available: {e}")

RATE_LIMIT_DELAY = 0.5  # Reduced delay for faster responses
API_TIMEOUT = 5  # Reduced timeout

# Set up logger for non-Streamlit environments
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Global API instances
_coingecko_api = None
_crypto_apis = None

def _get_coingecko_api():
    """Get or create CoinGecko API instance"""
    global _coingecko_api
    if _coingecko_api is None:
        _coingecko_api = CoinGeckoAPI()
    return _coingecko_api

def get_crypto_price(coin_id: str):
    """Get current price for a cryptocurrency with better error handling"""
    try:
        # Quick return for invalid requests
        if not coin_id or len(coin_id) < 2:
            return None
            
        api = _get_coingecko_api()
        time.sleep(RATE_LIMIT_DELAY)
        
        # Try exact ID first with timeout protection
        try:
            result = api.get_price(ids=[coin_id], vs_currencies=['usd'])
            if coin_id in result and 'usd' in result[coin_id]:
                return result[coin_id]['usd']
        except Exception as e:
            logger.debug(f"Direct price lookup failed for {coin_id}: {e}")
            # Quick fail for common issues
            if "timeout" in str(e).lower() or "connection" in str(e).lower():
                return None
        
        # Skip search if we've already failed (avoid double timeout)
        return None
        
    except Exception as e:
        logger.warning(f"Error fetching price for {coin_id}: {e}")
        return None

def get_crypto_info(coin_id: str):
    """Get detailed info for a cryptocurrency with better error handling"""
    try:
        # Quick return for invalid requests  
        if not coin_id or len(coin_id) < 2:
            return get_static_crypto_info(coin_id)
            
        # Always use static info first to avoid API delays
        static_info = get_static_crypto_info(coin_id)
        if static_info:
            return static_info
        
        return None
    except Exception as e:
        logger.warning(f"Error searching for {coin_id}: {e}")
        # Fallback to static data if API fails
        static_info = get_static_crypto_info(coin_id)
        if static_info:
            return static_info
        return None
        return None

def get_crypto_news(limit: int = 5):
    """Get crypto news (placeholder - can be enhanced with real news API)"""
    try:
        # For now, return some sample news
        return [
            {
                'title': 'Bitcoin Market Analysis',
                'summary': 'Latest trends in Bitcoin trading and market movements.',
                'url': 'https://example.com/bitcoin-news',
                'timestamp': '2025-06-22'
            },
            {
                'title': 'Ethereum Updates',
                'summary': 'Recent developments in the Ethereum ecosystem.',
                'url': 'https://example.com/ethereum-news',
                'timestamp': '2025-06-22'
            }
        ][:limit]
    except Exception as e:
        logger.warning(f"Error fetching news: {e}")
        return []

class CryptoAPIs:
    def __init__(self):
        self.apis = {}
        self.initialize_apis()
    
    def initialize_apis(self):
        try:
            # CoinGecko API
            self.apis['coingecko'] = CoinGeckoAPI()
            
            # KuCoin API (optional)
            if KUCOIN_AVAILABLE and Market:
                self.apis['kucoin'] = Market()
                print("✅ KuCoin API initialized")
            else:
                self.apis['kucoin'] = None
                print("⚠️ KuCoin API not available - continuing with CoinGecko only")
            
            return True
        except Exception as e:
            logger.error(f"Error initializing APIs: {str(e)}")
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
            logger.warning(f"CoinGecko API error: {str(e)}")        # Try KuCoin (if available)
        if self.apis.get('kucoin') is not None:
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
                logger.warning(f"KuCoin API error: {str(e)}")
        else:
            logger.info("KuCoin API not available - using CoinGecko data only")

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
            logger.warning(f"CoinGecko API error: {str(e)}")
        return None

# Fallback static data for common cryptocurrencies
STATIC_CRYPTO_DATA = {
    'bitcoin': {
        'name': 'Bitcoin',
        'symbol': 'BTC',
        'description': 'Bitcoin is the first decentralized cryptocurrency, created by Satoshi Nakamoto in 2009. It operates on a peer-to-peer network without central authority.'
    },
    'ethereum': {
        'name': 'Ethereum',
        'symbol': 'ETH',
        'description': 'Ethereum is a decentralized blockchain platform that enables smart contracts and decentralized applications (dApps).'
    },
    'pi-network': {
        'name': 'Pi Network',
        'symbol': 'PI',
        'description': 'Pi Network is a cryptocurrency project that allows users to mine Pi coins on their mobile phones. Currently in development phase.'
    },
    'dogecoin': {
        'name': 'Dogecoin',
        'symbol': 'DOGE',
        'description': 'Dogecoin started as a meme cryptocurrency but has gained significant popularity and community support.'
    }
}

def get_static_crypto_info(coin_id: str):
    """Get static information for common cryptocurrencies"""
    coin_data = STATIC_CRYPTO_DATA.get(coin_id.lower())
    if coin_data:
        return {
            'name': coin_data['name'],
            'symbol': coin_data['symbol'],
            'current_price': 0,
            'market_cap': 0,
            'price_change_24h': 0,
            'description': coin_data['description'] + " (Note: Live price data unavailable - check CoinGecko or CoinMarketCap for current prices.)"
        }
    return None