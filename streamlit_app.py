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
    page_title="Multi-Exchange Crypto Analysis",
    layout="wide",
)

# Initialize services
apis, analyzer = initialize_services()

# Custom CSS
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

# Title
st.title("🪙 Multi-Exchange Crypto Analysis")

# Cache market data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_market_data():
    with st.spinner('Fetching market data from multiple exchanges...'):
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

# Sidebar - Quick access to top coins
st.sidebar.markdown("### Quick Access")
for coin in market_data[:10]:  # Top 10 coins
    if st.sidebar.button(f"#{coin.get('market_cap_rank', '?')} {coin['symbol'].upper()}"):
        st.query_params['crypto'] = coin['id']

# Main search input
crypto_input = st.text_input("Enter a cryptocurrency symbol (e.g., BTC, ETH)", "")

if crypto_input:
    # Find matching coin
    crypto_input = crypto_input.lower()
    matching_coins = [
        coin for coin in market_data 
        if crypto_input in coin['symbol'].lower() or crypto_input in coin['name'].lower()
    ]

    if matching_coins:
        coin = matching_coins[0]
        
        # Display market metrics
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
        st.subheader("News & Sentiment Analysis")
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
            
            # Overall sentiment
            total_sentiment = news_df['sentiment'].mean()
            sentiment_color = '#4ecdc4' if total_sentiment > 0 else '#ff6b6b'
            st.markdown(f"### Overall Market Sentiment")
            st.markdown(
                f"<h2 style='text-align: center; color: {sentiment_color}'>Score: {total_sentiment:.2f}</h2>",
                unsafe_allow_html=True
            )

            # Sentiment visualization
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
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Detailed news
            with st.expander("📰 View Detailed News", expanded=True):
                for _, news in news_df.iterrows():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"[{news['title']}]({news['url']})")
                    with col2:
                        sentiment_color = '#4ecdc4' if news['sentiment'] > 0 else '#ff6b6b'
                        st.markdown(
                            f"Sentiment: <span style='color:{sentiment_color}'>{news['sentiment']:.2f}</span>",
                            unsafe_allow_html=True
                        )
                    st.markdown(f"Source: {news['source']} | {news['time'].strftime('%Y-%m-%d %H:%M')}")
                    st.markdown("---")
        else:
            st.info("No recent news found for this cryptocurrency")
    else:
        st.error("Cryptocurrency not found. Please try another symbol.")

# Footer
st.markdown("---")
st.markdown(
    "Developed with ❤️ | Data from CoinGecko, Binance, KuCoin & CryptoCompare"
)