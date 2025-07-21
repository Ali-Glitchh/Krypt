#!/usr/bin/env python3
"""
Test Enhanced KoinToss AI System
"""

from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
import json

def test_enhanced_system():
    print("Testing Enhanced KoinToss AI...")
    bot = ImprovedDualPersonalityChatbot()
    
    # Test cases with different sentiments
    test_cases = [
        ("price of bitcoin", "Price Query Test"),
        ("I am worried about bitcoin crashing", "Bearish Sentiment Test"),
        ("Bitcoin is going to the moon!", "Bullish Sentiment Test"),
        ("what is ethereum", "Technical Query Test"),
        ("how to buy crypto", "Investment Query Test")
    ]
    
    for question, description in test_cases:
        print(f"\n=== {description} ===")
        print(f"Q: {question}")
        
        response = bot.get_response(question)
        
        if isinstance(response, dict):
            print(f"Personality: {response.get('personality', 'unknown')}")
            enhanced = response.get('enhancements_applied', False)
            print(f"Enhanced: {enhanced}")
            
            if enhanced:
                sentiment = response.get('sentiment_analysis', {})
                sentiment_label = sentiment.get('sentiment_label', 'unknown')
                compound_score = sentiment.get('compound', 0)
                query_type = response.get('query_type', 'unknown')
                
                print(f"Sentiment: {sentiment_label} ({compound_score:.2f})")
                print(f"Query Type: {query_type}")
            
            message = response.get('message', '')
            print(f"Response Preview: {message[:100]}...")
        
        print("-" * 60)
    
    # Test personality switching
    print("\n=== Testing Personality Switch ===")
    bot.switch_personality('subzero')
    response = bot.get_response("what is bitcoin")
    
    if isinstance(response, dict):
        message = response.get('message', '')
        print(f"Warrior Response: {message[:100]}...")

if __name__ == "__main__":
    test_enhanced_system()
