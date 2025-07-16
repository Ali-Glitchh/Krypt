#!/usr/bin/env python3
"""
Enhanced KoinToss FastAPI Server for Production App Integration
- Production-ready with session management
- Enhanced error handling and validation
- WebSocket support for real-time chat
- Rate limiting and security features
- Comprehensive API endpoints
"""

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# FastAPI and related imports
try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel, ValidationError
    import uvicorn
except ImportError as e:
    print(f"❌ Missing FastAPI dependencies. Please install: pip install fastapi uvicorn pydantic")
    print(f"Error: {e}")
    exit(1)

# Import chatbot
try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    from advanced_autonomous_trainer import AdvancedAutonomousTrainer
except ImportError as e:
    print(f"❌ Could not import chatbot modules: {e}")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app with metadata
app = FastAPI(
    title="KoinToss Crypto Chatbot API",
    description="Production-ready embeddable crypto chatbot with dual personalities",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer(auto_error=False)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
chatbot = None
autonomous_trainer = None

# Session management
class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.cleanup_interval = 3600  # 1 hour

    def create_session(self, session_id: str = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "conversation_history": [],
            "personality": "normal",
            "message_count": 0
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        session = self.sessions.get(session_id)
        if session:
            session["last_activity"] = datetime.now()
        return session

    def update_session(self, session_id: str, data: Dict):
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            self.sessions[session_id]["last_activity"] = datetime.now()

    def cleanup_expired_sessions(self):
        """Remove sessions older than 1 hour"""
        cutoff = datetime.now() - timedelta(seconds=self.cleanup_interval)
        expired = [sid for sid, session in self.sessions.items() 
                  if session["last_activity"] < cutoff]
        for sid in expired:
            del self.sessions[sid]
        logger.info(f"Cleaned up {len(expired)} expired sessions")

session_manager = SessionManager()

# Rate limiting
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}
        self.limit = 30  # requests per minute
        self.window = 60  # seconds

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [req_time for req_time in self.requests[client_id] 
                                   if now - req_time < self.window]
        
        # Check if under limit
        if len(self.requests[client_id]) < self.limit:
            self.requests[client_id].append(now)
            return True
        return False

rate_limiter = RateLimiter()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    personality: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    personality: str
    type: str
    confidence: float
    session_id: str
    timestamp: str
    message_id: str

class PersonalityRequest(BaseModel):
    personality: str
    session_id: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    message_count: int
    current_personality: str

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize chatbot and services on startup"""
    global chatbot, autonomous_trainer
    
    try:
        logger.info("🚀 Starting KoinToss API Server...")
        
        # Initialize chatbot
        chatbot = ImprovedDualPersonalityChatbot()
        logger.info("✅ Chatbot initialized")
        
        # Initialize autonomous trainer
        autonomous_trainer = AdvancedAutonomousTrainer(chatbot)
        autonomous_trainer.start_autonomous_training()
        logger.info("✅ Autonomous training started")
        
        logger.info("🎉 KoinToss API Server ready!")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global autonomous_trainer
    
    logger.info("🛑 Shutting down KoinToss API Server...")
    
    if autonomous_trainer:
        autonomous_trainer.stop_autonomous_training()
        autonomous_trainer.export_training_data()
        logger.info("✅ Training data exported")

# Dependency functions
async def get_current_session(request: ChatRequest) -> str:
    """Get or create session"""
    session_id = request.session_id
    if not session_id or not session_manager.get_session(session_id):
        session_id = session_manager.create_session()
    return session_id

def check_rate_limit(client_id: str = "default"):
    """Check rate limiting"""
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    return True

# API Endpoints
@app.get("/")
async def root():
    """API status and information"""
    return {
        "service": "KoinToss Crypto Chatbot API",
        "status": "running",
        "version": "2.0.0",
        "features": {
            "dual_personality": True,
            "autonomous_training": True,
            "websocket_support": True,
            "session_management": True,
            "rate_limiting": True
        },
        "endpoints": {
            "chat": "/api/chat",
            "websocket": "/ws",
            "personality": "/api/personality",
            "session": "/api/session",
            "status": "/api/status",
            "training": "/api/training",
            "widget": "/widget"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    _: bool = Depends(check_rate_limit)
):
    """Enhanced chat endpoint with session management"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        # Get or create session
        session_id = await get_current_session(request)
        session = session_manager.get_session(session_id)
        
        # Switch personality if requested
        if request.personality and request.personality != session["personality"]:
            chatbot.switch_personality(request.personality)
            session["personality"] = request.personality
        
        # Get response from chatbot
        response = chatbot.get_response(request.message)
        
        # Create response
        message_id = str(uuid.uuid4())
        chat_response = ChatResponse(
            response=response["message"],
            personality=response["personality"],
            type=response["type"],
            confidence=response.get("confidence", 0.8),
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            message_id=message_id
        )
        
        # Update session
        session["message_count"] += 1
        session["conversation_history"].append({
            "user_message": request.message,
            "bot_response": response["message"],
            "timestamp": datetime.now().isoformat(),
            "message_id": message_id
        })
        session_manager.update_session(session_id, session)
        
        # Background task to clean up old sessions
        background_tasks.add_task(session_manager.cleanup_expired_sessions)
        
        return chat_response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    
    # Create or get session
    if not session_manager.get_session(session_id):
        session_manager.create_session(session_id)
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected to KoinToss chatbot",
            "session_id": session_id
        }))
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            if not user_message:
                continue
            
            # Get chatbot response
            response = chatbot.get_response(user_message)
            
            # Send response
            await websocket.send_text(json.dumps({
                "type": "chat_response",
                "response": response["message"],
                "personality": response["personality"],
                "confidence": response.get("confidence", 0.8),
                "timestamp": datetime.now().isoformat()
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.post("/api/personality")
async def switch_personality(request: PersonalityRequest):
    """Switch chatbot personality"""
    try:
        if not chatbot:
            raise HTTPException(status_code=503, detail="Chatbot not initialized")
        
        if request.personality not in ["normal", "subzero"]:
            raise HTTPException(status_code=400, detail="Invalid personality. Use 'normal' or 'subzero'")
        
        switch_message = chatbot.switch_personality(request.personality)
        
        # Update session if provided
        if request.session_id:
            session = session_manager.get_session(request.session_id)
            if session:
                session["personality"] = request.personality
                session_manager.update_session(request.session_id, session)
        
        return {
            "message": switch_message,
            "personality": chatbot.personality_mode,
            "session_id": request.session_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Personality switch error: {e}")
        raise HTTPException(status_code=500, detail=f"Personality switch error: {str(e)}")

@app.get("/api/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """Get session information"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionInfo(
        session_id=session_id,
        created_at=session["created_at"].isoformat(),
        message_count=session["message_count"],
        current_personality=session["personality"]
    )

@app.get("/api/status")
async def get_status():
    """Get comprehensive system status"""
    try:
        status_data = {
            "status": "ready" if chatbot else "not_initialized",
            "timestamp": datetime.now().isoformat(),
            "active_sessions": len(session_manager.sessions),
            "websocket_connections": len(manager.active_connections)
        }
        
        if chatbot:
            status_data.update({
                "current_personality": chatbot.personality_mode,
                "system_info": chatbot.get_system_info(),
                "learning_stats": chatbot.get_learning_statistics(),
                "conversation_count": len(chatbot.conversation_history)
            })
        
        if autonomous_trainer:
            status_data["training_stats"] = autonomous_trainer.get_training_statistics()
        
        return status_data
        
    except Exception as e:
        logger.error(f"Status error: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/api/training")
async def get_training_status():
    """Get autonomous training status"""
    if not autonomous_trainer:
        raise HTTPException(status_code=503, detail="Autonomous trainer not initialized")
    
    return autonomous_trainer.get_training_statistics()

@app.post("/api/training/export")
async def export_training_data():
    """Export training data"""
    if not autonomous_trainer:
        raise HTTPException(status_code=503, detail="Autonomous trainer not initialized")
    
    filename = autonomous_trainer.export_training_data()
    return {"message": "Training data exported", "filename": filename}

@app.get("/widget", response_class=HTMLResponse)
async def get_enhanced_widget():
    """Get enhanced embeddable JavaScript widget"""
    widget_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KoinToss Crypto Chatbot Widget</title>
    <style>
        .kointoss-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: min(350px, 90vw);
            height: min(500px, 80vh);
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            z-index: 10000;
            display: none;
            flex-direction: column;
            transition: all 0.3s ease;
        }
        
        .kointoss-widget.open {
            display: flex;
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
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ff00;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            padding: 5px;
            border-radius: 3px;
            transition: background 0.2s;
        }
        
        .close-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .chat-area {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #0E1117;
            scrollbar-width: thin;
            scrollbar-color: #4682B4 #0E1117;
        }
        
        .chat-area::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-area::-webkit-scrollbar-track {
            background: #0E1117;
        }
        
        .chat-area::-webkit-scrollbar-thumb {
            background: #4682B4;
            border-radius: 3px;
        }
        
        .message {
            margin-bottom: 12px;
            padding: 10px 12px;
            border-radius: 12px;
            max-width: 85%;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background: #2E3440;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }
        
        .bot-message {
            background: #87CEEB;
            color: #0E1117;
            border-bottom-left-radius: 4px;
        }
        
        .subzero-message {
            background: linear-gradient(45deg, #4682B4, #87CEEB);
            color: white;
            border-bottom-left-radius: 4px;
        }
        
        .message-time {
            font-size: 11px;
            opacity: 0.6;
            margin-top: 4px;
        }
        
        .typing-indicator {
            display: none;
            padding: 10px 12px;
            background: #87CEEB;
            border-radius: 12px;
            max-width: 85%;
            margin-bottom: 12px;
        }
        
        .typing-dots {
            display: flex;
            gap: 3px;
        }
        
        .typing-dots span {
            width: 6px;
            height: 6px;
            background: #0E1117;
            border-radius: 50%;
            animation: typingDots 1.4s infinite;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingDots {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        .input-area {
            padding: 15px;
            background: #262730;
            border-radius: 0 0 15px 15px;
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #4682B4;
            border-radius: 8px;
            background: #0E1117;
            color: white;
            outline: none;
            resize: none;
            font-family: inherit;
            max-height: 100px;
            transition: border-color 0.2s;
        }
        
        .chat-input:focus {
            border-color: #87CEEB;
        }
        
        .send-btn {
            padding: 12px 16px;
            background: #87CEEB;
            color: #0E1117;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
            min-width: 50px;
        }
        
        .send-btn:hover:not(:disabled) {
            background: #4682B4;
            color: white;
        }
        
        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
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
            transition: all 0.3s ease;
        }
        
        .toggle-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4);
        }
        
        .personality-switch {
            display: flex;
            gap: 5px;
            margin-bottom: 10px;
        }
        
        .personality-btn {
            padding: 5px 10px;
            background: transparent;
            border: 1px solid #4682B4;
            border-radius: 15px;
            color: #87CEEB;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .personality-btn.active {
            background: #4682B4;
            color: white;
        }
        
        @media (max-width: 480px) {
            .kointoss-widget {
                bottom: 10px;
                right: 10px;
                left: 10px;
                width: auto;
                height: 70vh;
            }
            
            .toggle-btn {
                bottom: 10px;
                right: 10px;
            }
        }
    </style>
</head>
<body>
    <!-- Toggle Button -->
    <button class="toggle-btn" onclick="toggleWidget()" title="Chat with KoinToss">⚔️</button>
    
    <!-- Chat Widget -->
    <div class="kointoss-widget" id="kointossWidget">
        <div class="widget-header">
            <div class="widget-title">
                <span class="status-indicator"></span>
                🤖 KoinToss AI
            </div>
            <button class="close-btn" onclick="toggleWidget()" title="Close">&times;</button>
        </div>
        <div class="chat-area" id="chatArea">
            <div class="personality-switch">
                <button class="personality-btn active" onclick="switchPersonality('normal')">🤖 Normal</button>
                <button class="personality-btn" onclick="switchPersonality('subzero')">🧊 Sub-Zero</button>
            </div>
            <div class="message bot-message">
                <strong>🤖 Krypt AI:</strong> Welcome to KoinToss! I'm your AI crypto assistant with dual personalities. Ask me about prices, analysis, or just say hi!
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
        </div>
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div class="input-area">
            <textarea class="chat-input" id="chatInput" placeholder="Ask about crypto..." onkeydown="handleKeyDown(event)" rows="1"></textarea>
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let currentPersonality = 'normal';
        let sessionId = null;
        let isConnected = false;
        
        // Auto-resize textarea
        const chatInput = document.getElementById('chatInput');
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        function toggleWidget() {
            const widget = document.getElementById('kointossWidget');
            const toggleBtn = document.querySelector('.toggle-btn');
            
            if (widget.classList.contains('open')) {
                widget.classList.remove('open');
                toggleBtn.style.display = 'block';
            } else {
                widget.classList.add('open');
                toggleBtn.style.display = 'none';
                chatInput.focus();
                if (!sessionId) {
                    initializeSession();
                }
            }
        }
        
        function handleKeyDown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        async function initializeSession() {
            try {
                const response = await fetch(`${API_BASE}/api/status`);
                const data = await response.json();
                isConnected = response.ok;
                updateConnectionStatus();
            } catch (error) {
                console.error('Connection error:', error);
                isConnected = false;
                updateConnectionStatus();
            }
        }
        
        function updateConnectionStatus() {
            const indicator = document.querySelector('.status-indicator');
            if (isConnected) {
                indicator.style.background = '#00ff00';
                indicator.title = 'Connected';
            } else {
                indicator.style.background = '#ff4444';
                indicator.title = 'Disconnected';
            }
        }
        
        async function switchPersonality(personality) {
            currentPersonality = personality;
            
            // Update button states
            document.querySelectorAll('.personality-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            try {
                await fetch(`${API_BASE}/api/personality`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        personality: personality,
                        session_id: sessionId
                    })
                });
                
                const icon = personality === 'subzero' ? '🧊' : '🤖';
                const name = personality === 'subzero' ? 'Sub-Zero AI' : 'Krypt AI';
                addMessage(`Switched to ${name} mode!`, 'bot', personality);
                
            } catch (error) {
                console.error('Error switching personality:', error);
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const sendBtn = document.getElementById('sendBtn');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            input.style.height = 'auto';
            
            // Disable input and show typing
            sendBtn.disabled = true;
            showTyping(true);
            
            try {
                const response = await fetch(`${API_BASE}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: sessionId,
                        personality: currentPersonality
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    sessionId = data.session_id;
                    currentPersonality = data.personality;
                    addMessage(data.response, 'bot', data.personality);
                    isConnected = true;
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                    isConnected = false;
                }
            } catch (error) {
                console.error('Chat error:', error);
                addMessage('Connection error. Please check your internet connection.', 'bot');
                isConnected = false;
            } finally {
                showTyping(false);
                sendBtn.disabled = false;
                updateConnectionStatus();
                input.focus();
            }
        }
        
        function showTyping(show) {
            const typingIndicator = document.getElementById('typingIndicator');
            const chatArea = document.getElementById('chatArea');
            
            if (show) {
                typingIndicator.style.display = 'block';
                chatArea.scrollTop = chatArea.scrollHeight;
            } else {
                typingIndicator.style.display = 'none';
            }
        }
        
        function addMessage(text, sender, personality = 'normal') {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            const timestamp = new Date().toLocaleTimeString();
            
            if (sender === 'user') {
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `
                    <strong>👤 You:</strong> ${escapeHtml(text)}
                    <div class="message-time">${timestamp}</div>
                `;
            } else {
                const icon = personality === 'subzero' ? '🧊' : '🤖';
                const name = personality === 'subzero' ? 'Sub-Zero AI' : 'Krypt AI';
                const className = personality === 'subzero' ? 'message bot-message subzero-message' : 'message bot-message';
                
                messageDiv.className = className;
                messageDiv.innerHTML = `
                    <strong>${icon} ${name}:</strong> ${escapeHtml(text)}
                    <div class="message-time">${timestamp}</div>
                `;
            }
            
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Initialize widget
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 KoinToss Widget v2.0 loaded!');
            
            // Auto-open widget if it's the only thing on the page
            if (document.body.children.length <= 2) {
                setTimeout(toggleWidget, 1000);
            }
        });
        
        // Check connection periodically
        setInterval(async () => {
            if (sessionId) {
                try {
                    const response = await fetch(`${API_BASE}/api/status`);
                    isConnected = response.ok;
                } catch (error) {
                    isConnected = false;
                }
                updateConnectionStatus();
            }
        }, 30000); // Check every 30 seconds
    </script>
</body>
</html>
    '''
    return widget_html

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chatbot": "ready" if chatbot else "not_ready",
        "autonomous_training": "active" if autonomous_trainer and autonomous_trainer.training_active else "inactive"
    }

# Error handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="KoinToss API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level")
    
    args = parser.parse_args()
    
    print("🚀 Starting KoinToss Production API Server...")
    print(f"📡 Server will be available at http://{args.host}:{args.port}")
    print(f"📖 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"🎨 Widget Demo: http://{args.host}:{args.port}/widget")
    
    uvicorn.run(
        "enhanced_kointoss_api_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level
    )
