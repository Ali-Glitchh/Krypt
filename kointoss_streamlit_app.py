import streamlit as st
import time
from datetime import datetime
import json

# Import chatbot with error handling
try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    CHATBOT_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing chatbot: {e}")
    CHATBOT_AVAILABLE = False

# Page config with KoinToss branding
st.set_page_config(
    page_title="KoinToss - Enhanced Crypto Assistant",
    page_icon="⚔️",
    layout="wide",
)

# Initialize chatbot
@st.cache_resource
def initialize_chatbot():
    if CHATBOT_AVAILABLE:
        return ImprovedDualPersonalityChatbot()
    else:
        return None

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
        padding: 30px;
        background: radial-gradient(circle, rgba(135, 206, 250, 0.15) 0%, transparent 70%);
        border-radius: 25px;
        border: 2px solid rgba(135, 206, 250, 0.3);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(135, 206, 250, 0.1);
    }
    
    .axe-symbol {
        font-size: 5rem;
        color: #87CEEB;
        text-shadow: 0 0 30px rgba(135, 206, 250, 0.8);
        animation: axeRotate 4s ease-in-out infinite;
        display: inline-block;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 20px rgba(135, 206, 250, 0.6));
    }
    
    .brand-name {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(135, 206, 250, 0.5);
        margin: 15px 0;
        letter-spacing: 3px;
        background: linear-gradient(45deg, #ffffff, #87CEEB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .brand-tagline {
        font-size: 1.1rem;
        color: #87CEEB;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 4px;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    /* Animations */
    @keyframes logoGlow {
        0% { 
            transform: scale(1); 
            box-shadow: 0 0 30px rgba(135, 206, 250, 0.3);
        }
        100% { 
            transform: scale(1.02); 
            box-shadow: 0 0 50px rgba(135, 206, 250, 0.6);
        }
    }
    
    @keyframes axeRotate {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(-8deg) scale(1.05); }
        50% { transform: rotate(0deg) scale(1); }
        75% { transform: rotate(8deg) scale(1.05); }
        100% { transform: rotate(0deg) scale(1); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 4px solid rgba(135, 206, 250, 0.3);
        border-radius: 50%;
        border-top-color: #87CEEB;
        animation: spin 1s ease-in-out infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Enhanced Chat Interface */
    .chat-container {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(135, 206, 250, 0.3);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .user-message {
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 15px 0;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 4px 20px rgba(135, 206, 250, 0.4);
        font-weight: 500;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(135, 206, 250, 0.4);
        color: #ffffff;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        max-width: 85%;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .subzero-message {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        border: 1px solid rgba(135, 206, 250, 0.6);
        box-shadow: 0 4px 20px rgba(30, 60, 114, 0.4);
    }
    
    /* Enhanced Status Cards */
    .status-card {
        background: rgba(26, 26, 46, 0.9);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(135, 206, 250, 0.3);
        text-align: center;
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .status-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(135, 206, 250, 0.3);
    }
    
    .status-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #87CEEB;
        text-shadow: 0 0 15px rgba(135, 206, 250, 0.5);
        margin: 10px 0;
    }
    
    .status-label {
        font-size: 1rem;
        color: #ffffff;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 15px 30px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(135, 206, 250, 0.3);
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(135, 206, 250, 0.5);
        background: linear-gradient(45deg, #4682B4, #87CEEB);
    }
    
    /* Enhanced Text Input */
    .stTextInput > div > div > input {
        background: rgba(26, 26, 46, 0.9);
        border: 2px solid rgba(135, 206, 250, 0.3);
        border-radius: 30px;
        color: white;
        padding: 15px 25px;
        font-size: 1.1rem;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #87CEEB;
        box-shadow: 0 0 20px rgba(135, 206, 250, 0.4);
    }
    
    /* Status Indicators */
    .status-online {
        color: #00ff88;
        animation: pulse 2s infinite;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff4444;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffaa00;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: rgba(10, 10, 10, 0.95);
        border-right: 2px solid rgba(135, 206, 250, 0.3);
        backdrop-filter: blur(15px);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        color: #87CEEB;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(135, 206, 250, 0.3);
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

def show_loading_animation(message="Processing your request..."):
    """Display loading animation with KoinToss branding"""
    return st.markdown(f"""
    <div style="text-align: center; padding: 30px;">
        <div class="loading-spinner"></div>
        <p style="color: #87CEEB; margin-top: 15px; font-weight: 500; font-size: 1.1rem;">{message}</p>
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

def main():
    """Main application with enhanced KoinToss interface"""
    
    # Apply KoinToss branding
    add_kointoss_branding()
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    # Main content area
    st.markdown('<div class="section-header">💬 Chat with KoinToss AI</div>', unsafe_allow_html=True)
    
    # Chat interface
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input(
            "", 
            placeholder="Ask me about 'pi coin', 'bitcoin price', 'ethereum info', or any crypto question...",
            key="chat_input",
            label_visibility="collapsed"
        )
        
        if user_input:
            # Show loading animation
            loading_placeholder = st.empty()
            with loading_placeholder:
                show_loading_animation("KoinToss AI is thinking...")
            
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced status display
    st.markdown('<div class="section-header">📊 System Status</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        if chatbot:
            st.markdown('<div class="status-value">🟢</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">Chatbot Online</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-value">🔴</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">Chatbot Offline</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        if CHATBOT_AVAILABLE:
            st.markdown('<div class="status-value">🤖</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">AI Ready</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-value">⚠️</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">AI Loading</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        if chatbot and hasattr(chatbot, 'autonomous_trainer'):
            training_status = "🟢" if getattr(chatbot, 'auto_training_enabled', False) else "🟡"
            status_text = "Auto Training" if getattr(chatbot, 'auto_training_enabled', False) else "Manual Mode"
            st.markdown(f'<div class="status-value">{training_status}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="status-label">{status_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-value">⏸️</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">Training Idle</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        # Check conversation count
        if chatbot and hasattr(chatbot, 'get_learning_stats'):
            try:
                stats = chatbot.get_learning_stats()
                conv_count = stats.get('total_conversations', 0)
                st.markdown(f'<div class="status-value">{conv_count}</div>', unsafe_allow_html=True)
                st.markdown('<div class="status-label">Conversations</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="status-value">-</div>', unsafe_allow_html=True)
                st.markdown('<div class="status-label">Conversations</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-value">0</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-label">Conversations</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with enhanced features
    with st.sidebar:
        st.markdown('<div class="section-header">⚔️ KoinToss Control</div>', unsafe_allow_html=True)
        
        # Personality toggle
        st.markdown("### 🤖 AI Personality")
        personality_mode = st.selectbox(
            "Choose AI Personality:",
            ["🤖 Krypt AI (Normal)", "🧊 Sub-Zero (Warrior)"],
            key="personality_select"
        )
        
        if personality_mode.startswith("🧊") and chatbot:
            try:
                chatbot.switch_personality('subzero')
                st.success("🧊 Sub-Zero mode activated!")
            except Exception as e:
                st.error(f"Error switching to Sub-Zero: {e}")
        elif chatbot:
            try:
                chatbot.switch_personality('normal')
                st.success("🤖 Krypt AI mode activated!")
            except Exception as e:
                st.error(f"Error switching to Krypt AI: {e}")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Reset Conversation"):
            st.session_state.clear()
            st.success("Conversation reset!")
            st.rerun()
        
        if st.button("📊 View Learning Stats") and chatbot:
            try:
                stats = chatbot.get_learning_stats()
                st.json(stats)
            except Exception as e:
                st.error(f"Error getting stats: {e}")
        
        if st.button("🚀 Manual Training") and chatbot:
            try:
                with st.spinner("Running training session..."):
                    chatbot.autonomous_trainer.run_single_training_iteration()
                st.success("Training completed!")
            except Exception as e:
                st.error(f"Training failed: {e}")
    
    # Enhanced footer with KoinToss branding
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 30px; color: #87CEEB;">
        <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 10px;">
            ⚔️ <strong>KoinToss</strong> - Making Cryptocurrency Simple
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 15px;">
            Powered by Enhanced AI • Real-time Data • Autonomous Learning
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.8rem; opacity: 0.7;">
            <span>🤖 Dual Personality AI</span>
            <span>•</span>
            <span>📊 Live Crypto Data</span>
            <span>•</span>
            <span>🧠 Continuous Learning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
