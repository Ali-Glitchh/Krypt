#!/usr/bin/env python3
"""
Simple Training Status Monitor
Shows current training status without external dependencies
"""

from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
from datetime import datetime

def show_training_status():
    print("🤖 AUTONOMOUS TRAINING STATUS MONITOR")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize chatbot
    print("\n🔄 Initializing chatbot systems...")
    try:
        bot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return
    
    # Show system capabilities
    print(f"\n🎯 SYSTEM CAPABILITIES")
    print("-" * 30)
    
    # Get personality info
    info = bot.get_personality_info()
    print(f"Available personalities: {', '.join(info.get('available_personalities', []))}")
    print(f"Current personality: {info.get('current_personality', 'Unknown').upper()}")
    print(f"System features: {len(info.get('features', []))} active")
    
    # Show training information
    if 'normal_training' in info:
        normal_info = info['normal_training']
        print(f"\n🧠 Normal Personality Training:")
        print(f"   Type: {normal_info.get('type', 'Unknown')}")
        print(f"   Accuracy: {normal_info.get('accuracy_rate', 'N/A')}")
        print(f"   Total conversations: {normal_info.get('total_conversations', 0)}")
        if 'features' in normal_info:
            print(f"   Features: {', '.join(normal_info['features'][:3])}...")
    
    if 'subzero_training' in info:
        subzero_info = info['subzero_training']
        print(f"\n🧊 Sub-Zero Personality Training:")
        print(f"   Type: {subzero_info.get('type', 'Unknown')}")
        if 'features' in subzero_info:
            print(f"   Features: {', '.join(subzero_info['features'][:2])}...")
    
    # Test conversation quality
    print(f"\n💬 CONVERSATION QUALITY ASSESSMENT")
    print("-" * 30)
    
    test_scenarios = [
        ("Hello!", "greeting"),
        ("What is Bitcoin?", "crypto_knowledge"),
        ("How do I invest safely?", "investment_advice"),
        ("Is crypto risky?", "risk_assessment")
    ]
    
    quality_scores = []
    for question, scenario_type in test_scenarios:
        print(f"\n[{scenario_type.upper()}]")
        print(f"Q: {question}")
        
        response = bot.get_response(question)
        quality = assess_response_quality(question, response['message'])
        quality_scores.append(quality)
        
        print(f"A: {response['message'][:70]}...")
        print(f"Quality score: {quality:.1%} | Type: {response['type']}")
    
    avg_quality = sum(quality_scores) / len(quality_scores)
    print(f"\n📊 Average response quality: {avg_quality:.1%}")
    
    # Determine quality rating
    if avg_quality >= 0.8:
        quality_rating = "EXCELLENT ⭐⭐⭐"
    elif avg_quality >= 0.6:
        quality_rating = "GOOD ⭐⭐"
    elif avg_quality >= 0.4:
        quality_rating = "FAIR ⭐"
    else:
        quality_rating = "NEEDS IMPROVEMENT"
    
    print(f"Quality rating: {quality_rating}")
    
    # Test personality switching
    print(f"\n🔄 PERSONALITY SWITCHING TEST")
    print("-" * 30)
    
    # Test Sub-Zero
    print("Switching to Sub-Zero personality...")
    bot.switch_personality('subzero')
    subzero_response = bot.get_response("What do you think about cryptocurrency?")
    print(f"Sub-Zero: {subzero_response['message'][:80]}...")
    
    # Switch back to normal
    print("Switching back to normal personality...")
    bot.switch_personality('normal')
    normal_response = bot.get_response("Thank you for the information")
    print(f"Normal: {normal_response['message'][:80]}...")
    
    # Show learning statistics
    print(f"\n📈 LEARNING STATISTICS")
    print("-" * 30)
    
    stats = bot.get_learning_statistics()
    print(f"Continuous learning enabled: {stats.get('continuous_learning_enabled', False)}")
    print(f"Autonomous training enabled: {stats.get('autonomous_training_enabled', False)}")
    print(f"Total training conversations: {stats.get('total_training_conversations', 0)}")
    print(f"Session conversations: {stats.get('conversation_history_length', 0)}")
    
    # Show training recommendations
    print(f"\n💡 TRAINING RECOMMENDATIONS")
    print("-" * 30)
    
    recommendations = bot.get_training_recommendations()
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("✅ No specific recommendations - system performing well")
    
    # Autonomous training status
    print(f"\n🤖 AUTONOMOUS TRAINING STATUS")
    print("-" * 30)
    
    auto_status = bot.get_autonomous_training_status()
    if auto_status.get('available', True):
        print("Status: Available")
        for key, value in auto_status.items():
            if key != 'available':
                print(f"{key}: {value}")
    else:
        print("Status: Not Available")
        print("Reason: System not initialized")
    
    # Show overall system health
    print(f"\n🏥 SYSTEM HEALTH SUMMARY")
    print("-" * 30)
    
    health_score = calculate_system_health(avg_quality, stats, auto_status)
    
    if health_score >= 0.8:
        health_status = "EXCELLENT 🟢"
        health_msg = "System is performing optimally with high accuracy"
    elif health_score >= 0.6:
        health_status = "GOOD 🟡"  
        health_msg = "System is performing well with room for improvement"
    elif health_score >= 0.4:
        health_status = "FAIR 🟠"
        health_msg = "System needs attention to improve performance"
    else:
        health_status = "POOR 🔴"
        health_msg = "System requires immediate optimization"
    
    print(f"Overall health: {health_status}")
    print(f"Health score: {health_score:.1%}")
    print(f"Assessment: {health_msg}")
    
    # Show next steps
    print(f"\n🚀 NEXT STEPS FOR CONTINUOUS IMPROVEMENT")
    print("-" * 30)
    
    if not stats.get('autonomous_training_enabled', False):
        print("1. Enable autonomous training for continuous learning")
        print("   Command: bot.enable_autonomous_training()")
    
    if avg_quality < 0.7:
        print("2. Expand training dataset with more diverse conversations")
        print("3. Implement user feedback collection")
    
    if stats.get('total_training_conversations', 0) < 1000:
        print("4. Increase training dataset size for better coverage")
    
    print("5. Monitor performance metrics regularly")
    print("6. Collect user satisfaction feedback")
    
    print(f"\n✅ TRAINING STATUS MONITORING COMPLETE")
    print("🎯 The chatbot is operational and ready for continuous improvement!")

