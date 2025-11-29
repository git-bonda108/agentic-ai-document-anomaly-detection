# 🚀 EC2 Next Steps - After Code Copy

## ✅ **Current Status:**

- ✅ Python 3.9.24 installed (good enough!)
- ✅ Git installed
- ⚠️  pip3 not found - need to install
- ✅ Code copied to EC2

---

## 📋 **Step 1: Install pip3 on EC2**

**On your EC2 instance, run:**

```bash
# Install pip3
sudo yum install -y python3-pip

# Verify installation
pip3 --version
python3 --version
```

---

## 📋 **Step 2: Navigate to Project Directory**

**On EC2:**

```bash
# List files to find project folder
ls -la

# Navigate to project (should be "DOC ANOMALY DETECTION SYSTEM")
cd "DOC ANOMALY DETECTION SYSTEM"

# Verify you're in the right place
ls -la
# Should see: agents/, streamlit_app/, requirements.txt, etc.
```

---

## 📋 **Step 3: Set Up Virtual Environment**

**On EC2 (in project directory):**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
# Verify
which python
# Should show: /home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/python
```

---

## 📋 **Step 4: Install Python Dependencies**

**On EC2 (with venv activated):**

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# This will take a few minutes...
# Watch for any errors (especially XGBoost - might take longer)
```

**If XGBoost installation is slow, that's normal - it compiles from source.**

---

## 📋 **Step 5: Configure Environment Variables**

**On EC2 (in project directory):**

```bash
# Create .env file
nano .env
```

**Paste this content:**

```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=597088017095
OPENAI_API_KEY=your_openai_api_key_here
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## 📋 **Step 6: Test AWS Connection**

**On EC2 (with venv activated):**

```bash
# Test AWS connection
python3 -c "
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
sts = boto3.client('sts', region_name='us-east-1')
identity = sts.get_caller_identity()
print('✅ AWS Connected!')
print(f'   Account: {identity[\"Account\"]}')
print(f'   ARN: {identity[\"Arn\"]}')
"
```

**Expected:** ✅ AWS Connected! with account details

---

## 📋 **Step 7: Test Streamlit (Quick Test)**

**On EC2 (with venv activated):**

```bash
# Run Streamlit in background
nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &

# Check if running
ps aux | grep streamlit

# Check logs
tail -f streamlit.log

# Check if port is listening
netstat -tuln | grep 8501
```

---

## 📋 **Step 8: Access Your Application**

**From your browser (on Mac or anywhere):**

Open: `http://13.221.62.92:8501`

**You should see the Streamlit app!** 🎉

---

## 📋 **Step 9: Set Up as System Service (Production)**

**On EC2 (for permanent service):**

```bash
# Create systemd service
sudo nano /etc/systemd/system/streamlit.service
```

**Paste this (adjust paths if needed):**

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

**Save:** `Ctrl+X`, `Y`, `Enter`

**Enable and start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

---

## ✅ **Quick Command Summary:**

**On EC2, run these in order:**

```bash
# 1. Install pip
sudo yum install -y python3-pip

# 2. Go to project
cd "DOC ANOMALY DETECTION SYSTEM"

# 3. Create venv
python3 -m venv venv
source venv/bin/activate

# 4. Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create .env (use nano as shown above)

# 6. Test Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Your Public URL:**

Once Streamlit is running:

**`http://13.221.62.92:8501`**

---

**Start with Step 1: Install pip3!** 🚀

