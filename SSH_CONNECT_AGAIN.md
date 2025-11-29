# 🔌 SSH Connection - Quick Guide

## ✅ **Connect to EC2:**

**On your Mac Terminal (in Downloads):**

```bash
# Navigate to Downloads
cd ~/Downloads

# SSH to EC2
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**If connection fails, check:**
- EC2 instance is running (not stopped)
- Public IP is correct (check AWS Console)
- Key file has correct permissions: `chmod 400 doc-anomaly-key.pem`

---

## 🎯 **After Connecting:**

1. Check disk space: `df -h`
2. Resize filesystem if needed (see EC2_DISK_RESIZE_STEPS.md)
3. Navigate to project: `cd "DOC ANOMALY DETECTION SYSTEM"`
4. Activate venv: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`

---

**First resize the disk (see EC2_DISK_RESIZE_STEPS.md), then connect!** 🚀





