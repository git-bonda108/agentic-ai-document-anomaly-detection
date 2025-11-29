# 🔍 Finding Project Directory on EC2

## ⚠️ **Issue:**

The project directory isn't found in `~` (home directory).

## ✅ **Solution: Check Different Locations**

### **Step 1: Check Home Directory Contents**

**On EC2:**

```bash
# List all files (including hidden)
ls -la

# Check if it's in a subdirectory
find ~ -name "*ANOMALY*" -type d 2>/dev/null

# Or search more broadly
find ~ -name "*DOC*" -type d 2>/dev/null
```

### **Step 2: Check Root Directory**

**On EC2:**

```bash
# Check root
ls -la /

# Check if it's in /home
ls -la /home/ec2-user/
```

### **Step 3: If Not Found - Copy Again from Mac**

If the project directory isn't found, copy it again from your Mac.

**On your Mac (in Downloads):**

```bash
# Make sure you're in Downloads
cd ~/Downloads

# Copy project again (will overwrite if exists)
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@13.221.62.92:~/

# Wait for copy to complete (this may take a few minutes)
```

**Then back on EC2:**

```bash
# List files
ls -la

# Should now see "DOC ANOMALY DETECTION SYSTEM" folder
```

### **Step 4: Navigate to Project**

**On EC2:**

```bash
# Navigate to project
cd ~/DOC\ ANOMALY\ DETECTION\ SYSTEM

# OR use quotes
cd ~/"DOC ANOMALY DETECTION SYSTEM"

# Verify you're in the right place
ls -la
# Should see: agents/, streamlit_app/, requirements.txt, etc.
```

---

## 🎯 **Quick Fix:**

**Option 1: If directory exists somewhere**
```bash
# Search for it
find ~ -type d -name "*DOC*" 2>/dev/null

# Then cd to the path it shows
```

**Option 2: Copy again from Mac**
```bash
# On Mac (Downloads folder)
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@13.221.62.92:~/

# Then on EC2
ls -la
cd ~/"DOC ANOMALY DETECTION SYSTEM"
```

---

## ✅ **Alternative: Use Git (If You Have Repo)**

**On EC2:**

```bash
# Clone from Git (if you have a repo)
git clone <your-repo-url>
cd doc-anomaly-detection
```

---

**Let's first check if it exists somewhere, or copy it again!**





