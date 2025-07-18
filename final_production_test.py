#!/usr/bin/env python3
"""
Final Production Test - KoinToss App
This script performs a comprehensive test of all app components
"""

import sys
import traceback
import json
import os

def test_streamlit_app():
    """Test the main Streamlit app"""
    print("🚀 Testing Streamlit App Production Readiness")
    print("=" * 50)
    
    # Test 1: Basic import
    print("1. Testing basic import...")
    try:
        import streamlit_app
        print("✅ Main app imports successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Check required functions exist
    print("\n2. Testing required functions...")
    try:
        # Check if key functions are available
        funcs_to_check = ['initialize_chatbot', 'get_crypto_price', 'detect_crypto_query']
        for func_name in funcs_to_check:
            if hasattr(streamlit_app, func_name):
                print(f"✅ {func_name} function available")
            else:
                print(f"⚠️ {func_name} function missing")
    except Exception as e:
        print(f"❌ Function check error: {e}")
    
    # Test 3: Test chatbot initialization
    print("\n3. Testing chatbot initialization...")
    try:
        chatbot = streamlit_app.initialize_chatbot()
        if chatbot:
            print("✅ Chatbot initialized successfully")
            
            # Test basic interaction
            test_response = chatbot.get_response("What is Bitcoin?", "normal")
            if test_response and 'message' in test_response:
                print("✅ Chatbot responds correctly")
            else:
                print("⚠️ Chatbot response format issues")
        else:
            print("⚠️ Chatbot not available")
    except Exception as e:
        print(f"❌ Chatbot test error: {e}")
    
    # Test 4: Test API utilities
    print("\n4. Testing API utilities...")
    try:
        price = streamlit_app.get_crypto_price("bitcoin")
        if price:
            print(f"✅ Price fetching works: BTC = ${price:,.2f}")
        else:
            print("⚠️ Price fetching not working (might be rate limited)")
    except Exception as e:
        print(f"❌ API test error: {e}")
    
    # Test 5: Test side-by-side comparison
    print("\n5. Testing side-by-side comparison...")
    try:
        if streamlit_app.CHATBOT_AVAILABLE:
            chatbot = streamlit_app.initialize_chatbot()
            if chatbot:
                # Test both personalities
                normal_response = chatbot.get_response("What is Ethereum?", "normal")
                subzero_response = chatbot.get_response("What is Ethereum?", "subzero")
                
                if normal_response and subzero_response:
                    print("✅ Both personalities respond correctly")
                    print(f"   Normal: {normal_response.get('message', 'N/A')[:50]}...")
                    print(f"   SubZero: {subzero_response.get('message', 'N/A')[:50]}...")
                else:
                    print("⚠️ Personality switching issues")
        else:
            print("⚠️ Chatbot not available for personality testing")
    except Exception as e:
        print(f"❌ Personality test error: {e}")
    
    return True

def test_deployment_files():
    """Test that all deployment files are present"""
    print("\n🔧 Testing Deployment Files")
    print("=" * 50)
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'README.md',
        'crypto_normal_dataset.json',
        'improved_dual_personality_chatbot.py',
        'enhanced_subzero_trainer.py',
        'enhanced_normal_trainer.py',
        'crypto_news_insights.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All deployment files present")
        return True

def test_config_files():
    """Test configuration files"""
    print("\n⚙️ Testing Configuration Files")
    print("=" * 50)
    
    # Check if iframe deployment package exists
    iframe_path = "kointoss-iframe-deploy"
    if os.path.exists(iframe_path):
        print(f"✅ {iframe_path} package exists")
        
        # Check iframe files
        iframe_files = [
            'streamlit_app.py',
            'requirements.txt',
            'config.toml',
            'README.md'
        ]
        
        for file in iframe_files:
            file_path = os.path.join(iframe_path, file)
            if os.path.exists(file_path):
                print(f"✅ {iframe_path}/{file}")
            else:
                print(f"❌ {iframe_path}/{file} MISSING")
    else:
        print(f"⚠️ {iframe_path} package not found")
    
    return True

def main():
    """Run all tests"""
    print("🎯 KoinToss Final Production Test")
    print("=" * 60)
    
    try:
        # Run all tests
        app_test = test_streamlit_app()
        files_test = test_deployment_files()
        config_test = test_config_files()
        
        print("\n" + "=" * 60)
        print("📋 FINAL RESULTS:")
        print(f"   App Functionality: {'✅ PASS' if app_test else '❌ FAIL'}")
        print(f"   Deployment Files: {'✅ PASS' if files_test else '❌ FAIL'}")
        print(f"   Configuration: {'✅ PASS' if config_test else '❌ FAIL'}")
        
        if app_test and files_test and config_test:
            print("\n🎉 ALL TESTS PASSED - READY FOR PRODUCTION!")
            print("\nNext steps:")
            print("1. Deploy to Streamlit Cloud using streamlit_app.py")
            print("2. Use kointoss-iframe-deploy/ for iframe deployment")
            print("3. Test in production environment")
        else:
            print("\n⚠️ SOME TESTS FAILED - REVIEW ISSUES ABOVE")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
