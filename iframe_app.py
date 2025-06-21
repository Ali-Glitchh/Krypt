import streamlit as st
import pandas as pd
import time
from datetime import datetime
import re
from enhanced_crypto_chatbot import EnhancedCryptoChatbot

# Configure the page for iframe embedding
st.set_page_config(
    page_title="Krypt AI Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar for iframe
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Initialize enhanced chatbot
@st.cache_resource
def initialize_chatbot():
    return EnhancedCryptoChatbot()

chatbot = initialize_chatbot()

# CSS for iframe-friendly styling
st.markdown("""
<style>
/* Hide Streamlit's default elements for iframe */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

/* Responsive design for mobile/web embedding */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Chat container styling */
.chat-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.user-message {
    background: #4ecdc4;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 10px;
    margin-left: 20%;
    text-align: right;
}

.bot-message {
    background: white;
    color: #333;
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 10px;
    margin-right: 20%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.subzero-message {
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 10px;
    margin-right: 20%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.price-data {
    background: #f8f9fa;
    border-left: 4px solid #4ecdc4;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
}

.insight-data {
    background: #e8f4f8;
    border-left: 4px solid #2196F3;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .user-message, .bot-message, .subzero-message {
        margin-left: 5%;
        margin-right: 5%;
    }
}

/* Personality indicator */
.personality-indicator {
    position: fixed;
    top: 10px;
    right: 10px;
    background: rgba(255, 255, 255, 0.9);
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 12px;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'bot_initialized' not in st.session_state:
    st.session_state.bot_initialized = True
    # Add welcome message
    welcome_response = chatbot.generate_response("hello")
    st.session_state.chat_history.append({
        'user': '',
        'bot': welcome_response['message'],
        'type': welcome_response['type'],
        'timestamp': datetime.now()
    })

# Personality indicator
personality_emoji = "🧊" if chatbot.personality_mode == "subzero" else "🤖"
st.markdown(f"""
<div class="personality-indicator">
    {personality_emoji} {chatbot.personality_mode.title()} Mode
</div>
""", unsafe_allow_html=True)

# Main chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Title
if chatbot.personality_mode == "subzero":
    st.markdown("## 🧊 Sub-Zero Crypto Assistant ❄️")
else:
    st.markdown("## 🤖 Krypt AI Assistant")

# Chat history display
chat_placeholder = st.container()

with chat_placeholder:
    for chat in st.session_state.chat_history:
        if chat['user']:
            st.markdown(f'<div class="user-message">👤 {chat["user"]}</div>', unsafe_allow_html=True)
        
        # Bot response styling based on personality
        message_class = "subzero-message" if chatbot.personality_mode == "subzero" else "bot-message"
        bot_emoji = "🧊" if chatbot.personality_mode == "subzero" else "🤖"
        
        if chat['type'] == 'price_query':
            st.markdown(f'<div class="{message_class}">{bot_emoji} {chat["bot"]}</div>', unsafe_allow_html=True)
        elif chat['type'] == 'article_insight':
            st.markdown(f'<div class="insight-data">{bot_emoji} {chat["bot"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="{message_class}">{bot_emoji} {chat["bot"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Ask me anything about crypto...", 
        placeholder="e.g., 'What's the price of Bitcoin?', 'Tell me about DeFi', 'Sub-Zero mode'",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", type="primary")

# Process user input
if (send_button and user_input) or (user_input and user_input != st.session_state.get('last_input', '')):
    if user_input.strip():
        # Update last input to prevent duplicates
        st.session_state.last_input = user_input
        
        # Get bot response
        with st.spinner("Thinking..."):
            response = chatbot.generate_response(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'user': user_input,
            'bot': response['message'],
            'type': response['type'],
            'timestamp': datetime.now()
        })
        
        # Clear input and rerun to show new message
        st.rerun()

# Quick action buttons
st.markdown("### Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Bitcoin Price"):
        response = chatbot.generate_response("what is the price of bitcoin")
        st.session_state.chat_history.append({
            'user': "Bitcoin price",
            'bot': response['message'],
            'type': response['type'],
            'timestamp': datetime.now()
        })
        st.rerun()

with col2:
    if st.button("📰 Crypto News"):
        response = chatbot.generate_response("latest crypto news")
        st.session_state.chat_history.append({
            'user': "Latest crypto news",
            'bot': response['message'],
            'type': response['type'],
            'timestamp': datetime.now()
        })
        st.rerun()

with col3:
    if st.button("📚 DeFi Insights"):
        response = chatbot.generate_response("tell me about DeFi from your analysis")
        st.session_state.chat_history.append({
            'user': "DeFi insights",
            'bot': response['message'],
            'type': response['type'],
            'timestamp': datetime.now()
        })
        st.rerun()

with col4:
    mode_label = "🤖 Normal" if chatbot.personality_mode == "subzero" else "🧊 Sub-Zero"
    if st.button(f"Switch to {mode_label}"):
        response = chatbot.generate_response("switch personality")
        st.session_state.chat_history.append({
            'user': f"Switch to {mode_label}",
            'bot': response['message'],
            'type': response['type'],
            'timestamp': datetime.now()
        })
        st.rerun()

# API for iframe integration
st.markdown("---")
with st.expander("🔗 Iframe Integration Code"):
    iframe_code = f"""
<!-- Krypt AI Assistant Iframe -->
<iframe 
    src="{st.secrets.get('iframe_url', 'http://localhost:8501')}" 
    width="100%" 
    height="600" 
    frameborder="0"
    style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
</iframe>

<!-- For mobile apps, you can also use: -->
<div style="width: 100%; height: 80vh;">
    <iframe 
        src="{st.secrets.get('iframe_url', 'http://localhost:8501')}" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border-radius: 10px;">
    </iframe>
</div>
"""
    st.code(iframe_code, language="html")

# Footer for iframe
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
    Powered by Krypt AI | Real-time crypto data & insights
</div>
""", unsafe_allow_html=True)
