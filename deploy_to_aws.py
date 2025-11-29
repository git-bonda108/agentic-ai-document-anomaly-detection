#!/usr/bin/env python3
"""
AWS Deployment Script
Prepares and deploys Streamlit app to AWS EC2/ECS
"""

import os
import sys
import json
import boto3
from pathlib import Path

def create_dockerfile():
    """Create Dockerfile for deployment"""
    dockerfile_content = """FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    tesseract-ocr \\
    libtesseract-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Created Dockerfile")

def create_requirements_deploy():
    """Create requirements file for deployment"""
    requirements = """# Core dependencies
streamlit>=1.28.0
openai>=1.3.0
boto3>=1.28.0
python-dotenv>=1.0.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0

# Visualization
plotly>=5.17.0

# Document processing
PyPDF2>=3.0.0
python-docx>=0.8.11
Pillow>=10.0.0
pytesseract>=0.3.10

# ML
scikit-learn>=1.3.0

# Text processing
nltk>=3.8.0
spacy>=3.6.0
"""
    
    with open("requirements_deploy.txt", "w") as f:
        f.write(requirements)
    
    print("✅ Created requirements_deploy.txt")

def create_ec2_deploy_script():
    """Create EC2 deployment script"""
    script_content = """#!/bin/bash
# EC2 Deployment Script for DOC Anomaly Detection System

echo "🚀 Deploying to EC2..."

# Update system
sudo apt-get update
sudo apt-get install -y python3.13 python3-pip git docker.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone or copy code
if [ ! -d "doc-anomaly-detection" ]; then
    git clone <your-repo-url> doc-anomaly-detection
    cd doc-anomaly-detection
else
    cd doc-anomaly-detection
    git pull
fi

# Set environment variables (replace with your actual credentials)
export AWS_ACCESS_KEY_ID='your_aws_access_key_here'
export AWS_SECRET_ACCESS_KEY='your_aws_secret_key_here'
export AWS_REGION='us-east-1'
export OPENAI_API_KEY='your_openai_api_key_here'

# Build and run with Docker
docker build -t doc-anomaly-detection .
docker run -d \\
    -p 8501:8501 \\
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \\
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \\
    -e AWS_REGION=$AWS_REGION \\
    -e OPENAI_API_KEY=$OPENAI_API_KEY \\
    doc-anomaly-detection

echo "✅ Deployment complete!"
echo "Access app at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8501"
"""
    
    with open("deploy_ec2.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("deploy_ec2.sh", 0o755)
    print("✅ Created deploy_ec2.sh")

def create_ecs_task_definition():
    """Create ECS task definition JSON"""
    task_def = {
        "family": "doc-anomaly-detection",
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "1024",
        "memory": "2048",
        "containerDefinitions": [
            {
                "name": "doc-anomaly-detection",
                "image": "<your-ecr-repo>/doc-anomaly-detection:latest",
                "essential": True,
                "portMappings": [
                    {
                        "containerPort": 8501,
                        "protocol": "tcp"
                    }
                ],
                "environment": [
                    {"name": "AWS_REGION", "value": "us-east-1"},
                    {"name": "AWS_ACCOUNT_ID", "value": "597088017095"}
                ],
                "secrets": [
                    {
                        "name": "AWS_ACCESS_KEY_ID",
                        "valueFrom": "arn:aws:secretsmanager:us-east-1:597088017095:secret:doc-anomaly/aws-key"
                    },
                    {
                        "name": "AWS_SECRET_ACCESS_KEY",
                        "valueFrom": "arn:aws:secretsmanager:us-east-1:597088017095:secret:doc-anomaly/aws-secret"
                    },
                    {
                        "name": "OPENAI_API_KEY",
                        "valueFrom": "arn:aws:secretsmanager:us-east-1:597088017095:secret:doc-anomaly/openai-key"
                    }
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/doc-anomaly-detection",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs"
                    }
                }
            }
        ]
    }
    
    with open("ecs-task-definition.json", "w") as f:
        json.dump(task_def, f, indent=2)
    
    print("✅ Created ecs-task-definition.json")

def main():
    """Main deployment preparation"""
    print("=" * 60)
    print("🚀 AWS Deployment Preparation")
    print("=" * 60)
    
    create_dockerfile()
    create_requirements_deploy()
    create_ec2_deploy_script()
    create_ecs_task_definition()
    
    print("\n" + "=" * 60)
    print("✅ Deployment files created!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Option A - EC2:")
    print("   - Launch EC2 instance (t3.medium or larger)")
    print("   - Copy code and run: bash deploy_ec2.sh")
    print("\n2. Option B - ECS Fargate:")
    print("   - Build Docker image")
    print("   - Push to ECR")
    print("   - Create ECS service using ecs-task-definition.json")
    print("\n3. Option C - Elastic Beanstalk:")
    print("   - Install EB CLI: pip install awsebcli")
    print("   - Run: eb init && eb create && eb deploy")

if __name__ == "__main__":
    main()





