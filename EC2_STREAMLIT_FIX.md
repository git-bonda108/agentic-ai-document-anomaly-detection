# 🔧 Streamlit Not Found - Fix

## ⚠️ **Issue:**

`streamlit: command not found` - Streamlit not installed in venv

## ✅ **Solution:**

### **Step 1: Verify venv is Activated**

**On EC2:**
```bash
# Check if venv is active (should show (venv) in prompt)
# Verify Python location
which python
# Should show: /home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/python

# If not showing venv path, activate it:
source venv/bin/activate
```

### **Step 2: Install Streamlit**

**On EC2 (with venv activated):**
```bash
# Install streamlit
pip install streamlit

# Verify installation
pip list | grep streamlit
# Should show: streamlit

# Verify command
which streamlit
# Should show: /home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/streamlit
```

### **Step 3: Install All Requirements**

**On EC2 (with venv activated):**
```bash
# Make sure you have requirements.txt
ls -la requirements.txt

# Install all requirements
pip install -r requirements.txt

# This will install:
# - streamlit
# - openai
# - boto3
# - xgboost
# - and all other dependencies
```

### **Step 4: Run Streamlit**

**On EC2 (with venv activated):**
```bash
# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📋 **Quick Fix Commands:**

```bash
# 1. Make sure venv is activated
source venv/bin/activate

# 2. Install requirements
pip install -r requirements.txt

# 3. Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

**Install requirements.txt to get all dependencies including Streamlit!** 🚀





