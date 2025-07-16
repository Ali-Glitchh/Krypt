#!/usr/bin/env python3
"""
Test to specifically check the API integration and coin detection
"""

def test_api_integration():
    print("🧪 Testing API Integration for Coin Queries")
    print("=" * 50)
    
    try:
        # Test direct API functions
        print("1. Testing API utilities...")
        from api_utils import get_crypto_price, get_crypto_info, get_static_crypto_info
        
        # Test static fallback
        pi_static = get_static_crypto_info('pi-network')
        print(f"   Pi static info: {pi_static['name'] if pi_static else 'None'}")
        
        # Test simple trainer response to "pi coin"
        print("\n2. Testing enhanced normal trainer...")
        from enhanced_normal_trainer import PureNormalTrainer
        trainer = PureNormalTrainer()
        
        test_queries = ["pi coin", "pi", "bitcoin", "what is pi coin", "pi coin price"]
        
        for query in test_queries:
            response = trainer.get_response(query)
            print(f"   Query: '{query}'")
            print(f"   Response: {response['message'][:100]}...")
            print(f"   Type: {response['type']}")
            print()
        
        print("✅ API integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ Error in API integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_api_integration()
