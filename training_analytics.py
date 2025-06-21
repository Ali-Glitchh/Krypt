#!/usr/bin/env python3
"""
Training Analytics and Monitoring System
Tracks training progress, analyzes performance, and provides insights
"""

import json
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import glob

class TrainingAnalytics:
    def __init__(self):
        self.training_history = []
        self.performance_metrics = []
        self.load_training_history()
    
    def load_training_history(self):
        """Load training history from saved files"""
        training_files = glob.glob("training_session_*.json")
        dynamic_files = glob.glob("dynamic_conversations_*.json")
        
        print(f"📊 Loading training history from {len(training_files)} training sessions...")
        
        for file in training_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    self.training_history.append(session_data)
            except Exception as e:
                print(f"⚠️ Error loading {file}: {e}")
        
        print(f"✅ Loaded {len(self.training_history)} training sessions")
        
        # Load dynamic conversations for analysis
        total_dynamic = 0
        for file in dynamic_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
                    total_dynamic += len(conversations)
            except Exception as e:
                print(f"⚠️ Error loading {file}: {e}")
        
        if total_dynamic > 0:
            print(f"📚 Found {total_dynamic} dynamic conversations from previous sessions")
    
    def analyze_training_progress(self) -> Dict:
        """Analyze training progress over time"""
        if not self.training_history:
            return {"error": "No training history available"}
        
        # Extract metrics from training sessions
        sessions_by_date = {}
        total_conversations = 0
        total_interactions = 0
        quality_scores = []
        
        for session in self.training_history:
            date = session['timestamp'][:10]  # Extract date
            if date not in sessions_by_date:
                sessions_by_date[date] = {
                    'sessions': 0,
                    'conversations': 0,
                    'interactions': 0,
                    'avg_quality': 0
                }
            
            sessions_by_date[date]['sessions'] += 1
            
            # Count training conversations
            training_convs = len(session.get('training_conversations', []))
            sessions_by_date[date]['conversations'] += training_convs
            total_conversations += training_convs
            
            # Count interactions
            metrics = session.get('performance_metrics', {})
            interactions = metrics.get('total_interactions', 0)
            sessions_by_date[date]['interactions'] += interactions
            total_interactions += interactions
            
            # Calculate quality scores
            for conv in session.get('training_conversations', []):
                quality = conv.get('quality_score', 0)
                if quality > 0:
                    quality_scores.append(quality)
        
        # Calculate overall statistics
        avg_quality = np.mean(quality_scores) if quality_scores else 0
        training_days = len(sessions_by_date)
        
        return {
            'total_training_sessions': len(self.training_history),
            'total_training_days': training_days,
            'total_conversations_added': total_conversations,
            'total_interactions_processed': total_interactions,
            'average_quality_score': round(avg_quality, 3),
            'quality_score_std': round(np.std(quality_scores), 3) if quality_scores else 0,
            'sessions_per_day': round(len(self.training_history) / max(training_days, 1), 2),
            'conversations_per_session': round(total_conversations / max(len(self.training_history), 1), 2),
            'daily_breakdown': sessions_by_date
        }
    
    def analyze_conversation_patterns(self) -> Dict:
        """Analyze patterns in training conversations"""
        all_conversations = []
        
        for session in self.training_history:
            conversations = session.get('training_conversations', [])
            all_conversations.extend(conversations)
        
        if not all_conversations:
            return {"error": "No conversation data available"}
        
        # Analyze conversation characteristics
        user_lengths = []
        bot_lengths = []
        quality_by_length = {}
        source_counts = {}
        
        for conv in all_conversations:
            user_text = conv.get('user', '')
            bot_text = conv.get('bot', '')
            quality = conv.get('quality_score', 0)
            source = conv.get('source', 'unknown')
            
            user_lengths.append(len(user_text))
            bot_lengths.append(len(bot_text))
            
            # Group quality by response length
            length_bucket = min(len(bot_text) // 50 * 50, 200)  # 0, 50, 100, 150, 200+
            if length_bucket not in quality_by_length:
                quality_by_length[length_bucket] = []
            quality_by_length[length_bucket].append(quality)
            
            # Count sources
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Calculate statistics
        avg_quality_by_length = {}
        for length, qualities in quality_by_length.items():
            avg_quality_by_length[length] = round(np.mean(qualities), 3)
        
        return {
            'total_conversations_analyzed': len(all_conversations),
            'avg_user_input_length': round(np.mean(user_lengths), 1),
            'avg_bot_response_length': round(np.mean(bot_lengths), 1),
            'user_length_std': round(np.std(user_lengths), 1),
            'bot_length_std': round(np.std(bot_lengths), 1),
            'quality_by_response_length': avg_quality_by_length,
            'conversation_sources': source_counts,
            'length_distribution': {
                'short_responses': sum(1 for l in bot_lengths if l < 50),
                'medium_responses': sum(1 for l in bot_lengths if 50 <= l < 150),
                'long_responses': sum(1 for l in bot_lengths if l >= 150)
            }
        }
    
    def generate_training_report(self) -> str:
        """Generate a comprehensive training report"""
        report = []
        report.append("🎓 COMPREHENSIVE TRAINING ANALYTICS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Training progress analysis
        progress = self.analyze_training_progress()
        if 'error' not in progress:
            report.append("📈 TRAINING PROGRESS OVERVIEW")
            report.append("-" * 40)
            report.append(f"Total training sessions: {progress['total_training_sessions']}")
            report.append(f"Training active for: {progress['total_training_days']} days")
            report.append(f"Conversations added: {progress['total_conversations_added']}")
            report.append(f"Interactions processed: {progress['total_interactions_processed']}")
            report.append(f"Average quality score: {progress['average_quality_score']}")
            report.append(f"Quality consistency (std): {progress['quality_score_std']}")
            report.append(f"Training frequency: {progress['sessions_per_day']} sessions/day")
            report.append("")
        
        # Conversation patterns analysis
        patterns = self.analyze_conversation_patterns()
        if 'error' not in patterns:
            report.append("💬 CONVERSATION PATTERNS ANALYSIS")
            report.append("-" * 40)
            report.append(f"Total conversations analyzed: {patterns['total_conversations_analyzed']}")
            report.append(f"Average user input length: {patterns['avg_user_input_length']} chars")
            report.append(f"Average bot response length: {patterns['avg_bot_response_length']} chars")
            report.append("")
            
            report.append("📊 Response Length Distribution:")
            length_dist = patterns['length_distribution']
            total_responses = sum(length_dist.values())
            for category, count in length_dist.items():
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                report.append(f"   {category}: {count} ({percentage:.1f}%)")
            report.append("")
            
            report.append("🎯 Quality by Response Length:")
            for length, quality in patterns['quality_by_response_length'].items():
                length_label = f"{length}-{length+49}" if length < 200 else "200+ chars"
                report.append(f"   {length_label}: {quality}")
            report.append("")
            
            if patterns['conversation_sources']:
                report.append("📚 Conversation Sources:")
                for source, count in patterns['conversation_sources'].items():
                    report.append(f"   {source}: {count}")
                report.append("")
        
        # Performance recommendations
        report.append("💡 TRAINING RECOMMENDATIONS")
        report.append("-" * 40)
        
        if 'error' not in progress:
            if progress['average_quality_score'] < 0.7:
                report.append("⚠️ Average quality score is below optimal (0.7+)")
                report.append("   → Focus on improving response relevance and accuracy")
            
            if progress['quality_score_std'] > 0.3:
                report.append("⚠️ Quality scores vary significantly")
                report.append("   → Review training data consistency")
            
            if progress['sessions_per_day'] < 1:
                report.append("📈 Training frequency could be increased")
                report.append("   → Consider more frequent training cycles")
        
        if 'error' not in patterns:
            if patterns['avg_bot_response_length'] < 50:
                report.append("📝 Responses are quite short on average")
                report.append("   → Consider expanding response detail")
            
            short_pct = patterns['length_distribution']['short_responses'] / max(patterns['total_conversations_analyzed'], 1) * 100
            if short_pct > 60:
                report.append("⚠️ High percentage of short responses")
                report.append("   → Focus on providing more comprehensive answers")
        
        if not any("⚠️" in line or "📈" in line or "📝" in line for line in report[-10:]):
            report.append("✅ Training performance is optimal!")
            report.append("   → Continue current training approach")
        
        report.append("")
        report.append("🎯 NEXT STEPS")
        report.append("-" * 40)
        report.append("1. Monitor quality scores in real-time")
        report.append("2. Gather user feedback for training improvement")
        report.append("3. Expand training dataset with high-quality conversations")
        report.append("4. Regularly review and optimize training parameters")
        report.append("")
        report.append("📊 For detailed metrics, run continuous_training_demo.py")
        
        return "\n".join(report)
    
    def save_analytics_report(self, filename: str = None):
        """Save analytics report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_analytics_report_{timestamp}.txt"
        
        report = self.generate_training_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Analytics report saved to {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None
    
    def visualize_training_progress(self):
        """Create visualizations of training progress (requires matplotlib)"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from datetime import datetime
            
            if not self.training_history:
                print("⚠️ No training history available for visualization")
                return
            
            # Prepare data for plotting
            dates = []
            quality_scores = []
            interaction_counts = []
            
            for session in self.training_history:
                date = datetime.fromisoformat(session['timestamp'].replace('Z', '+00:00'))
                dates.append(date)
                
                # Average quality score for this session
                convs = session.get('training_conversations', [])
                if convs:
                    avg_quality = np.mean([c.get('quality_score', 0) for c in convs])
                    quality_scores.append(avg_quality)
                else:
                    quality_scores.append(0)
                
                # Interaction count
                metrics = session.get('performance_metrics', {})
                interaction_counts.append(metrics.get('total_interactions', 0))
            
            # Create plots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Quality scores over time
            ax1.plot(dates, quality_scores, 'b-o', linewidth=2, markersize=6)
            ax1.set_title('Training Quality Scores Over Time', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Average Quality Score')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 1)
            
            # Interaction counts over time
            ax2.bar(dates, interaction_counts, alpha=0.7, color='green')
            ax2.set_title('Training Interactions Per Session', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Number of Interactions')
            ax2.set_xlabel('Date')
            ax2.grid(True, alpha=0.3)
            
            # Format x-axis
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            
            # Save plot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_filename = f"training_progress_{timestamp}.png"
            plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
            print(f"📊 Training progress chart saved to {plot_filename}")
            
            plt.show()
            
        except ImportError:
            print("⚠️ Matplotlib not available. Install with: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")

def main():
    """Main analytics interface"""
    print("📊 Training Analytics and Monitoring System")
    print("=" * 50)
    
    analytics = TrainingAnalytics()
    
    if not analytics.training_history:
        print("⚠️ No training history found. Run some training sessions first!")
        print("   Use: python continuous_training_demo.py")
        return
    
    while True:
        print("\n📋 Available Analytics:")
        print("1. Generate training report")
        print("2. View training progress")
        print("3. Analyze conversation patterns")
        print("4. Save detailed report")
        print("5. Create progress visualization")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            print("\n" + analytics.generate_training_report())
        
        elif choice == '2':
            progress = analytics.analyze_training_progress()
            print("\n📈 Training Progress Summary:")
            for key, value in progress.items():
                if key != 'daily_breakdown':
                    print(f"   {key}: {value}")
        
        elif choice == '3':
            patterns = analytics.analyze_conversation_patterns()
            print("\n💬 Conversation Patterns:")
            for key, value in patterns.items():
                if isinstance(value, dict) and len(value) > 5:
                    print(f"   {key}: {len(value)} categories")
                else:
                    print(f"   {key}: {value}")
        
        elif choice == '4':
            filename = analytics.save_analytics_report()
            if filename:
                print(f"✅ Report saved successfully!")
        
        elif choice == '5':
            analytics.visualize_training_progress()
        
        elif choice == '6':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
