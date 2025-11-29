#!/usr/bin/env python3
"""
Script to get the public URL from Gradio output
"""

import subprocess
import time
import re

def get_gradio_public_url():
    """Get the public URL from running Gradio app"""
    try:
        # Check if gradio is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'run_gradio.py' not in result.stdout:
            print("❌ Gradio app is not running")
            print("💡 Start it with: python run_gradio.py --mode remote")
            return None
        
        print("✅ Gradio app is running")
        print("🌐 Local URL: http://localhost:7860")
        print("")
        print("📤 To get the public URL, check the terminal where you started the app.")
        print("   Look for a line like: 'Running on public URL: https://xxxxx.gradio.live'")
        print("")
        print("🔄 If you need to restart with public URL:")
        print("   1. Stop current app: pkill -f 'run_gradio.py'")
        print("   2. Start with remote: python run_gradio.py --mode remote")
        print("   3. Copy the public URL from the output")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    get_gradio_public_url()











