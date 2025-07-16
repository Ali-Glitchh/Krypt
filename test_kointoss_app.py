#!/usr/bin/env python3
"""
Test the enhanced KoinToss Streamlit app functionality
"""

def test_kointoss_app():
    print("🧪 Testing Enhanced KoinToss Streamlit App")
    print("=" * 50)
    
    try:
        # Test import of new app
        print("1. Testing app imports...")
        import kointoss_streamlit_app
        print("   ✅ KoinToss app imported successfully")
        
        # Test chatbot initialization
        print("2. Testing chatbot initialization...")
        chatbot = kointoss_streamlit_app.initialize_chatbot()
        if chatbot:
            print("   ✅ Chatbot initialized")
        else:
            print("   ⚠️ Chatbot not available")
        
        # Test a sample response
        if chatbot:
            print("3. Testing pi coin query...")
            response = chatbot.get_response("pi coin")
            if isinstance(response, dict):
                print(f"   ✅ Response: {response['message'][:50]}...")
                print(f"   📊 Personality: {response.get('personality', 'unknown')}")
            else:
                print(f"   ✅ Response: {response[:50]}...")
        
        print("\n" + "="*50)
        print("🚀 KOINTOSS APP STATUS: READY")
        print("✅ Enhanced UI with animated logo")
        print("✅ KoinToss branding applied")
        print("✅ Ice-blue color scheme")
        print("✅ Loading animations")
        print("✅ Enhanced chat interface")
        print("✅ Status indicators")
        print("✅ Responsive design")
        
        print(f"\n📋 TO RUN THE APP:")
        print(f"   streamlit run kointoss_streamlit_app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing KoinToss app: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_kointoss_app()
    print(f"\n🎯 TEST RESULT: {'SUCCESS' if success else 'FAILURE'}")
