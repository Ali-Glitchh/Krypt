#!/usr/bin/env python3
"""
KoinToss Production Startup Script
- Starts the enhanced API server with autonomous training
- Handles graceful shutdown and error recovery
- Exports training data on exit
"""

import asyncio
import signal
import sys
import time
import threading
from datetime import datetime

def signal_handler(signum, frame):
    """Handle graceful shutdown"""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    
    # Stop autonomous training
    if 'autonomous_trainer' in globals() and autonomous_trainer:
        print("🔄 Stopping autonomous training...")
        autonomous_trainer.stop_autonomous_training()
        
        # Export training data
        try:
            export_file = autonomous_trainer.export_training_data()
            print(f"💾 Training data exported to: {export_file}")
        except Exception as e:
            print(f"⚠️ Could not export training data: {e}")
    
    print("👋 KoinToss shutdown complete!")
    sys.exit(0)

def start_autonomous_training():
    """Start autonomous training in background"""
    global autonomous_trainer
    
    try:
        print("🤖 Initializing KoinToss Chatbot...")
        from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
        chatbot = ImprovedDualPersonalityChatbot()
        print("✅ Chatbot ready!")
        
        print("🚀 Starting Advanced Autonomous Training...")
        from advanced_autonomous_trainer import AdvancedAutonomousTrainer
        autonomous_trainer = AdvancedAutonomousTrainer(chatbot)
        
        # Start training
        autonomous_trainer.start_autonomous_training()
        print("✅ Autonomous training started!")
        
        return autonomous_trainer
        
    except Exception as e:
        print(f"❌ Error starting autonomous training: {e}")
        return None

def monitor_training():
    """Monitor training progress"""
    global autonomous_trainer
    
    while True:
        try:
            if autonomous_trainer and autonomous_trainer.training_active:
                stats = autonomous_trainer.get_training_statistics()
                print(f"\n📊 Training Stats:")
                print(f"   • Sessions: {stats.get('training_sessions', 0)}")
                print(f"   • Learning Velocity: {stats.get('learning_velocity', 0):.4f}")
                print(f"   • Total Conversations: {stats.get('total_conversations', 0)}")
                print(f"   • Latest Score: {stats.get('latest_score', 'N/A')}")
                print(f"   • Interval: {stats.get('training_interval', 0):.0f}s")
                
            time.sleep(60)  # Report every minute
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Monitoring error: {e}")
            time.sleep(30)

def main():
    """Main startup function"""
    print("=" * 60)
    print("🎯 KoinToss Production Environment Starting...")
    print("=" * 60)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start autonomous training
    global autonomous_trainer
    autonomous_trainer = start_autonomous_training()
    
    if not autonomous_trainer:
        print("❌ Failed to start autonomous training, exiting...")
        sys.exit(1)
    
    print("\n🎉 KoinToss is now running with autonomous training!")
    print("📈 The bot will continuously learn and improve")
    print("🔄 Training cycles run every few minutes")
    print("📊 Progress will be reported below")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_training, daemon=True)
    monitor_thread.start()
    
    try:
        # Keep the main thread alive
        while autonomous_trainer.training_active:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
