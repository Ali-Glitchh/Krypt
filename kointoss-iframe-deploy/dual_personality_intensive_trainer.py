#!/usr/bin/env python3
"""
Enhanced Dual-Personality Autonomous Trainer
- Specialized training for both Normal and Sub-Zero personalities
- Comparative learning between personalities
- Advanced conversation pattern analysis
- Cross-personality knowledge transfer
- Enhanced quality metrics for each personality
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

class DualPersonalityAdvancedTrainer:
    def __init__(self, chatbot: ImprovedDualPersonalityChatbot):
        self.chatbot = chatbot
        self.training_active = False
        self.training_thread = None
        
        # Enhanced metrics for both personalities
        self.personality_metrics = {
            "normal": {
                "training_sessions": 0,
                "improvement_rate": 0.0,
                "average_confidence": 0.0,
                "conversation_quality": [],
                "response_patterns": [],
                "learning_velocity": 0.0,
                "specialization_score": 0.0
            },
            "subzero": {
                "training_sessions": 0,
                "improvement_rate": 0.0,
                "average_confidence": 0.0,
                "conversation_quality": [],
                "response_patterns": [],
                "learning_velocity": 0.0,
                "specialization_score": 0.0
            }
        }
        
        # Cross-personality learning
        self.cross_personality_insights = []
        self.personality_comparison_data = []
        
        # Enhanced training scenarios for each personality
        self.normal_scenarios = self.create_normal_personality_scenarios()
        self.subzero_scenarios = self.create_subzero_personality_scenarios()
        self.shared_scenarios = self.create_shared_scenarios()
        
        # Advanced training configuration
        self.training_interval = 120  # 2 minutes for intensive training
        self.quality_threshold = 0.80
        self.cross_training_ratio = 0.3  # 30% cross-personality training
        
        print("🎭 Enhanced Dual-Personality Training System initialized")
        print(f"🤖 Normal personality scenarios: {len(self.normal_scenarios)}")
        print(f"🧊 Sub-Zero personality scenarios: {len(self.subzero_scenarios)}")
        print(f"🔄 Shared scenarios: {len(self.shared_scenarios)}")

    def create_normal_personality_scenarios(self) -> List[Dict]:
        """Create training scenarios specifically for the normal personality"""
        return [
            {
                "category": "educational",
                "questions": [
                    "Can you explain blockchain technology in simple terms?",
                    "What are the benefits of cryptocurrency?",
                    "How does Bitcoin mining work?",
                    "What is DeFi and why is it important?",
                    "Can you help me understand smart contracts?"
                ],
                "expected_tone": "helpful, educational, encouraging"
            },
            {
                "category": "market_analysis",
                "questions": [
                    "What factors affect cryptocurrency prices?",
                    "How do I analyze crypto market trends?",
                    "What should I look for when researching altcoins?",
                    "How do regulations impact crypto markets?",
                    "What are the key indicators for crypto investing?"
                ],
                "expected_tone": "analytical, informative, balanced"
            },
            {
                "category": "beginner_friendly",
                "questions": [
                    "I'm new to crypto, where should I start?",
                    "What's the safest way to buy cryptocurrency?",
                    "How do I store my crypto securely?",
                    "What are the risks I should know about?",
                    "Can you recommend some beginner resources?"
                ],
                "expected_tone": "patient, supportive, encouraging"
            },
            {
                "category": "portfolio_guidance",
                "questions": [
                    "How should I diversify my crypto portfolio?",
                    "What percentage of my investment should be in crypto?",
                    "When is a good time to take profits?",
                    "How do I manage risk in crypto investing?",
                    "Should I dollar-cost average into crypto?"
                ],
                "expected_tone": "responsible, cautious, practical"
            }
        ]

    def create_subzero_personality_scenarios(self) -> List[Dict]:
        """Create training scenarios specifically for the Sub-Zero personality"""
        return [
            {
                "category": "aggressive_analysis",
                "questions": [
                    "Which crypto will dominate the market?",
                    "What's your take on the next crypto revolution?",
                    "Which altcoin has the most potential for massive gains?",
                    "How will crypto change the financial world?",
                    "What's the boldest crypto prediction you can make?"
                ],
                "expected_tone": "confident, bold, assertive"
            },
            {
                "category": "market_disruption",
                "questions": [
                    "How will crypto disrupt traditional banking?",
                    "Which industry will crypto transform next?",
                    "What's the most undervalued crypto right now?",
                    "How will CBDCs affect the crypto market?",
                    "What's the future of decentralized finance?"
                ],
                "expected_tone": "revolutionary, visionary, intense"
            },
            {
                "category": "technical_mastery",
                "questions": [
                    "What's the most advanced blockchain technology?",
                    "How will quantum computing affect crypto security?",
                    "What's the next evolution in consensus mechanisms?",
                    "Which layer-2 solution will win the scaling wars?",
                    "How will AI integrate with blockchain technology?"
                ],
                "expected_tone": "technical, authoritative, cutting-edge"
            },
            {
                "category": "market_psychology",
                "questions": [
                    "Why do most crypto traders lose money?",
                    "How do you identify market manipulation?",
                    "What drives crypto market cycles?",
                    "How do whales manipulate crypto prices?",
                    "What's the psychology behind crypto FOMO?"
                ],
                "expected_tone": "strategic, psychological, insightful"
            }
        ]

    def create_shared_scenarios(self) -> List[Dict]:
        """Create scenarios both personalities should handle well"""
        return [
            {
                "category": "price_analysis",
                "questions": [
                    "What's your analysis of Bitcoin's current price?",
                    "Where do you see Ethereum heading?",
                    "What are your thoughts on the current market sentiment?",
                    "How do you interpret today's crypto news?",
                    "What's driving the current market movement?"
                ]
            },
            {
                "category": "news_reaction",
                "questions": [
                    "What's your take on the latest crypto regulations?",
                    "How will institutional adoption affect prices?",
                    "What impact will the next Bitcoin halving have?",
                    "How do you view the current macro environment for crypto?",
                    "What's your reaction to recent crypto developments?"
                ]
            }
        ]

    def fetch_enhanced_market_data(self) -> Dict[str, Any]:
        """Fetch comprehensive market data for personality-specific training"""
        data = {"timestamp": datetime.now().isoformat()}
        
        try:
            # Get trending cryptocurrencies
            trending_response = requests.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=10
            )
            if trending_response.status_code == 200:
                trending_data = trending_response.json()
                data["trending"] = trending_data
                
                # Extract trending coins for personality-specific questions
                trending_coins = [coin["item"]["name"] for coin in trending_data.get("coins", [])[:5]]
                data["trending_names"] = trending_coins
            
            # Get detailed market data
            market_response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1",
                timeout=10
            )
            if market_response.status_code == 200:
                market_data = market_response.json()
                data["market_data"] = market_data
                
                # Analyze market conditions for personality-specific training
                data["market_analysis"] = self.analyze_market_conditions(market_data)
            
            # Get fear and greed index (if available)
            try:
                fear_greed_response = requests.get(
                    "https://api.alternative.me/fng/?limit=1",
                    timeout=5
                )
                if fear_greed_response.status_code == 200:
                    data["fear_greed"] = fear_greed_response.json()
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Error fetching enhanced market data: {e}")
            data["error"] = str(e)
            
        return data

    def analyze_market_conditions(self, market_data: List[Dict]) -> Dict[str, Any]:
        """Analyze market conditions for personality-specific training"""
        analysis = {}
        
        try:
            if not market_data:
                return analysis
            
            # Calculate market metrics
            price_changes_24h = [float(coin.get("price_change_percentage_24h", 0)) for coin in market_data]
            price_changes_7d = [float(coin.get("price_change_percentage_7d", 0)) for coin in market_data]
            
            analysis["avg_24h_change"] = sum(price_changes_24h) / len(price_changes_24h)
            analysis["avg_7d_change"] = sum(price_changes_7d) / len(price_changes_7d)
            
            # Determine market sentiment
            if analysis["avg_24h_change"] > 5:
                analysis["sentiment"] = "strongly_bullish"
            elif analysis["avg_24h_change"] > 2:
                analysis["sentiment"] = "bullish"
            elif analysis["avg_24h_change"] < -5:
                analysis["sentiment"] = "strongly_bearish"
            elif analysis["avg_24h_change"] < -2:
                analysis["sentiment"] = "bearish"
            else:
                analysis["sentiment"] = "neutral"
            
            # Market volatility
            volatility = np.std(price_changes_24h) if price_changes_24h else 0
            analysis["volatility"] = volatility
            analysis["volatility_level"] = "high" if volatility > 10 else "medium" if volatility > 5 else "low"
            
            # Top performers and losers
            sorted_by_change = sorted(market_data, key=lambda x: float(x.get("price_change_percentage_24h", 0)), reverse=True)
            analysis["top_performer"] = sorted_by_change[0].get("name", "Unknown") if sorted_by_change else None
            analysis["biggest_loser"] = sorted_by_change[-1].get("name", "Unknown") if sorted_by_change else None
            
        except Exception as e:
            print(f"⚠️ Error analyzing market conditions: {e}")
            
        return analysis

    def generate_personality_specific_training(self, personality: str, market_data: Dict[str, Any]) -> List[Dict]:
        """Generate training scenarios specific to each personality"""
        training_data = []
        market_analysis = market_data.get("market_analysis", {})
        sentiment = market_analysis.get("sentiment", "neutral")
        
        if personality == "normal":
            # Normal personality: Educational, helpful, balanced
            if sentiment in ["strongly_bullish", "bullish"]:
                training_data.extend([
                    {"question": "The market is rising, should I invest more?", "context": "risk_management"},
                    {"question": "How can I take advantage of this bull market safely?", "context": "portfolio_strategy"},
                    {"question": "What are the risks of investing during a rally?", "context": "education"}
                ])
            elif sentiment in ["strongly_bearish", "bearish"]:
                training_data.extend([
                    {"question": "The market is falling, should I sell?", "context": "emotional_support"},
                    {"question": "How can I protect my portfolio during a downturn?", "context": "risk_management"},
                    {"question": "Is this a good time to buy the dip?", "context": "strategy_guidance"}
                ])
            
            # Add trending coin questions with educational focus
            if "trending_names" in market_data:
                for coin in market_data["trending_names"][:2]:
                    training_data.append({
                        "question": f"Can you explain what {coin} is and its use case?",
                        "context": "education"
                    })
        
        elif personality == "subzero":
            # Sub-Zero personality: Bold, confident, aggressive
            if sentiment in ["strongly_bullish", "bullish"]:
                training_data.extend([
                    {"question": "Which crypto will lead this bull run?", "context": "market_prediction"},
                    {"question": "How high can Bitcoin go this cycle?", "context": "price_target"},
                    {"question": "What's the most aggressive play in this market?", "context": "high_risk_strategy"}
                ])
            elif sentiment in ["strongly_bearish", "bearish"]:
                training_data.extend([
                    {"question": "Is this the bottom or will it crash further?", "context": "market_timing"},
                    {"question": "Which altcoins will survive this bear market?", "context": "survival_analysis"},
                    {"question": "How do you profit in a falling market?", "context": "advanced_strategy"}
                ])
            
            # Add trending coin questions with aggressive analysis
            if "trending_names" in market_data:
                for coin in market_data["trending_names"][:2]:
                    training_data.append({
                        "question": f"{coin} is trending - is this the next moonshot?",
                        "context": "aggressive_analysis"
                    })
        
        return training_data

    def evaluate_personality_response(self, question: str, response: Dict, expected_personality: str) -> Dict[str, float]:
        """Enhanced evaluation for personality-specific responses"""
        scores = {
            "relevance": 0.0,
            "personality_consistency": 0.0,
            "confidence": 0.0,
            "quality": 0.0,
            "overall": 0.0
        }
        
        message = response.get("message", "").lower()
        personality = response.get("personality", "")
        confidence = response.get("confidence", 0.5)
        
        # Relevance score
        crypto_keywords = ["bitcoin", "crypto", "blockchain", "ethereum", "trading", "price", "market", "defi", "altcoin"]
        relevance_count = sum(1 for keyword in crypto_keywords if keyword in message)
        scores["relevance"] = min(relevance_count * 0.15, 1.0)
        
        # Personality consistency
        if personality == expected_personality:
            scores["personality_consistency"] = 0.5
            
            if expected_personality == "normal":
                # Look for helpful, educational tone
                helpful_words = ["help", "explain", "understand", "learn", "consider", "recommend", "suggest"]
                helpful_count = sum(1 for word in helpful_words if word in message)
                scores["personality_consistency"] += min(helpful_count * 0.1, 0.5)
                
            elif expected_personality == "subzero":
                # Look for bold, confident tone
                bold_words = ["dominate", "revolution", "massive", "bold", "aggressive", "winner", "destroy", "crush"]
                bold_count = sum(1 for word in bold_words if word in message)
                scores["personality_consistency"] += min(bold_count * 0.1, 0.5)
        
        # Confidence score
        scores["confidence"] = confidence
        
        # Quality score (length and complexity)
        if len(message) > 20:
            scores["quality"] = min(len(message) / 200.0, 1.0)
        
        # Overall score
        scores["overall"] = (
            scores["relevance"] * 0.3 +
            scores["personality_consistency"] * 0.3 +
            scores["confidence"] * 0.2 +
            scores["quality"] * 0.2
        )
        
        return scores

    def cross_personality_training_cycle(self):
        """Run comparative training between both personalities"""
        print(f"\n🎭 Cross-Personality Training Cycle")
        
        # Fetch market data
        market_data = self.fetch_enhanced_market_data()
        
        # Select shared scenarios
        shared_questions = random.sample(
            [q for scenario in self.shared_scenarios for q in scenario["questions"]], 
            min(3, len([q for scenario in self.shared_scenarios for q in scenario["questions"]]))
        )
        
        comparison_results = []
        
        for question in shared_questions:
            print(f"🔄 Cross-training on: {question}")
            
            # Get response from normal personality
            self.chatbot.switch_personality("normal")
            normal_response = self.chatbot.get_response(question)
            normal_scores = self.evaluate_personality_response(question, normal_response, "normal")
            
            # Get response from sub-zero personality
            self.chatbot.switch_personality("subzero")
            subzero_response = self.chatbot.get_response(question)
            subzero_scores = self.evaluate_personality_response(question, subzero_response, "subzero")
            
            # Compare responses
            comparison = {
                "question": question,
                "normal_response": normal_response,
                "normal_scores": normal_scores,
                "subzero_response": subzero_response,
                "subzero_scores": subzero_scores,
                "winner": "normal" if normal_scores["overall"] > subzero_scores["overall"] else "subzero",
                "score_difference": abs(normal_scores["overall"] - subzero_scores["overall"]),
                "timestamp": datetime.now().isoformat()
            }
            
            comparison_results.append(comparison)
            
            print(f"   🤖 Normal: {normal_scores['overall']:.2f} | 🧊 Sub-Zero: {subzero_scores['overall']:.2f}")
            print(f"   🏆 Winner: {comparison['winner'].title()}")
        
        self.personality_comparison_data.extend(comparison_results)
        return comparison_results

    def intensive_dual_training_cycle(self):
        """Main intensive training loop for both personalities"""
        cycle_count = 0
        
        while self.training_active:
            try:
                cycle_count += 1
                print(f"\n🎭 Dual-Personality Training Cycle {cycle_count}")
                
                # Fetch market data
                market_data = self.fetch_enhanced_market_data()
                market_analysis = market_data.get("market_analysis", {})
                print(f"📊 Market Sentiment: {market_analysis.get('sentiment', 'unknown').upper()}")
                print(f"📈 24h Change: {market_analysis.get('avg_24h_change', 0):.2f}%")
                
                # Train normal personality
                print("\n🤖 Training Normal Personality...")
                normal_training_data = self.generate_personality_specific_training("normal", market_data)
                normal_session_scores = []
                
                for scenario in normal_training_data[:3]:  # Train on 3 scenarios
                    self.chatbot.switch_personality("normal")
                    response = self.chatbot.get_response(scenario["question"])
                    scores = self.evaluate_personality_response(scenario["question"], response, "normal")
                    normal_session_scores.append(scores["overall"])
                    
                    print(f"   ✅ Q: {scenario['question'][:50]}...")
                    print(f"   📈 Score: {scores['overall']:.2f}")
                
                # Train sub-zero personality
                print("\n🧊 Training Sub-Zero Personality...")
                subzero_training_data = self.generate_personality_specific_training("subzero", market_data)
                subzero_session_scores = []
                
                for scenario in subzero_training_data[:3]:  # Train on 3 scenarios
                    self.chatbot.switch_personality("subzero")
                    response = self.chatbot.get_response(scenario["question"])
                    scores = self.evaluate_personality_response(scenario["question"], response, "subzero")
                    subzero_session_scores.append(scores["overall"])
                    
                    print(f"   ✅ Q: {scenario['question'][:50]}...")
                    print(f"   📈 Score: {scores['overall']:.2f}")
                
                # Cross-personality training (30% of the time)
                if random.random() < self.cross_training_ratio:
                    comparison_results = self.cross_personality_training_cycle()
                
                # Update metrics
                if normal_session_scores:
                    normal_avg = sum(normal_session_scores) / len(normal_session_scores)
                    self.personality_metrics["normal"]["conversation_quality"].append(normal_avg)
                    self.personality_metrics["normal"]["training_sessions"] += 1
                    
                if subzero_session_scores:
                    subzero_avg = sum(subzero_session_scores) / len(subzero_session_scores)
                    self.personality_metrics["subzero"]["conversation_quality"].append(subzero_avg)
                    self.personality_metrics["subzero"]["training_sessions"] += 1
                
                # Calculate learning velocities
                self.calculate_learning_velocities()
                
                # Report progress
                self.report_training_progress(cycle_count)
                
                # Wait before next cycle
                time.sleep(self.training_interval)
                
            except Exception as e:
                print(f"❌ Error in dual training cycle: {e}")
                time.sleep(30)

    def calculate_learning_velocities(self):
        """Calculate learning velocity for both personalities"""
        for personality in ["normal", "subzero"]:
            quality_scores = self.personality_metrics[personality]["conversation_quality"]
            
            if len(quality_scores) >= 2:
                recent_scores = quality_scores[-5:]  # Last 5 scores
                if len(recent_scores) >= 2:
                    velocity = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
                    self.personality_metrics[personality]["learning_velocity"] = velocity

    def report_training_progress(self, cycle_count: int):
        """Report detailed training progress for both personalities"""
        print(f"\n📊 Dual-Personality Training Report - Cycle {cycle_count}")
        print("=" * 60)
        
        for personality in ["normal", "subzero"]:
            metrics = self.personality_metrics[personality]
            icon = "🤖" if personality == "normal" else "🧊"
            
            if metrics["conversation_quality"]:
                recent_avg = sum(metrics["conversation_quality"][-5:]) / len(metrics["conversation_quality"][-5:])
                print(f"{icon} {personality.upper()} Personality:")
                print(f"   • Training Sessions: {metrics['training_sessions']}")
                print(f"   • Recent Avg Score: {recent_avg:.3f}")
                print(f"   • Learning Velocity: {metrics['learning_velocity']:.4f}")
                print(f"   • Total Conversations: {len(metrics['conversation_quality'])}")
        
        # Cross-personality insights
        if self.personality_comparison_data:
            recent_comparisons = self.personality_comparison_data[-10:]
            normal_wins = sum(1 for comp in recent_comparisons if comp["winner"] == "normal")
            subzero_wins = sum(1 for comp in recent_comparisons if comp["winner"] == "subzero")
            
            print(f"\n🎭 Personality Comparison (last 10):")
            print(f"   • Normal wins: {normal_wins}")
            print(f"   • Sub-Zero wins: {subzero_wins}")
            print(f"   • Performance balance: {'Balanced' if abs(normal_wins - subzero_wins) <= 2 else 'Imbalanced'}")

    def start_intensive_training(self):
        """Start intensive dual-personality training"""
        if self.training_active:
            print("⚠️ Training is already active")
            return
        
        self.training_active = True
        self.training_thread = threading.Thread(target=self.intensive_dual_training_cycle, daemon=True)
        self.training_thread.start()
        
        print("🎭 Intensive Dual-Personality Training Started!")
        print(f"🔄 Training every {self.training_interval} seconds")
        print("🤖 Normal personality: Educational, helpful, balanced")
        print("🧊 Sub-Zero personality: Bold, confident, aggressive")
        print("🎯 Cross-training ratio: 30%")

    def stop_training(self):
        """Stop the training process"""
        self.training_active = False
        if self.training_thread and self.training_thread.is_alive():
            self.training_thread.join(timeout=5)
        print("🛑 Dual-personality training stopped")

    def get_comprehensive_stats(self) -> Dict:
        """Get comprehensive training statistics"""
        stats = {
            "training_active": self.training_active,
            "training_interval": self.training_interval,
            "cross_training_ratio": self.cross_training_ratio,
            "personality_metrics": self.personality_metrics,
            "total_comparisons": len(self.personality_comparison_data)
        }
        
        # Add performance summary
        if self.personality_comparison_data:
            recent_comparisons = self.personality_comparison_data[-20:]
            normal_wins = sum(1 for comp in recent_comparisons if comp["winner"] == "normal")
            subzero_wins = len(recent_comparisons) - normal_wins
            
            stats["performance_summary"] = {
                "normal_win_rate": normal_wins / len(recent_comparisons) if recent_comparisons else 0,
                "subzero_win_rate": subzero_wins / len(recent_comparisons) if recent_comparisons else 0,
                "total_recent_comparisons": len(recent_comparisons)
            }
        
        return stats

    def export_dual_training_data(self, filename: str = None) -> str:
        """Export comprehensive dual-personality training data"""
        if not filename:
            filename = f"dual_personality_training_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "training_statistics": self.get_comprehensive_stats(),
            "personality_metrics": self.personality_metrics,
            "personality_comparisons": self.personality_comparison_data[-50:],  # Last 50 comparisons
            "cross_personality_insights": self.cross_personality_insights,
            "configuration": {
                "training_interval": self.training_interval,
                "quality_threshold": self.quality_threshold,
                "cross_training_ratio": self.cross_training_ratio
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"📁 Dual-personality training data exported to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exporting training data: {e}")
            return ""

# Main execution for dual-personality training
if __name__ == "__main__":
    print("🎭 Initializing Enhanced Dual-Personality Training System...")
    
    try:
        # Initialize chatbot
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        chatbot = ImprovedDualPersonalityChatbot()
        
        # Initialize dual-personality trainer
        trainer = DualPersonalityAdvancedTrainer(chatbot)
        
        # Start intensive training
        trainer.start_intensive_training()
        
        print("✅ Dual-personality training system is now running!")
        print("📊 Monitor training progress for both personalities")
        print("🛑 Press Ctrl+C to stop training")
        
        # Keep the system running
        try:
            while trainer.training_active:
                time.sleep(15)
                stats = trainer.get_comprehensive_stats()
                
                # Brief status update
                normal_sessions = stats["personality_metrics"]["normal"]["training_sessions"]
                subzero_sessions = stats["personality_metrics"]["subzero"]["training_sessions"]
                print(f"\n🔄 Status: Normal={normal_sessions} sessions, Sub-Zero={subzero_sessions} sessions")
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping dual-personality training...")
            trainer.stop_training()
            
            # Export final training data
            export_file = trainer.export_dual_training_data()
            print(f"💾 Training data saved to {export_file}")
            
    except Exception as e:
        print(f"❌ Error initializing dual-personality training: {e}")
        import traceback
        traceback.print_exc()
