# 🔧 SSH Connection Fix

## ❌ **Error You're Seeing:**
```bash
ssh -i doc-anomaly-key.pem ec2-user@<13.221.62.92>
zsh: parse error near `\n'
```

## ✅ **Solution:**

**The problem:** You're using angle brackets `< >` around the IP address. Remove them!

### **Correct Command:**
```bash
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

**Remove the `<` and `>` brackets!**

---

## 📋 **Step-by-Step:**

### **1. Navigate to Downloads (if not already there):**
```bash
cd ~/Downloads
```

### **2. Set Key Permissions (Important!):**
```bash
chmod 400 doc-anomaly-key.pem
```

### **3. Connect (WITHOUT brackets):**
```bash
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

---

## ⚠️ **Common Issues:**

### **Issue 1: "Permission denied (publickey)"**
**Fix:**
```bash
# Make sure key has correct permissions
chmod 400 doc-anomaly-key.pem

# Try again
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

### **Issue 2: "WARNING: UNPROTECTED PRIVATE KEY FILE!"**
**Fix:**
```bash
chmod 400 doc-anomaly-key.pem
```

### **Issue 3: Wrong username**
**For Amazon Linux:** `ec2-user`
**For Ubuntu:** `ubuntu`

**Try Ubuntu if ec2-user doesn't work:**
```bash
ssh -i doc-anomaly-key.pem ubuntu@13.221.62.92
```

---

## ✅ **Success Looks Like:**
```
The authenticity of host '13.221.62.92 (13.221.62.92)' can't be established.
ECDSA key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '13.221.62.92' (ECDSA) to the list of known hosts.

       __|  __|_  )
       _|  (     /   Amazon Linux 2023
      ___|\___|___|

[ec2-user@ip-xxx-xxx-xxx-xxx ~]$
```

---

## 🎯 **Quick Commands:**

```bash
# Navigate to Downloads
cd ~/Downloads

# Set permissions
chmod 400 doc-anomaly-key.pem

# Connect (NO BRACKETS!)
ssh -i doc-anomaly-key.pem ec2-user@13.221.62.92
```

---

**Try the corrected command without brackets!**





