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

# Utility functions
def format_number(num):
    """Format numbers for display"""
    if num is None:
        return "N/A"
    
    try:
        num = float(num)
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
    except (ValueError, TypeError):
        return "N/A"

def analyze_sentiment(text, symbol):
    """Analyze sentiment of text"""
    try:
        crypto_apis, analyzer = initialize_services()
        if crypto_apis and hasattr(analyzer, 'polarity_scores'):
            scores = analyzer.polarity_scores(text)
            return scores['compound']
        else:
            # Simple fallback sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'positive', 'bullish', 'up', 'gain', 'profit']
            negative_words = ['bad', 'poor', 'negative', 'bearish', 'down', 'loss', 'crash', 'dump']
            
            text_lower = text.lower()
            positive_count = sum(word in text_lower for word in positive_words)
            negative_count = sum(word in text_lower for word in negative_words)
            
            if positive_count > negative_count:
                return 0.5
            elif negative_count > positive_count:
                return -0.5
            else:
                return 0.0
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 0.0

def get_investment_sentiment(price_change, news_sentiment):
    """Get investment sentiment based on price and news"""
    try:
        combined_score = (price_change * 0.6) + (news_sentiment * 40)  # Weight price change more
        
        if combined_score > 5:
            return "🚀 Very Bullish", "Strong positive momentum with good news sentiment"
        elif combined_score > 2:
            return "📈 Bullish", "Positive momentum with favorable conditions"
        elif combined_score > -2:
            return "⚖️ Neutral", "Mixed signals, wait for clearer direction"
        elif combined_score > -5:
            return "📉 Bearish", "Negative momentum with concerning indicators"
        else:
            return "🔻 Very Bearish", "Strong negative momentum with poor sentiment"
    except Exception as e:
        return "❓ Unknown", "Unable to analyze sentiment"

def show_enhanced_learning_stats():
    """Placeholder for enhanced learning stats"""
    st.info("Enhanced learning stats feature coming soon!")

def show_configuration_panel():
    """Placeholder for configuration panel"""
    st.info("Configuration panel feature coming soon!")

# Disclaimer
DISCLAIMER = "⚠️ This is not financial advice. Always do your own research before making investment decisions."

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
    page_title="KoinToss - Enhanced Crypto Assistant",
    page_icon="⚔️",
    layout="wide",
)

