#!/usr/bin/env python3
"""
Autonomous Training System
Continuously trains the chatbot to improve conversation accuracy
"""

import json
import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot

class AutonomousTrainingSystem:
    def __init__(self, chatbot: ImprovedDualPersonalityChatbot):
        self.chatbot = chatbot
        self.training_active = False
        self.training_thread = None
        
        # Training metrics
        self.training_sessions = 0
        self.improvement_rate = 0.0
        self.baseline_accuracy = 0.0
        self.current_accuracy = 0.0
        
        # Self-training data
        self.synthetic_conversations = []
        self.quality_threshold = 0.8
        self.training_interval = 300  # 5 minutes
        
        # Performance tracking
        self.accuracy_history = []
        self.conversation_quality_scores = []
        
        # Training scenarios
        self.training_scenarios = self.generate_training_scenarios()
        
        print("🤖 Autonomous Training System initialized")
    
    def generate_training_scenarios(self) -> List[Dict]:
        """Generate diverse training scenarios for self-improvement"""
        scenarios = [
            # Basic crypto knowledge
            {
                "category": "crypto_basics",
                "questions": [
                    "What is Bitcoin?",
                    "How does blockchain work?",
                    "What is cryptocurrency mining?",
                    "Explain DeFi to me",
                    "What are smart contracts?",
                    "How do crypto wallets work?",
                    "What is proof of stake?",
                    "What are NFTs?",
                ],
                "expected_quality": 0.9
            },
            
            # Investment advice
            {
                "category": "investment",
                "questions": [
                    "Should I invest in Bitcoin?",
                    "How do I start crypto trading?",
                    "What's a good crypto portfolio?",
                    "When should I buy crypto?",
                    "How to avoid crypto scams?",
                    "What are the risks of crypto?",
                    "Best crypto exchange for beginners?",
                    "How to do technical analysis?",
                ],
                "expected_quality": 0.85
            },
            
            # Technical discussions
            {
                "category": "technical",
                "questions": [
                    "Explain blockchain consensus mechanisms",
                    "How does Ethereum 2.0 work?",
                    "What is layer 2 scaling?",
                    "How do atomic swaps work?",
                    "Explain lightning network",
                    "What is sharding in blockchain?",
                    "How do cross-chain bridges work?",
                    "What is zero knowledge proof?",
                ],
                "expected_quality": 0.8
            },
            
            # Market analysis
            {
                "category": "market_analysis",
                "questions": [
                    "Why is Bitcoin price falling?",
                    "What affects crypto market trends?",
                    "How to read crypto charts?",
                    "What is market sentiment analysis?",
                    "Explain crypto market cycles",
                    "What drives altcoin prices?",
                    "How do regulations affect crypto?",
                    "What is institutional adoption?",
                ],
                "expected_quality": 0.85
            },
            
            # Casual conversation
            {
                "category": "casual",
                "questions": [
                    "Hello, how are you?",
                    "What's your opinion on crypto?",
                    "Thanks for your help!",
                    "Have a good day!",
                    "Can you help me?",
                    "What do you think about that?",
                    "That's interesting",
                    "I'm new to crypto",
                ],
                "expected_quality": 0.75
            }
        ]
        
        return scenarios
    
    def start_autonomous_training(self):
        """Start the autonomous training loop"""
        if self.training_active:
            print("⚠️ Training is already active")
            return
        
        self.training_active = True
        self.training_thread = threading.Thread(target=self._training_loop, daemon=True)
        self.training_thread.start()
        
        print("🚀 Autonomous training started!")
        print(f"   Training interval: {self.training_interval} seconds")
        print(f"   Quality threshold: {self.quality_threshold}")
    
    def stop_autonomous_training(self):
        """Stop the autonomous training loop"""
        self.training_active = False
        if self.training_thread:
            self.training_thread.join(timeout=5)
        
        print("⏹️ Autonomous training stopped")
    
    def _training_loop(self):
        """Main training loop that runs continuously"""
        print("🔄 Training loop started...")
        
        while self.training_active:
            try:
                # Measure baseline if this is the first iteration
                if self.training_sessions == 0:
                    self.baseline_accuracy = self._measure_accuracy()
                    self.current_accuracy = self.baseline_accuracy
                    print(f"📊 Baseline accuracy established: {self.baseline_accuracy:.2f}%")
                
                # Run a training session
                self._run_training_session()
                
                # Wait for next training cycle
                time.sleep(self.training_interval)
                
            except Exception as e:
                print(f"❌ Error in training loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _run_training_session(self):
        """Run a single training session"""
        session_start = datetime.now()
        print(f"\n🎓 Training Session {self.training_sessions + 1} - {session_start.strftime('%H:%M:%S')}")
        
        # Select random scenarios for this session
        selected_scenarios = random.sample(self.training_scenarios, 3)
        session_improvements = []
        
        for scenario in selected_scenarios:
            category = scenario['category']
            questions = random.sample(scenario['questions'], min(3, len(scenario['questions'])))
            expected_quality = scenario['expected_quality']
            
            print(f"   Training on: {category}")
            
            for question in questions:
                # Test both personalities
                for personality in ['normal', 'subzero']:
                    # Switch personality
                    self.chatbot.switch_personality(personality)
                    
                    # Get response
                    response = self.chatbot.get_response(question)
                    
                    # Evaluate response quality
                    quality_score = self._evaluate_response_quality(
                        question, response['message'], expected_quality
                    )
                    
                    self.conversation_quality_scores.append(quality_score)
                    
                    # If quality is below threshold, attempt improvement
                    if quality_score < self.quality_threshold:
                        improvement = self._attempt_improvement(
                            question, response['message'], personality, expected_quality
                        )
                        if improvement:
                            session_improvements.append(improvement)
        
        # Measure current accuracy
        new_accuracy = self._measure_accuracy()
        accuracy_change = new_accuracy - self.current_accuracy
        self.current_accuracy = new_accuracy
        self.accuracy_history.append({
            'session': self.training_sessions + 1,
            'accuracy': new_accuracy,
            'timestamp': session_start.isoformat(),
            'improvements': len(session_improvements)
        })
        
        # Update improvement rate
        if self.baseline_accuracy > 0:
            self.improvement_rate = ((self.current_accuracy - self.baseline_accuracy) / self.baseline_accuracy) * 100
        
        # Log session results
        print(f"   ✅ Session completed in {(datetime.now() - session_start).seconds}s")
        print(f"   📈 Accuracy: {self.current_accuracy:.2f}% (Δ {accuracy_change:+.2f}%)")
        print(f"   🔧 Improvements made: {len(session_improvements)}")
        print(f"   📊 Overall improvement: {self.improvement_rate:+.2f}%")
        
        self.training_sessions += 1
        
        # Save progress periodically
        if self.training_sessions % 5 == 0:
            self._save_training_progress()
    
    def _evaluate_response_quality(self, question: str, response: str, expected_quality: float) -> float:
        """Evaluate the quality of a response"""
        if not response or len(response) < 10:
            return 0.1
        
        score = 0.5  # Base score
        
        # Length appropriateness (not too short, not too long)
        if 30 <= len(response) <= 300:
            score += 0.1
        
        # Relevance to crypto (if question is crypto-related)
        crypto_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'trading', 'investment']
        question_has_crypto = any(keyword in question.lower() for keyword in crypto_keywords)
        response_has_crypto = any(keyword in response.lower() for keyword in crypto_keywords)
        
        if question_has_crypto and response_has_crypto:
            score += 0.2
        elif not question_has_crypto:  # Non-crypto questions don't need crypto keywords
            score += 0.1
        
        # Information density
        words = len(response.split())
        if words >= 15:
            score += 0.1
        
        # Helpful indicators
        helpful_phrases = ['help', 'explain', 'understand', 'learn', 'here', 'important', 'consider']
        if any(phrase in response.lower() for phrase in helpful_phrases):
            score += 0.1
        
        # Avoid non-responses
        bad_phrases = ["i don't know", "not sure", "can't help", "don't understand"]
        if any(phrase in response.lower() for phrase in bad_phrases):
            score -= 0.3
        
        return min(max(score, 0.0), 1.0)
    
    def _attempt_improvement(self, question: str, response: str, personality: str, expected_quality: float) -> Optional[Dict]:
        """Attempt to improve a low-quality response"""
        
        # Generate alternative responses by rephrasing the question
        alternative_questions = self._generate_question_variations(question)
        
        best_response = response
        best_quality = self._evaluate_response_quality(question, response, expected_quality)
        
        for alt_question in alternative_questions:
            alt_response = self.chatbot.get_response(alt_question)
            alt_quality = self._evaluate_response_quality(question, alt_response['message'], expected_quality)
            
            if alt_quality > best_quality:
                best_response = alt_response['message']
                best_quality = alt_quality
        
        # If we found a better response, record it for learning
        if best_quality > self._evaluate_response_quality(question, response, expected_quality) + 0.1:
            improvement = {
                'original_question': question,
                'original_response': response,
                'improved_response': best_response,
                'quality_improvement': best_quality - self._evaluate_response_quality(question, response, expected_quality),
                'personality': personality,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add to synthetic training data
            self.synthetic_conversations.append({
                'user': question,
                'bot': best_response,
                'quality_score': best_quality,
                'source': 'autonomous_training'
            })
            
            # Update the trainer if possible
            if hasattr(self.chatbot.normal_trainer, 'add_dynamic_conversation'):
                self.chatbot.normal_trainer.add_dynamic_conversation(
                    question, best_response, best_quality
                )
            
            return improvement
        
        return None
    
    def _generate_question_variations(self, question: str) -> List[str]:
        """Generate variations of a question to find better responses"""
        variations = []
        
        # Simple rephrasings
        rephrase_patterns = [
            ("What is", "Can you explain"),
            ("How does", "How do you"),
            ("Tell me about", "What can you tell me about"),
            ("Explain", "Can you explain"),
            ("?", " please?"),
        ]
        
        for old, new in rephrase_patterns:
            if old in question:
                variations.append(question.replace(old, new))
        
        # Add context
        context_additions = [
            f"As a beginner, {question.lower()}",
            f"Can you help me understand {question.lower()}",
            f"I'm curious about {question.lower()}",
        ]
        
        variations.extend(context_additions[:2])  # Limit variations
        
        return variations[:3]  # Return max 3 variations
    
    def _measure_accuracy(self) -> float:
        """Measure current system accuracy"""
        if not self.conversation_quality_scores:
            return 0.0
        
        # Use recent scores (last 50 interactions)
        recent_scores = self.conversation_quality_scores[-50:]
        return (sum(recent_scores) / len(recent_scores)) * 100
    
    def _save_training_progress(self):
        """Save training progress to file"""
        progress_data = {
            'training_sessions': self.training_sessions,
            'baseline_accuracy': self.baseline_accuracy,
            'current_accuracy': self.current_accuracy,
            'improvement_rate': self.improvement_rate,
            'accuracy_history': self.accuracy_history,
            'synthetic_conversations': len(self.synthetic_conversations),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open('autonomous_training_progress.json', 'w') as f:
                json.dump(progress_data, f, indent=2)
            print(f"💾 Training progress saved ({self.training_sessions} sessions)")
        except Exception as e:
            print(f"⚠️ Error saving progress: {e}")
    
    def get_training_status(self) -> Dict:
        """Get current training status"""
        return {
            'active': self.training_active,
            'sessions_completed': self.training_sessions,
            'baseline_accuracy': round(self.baseline_accuracy, 2),
            'current_accuracy': round(self.current_accuracy, 2),
            'improvement_rate': round(self.improvement_rate, 2),
            'synthetic_conversations': len(self.synthetic_conversations),
            'avg_quality_score': round(
                sum(self.conversation_quality_scores[-20:]) / len(self.conversation_quality_scores[-20:]) 
                if self.conversation_quality_scores else 0, 2
            ),
            'training_interval': self.training_interval
        }
    
    def get_improvement_recommendations(self) -> List[str]:
        """Get recommendations for improvement"""
        recommendations = []
        
        if self.current_accuracy < 70:
            recommendations.append("Consider expanding the training dataset with more diverse conversations")
        
        if self.improvement_rate < 5 and self.training_sessions > 10:
            recommendations.append("Training plateau detected - consider adjusting training parameters")
        
        if len(self.synthetic_conversations) < 50:
            recommendations.append("Generate more synthetic training data for edge cases")
        
        recent_quality = sum(self.conversation_quality_scores[-10:]) / max(len(self.conversation_quality_scores[-10:]), 1)
        if recent_quality < 0.7:
            recommendations.append("Recent response quality is low - focus on improving response generation")
        
        if not recommendations:
            recommendations.append("Training system is performing well - continue current approach")
        
        return recommendations
    
    def record_interaction(self, user_input: str, bot_response: str, confidence: float, response_type: str, personality: str):
        """Record an interaction for training analysis"""
        interaction = {
            'timestamp': time.time(),
            'user_input': user_input,
            'bot_response': bot_response,
            'confidence': confidence,
            'response_type': response_type,
            'personality': personality
        }
        
        # Store for later analysis
        if not hasattr(self, 'recorded_interactions'):
            self.recorded_interactions = []
        
        self.recorded_interactions.append(interaction)
        
        # Keep only recent interactions to avoid memory issues
        if len(self.recorded_interactions) > 1000:
            self.recorded_interactions = self.recorded_interactions[-500:]
        
        # Update quality scores
        self.conversation_quality_scores.append(confidence)
        if len(self.conversation_quality_scores) > 100:
            self.conversation_quality_scores = self.conversation_quality_scores[-50:]

def main():
    """Demo of autonomous training system"""
    print("🤖 Autonomous Training System Demo")
    print("=" * 50)
    
    # Initialize chatbot and training system
    chatbot = ImprovedDualPersonalityChatbot()
    trainer = AutonomousTrainingSystem(chatbot)
    
    # Show initial status
    print("\n📊 Initial Status:")
    status = trainer.get_training_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Start training for a short demo
    print("\n🚀 Starting autonomous training (demo mode)...")
    trainer.training_interval = 30  # Faster for demo
    trainer.start_autonomous_training()
    
    try:
        # Let it train for a few minutes
        for i in range(6):  # 3 minutes of training
            time.sleep(30)
            status = trainer.get_training_status()
            print(f"\n📈 Progress Update {i+1}:")
            print(f"   Sessions: {status['sessions_completed']}")
            print(f"   Current accuracy: {status['current_accuracy']}%")
            print(f"   Improvement: {status['improvement_rate']:+.1f}%")
            
            if i == 2:  # Show recommendations halfway
                recommendations = trainer.get_improvement_recommendations()
                print("💡 Recommendations:")
                for rec in recommendations:
                    print(f"   - {rec}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
    
    finally:
        trainer.stop_autonomous_training()
    
    # Final status
    print("\n📊 Final Status:")
    final_status = trainer.get_training_status()
    for key, value in final_status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Autonomous training demo completed!")

if __name__ == "__main__":
    main()
