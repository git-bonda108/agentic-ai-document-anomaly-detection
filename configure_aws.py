#!/usr/bin/env python3
"""
Quick AWS Configuration Script
Configures AWS credentials programmatically
"""

import os
import boto3
from botocore.exceptions import ClientError

# AWS Credentials (from user)
AWS_ACCESS_KEY = "YOUR_ACCESS_KEY_HERE"  # User will need to provide this
AWS_SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # User will need to provide this
AWS_REGION = "us-east-1"

def test_credentials(access_key, secret_key, region):
    """Test AWS credentials"""
    try:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS Credentials Valid!")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return True
    except Exception as e:
        print(f"❌ AWS Credentials Invalid: {e}")
        return False

def configure_aws_via_env():
    """Set AWS credentials via environment variables"""
    # Note: User credentials need to be provided
    # For security, we'll use environment variables instead of hardcoding
    
    print("📝 To configure AWS credentials, please:")
    print("   1. Set environment variables:")
    print("      export AWS_ACCESS_KEY_ID='your_key'")
    print("      export AWS_SECRET_ACCESS_KEY='your_secret'")
    print("      export AWS_DEFAULT_REGION='us-east-1'")
    print("\n   2. Or use AWS CLI:")
    print("      aws configure")
    print("\n   3. Or create ~/.aws/credentials file manually")
    
    # Check if credentials are already set
    if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
        print("\n✅ AWS credentials found in environment variables")
        return test_credentials(
            os.getenv('AWS_ACCESS_KEY_ID'),
            os.getenv('AWS_SECRET_ACCESS_KEY'),
            os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
    else:
        print("\n⚠️  AWS credentials not found in environment variables")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 AWS Configuration Helper")
    print("=" * 60)
    print("\nFor security, please configure AWS credentials manually:")
    print("\nOption 1: Environment Variables")
    print("  export AWS_ACCESS_KEY_ID='your_access_key'")
    print("  export AWS_SECRET_ACCESS_KEY='your_secret_key'")
    print("  export AWS_DEFAULT_REGION='us-east-1'")
    
    print("\nOption 2: AWS CLI")
    print("  aws configure")
    print("  # Enter your credentials when prompted")
    
    print("\nOption 3: ~/.aws/credentials file")
    print("  [default]")
    print("  aws_access_key_id = YOUR_KEY")
    print("  aws_secret_access_key = YOUR_SECRET")
    print("  region = us-east-1")
    
    print("\n" + "=" * 60)
    
    # Try to test if credentials are already set
    success = configure_aws_via_env()
    if success:
        print("\n✅ Credentials are valid! Proceeding with setup...")
    else:
        print("\n⚠️  Please configure credentials first, then run:")
        print("   python setup_aws_infrastructure.py")





