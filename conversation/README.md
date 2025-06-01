# Conversation System for Krypt Bot

## 1. Using OpenAI GPT (Recommended for Quick Setup)

```python
import openai
from typing import Dict, List, Tuple
import json
import re

class ConversationManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.conversation_history = []
        self.system_prompt = """
        You are Krypt, a friendly cryptocurrency analysis assistant. You help users with:
        1. Cryptocurrency market analysis and sentiment
        2. Understanding crypto trends and news
        3. General crypto education
        4. Casual conversation about crypto and technology
        
        You should:
        - Be helpful, friendly, and conversational
        - Provide accurate crypto information
        - Warn about investment risks
        - Detect when users want specific crypto analysis vs general chat
        - Remember context from the conversation
        """
    
    def classify_intent(self, user_input: str) -> str:
        """Classify user intent"""
        crypto_keywords = ['price', 'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 
                          'coin', 'market', 'sentiment', 'analysis', 'worth']
        help_keywords = ['help', 'how', 'what can you', 'features', 'guide']
        greeting_keywords = ['hi', 'hello', 'hey', 'good morning', 'good evening']
        
        user_input_lower = user_input.lower()
        
        # Check for crypto-specific queries
        if any(keyword in user_input_lower for keyword in crypto_keywords):
            return 'crypto_analysis'
        elif any(keyword in user_input_lower for keyword in help_keywords):
            return 'help'
        elif any(keyword in user_input_lower for keyword in greeting_keywords):
            return 'greeting'
        else:
            return 'general_chat'
    
    def generate_response(self, user_input: str, intent: str) -> str:
        """Generate conversational response"""
        if intent == 'crypto_analysis':
            # Extract cryptocurrency name and redirect to analysis
            return self.handle_crypto_query(user_input)
        
        # For general conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history[-10:]  # Keep last 10 messages for context
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            assistant_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        
        except Exception as e:
            return f"I'm having trouble processing that. Could you try asking differently?"
    
    def handle_crypto_query(self, user_input: str) -> Dict:
        """Extract crypto name and prepare for analysis"""
        # Extract cryptocurrency mentions
        crypto_patterns = {
            'bitcoin': ['bitcoin', 'btc'],
            'ethereum': ['ethereum', 'eth'],
            'cardano': ['cardano', 'ada'],
            # Add more patterns
        }
        
        found_crypto = None
        for crypto, patterns in crypto_patterns.items():
            if any(pattern in user_input.lower() for pattern in patterns):
                found_crypto = crypto
                break
        
        if found_crypto:
            return {
                'type': 'crypto_analysis',
                'crypto': found_crypto,
                'query': user_input
            }
        else:
            return {
                'type': 'clarification',
                'message': "Which cryptocurrency would you like me to analyze?"
            }
```

## 2. Using Rasa (Open Source Conversational AI)

```yaml
# domain.yml
version: "3.1"

intents:
  - greet
  - goodbye
  - affirm
  - deny
  - mood_great
  - mood_unhappy
  - bot_challenge
  - ask_crypto_price
  - ask_crypto_sentiment
  - ask_crypto_news
  - general_crypto_question

entities:
  - cryptocurrency
  - time_period

responses:
  utter_greet:
    - text: "Hey! I'm Krypt, your crypto analysis assistant. How can I help you today?"
    
  utter_ask_crypto:
    - text: "Which cryptocurrency would you like to know about?"
    
  utter_crypto_analysis:
    - text: "Let me analyze {cryptocurrency} for you..."

actions:
  - action_analyze_crypto
  - action_get_sentiment
  - action_fetch_news

# stories.yml
version: "3.1"

stories:
  - story: happy path
    steps:
      - intent: greet
      - action: utter_greet
      - intent: ask_crypto_price
        entities:
          - cryptocurrency: "bitcoin"
      - action: action_analyze_crypto
      
  - story: sentiment analysis
    steps:
      - intent: ask_crypto_sentiment
        entities:
          - cryptocurrency: "ethereum"
      - action: action_get_sentiment
```

## 3. Using Dialogflow (Google's NLP)

```python
import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

class DialogflowManager:
    def __init__(self, project_id, credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self.session_client = dialogflow.SessionsClient(credentials=credentials)
        self.project_id = project_id
        
    def detect_intent(self, session_id, text_input, language_code='en'):
        """Detects the intent of the text using Dialogflow"""
        session = self.session_client.session_path(self.project_id, session_id)
        text_input = dialogflow.types.TextInput(
            text=text_input, language_code=language_code
        )
        query_input = dialogflow.types.QueryInput(text=text_input)
        
        response = self.session_client.detect_intent(
            session=session, query_input=query_input
        )
        
        return {
            'intent': response.query_result.intent.display_name,
            'parameters': response.query_result.parameters,
            'fulfillment_text': response.query_result.fulfillment_text
        }
```

## 4. Custom Training with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from torch.utils.data import Dataset, DataLoader
import json

