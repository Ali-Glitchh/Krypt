#!/usr/bin/env python3
"""
Fixed Streamlit App - Resolves the 'dict' object has no attribute 'strip' error
"""

import streamlit as st
from datetime import datetime

# Import chatbot with error handling
try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    CHATBOT_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing chatbot: {e}")
    CHATBOT_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="KoinToss - Fixed Crypto Assistant",
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

chatbot = initialize_chatbot()

# Enhanced styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
}

.chat-message {
    padding: 10px;
    margin: 5px 0;
    border-radius: 10px;
    border-left: 3px solid #4ecdc4;
}

.user-message {
    background-color: #0e1117;
    border-left-color: #4ecdc4;
}

.bot-message {
    background-color: #1e1e1e;
    border-left-color: #87CEEB;
}

.subzero-message {
    background-color: #1a1a2e;
    border-left-color: #00ccff;
}

.error-message {
    background-color: #2d1818;
    border-left-color: #ff6b6b;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1>⚔️ KoinToss - Fixed Crypto Assistant</h1>
    <p style="color: #87CEEB;">Dual-personality AI chatbot for cryptocurrency insights</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.personality_mode = 'normal'

# Sidebar for personality control
st.sidebar.markdown("### 🤖 AI Personality")

# Personality toggle
personality_toggle = st.sidebar.toggle(
    "🧊 Sub-Zero Mode", 
    value=(st.session_state.personality_mode == 'subzero'),
    help="Toggle between Normal and Sub-Zero personalities"
)

# Handle personality change
if personality_toggle and st.session_state.personality_mode != 'subzero':
    st.session_state.personality_mode = 'subzero'
    if chatbot:
        try:
            chatbot.switch_personality('subzero')
            st.sidebar.success("🧊 Sub-Zero activated!")
        except Exception as e:
            st.sidebar.error(f"Error activating Sub-Zero: {e}")
            
elif not personality_toggle and st.session_state.personality_mode != 'normal':
    st.session_state.personality_mode = 'normal'
    if chatbot:
        try:
            chatbot.switch_personality('normal')
            st.sidebar.success("💬 Normal mode activated!")
        except Exception as e:
            st.sidebar.error(f"Error activating Normal mode: {e}")

# Display current personality
current_personality = "🧊 Sub-Zero" if st.session_state.personality_mode == 'subzero' else "💬 Normal"
st.sidebar.markdown(f"**Current:** {current_personality}")

# Main chat interface
st.markdown("### 💬 Chat Interface")

# Chat input
user_input = st.text_input(
    "Ask me anything about cryptocurrency:",
    placeholder="Try: 'hi', 'what is bitcoin', 'switch to subzero'",
    key="chat_input"
)

# Process user input
if user_input:
    if not chatbot:
        st.error("🚫 Chatbot is not available. Please check the system.")
    else:
        try:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'message': user_input,
                'timestamp': datetime.now()
            })
            
            # Get AI response
            with st.spinner("🤖 Processing your request..."):
                ai_response = chatbot.get_response(user_input)
            
            # CRITICAL FIX: Properly handle both dict and string responses
            if isinstance(ai_response, dict):
                # Extract message from dictionary
                response_message = ai_response.get('message', '')
                if not response_message:
                    response_message = str(ai_response)
                response_type = ai_response.get('type', 'unknown')
                response_personality = ai_response.get('personality', st.session_state.personality_mode)
            elif isinstance(ai_response, str):
                # Handle string response
                response_message = ai_response
                response_type = 'string_response'
                response_personality = st.session_state.personality_mode
            else:
                # Handle unexpected response type
                response_message = f"Received unexpected response type: {type(ai_response)}"
                response_type = 'error'
                response_personality = st.session_state.personality_mode
            
            # Ensure we have a valid message (prevent empty responses)
            if not response_message or (isinstance(response_message, str) and response_message.strip() == ''):
                response_message = "Sorry, I couldn't generate a proper response. Please try again."
                response_type = 'error'
            
            # Add AI response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'message': response_message,
                'type': response_type,
                'personality': response_personality,
                'timestamp': datetime.now()
            })
            
            # Handle special response types
            if response_type == 'personality_switch':
                st.success(f"✅ Personality switched to {response_personality}!")
                
        except Exception as e:
            # Add error message to chat history
            error_message = f"Error processing request: {str(e)}"
            st.session_state.chat_history.append({
                'role': 'assistant',
                'message': error_message,
                'type': 'error',
                'personality': st.session_state.personality_mode,
                'timestamp': datetime.now()
            })
            st.error(f"🚫 Error: {e}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    
    # Show recent messages (last 10)
    recent_messages = st.session_state.chat_history[-10:]
    
    for message in recent_messages:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {message['message']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Determine bot name and styling
            personality = message.get('personality', 'normal')
            msg_type = message.get('type', 'normal')
            
            if personality == 'subzero':
                bot_name = "🧊 Sub-Zero AI"
                message_class = "subzero-message"
            else:
                bot_name = "🤖 Krypt AI"
                message_class = "bot-message"
            
            if msg_type == 'error':
                message_class = "error-message"
            
            st.markdown(f"""
            <div class="chat-message {message_class}">
                <strong>{bot_name}:</strong> {message['message']}
            </div>
            """, unsafe_allow_html=True)

# Clear chat button
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# System status
st.markdown("---")
st.markdown("### 📊 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    if chatbot:
        st.success("🟢 Chatbot Online")
    else:
        st.error("🔴 Chatbot Offline")

with col2:
    personality_status = f"🧊 Sub-Zero Mode" if st.session_state.personality_mode == 'subzero' else "💬 Normal Mode"
    st.info(f"🎭 {personality_status}")

with col3:
    total_messages = len(st.session_state.chat_history)
    st.info(f"💬 {total_messages} Messages")

# Testing section
st.markdown("---")
st.markdown("### 🧪 Test the Fix")

if st.button("🔬 Run Quick Test"):
    if chatbot:
        st.markdown("**Testing various message types...**")
        
        test_messages = ["hi", "what is bitcoin", "switch to subzero"]
        
        for test_msg in test_messages:
            with st.expander(f"Test: '{test_msg}'"):
                try:
                    response = chatbot.get_response(test_msg)
                    st.write(f"**Response Type:** {type(response)}")
                    
                    if isinstance(response, dict):
                        st.write("**Dictionary Response:**")
                        st.json(response)
                        
                        # Test safe string extraction
                        message = response.get('message', '')
                        if isinstance(message, str):
                            safe_message = message.strip()
                            st.write(f"**Safe String Extraction:** '{safe_message[:100]}...'")
                        else:
                            st.write(f"**Warning:** Message is not a string: {type(message)}")
                    else:
                        st.write(f"**Direct Response:** {response}")
                        
                except Exception as e:
                    st.error(f"Test failed: {e}")
    else:
        st.error("Chatbot not available for testing")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #87CEEB;">
    <p><strong>⚔️ KoinToss Fixed Version</strong> - Resolving the strip() error</p>
    <p style="font-size: 0.8rem;">This version properly handles dictionary responses from the chatbot</p>
</div>
""", unsafe_allow_html=True)
