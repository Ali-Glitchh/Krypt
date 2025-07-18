#!/usr/bin/env python3
"""
Enhanced Streamlit App with Improved Crypto Query Handling
Fixes SubZero personality response issues and adds real-time price data integration
"""

import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import re
import traceback
import json

# Import API utilities with error handling
try:
    from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
    API_UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ API utilities not available: {e}")
    API_UTILS_AVAILABLE = False
    RATE_LIMIT_DELAY = 1.5

# Import chatbot with comprehensive error handling
CHATBOT_AVAILABLE = False
chatbot_error = None

try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    CHATBOT_AVAILABLE = True
except ImportError as e:
    chatbot_error = f"improved_dual_personality_chatbot: {e}"

if not CHATBOT_AVAILABLE:
    try:
        from crypto_chatbot_fixed import CryptoChatbotFixed as ImprovedDualPersonalityChatbot
        CHATBOT_AVAILABLE = True
        chatbot_error = None
    except ImportError as e:
        chatbot_error = f"crypto_chatbot_fixed: {e}"

if not CHATBOT_AVAILABLE:
    try:
        from crypto_chatbot import CryptoChatbot as ImprovedDualPersonalityChatbot
        CHATBOT_AVAILABLE = True
        chatbot_error = None
    except ImportError as e:
        chatbot_error = f"crypto_chatbot: {e}"

