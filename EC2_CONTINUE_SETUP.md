# ✅ Code Copied - Continue Setup on EC2

## ✅ **Status:**
- ✅ Files copied successfully (~9.6 MB)
- ✅ Project is now on EC2

## 📋 **Next Steps on EC2:**

### **Step 1: Connect to EC2 (if not already connected)**

**On your Mac terminal:**
```bash
cd ~/Downloads
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

### **Step 2: Navigate to Project Directory**

**On EC2 (once connected):**
```bash
# List files to see the project
ls -la

# Navigate to project directory
cd "DOC ANOMALY DETECTION SYSTEM"

# Verify you're in the right place
ls -la
# Should see: agents/, streamlit_app/, requirements.txt, etc.
```

### **Step 3: Create Virtual Environment**

**On EC2 (in project directory):**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)
# Verify
which python
# Should show: /home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/python
```

### **Step 4: Upgrade pip and Install Dependencies**

**On EC2 (with venv activated):**
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements (this will take several minutes)
pip install -r requirements.txt

# Note: XGBoost may take a while to compile
# Be patient!
```

### **Step 5: Verify Key Packages**

**On EC2 (with venv activated):**
```bash
# Check if key packages installed
pip list | grep -E "streamlit|openai|boto3|xgboost"

# Should see:
# streamlit
# openai
# boto3
# xgboost
```

### **Step 6: Create .env File**

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

### **Step 7: Test AWS Connection**

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

### **Step 8: Run Streamlit**

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

### **Step 9: Access Your Application**

**From your browser (anywhere):**
Open: `http://13.221.62.92:8501`

**🎉 You should see the Streamlit app!**

---

## ✅ **Quick Command Summary:**

**On EC2, run these in order:**

```bash
# 1. Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# 2. Create venv
python3 -m venv venv
source venv/bin/activate

# 3. Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create .env (use nano as shown above)

# 5. Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Your Public URL:**

Once Streamlit is running:
**`http://13.221.62.92:8501`**

---

**Go to EC2 and continue with Step 2 above!** 🚀





