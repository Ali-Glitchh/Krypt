import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pycoingecko import CoinGeckoAPI
import pandas as pd
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import re

# Add rate limiting delay
RATE_LIMIT_DELAY = 1.5  # seconds between API calls

# Initialize APIs with better error handling and rate limiting
@st.cache_resource
def initialize_apis():
    try:
        cg = CoinGeckoAPI()
        analyzer = SentimentIntensityAnalyzer()
        return cg, analyzer
    except Exception as e:
        st.error(f"Failed to initialize APIs: {str(e)}")
        return None, None

# Cache API health check
@st.cache_data(ttl=60)  # Cache for 1 minute
def check_api_health(cg):
    try:
        time.sleep(RATE_LIMIT_DELAY)
        cg.ping()
        return True
    except Exception as e:
        st.error("CoinGecko API is experiencing issues. Please try again in a few minutes.")
        return False

# Initialize session state for API status
if 'api_healthy' not in st.session_state:
    st.session_state.api_healthy = False

# Custom error handler
def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            if "rate limit" in str(e).lower():
                st.warning("Rate limit reached. Please wait a few minutes before trying again.")
            elif "timeout" in str(e).lower():
                st.warning("Request timed out. The server might be busy.")
            return None
    return wrapper

cg, analyzer = initialize_apis()
if not cg or not analyzer:
    st.error("Failed to initialize APIs. Please refresh the page.")
    st.stop()

# Check API health with error handling
@handle_api_error
def check_api_status():
    result = check_api_health(cg)
    st.session_state.api_healthy = result
    return result

if not check_api_status():
    st.error("API is currently unavailable. Please try again later.")
    st.stop()

# Custom Kratos coin favicon (Base64 encoded)
KRATOS_ICON = """
data:image/png;base64,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
"""

# Page config with custom theme and Kratos icon
st.set_page_config(
    page_title="Crypto Sentiment Analysis",
    page_icon=KRATOS_ICON,
    layout="wide",
)

