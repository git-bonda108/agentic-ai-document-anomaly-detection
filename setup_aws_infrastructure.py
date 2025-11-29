#!/usr/bin/env python3
"""
AWS Infrastructure Setup Script
Creates S3 buckets, DynamoDB tables, and CloudWatch log groups
"""

import boto3
import os
from botocore.exceptions import ClientError
import json

# AWS Configuration
AWS_ACCOUNT_ID = "597088017095"
AWS_REGION = "us-east-1"

# Bucket names
BUCKETS = [
    f"doc-anomaly-raw-docs-{AWS_ACCOUNT_ID}",
    f"doc-anomaly-processed-{AWS_ACCOUNT_ID}",
    f"doc-anomaly-embeddings-{AWS_ACCOUNT_ID}",
    f"doc-anomaly-ml-models-{AWS_ACCOUNT_ID}"
]

# DynamoDB Table definitions
DYNAMODB_TABLES = [
    {
        "TableName": "DocumentMetadata",
        "KeySchema": [
            {"AttributeName": "document_id", "KeyType": "HASH"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "document_id", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "ContractInvoiceMapping",
        "KeySchema": [
            {"AttributeName": "contract_id", "KeyType": "HASH"},
            {"AttributeName": "invoice_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "contract_id", "AttributeType": "S"},
            {"AttributeName": "invoice_id", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "AnomalyResults",
        "KeySchema": [
            {"AttributeName": "document_id", "KeyType": "HASH"},
            {"AttributeName": "anomaly_timestamp", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "document_id", "AttributeType": "S"},
            {"AttributeName": "anomaly_timestamp", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "BusinessRules",
        "KeySchema": [
            {"AttributeName": "rule_id", "KeyType": "HASH"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "rule_id", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "HumanFeedback",
        "KeySchema": [
            {"AttributeName": "document_id", "KeyType": "HASH"},
            {"AttributeName": "feedback_timestamp", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "document_id", "AttributeType": "S"},
            {"AttributeName": "feedback_timestamp", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "ValidationResults",
        "KeySchema": [
            {"AttributeName": "document_id", "KeyType": "HASH"},
            {"AttributeName": "validation_timestamp", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "document_id", "AttributeType": "S"},
            {"AttributeName": "validation_timestamp", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST"
    }
]

def test_aws_credentials():
    """Test AWS credentials by getting caller identity"""
    try:
        # Try multiple credential sources
        sts = None
        # Try default credential chain first
        try:
            sts = boto3.client('sts', region_name=AWS_REGION)
        except:
            # Try environment variables
            if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
                sts = boto3.client(
                    'sts',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION', AWS_REGION)
                )
        
        if sts:
            identity = sts.get_caller_identity()
            print(f"✅ AWS Credentials Valid!")
            print(f"   Account ID: {identity['Account']}")
            print(f"   User ARN: {identity['Arn']}")
            return True
        else:
            raise Exception("No credentials found")
    except Exception as e:
        print(f"❌ AWS Credentials Invalid: {e}")
        print("\n   Please configure credentials using one of:")
        print("   1. AWS CLI: aws configure")
        print("   2. Environment variables:")
        print("      export AWS_ACCESS_KEY_ID='your_key'")
        print("      export AWS_SECRET_ACCESS_KEY='your_secret'")
        print("      export AWS_REGION='us-east-1'")
        print("   3. ~/.aws/credentials file")
        return False

def create_s3_buckets(s3_client):
    """Create S3 buckets for document storage"""
    print("\n📦 Creating S3 Buckets...")
    created = []
    existing = []
    
    for bucket_name in BUCKETS:
        try:
            # Check if bucket exists
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                print(f"   ⚠️  Bucket already exists: {bucket_name}")
                existing.append(bucket_name)
                continue
            except ClientError:
                pass
            
            # Create bucket
            if AWS_REGION == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
                )
            
            # Enable versioning
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            
            print(f"   ✅ Created: {bucket_name}")
            created.append(bucket_name)
            
        except Exception as e:
            print(f"   ❌ Error creating {bucket_name}: {e}")
    
    return created, existing

def create_dynamodb_tables(dynamodb_client):
    """Create DynamoDB tables"""
    print("\n🗄️  Creating DynamoDB Tables...")
    created = []
    existing = []
    
    for table_def in DYNAMODB_TABLES:
        table_name = table_def["TableName"]
        try:
            # Check if table exists
            try:
                response = dynamodb_client.describe_table(TableName=table_name)
                print(f"   ⚠️  Table already exists: {table_name}")
                existing.append(table_name)
                continue
            except ClientError:
                pass
            
            # Create table
            dynamodb_client.create_table(**table_def)
            print(f"   ✅ Created: {table_name}")
            created.append(table_name)
            
        except Exception as e:
            print(f"   ❌ Error creating {table_name}: {e}")
    
    # Wait for tables to be active
    if created:
        print("\n   ⏳ Waiting for tables to be active...")
        waiter = dynamodb_client.get_waiter('table_exists')
        for table_name in created:
            try:
                waiter.wait(TableName=table_name)
                print(f"   ✅ {table_name} is active")
            except Exception as e:
                print(f"   ⚠️  {table_name} may not be active yet: {e}")
    
    return created, existing

def seed_business_rules(dynamodb_resource):
    """Seed initial business rules"""
    print("\n📋 Seeding Business Rules...")
    
    business_rules = {
        "date_variance_days": {
            "rule_id": "date_variance_days",
            "rule_name": "Date Variance Tolerance",
            "rule_value": 30,
            "rule_type": "threshold",
            "description": "Maximum allowed days variance between contract dates and invoice dates"
        },
        "amount_variance_percent": {
            "rule_id": "amount_variance_percent",
            "rule_name": "Amount Variance Tolerance",
            "rule_value": 5,
            "rule_type": "threshold",
            "description": "Maximum allowed percentage variance between contract amounts and invoice amounts"
        },
        "schedule_miss_tolerance_days": {
            "rule_id": "schedule_miss_tolerance_days",
            "rule_name": "Schedule Miss Tolerance",
            "rule_value": 5,
            "rule_type": "threshold",
            "description": "Maximum allowed days for payment schedule misses"
        },
        "surplus_payment_threshold_percent": {
            "rule_id": "surplus_payment_threshold_percent",
            "rule_name": "Surplus Payment Threshold",
            "rule_value": 10,
            "rule_type": "threshold",
            "description": "Maximum allowed percentage for surplus payments"
        },
        "missed_payment_grace_days": {
            "rule_id": "missed_payment_grace_days",
            "rule_name": "Missed Payment Grace Period",
            "rule_value": 10,
            "rule_type": "threshold",
            "description": "Grace period in days before considering a payment as missed"
        },
        "lease_payment_variance_percent": {
            "rule_id": "lease_payment_variance_percent",
            "rule_name": "Lease Payment Variance",
            "rule_value": 3,
            "rule_type": "threshold",
            "description": "Maximum allowed percentage variance for lease payments"
        }
    }
    
    table = dynamodb_resource.Table("BusinessRules")
    inserted = 0
    
    for rule_id, rule_data in business_rules.items():
        try:
            table.put_item(Item=rule_data)
            print(f"   ✅ Inserted rule: {rule_data['rule_name']}")
            inserted += 1
        except Exception as e:
            print(f"   ⚠️  Error inserting {rule_id}: {e}")
    
    return inserted

def create_cloudwatch_log_groups(logs_client):
    """Create CloudWatch log groups"""
    print("\n📊 Creating CloudWatch Log Groups...")
    
    log_groups = [
        "/aws/doc-anomaly/orchestrator",
        "/aws/doc-anomaly/ingestion",
        "/aws/doc-anomaly/extraction",
        "/aws/doc-anomaly/contract-invoice",
        "/aws/doc-anomaly/anomaly-detection",
        "/aws/doc-anomaly/validation"
    ]
    
    created = []
    
    for log_group in log_groups:
        try:
            logs_client.create_log_group(logGroupName=log_group)
            # Set retention to 7 days for cost optimization
            logs_client.put_retention_policy(
                logGroupName=log_group,
                retentionInDays=7
            )
            print(f"   ✅ Created: {log_group}")
            created.append(log_group)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f"   ⚠️  Log group already exists: {log_group}")
            else:
                print(f"   ❌ Error creating {log_group}: {e}")
    
    return created

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 AWS Infrastructure Setup for DOC Anomaly Detection")
    print("=" * 60)
    
    # Test credentials first
    if not test_aws_credentials():
        print("\n❌ Cannot proceed without valid AWS credentials")
        print("   Please configure AWS credentials:")
        print("   aws configure")
        return False
    
    try:
        # Initialize clients
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        dynamodb_client = boto3.client('dynamodb', region_name=AWS_REGION)
        dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)
        logs_client = boto3.client('logs', region_name=AWS_REGION)
        
        # Create resources
        buckets_created, buckets_existing = create_s3_buckets(s3_client)
        tables_created, tables_existing = create_dynamodb_tables(dynamodb_client)
        rules_inserted = seed_business_rules(dynamodb_resource)
        log_groups_created = create_cloudwatch_log_groups(logs_client)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ Infrastructure Setup Complete!")
        print("=" * 60)
        print(f"\n📦 S3 Buckets: {len(buckets_created)} created, {len(buckets_existing)} existing")
        print(f"🗄️  DynamoDB Tables: {len(tables_created)} created, {len(tables_existing)} existing")
        print(f"📋 Business Rules: {rules_inserted} rules inserted")
        print(f"📊 CloudWatch Log Groups: {len(log_groups_created)} created")
        
        # Save configuration
        config = {
            "buckets": {
                "raw_docs": BUCKETS[0],
                "processed": BUCKETS[1],
                "embeddings": BUCKETS[2],
                "ml_models": BUCKETS[3]
            },
            "tables": {
                "documents": "DocumentMetadata",
                "contract_invoice_mapping": "ContractInvoiceMapping",
                "anomalies": "AnomalyResults",
                "business_rules": "BusinessRules",
                "human_feedback": "HumanFeedback",
                "validation_results": "ValidationResults"
            },
            "region": AWS_REGION,
            "account_id": AWS_ACCOUNT_ID
        }
        
        with open("aws_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"\n💾 Configuration saved to aws_config.json")
        print("\n✅ Ready to proceed with agent development!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

