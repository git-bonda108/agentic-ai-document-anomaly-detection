# 📋 Copy Streamlit App to EC2

## ✅ **Issue:**

Streamlit app directory (`streamlit_app/`) wasn't copied to EC2. We need to copy it!

## ✅ **Solution: Copy streamlit_app Directory to EC2**

### **Step 1: Copy streamlit_app Directory**

**On your Mac:**

```bash
# Navigate to Downloads
cd ~/Downloads

# Copy ONLY streamlit_app directory to EC2
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM/streamlit_app" ec2-user@13.219.178.111:~/DOC\ ANOMALY\ DETECTION\ SYSTEM/
```

**This will copy the entire `streamlit_app/` directory with all pages.**

---

### **Step 2: Verify on EC2**

**SSH to EC2:**

```bash
# On your Mac
ssh -i doc-anomaly-key.pem ec2-user@13.219.178.111

# On EC2, verify it was copied
cd "DOC ANOMALY DETECTION SYSTEM"
ls -la streamlit_app/
ls -la streamlit_app/app.py
ls -la streamlit_app/pages/
```

---

### **Step 3: Run Streamlit**

**On EC2 (with venv activated):**

```bash
cd "DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate

# Now run Streamlit with correct path
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📋 **Alternative: Copy Entire Project Again (If Needed)**

**If streamlit_app still doesn't exist, copy entire project:**

**On your Mac:**

```bash
cd ~/Downloads

# Copy entire project (will overwrite)
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@13.219.178.111:~/
```

**Then on EC2:**

```bash
cd "DOC ANOMALY DETECTION SYSTEM"
ls -la streamlit_app/
# Should now see streamlit_app directory
```

---

## 🎯 **Quick Fix:**

**On your Mac (Downloads folder):**

```bash
# Copy streamlit_app directory
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM/streamlit_app" ec2-user@13.219.178.111:~/DOC\ ANOMALY\ DETECTION\ SYSTEM/
```

**Then on EC2:**

```bash
cd "DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

**Copy streamlit_app directory to EC2 now!** 🚀





