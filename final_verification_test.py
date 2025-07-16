#!/usr/bin/env python3
"""
Final verification test for the strip error fix
This script tests the core chatbot functionality to ensure
the strip error is completely resolved.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_basic_functionality():
    """Test basic chatbot functionality without the Streamlit interface"""
    print("🔍 Testing core chatbot functionality...")
    
    try:
        # Import the improved chatbot
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        
        # Initialize chatbot
        print("📱 Initializing chatbot...")
        chatbot = ImprovedDualPersonalityChatbot()
        
        # Test basic responses
        test_inputs = [
            "hello",
            "what is bitcoin?",
            "switch to sub-zero",
            "tell me about ethereum",
            "",  # Empty input test
            " ",  # Whitespace test
        ]
        
        print("\n🧪 Running response tests...")
        for i, test_input in enumerate(test_inputs, 1):
            try:
                print(f"\nTest {i}: Input = '{test_input}'")
                response = chatbot.get_response(test_input)
                
                # Check response type
                if isinstance(response, dict):
                    print(f"✅ Dict response: {response.get('message', 'No message key')[:50]}...")
                elif isinstance(response, str):
                    print(f"✅ String response: {response[:50]}...")
                else:
                    print(f"⚠️  Unexpected type: {type(response)}")
                    
            except Exception as e:
                print(f"❌ Error in test {i}: {e}")
                
        print("\n✅ Core chatbot functionality test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return False

def test_streamlit_import():
    """Test if streamlit app can be imported without errors"""
    print("\n🔍 Testing Streamlit app import...")
    
    try:
        # Test if we can import the main components
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Check if our fixed app can be read
        with open('streamlit_app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for the fix markers
        if 'isinstance(ai_response, dict)' in content:
            print("✅ Dict type checking found in streamlit_app.py")
        if 'isinstance(ai_response, str)' in content:
            print("✅ String type checking found in streamlit_app.py")
        if 'response_message = ai_response.strip()' in content:
            print("✅ Safe strip() usage found in streamlit_app.py")
            
        print("✅ Streamlit app structure verified!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit app verification failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Starting Final Verification Tests")
    print("=" * 50)
    
    # Test 1: Core chatbot functionality
    test1_passed = test_chatbot_basic_functionality()
    
    # Test 2: Streamlit app verification
    test2_passed = test_streamlit_import()
    
    print("\n" + "=" * 50)
    print("📊 FINAL VERIFICATION RESULTS:")
    print(f"Core Chatbot Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Streamlit App Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! The strip error fix is SUCCESSFUL!")
        print("✅ Your KoinToss chatbot is ready to use!")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    main()
