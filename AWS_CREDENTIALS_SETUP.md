# AWS Credentials Setup - Step by Step Guide

## ⚠️ IMPORTANT: What You Need

The password you provided (`Krsna&2022`) is for **AWS Console login**, not programmatic access.

**I need:**
- ✅ AWS Access Key ID (starts with `AKIA...`)
- ✅ AWS Secret Access Key (long string)

---

## 📋 Step-by-Step Instructions

### Option 1: Use Existing IAM User (bond-admin)

**Step 1: Log into AWS Console**
1. Go to: https://597088017095.signin.aws.amazon.com/console
2. Or: https://console.aws.amazon.com/
3. Account ID: **597088017095**
4. Username: **bond-admin**
5. Password: **Krsna&2022**

**Step 2: Navigate to IAM**
1. Search for "IAM" in AWS Console
2. Click "IAM" service
3. Click "Users" in left sidebar
4. Find user: **bond-admin**

**Step 3: Check/Create Access Keys**
1. Click on user **bond-admin**
2. Go to "Security credentials" tab
3. Scroll to "Access keys" section
4. Check if access keys exist:
   - **If YES**: Click "Show" to reveal Secret Access Key
   - **If NO**: Click "Create access key"
     - Select use case: "Command Line Interface (CLI)"
     - Click "Next"
     - Click "Create access key"
     - **IMPORTANT**: Copy both:
       - Access Key ID
       - Secret Access Key (shown only once!)
5. Click "Download .csv file" to save credentials

**Step 4: Verify Permissions**
1. Still on user **bond-admin** page
2. Click "Permissions" tab
3. Check if user has these policies attached:
   - **Required Policies**:
     - `AmazonS3FullAccess` (or custom policy with S3 permissions)
     - `AmazonDynamoDBFullAccess` (or custom policy with DynamoDB permissions)
     - `CloudWatchLogsFullAccess` (or custom policy with CloudWatch permissions)
   - **OR** a custom policy with all required permissions

**Step 5: If Permissions Missing**
1. Click "Add permissions"
2. Select "Attach policies directly"
3. Search and attach:
   - `AmazonS3FullAccess`
   - `AmazonDynamoDBFullAccess`
   - `CloudWatchLogsFullAccess`
4. Click "Next"
5. Click "Add permissions"

---

### Option 2: Create New IAM User for Programmatic Access

**Step 1: Create IAM User**
1. In IAM Console, click "Users"
2. Click "Create user"
3. Username: `doc-anomaly-detection`
4. Click "Next"

**Step 2: Attach Permissions**
1. Select "Attach policies directly"
2. Attach these policies:
   - `AmazonS3FullAccess`
   - `AmazonDynamoDBFullAccess`
   - `CloudWatchLogsFullAccess`
3. Click "Next"
4. Click "Create user"

**Step 3: Create Access Keys**
1. Click on newly created user
2. Go to "Security credentials" tab
3. Scroll to "Access keys"
4. Click "Create access key"
5. Select "Command Line Interface (CLI)"
6. Click "Next"
7. Click "Create access key"
8. **COPY BOTH KEYS** (shown only once!)

---

## 🔧 After Getting Credentials

**Set environment variables locally:**

```bash
export AWS_ACCESS_KEY_ID='AKIA...'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
export AWS_REGION='us-east-1'
export AWS_ACCOUNT_ID='597088017095'
```

**OR create ~/.aws/credentials file:**

```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = your-secret-key
region = us-east-1
EOF
```

**Then test:**

```bash
python test_aws_access.py
```

---

## ✅ Next Steps After Credentials

1. **Test AWS Access**: `python test_aws_access.py`
2. **Create Infrastructure**: `python setup_aws_infrastructure.py`
3. **Verify Resources**: Check S3 buckets and DynamoDB tables created
4. **Test Document Processing**: Upload document and process

---

## 📝 What I Can Do Once You Provide Credentials

✅ Create all S3 buckets (4)
✅ Create all DynamoDB tables (6)
✅ Create CloudWatch log groups (6)
✅ Test document upload to S3
✅ Test batch processing from S3 folder
✅ Test full workflow end-to-end
✅ Deploy to AWS if needed

---

## ⚠️ Security Note

- **Never commit credentials to Git**
- **Use environment variables or AWS credentials file**
- **Rotate keys regularly**
- **Use least privilege principle** (custom IAM policy if possible)

---

## 🆘 If You Need Help

**If you can't create access keys:**
- You might need AWS Administrator permissions
- Contact AWS account administrator

**If permissions are missing:**
- I can provide exact IAM policy JSON for minimal permissions
- Or use full access policies (for POC/testing)





