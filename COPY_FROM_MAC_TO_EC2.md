# 📋 Copy Streamlit App - Correct Method

## ⚠️ **Issue:**

You're trying to run `scp` from EC2, but it needs to run from your Mac!

## ✅ **Solution:**

### **Step 1: Exit EC2**

**On EC2 (where you are now):**

```bash
# Exit EC2 session
exit
```

**You should now be back on your Mac terminal.**

---

### **Step 2: Copy from Mac**

**On your Mac (in Downloads folder):**

```bash
# Make sure you're in Downloads
cd ~/Downloads

# Check if key file exists
ls -la doc-anomaly-key.pem

# Copy streamlit_app directory to EC2
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM/streamlit_app" ec2-user@13.219.178.111:~/DOC\ ANOMALY\ DETECTION\ SYSTEM/
```

**Wait for copy to complete (may take a minute or two).**

---

### **Step 3: Reconnect to EC2**

**On your Mac:**

```bash
# Reconnect to EC2
ssh -i doc-anomaly-key.pem ec2-user@13.219.178.111

# Verify streamlit_app was copied
cd "DOC ANOMALY DETECTION SYSTEM"
ls -la streamlit_app/
ls -la streamlit_app/app.py
```

---

### **Step 4: Run Streamlit**

**On EC2:**

```bash
cd "DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate

# Now run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Quick Steps:**

1. **Exit EC2**: Type `exit` in EC2 terminal
2. **On Mac**: `cd ~/Downloads`
3. **On Mac**: Run `scp` command (from Mac, not EC2!)
4. **Reconnect EC2**: `ssh -i doc-anomaly-key.pem ec2-user@13.219.178.111`
5. **Verify**: `ls streamlit_app/`
6. **Run**: `streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0`

---

**First exit EC2, then run scp from your Mac!** 🚀





