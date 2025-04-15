import os
import webbrowser
import subprocess
import time
import signal
import sys

def kill_existing_servers():
    """Kill any existing Python processes"""
    if sys.platform == 'win32':
        os.system('taskkill /F /IM python.exe 2>nul')
    else:
        os.system('pkill -f "python.*Krypt.py"')

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    # Start server in a new process
    server = subprocess.Popen(['python', 'Krypt.py'])
    time.sleep(2)  # Give the server time to start
    return server

def open_browser():
    """Open the example.html in browser"""
    print("Opening example.html in browser...")
    file_path = os.path.abspath('example.html')
    webbrowser.open('file://' + file_path)

def main():
    try:
        # Kill any existing servers
        kill_existing_servers()
        time.sleep(1)
        
        # Start new server
        server = start_server()
        
        # Open browser
        time.sleep(2)  # Wait for server to be fully ready
        open_browser()
        
        print("\nServer is running. Press Ctrl+C to stop...")
        server.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        if 'server' in locals():
            server.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()