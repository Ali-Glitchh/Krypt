import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import re

# Import API utilities with error handling
try:
    from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
    API_UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ API utilities not available: {e}")
    API_UTILS_AVAILABLE = False
    RATE_LIMIT_DELAY = 1.5  # fallback value

# Import chatbot with error handling
try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    CHATBOT_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing chatbot: {e}")
    CHATBOT_AVAILABLE = False

# Initialize improved dual-personality chatbot
@st.cache_resource
def initialize_chatbot():
    if CHATBOT_AVAILABLE:
        return ImprovedDualPersonalityChatbot()
    else:
        return None

# Initialize APIs and Sentiment Analyzer
@st.cache_resource
def initialize_services():
    if API_UTILS_AVAILABLE:
        try:
            crypto_apis = CryptoAPIs()
        except Exception as e:
            st.warning(f"⚠️ Could not initialize crypto APIs: {e}")
            crypto_apis = None
    else:
        crypto_apis = None
        
    analyzer = SentimentIntensityAnalyzer()
    return crypto_apis, analyzer

# Page config
st.set_page_config(
    page_title="Krypt - Enhanced Crypto Assistant",
    layout="wide",
)

# Initialize services
apis, analyzer = initialize_services()
chatbot = initialize_chatbot()

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

# Personality switcher
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 🤖 Choose Your Assistant Personality")
    
    # Initialize personality in session state
    if 'personality_mode' not in st.session_state:
        st.session_state.personality_mode = 'normal'
    
    # Personality selection buttons
    personality_col1, personality_col2 = st.columns(2)
    
    with personality_col1:
        if st.button("💬 Normal Mode", 
                    type="primary" if st.session_state.personality_mode == 'normal' else "secondary",
                    use_container_width=True):
            st.session_state.personality_mode = 'normal'
            if CHATBOT_AVAILABLE and chatbot is not None:
                try:
                    chatbot.switch_personality('normal')
                    st.success("✅ Normal mode activated! Ready to help with crypto insights!")
                except Exception as e:
                    st.error(f"Error switching to normal mode: {e}")
            else:
                st.warning("💬 Normal mode selected (chatbot features limited)")
            st.rerun()
    
    with personality_col2:
        if st.button("🧊 Sub-Zero Mode", 
                    type="primary" if st.session_state.personality_mode == 'subzero' else "secondary",
                    use_container_width=True):
            st.session_state.personality_mode = 'subzero'
            if CHATBOT_AVAILABLE and chatbot is not None:
                try:
                    chatbot.switch_personality('subzero')
                    st.success("🧊 Sub-Zero mode activated! Ready to freeze the crypto markets! ❄️")
                except Exception as e:
                    st.error(f"Error switching to sub-zero mode: {e}")
            else:
                st.warning("🧊 Sub-Zero mode selected (chatbot features limited)")
            st.rerun()
    
    # Display current personality
    if st.session_state.personality_mode == 'subzero':
        st.markdown("**Current Personality:** 🧊 **Sub-Zero** - Ice-cold crypto warrior")
    else:
        st.markdown("**Current Personality:** 💬 **Normal** - Friendly crypto assistant")

st.markdown("---")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    # Initialize personality mode first
    if 'personality_mode' not in st.session_state:
        st.session_state.personality_mode = 'normal'
    
    # Set welcome message based on personality
    if st.session_state.personality_mode == 'subzero':
        welcome_msg = '🧊 Sub-Zero greets you, crypto warrior! The ice master stands ready to share frozen wisdom about the blockchain realm. What knowledge do you seek? ❄️'
    else:
        welcome_msg = '👋 Welcome to Krypt! I\'m your AI crypto assistant. Ask me about prices, analysis, or just say hi!'
    
    st.session_state.chat_history = [
        {
            'role': 'assistant',
            'message': welcome_msg,
            'personality': st.session_state.personality_mode,
            'timestamp': datetime.now()
        }
    ]

