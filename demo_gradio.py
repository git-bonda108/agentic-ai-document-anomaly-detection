#!/usr/bin/env python3
"""
Demo script for Gradio application
Shows system capabilities and launches with remote sharing
"""

import os
import sys
import time
from pathlib import Path

def show_banner():
    """Display welcome banner"""
    print("=" * 70)
    print("🤖 DOC ANOMALY DETECTION SYSTEM - GRADIO DEMO")
    print("=" * 70)
    print("🏢 Enterprise-Ready Agentic AI System")
    print("🌐 Remote Access & Public URL Generation")
    print("📊 Advanced Anomaly Detection & Processing")
    print("=" * 70)

def check_system_status():
    """Check if system is ready"""
    print("\n🔍 System Status Check...")
    
    # Check Python version
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Check virtual environment
    if os.path.exists("venv"):
        print("✅ Virtual environment ready")
    else:
        print("❌ Virtual environment missing")
        return False
    
    # Check key files
    key_files = [
        "gradio_app.py",
        "orchestrator.py",
        "agents/__init__.py",
        "sample_data/"
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def show_sample_documents():
    """Show available sample documents"""
    print("\n📄 Available Sample Documents:")
    sample_dir = Path("sample_data")
    
    if sample_dir.exists():
        pdf_files = list(sample_dir.glob("*.pdf"))
        if pdf_files:
            for pdf_file in pdf_files:
                size = pdf_file.stat().st_size
                print(f"  📄 {pdf_file.name} ({size:,} bytes)")
        else:
            print("  ⚠️  No PDF files found")
    else:
        print("  ❌ Sample data directory not found")

def show_features():
    """Display system features"""
    print("\n🚀 System Features:")
    print("  🤖 4 Specialized AI Agents")
    print("  📄 Multi-format Document Support (PDF, DOCX, Images)")
    print("  🔍 Advanced Anomaly Detection:")
    print("     • PO Mismatch Detection")
    print("     • Date Discrepancy Validation")
    print("     • Lease Schedule Analysis")
    print("     • Duplicate Document Detection")
    print("     • Amount Validation")
    print("  📊 Real-time Processing with Confidence Scoring")
    print("  🌐 Remote Access via Public URL")
    print("  📱 Mobile-Responsive Interface")

def show_demo_options():
    """Show demo options"""
    print("\n🎯 Demo Options:")
    print("\n1. 🌐 REMOTE DEMO (Recommended)")
    print("   • Creates public shareable URL")
    print("   • Access from anywhere")
    print("   • Perfect for stakeholder presentations")
    print("   • Command: python run_gradio.py --mode remote")
    
    print("\n2. 🏠 LOCAL DEMO")
    print("   • Runs on localhost only")
    print("   • No public URL")
    print("   • Good for testing")
    print("   • Command: python run_gradio.py --mode local")
    
    print("\n3. 🏢 ENTERPRISE DEMO")
    print("   • Internal network access")
    print("   • Custom port configuration")
    print("   • HP network deployment")
    print("   • Command: python run_gradio.py --mode enterprise --port 8080")

def show_expected_results():
    """Show what to expect during demo"""
    print("\n📊 Expected Demo Results:")
    print("\n📄 Normal Documents (invoice_001_normal.pdf, contract_001_normal.pdf):")
    print("  ✅ Clean data extraction")
    print("  ✅ High confidence scores (90%+)")
    print("  ✅ Minimal anomalies detected")
    print("  ✅ Standard format validation passed")
    
    print("\n🚨 Anomaly Document (invoice_003_anomalies.pdf):")
    print("  🔍 PO format anomalies detected")
    print("  🔍 Date discrepancy warnings")
    print("  🔍 Amount calculation issues")
    print("  🔍 Format compliance problems")
    print("  📊 Detailed anomaly reporting with severity levels")

def show_next_steps():
    """Show next steps"""
    print("\n🚀 Ready to Launch!")
    print("\nFor REMOTE DEMO (Recommended):")
    print("  python run_gradio.py --mode remote")
    print("\nThis will:")
    print("  • Launch the Gradio application")
    print("  • Generate a public shareable URL")
    print("  • Enable remote access from anywhere")
    print("  • Perfect for HP stakeholder presentations")

def main():
    """Main demo function"""
    show_banner()
    
    # Check system status
    if not check_system_status():
        print("\n❌ System not ready. Run setup first:")
        print("python setup_gradio.py")
        sys.exit(1)
    
    # Show system information
    show_sample_documents()
    show_features()
    show_demo_options()
    show_expected_results()
    show_next_steps()
    
    print("\n" + "=" * 70)
    print("🎉 System ready for demonstration!")
    print("🌐 Launch with: python run_gradio.py --mode remote")
    print("=" * 70)

if __name__ == "__main__":
    main()




