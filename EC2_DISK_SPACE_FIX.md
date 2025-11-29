# 💾 EC2 Disk Space Issue - Fix

## ⚠️ **Issue:**

`No space left on device` - EC2 instance has run out of disk space

## ✅ **Solutions:**

### **Step 1: Check Disk Space**

**On EC2:**
```bash
# Check disk usage
df -h

# Check home directory size
du -sh ~

# Check project directory size
du -sh "DOC ANOMALY DETECTION SYSTEM"
```

### **Step 2: Clean Up Space**

**On EC2:**
```bash
# Clean up pip cache
rm -rf ~/.cache/pip/*

# Clean up system package cache
sudo yum clean all

# Remove old logs
sudo journalctl --vacuum-time=3d

# Check for large files
find ~ -type f -size +100M 2>/dev/null
```

### **Step 3: Remove Heavy Dependencies (Temporary)**

**Option A: Install Minimum Requirements First**

Create a minimal requirements file:

**On EC2:**
```bash
# Create minimal requirements
cat > requirements_minimal.txt << 'EOF'
streamlit>=1.28.0
openai>=1.3.0
boto3>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0
python-docx>=0.8.11
Pillow>=10.0.0
plotly>=5.17.0
EOF

# Install minimal requirements
pip install -r requirements_minimal.txt
```

**Option B: Install Without XGBoost (Skip ML for Now)**

```bash
# Install everything except XGBoost
pip install streamlit openai boto3 pandas numpy python-dotenv PyPDF2 python-docx Pillow plotly
```

### **Step 4: Increase Disk Size (Recommended)**

**In AWS Console:**
1. Stop EC2 instance
2. Go to Volumes → Select your instance's volume
3. Modify → Increase size to 30-40 GB
4. Start instance
5. Expand filesystem:
   ```bash
   # Check current size
   df -h
   
   # Resize (for Amazon Linux 2023)
   sudo growpart /dev/xvda 1
   sudo resize2fs /dev/xvda1
   
   # Verify
   df -h
   ```

---

## 📋 **Quick Fix (Get Streamlit Running Now):**

**On EC2:**

```bash
# 1. Clean up space
rm -rf ~/.cache/pip/*
sudo yum clean all

# 2. Install minimal requirements
pip install streamlit openai boto3 pandas numpy python-dotenv PyPDF2 python-docx Pillow plotly

# 3. Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

**Note:** This skips XGBoost temporarily. You can install it later after increasing disk space.

---

## 🎯 **Recommended: Increase Disk Size**

1. Stop EC2 instance in AWS Console
2. Modify volume size to 40 GB
3. Start instance
4. Resize filesystem (commands above)
5. Then install full requirements.txt

---

**Try the quick fix first to get Streamlit running, then increase disk size!** 🚀





