#!/usr/bin/env python3
"""
Complete setup script for Gradio version
Handles dependencies, sample data, and testing
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please use Python 3.8 or higher")
        return False

def setup_virtual_environment():
    """Set up virtual environment"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    print("🔄 Creating virtual environment...")
    return run_command("python -m venv venv", "Virtual environment creation")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Activate virtual environment and install
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    
    return run_command(install_cmd, "Dependencies installation")

def create_sample_data():
    """Create sample data if it doesn't exist"""
    sample_dir = Path("sample_data")
    if sample_dir.exists() and list(sample_dir.glob("*.pdf")):
        print("✅ Sample data already exists")
        return True
    
    print("📄 Creating sample data...")
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    create_cmd = f"{activate_cmd} && python create_sample_data.py"
    
    return run_command(create_cmd, "Sample data creation")

def test_gradio_imports():
    """Test if Gradio and all components can be imported"""
    print("🧪 Testing imports...")
    
    test_script = """
import sys
try:
    import gradio
    import pandas
    from orchestrator import DocumentProcessingOrchestrator
    from agents import DocumentIngestionAgent, ExtractionAgent, AnomalyDetectionAgent
    print("✅ All imports successful")
    sys.exit(0)
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    test_cmd = f"{activate_cmd} && python test_imports.py"
    
    success = run_command(test_cmd, "Import testing")
    
    # Clean up test file
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")
    
    return success

def create_launch_scripts():
    """Create convenient launch scripts"""
    
    # Create local launch script
    local_script = """#!/bin/bash
# Launch Gradio app locally
source venv/bin/activate
python gradio_app.py
"""
    
    with open("launch_local.sh", "w") as f:
        f.write(local_script)
    os.chmod("launch_local.sh", 0o755)
    
    # Create remote launch script
    remote_script = """#!/bin/bash
# Launch Gradio app with remote sharing
source venv/bin/activate
python run_gradio.py --mode remote
"""
    
    with open("launch_remote.sh", "w") as f:
        f.write(remote_script)
    os.chmod("launch_remote.sh", 0o755)
    
    print("✅ Created launch scripts")

def show_next_steps():
    """Show next steps to the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("\n1. 🚀 Launch locally:")
    print("   ./launch_local.sh")
    print("   # or")
    print("   python run_gradio.py --mode local")
    
    print("\n2. 🌐 Launch with remote sharing:")
    print("   ./launch_remote.sh")
    print("   # or")
    print("   python run_gradio.py --mode remote")
    
    print("\n3. 🏢 Launch for enterprise:")
    print("   python run_gradio.py --mode enterprise --port 8080")
    
    print("\n4. 🌐 Deploy to Hugging Face Spaces:")
    print("   python deploy_to_hf.py")
    print("   # Follow instructions in DEPLOYMENT_INSTRUCTIONS.md")
    
    print("\n📊 Test with sample documents:")
    print("   - sample_data/invoice_001_normal.pdf")
    print("   - sample_data/contract_002_normal.pdf")
    print("   - sample_data/invoice_003_anomalies.pdf")
    
    print("\n📖 Documentation:")
    print("   - README_GRADIO.md - Complete Gradio documentation")
    print("   - DEPLOYMENT_INSTRUCTIONS.md - HF Spaces deployment")
    print("   - ARCHITECTURE.md - System architecture")

def main():
    print("🤖 DOC Anomaly Detection System - Gradio Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create sample data
    if not create_sample_data():
        sys.exit(1)
    
    # Test imports
    if not test_gradio_imports():
        sys.exit(1)
    
    # Create launch scripts
    create_launch_scripts()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()




