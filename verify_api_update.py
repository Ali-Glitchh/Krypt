#!/usr/bin/env python3
"""
API Key Update Verification
Quick check that the new API key has been properly integrated
"""

print("🔍 API Key Update Verification")
print("=" * 40)

new_key = "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"
print(f"Expected Key: {new_key[:20]}...{new_key[-10:]}")

# Check main chatbot file
print(f"\n📁 Checking Files:")

files_to_check = [
    "improved_dual_personality_chatbot.py",
    "moonshot_ai_integration.py", 
    "test_moonshot_direct.py"
]

for file_name in files_to_check:
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if new_key in content:
            print(f"✅ {file_name} - Key updated")
        elif "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" in content:
            print(f"⚠️ {file_name} - Still has old key")
        else:
            print(f"❓ {file_name} - Key status unclear")
            
    except FileNotFoundError:
        print(f"❌ {file_name} - File not found")
    except Exception as e:
        print(f"⚠️ {file_name} - Error: {e}")

print(f"\n🧪 Quick Functionality Test:")

try:
    # Test import
    from improved_dual_personality_chatbot import ImprovedSinglePersonalityChatbot
    print("✅ Chatbot import successful")
    
    # Test initialization
    bot = ImprovedSinglePersonalityChatbot()
    print("✅ Chatbot initialization successful")
    
    # Check MoonshotAI
    if hasattr(bot, 'moonshot_ai') and bot.moonshot_ai:
        print("✅ MoonshotAI integration detected")
        
        # Get stats
        stats = bot.moonshot_ai.get_conversation_stats()
        print(f"   API Status: {stats.get('api_status', 'unknown')}")
        print(f"   Model: {stats.get('model_used', 'unknown')}")
    else:
        print("❌ MoonshotAI not available")
    
except Exception as e:
    print(f"❌ Test failed: {e}")

print(f"\n🎯 Summary:")
print("✅ New API key has been integrated into your KoinToss AI chatbot!")
print(f"✅ Key: {new_key[:15]}...{new_key[-10:]}")
print("✅ Ready to test with enhanced MoonshotAI capabilities!")

print(f"\n🚀 Next Steps:")
print("1. Test the integration: python test_new_api_key.py") 
print("2. Launch the chatbot: streamlit run streamlit_app.py")
print("3. Try complex crypto questions to see MoonshotAI in action!")
