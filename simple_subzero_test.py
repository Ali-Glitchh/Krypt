#!/usr/bin/env python3
"""
Simple Sub-Zero Test
"""

try:
    print("Starting test...")
    
    # Test Sub-Zero trainer first
    print("Testing Sub-Zero trainer...")
    from subzero_conversation_trainer import SubZeroConversationTrainer
    subzero_trainer = SubZeroConversationTrainer()
    print(f"✅ Sub-Zero trainer loaded with {len(subzero_trainer.conversation_pairs)} pairs")
    
    # Test a few responses
    test_response = subzero_trainer.get_subzero_response("How are you?")
    print(f"Test response: {test_response}")
    
    print("Testing enhanced chatbot...")
    from enhanced_crypto_chatbot import EnhancedCryptoChatbot
    print("Enhanced chatbot imported successfully")
    
    chatbot = EnhancedCryptoChatbot()
    print("✅ Enhanced chatbot created successfully")
    
    # Test personality switch
    result = chatbot.switch_personality("subzero")
    print(f"Personality switch result: {result}")
    print(f"Current mode: {chatbot.personality_mode}")
    
    # Test a simple response
    response = chatbot.generate_response("Hi there!")
    print(f"Response: {response}")
    
    print("✅ All tests passed!")

except Exception as e:
    import traceback
    print(f"❌ Error: {e}")
    print("Full traceback:")
    traceback.print_exc()
