#!/usr/bin/env python3
"""
KoinToss FastAPI Server for App Integration
- RESTful API endpoints for chatbot functionality
- CORS enabled for cross-origin requests
- Embeddable via JavaScript widget
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import json

# Import your chatbot
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot

app = FastAPI(
    title="KoinToss Crypto Chatbot API",
    description="Embeddable crypto chatbot with dual personalities",
    version="1.0.0"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot = None

@app.on_event("startup")
async def startup_event():
    """Initialize chatbot on startup"""
    global chatbot
    chatbot = ImprovedDualPersonalityChatbot()
    print("🚀 KoinToss API Server started!")

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    personality: str
    type: str
    confidence: float
    session_id: str

class PersonalityRequest(BaseModel):
    personality: str  # "normal" or "subzero"
    session_id: Optional[str] = "default"

# API Endpoints
@app.get("/")
async def root():
    """API status endpoint"""
    return {
        "service": "KoinToss Crypto Chatbot API",
        "status": "running",
        "version": "1.0.0",
        "personalities": ["normal", "subzero"],
        "endpoints": {
            "chat": "/api/chat",
            "personality": "/api/personality",
            "status": "/api/status",
            "widget": "/widget"
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        # Get response from chatbot
        response = chatbot.get_response(request.message)
        
        return ChatResponse(
            response=response["message"],
            personality=response["personality"],
            type=response["type"],
            confidence=response.get("confidence", 0.8),
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/api/personality")
async def switch_personality(request: PersonalityRequest):
    """Switch chatbot personality"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        switch_message = chatbot.switch_personality(request.personality)
        
        return {
            "message": switch_message,
            "personality": chatbot.personality_mode,
            "session_id": request.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personality switch error: {str(e)}")

@app.get("/api/status")
async def get_status():
    """Get chatbot status and info"""
    try:
        if not chatbot:
            return {"status": "not_initialized"}
        
        system_info = chatbot.get_system_info()
        learning_stats = chatbot.get_learning_statistics()
        
        return {
            "status": "ready",
            "current_personality": chatbot.personality_mode,
            "system_info": system_info,
            "learning_stats": learning_stats,
            "conversation_count": len(chatbot.conversation_history)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/widget", response_class=HTMLResponse)
async def get_widget():
    """Get embeddable JavaScript widget"""
    widget_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>KoinToss Crypto Chatbot Widget</title>
    <style>
        .kointoss-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            font-family: 'Inter', sans-serif;
            z-index: 10000;
            display: none;
        }
        
        .kointoss-widget.open {
            display: flex;
            flex-direction: column;
        }
        
        .widget-header {
            background: linear-gradient(90deg, #87CEEB, #4682B4);
            color: white;
            padding: 15px;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .widget-title {
            font-weight: 600;
            font-size: 16px;
        }
        
        .close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        
        .chat-area {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #0E1117;
        }
        
        .message {
            margin-bottom: 12px;
            padding: 10px;
            border-radius: 10px;
            max-width: 85%;
        }
        
        .user-message {
            background: #2E3440;
            color: white;
            margin-left: auto;
        }
        
        .bot-message {
            background: #87CEEB;
            color: #0E1117;
        }
        
        .subzero-message {
            background: linear-gradient(45deg, #4682B4, #87CEEB);
            color: white;
        }
        
        .input-area {
            padding: 15px;
            background: #262730;
            border-radius: 0 0 15px 15px;
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 8px;
            background: #0E1117;
            color: white;
            outline: none;
        }
        
        .send-btn {
            padding: 10px 15px;
            background: #87CEEB;
            color: #0E1117;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .toggle-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #87CEEB, #4682B4);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(135, 206, 235, 0.3);
            z-index: 10001;
        }
    </style>
</head>
<body>
    <!-- Toggle Button -->
    <button class="toggle-btn" onclick="toggleWidget()">⚔️</button>
    
    <!-- Chat Widget -->
    <div class="kointoss-widget" id="kointossWidget">
        <div class="widget-header">
            <div class="widget-title">🤖 KoinToss Crypto Assistant</div>
            <button class="close-btn" onclick="toggleWidget()">&times;</button>
        </div>
        <div class="chat-area" id="chatArea">
            <div class="message bot-message">
                👋 Welcome to KoinToss! I'm your AI crypto assistant. Ask me about prices, analysis, or just say hi!
            </div>
        </div>
        <div class="input-area">
            <input type="text" class="chat-input" id="chatInput" placeholder="Ask about crypto..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let currentPersonality = 'normal';
        
        function toggleWidget() {
            const widget = document.getElementById('kointossWidget');
            const toggleBtn = document.querySelector('.toggle-btn');
            
            if (widget.classList.contains('open')) {
                widget.classList.remove('open');
                toggleBtn.style.display = 'block';
            } else {
                widget.classList.add('open');
                toggleBtn.style.display = 'none';
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            try {
                // Send to API
                const response = await fetch(`${API_BASE}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: 'widget_session'
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentPersonality = data.personality;
                    addMessage(data.response, 'bot', data.personality);
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            } catch (error) {
                addMessage('Connection error. Please check your internet connection.', 'bot');
            }
        }
        
        function addMessage(text, sender, personality = 'normal') {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            
            if (sender === 'user') {
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `<strong>👤 You:</strong> ${text}`;
            } else {
                const icon = personality === 'subzero' ? '🧊' : '🤖';
                const name = personality === 'subzero' ? 'Sub-Zero AI' : 'Krypt AI';
                const className = personality === 'subzero' ? 'message bot-message subzero-message' : 'message bot-message';
                
                messageDiv.className = className;
                messageDiv.innerHTML = `<strong>${icon} ${name}:</strong> ${text}`;
            }
            
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // Initialize widget
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 KoinToss Widget loaded!');
        });
    </script>
</body>
</html>
    '''
    return widget_html

if __name__ == "__main__":
    uvicorn.run(
        "kointoss_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
