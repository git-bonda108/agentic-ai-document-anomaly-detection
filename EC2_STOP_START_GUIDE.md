# 💰 EC2 Stop/Start Guide - Save Costs

## ✅ **Quick Answer:**

**Yes!** Stopping EC2 will stop Streamlit, and you'll only pay for storage (very cheap)!

## 💰 **Cost Implications:**

### **When EC2 is Running:**
- **EC2 Instance Cost**: ~$0.083/hour for t3.large (~$60/month if running 24/7)
- **EBS Storage**: ~$0.10/month per GB (40GB = ~$4/month)
- **Data Transfer**: Minimal cost
- **Total**: ~$64/month if running 24/7

### **When EC2 is Stopped:**
- **EC2 Instance Cost**: $0.00 (no charge when stopped!)
- **EBS Storage**: ~$0.10/month per GB (40GB = ~$4/month) - Still charged
- **Total**: ~$4/month (only storage)

**💰 Savings: ~$60/month when stopped!**

---

## ✅ **How to Stop EC2:**

### **In AWS Console:**

1. Go to: https://console.aws.amazon.com/ec2/
2. Click **"Instances"**
3. Select your instance (`doc-anomaly-detection`)
4. Click **"Instance state"** → **"Stop instance"**
5. Confirm **"Stop"**
6. Wait for status to show **"Stopped"**

**⚠️ IMPORTANT: Choose "Stop" NOT "Terminate"!**
- **Stop** = Pause (can restart, data preserved)
- **Terminate** = Delete (cannot restart, data lost!)

---

## ✅ **What Happens When You Stop:**

- ✅ **Streamlit stops** (app no longer accessible)
- ✅ **All processes stop**
- ✅ **EC2 compute charges stop** (you save money!)
- ✅ **Data is preserved** (EBS volumes stay)
- ✅ **Public IP may change** (unless using Elastic IP)

---

## ✅ **How to Start EC2 Again:**

### **In AWS Console:**

1. Go to **"Instances"**
2. Select your stopped instance
3. Click **"Instance state"** → **"Start instance"**
4. Wait for status to show **"Running"**
5. **Get new Public IP** (it may have changed)
6. **SSH to EC2** and restart Streamlit

---

## ✅ **Restart Streamlit After Starting EC2:**

**After EC2 is running, SSH and start Streamlit:**

```bash
# SSH to EC2
ssh -i doc-anomaly-key.pem ec2-user@<NEW_PUBLIC_IP>

# Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# Activate venv
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Set Up Auto-Start Streamlit (Optional):**

**To automatically start Streamlit when EC2 starts:**

**On EC2, create a systemd service:**

```bash
# Create service file
sudo nano /etc/systemd/system/streamlit.service
```

**Paste this:**

```ini
[Unit]
Description=DOC Anomaly Detection Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM
Environment="PATH=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin"
EnvironmentFile=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/.env
ExecStart=/home/ec2-user/DOC ANOMALY DETECTION SYSTEM/venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit
```

**Now Streamlit will auto-start when EC2 starts!**

---

## 📋 **Quick Reference:**

- **Stop EC2**: AWS Console → Instance → Stop instance
- **Start EC2**: AWS Console → Instance → Start instance
- **Cost when stopped**: ~$4/month (storage only)
- **Cost when running**: ~$64/month (instance + storage)
- **Public IP**: May change after stop/start (get new IP from console)

---

## ✅ **Best Practice:**

**Stop EC2 when not in use to save costs!**

You can:
- Stop during nights/weekends
- Start only when needed
- Keep data safe (EBS preserved)
- Save ~$60/month when stopped

---

**Stop EC2 to save money - data is safe!** 💰





