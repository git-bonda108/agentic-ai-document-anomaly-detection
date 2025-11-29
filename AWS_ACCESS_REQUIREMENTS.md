# AWS Access Requirements - Summary

## 🔐 What I Have vs What I Need

### ❌ What I Have:
- IAM user name: `bond-admin`
- Group ARN: `arn:aws:iam::597088017095:group/bond-admin`
- Password: `Krsna&2022` (for console login)

### ✅ What I Need:
- **AWS Access Key ID** (starts with `AKIA...`)
- **AWS Secret Access Key** (long string)
- **IAM permissions** (see below)

---

## 📋 Required IAM Permissions

The IAM user (`bond-admin`) needs these permissions:

### S3 Permissions:
- `s3:CreateBucket`
- `s3:PutObject`
- `s3:GetObject`
- `s3:ListBucket`
- `s3:DeleteObject`

### DynamoDB Permissions:
- `dynamodb:CreateTable`
- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:Query`
- `dynamodb:Scan`
- `dynamodb:ListTables`

### CloudWatch Permissions:
- `logs:CreateLogGroup`
- `logs:PutLogEvents`
- `logs:DescribeLogGroups`

### STS Permissions:
- `sts:GetCallerIdentity` (for testing credentials)

---

## 🚀 Quick Setup Steps

### Step 1: Get Access Keys
1. Login to AWS Console: https://console.aws.amazon.com/
2. Account: **597088017095**
3. Username: **bond-admin**
4. Password: **Krsna&2022**
5. Navigate to: IAM → Users → bond-admin → Security credentials
6. Create or view Access Keys
7. Copy **Access Key ID** and **Secret Access Key**

### Step 2: Verify Permissions
- Check if user has required policies attached
- If missing, attach:
  - `AmazonS3FullAccess`
  - `AmazonDynamoDBFullAccess`
  - `CloudWatchLogsFullAccess`

### Step 3: Provide Credentials
- Send me the Access Key ID and Secret Access Key
- I'll configure and test immediately

---

## ✅ After Credentials Provided

I will:
1. ✅ Test AWS access
2. ✅ Create all infrastructure (S3, DynamoDB, CloudWatch)
3. ✅ Test batch ingestion from S3 folder
4. ✅ Test full workflow
5. ✅ Deploy if needed

---

## 📝 Status

**Waiting for:**
- AWS Access Key ID
- AWS Secret Access Key

**Once provided, I can:**
- Complete AWS setup
- Test batch processing
- Test full application
- Deploy to production





