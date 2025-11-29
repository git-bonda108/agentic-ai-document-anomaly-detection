#!/usr/bin/env python3
"""
Deployment script for Hugging Face Spaces
Creates all necessary files for HF Spaces deployment
"""

import os
import shutil
from pathlib import Path

def create_hf_space_files():
    """Create files needed for Hugging Face Spaces deployment"""
    
    print("🌐 Preparing files for Hugging Face Spaces deployment...")
    
    # Create HF Space configuration
    readme_content = """---
title: DOC Anomaly Detection System
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: gradio_app.py
pinned: false
license: mit
short_description: Agentic AI system for document anomaly detection in HP enterprise environment
---

# 🤖 DOC Anomaly Detection System

**Agentic AI System** for processing invoices and contracts with advanced anomaly detection capabilities.

## Features

- 🤖 **4 Specialized AI Agents** working autonomously
- 📄 **Multi-format Support** - PDF, DOCX, DOC, Images
- 🚨 **Advanced Anomaly Detection** - PO mismatch, date issues, duplicates
- 📊 **Real-time Processing** with confidence scoring
- 🌐 **Remote Access** - Shareable public URL

## How to Use

1. **Upload Document** - Drag and drop your file
2. **Process** - Click "Process Document" 
3. **Review Results** - Check extracted data and anomalies
4. **Take Action** - Address any detected issues

## Anomaly Types Detected

- 🔍 **PO Mismatch** - Purchase order inconsistencies
- 📅 **Date Discrepancies** - Cross-document validation
- 📊 **Lease Schedule Issues** - Payment vs contract terms
- 🔄 **Duplicate Documents** - Similar content detection
- 💰 **Amount Anomalies** - Unusual amounts and calculations
- 📝 **Format Issues** - Non-standard document formats

## Enterprise Features

- **Agentic AI Architecture** - Autonomous processing
- **Business Rule Engine** - Configurable thresholds
- **Confidence Scoring** - AI-powered accuracy metrics
- **Audit Trail** - Complete logging of agent actions
- **Scalable Design** - Ready for enterprise deployment

**Built for HP Enterprise Solutions** | **Powered by Agentic AI**
"""
    
    # Write README.md for HF Space
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README.md for HF Space")
    
    # Copy necessary files
    files_to_copy = [
        "gradio_app.py",
        "orchestrator.py", 
        "agents/",
        "requirements.txt",
        "sample_data/"
    ]
    
    print("📁 Files ready for deployment:")
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
    
    # Create deployment instructions
    deployment_instructions = """
# 🚀 Hugging Face Spaces Deployment Instructions

## Step 1: Create HF Space
1. Go to https://huggingface.co/new-space
2. Choose name: `doc-anomaly-detection`
3. Select SDK: **Gradio**
4. Set visibility: **Public** (for sharing)

## Step 2: Upload Files
Upload these files to your HF Space:

### Core Application Files
- `gradio_app.py` - Main Gradio application
- `orchestrator.py` - Processing orchestrator
- `requirements.txt` - Dependencies

### Agent Directory
- `agents/` - Complete directory with all agent files

### Sample Data
- `sample_data/` - Sample documents for testing

### Configuration
- `README.md` - Space description and documentation

## Step 3: Deploy
1. HF Spaces will automatically build and deploy
2. Wait for "Building" to complete (5-10 minutes)
3. Your app will be live at: `https://huggingface.co/spaces/[username]/doc-anomaly-detection`

## Step 4: Share
- Copy the public URL
- Share with HP stakeholders
- Use for demos and presentations

## Troubleshooting

### Build Failures
- Check `requirements.txt` for version conflicts
- Ensure all dependencies are compatible
- Review build logs for specific errors

### Runtime Errors
- Verify all files are uploaded correctly
- Check agent imports and dependencies
- Test with sample documents first

### Performance Issues
- HF Spaces has resource limits
- Optimize for concurrent users
- Consider upgrading to paid tier for production

## Customization

### Branding
- Update title and description in `README.md`
- Modify colors in `gradio_app.py` theme settings
- Add HP logo and branding elements

### Features
- Add authentication for enterprise use
- Implement custom business rules
- Add additional document types

## Support
- HF Spaces Documentation: https://huggingface.co/docs/hub/spaces
- Gradio Documentation: https://gradio.app/docs
- Issues: Create GitHub issue or HF Space discussion
"""
    
    with open("DEPLOYMENT_INSTRUCTIONS.md", "w") as f:
        f.write(deployment_instructions)
    
    print("✅ Created DEPLOYMENT_INSTRUCTIONS.md")
    
    print("\n🎉 Ready for Hugging Face Spaces deployment!")
    print("\n📋 Next steps:")
    print("1. Go to https://huggingface.co/new-space")
    print("2. Create new Gradio space")
    print("3. Upload all files from this directory")
    print("4. Wait for deployment to complete")
    print("5. Share your public URL!")

def main():
    print("🤖 DOC Anomaly Detection System - HF Spaces Deployment")
    print("=" * 60)
    
    create_hf_space_files()

if __name__ == "__main__":
    main()




