# 💾 Increase EC2 Disk to 60GB - Online Resize

## ✅ **Good News: You Can Resize While Running!**

You don't need to stop the instance - EBS supports **online resizing**!

## 📋 **Step-by-Step:**

### **Step 1: Resize Volume in AWS Console**

1. **Go to AWS Console**: https://console.aws.amazon.com/ec2/
2. **Navigate to**: EC2 → **Elastic Block Store** → **Volumes**
3. **Find your instance's volume** (look for volume attached to your instance)
4. **Select the volume**
5. **Click "Actions"** → **"Modify volume"**
6. **Change size**: From `40` to `60` GB (or `80` GB if you want even more)
7. **Click "Modify"**
8. **Confirm** the change

**⏱️ Wait 1-2 minutes for modification to complete**

---

### **Step 2: Resize Filesystem (On EC2)**

**On your EC2 instance (you don't need to disconnect):**

```bash
# Check current size (before resize)
df -h

# Wait for volume modification to complete (1-2 minutes)
# Check if partition can be grown
sudo growpart /dev/nvme0n1 1

# Resize the filesystem
sudo xfs_growfs /dev/nvme0n1p1

# Verify new size
df -h
# Should now show ~60GB available
```

**If growpart says "NOCHANGE", the partition is already at max size.**
**Just run xfs_growfs to extend the filesystem.**

---

### **Step 3: Clean Up and Continue Installation**

**On EC2:**

```bash
# Clean up pip cache
pip cache purge
rm -rf ~/.cache/pip/*

# Check space
df -h

# Now install without cache
pip install --no-cache-dir -r requirements.txt
```

---

## 🎯 **Recommended Sizes:**

- **60GB**: Should be enough for all packages
- **80GB**: Safe buffer for future growth

---

## 📋 **Quick Steps:**

1. **AWS Console** → Volumes → Modify → **60GB** (or **80GB**)
2. **Wait 1-2 minutes**
3. **On EC2**: `sudo growpart /dev/nvme0n1 1` (if needed)
4. **On EC2**: `sudo xfs_growfs /dev/nvme0n1p1`
5. **On EC2**: `df -h` to verify
6. **On EC2**: `pip install --no-cache-dir -r requirements.txt`

---

## ⚠️ **Important:**

- **Don't stop the instance** - online resize works!
- **Wait 1-2 minutes** after modifying volume
- **Then resize filesystem** on EC2

---

**Go to AWS Console and resize volume to 60GB (or 80GB)!** 🚀





