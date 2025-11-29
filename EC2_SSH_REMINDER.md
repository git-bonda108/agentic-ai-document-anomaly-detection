# ⚠️ IMPORTANT: Run Commands on EC2, Not Mac!

## 🎯 **Current Issue:**

You're running commands on your **Mac**, but they need to run on your **EC2 instance**!

## ✅ **Solution: Connect to EC2 First**

### **Step 1: Connect to EC2**

**On your Mac Terminal (in Downloads folder):**

```bash
# Make sure you're in Downloads
cd ~/Downloads

# Connect to EC2
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**After connecting, you should see:**
```
[ec2-user@ip-172-31-69-250 ~]$
```

**Notice:** Your prompt changes from `macbook@mac` to `ec2-user@ip-172-31-69-250`!

---

## ✅ **Step 2: Now Run Commands on EC2**

**Once connected to EC2, run these commands:**

```bash
# Install pip3 (on EC2)
sudo yum install -y python3-pip

# Verify
pip3 --version
python3 --version

# Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# List files to verify
ls -la
```

---

## 🔍 **How to Tell Where You Are:**

### **On Mac:**
```
(base) macbook@mac Downloads %
```
or
```
(base) macbook@mac ~ %
```

### **On EC2:**
```
[ec2-user@ip-172-31-69-250 ~]$
```
or
```
[ec2-user@ip-172-31-69-250 DOC ANOMALY DETECTION SYSTEM]$
```

---

## 📋 **Complete Process:**

### **1. On Mac: Connect to EC2**
```bash
cd ~/Downloads
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

### **2. On EC2: Install pip3**
```bash
sudo yum install -y python3-pip
pip3 --version
```

### **3. On EC2: Go to project**
```bash
cd "DOC ANOMALY DETECTION SYSTEM"
ls -la
```

### **4. On EC2: Set up environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **5. On EC2: Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **6. On EC2: Create .env**
```bash
nano .env
# (paste credentials, save with Ctrl+X, Y, Enter)
```

### **7. On EC2: Run Streamlit**
```bash
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## ✅ **Quick Reference:**

**To connect to EC2:**
```bash
cd ~/Downloads
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**To exit EC2 and return to Mac:**
```bash
exit
```

---

## 🎯 **Next Step:**

**1. Connect to EC2:**
```bash
cd ~/Downloads
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**2. Once connected (you'll see `[ec2-user@...]`), then run:**
```bash
sudo yum install -y python3-pip
pip3 --version
cd "DOC ANOMALY DETECTION SYSTEM"
ls -la
```

---

**SSH into EC2 first, then run the commands there!** 🚀