# Cache market data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_market_data():
    if apis is None:
        st.warning("⚠️ Market data not available - API services could not be initialized")
        return []
    
    with st.spinner('Fetching market data...'):
        try:
            return apis.get_markets_data()
        except Exception as e:
            st.warning(f"⚠️ Error fetching market data: {e}")
            return []

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

# Sidebar setup
st.sidebar.markdown("### 🤖 AI Personality")

# Initialize personality in session state if not exists
if 'personality_mode' not in st.session_state:
    st.session_state.personality_mode = 'normal'

# Personality toggle switch
personality_toggle = st.sidebar.toggle(
    "🧊 Sub-Zero Mode", 
    value=(st.session_state.personality_mode == 'subzero'),
    help="Toggle between Normal and Sub-Zero personalities"
)

# Handle personality change
if personality_toggle and st.session_state.personality_mode != 'subzero':
    st.session_state.personality_mode = 'subzero'
    if CHATBOT_AVAILABLE and chatbot is not None:
        try:
            chatbot.switch_personality('subzero')
            st.sidebar.success("🧊 Sub-Zero activated!")
        except Exception as e:
            st.sidebar.error(f"Error activating Sub-Zero: {e}")
    else:
        st.sidebar.warning("🧊 Sub-Zero mode selected (limited features)")
elif not personality_toggle and st.session_state.personality_mode != 'normal':
    st.session_state.personality_mode = 'normal'
    if CHATBOT_AVAILABLE and chatbot is not None:
        try:
            chatbot.switch_personality('normal')
            st.sidebar.success("💬 Normal mode activated!")
        except Exception as e:
            st.sidebar.error(f"Error activating Normal mode: {e}")
    else:
        st.sidebar.warning("💬 Normal mode selected (limited features)")

# Display current personality info
if st.session_state.personality_mode == 'subzero':
    st.sidebar.markdown("**Current:** 🧊 **Sub-Zero** - Ice-cold crypto warrior")
else:
    st.sidebar.markdown("**Current:** 💬 **Normal** - Friendly crypto assistant")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Market Overview")

# Group coins by first letter
coins_by_letter = {}
for coin in market_data:
    first_letter = coin['symbol'][0].upper()
    if first_letter not in coins_by_letter:
        coins_by_letter[first_letter] = []  # Correctly initialize a list for the first letter
    coins_by_letter[first_letter].append(coin)  # Append the coin to the correct list

# Create tabs for navigation
tab1, tab2, tab3 = st.sidebar.tabs(["🏠 Main", "🔝 Top Coins", "📑 All Coins"])

with tab1:
    st.sidebar.markdown("### Latest Updates")
    st.sidebar.info("Welcome to Krypt - Get real-time cryptocurrency analysis and news.")
      # Show featured coins in main tab
    st.sidebar.markdown("### Featured Coins")
    featured_coins = market_data[:5] if len(market_data) >= 5 else market_data
    
    for coin in featured_coins:
        price_change = coin.get('price_change_percentage_24h', 0) or 0
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
        if st.sidebar.button(f"View {coin['symbol'].upper()}", key=f"main_{coin['id']}"):
            st.session_state.selected_coin = coin['id']

with tab2:
    for coin in market_data[:15]:
        price_change = coin.get('price_change_percentage_24h', 0) or 0
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

