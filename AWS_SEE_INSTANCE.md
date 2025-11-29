# 👁️ How to See Your Stopped Instance in AWS Console

## ⚠️ **Issue:**

You can't see your instance because the filter shows "Instance state = running"
But your instance is now **stopped**!

## ✅ **Solution: Remove or Change Filter**

### **Step 1: Remove the Filter**

**In AWS Console:**

1. **Look at the filter chip** that says "Instance state = running"
2. **Click the X** on that filter chip to remove it
3. **OR click "Clear filters"** button

**Now you should see your instance!**

---

### **Step 2: Change Filter to "All States"**

**In AWS Console:**

1. **Click the dropdown** that says "All states"
2. **Select "All states"** (or uncheck specific states)
3. **Your stopped instance will now appear!**

---

### **Step 3: Find Your Instance**

**You should now see:**
- Instance ID: `i-0b3ec476d654012b5`
- Name: `doc-anomaly-detection`
- State: **Stopped** (not running)

---

### **Step 4: Resize Volume**

**Once you see your instance:**

1. **Click on your instance** to select it
2. **Look at the bottom panel** - click **"Storage"** tab
3. **You'll see the volume** attached to the instance
4. **Click on the volume ID** (or go to Volumes section)
5. **Actions** → **"Modify volume"**
6. **Change size** to **60GB** or **80GB**
7. **Modify** and confirm

---

## 📋 **Quick Steps:**

1. **Remove filter**: Click **X** on "Instance state = running" filter
2. **See instance**: Your stopped instance will appear
3. **Select instance**: Click on it
4. **Go to Storage tab**: Click "Storage" in bottom panel
5. **Click volume**: Click the volume ID
6. **Modify volume**: Actions → Modify volume → **60GB**
7. **Start instance**: After modifying, start the instance

---

**Remove the filter and you'll see your instance!** 🚀





