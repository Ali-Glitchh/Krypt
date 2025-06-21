#!/usr/bin/env python3
"""
API Endpoint for Krypt AI Assistant
Provides REST API access to chatbot functionality for mobile/web app integration
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
from enhanced_crypto_chatbot import EnhancedCryptoChatbot
from article_manager import ArticleManager

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from web/mobile apps

# Initialize chatbot and article manager
chatbot = EnhancedCryptoChatbot()
article_manager = ArticleManager()

# Simple HTML template for testing the API
API_DOCS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Krypt AI Assistant API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .method { color: #007bff; font-weight: bold; }
        .response { background: #e9ecef; padding: 10px; margin: 10px 0; border-radius: 3px; font-family: monospace; }
        h1 { color: #333; }
        h2 { color: #666; border-bottom: 2px solid #4ecdc4; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Krypt AI Assistant API</h1>
        <p>REST API for integrating crypto chatbot into your mobile/web applications</p>
        
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <span class="method">POST</span> <strong>/api/chat</strong>
            <p>Send a message to the chatbot and get a response</p>
            <div class="response">
                Request: {"message": "What's the price of Bitcoin?", "personality": "normal"}
                Response: {"type": "price_query", "message": "...", "personality": "normal", "timestamp": "..."}
            </div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/articles</strong>
            <p>Get all available articles</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/articles/search?q=bitcoin</strong>
            <p>Search articles by query</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/insights?q=ethereum</strong>
            <p>Get insights from articles about a topic</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <strong>/api/articles</strong>
            <p>Add a new article to the knowledge base</p>
            <div class="response">
                Request: {"title": "...", "content": "...", "category": "...", "tags": [...]}
            </div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/status</strong>
            <p>Check API status and chatbot information</p>
        </div>
        
        <h2>Test the API</h2>
        <p>Use tools like Postman, curl, or your mobile/web app to test these endpoints.</p>
        
        <div class="endpoint">
            <strong>Example curl command:</strong>
            <div class="response">
curl -X POST http://localhost:5000/api/chat \\
     -H "Content-Type: application/json" \\
     -d '{"message": "What is the price of Bitcoin?"}'
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def api_docs():
    """API documentation page"""
    return render_template_string(API_DOCS_TEMPLATE)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get API status and chatbot information"""
    return jsonify({
        'status': 'online',
        'chatbot_personality': chatbot.personality_mode,
        'articles_count': len(article_manager.articles),
        'features': {
            'real_time_prices': True,
            'news_api': True,
            'article_insights': True,
            'personality_modes': ['normal', 'subzero']
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint for sending messages to the bot"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Set personality if specified
        if 'personality' in data and data['personality'] in ['normal', 'subzero']:
            chatbot.switch_personality(data['personality'])
        
        # Get bot response
        response = chatbot.generate_response(message)
        
        return jsonify({
            'type': response['type'],
            'message': response['message'],
            'action': response.get('action', 'show_response'),
            'data': response.get('data'),
            'personality': chatbot.personality_mode,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['GET', 'POST'])
def articles():
    """Get all articles or add a new article"""
    try:
        if request.method == 'GET':
            # Get all articles
            articles_list = article_manager.articles
            return jsonify({
                'articles': articles_list,
                'count': len(articles_list),
                'timestamp': datetime.now().isoformat()
            })
        
        elif request.method == 'POST':
            # Add new article
            data = request.get_json()
            
            if not data or 'title' not in data or 'content' not in data:
                return jsonify({'error': 'Title and content are required'}), 400
            
            article_id = article_manager.add_article(
                title=data['title'],
                content=data['content'],
                category=data.get('category', 'general'),
                tags=data.get('tags', []),
                url=data.get('url')
            )
            
            return jsonify({
                'success': True,
                'article_id': article_id,
                'message': 'Article added successfully',
                'timestamp': datetime.now().isoformat()
            }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/search', methods=['GET'])
def search_articles():
    """Search articles by query"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        
        if not query:
            return jsonify({'error': 'Query parameter q is required'}), 400
        
        results = article_manager.search_articles(query, category)
        
        return jsonify({
            'query': query,
            'category': category,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get insights from articles about a topic"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Query parameter q is required'}), 400
        
        insights = article_manager.get_insights_from_articles(query)
        
        return jsonify({
            'query': query,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    """Get a specific article by ID"""
    try:
        article = article_manager.get_article(article_id)
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        return jsonify({
            'article': article,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available article categories"""
    try:
        categories = set()
        for article in article_manager.articles:
            categories.add(article.get('category', 'general'))
        
        return jsonify({
            'categories': list(categories),
            'count': len(categories),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personality', methods=['GET', 'POST'])
def personality():
    """Get or set chatbot personality"""
    try:
        if request.method == 'GET':
            return jsonify({
                'current_personality': chatbot.personality_mode,
                'available_modes': ['normal', 'subzero'],
                'timestamp': datetime.now().isoformat()
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if not data or 'mode' not in data:
                return jsonify({'error': 'Mode is required'}), 400
            
            mode = data['mode']
            if mode not in ['normal', 'subzero']:
                return jsonify({'error': 'Invalid personality mode'}), 400
            
            response = chatbot.switch_personality(mode)
            
            return jsonify({
                'success': True,
                'message': response,
                'current_personality': chatbot.personality_mode,
                'timestamp': datetime.now().isoformat()
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Krypt AI Assistant API...")
    print("📚 Article manager loaded with", len(article_manager.articles), "articles")
    print("🤖 Chatbot ready in", chatbot.personality_mode, "mode")
    print("🌐 API Documentation: http://localhost:5000")
    print("🔗 Chat endpoint: http://localhost:5000/api/chat")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
