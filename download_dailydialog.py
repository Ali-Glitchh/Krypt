#!/usr/bin/env python3
"""
Download and preprocess DailyDialog dataset for training a human-like normal bot.
DailyDialog contains 13,118 daily conversation topics with human-annotated emotions.
"""

import os
import requests
import zipfile
import json
from typing import List, Tuple

def download_dailydialog():
    """Download and extract DailyDialog dataset"""
    url = "http://yanran.li/files/ijcnlp_dailydialog.zip"
    zip_path = "ijcnlp_dailydialog.zip"
    extract_path = "dailydialog_data"
    
    print("🔄 Downloading DailyDialog dataset...")
    
    if not os.path.exists(zip_path):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ Downloaded DailyDialog dataset")
    else:
        print("📁 DailyDialog zip already exists")
    
    # Extract
    if not os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print("✅ Extracted DailyDialog dataset")
    else:
        print("📁 DailyDialog data already extracted")
    
    return extract_path

def parse_dailydialog_files(extract_path: str) -> List[Tuple[str, str]]:
    """Parse DailyDialog files into conversation pairs"""
      # Find the dialogue file
    train_file = None
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file == "dialogues_text.txt":
                train_file = os.path.join(root, file)
                break
        if train_file:
            break
    
    if not train_file:
        print("❌ Could not find dialogues_text.txt in extracted files")
        return []
    
    print(f"📖 Reading dialogues from: {train_file}")
    
    conversation_pairs = []
    
    with open(train_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # Split dialogue by utterances (separated by __eou__)
            utterances = line.split(' __eou__')
            utterances = [u.strip() for u in utterances if u.strip()]
            
            # Create conversation pairs from consecutive utterances
            for i in range(len(utterances) - 1):
                user_msg = utterances[i]
                bot_response = utterances[i + 1]
                
                # Clean up messages
                user_msg = user_msg.replace('__eou__', '').strip()
                bot_response = bot_response.replace('__eou__', '').strip()
                
                if user_msg and bot_response:
                    conversation_pairs.append((user_msg, bot_response))
    
    print(f"✅ Extracted {len(conversation_pairs)} conversation pairs")
    return conversation_pairs

def create_normal_dataset(conversation_pairs: List[Tuple[str, str]]) -> str:
    """Create a dataset file for normal bot training"""
    
    # Filter for quality conversations (length, no weird characters, etc.)
    filtered_pairs = []
    
    for user_msg, bot_response in conversation_pairs:
        # Basic quality filters
        if (len(user_msg) < 200 and len(bot_response) < 200 and 
            len(user_msg) > 5 and len(bot_response) > 5 and
            not any(char in user_msg + bot_response for char in ['<', '>', '[', ']', '__']) and
            user_msg.count(' ') > 0 and bot_response.count(' ') > 0):
            filtered_pairs.append((user_msg, bot_response))
    
    print(f"✅ Filtered to {len(filtered_pairs)} high-quality conversation pairs")
    
    # Convert to the format expected by our trainer
    dataset = []
    for user_msg, bot_response in filtered_pairs:
        dataset.append({
            "user": user_msg,
            "bot": bot_response
        })
    
    # Save as JSON
    output_file = "normal_conversation_dataset.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(dataset)} conversations to {output_file}")
    return output_file