class CryptoConversationDataset(Dataset):
    def __init__(self, conversations_file):
        with open(conversations_file, 'r') as f:
            self.conversations = json.load(f)
    
    def __len__(self):
        return len(self.conversations)
    
    def __getitem__(self, idx):
        return self.conversations[idx]

class KryptConversationModel:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
    def train_on_conversations(self, dataset_path, epochs=3):
        """Fine-tune the model on crypto conversations"""
        dataset = CryptoConversationDataset(dataset_path)
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
        
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5)
        
        for epoch in range(epochs):
            for batch in dataloader:
                # Training logic here
                pass
    
    def generate_response(self, user_input, chat_history_ids=None):
        """Generate response for user input"""
        # Encode user input
        new_user_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token, 
            return_tensors='pt'
        )
        
        # Append to chat history
        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        else:
            bot_input_ids = new_user_input_ids
        
        # Generate response
        chat_history_ids = self.model.generate(
            bot_input_ids, 
            max_length=1000,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Decode response
        response = self.tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )
        
        return response, chat_history_ids
```

## 5. Training Data Collection

```python
# training_data_collector.py
import json
from datetime import datetime

class TrainingDataCollector:
    def __init__(self, data_file='conversation_data.json'):
        self.data_file = data_file
        self.conversations = []
        
    def collect_conversation(self, user_input, bot_response, intent, entities=None):
        """Collect conversation data for training"""
        self.conversations.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'intent': intent,
            'entities': entities or {},
            'feedback': None  # Can be filled later
        })
        
    def save_data(self):
        """Save collected data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    def create_training_examples(self):
        """Convert conversations to training format"""
        examples = []
        for conv in self.conversations:
            examples.append({
                'input': conv['user_input'],
                'output': conv['bot_response'],
                'intent': conv['intent']
            })
        return examples

# Example training data format
training_data = [
    {
        "conversations": [
            {
                "user": "Hey, what's up with Bitcoin today?",
                "bot": "Hi! Let me check Bitcoin's current status for you. Bitcoin is currently trading at $X with a Y% change in the last 24 hours. Would you like to see the detailed analysis?"
            },
            {
                "user": "Is it a good time to invest?",
                "bot": "I can provide market analysis, but remember that I'm not a financial advisor. Based on current sentiment analysis, Bitcoin shows [positive/negative/neutral] indicators. However, cryptocurrency investments are highly volatile and risky. Always do your own research and consider consulting with a financial professional before making investment decisions."
            }
        ]
    }
]
```

## 6. Integration with Your Existing Code

```python
# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
from conversation.conversation_manager import ConversationManager
import os

conversation_manager = ConversationManager(api_key=os.getenv('OPENAI_API_KEY'))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_input = data.get('message', '')
            session_id = data.get('session_id', 'default')
            
            # Classify intent
            intent = conversation_manager.classify_intent(user_input)
            
            # Generate response
            response_data = conversation_manager.generate_response(user_input, intent)
            
            # If it's a crypto query, include analysis data
            if isinstance(response_data, dict) and response_data.get('type') == 'crypto_analysis':
                # Call your existing crypto analysis function
                crypto_data = analyze_crypto(response_data.get('crypto'))
                response = {
                    'message': f"I'll analyze {response_data['crypto']} for you.",
                    'crypto_data': crypto_data,
                    'intent': 'crypto_analysis'
                }
            else:
                response = {
                    'message': response_data,
                    'intent': intent
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
```

## 7. Frontend Integration

```javascript
// Add to your index.html
class ChatBot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.chatHistory = [];
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
    
    async sendMessage(message) {
        // Add user message to chat
        this.addMessageToChat('user', message);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            // Add bot response to chat
            this.addMessageToChat('bot', data.message);
            
            // If crypto analysis, show detailed view
            if (data.crypto_data) {
                this.displayCryptoAnalysis(data.crypto_data);
            }
            
        } catch (error) {
            this.addMessageToChat('bot', 'Sorry, I encountered an error. Please try again.');
        }
    }
    
    addMessageToChat(sender, message) {
        const chatContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                ${message}
            </div>
            <div class="message-time">
                ${new Date().toLocaleTimeString()}
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
```

## 8. Step-by-Step Implementation Plan

1. **Choose Your Approach**:
   - Quick setup: Use OpenAI GPT or Claude API
   - Free option: Use Rasa or train your own model
   - Enterprise: Use Dialogflow or AWS Lex

2. **Set Up Basic Conversation**:
   ```bash
   pip install openai transformers rasa
   ```

3. **Create Training Data**:
   - Collect common crypto questions
   - Create intent categories
   - Build response templates

4. **Implement Intent Recognition**:
   - Crypto queries
   - General questions
   - Greetings/Small talk
   - Help requests

5. **Train Your Model**:
   - Use pre-trained model with fine-tuning
   - Or train from scratch with your data

6. **Deploy and Test**:
   - Add chat endpoint to your API
   - Update frontend with chat interface
   - Test with various queries

7. **Continuous Improvement**:
   - Collect user interactions
   - Review and improve responses
   - Retrain periodically

Would you like me to implement a specific approach for your Krypt bot?