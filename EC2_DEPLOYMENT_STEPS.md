# 🚀 EC2 Deployment - Step-by-Step Guide

## ✅ **Pre-Deployment Checklist**

### **ML/RL Implementation Status:**
- ✅ TrainingAgent implemented with **XGBoost** support
- ✅ **XGBoost** model (XGBClassifier) - Primary ML model
- ✅ Reinforcement Learning from feedback implemented
- ✅ Human-in-the-Loop (HITL) system implemented
- ✅ Model versioning and management ready
- ✅ Evaluation metrics (F1, Precision, Recall, Confusion Matrix)

**Note:** XGBoost is fully implemented and will be used automatically on EC2.

---

## 📋 **Step 1: Launch EC2 Instance**

### **1.1. Go to AWS Console**
1. Open: https://console.aws.amazon.com/ec2/
2. Login with: **bond-admin** / Password: **Krsna&2022**
3. Make sure region is: **us-east-1** (N. Virginia)

### **1.2. Launch Instance**
1. Click **"Launch Instance"** button (orange button, top right)
2. Fill in details:

**Name and tags:**
- **Name:** `doc-anomaly-detection`

**Application and OS Images:**
- **AMI:** Amazon Linux 2023 AMI (or Ubuntu 22.04 LTS)
- **Architecture:** x86_64

**Instance type:**
- **Type:** `t3.medium` (2 vCPU, 4 GB RAM) - Minimum
- OR `t3.large` (2 vCPU, 8 GB RAM) - Recommended

**Key pair (login):**
- Click **"Create new key pair"**
- **Name:** `doc-anomaly-key`
- **Key pair type:** RSA
- **Private key file format:** .pem
- Click **"Create key pair"**
- **DOWNLOAD THE KEY** - Save to Downloads folder

**Network settings:**
- Click **"Edit"** network settings
- **VPC:** Default VPC (or create new)
- **Subnet:** Any public subnet
- **Auto-assign public IP:** Enable
- **Firewall (security groups):**
  - **Create security group:** Check this
  - **Security group name:** `doc-anomaly-sg`
  - **Description:** Allow Streamlit access
  - **Rules:**
    1. **Type:** SSH, **Port:** 22, **Source:** My IP (or 0.0.0.0/0 for testing)
    2. **Type:** Custom TCP, **Port:** 8501, **Source:** 0.0.0.0/0
    3. **Type:** HTTP, **Port:** 80, **Source:** 0.0.0.0/0 (optional)

**Configure storage:**
- **Volume size:** 20 GB (minimum)
- **Volume type:** gp3

### **1.3. Launch**
1. Click **"Launch Instance"** (orange button, bottom right)
2. Wait for instance to be **"Running"** (green status)
3. Click **"View Instances"**

---

## 📋 **Step 2: Get Instance Details**

### **2.1. Note Public IP**
1. Select your instance
2. Find **"Public IPv4 address"** (e.g., `54.123.45.67`)
3. **COPY THIS IP** - you'll need it

### **2.2. Connect to Instance**

**From your Mac Terminal:**

```bash
# Navigate to Downloads
cd ~/Downloads

# Set permissions for key file
chmod 400 doc-anomaly-key.pem

# Connect (for Amazon Linux)
# IMPORTANT: Replace <PUBLIC_IP> with your actual IP WITHOUT brackets!
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92

# OR for Ubuntu
ssh -i doc-anomaly-key.pem ubuntu@13.221.62.92
```

**IMPORTANT:** Use your actual IP address (e.g., `13.221.62.92`) WITHOUT angle brackets `< >`!

**Example:** `ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92`

---

## 📋 **Step 3: Install Dependencies on EC2**

### **3.1. Update System**

**For Amazon Linux 2023:**
```bash
sudo yum update -y
```

**For Ubuntu 22.04:**
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### **3.2. Install Python and Tools**