# Custom CSS for dark mode
st.markdown("""
<style>
.stButton>button {
    width: 100%;
}
.reportview-container {
    background: var(--secondary-background-color);
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🪙 Crypto Sentiment Analysis")

# Greeting handler
def get_greeting_response(text):
    greetings = {
        r'\b(hi|hello|hey)\b': "👋 Hello! How can I help you analyze the crypto market today?",
        r'\b(good morning)\b': "🌅 Good morning! Ready to explore some crypto insights?",
        r'\b(good afternoon)\b': "☀️ Good afternoon! Let's check the crypto markets!",
        r'\b(good evening)\b': "🌆 Good evening! Time for some crypto analysis!",
        r'\b(help)\b': "💡 Just type a cryptocurrency name or symbol (like Bitcoin or BTC) to get started!",
    }
    
    text = text.lower()
    for pattern, response in greetings.items():
        if re.search(pattern, text):
            return response
    return None
# Format numbers with appropriate precision
def format_number(num):
    if num is None:
        return "N/A"
    try:
        num = float(num)
        
        # Handle very small numbers
        if 0 < abs(num) < 0.01:
            return f"{num:.8f}"
            
        # Handle zero
        if num == 0:
            return "0.00"
            
        # Standard notation with suffix for large numbers
        if num >= 1e12:
            standard = f"{num/1e12:.2f}T"
        elif num >= 1e9:
            standard = f"{num/1e9:.2f}B"
        elif num >= 1e6:
            standard = f"{num/1e6:.2f}M"
        elif num >= 1e3:
            standard = f"{num/1e3:.2f}K"
        else:
            # Use more decimal places for small numbers
            if num < 100:
                standard = f"{num:.4f}"
            else:
                standard = f"{num:.2f}"
        
        # Scientific notation only for very large numbers
        if num >= 1e6:
            power = 0
            scientific_num = num
            while scientific_num >= 10:
                scientific_num /= 10
                power += 1
            return f"{standard} ({scientific_num:.2f}×10^{power})"
        
        return standard
        
    except (TypeError, ValueError):
        return "N/A"

# Cryptocurrency input
crypto_input = st.text_input("Enter a cryptocurrency name or symbol (e.g., Bitcoin, BTC, ETH)", "")

# Check for greetings first
greeting_response = get_greeting_response(crypto_input)
if greeting_response:
    st.info(greeting_response)

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

if crypto_input and not greeting_response:
    try:
        # Clear previous data when new coin is searched
        if 'last_search' not in st.session_state or st.session_state.last_search != crypto_input:
            st.session_state.last_search = crypto_input
            if 'market_data' in st.session_state:
                del st.session_state.market_data
            if 'news_data' in st.session_state:
                del st.session_state.news_data

        with st.spinner('Analyzing cryptocurrency data...'):
            # Extract cryptocurrency name
            crypto_name = crypto_input.lower()
            # Initialize coin mapping cache
            if 'coin_mapping' not in st.session_state:
                try:
                    # Get complete list of coins from CoinGecko
                    all_coins = cg.get_coins_list()
                    coin_mapping = {}
                    
                    # Create comprehensive mapping with id, symbol, and name
                    for coin in all_coins:
                        coin_id = coin['id']
                        # Basic patterns
                        patterns = set([
                            coin['id'].lower(),
                            coin['symbol'].lower(),
                            coin['name'].lower(),
                            coin['symbol'].lower().strip(),
                            coin['name'].lower().strip()
                        ])

                        # Handle special characters and variations
                        name_variations = [
                            coin['name'].lower(),
                            coin['name'].lower().replace(' ', ''),
                            coin['name'].lower().replace('-', ''),
                            coin['name'].lower().replace('_', ''),
                            coin['name'].lower().replace('.', '')
                        ]
                        patterns.update(name_variations)

                        # Handle common token variations
                        if 'token' in coin_id:
                            patterns.add(coin_id.replace('-token', ''))
                        if 'coin' in coin_id:
                            patterns.add(coin_id.replace('-coin', ''))
                        if 'inu' in coin_id:
                            patterns.add(coin_id.replace('-inu', ''))
                        
                        # Special cases for common coins
                        special_cases = {
                            'bitcoin': ['btc', 'xbt', 'bitcoin'],
                            'ethereum': ['eth', 'ether', 'ethereum'],
                            'binancecoin': ['bnb', 'binance', 'binance coin'],
                            'ripple': ['xrp', 'ripple'],
                            'dogecoin': ['doge', 'dogecoin'],
                            'stellar': ['xlm', 'stellar'],
                            'cardano': ['ada', 'cardano'],
                            'polkadot': ['dot', 'polkadot'],
                            'solana': ['sol', 'solana'],
                            'matic-network': ['matic', 'polygon'],
                            'shiba-inu': ['shib', 'shiba', 'shiba inu']
                        }
                        
                        if coin_id in special_cases:
                            patterns.update(special_cases[coin_id])

                        # Remove any empty strings and convert to list
                        patterns = [p for p in patterns if p and len(p) > 1]
                        
                        coin_mapping[coin_id] = list(set(patterns))  # Remove duplicates
                    
                    st.session_state.coin_mapping = coin_mapping
                except Exception as e:
                    st.error(f"Error fetching coin list: {str(e)}")
                    # Fallback to basic mapping if API fails
                    st.session_state.coin_mapping = {
                        'bitcoin': ['bitcoin', 'btc', 'xbt'],
                        'ethereum': ['ethereum', 'eth', 'ether'],
                        'cardano': ['cardano', 'ada'],
                        'binancecoin': ['bnb', 'binance coin'],
                        'solana': ['solana', 'sol'],
                        'ripple': ['ripple', 'xrp'],
                        'dogecoin': ['dogecoin', 'doge']
                    }
            
            coin_patterns = st.session_state.coin_mapping

            # Enhanced coin mapping with priority matching
            def find_best_coin_match(search_term, patterns_dict):
                search_term = search_term.lower().strip()
                
                # Direct symbol/name match first
                for coin_id, patterns in patterns_dict.items():
                    if search_term in [p.lower() for p in patterns]:
                        return coin_id
                
                # Partial match with confidence scoring
                best_match = None
                highest_score = 0
                
                for coin_id, patterns in patterns_dict.items():
                    for pattern in patterns:
                        pattern = pattern.lower()
                        # Exact match gets highest priority
                        if search_term == pattern:
                            return coin_id
                        # Symbol match gets high priority
                        elif len(pattern) <= 5 and pattern in search_term:
                            if len(pattern) > highest_score:
                                highest_score = len(pattern)
                                best_match = coin_id
                        # Name match gets medium priority
                        elif search_term in pattern:
                            if len(search_term) > highest_score:
                                highest_score = len(search_term)
                                best_match = coin_id
                
                return best_match

            # Try to find coin using enhanced matching
            coin_id = find_best_coin_match(crypto_name, coin_patterns)

            # Fallback to API search if no match found
            if not coin_id:
                try:
                    search_results = cg.search(crypto_name)
                    if search_results and search_results['coins']:
                        # Find the most relevant match
                        best_match = None
                        highest_score = 0
                        search_term = crypto_name.lower()

                        for coin in search_results['coins'][:5]:  # Check top 5 results
                            score = 0
                            if search_term == coin['symbol'].lower():
                                score = 100  # Exact symbol match
                            elif search_term == coin['name'].lower():
                                score = 90   # Exact name match
                            elif search_term in coin['symbol'].lower():
                                score = 80   # Partial symbol match
                            elif search_term in coin['name'].lower():
                                score = 70   # Partial name match
                            
                            if score > highest_score:
                                highest_score = score
                                best_match = coin['id']
                        
                        coin_id = best_match
                except Exception as e:
                    st.error(f"Error searching for coin: {str(e)}")

            if coin_id:
                # Get fresh market data with retry mechanism and rate limiting
                retry_count = 0
                max_retries = 3
                market_data = {}

                while retry_count < max_retries:
                    try:
                        with st.spinner('Fetching market data...'):
                            # Add rate limiting delay
                            time.sleep(RATE_LIMIT_DELAY)
                            
                            # Try to get data from markets endpoint first (more reliable for prices)
                            markets = cg.get_coins_markets(
                                vs_currency='usd',
                                ids=[coin_id],
                                order='market_cap_desc',
                                per_page=1,
                                sparkline=False,
                                price_change_percentage='24h'
                            )

                        if markets and len(markets) > 0:
                                                    market = markets[0]
                                                    # Get detailed coin data first
                                                    try:
                                                        coin_data = cg.get_coin_by_id(
                                                            coin_id,
                                                            localization=False,
                                                            tickers=False,
                                                            market_data=True,
                                                            community_data=False,
                                                            developer_data=False
                                                        )
                                                        market_data = coin_data
                                                        # Update with real-time price data
                                                        market_data['market_data']['current_price']['usd'] = market['current_price']
                                                        market_data['market_data']['price_change_percentage_24h'] = market['price_change_percentage_24h']
                                                        market_data['market_data']['market_cap']['usd'] = market['market_cap']
                                                        market_data['market_data']['total_volume']['usd'] = market['total_volume']
                                                    except:
                                                        # Fallback to basic market data if detailed fetch fails
                                                        market_data = {
                                                            'market_data': {
                                                                'current_price': {'usd': market['current_price']},
                                                                'price_change_percentage_24h': market['price_change_percentage_24h'],
                                                                'market_cap': {'usd': market['market_cap']},
                                                                'total_volume': {'usd': market['total_volume']}
                                                            },
                                                            'name': market['name'],
                                                            'symbol': market['symbol']
                                                        }

                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Error fetching market data: {str(e)}")
                        else:
                            time.sleep(1)  # Wait before retrying

                # Display market data with formatted numbers safely
                col1, col2, col3 = st.columns(3)
                
                market_data_metrics = market_data.get('market_data', {})
                price = market_data_metrics.get('current_price', {}).get('usd')
                price_change = market_data_metrics.get('price_change_percentage_24h')
                market_cap = market_data_metrics.get('market_cap', {}).get('usd')
                volume = market_data_metrics.get('total_volume', {}).get('usd')
                
                with col1:
                    if price is not None and isinstance(price, (int, float)):
                        formatted_price = format_number(price)
                        formatted_change = f"{price_change:+.2f}%" if price_change is not None else None
                        st.metric(
                            "Price (USD)",
                            f"${formatted_price}",
                            formatted_change
                        )
                    else:
                        st.metric("Price (USD)", "N/A")

                with col2:
                    if market_cap is not None and isinstance(market_cap, (int, float)):
                        formatted_mcap = format_number(market_cap)
                        st.metric("Market Cap", f"${formatted_mcap}")
                    else:
                        st.metric("Market Cap", "N/A")

                with col3:
                    if volume is not None and isinstance(volume, (int, float)):
                        formatted_vol = format_number(volume)
                        st.metric("24h Volume", f"${formatted_vol}")
                    else:
                        st.metric("24h Volume", "N/A")

                # News and sentiment analysis
                st.subheader("News & Sentiment Analysis")
                
                news_items = []
                
                # Enhanced news fetching and filtering
                try:
                    # Get coin info for better news matching
                    coin_info = market_data.get('name', '').lower()
                    coin_symbol = market_data.get('symbol', '').lower()
                    search_terms = [coin_id, coin_info, coin_symbol] + coin_patterns.get(coin_id, [])
                    search_terms = list(set([term.lower() for term in search_terms if term]))

                    # Fetch news with timeout and better error handling
                    with st.spinner('Fetching news data...'):
                        time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
                        crypto_compare_url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={coin_symbol}"
                        try:
                            news_response = requests.get(crypto_compare_url, timeout=10)
                            if news_response.status_code == 429:  # Rate limit error
                                st.warning("News API rate limit reached. Please wait a few minutes and try again.")
                                news_data = {'Data': []}  # Return empty data
                            elif news_response.status_code != 200:
                                st.warning(f"News API returned status code: {news_response.status_code}")
                                news_data = {'Data': []}  # Return empty data
                            else:
                                news_data = news_response.json()
                        except requests.Timeout:
                            st.warning("News API request timed out. Skipping news data.")
                            news_data = {'Data': []}  # Return empty data
                        except requests.RequestException as e:
                            st.warning(f"Error fetching news: {str(e)}")
                            news_data = {'Data': []}  # Return empty data
                        news_data = news_response.json()
                        for item in news_data.get('Data', []):
                            title = item.get('title', '').lower()
                            body = item.get('body', '').lower()
                            categories = [cat.lower() for cat in item.get('categories', '').split('|')]
                            
                            # Check if news is relevant to the coin
                            is_relevant = any(term in title or term in body for term in search_terms)
                            is_relevant = is_relevant or any(term in categories for term in search_terms)
                            
                            if is_relevant:
                                # Analyze full text for better sentiment
                                full_text = f"{title} {body}"
                                sentiment = analyze_sentiment(full_text, coin_id)
                                news_items.append({
                                    'title': item['title'],
                                    'source': item['source'],
                                    'sentiment': sentiment,
                                    'url': item['url'],
                                    'time': datetime.fromtimestamp(item['published_on']),
                                    'categories': item.get('categories', '')
                                })
                except Exception as e:
                    st.warning(f"Error fetching news: {str(e)}")

                # Display news items
                if news_items:
                    news_df = pd.DataFrame(news_items)
                    news_df = news_df.sort_values('time', ascending=False)
                    
                    # Calculate and display total sentiment score
                    total_sentiment = news_df['sentiment'].mean()
                    sentiment_color = '#4ecdc4' if total_sentiment > 0 else '#ff6b6b'
                    st.markdown(f"### Overall Market Sentiment")
                    st.markdown(f"<h2 style='text-align: center; color: {sentiment_color}'>Score: {total_sentiment:.2f}</h2>", unsafe_allow_html=True)
                    
                    # Create sentiment visualization
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=news_df['title'],
                        y=news_df['sentiment'],
                        marker_color=['#ff6b6b' if x < 0 else '#4ecdc4' for x in news_df['sentiment']],
                        text=news_df['sentiment'].round(2),
                        textposition='auto',
                    ))
                    fig.update_layout(
                        title="News Sentiment Analysis",
                        xaxis_title="News Articles",
                        yaxis_title="Sentiment Score",
                        showlegend=False,
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Display news items in an expander
                    with st.expander("📰 View Detailed News", expanded=True):
                        for _, news in news_df.iterrows():
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(f"[{news['title']}]({news['url']})")
                            with col2:
                                sentiment_color = '#4ecdc4' if news['sentiment'] > 0 else '#ff6b6b'
                                st.markdown(f"Sentiment: <span style='color:{sentiment_color}'>{news['sentiment']:.2f}</span>", unsafe_allow_html=True)
                            st.markdown(f"Source: {news['source']} | {news['time'].strftime('%Y-%m-%d %H:%M')}")
                            st.markdown("---")
                else:
                    st.warning("No recent news found specifically mentioning this cryptocurrency")

            else:
                st.error("Could not find the specified cryptocurrency. Please try another name or symbol.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Quick access buttons with dynamic top coins
st.sidebar.markdown("### Quick Access")

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_top_coins():
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            time.sleep(RATE_LIMIT_DELAY)
            markets = cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=250,
                sparkline=False,
                price_change_percentage='24h'
            )
            if markets:
                return [
                    {
                        'id': coin['id'],
                        'symbol': coin['symbol'].upper(),
                        'name': coin['name'],
                        'price': coin['current_price'],
                        'market_cap': coin['market_cap'],
                        'price_change': coin.get('price_change_percentage_24h', 0),
                        'rank': coin['market_cap_rank']
                    }
                    for coin in markets
                ]
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                st.error(f"Error fetching market data: {str(e)}")
                return [{'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin', 'rank': 1}]
            time.sleep(2)
    return [{'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin', 'rank': 1}]

# Get all coins market data if not in session state
@st.cache_data(ttl=60)  # Refresh button cache
def refresh_data():
    return st.sidebar.button("🔄 Refresh Data")

if 'all_coins' not in st.session_state or refresh_data():
    with st.spinner('Loading market data...'):
        st.session_state.all_coins = get_top_coins()

if 'all_coins' not in st.session_state or st.sidebar.button("🔄 Refresh Data"):
    with st.spinner('Loading market data...'):
        markets = fetch_all_coins(cg)
        st.session_state.all_coins = [
            {
                'id': coin['id'],
                'symbol': coin['symbol'].upper(),
                'name': coin['name'],
                'price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'price_change': coin.get('price_change_percentage_24h', 0),
                'rank': coin['market_cap_rank']
            }
            for coin in markets
        ]
    except Exception as e:
        st.error(f"Error fetching coins: {str(e)}")
        st.session_state.all_coins = [
            {'id': 'bitcoin', 'symbol': 'BTC', 'name': 'Bitcoin', 'rank': 1}
        ]

# Add search box in sidebar
st.sidebar.markdown("### Find Coins")
search_term = st.sidebar.text_input("Search by name or symbol", "").lower()

# Filter coins based on search
displayed_coins = [
    coin for coin in st.session_state.all_coins
    if search_term in coin['name'].lower() or search_term in coin['symbol'].lower()
] if search_term else st.session_state.all_coins

# Display coins in sidebar with pagination
COINS_PER_PAGE = 20
total_pages = (len(displayed_coins) + COINS_PER_PAGE - 1) // COINS_PER_PAGE

if total_pages > 1:
    page = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1) - 1
else:
    page = 0

start_idx = page * COINS_PER_PAGE
end_idx = min(start_idx + COINS_PER_PAGE, len(displayed_coins))

# Show coin count
st.sidebar.markdown(f"Showing {start_idx+1}-{end_idx} of {len(displayed_coins)} coins")

# Display coins in sidebar
for coin in displayed_coins[start_idx:end_idx]:
    # Create a container for each coin
    with st.sidebar.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"#{coin['rank']} {coin['name']}", key=f"btn_{coin['id']}"):
                st.query_params['crypto'] = coin['id']
        with col2:
            if 'price' in coin:
                price_color = 'green' if coin.get('price_change', 0) > 0 else 'red'
                st.markdown(f"<span style='color: {price_color}'>${format_number(coin['price'])}</span>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ | Data from CoinGecko & CryptoCompare")