#!/usr/bin/env python3
"""
Quick test of autonomous training system
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_autonomous_training():
    print("🧪 Testing Autonomous Training System")
    print("=" * 50)
    
    try:
        # Test the autonomous training system directly
        print("1. Testing autonomous training system import...")
        from autonomous_training_system import AutonomousTrainingSystem
        print("   ✅ Import successful")
        
        # Test the chatbot import
        print("2. Testing chatbot import...")
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        print("   ✅ Chatbot import successful")
        
        # Initialize chatbot
        print("3. Initializing chatbot...")
        bot = ImprovedDualPersonalityChatbot()
        print("   ✅ Chatbot initialized")
        
        # Test basic functionality
        print("4. Testing basic conversation...")
        response = bot.get_response("Hello!")
        print(f"   Response: {response['message'][:50]}...")
        print("   ✅ Basic conversation working")
        
        # Test learning statistics
        print("5. Testing learning statistics...")
        stats = bot.get_learning_statistics()
        print(f"   Continuous learning: {stats.get('continuous_learning_enabled', False)}")
        print(f"   Autonomous training: {stats.get('autonomous_training_enabled', False)}")
        print("   ✅ Statistics working")
        
        # Test autonomous training if available
        print("6. Testing autonomous training...")
        if bot.autonomous_trainer:
            print("   ✅ Autonomous trainer available")
            
            # Test getting recommendations
            recommendations = bot.get_training_recommendations()
            print(f"   Recommendations: {len(recommendations)} items")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"      {i}. {rec}")
            
            # Test training status
            auto_status = bot.get_autonomous_training_status()
            print(f"   Training status: {auto_status}")
            
        else:
            print("   ⚠️ Autonomous trainer not available")
        
        print("\n✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_continuous_learning():
    """Test the continuous learning trainer directly"""
    print("\n🧪 Testing Continuous Learning Trainer")
    print("-" * 40)
    
    try:
        from continuous_learning_trainer import ContinuousLearningTrainer
        
        trainer = ContinuousLearningTrainer()
        print("✅ Continuous learning trainer loaded")
        
        # Test response generation
        result = trainer.find_best_response_with_learning("What is Bitcoin?")
        print(f"Test response: {result['response'][:50]}...")
        print(f"Confidence: {result['confidence']:.3f}")
        
        # Get learning stats
        stats = trainer.get_learning_stats()
        print(f"Learning stats: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing continuous learning: {e}")
        return False

if __name__ == "__main__":
    success1 = test_autonomous_training()
    success2 = test_continuous_learning()
    
    if success1 and success2:
        print("\n🎉 All systems operational!")
        print("🚀 Ready for autonomous training!")
    else:
        print("\n⚠️ Some issues detected - check the logs above")