**For Amazon Linux 2023:**
```bash
# Update system first
sudo yum update -y

# Install Python 3 (default version - usually 3.11 or 3.12)
sudo yum install -y python3 python3-pip python3-devel git curl

# Tesseract OCR (OPTIONAL - not available in default repos)
# Skip for now - system will work without it (OCR disabled)
# sudo yum install -y tesseract tesseract-devel

# Install build tools
sudo yum install -y gcc g++ make

# Install development tools group
sudo yum groupinstall -y "Development Tools"
```

**For Ubuntu 22.04:**
```bash
# Install Python 3.13 (or use default 3.10/3.11)
sudo apt-get install -y python3 python3-pip python3-venv git curl

# Install Tesseract OCR
sudo apt-get install -y tesseract-ocr

# Install build tools
sudo apt-get install -y build-essential
```

### **3.3. Verify Installation**
```bash
# Check Python version (might be 3.11 or 3.12, not 3.13)
python3 --version

# Check pip
pip3 --version

# Check Tesseract
tesseract --version

# Check git
git --version
```

**Note:** Amazon Linux 2023 typically comes with Python 3.11 or 3.12, which is perfectly fine for this project. You don't need Python 3.13 specifically.

---

## 📋 **Step 4: Copy Code to EC2**

### **Option A: Using SCP (From Your Mac)**

```bash
# From your Mac Terminal
cd ~/Downloads

# Copy entire project
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@<PUBLIC_IP>:~/

# OR for Ubuntu
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ubuntu@<PUBLIC_IP>:~/
```

**Note:** This may take a few minutes (copying venv too)

### **Option B: Using Git (Recommended)**

**Step 4.1: Push to Git Repository**
```bash
# On your Mac
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - DOC Anomaly Detection System"

# Push to GitHub/GitLab/CodeCommit
# (You'll need to set up a repo first)
```

**Step 4.2: Clone on EC2**
```bash
# On EC2
git clone <your-repo-url>
cd doc-anomaly-detection
```

---

## 📋 **Step 5: Set Up Python Environment on EC2**

### **5.1. Navigate to Project**
```bash
# If copied via SCP
cd "DOC ANOMALY DETECTION SYSTEM"

# If cloned via Git
cd doc-anomaly-detection
```

### **5.2. Create Virtual Environment**
```bash
# Use python3 (whatever version is installed - 3.11, 3.12, or 3.13)
python3 -m venv venv
source venv/bin/activate
```

### **5.3. Install Dependencies**
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install XGBoost for ML
pip install xgboost lightgbm

# Verify
pip list | grep -E "streamlit|openai|boto3|xgboost"
```

---

## 📋 **Step 6: Configure Environment Variables**

### **6.1. Create .env File**
```bash
nano .env
```

**Paste this content (replace with your actual credentials):**
```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your_aws_account_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### **6.2. Export Variables (Alternative)**
```bash
export AWS_ACCESS_KEY_ID='your_aws_access_key_here'
export AWS_SECRET_ACCESS_KEY='your_aws_secret_key_here'
export AWS_REGION='us-east-1'
export OPENAI_API_KEY='your_openai_api_key_here'
```

---

## 📋 **Step 7: Test AWS Connection**

```bash
# Activate virtual environment
source venv/bin/activate

# Test AWS access
python -c "
from aws.s3_handler import S3Handler
from aws.dynamodb_handler import DynamoDBHandler

s3 = S3Handler()
print('✅ S3 Handler: OK')

db = DynamoDBHandler()
rules = db.get_business_rules()
print(f'✅ DynamoDB Handler: {len(rules)} rules loaded')
"
```

**Expected Output:**
```
✅ S3 Handler: OK
✅ DynamoDB Handler: 6 rules loaded
```

---

## 📋 **Step 8: Run Streamlit on EC2**

### **8.1. Run in Background (Quick Test)**
```bash
source venv/bin/activate
nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

### **8.2. Check if Running**
```bash
# Check process
ps aux | grep streamlit

# Check logs
tail -f streamlit.log

# Check if port is listening
netstat -tuln | grep 8501
```

### **8.3. Access Application**
- **Public URL:** `http://<PUBLIC_IP>:8501`
- Open in browser from anywhere

---