with tab3:
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
    st.markdown("### 🤖 AI Assistant & Crypto Search")
    crypto_input = st.text_input("💬 Ask me anything about crypto or search for a coin", "", placeholder="Try: 'hi', 'bitcoin price', 'what is ethereum'")
    
    matching_coins = []
    selected_coin = None    # AI Chatbot Integration
    if crypto_input:
        if not CHATBOT_AVAILABLE or chatbot is None:
            st.error("🚫 AI Chatbot is currently unavailable due to missing dependencies. Please contact support.")
        else:
            try:
                # Sync chatbot personality with session state
                if hasattr(chatbot, 'personality_mode'):
                    if chatbot.personality_mode != st.session_state.personality_mode:
                        chatbot.switch_personality(st.session_state.personality_mode)
                
                # Add user message to chat history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'message': crypto_input,
                    'timestamp': datetime.now()
                })
                
                # Get AI response with enhanced capabilities
                ai_response = chatbot.get_response(crypto_input)
                
                # Add AI response to chat history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'message': ai_response['message'],
                    'type': ai_response['type'],
                    'personality': ai_response['personality'],
                    'timestamp': datetime.now()
                })
                
                # Handle specific actions
                if ai_response['type'] == 'personality_switch':
                    st.success(f"🤖 Personality switched! Current mode: {ai_response['personality']}")
                elif ai_response['type'] == 'news_insights':
                    st.info("📰 Real-time crypto news delivered!")
                elif ai_response['type'] in ['subzero_response', 'normal_response']:
                    # Standard chatbot response - no special action needed
                    pass
            except Exception as e:
                st.error(f"🚫 Error with AI chatbot: {e}")
                # Add fallback message to chat history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'message': "Sorry, I'm having trouble processing your request right now. Please try again later.",
                    'type': 'error',
                    'personality': st.session_state.personality_mode,
                    'timestamp': datetime.now()
                })
    
    # Display chat history
    if len(st.session_state.chat_history) > 1:  # More than just welcome message
        st.markdown("### 💬 Chat History")
        chat_container = st.container()
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history[-6:]):  # Show last 6 messages
                if chat['role'] == 'user':
                    st.markdown(f"""
                    <div style='background-color: #0e1117; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 3px solid #4ecdc4;'>
                        <strong>👤 You:</strong> {chat['message']}
                    </div>
                    """, unsafe_allow_html=True)
                else:                    # Color code based on response type
                    color = {
                        'greeting': '#4ecdc4',
                        'price_query': '#00ff00',
                        'news_query': '#ff9800', 
                        'personality_switch': '#9c27b0',
                        'crypto_general': '#2196f3',
                        'farewell': '#4ecdc4',
                        'general': '#607d8b'                    }.get(chat.get('type', 'general'), '#4ecdc4')
                    
                    # Add personality mode indicator
                    current_personality = chat.get('personality', st.session_state.personality_mode)
                    bot_name = "🧊 Sub-Zero AI" if current_personality == "subzero" else "🤖 Krypt AI"
                    
                    st.markdown(f"""
                    <div style='background-color: #1e1e1e; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 3px solid {color};'>
                        <strong>{bot_name}:</strong> {chat['message']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = [st.session_state.chat_history[0]]  # Keep welcome message
            st.experimental_rerun()
          # Fallback to original search if no AI match
        if not selected_coin and len(crypto_input) > 2:
            crypto_input_clean = crypto_input.lower().strip()
            
            # Avoid searching if it's clearly a greeting
            greeting_words = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
            if crypto_input_clean not in greeting_words:
                matching_coins = [
                    coin for coin in market_data 
                    if (crypto_input_clean == coin['symbol'].lower() or 
                        crypto_input_clean == coin['name'].lower() or
                        crypto_input_clean == coin['id'].lower() or
                        (len(crypto_input_clean) > 4 and 
                         crypto_input_clean in coin['name'].lower() and
                         len(coin['name']) - len(crypto_input_clean) <= 3))  # More restrictive substring matching
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
        change = selected_coin.get('price_change_percentage_24h', 0) or 0
        
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
            and abs((c.get('price_change_percentage_24h', 0) or 0) - (selected_coin.get('price_change_percentage_24h', 0) or 0)) < 5        ][:5]
        
        for similar in similar_coins:
            price_change = similar.get('price_change_percentage_24h', 0) or 0
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Developed with ❤️ | Data from CoinGecko, KuCoin & CryptoCompare
</div>
""", unsafe_allow_html=True)