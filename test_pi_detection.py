#!/usr/bin/env python3
"""
Quick test to check if the trainer can handle pi coin queries without API calls
"""

def test_pi_coin_detection():
    print("🧪 Testing Pi Coin Detection")
    print("=" * 40)
    
    try:
        # Test the trainer without API calls
        import sys
        sys.path.insert(0, '.')
        
        # Mock the API functions to avoid hanging
        import api_utils
        api_utils.get_crypto_price = lambda x: None
        api_utils.get_crypto_info = lambda x: None
        
        from enhanced_normal_trainer import PureNormalTrainer
        trainer = PureNormalTrainer()
        
        test_queries = [
            "pi coin",
            "pi", 
            "what is pi coin",
            "pi coin price",
            "tell me about pi"
        ]
        
        for query in test_queries:
            response = trainer.get_response(query)
            print(f"Query: '{query}'")
            print(f"Response: {response['message'][:100]}...")
            print(f"Type: {response['type']}")
            print()
        
        print("✅ Pi coin detection test completed")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pi_coin_detection()
