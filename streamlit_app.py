import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pycoingecko import CoinGeckoAPI
import pandas as pd
import requests
import feedparser
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Initialize APIs
cg = CoinGeckoAPI()
analyzer = SentimentIntensityAnalyzer()

# Page config
st.set_page_config(page_title="Crypto Sentiment Analysis", page_icon="🪙", layout="wide")

# Title and description
st.title("🪙 Crypto Sentiment Analysis")
st.markdown("Get real-time cryptocurrency analysis with sentiment from multiple sources.")

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This application provides real-time cryptocurrency analysis including:"
    "\n- Price information"
    "\n- Market sentiment"
    "\n- News analysis"
    "\n- Overall market trends"
)

# Cryptocurrency input
crypto_input = st.text_input("Enter a cryptocurrency name or symbol (e.g., Bitcoin, BTC, ETH)", "")

def analyze_sentiment(text, coin_name):
    relevant_terms = {
        'bullish': 2.0,
        'bearish': -2.0,
        'surge': 1.5,
        'plunge': -1.5,
        'gain': 1.0,
        'loss': -1.0,
        'high': 0.5,
        'low': -0.5
    }
    
    base_sentiment = analyzer.polarity_scores(text)
    score = base_sentiment['compound']
    
    text_lower = text.lower()
    for term, weight in relevant_terms.items():
        if term in text_lower and coin_name in text_lower:
            score += weight
    
    return max(min(score, 1.0), -1.0)

if crypto_input:
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
                'polkadot': ['polkadot', 'dot'],
                'matic-network': ['polygon', 'matic'],
                'avalanche-2': ['avalanche', 'avax'],
                'sui': ['sui', 'sui coin', 'sui token']
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

                # Display market data
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Price (USD)", 
                        f"${market_data['market_data']['current_price']['usd']:,.2f}",
                        f"{market_data['market_data']['price_change_percentage_24h']:.2f}%"
                    )
                with col2:
                    st.metric(
                        "Market Cap", 
                        f"${market_data['market_data']['market_cap']['usd']:,.0f}"
                    )
                with col3:
                    st.metric(
                        "24h Volume", 
                        f"${market_data['market_data']['total_volume']['usd']:,.0f}"
                    )

                # News and sentiment analysis
                st.subheader("News & Sentiment Analysis")
                
                news_items = []
                
                # CryptoCompare News
                try:
                    crypto_compare_url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={coin_id}"
                    news_response = requests.get(crypto_compare_url, timeout=5)
                    if news_response.status_code == 200:
                        news_data = news_response.json()
                        for item in news_data.get('Data', [])[:5]:
                            if item.get('title') and item.get('source'):
                                text = item.get('title', '') + ' ' + item.get('body', '')
                                sentiment = analyze_sentiment(text, coin_id)
                                news_items.append({
                                    'title': item['title'],
                                    'source': item['source'],
                                    'sentiment': sentiment,
                                    'url': item['url'],
                                    'time': datetime.fromtimestamp(item['published_on'])
                                })
                except Exception as e:
                    st.warning(f"Error fetching CryptoCompare news: {str(e)}")

                # Display news items
                if news_items:
                    news_df = pd.DataFrame(news_items)
                    
                    # Create sentiment visualization
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=news_df['title'],
                        y=news_df['sentiment'],
                        marker_color=['red' if x < 0 else 'green' for x in news_df['sentiment']],
                        text=news_df['sentiment'].round(2),
                        textposition='auto',
                    ))
                    fig.update_layout(
                        title="News Sentiment Analysis",
                        xaxis_title="News Articles",
                        yaxis_title="Sentiment Score",
                        showlegend=False
                    )
                    st.plotly_chart(fig)

                    # Display news items in an expander
                    with st.expander("View Detailed News", expanded=True):
                        for _, news in news_df.iterrows():
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(f"[{news['title']}]({news['url']})")
                            with col2:
                                sentiment_color = 'green' if news['sentiment'] > 0 else 'red'
                                st.markdown(f"Sentiment: <span style='color:{sentiment_color}'>{news['sentiment']:.2f}</span>", unsafe_allow_html=True)
                            st.markdown(f"Source: {news['source']} | Time: {news['time'].strftime('%Y-%m-%d %H:%M')}")
                            st.markdown("---")
                else:
                    st.warning("No recent news found for this cryptocurrency")

            else:
                st.error("Could not find the specified cryptocurrency. Please try another name or symbol.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add suggestions
st.markdown("### Try these examples:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Bitcoin (BTC)"):
        crypto_input = "bitcoin"
with col2:
    if st.button("Ethereum (ETH)"):
        crypto_input = "ethereum"
with col3:
    if st.button("Cardano (ADA)"):
        crypto_input = "cardano"
with col4:
    if st.button("Binance Coin (BNB)"):
        crypto_input = "bnb"