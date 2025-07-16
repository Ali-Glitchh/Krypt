#!/usr/bin/env python3
"""
Test just the basic chatbot without autonomous training
"""

import sys
import os

def test_basic_chatbot():
    print("🔍 Testing Basic Chatbot (No Autonomous Training)")
    print("=" * 50)
    
    try:
        # Test individual components first
        print("1. Testing Enhanced Normal Trainer...")
        from enhanced_normal_trainer import PureNormalTrainer
        normal_trainer = PureNormalTrainer()
        normal_response = normal_trainer.get_response("Hello!")
        print(f"   Normal trainer: {normal_response['message'][:50]}...")
        print("   ✅ Normal trainer working")
        
        print("2. Testing Sub-Zero Trainer...")
        from pure_subzero_trainer import PureSubZeroTrainer
        subzero_trainer = PureSubZeroTrainer()
        subzero_response = subzero_trainer.get_response("Hello!")
        print(f"   Sub-Zero trainer: {subzero_response['message'][:50]}...")
        print("   ✅ Sub-Zero trainer working")
        
        print("3. Testing News Service...")
        from crypto_news_insights import CryptoNewsInsights
        news_service = CryptoNewsInsights()
        print("   ✅ News service loaded")
        
        print("\n4. Testing Individual Response Processing...")
        # Test the response format that might be causing the strip error
        for response in [normal_response, subzero_response]:
            print(f"   Response type: {type(response)}")
            if isinstance(response, dict) and 'message' in response:
                message = response['message']
                print(f"   Message type: {type(message)}")
                try:
                    stripped = message.strip()
                    print(f"   ✅ Strip successful")
                except AttributeError as e:
                    print(f"   ❌ Strip failed: {e}")
                    print(f"   ❌ Message value: {repr(message)}")
        
        print("\n✅ All core components working without full chatbot!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_chatbot()
