"""
KoinToss Streamlit App - iframe Optimized
Designed for seamless embedding in mobile and web applications
"""

import streamlit as st
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Configure page for iframe embedding
st.set_page_config(
    page_title="KoinToss AI Assistant",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar for iframe
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for iframe optimization
st.markdown("""
<style>
/* Hide Streamlit branding and menu for iframe */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Optimize for mobile iframe */
.stApp {
    padding: 0px;
    margin: 0px;
}

.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* Mobile responsive chat interface */
.stChatMessage {
    margin-bottom: 0.5rem;
}

.stChatInput {
    position: sticky;
    bottom: 0;
    background: white;
    padding: 0.5rem;
    border-top: 1px solid #e0e0e0;
}

/* Custom styling for iframe */
.chat-container {
    height: 70vh;
    overflow-y: auto;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 10px;
}

.personality-switch {
    text-align: center;
    padding: 10px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 10px;
    font-weight: bold;
}

.crypto-price {
    background: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    display: inline-block;
    margin: 2px;
    font-size: 0.8rem;
}

/* Hide Streamlit elements for clean iframe */
.stDeployButton {display: none;}
.stDecoration {display: none;}
.stToolbar {display: none;}
</style>
""", unsafe_allow_html=True)

def load_chatbot():
    """Load the chatbot safely"""
    try:
        # Try importing the main chatbot
        from improved_dual_personality_chatbot_fixed import ImprovedDualPersonalityChatbot
        return ImprovedDualPersonalityChatbot()
    except ImportError:
        try:
            # Fallback to alternative chatbot
            from crypto_chatbot_fixed import ImprovedDualPersonalityChatbot
            return ImprovedDualPersonalityChatbot()
        except ImportError:
            st.error("⚠️ Chatbot temporarily unavailable. Please try again later.")
            return None

def main():
    """Main iframe-optimized KoinToss app"""
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        with st.spinner("🔄 Initializing KoinToss AI..."):
            st.session_state.chatbot = load_chatbot()
    
    # Header optimized for iframe
    st.markdown("""
    <div class="personality-switch">
        🪙 KoinToss AI Assistant - Your Crypto Companion
    </div>
    """, unsafe_allow_html=True)
    
    # Quick info panel
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="crypto-price">BTC: $43,500</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="crypto-price">ETH: $2,650</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="crypto-price">Market: 📈</div>', unsafe_allow_html=True)
    
    # Chat interface in container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input at bottom
        if prompt := st.chat_input("Ask me about crypto, trading, or switch personality..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            if st.session_state.chatbot:
                with st.chat_message("assistant"):
                    with st.spinner("🤖 Thinking..."):
                        try:
                            response = st.session_state.chatbot.get_response(prompt)
                            st.markdown(response)
                            
                            # Add bot response to history
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                        except Exception as e:
                            error_msg = "⚠️ Sorry, I'm having technical difficulties. Please try again!"
                            st.markdown(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                st.error("🔧 Bot is currently being updated. Please refresh the page.")
    
    # Personality switch buttons (mobile-friendly)
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎓 Switch to Educational Mode", use_container_width=True):
            if st.session_state.chatbot:
                response = st.session_state.chatbot.switch_personality("normal")
                st.success(f"✅ {response}")
                st.rerun()
    
    with col2:
        if st.button("⚔️ Switch to Warrior Mode", use_container_width=True):
            if st.session_state.chatbot:
                response = st.session_state.chatbot.switch_personality("subzero")
                st.success(f"✅ {response}")
                st.rerun()
    
    # Footer info for iframe
    st.markdown("""
    <div style="text-align: center; padding: 10px; font-size: 0.8rem; color: #666;">
        🪙 Powered by KoinToss AI | Real-time Crypto Intelligence
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
