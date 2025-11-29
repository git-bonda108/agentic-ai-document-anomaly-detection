# 🔌 EC2 SSH Connection Fix

## ⚠️ **Issues:**

1. **SSH timeout**: Can't connect to EC2
2. **growpart**: That command runs ON EC2, not on your Mac

## ✅ **Solution:**

### **Step 1: Check EC2 Instance Status**

**In AWS Console:**

1. Go to: https://console.aws.amazon.com/ec2/
2. Click **"Instances"**
3. Find your instance (`doc-anomaly-detection` or similar)
4. Check **"Instance state"**:
   - Should be **"Running"** (green dot)
   - If **"Stopped"**, click **"Start instance"**
   - If **"Stopping"**, wait for it to finish, then start

### **Step 2: Get Current Public IP**

**In AWS Console:**

1. Select your instance
2. Look at **"Public IPv4 address"** (this might have changed!)
3. **Copy the new IP address**

**Note:** Public IPs change when you stop/start an instance (unless you use Elastic IP)

### **Step 3: Check Security Group**

**In AWS Console:**

1. Select your instance
2. Click **"Security"** tab
3. Click on **Security group name**
4. Check **"Inbound rules"**:
   - Should have **SSH (port 22)** from **"My IP"** or **0.0.0.0/0**
   - If missing, add it:
     - Type: SSH
     - Port: 22
     - Source: My IP (or 0.0.0.0/0 for testing)

### **Step 4: SSH with Correct IP**

**On your Mac:**

```bash
cd ~/Downloads

# Use the NEW public IP from AWS Console
ssh -i doc-anomaly-key.pem ec2-user@<NEW_IP_ADDRESS>

# For example, if new IP is 54.123.45.67:
ssh -i doc-anomaly-key.pem ec2-user@54.123.45.67
```

---

## 📋 **Quick Check:**

**In AWS Console, verify:**
- ✅ Instance is "Running"
- ✅ Public IP address (copy it)
- ✅ Security group allows SSH (port 22)

**Then SSH with the new IP:**

```bash
ssh -i doc-anomaly-key.pem ec2-user@<NEW_IP>
```

---

## ⚠️ **Important Notes:**

1. **Public IPs change** when you stop/start an instance
2. **growpart** runs ON EC2, not on your Mac
3. **Check AWS Console** for current status and IP

---

## 🎯 **Steps:**

1. **Check AWS Console** → Instance status and Public IP
2. **SSH with new IP** (if instance is running)
3. **Once connected to EC2**, then run growpart commands

---

**First check AWS Console for instance status and new IP address!** 🚀





