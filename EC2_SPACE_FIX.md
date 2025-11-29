# 💾 EC2 Space Issue During Install - Fix

## ⚠️ **Issue:**

Disk space still running out during pip install (pip cache + temp files filling up)

## ✅ **Solution: Install Without Cache**

### **Step 1: Clean Up Space**

**On EC2:**
```bash
# Check disk space
df -h

# Clean pip cache
pip cache purge
rm -rf ~/.cache/pip/*

# Clean system temp
sudo rm -rf /tmp/pip-*

# Check space again
df -h
```

### **Step 2: Install Without Cache**

**On EC2 (with venv activated):**
```bash
# Install requirements WITHOUT cache (saves space)
pip install --no-cache-dir -r requirements.txt
```

**This installs directly without using disk cache, saving ~2-3GB of space.**

### **Step 3: Alternative - Install CPU-Only XGBoost (Lighter)**

**If still running out of space, install CPU-only XGBoost:**

**On EC2 (with venv activated):**
```bash
# Install without XGBoost first
pip install --no-cache-dir streamlit openai boto3 pandas numpy python-dotenv PyPDF2 python-docx Pillow plotly matplotlib seaborn

# Install XGBoost CPU-only (much smaller)
pip install --no-cache-dir xgboost --no-binary xgboost

# OR skip XGBoost for now
# System will work without ML features
```

---

## 📋 **Recommended: Install Without Cache**

**On EC2:**
```bash
# 1. Clean up
pip cache purge
rm -rf ~/.cache/pip/*
df -h

# 2. Install without cache
pip install --no-cache-dir -r requirements.txt

# This will take longer but saves space!
```

---

## 🎯 **Alternative: Skip Heavy Dependencies**

**If space is still an issue:**

```bash
# Install essential packages only
pip install --no-cache-dir streamlit openai boto3 pandas numpy python-dotenv PyPDF2 python-docx Pillow plotly

# Skip XGBoost for now (can install later)
# ML features will be disabled but system will work
```

---

**Try installing with --no-cache-dir flag first!** 🚀





