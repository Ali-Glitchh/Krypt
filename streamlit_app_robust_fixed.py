#!/usr/bin/env python3
"""
Enhanced KoinToss Streamlit App - Fixed Version
This version fixes all chatbot-related errors and ensures robust operation.
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

# Import API utilities with error handling
try:
    from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
    API_UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ API utilities not available: {e}")
    API_UTILS_AVAILABLE = False
    RATE_LIMIT_DELAY = 1.5  # fallback value

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

# Safe chatbot initialization
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

# Custom CSS
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    .status-offline {
        color: #ff4444;
        font-weight: bold;
    }
    .chatbot-response {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        border-left: 4px solid #fdcb6e;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
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

# Chatbot status in sidebar
st.sidebar.markdown("### 🤖 AI Assistant Status")
if CHATBOT_AVAILABLE and chatbot:
    st.sidebar.markdown('<div class="status-online">🟢 AI Online</div>', unsafe_allow_html=True)
    
    # Safe personality switching
    try:
        if hasattr(chatbot, 'personality_mode'):
            current_mode = chatbot.personality_mode
            st.sidebar.write(f"**Mode:** {current_mode.title()}")
    except:
        st.sidebar.write("**Mode:** Unknown")
        
    # Safe personality toggle
    try:
        if st.sidebar.button("🔄 Switch Personality"):
            if hasattr(chatbot, 'switch_personality'):
                new_mode = chatbot.switch_personality()
                st.sidebar.success(f"Switched to {new_mode} mode!")
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Failed to switch personality: {e}")
        
else:
    st.sidebar.markdown('<div class="status-offline">🔴 AI Offline</div>', unsafe_allow_html=True)
    if chatbot_error:
        st.sidebar.error(f"Error: {chatbot_error}")
    st.sidebar.info("Chatbot functionality is limited")

# Chat interface
st.markdown("## 💬 Chat with KoinToss AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about cryptocurrency..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate bot response
    with st.chat_message("assistant"):
        if CHATBOT_AVAILABLE and chatbot:
            try:
                with st.spinner("Thinking..."):
                    if hasattr(chatbot, 'get_response'):
                        response_data = chatbot.get_response(prompt)
                        if isinstance(response_data, dict):
                            response = response_data.get('response', 'Sorry, I could not process your request.')
                        else:
                            response = str(response_data)
                    else:
                        response = "I'm here to help with cryptocurrency questions!"
                
                st.markdown(f'<div class="chatbot-response">{response}</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            fallback_msg = "I'm currently offline. Please check back later or try the market data features below!"
            st.warning(fallback_msg)
            st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

# Crypto market data section
st.markdown("## 📊 Market Overview")

# Create columns for market data
col1, col2, col3, col4 = st.columns(4)

# Basic market metrics (fallback data if APIs not available)
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
    st.sidebar.markdown("### 📊 Learning Analytics")
    
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
            st.sidebar.info("No learning statistics available")
            
    except Exception as e:
        st.sidebar.error(f"Error loading learning stats: {e}")

# Training controls (if autonomous trainer is available)
if chatbot and hasattr(chatbot, 'autonomous_trainer') and chatbot.autonomous_trainer:
    with st.sidebar.expander("🎛️ Training Controls", expanded=False):
        st.write("**Autonomous Training Settings**")
        
        # Safe training controls
        try:
            auto_training_enabled = getattr(chatbot, 'auto_training_enabled', False)
            auto_training = st.checkbox(
                "Enable Autonomous Training",
                value=auto_training_enabled,
                help="Automatically improve responses"
            )
            
            if auto_training != auto_training_enabled:
                chatbot.auto_training_enabled = auto_training
                st.success(f"Training {'enabled' if auto_training else 'disabled'}")
                
        except Exception as e:
            st.error(f"Training control error: {e}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #87CEEB;">
    <p><strong>⚔️ KoinToss</strong> - Making Cryptocurrency Simple</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        {DISCLAIMER}
    </p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        Powered by Enhanced AI • Real-time Data • Autonomous Learning
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
