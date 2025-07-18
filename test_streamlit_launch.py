#!/usr/bin/env python3
"""
Simple test to launch the Streamlit app and check for issues
"""

import subprocess
import sys
import time
import os
import signal

def test_streamlit_launch():
    """Test if Streamlit app can be launched without immediate errors"""
    print("🚀 Testing Streamlit App Launch")
    print("=" * 40)
    
    try:
        # Start the streamlit app
        print("Starting streamlit app...")
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds to see if it starts successfully
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Streamlit app started successfully!")
            print("✅ Process is running without immediate errors")
            
            # Kill the process
            if os.name == 'nt':  # Windows
                process.terminate()
            else:  # Unix-like
                process.send_signal(signal.SIGTERM)
            
            process.wait()
            return True
        else:
            print("❌ Streamlit app failed to start")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error launching streamlit: {e}")
        return False

if __name__ == "__main__":
    success = test_streamlit_launch()
    if success:
        print("\n🎉 App can be launched successfully!")
        print("To run the app, use: streamlit run streamlit_app.py")
    else:
        print("\n⚠️ App has launch issues - check the errors above")
