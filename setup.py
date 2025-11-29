"""
Setup script for DOC Anomaly Detection System
Installs dependencies and creates sample data
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up DOC Anomaly Detection System")
    print("=" * 50)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("   Please activate your virtual environment first:")
        print("   source venv/bin/activate")
        print()
    
    # Install dependencies
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create necessary directories
    directories = ['uploads', 'logs', 'templates', 'static/css', 'static/js', 'sample_data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create sample data
    print("\n📄 Creating sample test data...")
    try:
        import create_sample_data
        create_sample_data.main()
        print("✅ Sample data created successfully")
    except ImportError as e:
        print(f"⚠️  Could not create sample data: {e}")
        print("   You can run 'python create_sample_data.py' later")
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
    
    # Create configuration file
    config_content = """# DOC Anomaly Detection System Configuration

# Database settings
DATABASE_PATH = "doc_anomaly.db"

# File upload settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png', 'tiff']

# Anomaly detection thresholds
THRESHOLDS = {
    'date_variance_days': 30,
    'amount_variance_percent': 10,
    'duplicate_similarity_threshold': 0.8,
    'lease_payment_variance_percent': 5,
    'po_amount_variance_percent': 15
}

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "doc_processing.log"
"""
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("📝 Created configuration file: config.py")
    
    # Create environment file
    env_content = """# Environment variables for DOC Anomaly Detection System
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=doc_anomaly_detection_secret_key_2024
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("🔐 Created environment file: .env")
    
    # Test installation
    print("\n🧪 Testing installation...")
    try:
        from agents import DocumentIngestionAgent, ExtractionAgent, AnomalyDetectionAgent
        from orchestrator import DocumentProcessingOrchestrator
        print("✅ All agents imported successfully")
        
        # Test orchestrator initialization
        orchestrator = DocumentProcessingOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the application: python app.py")
    print("3. Open browser: http://localhost:5000")
    print("4. Upload sample documents from 'sample_data' directory")
    print("\n🔧 For development:")
    print("- Sample data: python create_sample_data.py")
    print("- Test agents: python -c \"from agents import *; print('Agents ready!')\"")
    print("\n📚 Documentation:")
    print("- Architecture: ARCHITECTURE.md")
    print("- README: README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