# Enhanced KoinToss Branding and Logo Animation
def add_kointoss_branding():
    """Add KoinToss branding with animated logo and enhanced styling"""
    
    # Custom CSS for KoinToss branding
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* KoinToss Logo Animation */
    .kointoss-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
        animation: logoGlow 3s ease-in-out infinite alternate;
    }
    
    .logo-container {
        position: relative;
        text-align: center;
        padding: 20px;
        background: radial-gradient(circle, rgba(135, 206, 250, 0.1) 0%, transparent 70%);
        border-radius: 20px;
        border: 1px solid rgba(135, 206, 250, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .axe-symbol {
        font-size: 4rem;
        color: #87CEEB;
        text-shadow: 0 0 20px rgba(135, 206, 250, 0.6);
        animation: axeRotate 4s linear infinite;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .brand-name {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 15px rgba(135, 206, 250, 0.4);
        margin: 10px 0;
        letter-spacing: 2px;
    }
    
    .brand-tagline {
        font-size: 1rem;
        color: #87CEEB;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 3px;
        opacity: 0.9;
    }
    
    /* Animations */
    @keyframes logoGlow {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(135, 206, 250, 0.3); }
        100% { transform: scale(1.02); box-shadow: 0 0 40px rgba(135, 206, 250, 0.6); }
    }
    
    @keyframes axeRotate {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(-5deg); }
        50% { transform: rotate(0deg); }
        75% { transform: rotate(5deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid rgba(135, 206, 250, 0.3);
        border-radius: 50%;
        border-top-color: #87CEEB;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Enhanced Chat Interface */
    .chat-container {
        background: rgba(26, 26, 46, 0.7);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(135, 206, 250, 0.2);
        backdrop-filter: blur(10px);
        margin: 10px 0;
    }
    
    .user-message {
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(135, 206, 250, 0.3);
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(135, 206, 250, 0.3);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .subzero-message {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        border: 1px solid rgba(135, 206, 250, 0.5);
    }
    
    /* Enhanced Metrics */
    .metric-card {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(135, 206, 250, 0.2);
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #87CEEB;
        text-shadow: 0 0 10px rgba(135, 206, 250, 0.4);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #ffffff;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-weight: 500;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(135, 206, 250, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(135, 206, 250, 0.4);
        background: linear-gradient(45deg, #4682B4, #87CEEB);
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: rgba(10, 10, 10, 0.9);
        border-right: 1px solid rgba(135, 206, 250, 0.2);
    }
    
    /* Enhanced Text Input */
    .stTextInput > div > div > input {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid rgba(135, 206, 250, 0.3);
        border-radius: 25px;
        color: white;
        padding: 12px 20px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #87CEEB;
        box-shadow: 0 0 15px rgba(135, 206, 250, 0.3);
    }
    
    /* Status Indicators */
    .status-online {
        color: #00ff88;
        animation: pulse 2s infinite;
    }
    
    .status-offline {
        color: #ff4444;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Enhanced Tables */
    .dataframe {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(135, 206, 250, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(135, 206, 250, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # KoinToss Logo Header
    st.markdown("""
    <div class="kointoss-logo">
        <div class="logo-container">
            <div class="axe-symbol">⚔️</div>
            <div class="brand-name">KOINTOSS</div>
            <div class="brand-tagline">CRYPTO MADE SIMPLE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation(message="Loading..."):
    """Display loading animation with KoinToss branding"""
    return st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div class="loading-spinner"></div>
        <p style="color: #87CEEB; margin-top: 10px; font-weight: 500;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def enhanced_chat_message(message, is_user=False, personality="normal"):
    """Display enhanced chat messages with KoinToss styling"""
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 You:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        personality_icon = "🧊" if personality == "subzero" else "🤖"
        personality_name = "Sub-Zero AI" if personality == "subzero" else "Krypt AI"
        message_class = "subzero-message" if personality == "subzero" else "bot-message"
        
        st.markdown(f"""
        <div class="bot-message {message_class}">
            <strong>{personality_icon} {personality_name}:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

def enhanced_metric_display(label, value, delta=None):
    """Display enhanced metrics with KoinToss styling"""
    delta_html = f"<div style='color: #00ff88; font-size: 0.8rem;'>↗ {delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

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

# Initialize services and chatbot
apis, analyzer = initialize_services()
chatbot = initialize_chatbot()

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

# Check if special panels should be shown
if st.session_state.get('show_learning_stats'):
    show_enhanced_learning_stats()
    if st.button("← Back to Chat"):
        st.session_state['show_learning_stats'] = False
        st.rerun()
elif st.session_state.get('show_config'):
    show_configuration_panel()
    if st.button("← Back to Chat"):
        st.session_state['show_config'] = False
        st.rerun()
else:
    # Normal chat interface
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
                    })                    # Get AI response with enhanced capabilities
                    ai_response = chatbot.get_response(crypto_input)
                    
                    # FINAL FIX: Robust handling of all response types
                    response_message = ""
                    response_type = "unknown"
                    response_personality = st.session_state.personality_mode
                    
                    try:
                        if isinstance(ai_response, dict):
                            # Extract message from dictionary response
                            response_message = ai_response.get('message', '')
                            response_type = ai_response.get('type', 'dict_response')
                            response_personality = ai_response.get('personality', st.session_state.personality_mode)
                            
                            # If message is empty, try other keys or convert to string
                            if not response_message:
                                response_message = ai_response.get('response', str(ai_response))
                                
                        elif isinstance(ai_response, str):
                            # Handle string response directly - SAFE STRIP
                            response_message = ai_response.strip() if ai_response else ""
                            response_type = 'string_response'
                            
                        else:
                            # Handle any other type by converting to string
                            response_message = str(ai_response) if ai_response else ""
                            response_type = f'converted_from_{type(ai_response).__name__}'
                    
                    except Exception as response_parse_error:
                        # If any error in parsing, provide safe fallback
                        response_message = f"Response parsing error: {str(response_parse_error)}"
                        response_type = 'parse_error'
                    
                    # Final safety check - ensure we have a valid string message
                    if not response_message or not isinstance(response_message, str):
                        response_message = "Sorry, I'm having trouble processing your request right now. Please try again later."
                        response_type = 'fallback_error'
                    
                    # Safe strip only if it's definitely a string
                    if isinstance(response_message, str) and response_message.strip() == '':
                        response_message = "Sorry, I received an empty response. Please try again."
                    
                    # Add AI response to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'message': response_message,
                        'type': response_type,
                        'personality': response_personality,
                        'timestamp': datetime.now()
                    })
                      # Handle specific actions
                    if response_type == 'personality_switch':
                        st.success(f"🤖 Personality switched! Current mode: {response_personality}")
                    elif response_type == 'news_insights':
                        st.info("📰 Real-time crypto news delivered!")
                    elif response_type in ['subzero_response', 'normal_response']:
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

# Enhanced Learning Analytics and Configuration
if CHATBOT_AVAILABLE and chatbot is not None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Learning & Configuration")
    
    # Learning analytics section
    with st.sidebar.expander("🧠 Advanced Learning Analytics", expanded=False):
        try:
            # Get learning stats
            stats = chatbot.get_learning_stats()
            training_stats = chatbot.autonomous_trainer.get_training_statistics()
            
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Conversations", stats.get('total_conversations', 0))
                st.metric("Training Sessions", training_stats.get('total_sessions', 0))
            
            with col2:
                st.metric("Learning Accuracy", f"{stats.get('accuracy_rate', 0):.1f}%")
                st.metric("Improvement Rate", f"{training_stats.get('improvement_rate', 0):.1f}%")
            
            with col3:
                st.metric("Context Awareness", f"{stats.get('context_awareness_rate', 0):.1f}%")
                st.metric("Quality Threshold", f"{stats.get('current_threshold', 0):.3f}")
            
            with col4:
                st.metric("Vocabulary Size", stats.get('vocabulary_size', 0))
                st.metric("Auto Training", "🟢 ON" if chatbot.auto_training_enabled else "🔴 OFF")
            
            # Training progress chart
            if training_stats.get('accuracy_history'):
                st.subheader("📈 Learning Progress Over Time")
                
                import plotly.express as px
                import pandas as pd
                
                df = pd.DataFrame({
                    'Session': range(1, len(training_stats['accuracy_history']) + 1),
                    'Accuracy': training_stats['accuracy_history']
                })
                
                fig = px.line(df, x='Session', y='Accuracy', 
                             title='Training Accuracy Improvement',
                             labels={'Accuracy': 'Accuracy (%)', 'Session': 'Training Session'})
                fig.update_traces(line_color='#1f77b4', line_width=3)
                fig.update_layout(
                    xaxis_title="Training Session",
                    yaxis_title="Accuracy (%)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Training scenarios breakdown
            st.subheader("🎯 Training Scenarios Coverage")
            scenarios = chatbot.autonomous_trainer.training_scenarios
            
            scenario_data = []
            for scenario in scenarios:
                scenario_data.append({
                    'Category': scenario['category'].replace('_', ' ').title(),
                    'Questions': len(scenario['questions']),
                    'Expected Quality': f"{scenario['expected_quality']:.1%}"
                })
            
            df_scenarios = pd.DataFrame(scenario_data)
            st.dataframe(df_scenarios, use_container_width=True)
            
            # Recent training activities
            st.subheader("🔄 Recent Training Activities")
            recent_activities = training_stats.get('recent_activities', [])
            
            if recent_activities:
                for activity in recent_activities[-5:]:  # Show last 5
                    with st.expander(f"Session {activity.get('session_id', 'Unknown')} - {activity.get('timestamp', 'Unknown time')}"):
                        st.write(f"**Scenario:** {activity.get('scenario', 'Unknown')}")
                        st.write(f"**Question:** {activity.get('question', 'Unknown')}")
                        st.write(f"**Quality Score:** {activity.get('quality_score', 0):.2f}")
                        st.write(f"**Improvement:** {activity.get('improvement', 'Unknown')}")
            else:
                st.info("No recent training activities available. Start autonomous training to see activities here.")
        
        except Exception as e:
            st.error(f"Error loading learning stats: {e}")
            st.info("Basic learning functionality may still be available.")
    
    # Configuration panel section
    with st.sidebar.expander("⚙️ Training Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Autonomous Training Settings**")
            
            # Auto-training toggle
            auto_training = st.checkbox(
                "Enable Autonomous Training",
                value=chatbot.auto_training_enabled,
                help="Automatically improve responses through background training"
            )
            
            if auto_training != chatbot.auto_training_enabled:
                if auto_training:
                    chatbot.start_autonomous_training()
                else:
                    chatbot.stop_autonomous_training()
            
            # Training interval
            if hasattr(chatbot.autonomous_trainer, 'training_interval'):
                interval = st.slider(
                    "Training Interval (minutes)",
                    min_value=1,
                    max_value=60,
                    value=chatbot.autonomous_trainer.training_interval // 60,
                    help="How often to run training sessions"
                )
                chatbot.autonomous_trainer.training_interval = interval * 60
            
            # Quality threshold
            if hasattr(chatbot.autonomous_trainer, 'quality_threshold'):
                threshold = st.slider(
                    "Quality Threshold",
                    min_value=0.5,
                    max_value=1.0,
                    value=chatbot.autonomous_trainer.quality_threshold,
                    step=0.05,
                    help="Minimum quality score for accepting responses"
                )
                chatbot.autonomous_trainer.quality_threshold = threshold
        
        with col2:
            st.write("**Data Export Options**")
            
            # Export conversation history
            if st.button("📥 Export Conversation History"):
                try:
                    conversations = chatbot.conversation_history
                    if conversations:
                        import json
                        export_data = {
                            'export_date': datetime.now().isoformat(),
                            'total_conversations': len(conversations),
                            'conversations': conversations
                        }
                        
                        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="Download Conversation History",
                            data=json_data,
                            file_name=f"conversation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    else:
                        st.info("No conversation history available for export.")
                except Exception as e:
                    st.error(f"Export failed: {e}")
            
            # Export training data
            if st.button("📊 Export Training Statistics"):
                try:
                    stats = chatbot.get_learning_stats()
                    training_stats = chatbot.autonomous_trainer.get_training_statistics()
                    
                    export_data = {
                        'export_date': datetime.now().isoformat(),
                        'learning_stats': stats,
                        'training_stats': training_stats
                    }
                    
                    import json
                    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="Download Training Statistics",
                        data=json_data,
                        file_name=f"training_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Export failed: {e}")
            
            # Manual training trigger
            st.write("**Manual Training Controls**")
            if st.button("🚀 Run Training Session Now"):
                try:
                    with st.spinner("Running training session..."):
                        chatbot.autonomous_trainer.run_single_training_iteration()
                    st.success("Training session completed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Training session failed: {e}")

# Utility functions
def format_number(num):
    """Format numbers for display"""
    if num is None:
        return "N/A"
    
    try:
        num = float(num)
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
    except (ValueError, TypeError):
        return "N/A"

def analyze_sentiment(text, symbol):
    """Analyze sentiment of text"""
    try:
        crypto_apis, analyzer = initialize_services()
        if crypto_apis and hasattr(analyzer, 'polarity_scores'):
            scores = analyzer.polarity_scores(text)
            return scores['compound']
        else:
            # Simple fallback sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'positive', 'bullish', 'up', 'gain', 'profit']
            negative_words = ['bad', 'poor', 'negative', 'bearish', 'down', 'loss', 'crash', 'dump']
            
            text_lower = text.lower()
            positive_count = sum(word in text_lower for word in positive_words)
            negative_count = sum(word in text_lower for word in negative_words)
            
            if positive_count > negative_count:
                return 0.5
            elif negative_count > positive_count:
                return -0.5
            else:
                return 0.0
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 0.0

def get_investment_sentiment(price_change, news_sentiment):
    """Get investment sentiment based on price and news"""
    try:
        combined_score = (price_change * 0.6) + (news_sentiment * 40)  # Weight price change more
        
        if combined_score > 5:
            return "🚀 Very Bullish", "Strong positive momentum with good news sentiment"
        elif combined_score > 2:
            return "📈 Bullish", "Positive momentum with favorable conditions"
        elif combined_score > -2:
            return "⚖️ Neutral", "Mixed signals, wait for clearer direction"
        elif combined_score > -5:
            return "📉 Bearish", "Negative momentum with concerning indicators"
        else:
            return "🔻 Very Bearish", "Strong negative momentum with poor sentiment"
    except Exception as e:
        return "❓ Unknown", "Unable to analyze sentiment"

# Disclaimer
DISCLAIMER = "⚠️ This is not financial advice. Always do your own research before making investment decisions."

# Main Interface with Enhanced KoinToss Styling
st.markdown("### 💬 Chat with KoinToss AI")

# Chat interface with enhanced styling
with st.container():
    # Chat input
    user_input = st.text_input(
        "Ask me anything about cryptocurrency:", 
        placeholder="Try asking about 'pi coin', 'bitcoin price', or 'what is ethereum'",
        key="chat_input"
    )
    
    if user_input:
        # Show loading animation
        loading_placeholder = st.empty()
        with loading_placeholder:
            show_loading_animation("Processing your request...")
        
        try:
            # Get response from chatbot
            if chatbot:
                response = chatbot.get_response(user_input)
                
                # Clear loading animation
                loading_placeholder.empty()
                
                # Display enhanced chat messages
                enhanced_chat_message(user_input, is_user=True)
                
                if isinstance(response, dict):
                    enhanced_chat_message(
                        response['message'], 
                        is_user=False, 
                        personality=response.get('personality', 'normal')
                    )
                else:
                    enhanced_chat_message(response, is_user=False)
                    
            else:
                loading_placeholder.empty()
                st.error("❌ Chatbot not available. Please check the system status.")
                
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"❌ Error processing your request: {e}")

# Enhanced status display
st.markdown("---")
st.markdown("### 📊 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if chatbot:
        st.markdown('<div class="status-online">🟢 Online</div>', unsafe_allow_html=True)
        st.text("Chatbot Status")
    else:
        st.markdown('<div class="status-offline">🔴 Offline</div>', unsafe_allow_html=True)
        st.text("Chatbot Status")

with col2:
    if API_UTILS_AVAILABLE:
        st.markdown('<div class="status-online">🟢 Connected</div>', unsafe_allow_html=True)
        st.text("API Services")
    else:
        st.markdown('<div class="status-offline">🔴 Disconnected</div>', unsafe_allow_html=True)
        st.text("API Services")

with col3:
    if chatbot and hasattr(chatbot, 'autonomous_trainer'):
        training_status = "🟢 Active" if getattr(chatbot, 'auto_training_enabled', False) else "🟡 Standby"
        st.markdown(f'<div class="status-online">{training_status}</div>', unsafe_allow_html=True)
        st.text("Auto Training")
    else:
        st.markdown('<div class="status-offline">🔴 Inactive</div>', unsafe_allow_html=True)
        st.text("Auto Training")

with col4:
    # Check conversation count
    if chatbot and hasattr(chatbot, 'get_learning_stats'):
        try:
            stats = chatbot.get_learning_stats()
            conv_count = stats.get('total_conversations', 0)
            st.markdown(f'<div class="metric-value">{conv_count}</div>', unsafe_allow_html=True)
            st.text("Conversations")
        except:
            st.markdown('<div class="metric-value">-</div>', unsafe_allow_html=True)
            st.text("Conversations")
    else:
        st.markdown('<div class="metric-value">-</div>', unsafe_allow_html=True)
        st.text("Conversations")

# Enhanced footer with KoinToss branding
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #87CEEB;">
    <p><strong>⚔️ KoinToss</strong> - Making Cryptocurrency Simple</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        Powered by Enhanced AI • Real-time Data • Autonomous Learning
    </p>
</div>
""", unsafe_allow_html=True)