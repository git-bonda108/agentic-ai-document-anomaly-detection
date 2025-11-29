#!/usr/bin/env python3
"""
Test AWS Access Script
Tests IAM credentials and creates necessary infrastructure
"""

import boto3
import os
import sys
from botocore.exceptions import ClientError, NoCredentialsError

def test_aws_credentials():
    """Test AWS credentials"""
    print("=" * 60)
    print("🔐 Testing AWS Access")
    print("=" * 60)
    
    # Try to get credentials from environment
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    if not access_key or not secret_key:
        print("❌ AWS credentials not found in environment variables")
        print("\nPlease set:")
        print("  export AWS_ACCESS_KEY_ID='your_access_key'")
        print("  export AWS_SECRET_ACCESS_KEY='your_secret_key'")
        print("  export AWS_REGION='us-east-1'")
        return False
    
    try:
        # Test credentials with STS
        print(f"\n📋 Testing credentials...")
        print(f"   Access Key: {access_key[:10]}...")
        print(f"   Region: {region}")
        
        sts = boto3.client(
            'sts',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        # Get caller identity
        identity = sts.get_caller_identity()
        
        print("\n✅ AWS Credentials Valid!")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        print(f"   User ID: {identity.get('UserId', 'N/A')}")
        
        # Test S3 access
        print("\n📦 Testing S3 access...")
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        try:
            buckets = s3.list_buckets()
            print(f"   ✅ Can list buckets ({len(buckets.get('Buckets', []))} buckets found)")
        except ClientError as e:
            print(f"   ⚠️  S3 ListBuckets permission: {e}")
        
        # Test DynamoDB access
        print("\n🗄️  Testing DynamoDB access...")
        dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        try:
            tables = dynamodb.list_tables()
            print(f"   ✅ Can list tables ({len(tables.get('TableNames', []))} tables found)")
        except ClientError as e:
            print(f"   ⚠️  DynamoDB ListTables permission: {e}")
        
        # Test CloudWatch access
        print("\n📊 Testing CloudWatch access...")
        logs = boto3.client(
            'logs',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        try:
            log_groups = logs.describe_log_groups(limit=1)
            print(f"   ✅ Can access CloudWatch Logs")
        except ClientError as e:
            print(f"   ⚠️  CloudWatch Logs permission: {e}")
        
        return True
        
    except NoCredentialsError:
        print("❌ No AWS credentials found")
        return False
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidUserID.NotFound':
            print(f"❌ Invalid credentials: {e}")
        elif error_code == 'AccessDenied':
            print(f"⚠️  Access denied - credentials valid but insufficient permissions")
            print(f"   Error: {e}")
        else:
            print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_permissions():
    """Check required IAM permissions"""
    print("\n" + "=" * 60)
    print("📋 Required IAM Permissions")
    print("=" * 60)
    
    required_permissions = {
        "S3": [
            "s3:CreateBucket",
            "s3:PutObject",
            "s3:GetObject",
            "s3:ListBucket",
            "s3:DeleteObject"
        ],
        "DynamoDB": [
            "dynamodb:CreateTable",
            "dynamodb:PutItem",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:ListTables"
        ],
        "CloudWatch": [
            "logs:CreateLogGroup",
            "logs:PutLogEvents",
            "logs:DescribeLogGroups"
        ],
        "STS": [
            "sts:GetCallerIdentity"
        ]
    }
    
    for service, permissions in required_permissions.items():
        print(f"\n{service}:")
        for perm in permissions:
            print(f"  • {perm}")

if __name__ == "__main__":
    print("\n🚀 AWS Access Test for DOC Anomaly Detection System\n")
    
    # Check required permissions
    check_permissions()
    
    print("\n" + "=" * 60)
    print("Starting tests...")
    print("=" * 60)
    
    success = test_aws_credentials()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ AWS Access Test Complete")
        print("\n📝 Next Steps:")
        print("1. Run: python setup_aws_infrastructure.py")
        print("2. Verify S3 buckets and DynamoDB tables created")
        print("3. Test document processing")
    else:
        print("❌ AWS Access Test Failed")
        print("\n📝 Required Actions:")
        print("1. Get AWS Access Key ID and Secret Access Key")
        print("2. Set environment variables:")
        print("   export AWS_ACCESS_KEY_ID='your_key'")
        print("   export AWS_SECRET_ACCESS_KEY='your_secret'")
        print("   export AWS_REGION='us-east-1'")
        print("3. Ensure IAM user has required permissions (see above)")
        print("4. Re-run this script to verify")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)

