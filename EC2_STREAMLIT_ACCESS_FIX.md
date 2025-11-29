# 🔧 Fix Streamlit Access - Troubleshooting

## ⚠️ **Issue:**

Can't access Streamlit app at `http://13.219.178.111:8501`

## ✅ **Step-by-Step Troubleshooting:**

### **Step 1: Check Security Group (Most Common Issue)**

**In AWS Console:**

1. **Select your instance** (i-0b3ec476d654012b5)
2. **Click "Security" tab** (bottom panel)
3. **Click on Security group name** (e.g., `doc-anomaly-sg`)
4. **Check "Inbound rules"**:
   - **Look for Custom TCP rule with port 8501**
   - If **missing**, add it:
     - Click **"Edit inbound rules"**
     - Click **"Add rule"**
     - **Type**: Custom TCP
     - **Port range**: 8501
     - **Source**: 0.0.0.0/0
     - Click **"Save rules"**

---

### **Step 2: Verify Streamlit is Running on EC2**

**SSH to EC2:**

```bash
# On your Mac
cd ~/Downloads
ssh -i doc-anomaly-key.pem ec2-user@13.219.178.111

# On EC2, check if Streamlit is running
ps aux | grep streamlit

# Check if port 8501 is listening
netstat -tuln | grep 8501
# OR
sudo lsof -i :8501
```

**If not running, start it:**

```bash
# On EC2
cd "DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

### **Step 3: Check Firewall/Security Group**

**In AWS Console:**

1. **Go to**: EC2 → **Security Groups**
2. **Find your instance's security group**
3. **Check Inbound Rules**:
   - Must have: **Custom TCP, Port 8501, Source: 0.0.0.0/0**

---

### **Step 4: Test Connection**

**On your Mac:**

```bash
# Test if port is accessible
telnet 13.219.178.111 8501
# OR
curl -v http://13.219.178.111:8501

# If connection refused, security group is blocking
# If timeout, instance might not be accessible
```

---

## 🎯 **Most Likely Issue: Security Group**

**90% of access issues are Security Group related!**

**Fix:**

1. **AWS Console** → Select instance → **Security** tab
2. **Click Security group name**
3. **Edit inbound rules**
4. **Add rule**: Custom TCP, Port 8501, Source: 0.0.0.0/0
5. **Save rules**
6. **Try again**: `http://13.219.178.111:8501`

---

## 📋 **Quick Checklist:**

- [ ] Security Group allows port 8501 (0.0.0.0/0)
- [ ] Streamlit is running on EC2
- [ ] Using correct URL: `http://13.219.178.111:8501`
- [ ] Instance is in "Running" state

---

**Check Security Group first - that's usually the issue!** 🚀





