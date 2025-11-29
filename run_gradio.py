#!/usr/bin/env python3
"""
Launch script for Gradio application
Handles different deployment scenarios
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import gradio
        import pandas
        from orchestrator import DocumentProcessingOrchestrator
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def launch_local(port=7860, share=False):
    """Launch local Gradio application"""
    print(f"🚀 Launching Gradio app on port {port}")
    print(f"📱 Share mode: {'Enabled' if share else 'Disabled'}")
    
    if share:
        print("🌐 Public URL will be generated automatically")
        print("📤 Share the URL with anyone for remote access")
    
    # Import and run the app
    from gradio_app import demo
    
    demo.queue()  # Enable queue for multiple users
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=share,
        show_error=True,
        debug=False,
        show_api=True
    )

def launch_remote():
    """Launch with remote sharing enabled"""
    print("🌐 Launching with remote sharing enabled...")
    print("📤 A public URL will be generated for sharing")
    launch_local(port=7860, share=True)

def launch_enterprise(port=7860):
    """Launch for enterprise deployment"""
    print("🏢 Launching for enterprise deployment...")
    print(f"🔒 Running on port {port} (no public sharing)")
    print("📊 Ready for internal HP network access")
    launch_local(port=port, share=False)

def main():
    parser = argparse.ArgumentParser(description="Launch DOC Anomaly Detection Gradio App")
    parser.add_argument(
        "--mode", 
        choices=["local", "remote", "enterprise"], 
        default="local",
        help="Deployment mode (default: local)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=7860,
        help="Port number (default: 7860)"
    )
    
    args = parser.parse_args()
    
    print("🤖 DOC Anomaly Detection System - Gradio Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if sample data exists
    sample_dir = Path("sample_data")
    if not sample_dir.exists():
        print("⚠️  Sample data directory not found")
        print("Run: python create_sample_data.py")
    else:
        print("✅ Sample data available")
    
    # Launch based on mode
    if args.mode == "local":
        launch_local(port=args.port, share=False)
    elif args.mode == "remote":
        launch_remote()
    elif args.mode == "enterprise":
        launch_enterprise(port=args.port)

if __name__ == "__main__":
    main()
