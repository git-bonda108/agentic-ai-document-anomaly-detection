#!/usr/bin/env python3
"""
Immediate deployment script - starts app and shows public URL
"""

import subprocess
import time
import sys
import os

def deploy_with_public_url():
    """Deploy app and capture public URL"""
    print("🚀 Starting DOC Anomaly Detection System...")
    print("=" * 50)
    
    # Kill any existing instances
    subprocess.run(['pkill', '-f', 'run_gradio.py'], capture_output=True)
    time.sleep(2)
    
    print("🌐 Launching with remote sharing enabled...")
    print("📤 Public URL will be generated automatically")
    print("")
    print("⏳ Starting application... (this may take 10-15 seconds)")
    
    try:
        # Start the app and capture output
        process = subprocess.Popen(
            ['python', 'run_gradio.py', '--mode', 'remote'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        public_url = None
        local_url = "http://localhost:7860"
        
        # Monitor output for public URL
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            
            # Look for public URL
            if "Running on public URL:" in line:
                public_url = line.split("Running on public URL:")[-1].strip()
                break
            elif "gradio.live" in line:
                public_url = line.strip()
                break
        
        if public_url:
            print("\n" + "=" * 60)
            print("🎉 DEPLOYMENT SUCCESSFUL!")
            print("=" * 60)
            print(f"🌐 PUBLIC URL: {public_url}")
            print(f"🏠 LOCAL URL: {local_url}")
            print("=" * 60)
            print("📤 Share the PUBLIC URL with anyone, anywhere!")
            print("🌍 The app is accessible from any device with internet")
            print("⏰ Keep this terminal open to keep the app running")
            print("=" * 60)
            
            # Keep the process running
            process.wait()
            
        else:
            print("\n⚠️  App started but public URL not detected")
            print(f"🏠 Try accessing locally: {local_url}")
            process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    deploy_with_public_url()











