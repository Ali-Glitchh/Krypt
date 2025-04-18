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
.disclaimer {
    font-size: 0.8em;
    color: #666;
    font-style: italic;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Disclaimer text
DISCLAIMER = """
⚠️ **Investment Disclaimer:** The analysis and insights provided are for informational purposes only. 
This is not financial advice. Cryptocurrency investments are highly volatile and risky. 
Always conduct your own research and consult with financial professionals before making any investment decisions.
"""

def get_investment_sentiment(price_change, sentiment_score, volume_change=0):
    total_score = (
        0.4 * sentiment_score +
        0.4 * (price_change / 10) +
        0.2 * (volume_change / 100)
    )

    if total_score > 0.5:
        return "Strong Positive", "Market indicators suggest strong positive sentiment, but remember to do your own research."
    elif total_score > 0.2:
        return "Positive", "Market indicators are positive, but cryptocurrency markets are highly volatile."
    elif total_score > -0.2:
        return "Neutral", "Market indicators are mixed. Consider monitoring for clearer signals."
    elif total_score > -0.5:
        return "Negative", "Market indicators show some concerning signals. Exercise caution."
    else:
        return "Strong Negative", "Market indicators suggest strong negative sentiment. High risk environment."

# Format numbers with appropriate precision
def format_number(num):
    if num is None:
        return "N/A"
    try:
        num = float(num)
        if 0 < abs(num) < 0.0001:  # Adjusted threshold for very small values
            return f"{num:.10f}"  # Increased precision for very small values
        if 0 < abs(num) < 0.01:
            return f"{num:.8f}"
        if num == 0:
            return "0.00"
        if num >= 1e12:
            return f"{num/1e12:.2f}T"
        elif num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif num >= 1e3:
            return f"{num/1e3:.2f}K"
        else:
            return f"{num:.2f}"
    except (TypeError, ValueError):
        return "N/A"

# Analyze sentiment of text related to a cryptocurrency
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

# Load market data
market_data = get_market_data()

# Mode selection
mode = st.radio("Select Mode", ["Market Analysis", "Q&A"], horizontal=True)

if mode == "Market Analysis":
    # Sidebar setup
    st.sidebar.markdown("### 📊 Market Overview")
    
    # Group coins by first letter
    coins_by_letter = {}
    for coin in market_data:
        first_letter = coin['symbol'][0].upper()
        if first_letter not in coins_by_letter:
            coins_by_letter[first_letter] = []  # Correctly initialize a list for the first letter
        coins_by_letter[first_letter].append(coin)  # Append the coin to the correct list
    
    # Create tabs for navigation
    tab1, tab2 = st.sidebar.tabs(["🔝 Top Coins", "📑 All Coins"])
    
    with tab1:
        for coin in market_data[:15]:
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
                st.session_state.selected_coin = coin['id']
    
    with tab2:
        selected_letter = st.sidebar.selectbox(
            "Select letter",
            sorted(coins_by_letter.keys())
        )
        if selected_letter in coins_by_letter:
            for coin in coins_by_letter[selected_letter]:
                if st.sidebar.button(f"{coin['symbol'].upper()} - ${format_number(coin.get('current_price'))}", key=f"alpha_{coin['id']}"):
                    st.session_state.selected_coin = coin['id']

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        crypto_input = st.text_input("🔍 Search cryptocurrency by name or symbol", "")
        matching_coins = []
        selected_coin = None

        if crypto_input:
            crypto_input = crypto_input.lower()
            matching_coins = [
                coin for coin in market_data 
                if crypto_input in coin['symbol'].lower() or crypto_input in coin['name'].lower()
            ]
            if matching_coins:
                selected_coin = matching_coins[0]

        if selected_coin:
            # Display market metrics
            st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2>{selected_coin['name']} ({selected_coin['symbol'].upper()})</h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            
            price = selected_coin.get('current_price')
            change = selected_coin.get('price_change_percentage_24h')
            
            with col1:
                st.metric(
                    "Price (USD)",
                    f"${format_number(price)}",
                    f"{change:+.2f}%" if change else None
                )
                
            with col2:
                mcap = selected_coin.get('market_cap')
                st.metric("Market Cap", f"${format_number(mcap)}")
                
            with col3:
                vol = selected_coin.get('total_volume')
                st.metric("24h Volume", f"${format_number(vol)}")

            # Get and analyze news
            news_data = get_news_data(selected_coin['symbol'])
            news_items = []
            
            for item in news_data.get('Data', []):
                sentiment = analyze_sentiment(f"{item['title']} {item['body']}", selected_coin['symbol'])
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
                
                # Get investment sentiment
                sentiment_status, sentiment_message = get_investment_sentiment(
                    change or 0,
                    total_sentiment
                )
                
                sentiment_color = '#4ecdc4' if total_sentiment > 0 else '#ff6b6b'
                
                # Display sentiment analysis
                st.markdown(f"""
                <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h3 style='margin: 0;'>Market Analysis</h3>
                    <p>Sentiment Score: <span style='color: {sentiment_color}'>{total_sentiment:.2f}</span></p>
                    <p>Status: {sentiment_status}</p>
                    <p>{sentiment_message}</p>
                    <div class='disclaimer'>{DISCLAIMER}</div>
                </div>
                """, unsafe_allow_html=True)

                # Display news
                st.markdown("### 📰 Latest News")
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

    with col2:
        if selected_coin:
            st.markdown("### 📈 Similar Coins")
            similar_coins = [
                c for c in market_data 
                if c['id'] != selected_coin['id'] 
                and abs(c.get('price_change_percentage_24h', 0) - selected_coin.get('price_change_percentage_24h', 0)) < 5
            ][:5]
            
            for similar in similar_coins:
                price_change = similar.get('price_change_percentage_24h', 0)
                color = '#4ecdc4' if price_change >= 0 else '#ff6b6b'
                st.markdown(f"""
                <div class='coin-button'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span>{similar['symbol'].upper()}</span>
                        <span style='color: {color}'>{price_change:+.2f}%</span>
                    </div>
                    <div style='font-size: 0.8em; color: #666;'>
                        ${format_number(similar.get('current_price'))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif mode == "Q&A":
    st.markdown("### 💬 Crypto Q&A")
    st.markdown("""
    Ask questions about cryptocurrencies like:
    - What do you think about Bitcoin?
    - How is Ethereum performing?
    - Analysis of recent market trends
    """)

    question = st.text_input("Ask your question:")
    if question:
        crypto_mentioned = None
        question_lower = question.lower()

        # Predefined knowledge about popular cryptocurrencies
        crypto_knowledge = {
            "bitcoin": "Bitcoin is the first decentralized cryptocurrency, created in 2009 by an unknown person or group using the pseudonym Satoshi Nakamoto. It is often referred to as digital gold.",
            "ethereum": "Ethereum is a decentralized platform that enables smart contracts and decentralized applications (DApps) to be built and run without any downtime, fraud, or control.",
            "dogecoin": "Dogecoin started as a joke based on a popular internet meme but has since gained a large community and is often used for tipping and charitable donations.",
        }

        # Try to identify which cryptocurrency is being asked about
        for coin in market_data:
            if coin['symbol'].lower() in question_lower or coin['name'].lower() in question_lower:
                crypto_mentioned = coin
                break

        if crypto_mentioned:
            # Get news and sentiment for the mentioned crypto
            news_data = get_news_data(crypto_mentioned['symbol'])
            news_items = []
            for item in news_data.get('Data', []):
                sentiment = analyze_sentiment(f"{item['title']} {item['body']}", crypto_mentioned['symbol'])
                news_items.append({
                    'title': item['title'],
                    'sentiment': sentiment,
                    'time': datetime.fromtimestamp(item['published_on'])
                })

            if news_items:
                news_df = pd.DataFrame(news_items)
                total_sentiment = news_df['sentiment'].mean()
                price_change = crypto_mentioned.get('price_change_percentage_24h', 0)

                # Get investment sentiment
                sentiment_status, sentiment_message = get_investment_sentiment(
                    price_change,
                    total_sentiment
                )

                # Generate conversational response
                response = f"Hi there! Here's what I found about {crypto_mentioned['name']} ({crypto_mentioned['symbol'].upper()}):\n\n"
                response += f"📊 Market Metrics:\n"
                response += f"- Current price: ${format_number(crypto_mentioned.get('current_price'))}\n"
                response += f"- 24h change: {price_change:+.2f}%\n"
                response += f"- Market cap: ${format_number(crypto_mentioned.get('market_cap'))}\n\n"

                response += f"🔍 Market Analysis:\n"
                response += f"- Overall sentiment: {sentiment_status}\n"
                response += f"- Sentiment score: {total_sentiment:.2f}\n"
                response += f"- {sentiment_message}\n\n"

                response += "📰 Recent Developments:\n"
                for _, news in news_df.head(3).iterrows():
                    response += f"- {news['title']}\n"

                st.markdown(f"""
                <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <pre style='white-space: pre-wrap; font-family: inherit;'>{response}</pre>
                    <div class='disclaimer'>{DISCLAIMER}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"I couldn't find any recent news about {crypto_mentioned['symbol'].upper()}, but feel free to ask another question!")
        else:
            # Check if the question is about general crypto knowledge
            for key, value in crypto_knowledge.items():
                if key in question_lower:
                    st.markdown(f"""
                    <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                        <p>{value}</p>
                        <div class='disclaimer'>{DISCLAIMER}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    break
            else:
                # Fallback response for unrecognized questions
                st.warning("I'm not sure about that. Could you rephrase or ask about a specific cryptocurrency? For example, try asking about Bitcoin or Ethereum.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Developed with ❤️ | Data from CoinGecko, KuCoin & CryptoCompare
</div>
""", unsafe_allow_html=True)