def assess_response_quality(question, response):
    """Assess the quality of a response"""
    if not response or len(response) < 5:
        return 0.0
    
    score = 0.3  # Base score
    
    # Length appropriateness (20-200 characters is good)
    if 20 <= len(response) <= 200:
        score += 0.2
    elif len(response) > 200:
        score += 0.1  # Long responses are okay but not ideal
    
    # Crypto relevance
    crypto_words = ['crypto', 'bitcoin', 'blockchain', 'investment', 'trading', 'defi', 'ethereum']
    if any(word in response.lower() for word in crypto_words):
        score += 0.2
    
    # Helpful tone
    helpful_words = ['help', 'assist', 'explain', 'understand', 'important', 'consider']
    if any(word in response.lower() for word in helpful_words):
        score += 0.15
    
    # Information density (good number of words)
    word_count = len(response.split())
    if 10 <= word_count <= 50:
        score += 0.1
    
    # Avoid poor responses
    poor_indicators = ["don't know", "not sure", "can't help", "sorry"]
    if any(indicator in response.lower() for indicator in poor_indicators):
        score -= 0.2
    
    # Question answering
    if '?' in question and len(response) > 30:
        score += 0.05
    
    return max(min(score, 1.0), 0.0)

def calculate_system_health(quality_score, stats, auto_status):
    """Calculate overall system health score"""
    health = 0.0
    
    # Response quality (40% weight)
    health += quality_score * 0.4
    
    # Continuous learning (30% weight)
    if stats.get('continuous_learning_enabled', False):
        health += 0.3
    
    # Training data availability (20% weight)
    training_conversations = stats.get('total_training_conversations', 0)
    if training_conversations > 1000:
        health += 0.2
    elif training_conversations > 500:
        health += 0.15
    elif training_conversations > 100:
        health += 0.1
    
    # Autonomous training capability (10% weight)
    if auto_status.get('available', False):
        health += 0.1
    
    return min(health, 1.0)

if __name__ == "__main__":
    show_training_status()
