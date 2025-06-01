#!/usr/bin/env python3
"""Direct test of Sub-Zero functionality without terminal capture issues"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_sub_zero_direct():
    """Test Sub-Zero integration directly"""
    
    # Test 1: Check if datasets exist
    print("=" * 60)
    print("🧊 SUB-ZERO INTEGRATION VERIFICATION ❄️")
    print("=" * 60)
    
    # Check Sub-Zero dataset
    sub_zero_path = 'sub_zero_crypto_dataset.json'
    if os.path.exists(sub_zero_path):
        print("✅ Sub-Zero dataset found!")
        with open(sub_zero_path, 'r', encoding='utf-8') as f:
            sub_zero_data = json.load(f)
        print(f"   Contains {len(sub_zero_data)} Sub-Zero responses")
        
        # Show a sample response
        if sub_zero_data:
            sample = sub_zero_data[0]['sub_zero']
            print(f"   Sample: {sample[:100]}...")
    else:
        print("❌ Sub-Zero dataset not found!")
        return
    
    # Check original dataset
    crypto_path = 'crypto_chat_dataset.json'
    if os.path.exists(crypto_path):
        print("✅ Original crypto dataset found!")
        with open(crypto_path, 'r', encoding='utf-8') as f:
            crypto_data = json.load(f)
        print(f"   Contains {len(crypto_data)} crypto conversations")
    else:
        print("❌ Original crypto dataset not found!")
    
    # Test 2: Import chatbot
    print("\n" + "-" * 50)
    print("🤖 CHATBOT INITIALIZATION TEST")
    print("-" * 50)
    
    try:
        from crypto_chatbot import CryptoChatbot
        print("✅ Successfully imported CryptoChatbot class")
        
        chatbot = CryptoChatbot()
        print("✅ Chatbot initialized successfully")
        
        # Check dataset loading
        dataset = chatbot.chat_dataset
        print(f"✅ Dataset loaded with {len(dataset)} categories")
        
        # Show dataset stats
        for category, items in dataset.items():
            print(f"   {category}: {len(items)} items")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Sub-Zero responses
    print("\n" + "-" * 50)
    print("🎭 SUB-ZERO PERSONALITY TEST")
    print("-" * 50)
    
    test_queries = [
        ("hello", "greeting"),
        ("tell me a joke", "joke request"),
        ("what is bitcoin", "crypto question"),
        ("explain ethereum", "crypto education"),
        ("what's your favorite crypto", "personality question")
    ]
    
    for query, description in test_queries:
        print(f"\n🔹 Testing: {description}")
        print(f"   Query: '{query}'")
        
        try:
            response = chatbot.generate_response(query)
            message = response.get('message', 'No message')
            response_type = response.get('type', 'unknown')
            
            print(f"   Type: {response_type}")
            print(f"   Response: {message[:150]}{'...' if len(message) > 150 else ''}")
            
            # Check for Sub-Zero personality markers
            sub_zero_markers = ['ice', 'frost', 'freeze', 'sub-zero', 'frozen', 'cold', 'mortal']
            has_personality = any(marker in message.lower() for marker in sub_zero_markers)
            
            if has_personality:
                print("   🧊 Sub-Zero personality: DETECTED!")
            else:
                print("   ⚠️  Sub-Zero personality: NOT DETECTED")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("❄️ VERIFICATION COMPLETE ❄️")
    print("The Sub-Zero integration should now be ready for live testing!")
    print("=" * 60)

if __name__ == "__main__":
    test_sub_zero_direct()
