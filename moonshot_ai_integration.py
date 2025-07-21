#!/usr/bin/env python3
"""
MoonshotAI Kimi K2 Integration for KoinToss AI
Enhanced conversation capabilities with secure API handling
"""

import requests
import json
import os
from typing import Dict, Optional, List
import time

class MoonshotAIIntegration:
    def __init__(self, api_key: str = None):
        """Initialize MoonshotAI integration"""
        self.api_key = api_key or os.getenv('MOONSHOT_API_KEY')
        self.base_url = "https://api.moonshot.cn/v1"
        self.model = "moonshot-v1-8k"  # Using Kimi K2 model
        self.max_retries = 3
        self.retry_delay = 1.0
        
        # Conversation context
        self.conversation_history = []
        self.max_history_length = 10
        
        # KoinToss specific system prompt
        self.system_prompt = """You are KoinToss AI, a friendly and educational cryptocurrency assistant. 
        Your personality is helpful, informative, and beginner-friendly. 
        You explain crypto concepts clearly and provide balanced investment guidance.
        Always remind users to do their own research and never invest more than they can afford to lose.
        Use emojis appropriately and maintain a supportive, educational tone.
        Focus on education, clarity, and helping users understand complex crypto concepts."""
    
    def _make_api_request(self, messages: List[Dict]) -> Optional[Dict]:
        """Make API request to MoonshotAI"""
        if not self.api_key:
            print("⚠️ MoonshotAI API key not found")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add system prompt
        system_message = {
            "role": "system",
            "content": self.system_prompt
        }
        
        full_messages = [system_message] + messages
        
        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"⚠️ MoonshotAI API error: {response.status_code}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    return None
                    
            except Exception as e:
                print(f"⚠️ MoonshotAI request error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                return None
        
        return None
    
    def get_enhanced_response(self, user_input: str, context: Dict = None) -> Optional[Dict]:
        """Get enhanced response from MoonshotAI with crypto context"""
        
        # Prepare conversation messages
        messages = []
        
        # Add conversation history (last few exchanges)
        for history_item in self.conversation_history[-self.max_history_length:]:
            messages.append({"role": "user", "content": history_item.get("user", "")})
            messages.append({"role": "assistant", "content": history_item.get("assistant", "")})
        
        # Enhance user input with context if available
        enhanced_input = user_input
        if context:
            if context.get('price_data'):
                price_info = context['price_data']
                enhanced_input += f"\n\nCurrent market context: {price_info.get('symbol', 'crypto')} is trading at ${price_info.get('price', 'N/A')} with 24h change of {price_info.get('change_24h', 0):+.2f}%"
            
            if context.get('news_sentiment'):
                sentiment_info = context['news_sentiment']
                enhanced_input += f"\n\nNews sentiment: {sentiment_info.get('overall_sentiment', 'neutral')} based on recent headlines"
        
        # Add current user message
        messages.append({"role": "user", "content": enhanced_input})
        
        # Make API request
        response = self._make_api_request(messages)
        
        if response and 'choices' in response:
            assistant_message = response['choices'][0]['message']['content']
            
            # Add to conversation history
            self.conversation_history.append({
                "user": user_input,
                "assistant": assistant_message,
                "timestamp": time.time()
            })
            
            # Keep history manageable
            if len(self.conversation_history) > self.max_history_length:
                self.conversation_history = self.conversation_history[-self.max_history_length:]
            
            return {
                "message": assistant_message,
                "type": "moonshot_enhanced",
                "confidence": 0.9,
                "model_used": self.model,
                "tokens_used": response.get('usage', {}).get('total_tokens', 0),
                "enhanced_with_context": context is not None
            }
        
        return None
    
    def get_crypto_specific_response(self, user_input: str) -> Optional[Dict]:
        """Get crypto-specific response with enhanced prompting"""
        
        # Add crypto-specific context to the prompt
        crypto_context = """
        You are an expert cryptocurrency assistant with deep knowledge of:
        - Bitcoin, Ethereum, and major altcoins
        - DeFi, NFTs, and Web3 technologies  
        - Trading strategies and market analysis
        - Blockchain technology and consensus mechanisms
        - Current market trends and news
        
        Provide accurate, helpful, and up-to-date information about cryptocurrency topics.
        """
        
        messages = [
            {"role": "system", "content": crypto_context + self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = self._make_api_request(messages)
        
        if response and 'choices' in response:
            return {
                "message": response['choices'][0]['message']['content'],
                "type": "moonshot_crypto_enhanced",
                "confidence": 0.95,
                "model_used": self.model,
                "tokens_used": response.get('usage', {}).get('total_tokens', 0)
            }
        
        return None
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_stats(self) -> Dict:
        """Get conversation statistics"""
        return {
            "total_conversations": len(self.conversation_history),
            "model_used": self.model,
            "api_status": "connected" if self.api_key else "no_api_key"
        }

# Test the integration
if __name__ == "__main__":
    # Test with the provided API key
    api_key = "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"
    
    moonshot = MoonshotAIIntegration(api_key)
    
    print("🌙 Testing MoonshotAI Kimi K2 Integration...")
    
    # Test basic functionality
    test_queries = [
        "Hello, what is Bitcoin?",
        "How do I start trading crypto?",
        "Explain the technical aspects of blockchain consensus"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        response = moonshot.get_crypto_specific_response(query)
        
        if response:
            print(f"✅ Response received!")
            print(f"Model: {response['model_used']}")
            print(f"Tokens: {response['tokens_used']}")
            print(f"Message preview: {response['message'][:200]}...")
        else:
            print("❌ No response received")
        
        time.sleep(1)  # Rate limiting
    
    print(f"\n🎉 MoonshotAI integration test complete!")
    stats = moonshot.get_conversation_stats()
    print(f"Stats: {stats}")
