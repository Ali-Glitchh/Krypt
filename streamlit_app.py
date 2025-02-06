import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pycoingecko import CoinGeckoAPI
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import re

# Initialize APIs
try:
    cg = CoinGeckoAPI()
    analyzer = SentimentIntensityAnalyzer()
except Exception as e:
    st.error(f"Error initializing APIs: {str(e)}")

# Page config with theme support
st.set_page_config(
    page_title="Crypto Sentiment Analysis",
    page_icon="🪙",
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

# Format large numbers
def format_number(num):
    if num >= 1e12:
        return f"{num/1e12:.2f}T"
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    if num >= 1e6:
        return f"{num/1e6:.2f}M"
    if num >= 1e3:
        return f"{num/1e3:.2f}K"
    return f"{num:.2f}"

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
        with st.spinner('Analyzing cryptocurrency data...'):
            # Extract cryptocurrency name
            crypto_name = crypto_input.lower()
            coin_patterns = {
                'bitcoin': ['bitcoin', 'btc', 'xbt'],
                'ethereum': ['ethereum', 'eth', 'ether'],
                'cardano': ['cardano', 'ada'],
                'binancecoin': ['bnb', 'binance coin'],
                'solana': ['solana', 'sol'],
                'ripple': ['ripple', 'xrp'],
                'dogecoin': ['dogecoin', 'doge'],
            }

            coin_id = None
            for official_name, patterns in coin_patterns.items():
                if any(pattern in crypto_name for pattern in patterns):
                    coin_id = official_name
                    break

            if not coin_id:
                # Search CoinGecko API
                search_results = cg.search(crypto_name)
                if search_results and search_results['coins']:
                    coin_id = search_results['coins'][0]['id']

            if coin_id:
                # Get market data
                market_data = cg.get_coin_by_id(
                    coin_id,
                    localization=False,
                    tickers=False,
                    market_data=True,
                    community_data=False,
                    developer_data=False
                )

                # Display market data with formatted numbers
                col1, col2, col3 = st.columns(3)
                
                price = market_data['market_data']['current_price']['usd']
                price_change = market_data['market_data']['price_change_percentage_24h']
                market_cap = market_data['market_data']['market_cap']['usd']
                volume = market_data['market_data']['total_volume']['usd']
                
                with col1:
                    st.metric(
                        "Price (USD)", 
                        f"${format_number(price)}",
                        f"{price_change:.2f}%"
                    )
                with col2:
                    st.metric(
                        "Market Cap", 
                        f"${format_number(market_cap)}"
                    )
                with col3:
                    st.metric(
                        "24h Volume", 
                        f"${format_number(volume)}"
                    )

                # News and sentiment analysis
                st.subheader("News & Sentiment Analysis")
                
                news_items = []
                
                # CryptoCompare News with improved filtering
                try:
                    crypto_compare_url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
                    news_response = requests.get(crypto_compare_url, timeout=5)
                    if news_response.status_code == 200:
                        news_data = news_response.json()
                        for item in news_data.get('Data', []):
                            text = f"{item.get('title', '')} {item.get('body', '')}"
                            if any(pattern in text.lower() for pattern in [coin_id] + coin_patterns.get(coin_id, [])):
                                sentiment = analyze_sentiment(text, coin_id)
                                news_items.append({
                                    'title': item['title'],
                                    'source': item['source'],
                                    'sentiment': sentiment,
                                    'url': item['url'],
                                    'time': datetime.fromtimestamp(item['published_on'])
                                })
                except Exception as e:
                    st.warning(f"Error fetching news: {str(e)}")

                # Display news items
                if news_items:
                    news_df = pd.DataFrame(news_items)
                    news_df = news_df.sort_values('time', ascending=False)
                    
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

# Quick access buttons
st.sidebar.markdown("### Quick Access")
if st.sidebar.button("Bitcoin (BTC)"):
    st.experimental_set_query_params(crypto="bitcoin")
if st.sidebar.button("Ethereum (ETH)"):
    st.experimental_set_query_params(crypto="ethereum")
if st.sidebar.button("Cardano (ADA)"):
    st.experimental_set_query_params(crypto="cardano")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ | Data from CoinGecko & CryptoCompare")