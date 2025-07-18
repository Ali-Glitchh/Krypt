#!/usr/bin/env python3
"""
Chatbot Cleanup Script
Removes redundant chatbot files to prevent import confusion.
Keeps only the essential chatbot files.
"""

import os
import shutil
from pathlib import Path

def cleanup_redundant_chatbots():
    """Remove redundant chatbot files, keeping only essential ones"""
    
    # Files to KEEP (essential)
    keep_files = [
        'improved_dual_personality_chatbot.py',  # Main chatbot
        'crypto_chatbot.py',  # Fallback option
        'crypto_chatbot_fixed.py',  # Fixed version
        'enhanced_crypto_chatbot.py'  # Enhanced version
    ]
    
    # Files to REMOVE (redundant/test files)
    remove_files = [
        'test_simplified_chatbot.py',
        'test_pure_chatbot.py', 
        'test_improved_chatbot.py',
        'test_chatbot_with_news.py',
        'simple_chatbot_test.py',
        'quick_chatbot_test_fixed.py',
        'quick_chatbot_test.py',
        'pure_dual_personality_chatbot.py',
        'improved_dual_personality_chatbot_fixed.py',
        'improved_dual_personality_chatbot_broken.py',
        'final_dual_personality_chatbot.py',
        'crypto_chatbot_simple.py',
        'crypto_chatbot_fixed_subzero.py'
    ]
    
    # Create backup directory
    backup_dir = Path('chatbot_backups')
    backup_dir.mkdir(exist_ok=True)
    
    removed_count = 0
    backed_up_count = 0
    
    print("🧹 Starting chatbot cleanup...")
    print(f"📁 Backup directory: {backup_dir.absolute()}")
    
    for filename in remove_files:
        filepath = Path(filename)
        
        if filepath.exists():
            # Move to backup instead of deleting
            backup_path = backup_dir / filename
            shutil.move(str(filepath), str(backup_path))
            backed_up_count += 1
            print(f"📦 Moved to backup: {filename}")
            
    print(f"\n✅ Cleanup completed!")
    print(f"📦 Backed up {backed_up_count} files")
    print(f"🔄 Kept {len(keep_files)} essential chatbot files:")
    
    for keep_file in keep_files:
        if Path(keep_file).exists():
            print(f"   ✅ {keep_file}")
        else:
            print(f"   ❌ {keep_file} (not found)")
    
    print(f"\n📊 Summary:")
    print(f"   Before: ~19 chatbot files")
    print(f"   After: {len([f for f in keep_files if Path(f).exists()])} main files")
    print(f"   Backed up: {backed_up_count} redundant files")

if __name__ == "__main__":
    cleanup_redundant_chatbots()