def create_fallback_text_format(dataset_file: str):
    """Create text format as backup for trainers that expect text format"""
    
    with open(dataset_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    text_output = "normal_conversation_dataset.txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"Human: {item['user']}\n")
            f.write(f"Bot: {item['bot']}\n")
            f.write("\n")
    
    print(f"💾 Also saved text format to {text_output}")
    return text_output

def main():
    """Main function to download and process DailyDialog dataset"""
    
    print("🤖 Setting up high-quality conversational dataset for normal bot")
    print("📊 Using DailyDialog - 13k+ human-written daily conversations")
    print()
    
    try:
        # Download dataset
        extract_path = download_dailydialog()
        
        # Parse conversations
        conversation_pairs = parse_dailydialog_files(extract_path)
        
        if not conversation_pairs:
            print("❌ Failed to extract conversation pairs")
            return
        
        # Create dataset files
        json_file = create_normal_dataset(conversation_pairs)
        text_file = create_fallback_text_format(json_file)
        
        print()
        print("🎉 Successfully created normal bot dataset!")
        print(f"📁 JSON format: {json_file}")
        print(f"📁 Text format: {text_file}")
        print()
        print("Next steps:")
        print("1. Run enhanced_normal_trainer.py with new dataset")
        print("2. Test improved normal bot responses")
        print("3. Compare with Sub-Zero bot quality")
        
    except Exception as e:
        print(f"❌ Error processing dataset: {e}")
        print("💡 Trying fallback approach...")
        
        # Fallback: Create a smaller but high-quality dataset manually
        create_fallback_dataset()

def create_fallback_dataset():
    """Create a fallback high-quality conversation dataset if download fails"""
    
    print("📝 Creating fallback high-quality conversation dataset...")
    
    # High-quality conversation examples that sound natural and human-like
    fallback_conversations = [
        ("Hey, how's your day going?", "Pretty good! Just finished a meeting that went better than expected. How about you?"),
        ("What did you think of that movie last night?", "I really enjoyed it! The plot twists kept me on the edge of my seat. What was your favorite part?"),
        ("I'm thinking about learning a new language", "That's awesome! Which language are you considering? I've always wanted to learn Spanish myself."),
        ("Do you have any weekend plans?", "I'm planning to visit the farmers market and maybe catch up on some reading. Nothing too exciting, but I'm looking forward to it."),
        ("This weather has been crazy lately", "Tell me about it! One day it's sunny, the next it's pouring rain. I can never decide what to wear anymore."),
        ("I just started a new job", "Congratulations! How are you finding it so far? New jobs can be both exciting and nerve-wracking."),
        ("What's your favorite type of music?", "I love indie rock and some electronic stuff. There's something about a good melody that just hits different. What about you?"),
        ("I'm having trouble sleeping lately", "That's tough. Have you tried any relaxation techniques? Sometimes I listen to calming music or do some light stretching before bed."),
        ("What do you like to do for fun?", "I enjoy hiking, reading, and trying out new recipes. There's something satisfying about cooking a meal from scratch. Do you cook much?"),
        ("This coffee is amazing", "Right? I discovered this place last month and I've been coming back ever since. Their barista really knows what they're doing."),
        ("I'm thinking of getting a pet", "That's exciting! What kind of pet are you considering? Dogs and cats each have their own charm, but they're quite different commitments."),
        ("How do you stay motivated when things get tough?", "I try to break big problems into smaller, manageable pieces. Also, reminding myself of past challenges I've overcome helps give me perspective."),
        ("What's the best advice you've ever received?", "Someone once told me that you can't control what happens to you, but you can control how you respond. It's helped me through a lot of difficult situations."),
        ("I love this time of year", "Same here! There's something special about the changing seasons. Are you more of a spring person or do you prefer fall?"),
        ("Do you believe in work-life balance?", "Absolutely. I think it's important to set boundaries and make time for the things that matter outside of work. It makes you more effective in all areas of life."),
        ("What's something you're passionate about?", "I'm really passionate about environmental conservation. Small changes in our daily habits can make a big difference over time."),
        ("I had the weirdest dream last night", "Dreams can be so strange! I had one where I could fly, but only three feet off the ground. Do you usually remember your dreams?"),
        ("Technology moves so fast these days", "It really does! Sometimes I feel like I just learned how to use something and there's already a newer version out. But it's also pretty amazing what we can do now."),
        ("What's your idea of a perfect day?", "Probably starting with good coffee, spending time outdoors, having meaningful conversations with friends, and ending with a good book. Simple but fulfilling."),
        ("I'm trying to eat healthier", "That's great! I've been working on that too. I find meal prepping on Sundays really helps me make better choices during the week."),
    ]
    
    # Expand the dataset with variations and additional conversations
    expanded_conversations = []
    
    # Add the base conversations
    for user, bot in fallback_conversations:
        expanded_conversations.append({"user": user, "bot": bot})
    
    # Add variations and follow-ups
    follow_ups = [
        ("Tell me more about that", "Well, there are quite a few aspects to consider. What specifically interests you most?"),
        ("That sounds interesting", "I'm glad you think so! It's something I've been thinking about a lot lately."),
        ("I've never thought about it that way", "It's funny how a different perspective can change everything, isn't it?"),
        ("Thanks for sharing that", "Of course! I enjoy having these kinds of conversations."),
        ("What made you realize that?", "It was actually a combination of experiences over time that led me to that conclusion."),
        ("How long have you been interested in this?", "It's been a gradual thing, probably started a few years ago and has grown from there."),
        ("Do you have any recommendations?", "I'd suggest starting with the basics and then exploring what resonates with you personally."),
        ("That's a good point", "Thanks! I think it's important to consider all angles when looking at complex topics."),
        ("I should try that sometime", "You definitely should! It might be just what you're looking for."),
        ("What's been your experience with that?", "Overall quite positive, though there have been some challenges along the way."),
    ]
    
    expanded_conversations.extend([{"user": user, "bot": bot} for user, bot in follow_ups])
    
    # Save JSON format
    json_file = "normal_conversation_dataset.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(expanded_conversations, f, indent=2, ensure_ascii=False)
    
    # Save text format
    text_file = "normal_conversation_dataset.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        for item in expanded_conversations:
            f.write(f"Human: {item['user']}\n")
            f.write(f"Bot: {item['bot']}\n")
            f.write("\n")
    
    print(f"✅ Created fallback dataset with {len(expanded_conversations)} conversations")
    print(f"📁 JSON format: {json_file}")
    print(f"📁 Text format: {text_file}")

if __name__ == "__main__":
    main()
