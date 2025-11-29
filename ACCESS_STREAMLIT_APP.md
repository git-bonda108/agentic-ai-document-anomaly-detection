# 🌐 Access Your Streamlit App

## ✅ **Streamlit is Running!**

Your Streamlit app is running on EC2. Now you need to access it from your browser!

## 🌐 **How to Access:**

### **Step 1: Get Your EC2 Public IP**

**In AWS Console:**

1. Go to: https://console.aws.amazon.com/ec2/
2. Click **"Instances"**
3. Find your instance (`doc-anomaly-detection`)
4. Look at **"Public IPv4 address"** - copy this IP
5. **Example:** `44.220.247.17` (your IP will be different!)

---

### **Step 2: Open in Browser**

**On your Mac (or any computer):**

Open your web browser and go to:

```
http://<YOUR_EC2_PUBLIC_IP>:8501
```

**Example:**
- If your EC2 IP is `44.220.247.17`, go to:
- `http://44.220.247.17:8501`

---

### **Step 3: Check Security Group**

**If you can't access it, check Security Group:**

**In AWS Console:**

1. Select your EC2 instance
2. Click **"Security"** tab
3. Click on **Security group name**
4. Check **"Inbound rules"**:
   - Should have **Custom TCP, Port 8501, Source: 0.0.0.0/0**
   - If missing, add it:
     - Type: **Custom TCP**
     - Port: **8501**
     - Source: **0.0.0.0/0**
     - Click **"Save rules"**

---

## 🎯 **Quick Steps:**

1. **Get EC2 Public IP** from AWS Console
2. **Open browser**: `http://<EC2_IP>:8501`
3. **If can't access**: Add Security Group rule for port 8501

---

## 📋 **Example:**

**If your EC2 Public IP is `44.220.247.17`:**

**Open in browser:**
```
http://44.220.247.17:8501
```

---

**Get your EC2 Public IP from AWS Console and open it in your browser!** 🚀





