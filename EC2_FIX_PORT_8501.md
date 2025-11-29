# 🔧 Fix Port 8501 Already in Use

## ✅ **Issue:**

Port 8501 is already in use (likely from previous attempt)

## ✅ **Solution:**

### **Step 1: Kill Process Using Port 8501**

**On EC2:**

```bash
# Find process using port 8501
sudo lsof -ti:8501 | xargs sudo kill -9

# OR
sudo pkill -f streamlit

# Verify port is free
sudo lsof -i :8501
# Should show nothing
```

### **Step 2: Run Streamlit**

**On EC2 (with venv activated):**

```bash
cd "DOC ANOMALY DETECTION SYSTEM"
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🎯 **Quick Commands:**

```bash
# Kill existing process
sudo pkill -f streamlit

# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

**Kill the old process, then run Streamlit!** 🚀





