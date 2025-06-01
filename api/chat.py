from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversation.conversation_bot import ConversationBot

# Initialize the conversation bot
bot = ConversationBot()

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            
            # Generate response
            response_data = bot.generate_response(message, session_id)
            
            # If it's a crypto analysis request, we need to trigger the analysis
            if response_data.get('type') == 'crypto_analysis' and response_data.get('crypto'):
                # Add a flag to indicate the frontend should perform crypto analysis
                response_data['trigger_analysis'] = True
                response_data['crypto_name'] = response_data['crypto']
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())