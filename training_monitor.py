#!/usr/bin/env python3
"""
KoinToss Dual Training Monitor
- Monitors both training systems simultaneously
- Provides real-time performance comparison
- Tracks learning progress for both personalities
"""

import time
import json
import os
from datetime import datetime

def monitor_training_progress():
    """Monitor and display training progress"""
    print("🎭 KoinToss Dual-Personality Training Monitor")
    print("=" * 70)
    print("📊 Monitoring both training systems...")
    print("🔄 Updates every 30 seconds")
    print("🛑 Press Ctrl+C to stop monitoring\n")
    
    monitoring_count = 0
    
    try:
        while True:
            monitoring_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n📊 Training Status Update #{monitoring_count} - {current_time}")
            print("-" * 70)
            
            # Check for export files to see training activity
            export_files = [f for f in os.listdir('.') if f.endswith('_export.json') or 'training_export' in f]
            
            if export_files:
                print(f"📁 Found {len(export_files)} training export files")
                
                # Get the most recent export file
                latest_export = max(export_files, key=os.path.getctime)
                try:
                    with open(latest_export, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    print(f"📈 Latest Export: {latest_export}")
                    
                    # Display training statistics if available
                    if 'training_statistics' in data:
                        stats = data['training_statistics']
                        print(f"   • Total Conversations: {stats.get('total_conversations', 0)}")
                        print(f"   • Training Sessions: {stats.get('training_sessions', 0)}")
                        print(f"   • Learning Velocity: {stats.get('learning_velocity', 0):.4f}")
                    
                    # Display personality metrics if available
                    if 'personality_metrics' in data:
                        metrics = data['personality_metrics']
                        for personality, data_p in metrics.items():
                            icon = "🤖" if personality == "normal" else "🧊"
                            sessions = data_p.get('training_sessions', 0)
                            velocity = data_p.get('learning_velocity', 0)
                            quality = data_p.get('conversation_quality', [])
                            avg_quality = sum(quality[-5:]) / len(quality[-5:]) if quality else 0
                            
                            print(f"   {icon} {personality.title()}: {sessions} sessions, "
                                  f"velocity={velocity:.4f}, quality={avg_quality:.3f}")
                
                except Exception as e:
                    print(f"⚠️ Error reading export file: {e}")
            else:
                print("📁 No training export files found yet")
            
            # Display system status
            print(f"\n🎯 Training Objectives:")
            print(f"   • Normal AI: Educational, helpful, balanced responses")
            print(f"   • Sub-Zero AI: Bold, confident, aggressive analysis")
            print(f"   • Cross-training: Comparative learning between personalities")
            print(f"   • Market awareness: Real-time crypto data integration")
            
            # Performance indicators
            print(f"\n📈 Performance Indicators:")
            print(f"   • Response quality: Higher scores = better responses")
            print(f"   • Learning velocity: Positive = improving, negative = declining")
            print(f"   • Training sessions: More sessions = more learning opportunities")
            print(f"   • Cross-personality comparison: Balanced performance preferred")
            
            # Tips for optimization
            if monitoring_count % 5 == 0:  # Every 5th update
                print(f"\n💡 Training Optimization Tips:")
                print(f"   • Let training run for at least 30 minutes for meaningful results")
                print(f"   • Both personalities should have similar training session counts")
                print(f"   • Learning velocity should stabilize around 0.01-0.05")
                print(f"   • Quality scores above 0.7 indicate good performance")
            
            print(f"\n⏰ Next update in 30 seconds...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Training monitor stopped")
        print(f"📊 Total monitoring cycles: {monitoring_count}")
        print(f"💾 Check export files for detailed training data")

if __name__ == "__main__":
    monitor_training_progress()
