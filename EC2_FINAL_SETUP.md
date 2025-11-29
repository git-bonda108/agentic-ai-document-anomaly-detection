# ✅ EC2 Final Setup - Continue Here

## ✅ **Status:**

- ✅ Connected to EC2 (new IP: 44.220.247.17)
- ✅ Disk resized to 40GB (37GB available)
- ✅ Ready to install requirements

## 📋 **Next Steps:**

### **Step 1: Navigate to Project Directory**

**On EC2:**
```bash
# Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# Verify you're in the right place
ls -la
# Should see: agents/, streamlit_app/, requirements.txt, etc.
```

### **Step 2: Activate Virtual Environment**

**On EC2:**
```bash
# Activate venv
source venv/bin/activate

# Verify (prompt should show (venv))
which python
# Should show: .../venv/bin/python
```

### **Step 3: Clean Up and Install Requirements**

**On EC2 (with venv activated):**
```bash
# Clean up any partial installs
pip cache purge
rm -rf ~/.cache/pip/*

# Upgrade pip
pip install --upgrade pip

# Install requirements (this will take several minutes)
pip install -r requirements.txt

# XGBoost will take a while to compile - be patient!
```

### **Step 4: Verify Key Packages**

**On EC2 (with venv activated):**
```bash
# Check key packages
pip list | grep -E "streamlit|openai|boto3|xgboost"

# Should show:
# streamlit
# openai
# boto3
# xgboost
```

### **Step 5: Create .env File**

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

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### **Step 6: Test AWS Connection**

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

### **Step 7: Run Streamlit**

**On EC2 (with venv activated):**
```bash
# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

**You should see:**
```
You can now view your Streamlit app in your browser.
URL: http://0.0.0.0:8501
```

### **Step 8: Access Your Application**

**From your browser (anywhere):**
Open: `http://44.220.247.17:8501`

**🎉 You should see the Streamlit app!**

---

## 📋 **Quick Command Summary:**

**On EC2, run these in order:**

```bash
# 1. Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# 2. Activate venv
source venv/bin/activate

# 3. Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create .env (use nano as shown above)

# 5. Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Your Public URL:**

**`http://44.220.247.17:8501`**

---

**Start with Step 1: Navigate to project directory!** 🚀





