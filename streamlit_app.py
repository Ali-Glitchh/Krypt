import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import re
from api_utils import CryptoAPIs, RATE_LIMIT_DELAY

# Initialize APIs and Sentiment Analyzer
@st.cache_resource
def initialize_services():
    crypto_apis = CryptoAPIs()
    analyzer = SentimentIntensityAnalyzer()
    return crypto_apis, analyzer

# Page config
st.set_page_config(
    page_title="Krypt - Crypto News & Analysis",
    layout="wide",
)

# Initialize services
apis, analyzer = initialize_services()

# Custom CSS
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    margin-bottom: 5px;
}
.reportview-container {
    background: var(--secondary-background-color);
}
.coin-button {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
}
.coin-button:hover {
    background-color: #2e2e2e;
}
.news-container {
    border: 1px solid #333;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 15px;
}
.sentiment-badge {
    padding: 5px 10px;
    border-radius: 15px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown("""
<h1 style='text-align: center; color: #4ecdc4; margin-bottom: 30px;'>
    🪙 Krypt - Crypto News & Analysis
</h1>
""", unsafe_allow_html=True)

# Cache market data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_market_data():
    with st.spinner('Fetching market data...'):
        return apis.get_markets_data()

# Cache news data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_news_data(symbol):
    try:
        time.sleep(RATE_LIMIT_DELAY)
        url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={symbol}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {'Data': []}
    except Exception as e:
        st.warning(f"Error fetching news: {str(e)}")
        return {'Data': []}

# Sentiment analysis function
def analyze_sentiment(text, coin_name):
    relevant_terms = {
        'bullish': 2.0, 'bearish': -2.0,
        'surge': 1.5, 'plunge': -1.5,
        'gain': 1.0, 'loss': -1.0,
        'high': 0.5, 'low': -0.5,
        'up': 0.3, 'down': -0.3,
    }
    
    base_sentiment = analyzer.polarity_scores(text)
    score = base_sentiment['compound']
    
    text_lower = text.lower()
    for term, weight in relevant_terms.items():
        if term in text_lower and coin_name in text_lower:
            score += weight
    
    return max(min(score, 1.0), -1.0)

# Number formatting
def format_number(num):
    if num is None:
        return "N/A"
    try:
        num = float(num)
        if abs(num) < 0.01:
            return f"{num:.8f}"
        if abs(num) >= 1e9:
            return f"{num/1e9:.2f}B"
        if abs(num) >= 1e6:
            return f"{num/1e6:.2f}M"
        if abs(num) >= 1e3:
            return f"{num/1e3:.2f}K"
        return f"{num:.2f}"
    except:
        return "N/A"

# Load market data
market_data = get_market_data()

# Sidebar with market overview
st.sidebar.markdown("### 📊 Market Overview")

# Group coins by first letter for side tray
coins_by_letter = {}
for coin in market_data:
    first_letter = coin['symbol'][0].upper()
    if first_letter not in coins_by_letter:
        coins_by_letter[first_letter] = []
    coins_by_letter[first_letter].append(coin)

# Create tabs for top coins and alphabetical list
tab1, tab2 = st.sidebar.tabs(["🔝 Top Coins", "📑 All Coins"])

with tab1:
    for coin in market_data[:15]:  # Show top 15 coins
        price_change = coin.get('price_change_percentage_24h', 0)
        color = '#4ecdc4' if price_change >= 0 else '#ff6b6b'
        st.sidebar.markdown(f"""
        <div class='coin-button'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span>#{coin.get('market_cap_rank', '?')} {coin['symbol'].upper()}</span>
                <span style='color: {color}'>{price_change:+.2f}%</span>
            </div>
            <div style='font-size: 0.8em; color: #666;'>
                ${format_number(coin.get('current_price'))}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button(f"View {coin['symbol'].upper()}", key=f"btn_{coin['id']}"):
            st.query_params['crypto'] = coin['id']

with tab2:
    selected_letter = st.sidebar.selectbox(
        "Select letter",
        sorted(coins_by_letter.keys())
    )
    
    if selected_letter in coins_by_letter:
        for coin in coins_by_letter[selected_letter]:
            if st.sidebar.button(f"{coin['symbol'].upper()} - ${format_number(coin.get('current_price'))}", key=f"alpha_{coin['id']}"):
                st.query_params['crypto'] = coin['id']

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Main search input with auto-complete
    crypto_input = st.text_input("🔍 Search cryptocurrency by name or symbol", "")

    if crypto_input:
        # Find matching coin
        crypto_input = crypto_input.lower()
        matching_coins = [
            coin for coin in market_data 
            if crypto_input in coin['symbol'].lower() or crypto_input in coin['name'].lower()
        ]

        if matching_coins:
            coin = matching_coins[0]
            
            # Display market metrics in a styled container
            st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2>{coin['name']} ({coin['symbol'].upper()})</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                price = coin.get('current_price')
                change = coin.get('price_change_percentage_24h')
                st.metric(
                    "Price (USD)",
                    f"${format_number(price)}",
                    f"{change:+.2f}%" if change else None
                )
                
            with col2:
                mcap = coin.get('market_cap')
                st.metric("Market Cap", f"${format_number(mcap)}")
                
            with col3:
                vol = coin.get('total_volume')
                st.metric("24h Volume", f"${format_number(vol)}")

            # Get and display news
            st.markdown("### 📰 Latest News & Analysis")
            news_data = get_news_data(coin['symbol'])
            
            news_items = []
            for item in news_data.get('Data', []):
                sentiment = analyze_sentiment(f"{item['title']} {item['body']}", coin['symbol'])
                news_items.append({
                    'title': item['title'],
                    'source': item['source'],
                    'sentiment': sentiment,
                    'url': item['url'],
                    'time': datetime.fromtimestamp(item['published_on'])
                })

            if news_items:
                news_df = pd.DataFrame(news_items)
                total_sentiment = news_df['sentiment'].mean()
                sentiment_color = '#4ecdc4' if total_sentiment > 0 else '#ff6b6b'
                
                # Market sentiment score
                st.markdown(f"""
                <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h3 style='margin: 0;'>Market Sentiment Score: <span style='color: {sentiment_color}'>{total_sentiment:.2f}</span></h3>
                </div>
                """, unsafe_allow_html=True)

                # News items with improved styling
                for _, news in news_df.iterrows():
                    sentiment_color = '#4ecdc4' if news['sentiment'] > 0 else '#ff6b6b'
                    st.markdown(f"""
                    <div class='news-container'>
                        <h3 style='margin-top: 0;'>{news['title']}</h3>
                        <p>
                            <span class='sentiment-badge' style='background-color: {sentiment_color}'>
                                Sentiment: {news['sentiment']:.2f}
                            </span>
                            <span style='margin-left: 10px; color: #666;'>
                                {news['source']} | {news['time'].strftime('%Y-%m-%d %H:%M')}
                            </span>
                        </p>
                        <a href='{news['url']}' target='_blank'>Read more</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No recent news found for {coin['symbol'].upper()}")
        else:
            st.error("Cryptocurrency not found. Please try another symbol.")

with col2:
    st.markdown("### 📈 Similar Coins")
    if 'crypto_input' in locals() and matching_coins:
        similar_coins = [
            c for c in market_data 
            if c['id'] != coin['id'] 
            and abs(c.get('price_change_percentage_24h', 0) - coin.get('price_change_percentage_24h', 0)) < 5
        ][:5]
        
        for similar in similar_coins:
            price_change = similar.get('price_change_percentage_24h', 0)
            color = '#4ecdc4' if price_change >= 0 else '#ff6b6b'
            st.markdown(f"""
            <div class='coin-button' onclick='window.location.href="?crypto={similar['id']}"' style='cursor: pointer;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span>{similar['symbol'].upper()}</span>
                    <span style='color: {color}'>{price_change:+.2f}%</span>
                </div>
                <div style='font-size: 0.8em; color: #666;'>
                    ${format_number(similar.get('current_price'))}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Developed with ❤️ | Data from CoinGecko, KuCoin & CryptoCompare
</div>
""", unsafe_allow_html=True)