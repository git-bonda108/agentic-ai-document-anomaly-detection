# 🔧 EC2 Disk Resize - Step by Step

## ⚠️ **Issue:**

EC2 instance ran out of disk space. Need to increase from 20GB to 40GB.

## ✅ **Solution: Resize EC2 Volume**

### **Step 1: Stop EC2 Instance (IMPORTANT - Don't Skip!)**

1. **Go to AWS Console**: https://console.aws.amazon.com/ec2/
2. **Login** with your AWS credentials
3. **Go to EC2 Dashboard** → **Instances**
4. **Find your instance**: `doc-anomaly-detection` (or similar)
5. **Select the instance**
6. **Click "Instance state"** → **"Stop instance"**
7. **Wait** for status to show "Stopped" (green dot)

**⚠️ DO NOT TERMINATE - Only STOP!**

---

### **Step 2: Modify Volume Size**

1. **Go to EC2** → **Elastic Block Store** → **Volumes**
2. **Find your instance's volume** (look for the volume attached to your instance)
3. **Select the volume**
4. **Click "Actions"** → **"Modify volume"**
5. **Change size**: From `20` to `40` GB
6. **Click "Modify"**
7. **Confirm** the change

---

### **Step 3: Start EC2 Instance**

1. **Go back to Instances**
2. **Select your instance**
3. **Click "Instance state"** → **"Start instance"**
4. **Wait** for status to show "Running" (green dot)
5. **Note the Public IP** (should be `13.221.62.92` or similar)

---

### **Step 4: SSH to EC2 and Resize Filesystem**

**On your Mac Terminal:**

```bash
# Navigate to Downloads
cd ~/Downloads

# SSH to EC2
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**Once connected to EC2, run:**

```bash
# Check current disk size (before resize)
df -h

# Resize the partition (for Amazon Linux 2023)
sudo growpart /dev/nvme0n1 1

# Resize the filesystem
sudo xfs_growfs /dev/nvme0n1p1

# OR if that doesn't work, try:
sudo resize2fs /dev/nvme0n1p1

# Verify new size
df -h
# Should now show ~40GB available
```

**Note:** The device name might be different. If above doesn't work:

```bash
# Find the device name
lsblk

# Use the actual device name from lsblk output
# Usually it's /dev/nvme0n1p1 or /dev/xvda1
```

---

### **Step 5: Clean Up and Install Requirements**

**On EC2:**

```bash
# Clean up space
sudo yum clean all
rm -rf ~/.cache/pip/*

# Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# Activate venv
source venv/bin/activate

# Now install full requirements
pip install -r requirements.txt

# This should work now with 40GB!
```

---

## 📋 **Quick Reference:**

1. **Stop EC2 instance** (AWS Console)
2. **Modify volume** → Increase to 40GB
3. **Start EC2 instance**
4. **SSH to EC2**
5. **Resize filesystem** (commands above)
6. **Install requirements**

---

## ✅ **After Resize:**

- Disk space: 40GB (was 20GB)
- Can install all requirements including XGBoost
- Full functionality available

---

**Follow steps 1-4 first, then SSH and resize filesystem!** 🚀