## 📋 **Step 9: Set Up as System Service (Production)**

### **9.1. Create Systemd Service**
```bash
sudo nano /etc/systemd/system/streamlit.service
```

**Paste this (adjust paths):**
```ini
[Unit]
Description=DOC Anomaly Detection Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM
Environment="PATH=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin"
EnvironmentFile=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/.env
ExecStart=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Adjust paths:**
- Replace `/home/ec2-user` with your actual home directory
- Replace `ec2-user` with `ubuntu` if using Ubuntu

### **9.2. Enable and Start Service**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable streamlit

# Start service
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit

# View logs
sudo journalctl -u streamlit -f
```

---

## 📋 **Step 10: Set Up Public URL (Optional but Recommended)**

### **10.1. Get Public IP**
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### **10.2. Set Up Domain (Optional)**
1. Buy domain (e.g., from Route 53 or external)
2. Point A record to EC2 public IP
3. Access via: `http://your-domain.com:8501`

### **10.3. Set Up Nginx Reverse Proxy (Recommended)**
```bash
# Install Nginx
sudo yum install -y nginx  # Amazon Linux
# OR
sudo apt-get install -y nginx  # Ubuntu

# Create config
sudo nano /etc/nginx/conf.d/streamlit.conf
```

**Paste:**
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or use EC2 public IP

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

**Now access via:** `http://<PUBLIC_IP>` (port 80) instead of port 8501

---

## ✅ **Step 11: Verify Deployment**

### **11.1. Check Service Status**
```bash
sudo systemctl status streamlit
```

### **11.2. Test Access**
1. Open browser
2. Go to: `http://<EC2_PUBLIC_IP>:8501`
3. You should see Streamlit app

### **11.3. Test Document Processing**
1. Go to "Upload & Process"
2. Upload sample document
3. Click "Process Document"
4. Verify results

### **11.4. Test Batch Processing**
1. Upload documents to S3: `doc-anomaly-raw-docs-597088017095/documents/`
2. Go to "Batch Processing (S3)"
3. Process folder
4. Verify results

---

## 🔐 **Security Best Practices**

### **1. Use IAM Roles (Recommended for Production)**
Instead of access keys on EC2:
1. Create IAM role with required permissions
2. Attach role to EC2 instance
3. Remove access keys from .env

### **2. Restrict Security Group**
- Only allow your IP for SSH (port 22)
- Only allow trusted IPs for Streamlit (port 8501)

### **3. Use Secrets Manager (Advanced)**
- Store credentials in AWS Secrets Manager
- Retrieve in code at runtime

---

## 📋 **Troubleshooting**

### **Issue: Can't access Streamlit**
- Check Security Group: Port 8501 open to 0.0.0.0/0
- Check service status: `sudo systemctl status streamlit`
- Check logs: `sudo journalctl -u streamlit -n 50`

### **Issue: AWS connection fails**
- Check .env file exists
- Verify credentials
- Check IAM permissions

### **Issue: Tesseract not found**
- **Note:** Tesseract is optional - system works without it
- OCR features will be disabled, but PDF/DOCX processing works
- If needed later: See `EC2_TESSERACT_INSTALL.md` for source build instructions

---

## 🎯 **Final Result**

**After completing all steps:**

✅ Streamlit app running on EC2
✅ Public URL: `http://<EC2_PUBLIC_IP>:8501`
✅ Accessible from anywhere
✅ Connects to AWS services
✅ Full functionality working

**OR with Nginx:**
✅ Public URL: `http://<EC2_PUBLIC_IP>` (port 80)
✅ Cleaner URL (no port number)

---

## 📝 **Quick Reference Commands**

```bash
# Connect to EC2
ssh -i ~/Downloads/doc-anomaly-key.pem ec2-user@<PUBLIC_IP>

# Check service
sudo systemctl status streamlit

# Restart service
sudo systemctl restart streamlit

# View logs
sudo journalctl -u streamlit -f

# Check ports
netstat -tuln | grep 8501

# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

---

**Ready to deploy? Follow steps 1-11 above!**

