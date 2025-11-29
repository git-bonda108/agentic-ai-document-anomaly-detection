# ✅ Setting Up Virtual Environment on EC2

## ⚠️ **Issue:**

The `venv` folder exists from the Mac copy, but it won't work on Linux EC2.
We need to remove it and create a fresh one.

## ✅ **Solution:**

### **Step 1: Remove Old venv**

**On EC2 (in project directory):**
```bash
# Remove the old venv (it's from Mac, won't work on Linux)
rm -rf venv

# Verify it's gone
ls -la | grep venv
# Should show nothing
```

### **Step 2: Create New Virtual Environment**

**On EC2:**
```bash
# Create fresh virtual environment (Linux-compatible)
python3 -m venv venv

# This should work now!
```

### **Step 3: Activate venv**

**On EC2:**
```bash
# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
# Verify
which python
# Should show: /home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/python
```

### **Step 4: Install Dependencies**

**On EC2 (with venv activated):**
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements (will take several minutes)
pip install -r requirements.txt

# XGBoost may take a while to compile - be patient!
```

---

## 📋 **Complete Commands (Run These):**

```bash
# 1. Remove old venv
rm -rf venv

# 2. Create new venv
python3 -m venv venv

# 3. Activate
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt
```

---

**Remove the old venv first, then create a new one!** 🚀





