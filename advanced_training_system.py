#!/usr/bin/env python3
"""
Advanced Training System for Continuous Learning and Model Improvement
- Real-time feedback learning
- Conversation quality assessment
- Dynamic model updating
- Performance optimization
"""

import json
import time
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import threading
import pickle
import random
import re
import math

class AdvancedTrainingSystem:
    def __init__(self, chatbot_instance=None):
        self.chatbot = chatbot_instance
        self.training_session_id = f"training_{int(time.time())}"
        
        # Training metrics
        self.performance_metrics = {
            'total_interactions': 0,
            'successful_interactions': 0,
            'failed_interactions': 0,
            'learning_iterations': 0,
            'model_updates': 0,
            'accuracy_improvements': [],
            'response_quality_scores': [],
            'user_satisfaction_scores': []
        }
        
        # Real-time learning data
        self.interaction_buffer = []
        self.feedback_buffer = []
        self.quality_assessment_buffer = []
        
        # Training configuration
        self.config = {
            'min_interactions_for_training': 5,
            'training_frequency_minutes': 30,
            'quality_threshold': 0.7,
            'feedback_weight': 0.8,
            'automatic_improvement': True,
            'save_training_data': True
        }
        
        # Background training thread
        self.training_thread = None
        self.training_active = False
        
        print("🎓 Advanced Training System initialized!")
        self.start_background_training()
    
    def start_background_training(self):
        """Start background training thread for continuous improvement"""
        if not self.training_active:
            self.training_active = True
            self.training_thread = threading.Thread(
                target=self._background_training_loop, 
                daemon=True
            )
            self.training_thread.start()
            print("🔄 Background training system started!")
    
    def stop_background_training(self):
        """Stop background training system"""
        self.training_active = False
        if self.training_thread:
            self.training_thread.join(timeout=5)
        print("⏹️ Background training system stopped!")
    
    def _background_training_loop(self):
        """Background loop for continuous training"""
        while self.training_active:
            try:
                time.sleep(self.config['training_frequency_minutes'] * 60)
                
                if len(self.interaction_buffer) >= self.config['min_interactions_for_training']:
                    print(f"🔄 Starting automatic training cycle...")
                    self.train_from_interactions()
                    
            except Exception as e:
                print(f"⚠️ Background training error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def record_interaction(self, user_input: str, bot_response: str, 
                          confidence: float, response_type: str, 
                          personality: str, feedback_score: float = None):
        """Record a conversation interaction for learning"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'confidence': confidence,
            'response_type': response_type,
            'personality': personality,
            'feedback_score': feedback_score,
            'session_id': self.training_session_id
        }
        
        self.interaction_buffer.append(interaction)
        self.performance_metrics['total_interactions'] += 1
        
        # Assess interaction quality
        quality_score = self.assess_interaction_quality(interaction)
        self.quality_assessment_buffer.append(quality_score)
        
        if quality_score > self.config['quality_threshold']:
            self.performance_metrics['successful_interactions'] += 1
        else:
            self.performance_metrics['failed_interactions'] += 1
        
        print(f"📊 Interaction recorded - Quality: {quality_score:.2f}, Confidence: {confidence:.2f}")
    
    def assess_interaction_quality(self, interaction: Dict) -> float:
        """Assess the quality of an interaction for learning"""
        quality_score = 0.5  # Base score
        
        # Confidence factor
        quality_score += interaction['confidence'] * 0.3
        
        # Response length appropriateness
        response_length = len(interaction['bot_response'])
        if 20 <= response_length <= 300:
            quality_score += 0.15
        elif response_length < 10:
            quality_score -= 0.2
        
        # Response type quality
        type_scores = {
            'trained_data': 0.2,
            'pattern_match': 0.15,
            'news_insights': 0.25,
            'smart_fallback': 0.1,
            'error_fallback': -0.1,
            'system_fallback': -0.15
        }
        
        response_type = interaction['response_type'].replace('normal_', '').replace('subzero_', '')
        quality_score += type_scores.get(response_type, 0)
        
        # Crypto relevance check
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'trading', 'mining']
        crypto_relevance = sum(1 for keyword in crypto_keywords 
                              if keyword in interaction['bot_response'].lower())
        quality_score += min(crypto_relevance * 0.05, 0.1)
        
        # User feedback if available
        if interaction.get('feedback_score'):
            quality_score += interaction['feedback_score'] * self.config['feedback_weight'] * 0.1
        
        return min(max(quality_score, 0.0), 1.0)
    
    def collect_user_feedback(self, interaction_index: int, 
                            satisfaction_rating: float, 
                            specific_feedback: str = None):
        """Collect user feedback for a specific interaction"""
        if 0 <= interaction_index < len(self.interaction_buffer):
            feedback = {
                'interaction_index': interaction_index,
                'satisfaction_rating': satisfaction_rating,  # 0.0 to 1.0
                'specific_feedback': specific_feedback,
                'timestamp': datetime.now().isoformat()
            }
            
            self.feedback_buffer.append(feedback)
            self.interaction_buffer[interaction_index]['feedback_score'] = satisfaction_rating
            
            print(f"📝 User feedback collected: {satisfaction_rating:.2f}")
            
            # Update metrics
            self.performance_metrics['user_satisfaction_scores'].append(satisfaction_rating)
    
    def train_from_interactions(self):
        """Train the model from recent interactions"""
        if len(self.interaction_buffer) < self.config['min_interactions_for_training']:
            print("⚠️ Not enough interactions for training")
            return
        
        print(f"🎓 Training from {len(self.interaction_buffer)} interactions...")
        
        # Filter high-quality interactions
        high_quality_interactions = [
            interaction for interaction in self.interaction_buffer
            if self.assess_interaction_quality(interaction) > self.config['quality_threshold']
        ]
        
        if len(high_quality_interactions) < 2:
            print("⚠️ Not enough high-quality interactions for training")
            return
        
        # Prepare training data
        training_conversations = []
        for interaction in high_quality_interactions:
            if interaction['confidence'] > 0.6:  # Only use confident responses
                training_conversations.append({
                    'user': interaction['user_input'],
                    'bot': interaction['bot_response'],
                    'quality_score': self.assess_interaction_quality(interaction),
                    'source': 'real_conversation'
                })
        
        # Update the continuous learning trainer
        if self.chatbot and hasattr(self.chatbot, 'normal_trainer'):
            trainer = self.chatbot.normal_trainer
            if hasattr(trainer, 'add_dynamic_conversation'):
                added_count = 0
                for conv in training_conversations:
                    trainer.add_dynamic_conversation(
                        conv['user'], 
                        conv['bot'], 
                        conv['quality_score']
                    )
                    added_count += 1
                
                print(f"✅ Added {added_count} new training conversations")
                self.performance_metrics['learning_iterations'] += 1
                self.performance_metrics['model_updates'] += 1
        
        # Clear processed interactions
        self.interaction_buffer = []
        self.quality_assessment_buffer = []
        
        # Save training session data
        if self.config['save_training_data']:
            self.save_training_session(training_conversations)
    
    def save_training_session(self, training_data: List[Dict]):
        """Save training session data for analysis"""
        session_data = {
            'session_id': self.training_session_id,
            'timestamp': datetime.now().isoformat(),
            'training_conversations': training_data,
            'performance_metrics': self.performance_metrics.copy(),
            'config': self.config.copy()
        }
        
        filename = f"training_session_{self.training_session_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Training session saved to {filename}")
        except Exception as e:
            print(f"⚠️ Error saving training session: {e}")
    
    def optimize_trainer_parameters(self):
        """Optimize trainer parameters based on performance metrics"""
        if not self.chatbot or not hasattr(self.chatbot, 'normal_trainer'):
            return
        
        trainer = self.chatbot.normal_trainer
        if not hasattr(trainer, 'similarity_threshold'):
            return
        
        success_rate = self.get_success_rate()
        current_threshold = trainer.similarity_threshold
        
        print(f"📊 Current success rate: {success_rate:.2f}, threshold: {current_threshold:.3f}")
        
        # Adaptive threshold adjustment
        if success_rate < 0.6:
            # Too restrictive, lower threshold
            new_threshold = max(current_threshold - 0.02, 0.05)
            trainer.similarity_threshold = new_threshold
            print(f"🔽 Lowered similarity threshold to {new_threshold:.3f}")
        elif success_rate > 0.9:
            # Too permissive, raise threshold
            new_threshold = min(current_threshold + 0.01, 0.3)
            trainer.similarity_threshold = new_threshold
            print(f"🔼 Raised similarity threshold to {new_threshold:.3f}")
    
    def get_success_rate(self) -> float:
        """Calculate current success rate"""
        total = self.performance_metrics['total_interactions']
        successful = self.performance_metrics['successful_interactions']
        
        if total == 0:
            return 0.0
        
        return successful / total
    
    def get_training_statistics(self) -> Dict:
        """Get comprehensive training statistics"""
        success_rate = self.get_success_rate()
        
        avg_satisfaction = 0.0
        if self.performance_metrics['user_satisfaction_scores']:
            avg_satisfaction = np.mean(self.performance_metrics['user_satisfaction_scores'])
        
        avg_quality = 0.0
        if self.performance_metrics['response_quality_scores']:
            avg_quality = np.mean(self.performance_metrics['response_quality_scores'])
        
        return {
            'session_id': self.training_session_id,
            'total_interactions': self.performance_metrics['total_interactions'],
            'success_rate': round(success_rate * 100, 1),
            'learning_iterations': self.performance_metrics['learning_iterations'],
            'model_updates': self.performance_metrics['model_updates'],
            'avg_user_satisfaction': round(avg_satisfaction, 2),
            'avg_response_quality': round(avg_quality, 2),
            'pending_interactions': len(self.interaction_buffer),
            'training_active': self.training_active,
            'last_training': datetime.now().isoformat(),
            'features': [
                'real_time_learning',
                'quality_assessment',
                'user_feedback',
                'automatic_optimization',
                'background_training'
            ]
        }
    
    def manual_training_cycle(self):
        """Manually trigger a training cycle"""
        print("🎓 Manual training cycle triggered!")
        self.train_from_interactions()
        self.optimize_trainer_parameters()
        
        # Show updated stats
        stats = self.get_training_statistics()
        print(f"📊 Training completed - Success rate: {stats['success_rate']}%")

def test_advanced_training():
    """Test the advanced training system"""
    print("🧪 Testing Advanced Training System")
    print("=" * 50)
    
    # Create training system (without chatbot for testing)
    training_system = AdvancedTrainingSystem()
    
    # Simulate some interactions
    test_interactions = [
        ("Hello!", "Hey! I'm here to help you navigate the exciting world of cryptocurrency.", 0.8, "pattern_match", "normal"),
        ("What is Bitcoin?", "Bitcoin is a decentralized digital currency that operates on blockchain technology.", 0.9, "trained_data", "normal"),
        ("How safe is crypto?", "Cryptocurrency safety depends on proper security practices and understanding the risks.", 0.7, "trained_data", "normal"),
        ("Tell me a joke", "I specialize in crypto topics - feel free to ask about trading or investing!", 0.3, "smart_fallback", "normal"),
        ("Thanks for the help!", "You're welcome! Always happy to help with crypto questions!", 0.8, "pattern_match", "normal")
    ]
    
    # Record interactions
    for i, (user_input, bot_response, confidence, response_type, personality) in enumerate(test_interactions):
        training_system.record_interaction(
            user_input, bot_response, confidence, response_type, personality
        )
        
        # Simulate user feedback for some interactions
        if i % 2 == 0:
            satisfaction = random.uniform(0.6, 1.0)
            training_system.collect_user_feedback(i, satisfaction)
    
    # Manual training cycle
    training_system.manual_training_cycle()
    
    # Show statistics
    stats = training_system.get_training_statistics()
    print(f"\n📊 Final Training Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Stop background training
    training_system.stop_background_training()
    
    print(f"\n✅ Advanced training system testing completed!")

if __name__ == "__main__":
    test_advanced_training()