# Enhanced utility functions
def get_crypto_price(symbol):
    """Get real-time crypto price from CoinGecko"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if symbol in data:
                return data[symbol]['usd']
    except Exception as e:
        st.error(f"Error fetching price for {symbol}: {e}")
    return None

def detect_crypto_query(text):
    """Detect if user is asking about specific crypto prices or info"""
    text_lower = text.lower()
    
    # Price keywords
    price_keywords = ['price', 'cost', 'value', 'worth', 'trading at', 'current']
    
    # Crypto mapping
    crypto_map = {
        'bitcoin': 'bitcoin',
        'btc': 'bitcoin',
        'ethereum': 'ethereum', 
        'eth': 'ethereum',
        'cardano': 'cardano',
        'ada': 'cardano',
        'solana': 'solana',
        'sol': 'solana',
        'dogecoin': 'dogecoin',
        'doge': 'dogecoin',
        'polkadot': 'polkadot',
        'dot': 'polkadot',
        'chainlink': 'chainlink',
        'link': 'chainlink'
    }
    
    # Check for price queries
    is_price_query = any(keyword in text_lower for keyword in price_keywords)
    
    # Find mentioned crypto
    mentioned_crypto = None
    for crypto_name, api_id in crypto_map.items():
        if crypto_name in text_lower:
            mentioned_crypto = api_id
            break
    
    return is_price_query, mentioned_crypto

def enhance_response_with_price_data(user_input, bot_response, personality_mode):
    """Enhance bot response with real-time price data if relevant"""
    is_price_query, crypto_id = detect_crypto_query(user_input)
    
    if is_price_query and crypto_id:
        price = get_crypto_price(crypto_id)
        if price:
            if personality_mode == "subzero":
                price_info = f"\n\n🧊 **ICE-COLD PRICE UPDATE**: {crypto_id.title()} is currently trading at **${price:,.2f}** USD. The markets flow like ice through my veins! ❄️"
            else:
                price_info = f"\n\n📊 **Real-time Price**: {crypto_id.title()} is currently trading at **${price:,.2f}** USD."
            
            return bot_response + price_info
    
    return bot_response

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
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = "Bullish 📈"
            color = "green"
        elif compound <= -0.05:
            sentiment = "Bearish 📉"
            color = "red"
        else:
            sentiment = "Neutral ➡️"
            color = "gray"
            
        return sentiment, color, compound
    except Exception as e:
        return "Unknown", "gray", 0.0

# Disclaimer
DISCLAIMER = "⚠️ This is not financial advice. Always do your own research before making investment decisions."

# Enhanced chatbot initialization
@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot with comprehensive error handling"""
    if not CHATBOT_AVAILABLE:
        return None
    
    try:
        chatbot = ImprovedDualPersonalityChatbot()
        return chatbot
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
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
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4A90E2;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        text-align: center;
        color: #87CEEB;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .personality-toggle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .subzero-mode {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        border-left: 4px solid #00cec9;
    }
    .normal-mode {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        border-left: 4px solid #00b894;
    }
    .chatbot-response {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .price-highlight {
        background: #00b894;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
    }
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    .status-offline {
        color: #ff4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
crypto_apis, analyzer = initialize_services()

# Initialize chatbot
chatbot = initialize_chatbot()

# Main header
st.markdown('<h1 class="main-header">⚔️ KoinToss</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enhanced Cryptocurrency Assistant with Dual Personality AI</p>', unsafe_allow_html=True)

# Enhanced personality display and controls
if CHATBOT_AVAILABLE and chatbot:
    current_personality = getattr(chatbot, 'personality_mode', 'normal')
    
    # Personality status display
    if current_personality == "subzero":
        st.markdown("""
        <div class="personality-toggle subzero-mode">
            🧊 <strong>SUB-ZERO MODE ACTIVE</strong> ❄️<br>
            <em>Ice-cold crypto wisdom from the Lin Kuei master</em>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="personality-toggle normal-mode">
            🤖 <strong>NORMAL MODE ACTIVE</strong> 📈<br>
            <em>Friendly crypto assistance and guidance</em>
        </div>
        """, unsafe_allow_html=True)

# Chatbot status in sidebar
st.sidebar.markdown("### 🤖 AI Assistant Status")
if CHATBOT_AVAILABLE and chatbot:
    st.sidebar.markdown('<div class="status-online">🟢 AI Online</div>', unsafe_allow_html=True)
    
    # Enhanced personality switching
    try:
        if hasattr(chatbot, 'personality_mode'):
            current_mode = chatbot.personality_mode
            st.sidebar.write(f"**Current Mode:** {current_mode.title()}")
            
            # Personality selection
            new_mode = st.sidebar.selectbox(
                "Choose Personality:",
                ["normal", "subzero"],
                index=0 if current_mode == "normal" else 1,
                help="Switch between friendly normal mode and ice-cold SubZero mode"
            )
            
            if new_mode != current_mode:
                if hasattr(chatbot, 'switch_personality'):
                    switch_msg = chatbot.switch_personality(new_mode)
                    st.sidebar.success(switch_msg)
                    st.rerun()
    except Exception as e:
        st.sidebar.error(f"Personality control error: {e}")
        
else:
    st.sidebar.markdown('<div class="status-offline">🔴 AI Offline</div>', unsafe_allow_html=True)
    if chatbot_error:
        st.sidebar.error(f"Error: {chatbot_error}")
    st.sidebar.info("Chatbot functionality is limited")

# Enhanced Chat Interface
st.markdown("## 💬 Chat with KoinToss AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "personality" in message:
            personality = message.get("personality", "normal")
            css_class = "subzero-mode" if personality == "subzero" else "normal-mode"
            st.markdown(f'<div class="chatbot-response {css_class}">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Enhanced Chat input with suggestions
example_queries = [
    "What is the price of Bitcoin?",
    "Tell me about Ethereum",
    "How does DeFi work?",
    "What is cold storage?",
    "Explain blockchain technology"
]

with st.expander("💡 Example Questions", expanded=False):
    for query in example_queries:
        if st.button(query, key=f"example_{query[:10]}"):
            st.session_state.example_query = query

# Handle example query
if "example_query" in st.session_state:
    prompt = st.session_state.example_query
    del st.session_state.example_query
else:
    prompt = st.chat_input("Ask me anything about cryptocurrency...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate enhanced bot response
    with st.chat_message("assistant"):
        if CHATBOT_AVAILABLE and chatbot:
            try:
                with st.spinner("Thinking..."):
                    if hasattr(chatbot, 'get_response'):
                        response_data = chatbot.get_response(prompt)
                        if isinstance(response_data, dict):
                            base_response = response_data.get('response', response_data.get('message', 'Sorry, I could not process your request.'))
                            personality = response_data.get('personality', 'normal')
                        else:
                            base_response = str(response_data)
                            personality = getattr(chatbot, 'personality_mode', 'normal')
                        
                        # Enhance response with price data
                        enhanced_response = enhance_response_with_price_data(prompt, base_response, personality)
                        
                    else:
                        enhanced_response = "I'm here to help with cryptocurrency questions!"
                        personality = "normal"
                
                # Display with personality-specific styling
                css_class = "subzero-mode" if personality == "subzero" else "normal-mode"
                st.markdown(f'<div class="chatbot-response {css_class}">{enhanced_response}</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": enhanced_response,
                    "personality": personality
                })
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            fallback_msg = "I'm currently offline. Please check back later or try the market data features below!"
            st.warning(fallback_msg)
            st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

# Quick Price Checker
st.markdown("## 💰 Quick Price Checker")
price_col1, price_col2, price_col3 = st.columns(3)

popular_cryptos = ['bitcoin', 'ethereum', 'cardano', 'solana', 'dogecoin', 'polkadot']

with price_col1:
    if st.button("📊 Bitcoin Price"):
        price = get_crypto_price('bitcoin')
        if price:
            st.success(f"Bitcoin: ${price:,.2f} USD")

with price_col2:
    if st.button("📊 Ethereum Price"):
        price = get_crypto_price('ethereum')
        if price:
            st.success(f"Ethereum: ${price:,.2f} USD")

with price_col3:
    if st.button("📊 Cardano Price"):
        price = get_crypto_price('cardano')
        if price:
            st.success(f"Cardano: ${price:,.2f} USD")

# Market Overview
st.markdown("## 📊 Market Overview")

# Create columns for market data
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-value">$2.1T</div>', unsafe_allow_html=True)
    st.text("Market Cap")

with col2:
    st.markdown('<div class="metric-value">$95B</div>', unsafe_allow_html=True)
    st.text("24h Volume")

with col3:
    if chatbot and hasattr(chatbot, 'autonomous_trainer') and chatbot.autonomous_trainer:
        st.markdown('<div class="status-online">🟢 Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">🔴 Inactive</div>', unsafe_allow_html=True)
    st.text("Auto Training")

with col4:
    # Safe conversation count
    if chatbot:
        try:
            if hasattr(chatbot, 'get_learning_statistics'):
                stats = chatbot.get_learning_statistics()
                conv_count = stats.get('total_conversations', 0)
            elif hasattr(chatbot, 'conversation_history'):
                conv_count = len(chatbot.conversation_history)
            else:
                conv_count = len(st.session_state.messages) // 2
            st.markdown(f'<div class="metric-value">{conv_count}</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="metric-value">-</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-value">-</div>', unsafe_allow_html=True)
    st.text("Conversations")

# Learning stats sidebar (if available)
if chatbot and CHATBOT_AVAILABLE:
    st.sidebar.markdown("### 📊 AI Analytics")
    
    try:
        # Safe stats retrieval
        stats = {}
        if hasattr(chatbot, 'get_learning_statistics'):
            stats = chatbot.get_learning_statistics()
        elif hasattr(chatbot, 'learning_stats'):
            stats = chatbot.learning_stats
        
        # Display available stats
        if stats:
            st.sidebar.metric("Total Conversations", stats.get('total_conversations', 0))
            st.sidebar.metric("Successful Responses", stats.get('successful_responses', 0))
            accuracy = stats.get('accuracy_rate', 0.0)
            st.sidebar.metric("Accuracy Rate", f"{accuracy:.1%}")
        else:
            st.sidebar.info("No analytics available")
            
    except Exception as e:
        st.sidebar.error(f"Analytics error: {e}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #87CEEB;">
    <p><strong>⚔️ KoinToss</strong> - Making Cryptocurrency Simple</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        {DISCLAIMER}
    </p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        Enhanced with Real-time Price Data • Dual Personality AI • Live Market Updates
    </p>
</div>
""", unsafe_allow_html=True)

# Debug info (only in development)
if st.sidebar.checkbox("Show Debug Info", value=False):
    st.sidebar.markdown("### 🐛 Debug Information")
    st.sidebar.write(f"Chatbot Available: {CHATBOT_AVAILABLE}")
    st.sidebar.write(f"API Utils Available: {API_UTILS_AVAILABLE}")
    if chatbot_error:
        st.sidebar.write(f"Chatbot Error: {chatbot_error}")
    if chatbot:
        st.sidebar.write(f"Chatbot Type: {type(chatbot).__name__}")
        if hasattr(chatbot, 'personality_mode'):
            st.sidebar.write(f"Personality Mode: {chatbot.personality_mode}")

# Personality Comparison Feature
st.markdown("## ⚔️ Personality Comparison")
st.markdown("*See how both personalities respond to the same question*")

if CHATBOT_AVAILABLE and chatbot:
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("### 🤖 Normal Mode")
        comparison_query = st.text_input("Ask both personalities:", key="comparison_input")
        
    with comp_col2:
        st.markdown("### 🧊 SubZero Mode")
        st.text_input("Same question:", value=comparison_query, disabled=True, key="comparison_display")
    
    if st.button("🔄 Compare Responses") and comparison_query:
        with st.spinner("Getting responses from both personalities..."):
            # Get normal response
            original_mode = chatbot.personality_mode
            
            # Normal mode response
            chatbot.switch_personality("normal")
            try:
                normal_response_data = chatbot.get_response(comparison_query)
                if isinstance(normal_response_data, dict):
                    normal_response = normal_response_data.get('response', normal_response_data.get('message', 'No response'))
                else:
                    normal_response = str(normal_response_data)
                normal_response = enhance_response_with_price_data(comparison_query, normal_response, "normal")
            except Exception as e:
                normal_response = f"Error in normal mode: {e}"
            
            # SubZero mode response  
            chatbot.switch_personality("subzero")
            try:
                subzero_response_data = chatbot.get_response(comparison_query)
                if isinstance(subzero_response_data, dict):
                    subzero_response = subzero_response_data.get('response', subzero_response_data.get('message', 'No response'))
                else:
                    subzero_response = str(subzero_response_data)
                subzero_response = enhance_response_with_price_data(comparison_query, subzero_response, "subzero")
            except Exception as e:
                subzero_response = f"Error in SubZero mode: {e}"
            
            # Restore original mode
            chatbot.switch_personality(original_mode)
            
            # Display comparison
            comp_display_col1, comp_display_col2 = st.columns(2)
            
            with comp_display_col1:
                st.markdown('<div class="chatbot-response normal-mode">' + normal_response + '</div>', unsafe_allow_html=True)
                
            with comp_display_col2:
                st.markdown('<div class="chatbot-response subzero-mode">' + subzero_response + '</div>', unsafe_allow_html=True)
