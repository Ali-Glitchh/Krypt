#!/usr/bin/env python3
"""
MoonshotAI API Key Updater
Script to easily update the API key when you get a new one
"""

import os

def update_api_key():
    """Interactive script to update MoonshotAI API key"""
    
    print("🔑 MoonshotAI API Key Updater")
    print("=" * 40)
    
    # Get new API key from user
    print("\n📝 Enter your new MoonshotAI API key:")
    print("   Format should be: sk-xxxxxxxxxxxxxxxxxxxxxxx")
    print("   (Leave blank to cancel)")
    
    new_key = input("\nAPI Key: ").strip()
    
    if not new_key:
        print("❌ No key entered. Operation cancelled.")
        return
    
    if not new_key.startswith('sk-'):
        print("⚠️ Warning: API key doesn't start with 'sk-'. Continue anyway? (y/N)")
        confirm = input().strip().lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return
    
    # Update the main chatbot file
    file_path = "improved_dual_personality_chatbot.py"
    
    try:
        # Read current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the old API key
        old_key_start = 'moonshot_api_key = "sk-'
        new_key_line = f'moonshot_api_key = "{new_key}"'
        
        if old_key_start in content:
            # Find the line with the old key
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('moonshot_api_key = "sk-'):
                    lines[i] = f'            {new_key_line}'
                    print(f"✅ Found old API key on line {i+1}")
                    break
            
            # Write updated content
            updated_content = '\n'.join(lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ API key updated in {file_path}")
            
        else:
            print(f"⚠️ Could not find old API key in {file_path}")
            print("You may need to update it manually.")
        
        # Also update the MoonshotAI integration file if needed
        moonshot_file = "moonshot_ai_integration.py"
        if os.path.exists(moonshot_file):
            print(f"\n🔍 Checking {moonshot_file}...")
            with open(moonshot_file, 'r', encoding='utf-8') as f:
                moonshot_content = f.read()
            
            if 'sk-or-v1-' in moonshot_content:
                moonshot_content = moonshot_content.replace(
                    '"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"',
                    f'"{new_key}"'
                )
                
                with open(moonshot_file, 'w', encoding='utf-8') as f:
                    f.write(moonshot_content)
                
                print(f"✅ API key also updated in {moonshot_file}")
        
        print(f"\n🧪 Testing new API key...")
        
        # Test the new key
        try:
            from moonshot_ai_integration import MoonshotAIIntegration
            
            test_moonshot = MoonshotAIIntegration(api_key=new_key)
            test_response = test_moonshot.get_crypto_specific_response("Hello, test message")
            
            if test_response:
                print("✅ New API key works! Test response received.")
                print(f"   Model: {test_response.get('model_used', 'N/A')}")
                print(f"   Tokens: {test_response.get('tokens_used', 0)}")
            else:
                print("⚠️ Test response failed. Key may be invalid or have no credits.")
                
        except Exception as e:
            print(f"⚠️ API test failed: {e}")
            print("This might be due to network issues or key problems.")
        
        print(f"\n🎉 API Key Update Complete!")
        print("Your KoinToss AI chatbot is now ready with the new MoonshotAI key!")
        print("\nNext steps:")
        print("1. Test with: python test_moonshot_direct.py")
        print("2. Launch app: streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Error updating API key: {e}")
        print("You may need to update the key manually in the source files.")

if __name__ == "__main__":
    update_api_key()
