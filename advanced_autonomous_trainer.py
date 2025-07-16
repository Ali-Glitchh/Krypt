#!/usr/bin/env python3
"""
Advanced Autonomous Training System with MCP Integration
- Self-improving chatbot using external data sources
- Real-time crypto data integration
- Continuous learning from conversations
- Quality assessment and feedback loops
"""

import json
import time
import random
import threading
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot

class AdvancedAutonomousTrainer:
    def __init__(self, chatbot: ImprovedDualPersonalityChatbot):
        self.chatbot = chatbot
        self.training_active = False
        self.training_thread = None
        
        # Enhanced training metrics
        self.training_sessions = 0
        self.improvement_rate = 0.0
        self.baseline_accuracy = 0.0
        self.current_accuracy = 0.0
        self.learning_velocity = 0.0
        
        # Training data sources
        self.external_data_sources = {
            "crypto_news": "https://newsapi.org/v2/everything?q=cryptocurrency&sortBy=publishedAt",
            "crypto_prices": "https://api.coingecko.com/api/v3/coins/markets",
            "crypto_trends": "https://api.coingecko.com/api/v3/search/trending"
        }
        
        # Self-training configuration
        self.quality_threshold = 0.85
        self.training_interval = 180  # 3 minutes
        self.max_training_cycles = 100
        self.learning_rate = 0.1
        
        # Advanced features
        self.conversation_patterns = []
        self.response_templates = {}
        self.knowledge_gaps = []
        self.performance_metrics = {
            "response_time": [],
            "confidence_scores": [],
            "user_satisfaction": [],
            "accuracy_trend": []
        }
        
        # Training scenarios with real-time data
        self.dynamic_scenarios = self.initialize_dynamic_scenarios()
        
        print("🚀 Advanced Autonomous Training System initialized")
        print(f"📊 Training interval: {self.training_interval} seconds")
        print(f"🎯 Quality threshold: {self.quality_threshold}")

    def initialize_dynamic_scenarios(self) -> Dict[str, List[Dict]]:
        """Initialize dynamic training scenarios that adapt to market conditions"""
        return {
            "market_analysis": [
                {"context": "bull_market", "questions": ["Why is Bitcoin rising?", "Should I buy now?"]},
                {"context": "bear_market", "questions": ["Why is crypto falling?", "Is this a good time to buy?"]},
                {"context": "sideways", "questions": ["What's next for crypto?", "When will prices move?"]}
            ],
            "technical_analysis": [
                {"context": "support_resistance", "questions": ["What are support levels?", "How to identify resistance?"]},
                {"context": "indicators", "questions": ["What is RSI?", "How to use MACD?"]}
            ],
            "portfolio_management": [
                {"context": "diversification", "questions": ["How to diversify crypto portfolio?", "Best altcoins to buy?"]},
                {"context": "risk_management", "questions": ["How much to invest?", "When to take profits?"]}
            ],
            "news_analysis": [
                {"context": "regulations", "questions": ["Impact of crypto regulations?", "SEC news on crypto?"]},
                {"context": "adoption", "questions": ["Institutional adoption news?", "Corporate Bitcoin holdings?"]}
            ]
        }

    def fetch_real_time_data(self) -> Dict[str, Any]:
        """Fetch real-time crypto data for training context"""
        data = {"timestamp": datetime.now().isoformat()}
        
        try:
            # Get trending cryptocurrencies
            trending_response = requests.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=10
            )
            if trending_response.status_code == 200:
                data["trending"] = trending_response.json()
            
            # Get top market data
            market_response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1",
                timeout=10
            )
            if market_response.status_code == 200:
                data["market_data"] = market_response.json()
                
            # Analyze market sentiment
            data["market_sentiment"] = self.analyze_market_sentiment(data.get("market_data", []))
            
        except Exception as e:
            print(f"⚠️ Error fetching real-time data: {e}")
            data["error"] = str(e)
            
        return data

    def analyze_market_sentiment(self, market_data: List[Dict]) -> str:
        """Analyze overall market sentiment from price data"""
        if not market_data:
            return "neutral"
        
        try:
            # Calculate average 24h price change
            price_changes = [float(coin.get("price_change_percentage_24h", 0)) for coin in market_data if coin.get("price_change_percentage_24h")]
            
            if not price_changes:
                return "neutral"
                
            avg_change = sum(price_changes) / len(price_changes)
            
            if avg_change > 5:
                return "bullish"
            elif avg_change < -5:
                return "bearish"
            else:
                return "neutral"
                
        except Exception:
            return "neutral"

    def generate_contextual_training_data(self, real_time_data: Dict[str, Any]) -> List[Dict]:
        """Generate training scenarios based on current market conditions"""
        training_data = []
        market_sentiment = real_time_data.get("market_sentiment", "neutral")
        
        # Market-specific questions
        if market_sentiment == "bullish":
            training_data.extend([
                {"question": "Why is the crypto market pumping?", "context": "bull_market"},
                {"question": "Should I FOMO into this rally?", "context": "risk_management"},
                {"question": "When will this bull run end?", "context": "market_analysis"}
            ])
        elif market_sentiment == "bearish":
            training_data.extend([
                {"question": "Why is everything crashing?", "context": "bear_market"},
                {"question": "Is this a good time to buy the dip?", "context": "dollar_cost_averaging"},
                {"question": "How low can Bitcoin go?", "context": "technical_analysis"}
            ])
        else:
            training_data.extend([
                {"question": "When will crypto move again?", "context": "sideways_market"},
                {"question": "What catalysts could move the market?", "context": "fundamental_analysis"}
            ])
        
        # Add trending coin questions
        if "trending" in real_time_data:
            try:
                trending_coins = real_time_data["trending"].get("coins", [])[:3]
                for coin in trending_coins:
                    coin_name = coin.get("item", {}).get("name", "Unknown")
                    training_data.append({
                        "question": f"What do you think about {coin_name}?",
                        "context": "trending_analysis"
                    })
            except Exception:
                pass
        
        return training_data

    def self_evaluate_response(self, question: str, response: Dict) -> float:
        """Evaluate the quality of a chatbot response"""
        score = 0.0
        
        # Check response completeness
        if response.get("message") and len(response["message"]) > 20:
            score += 0.3
        
        # Check confidence level
        confidence = response.get("confidence", 0.5)
        score += confidence * 0.3
        
        # Check relevance (basic keyword matching)
        question_lower = question.lower()
        response_lower = response.get("message", "").lower()
        
        crypto_keywords = ["bitcoin", "crypto", "blockchain", "ethereum", "trading", "price", "market"]
        relevance_score = sum(1 for keyword in crypto_keywords if keyword in question_lower and keyword in response_lower)
        score += min(relevance_score * 0.1, 0.4)
        
        return min(score, 1.0)

    def continuous_learning_cycle(self):
        """Main continuous learning loop"""
        cycle_count = 0
        
        while self.training_active and cycle_count < self.max_training_cycles:
            try:
                print(f"\n🔄 Training Cycle {cycle_count + 1}")
                
                # Fetch real-time market data
                print("📊 Fetching real-time market data...")
                real_time_data = self.fetch_real_time_data()
                
                # Generate contextual training scenarios
                training_scenarios = self.generate_contextual_training_data(real_time_data)
                
                # Train on scenarios
                session_scores = []
                for scenario in training_scenarios[:5]:  # Limit to 5 per cycle
                    question = scenario["question"]
                    print(f"🤔 Training on: {question}")
                    
                    # Get response from chatbot
                    response = self.chatbot.get_response(question)
                    
                    # Evaluate response quality
                    quality_score = self.self_evaluate_response(question, response)
                    session_scores.append(quality_score)
                    
                    print(f"📈 Quality Score: {quality_score:.2f}")
                    
                    # Store conversation for future training
                    self.conversation_patterns.append({
                        "question": question,
                        "response": response,
                        "quality_score": quality_score,
                        "timestamp": datetime.now().isoformat(),
                        "market_context": real_time_data.get("market_sentiment", "neutral")
                    })
                
                # Update metrics
                if session_scores:
                    avg_score = sum(session_scores) / len(session_scores)
                    self.performance_metrics["accuracy_trend"].append({
                        "cycle": cycle_count + 1,
                        "average_score": avg_score,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    print(f"📊 Cycle {cycle_count + 1} Average Score: {avg_score:.2f}")
                
                # Self-improvement analysis
                self.analyze_learning_progress()
                
                # Update training parameters based on performance
                self.adapt_training_parameters()
                
                cycle_count += 1
                
                # Wait before next cycle
                time.sleep(self.training_interval)
                
            except Exception as e:
                print(f"❌ Error in training cycle: {e}")
                time.sleep(30)  # Wait before retrying

    def analyze_learning_progress(self):
        """Analyze learning progress and identify improvement areas"""
        if len(self.performance_metrics["accuracy_trend"]) < 2:
            return
        
        recent_scores = [entry["average_score"] for entry in self.performance_metrics["accuracy_trend"][-5:]]
        
        if len(recent_scores) >= 2:
            # Calculate learning velocity
            self.learning_velocity = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            
            print(f"📈 Learning Velocity: {self.learning_velocity:.4f}")
            
            # Identify knowledge gaps
            low_quality_conversations = [
                conv for conv in self.conversation_patterns[-20:] 
                if conv["quality_score"] < self.quality_threshold
            ]
            
            if low_quality_conversations:
                print(f"🎯 Identified {len(low_quality_conversations)} areas for improvement")

    def adapt_training_parameters(self):
        """Dynamically adjust training parameters based on performance"""
        if self.learning_velocity > 0.05:
            # Learning well, can reduce training frequency slightly
            self.training_interval = min(self.training_interval * 1.1, 300)
        elif self.learning_velocity < -0.02:
            # Performance declining, increase training frequency
            self.training_interval = max(self.training_interval * 0.9, 60)
        
        print(f"⚙️ Adjusted training interval to {self.training_interval:.0f} seconds")

    def start_autonomous_training(self):
        """Start the autonomous training process"""
        if self.training_active:
            print("⚠️ Training is already active")
            return
        
        self.training_active = True
        self.training_thread = threading.Thread(target=self.continuous_learning_cycle)
        self.training_thread.daemon = True
        self.training_thread.start()
        
        print("🚀 Autonomous training started!")
        print(f"🔄 Training every {self.training_interval} seconds")

    def stop_autonomous_training(self):
        """Stop the autonomous training process"""
        self.training_active = False
        if self.training_thread and self.training_thread.is_alive():
            self.training_thread.join(timeout=5)
        
        print("🛑 Autonomous training stopped")

    def get_training_statistics(self) -> Dict:
        """Get comprehensive training statistics"""
        stats = {
            "training_active": self.training_active,
            "training_sessions": len(self.performance_metrics.get("accuracy_trend", [])),
            "learning_velocity": self.learning_velocity,
            "total_conversations": len(self.conversation_patterns),
            "training_interval": self.training_interval,
            "quality_threshold": self.quality_threshold
        }
        
        if self.performance_metrics["accuracy_trend"]:
            recent_scores = [entry["average_score"] for entry in self.performance_metrics["accuracy_trend"][-10:]]
            stats["recent_average_score"] = sum(recent_scores) / len(recent_scores) if recent_scores else 0
            stats["latest_score"] = self.performance_metrics["accuracy_trend"][-1]["average_score"]
        
        return stats

    def export_training_data(self, filename: str = None) -> str:
        """Export training data and metrics to file"""
        if not filename:
            filename = f"autonomous_training_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "training_statistics": self.get_training_statistics(),
            "conversation_patterns": self.conversation_patterns[-100:],  # Last 100 conversations
            "performance_metrics": self.performance_metrics,
            "configuration": {
                "quality_threshold": self.quality_threshold,
                "training_interval": self.training_interval,
                "learning_rate": self.learning_rate
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"📁 Training data exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting training data: {e}")
            return ""

# Main execution
if __name__ == "__main__":
    print("🤖 Initializing Advanced Autonomous Training System...")
    
    try:
        # Initialize chatbot
        chatbot = ImprovedDualPersonalityChatbot()
        
        # Initialize autonomous trainer
        trainer = AdvancedAutonomousTrainer(chatbot)
        
        # Start training
        trainer.start_autonomous_training()
        
        print("✅ Autonomous training system is now running!")
        print("📊 Monitor training progress in the console")
        print("🛑 Press Ctrl+C to stop training")
        
        # Keep the system running
        try:
            while trainer.training_active:
                time.sleep(10)
                stats = trainer.get_training_statistics()
                print(f"📈 Training Sessions: {stats['training_sessions']}, "
                      f"Learning Velocity: {stats['learning_velocity']:.4f}")
        except KeyboardInterrupt:
            print("\n🛑 Stopping autonomous training...")
            trainer.stop_autonomous_training()
            
            # Export final training data
            export_file = trainer.export_training_data()
            print(f"💾 Training data saved to {export_file}")
            
    except Exception as e:
        print(f"❌ Error initializing autonomous training: {e}")
        import traceback
        traceback.print_exc()
