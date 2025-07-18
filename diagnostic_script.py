#!/usr/bin/env python3
"""
Diagnostic script to identify issues with the Streamlit app
"""

import sys
import traceback

print("🔍 KoinToss App Diagnostic Script")
print("=" * 50)

# Test 1: Basic Python imports
print("\n1. Testing basic Python imports...")
try:
    import os
    import json
    import time
    import datetime
    print("✅ Basic Python modules OK")
except Exception as e:
    print(f"❌ Basic Python modules error: {e}")

# Test 2: Required packages
print("\n2. Testing required packages...")
required_packages = [
    'streamlit',
    'requests', 
    'pandas',
    'plotly',
    'vaderSentiment',
    'numpy'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"✅ {package} OK")
    except ImportError:
        print(f"❌ {package} NOT FOUND")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️ Missing packages: {missing_packages}")
    print("Install with: pip install", " ".join(missing_packages))

# Test 3: Custom modules
print("\n3. Testing custom modules...")
custom_modules = [
    'improved_dual_personality_chatbot',
    'enhanced_subzero_trainer', 
    'enhanced_normal_trainer',
    'crypto_news_insights',
    'api_utils'
]

for module in custom_modules:
    try:
        __import__(module)
        print(f"✅ {module} OK")
    except ImportError as e:
        print(f"❌ {module} error: {e}")
    except Exception as e:
        print(f"⚠️ {module} import issue: {e}")

# Test 4: Dataset files
print("\n4. Testing dataset files...")
dataset_files = [
    'sub_zero_crypto_comprehensive_dataset.json',
    'crypto_normal_dataset.json'
]

for file in dataset_files:
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        print(f"✅ {file} OK ({len(data)} items)")
    except FileNotFoundError:
        print(f"❌ {file} NOT FOUND")
    except Exception as e:
        print(f"⚠️ {file} issue: {e}")

# Test 5: Streamlit app syntax
print("\n5. Testing Streamlit app syntax...")
try:
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
    
    # Compile check
    compile(content, 'streamlit_app.py', 'exec')
    print("✅ streamlit_app.py syntax OK")
except SyntaxError as e:
    print(f"❌ streamlit_app.py syntax error: {e}")
except Exception as e:
    print(f"⚠️ streamlit_app.py issue: {e}")

# Test 6: Chatbot creation
print("\n6. Testing chatbot creation...")
try:
    from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
    bot = ImprovedDualPersonalityChatbot()
    print("✅ Chatbot created successfully")
    print(f"✅ Current personality: {bot.personality_mode}")
    
    # Test response
    response = bot.get_response("hello")
    print(f"✅ Test response: {str(response)[:100]}...")
    
except Exception as e:
    print(f"❌ Chatbot creation error: {e}")
    traceback.print_exc()

print("\n" + "=" * 50)
print("🏁 Diagnostic complete!")
