#!/usr/bin/env python3
"""
Minimal test to verify core chatbot functionality without autonomous training
"""

def test_core_chatbot():
    print("🧪 Testing Core Chatbot (No Autonomous Training)")
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
        
        print("\n✅ All core components working without scikit-learn!")
        print("🚀 System is ready for deployment")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_core_chatbot()
