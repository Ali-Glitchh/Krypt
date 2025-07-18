import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import re
import os
import json

# Import API utilities with error handling
try:
    from api_utils import CryptoAPIs, RATE_LIMIT_DELAY
    API_UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ API utilities not available: {e}")
    API_UTILS_AVAILABLE = False
    RATE_LIMIT_DELAY = 1.5  # fallback value

# Import chatbot with error handling - try multiple versions
CHATBOT_AVAILABLE = False
chatbot_module = None

# Try importing different chatbot versions
try:
    from improved_dual_personality_chatbot_fixed import ImprovedDualPersonalityChatbot
    chatbot_module = "improved_dual_personality_chatbot_fixed"
    CHATBOT_AVAILABLE = True
    st.success("✅ Using fixed dual personality chatbot")
except ImportError:
    try:
        from crypto_chatbot_fixed import ImprovedDualPersonalityChatbot
        chatbot_module = "crypto_chatbot_fixed"
        CHATBOT_AVAILABLE = True
        st.success("✅ Using crypto chatbot fixed version")
    except ImportError:
        try:
            from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
            chatbot_module = "improved_dual_personality_chatbot"
            CHATBOT_AVAILABLE = True
            st.warning("⚠️ Using original chatbot - some features may be limited")
        except ImportError:
            try:
                from crypto_chatbot import ImprovedDualPersonalityChatbot
                chatbot_module = "crypto_chatbot"
                CHATBOT_AVAILABLE = True
                st.warning("⚠️ Using basic crypto chatbot")
            except ImportError as e:
                st.error(f"❌ Error importing chatbot: {e}")
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
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        
        # Additional crypto-specific keyword analysis
        crypto_keywords = {
            'positive': ['moon', 'rocket', 'hodl', 'diamond hands', 'bullish', 'pump', 'surge', 'rally'],
            'negative': ['dump', 'crash', 'bear', 'dip', 'fud', 'panic', 'sell off', 'decline']
        }
        
        text_lower = text.lower()
        keyword_score = 0
        
        for word in crypto_keywords['positive']:
            if word in text_lower:
                keyword_score += 0.1
        
        for word in crypto_keywords['negative']:
            if word in text_lower:
                keyword_score -= 0.1
        
        # Combine scores
        final_score = scores['compound'] + keyword_score
        final_score = max(-1, min(1, final_score))  # Clamp between -1 and 1
        
        return {
            'compound': final_score,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
    except Exception as e:
        st.error(f"Error in sentiment analysis: {e}")
        return {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1}

def get_crypto_data():
    """Get cryptocurrency data"""
    if not API_UTILS_AVAILABLE:
        return None
    
    try:
        crypto_apis = CryptoAPIs()
        data = crypto_apis.get_top_cryptocurrencies(limit=10)
        return data
    except Exception as e:
        st.error(f"Error fetching crypto data: {e}")
        return None

def safe_get_attribute(obj, attr, default=None):
    """Safely get attribute from object"""
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default

def safe_call_method(obj, method_name, *args, **kwargs):
    """Safely call method on object"""
    try:
        method = getattr(obj, method_name, None)
        if callable(method):
            return method(*args, **kwargs)
        return None
    except Exception as e:
        st.error(f"Error calling {method_name}: {e}")
        return None

# Streamlit configuration
st.set_page_config(
    page_title="KoinToss - AI Crypto Assistant",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .personality-indicator {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🪙 KoinToss AI Assistant</h1>
        <p>Your Intelligent Cryptocurrency Companion with Dual Personality AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state and CHATBOT_AVAILABLE:
        with st.spinner("🤖 Initializing KoinToss AI..."):
            try:
                st.session_state.chatbot = ImprovedDualPersonalityChatbot()
                st.success(f"✅ Chatbot initialized using {chatbot_module}")
            except Exception as e:
                st.error(f"Error initializing chatbot: {e}")
                st.session_state.chatbot = None

    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Chatbot status
        if CHATBOT_AVAILABLE and "chatbot" in st.session_state and st.session_state.chatbot:
            st.success("🤖 AI Assistant: Online")
            
            # Current personality indicator
            current_personality = safe_get_attribute(st.session_state.chatbot, 'current_personality', 'normal')
            personality_display = "🎓 Educational Mode" if current_personality == 'normal' else "⚔️ Warrior Mode"
            
            st.markdown(f"""
            <div class="personality-indicator">
                Current Mode: {personality_display}
            </div>
            """, unsafe_allow_html=True)
            
            # Personality switch buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎓 Educational", key="normal_mode"):
                    if st.session_state.chatbot:
                        response = safe_call_method(st.session_state.chatbot, 'switch_personality', 'normal')
                        if response:
                            st.success("Switched to Educational Mode")
                            st.rerun()
            
            with col2:
                if st.button("⚔️ Warrior", key="warrior_mode"):
                    if st.session_state.chatbot:
                        response = safe_call_method(st.session_state.chatbot, 'switch_personality', 'subzero')
                        if response:
                            st.success("Switched to Warrior Mode")
                            st.rerun()
            
            # Learning stats (if available)
            if hasattr(st.session_state.chatbot, 'get_learning_stats'):
                try:
                    stats = st.session_state.chatbot.get_learning_stats()
                    if stats:
                        st.write("**📊 Learning Progress**")
                        st.json(stats)
                except Exception as e:
                    st.write("**📊 Learning Progress**")
                    st.info("Learning stats will be available after training")
            else:
                st.write("**📊 Learning Progress**")
                st.info("Advanced learning features available in enhanced version")
            
        else:
            st.error("🤖 AI Assistant: Offline")
            st.write("Please check chatbot configuration")
        
        # Market data section
        st.header("💰 Market Overview")
        
        with st.spinner("Loading market data..."):
            crypto_data = get_crypto_data()
            
            if crypto_data:
                for crypto in crypto_data[:5]:  # Show top 5
                    try:
                        name = crypto.get('name', 'Unknown')
                        symbol = crypto.get('symbol', 'N/A')
                        price = crypto.get('current_price', 0)
                        change = crypto.get('price_change_percentage_24h', 0)
                        
                        change_color = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>{symbol}</strong><br>
                            ${price:.4f}<br>
                            {change_color} {change:.2f}%
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception:
                        continue
            else:
                st.info("Market data temporarily unavailable")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.header("💬 Chat with KoinToss AI")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about crypto, trading, or type 'switch' to change personality..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            if CHATBOT_AVAILABLE and "chatbot" in st.session_state and st.session_state.chatbot:
                with st.spinner("🤖 Thinking..."):
                    try:
                        response = safe_call_method(st.session_state.chatbot, 'get_response', prompt)
                        if response:
                            st.markdown(response)
                            # Add response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        else:
                            error_msg = "⚠️ I'm having trouble generating a response. Please try again or rephrase your question."
                            st.markdown(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    except Exception as e:
                        error_msg = f"⚠️ Error: {str(e)[:100]}... Please try again."
                        st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                error_msg = "🔧 Chatbot is currently unavailable. Please refresh the page or check system status."
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        🪙 <strong>KoinToss AI Assistant</strong> - Powered by Advanced Dual Personality AI<br>
        <small>Real-time crypto insights • Educational & Warrior modes • Continuous learning</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
