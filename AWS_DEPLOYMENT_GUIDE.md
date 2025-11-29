# AWS Deployment Guide - Step by Step

## 🎯 Deployment Options

### **Option 1: EC2 (Simplest for POC)** ⭐ RECOMMENDED
- Launch EC2 instance
- Run Streamlit app
- Access via public IP

### **Option 2: ECS Fargate (Production)**
- Container-based deployment
- Auto-scaling
- Load balancing

### **Option 3: Elastic Beanstalk (Easiest)**
- Fully managed
- Auto-scaling
- Health monitoring

---

## 📋 Option 1: Deploy to EC2 (Step by Step)

### **Step 1: Launch EC2 Instance**

**In AWS Console:**
1. Go to EC2 Console
2. Click "Launch Instance"
3. Configure:
   - **Name:** doc-anomaly-detection
   - **AMI:** Amazon Linux 2023 or Ubuntu 22.04
   - **Instance Type:** t3.medium (2 vCPU, 4 GB RAM)
   - **Key Pair:** Create or select existing
   - **Security Group:** 
     - Add rule: HTTP (port 80)
     - Add rule: Custom TCP (port 8501)
     - Source: 0.0.0.0/0 (for public access)
   - **Storage:** 20 GB
4. Click "Launch Instance"

### **Step 2: Connect to EC2**

**From your Mac:**
```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@<EC2_PUBLIC_IP>
# Or for Ubuntu:
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### **Step 3: Install Dependencies**

```bash
# Update system
sudo yum update -y  # For Amazon Linux
# OR
sudo apt-get update && sudo apt-get upgrade -y  # For Ubuntu

# Install Python 3.13
sudo yum install -y python3.13 python3-pip git  # Amazon Linux
# OR for Ubuntu:
sudo apt-get install -y python3.13 python3-pip git

# Install Tesseract OCR
sudo yum install -y tesseract  # Amazon Linux
# OR
sudo apt-get install -y tesseract-ocr  # Ubuntu
```

### **Step 4: Copy Code to EC2**

**Option A: From your Mac**
```bash
# Copy entire project
scp -r -i your-key.pem "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@<EC2_IP>:~/
```

**Option B: Clone from Git (if you push to repo)**
```bash
# On EC2
git clone <your-repo-url>
cd doc-anomaly-detection
```

### **Step 5: Set Up on EC2**

```bash
# On EC2 instance
cd "DOC ANOMALY DETECTION SYSTEM"

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_ACCESS_KEY_ID='your_aws_access_key_here'
export AWS_SECRET_ACCESS_KEY='your_aws_secret_key_here'
export AWS_REGION='us-east-1'
export OPENAI_API_KEY='your_openai_api_key_here'

# Or create .env file
cat > .env << EOF
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### **Step 6: Run Streamlit on EC2**

```bash
# Run in background with screen or nohup
screen -S streamlit
# OR
nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 &

# Or use systemd service (better for production)
sudo nano /etc/systemd/system/streamlit.service
```

**Create systemd service:**
```ini
[Unit]
Description=DOC Anomaly Detection Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM
Environment="PATH=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin"
Environment="AWS_ACCESS_KEY_ID=your_aws_access_key_here"
Environment="AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here"
Environment="AWS_REGION=us-east-1"
Environment="OPENAI_API_KEY=your_openai_api_key_here"
ExecStart=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

### **Step 7: Access Application**

```bash
# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Access app at:
http://<EC2_PUBLIC_IP>:8501
```

### **Step 8: Set Up Domain (Optional)**

- Use Route 53 for domain
- Point domain to EC2 public IP
- Use Nginx as reverse proxy for port 80

---

## 📋 Option 2: Deploy to ECS Fargate

### **Step 1: Build Docker Image**

```bash
# On your Mac
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"
docker build -t doc-anomaly-detection .
```

### **Step 2: Push to ECR**

```bash
# Create ECR repository
aws ecr create-repository --repository-name doc-anomaly-detection --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 597088017095.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag doc-anomaly-detection:latest 597088017095.dkr.ecr.us-east-1.amazonaws.com/doc-anomaly-detection:latest
docker push 597088017095.dkr.ecr.us-east-1.amazonaws.com/doc-anomaly-detection:latest
```

### **Step 3: Create ECS Cluster and Service**

```bash
# Create cluster
aws ecs create-cluster --cluster-name doc-anomaly-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create service
aws ecs create-service \
    --cluster doc-anomaly-cluster \
    --service-name doc-anomaly-service \
    --task-definition doc-anomaly-detection \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## 📋 Option 3: Deploy to Elastic Beanstalk

### **Step 1: Install EB CLI**

```bash
pip install awsebcli
```

### **Step 2: Initialize and Deploy**

```bash
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"
eb init -p "Python 3.13" doc-anomaly-detection --region us-east-1
eb create doc-anomaly-env
eb deploy
eb open
```

---

## ✅ **Recommended for Now: Keep Local + AWS Services**

**Current Setup:**
- ✅ Code runs locally on your Mac
- ✅ Connects to AWS services (S3, DynamoDB, CloudWatch)
- ✅ Works perfectly for POC/testing

**When to Deploy:**
- When you need 24/7 availability
- When you need to share with team
- When ready for production

---

## 🚀 **Quick Test: Restart Streamlit with Credentials**

```bash
# Kill existing Streamlit
pkill -f streamlit

# Restart with credentials
export AWS_ACCESS_KEY_ID='your_aws_access_key_here'
export AWS_SECRET_ACCESS_KEY='your_aws_secret_key_here'
export AWS_REGION='us-east-1'
export OPENAI_API_KEY='your_openai_api_key_here'

cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

**Then access from any device on your network:**
- `http://localhost:8501` (local)
- `http://<your-mac-ip>:8501` (from other devices)

---

## ⚠️ **What You Need to Do for EC2 Deployment**

**If you want to deploy to AWS EC2:**

1. **Launch EC2 instance** (I can guide you through AWS Console)
2. **Set up security group** (port 8501 open)
3. **Copy code** to EC2 (via SCP or Git)
4. **Install dependencies** on EC2
5. **Run Streamlit** on EC2
6. **Access via EC2 public IP**

**OR keep it local** (recommended for POC) - it connects to AWS services perfectly!

---

**Which would you prefer?**
1. **Test locally first** (easier, works now)
2. **Deploy to EC2** (I'll guide you step-by-step)
3. **Deploy to ECS** (more complex, production-ready)





