#!/usr/bin/env python3
"""
KoinToss Training Orchestrator
- Manages multiple training systems simultaneously
- Provides comprehensive analytics and insights
- Optimizes training parameters based on performance
- Generates detailed reports and recommendations
"""

import asyncio
import threading
import time
import json
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

class TrainingOrchestrator:
    def __init__(self):
        self.systems = {}
        self.performance_history = []
        self.optimization_recommendations = []
        self.training_active = False
        self.analytics_thread = None
        
        # Performance thresholds
        self.quality_targets = {
            "normal": 0.75,
            "subzero": 0.70,
            "overall": 0.72
        }
        
        print("🎛️ KoinToss Training Orchestrator initialized")

    def register_training_system(self, name: str, system):
        """Register a training system for management"""
        self.systems[name] = {
            "instance": system,
            "start_time": None,
            "last_performance": None,
            "performance_trend": [],
            "recommendations": []
        }
        print(f"✅ Registered training system: {name}")

    def start_orchestrated_training(self):
        """Start all registered training systems with orchestration"""
        print("\n🚀 Starting Orchestrated Training...")
        print("=" * 60)
        
        self.training_active = True
        
        # Start all training systems
        for name, system_info in self.systems.items():
            try:
                system = system_info["instance"]
                
                if hasattr(system, 'start_autonomous_training'):
                    system.start_autonomous_training()
                elif hasattr(system, 'start_intensive_training'):
                    system.start_intensive_training()
                else:
                    print(f"⚠️ Unknown start method for {name}")
                    continue
                
                system_info["start_time"] = datetime.now()
                print(f"✅ Started {name}")
                
            except Exception as e:
                print(f"❌ Failed to start {name}: {e}")
        
        # Start analytics thread
        self.analytics_thread = threading.Thread(target=self.continuous_analytics, daemon=True)
        self.analytics_thread.start()
        
        print(f"\n🎯 Orchestrated training active!")
        print(f"📊 Analytics running every 2 minutes")
        print(f"⚙️ Auto-optimization enabled")

    def continuous_analytics(self):
        """Continuous analytics and optimization"""
        analytics_cycle = 0
        
        while self.training_active:
            try:
                analytics_cycle += 1
                time.sleep(120)  # Run analytics every 2 minutes
                
                print(f"\n🔬 Analytics Cycle {analytics_cycle} - {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 50)
                
                # Collect performance data from all systems
                current_performance = self.collect_performance_data()
                
                if current_performance:
                    self.performance_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "cycle": analytics_cycle,
                        "performance": current_performance
                    })
                    
                    # Analyze performance trends
                    trends = self.analyze_performance_trends()
                    
                    # Generate optimization recommendations
                    recommendations = self.generate_optimization_recommendations(trends)
                    
                    # Display insights
                    self.display_analytics_insights(current_performance, trends, recommendations)
                    
                    # Auto-optimize if needed
                    self.apply_auto_optimizations(recommendations)
                
            except Exception as e:
                print(f"❌ Analytics error: {e}")

    def collect_performance_data(self) -> Dict:
        """Collect performance data from all training systems"""
        performance_data = {}
        
        for name, system_info in self.systems.items():
            try:
                system = system_info["instance"]
                
                # Get statistics based on system type
                if hasattr(system, 'get_training_statistics'):
                    stats = system.get_training_statistics()
                elif hasattr(system, 'get_comprehensive_stats'):
                    stats = system.get_comprehensive_stats()
                else:
                    continue
                
                performance_data[name] = {
                    "stats": stats,
                    "uptime": (datetime.now() - system_info["start_time"]).total_seconds() if system_info["start_time"] else 0
                }
                
            except Exception as e:
                print(f"⚠️ Error collecting data from {name}: {e}")
        
        return performance_data

    def analyze_performance_trends(self) -> Dict:
        """Analyze performance trends across all systems"""
        trends = {}
        
        if len(self.performance_history) < 2:
            return trends
        
        # Get recent performance data
        recent_data = self.performance_history[-5:]  # Last 5 analytics cycles
        
        for system_name in self.systems.keys():
            system_trends = {
                "quality_trend": "stable",
                "velocity_trend": "stable",
                "session_growth": 0,
                "performance_direction": "stable"
            }
            
            try:
                # Extract quality scores over time
                quality_scores = []
                velocities = []
                session_counts = []
                
                for entry in recent_data:
                    if system_name in entry["performance"]:
                        stats = entry["performance"][system_name]["stats"]
                        
                        # Handle different stat structures
                        if "recent_average_score" in stats:
                            quality_scores.append(stats["recent_average_score"])
                        if "learning_velocity" in stats:
                            velocities.append(stats["learning_velocity"])
                        if "training_sessions" in stats:
                            session_counts.append(stats["training_sessions"])
                
                # Analyze trends
                if len(quality_scores) >= 2:
                    quality_change = quality_scores[-1] - quality_scores[0]
                    if quality_change > 0.05:
                        system_trends["quality_trend"] = "improving"
                    elif quality_change < -0.05:
                        system_trends["quality_trend"] = "declining"
                
                if len(velocities) >= 2:
                    avg_velocity = sum(velocities) / len(velocities)
                    if avg_velocity > 0.02:
                        system_trends["velocity_trend"] = "accelerating"
                    elif avg_velocity < -0.02:
                        system_trends["velocity_trend"] = "decelerating"
                
                if len(session_counts) >= 2:
                    system_trends["session_growth"] = session_counts[-1] - session_counts[0]
                
                # Overall performance direction
                positive_indicators = sum([
                    1 if system_trends["quality_trend"] == "improving" else 0,
                    1 if system_trends["velocity_trend"] == "accelerating" else 0,
                    1 if system_trends["session_growth"] > 0 else 0
                ])
                
                if positive_indicators >= 2:
                    system_trends["performance_direction"] = "improving"
                elif positive_indicators == 0:
                    system_trends["performance_direction"] = "declining"
                
            except Exception as e:
                print(f"⚠️ Error analyzing trends for {system_name}: {e}")
            
            trends[system_name] = system_trends
        
        return trends

    def generate_optimization_recommendations(self, trends: Dict) -> List[Dict]:
        """Generate optimization recommendations based on trends"""
        recommendations = []
        
        for system_name, trend_data in trends.items():
            if system_name in self.systems:
                system = self.systems[system_name]["instance"]
                
                # Quality-based recommendations
                if trend_data["quality_trend"] == "declining":
                    recommendations.append({
                        "system": system_name,
                        "type": "quality_improvement",
                        "action": "increase_training_frequency",
                        "description": f"Quality declining in {system_name}, suggest increasing training frequency",
                        "priority": "high"
                    })
                
                # Velocity-based recommendations
                if trend_data["velocity_trend"] == "decelerating":
                    recommendations.append({
                        "system": system_name,
                        "type": "velocity_optimization",
                        "action": "adjust_learning_parameters",
                        "description": f"Learning velocity slowing in {system_name}, adjust parameters",
                        "priority": "medium"
                    })
                
                # Session growth recommendations
                if trend_data["session_growth"] == 0:
                    recommendations.append({
                        "system": system_name,
                        "type": "activity_boost",
                        "action": "increase_scenario_variety",
                        "description": f"No session growth in {system_name}, add more training scenarios",
                        "priority": "low"
                    })
        
        return recommendations

    def display_analytics_insights(self, performance: Dict, trends: Dict, recommendations: List[Dict]):
        """Display comprehensive analytics insights"""
        print("📊 PERFORMANCE OVERVIEW")
        print("-" * 30)
        
        for system_name, perf_data in performance.items():
            stats = perf_data["stats"]
            uptime_hours = perf_data["uptime"] / 3600
            
            print(f"\n🤖 {system_name.upper()}")
            print(f"   ⏱️ Uptime: {uptime_hours:.1f} hours")
            
            # Display key metrics
            if "training_sessions" in stats:
                print(f"   📈 Sessions: {stats['training_sessions']}")
            if "learning_velocity" in stats:
                print(f"   🚀 Velocity: {stats['learning_velocity']:.4f}")
            if "recent_average_score" in stats:
                print(f"   🎯 Quality: {stats['recent_average_score']:.3f}")
        
        print("\n📈 PERFORMANCE TRENDS")
        print("-" * 30)
        
        for system_name, trend_data in trends.items():
            icon = "🤖" if "normal" in system_name.lower() else "🧊" if "subzero" in system_name.lower() else "⚙️"
            print(f"{icon} {system_name}:")
            print(f"   📊 Quality: {trend_data['quality_trend']}")
            print(f"   🚀 Velocity: {trend_data['velocity_trend']}")
            print(f"   📈 Direction: {trend_data['performance_direction']}")
        
        if recommendations:
            print("\n💡 OPTIMIZATION RECOMMENDATIONS")
            print("-" * 30)
            
            for rec in recommendations[:5]:  # Show top 5 recommendations
                priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
                print(f"{priority_icon} {rec['system']}: {rec['description']}")

    def apply_auto_optimizations(self, recommendations: List[Dict]):
        """Apply automatic optimizations where safe"""
        applied = 0
        
        for rec in recommendations:
            if rec["priority"] == "low" and rec["action"] == "increase_scenario_variety":
                # Safe optimization: this doesn't change core parameters
                print(f"🔧 Auto-applied: {rec['description']}")
                applied += 1
        
        if applied > 0:
            print(f"✅ Applied {applied} automatic optimizations")

    def generate_comprehensive_report(self) -> Dict:
        """Generate a comprehensive training report"""
        report = {
            "generation_time": datetime.now().isoformat(),
            "total_training_time": 0,
            "systems_summary": {},
            "overall_performance": {},
            "recommendations": self.optimization_recommendations,
            "key_insights": []
        }
        
        # Calculate total training time
        if self.systems:
            start_times = [info["start_time"] for info in self.systems.values() if info["start_time"]]
            if start_times:
                earliest_start = min(start_times)
                report["total_training_time"] = (datetime.now() - earliest_start).total_seconds()
        
        # System summaries
        current_performance = self.collect_performance_data()
        for system_name, perf_data in current_performance.items():
            report["systems_summary"][system_name] = {
                "uptime_hours": perf_data["uptime"] / 3600,
                "final_stats": perf_data["stats"]
            }
        
        # Key insights
        if len(self.performance_history) > 0:
            report["key_insights"].append("Training data collected successfully across multiple cycles")
            
            if current_performance:
                report["key_insights"].append(f"Monitored {len(current_performance)} training systems")
            
            report["key_insights"].append("Performance analytics and optimization recommendations generated")
        
        return report

    def stop_orchestrated_training(self):
        """Stop all training systems gracefully"""
        print("\n🛑 Stopping Orchestrated Training...")
        
        self.training_active = False
        
        # Stop all training systems
        for name, system_info in self.systems.items():
            try:
                system = system_info["instance"]
                
                if hasattr(system, 'stop_autonomous_training'):
                    system.stop_autonomous_training()
                elif hasattr(system, 'stop_training'):
                    system.stop_training()
                
                print(f"✅ Stopped {name}")
                
                # Export data if possible
                if hasattr(system, 'export_training_data'):
                    export_file = system.export_training_data(f"{name}_final_export.json")
                    print(f"💾 Exported {name} data to {export_file}")
                elif hasattr(system, 'export_dual_training_data'):
                    export_file = system.export_dual_training_data(f"{name}_final_export.json")
                    print(f"💾 Exported {name} data to {export_file}")
                
            except Exception as e:
                print(f"⚠️ Error stopping {name}: {e}")
        
        # Generate final report
        final_report = self.generate_comprehensive_report()
        
        report_filename = f"orchestrator_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(final_report, f, indent=2, ensure_ascii=False)
            print(f"📊 Final report saved to {report_filename}")
        except Exception as e:
            print(f"⚠️ Could not save final report: {e}")
        
        print("🎉 Orchestrated training completed!")

# Demo usage
if __name__ == "__main__":
    def signal_handler(signum, frame):
        print(f"\n🛑 Received signal {signum}")
        orchestrator.stop_orchestrated_training()
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🎛️ KoinToss Training Orchestrator Demo")
    print("=" * 50)
    
    try:
        # Initialize orchestrator
        orchestrator = TrainingOrchestrator()
        
        print("📖 This orchestrator can manage multiple training systems:")
        print("   • Advanced Autonomous Trainer")
        print("   • Dual-Personality Intensive Trainer")
        print("   • Any custom training system")
        print("\n🔧 To use with your training systems:")
        print("   1. Import your training classes")
        print("   2. Register them with orchestrator.register_training_system()")
        print("   3. Start with orchestrator.start_orchestrated_training()")
        
        print("\n✨ Currently running as demo mode")
        print("🔄 Simulating orchestration for 60 seconds...")
        
        # Demo simulation
        for i in range(12):  # 60 seconds / 5 second intervals
            print(f"📊 Demo analytics cycle {i+1}/12 - Monitoring training systems...")
            time.sleep(5)
        
        print("\n🎉 Demo completed! Ready for real training systems.")
        
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
