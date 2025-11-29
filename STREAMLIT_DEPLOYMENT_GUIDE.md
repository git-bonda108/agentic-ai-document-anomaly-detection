# 🚀 Streamlit Deployment Guide - Complete Steps

## 📋 **Table of Contents**

1. [Local Deployment](#local-deployment)
2. [EC2 Production Deployment](#ec2-production-deployment)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Configuration & Environment](#configuration--environment)
6. [Security Setup](#security-setup)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ **Local Deployment**

### **Step 1: Prerequisites**

```bash
# Check Python version (3.9+ required)
python3 --version

# Check if virtual environment exists
ls -la venv/
```

### **Step 2: Install Dependencies**

```bash
cd "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM"

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install/update dependencies
pip install -r requirements.txt
```

### **Step 3: Configure Environment**

Create `.env` file in project root:

```bash
# .env file
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_api_key_here
```

### **Step 4: Launch Streamlit**

```bash
# Kill any existing Streamlit processes
pkill -f streamlit

# Launch Streamlit app
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

### **Step 5: Access Application**

- **Local:** http://localhost:8501
- **Network:** http://YOUR_IP:8501 (if firewall allows)

---

## ☁️ **EC2 Production Deployment**

### **Step 1: Launch EC2 Instance**

1. **Go to AWS Console:** https://console.aws.amazon.com/ec2/
2. **Click "Launch Instance"**
3. **Configure:**
   - **Name:** `doc-anomaly-streamlit`
   - **AMI:** Amazon Linux 2023 (or Ubuntu 22.04 LTS)
   - **Instance Type:** `t3.medium` (2 vCPU, 4GB RAM) minimum
   - **Key Pair:** Create new or use existing
   - **Security Group:** Allow inbound on port 8501
4. **Launch Instance**

### **Step 2: Connect to EC2**

```bash
# From your local machine
ssh -i your-key.pem ec2-user@YOUR_EC2_IP
```

### **Step 3: Install System Dependencies**

```bash
# Amazon Linux 2023
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Ubuntu 22.04
# sudo apt update
# sudo apt install -y python3 python3-pip python3-venv git
```

### **Step 4: Clone Repository**

```bash
# Clone from GitHub
git clone https://github.com/git-bonda108/agentic-ai-document-anomaly-detection.git
cd agentic-ai-document-anomaly-detection
```

### **Step 5: Set Up Python Environment**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 6: Configure Environment Variables**

```bash
# Create .env file
nano .env
```

**Paste:**
```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_api_key_here
```

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### **Step 7: Configure Security Group**

1. **AWS Console** → **EC2** → **Security Groups**
2. **Select your instance's security group**
3. **Inbound Rules** → **Edit Inbound Rules**
4. **Add Rule:**
   - **Type:** Custom TCP
   - **Port:** 8501
   - **Source:** 0.0.0.0/0 (or specific IP for security)
5. **Save Rules**

### **Step 8: Launch Streamlit**

```bash
# Activate virtual environment
source venv/bin/activate

# Launch Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

### **Step 9: Access Application**

- **Public URL:** http://YOUR_EC2_PUBLIC_IP:8501
- **Example:** http://13.221.62.92:8501

### **Step 10: Run as Background Service (Optional)**

Create systemd service for auto-start:

```bash
# Create service file
sudo nano /etc/systemd/system/streamlit-app.service
```

**Paste:**
```ini
[Unit]
Description=Streamlit Doc Anomaly Detection App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/agentic-ai-document-anomaly-detection
Environment="PATH=/home/ec2-user/agentic-ai-document-anomaly-detection/venv/bin"
ExecStart=/home/ec2-user/agentic-ai-document-anomaly-detection/venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app
sudo systemctl status streamlit-app
```

---

## 🌐 **Streamlit Cloud Deployment**

### **Step 1: Prepare Repository**

1. **Ensure code is on GitHub:**
   ```bash
   git push origin main
   ```

2. **Verify `.streamlit/config.toml` exists** (optional):
   ```toml
   [server]
   port = 8501
   address = "0.0.0.0"
   ```

### **Step 2: Deploy to Streamlit Cloud**

1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Configure:**
   - **Repository:** `git-bonda108/agentic-ai-document-anomaly-detection`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`
5. **Add Secrets:**
   - Go to **"Advanced settings"** → **"Secrets"**
   - Add:
     ```
     AWS_ACCESS_KEY_ID=your_key
     AWS_SECRET_ACCESS_KEY=your_secret
     AWS_REGION=us-east-1
     OPENAI_API_KEY=your_key
     ```
6. **Click "Deploy"**

### **Step 3: Access Application**

- **URL:** https://your-app-name.streamlit.app
- **Auto-updates** on git push

---

## 🐳 **Docker Deployment**

### **Step 1: Create Dockerfile**

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Step 2: Create .dockerignore**

```
venv/
__pycache__/
*.pyc
.env
*.log
*.db
uploads/
documents/
.git/
```

### **Step 3: Build Docker Image**

```bash
docker build -t doc-anomaly-streamlit:latest .
```

### **Step 4: Run Container**

```bash
docker run -d \
  -p 8501:8501 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=us-east-1 \
  -e OPENAI_API_KEY=your_key \
  --name doc-anomaly-app \
  doc-anomaly-streamlit:latest
```

### **Step 5: Access Application**

- **URL:** http://localhost:8501

### **Step 6: Deploy to AWS ECS/Fargate (Optional)**

1. **Push to ECR:**
   ```bash
   aws ecr create-repository --repository-name doc-anomaly-streamlit
   docker tag doc-anomaly-streamlit:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/doc-anomaly-streamlit:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/doc-anomaly-streamlit:latest
   ```

2. **Create ECS Task Definition** with environment variables
3. **Deploy to Fargate** with public IP

---

## ⚙️ **Configuration & Environment**

### **Environment Variables**

**Required:**
```bash
AWS_ACCESS_KEY_ID          # AWS IAM access key
AWS_SECRET_ACCESS_KEY      # AWS IAM secret key
AWS_REGION                 # AWS region (e.g., us-east-1)
OPENAI_API_KEY            # OpenAI API key for GPT-4o
```

**Optional:**
```bash
STREAMLIT_SERVER_PORT      # Custom port (default: 8501)
STREAMLIT_SERVER_ADDRESS   # Server address (default: 0.0.0.0)
```

### **Streamlit Configuration**

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 🔒 **Security Setup**

### **1. Environment Variables**

✅ **DO:**
- Use `.env` file (not committed to git)
- Use AWS Secrets Manager for production
- Rotate credentials regularly

❌ **DON'T:**
- Commit `.env` to git
- Hardcode credentials in code
- Share credentials in documentation

### **2. Security Group Rules**

**Production:**
- Restrict port 8501 to specific IPs
- Use VPN or bastion host
- Enable HTTPS (use reverse proxy)

**Development:**
- Can allow 0.0.0.0/0 temporarily
- Monitor access logs

### **3. IAM Permissions**

Use **least privilege** IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::doc-anomaly-*/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/DocumentMetadata",
        "arn:aws:dynamodb:us-east-1:*:table/AnomalyResults"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:*:*"
    }
  ]
}
```

---

## 🔧 **Troubleshooting**

### **Issue: Port 8501 Already in Use**

```bash
# Find process using port
sudo lsof -i :8501

# Kill process
sudo pkill -f streamlit

# Or kill specific PID
kill -9 <PID>
```

### **Issue: Cannot Access from Network**

1. **Check Security Group:**
   - Ensure port 8501 is open
   - Source: 0.0.0.0/0 (or your IP)

2. **Check Firewall:**
   ```bash
   # EC2 - Check if port is listening
   sudo netstat -tlnp | grep 8501
   ```

3. **Check Streamlit Address:**
   - Must use `--server.address 0.0.0.0` (not `localhost`)

### **Issue: Import Errors**

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Issue: AWS Credentials Not Working**

```bash
# Test AWS credentials
python test_aws_access.py

# Verify environment variables
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

### **Issue: Streamlit App Crashes**

1. **Check logs:**
   ```bash
   # View Streamlit logs
   streamlit run streamlit_app/app.py --logger.level=debug
   ```

2. **Check CloudWatch logs** (if deployed on AWS)

3. **Verify dependencies:**
   ```bash
   pip list | grep streamlit
   pip list | grep boto3
   pip list | grep openai
   ```

### **Issue: Slow Performance**

1. **Increase EC2 instance size** (t3.medium → t3.large)
2. **Check CloudWatch metrics** for bottlenecks
3. **Optimize OpenAI API calls** (batch requests)
4. **Use caching** for repeated operations

---

## 📊 **Monitoring & Maintenance**

### **Health Checks**

```bash
# Check if app is running
curl http://localhost:8501/_stcore/health

# Check process
ps aux | grep streamlit
```

### **Logs**

**Local:**
- Check terminal output
- Check `doc_processing.log` (if configured)

**EC2:**
- Check systemd logs: `sudo journalctl -u streamlit-app -f`
- Check CloudWatch logs

### **Updates**

```bash
# Pull latest code
git pull origin main

# Restart service (if using systemd)
sudo systemctl restart streamlit-app

# Or restart manually
pkill -f streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## ✅ **Deployment Checklist**

- [ ] Dependencies installed (`requirements.txt`)
- [ ] Environment variables configured (`.env` or system)
- [ ] AWS credentials valid and tested
- [ ] OpenAI API key configured
- [ ] Security group allows port 8501
- [ ] Streamlit app launches successfully
- [ ] Application accessible from browser
- [ ] All pages load correctly
- [ ] Document upload works
- [ ] AWS services (S3, DynamoDB) accessible
- [ ] CloudWatch logging working
- [ ] Background service configured (if needed)

---

## 🎯 **Quick Reference**

### **Local Development**
```bash
source venv/bin/activate
streamlit run streamlit_app/app.py
```

### **Production (EC2)**
```bash
source venv/bin/activate
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

### **Docker**
```bash
docker build -t doc-anomaly-streamlit .
docker run -p 8501:8501 -e AWS_ACCESS_KEY_ID=... doc-anomaly-streamlit
```

### **Streamlit Cloud**
- Push to GitHub → Deploy on share.streamlit.io

---

**🚀 Your Streamlit app is now ready for deployment!**

**For questions or issues, refer to the troubleshooting section above.**

