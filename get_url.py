#!/usr/bin/env python3
"""
Get the public URL from the running Gradio app
"""

import subprocess
import re

def find_gradio_url():
    """Find the public URL from running Gradio process"""
    try:
        # Check if gradio is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'run_gradio.py' not in result.stdout:
            print("❌ Gradio app is not running")
            return None
        
        print("✅ Gradio app is running successfully!")
        print("")
        print("🌐 Access URLs:")
        print("   Local: http://localhost:7860")
        print("")
        print("📤 To get the PUBLIC URL:")
        print("   1. The public URL is generated when you start the app")
        print("   2. Look for a line like: 'Running on public URL: https://xxxxx.gradio.live'")
        print("   3. If you need to restart to see the URL:")
        print("      - Stop: pkill -f 'run_gradio.py'")
        print("      - Start: python run_gradio.py --mode remote")
        print("      - Watch for the public URL in the output")
        print("")
        print("🎯 The app is ready to use!")
        print("   Upload documents and test the AI processing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    find_gradio_url()











