# ⚡ Streamlit Quick Deployment - Quick Reference

## 🖥️ **Local Deployment (Current)**

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Kill existing processes
pkill -f streamlit

# 3. Launch
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0

# 4. Access
# http://localhost:8501
```

---

## ☁️ **EC2 Production Deployment**

### **Quick Steps:**

1. **Launch EC2 Instance** (t3.medium, Amazon Linux 2023)
2. **SSH into EC2:**
   ```bash
   ssh -i key.pem ec2-user@EC2_IP
   ```
3. **Install Dependencies:**
   ```bash
   sudo yum install -y python3 python3-pip git
   ```
4. **Clone Repository:**
   ```bash
   git clone https://github.com/git-bonda108/agentic-ai-document-anomaly-detection.git
   cd agentic-ai-document-anomaly-detection
   ```
5. **Setup Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
6. **Configure .env:**
   ```bash
   nano .env
   # Add: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, OPENAI_API_KEY
   ```
7. **Open Security Group Port 8501**
8. **Launch Streamlit:**
   ```bash
   streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
   ```
9. **Access:** http://EC2_PUBLIC_IP:8501

---

## 🌐 **Streamlit Cloud (Easiest)**

1. **Push code to GitHub** (already done ✅)
2. **Go to:** https://share.streamlit.io/
3. **Sign in with GitHub**
4. **New app** → Select repository
5. **Main file:** `streamlit_app/app.py`
6. **Add secrets** (AWS keys, OpenAI key)
7. **Deploy** → Get permanent URL

---

## 🐳 **Docker Deployment**

```bash
# Build
docker build -t doc-anomaly-streamlit .

# Run
docker run -d -p 8501:8501 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e AWS_REGION=us-east-1 \
  -e OPENAI_API_KEY=... \
  doc-anomaly-streamlit
```

---

## 🔧 **Common Commands**

### **Stop Streamlit:**
```bash
pkill -f streamlit
```

### **Check if Running:**
```bash
ps aux | grep streamlit
curl http://localhost:8501/_stcore/health
```

### **View Logs:**
```bash
# Local: Check terminal output
# EC2: sudo journalctl -u streamlit-app -f
```

### **Update & Restart:**
```bash
git pull origin main
pkill -f streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## ✅ **Required Environment Variables**

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
OPENAI_API_KEY=your_key
```

---

## 🔒 **Security Checklist**

- [ ] `.env` file not in git (✅ in .gitignore)
- [ ] Security group restricts port 8501 (production)
- [ ] IAM credentials have least privilege
- [ ] Credentials rotated regularly

---

**📖 Full Guide:** See `STREAMLIT_DEPLOYMENT_GUIDE.md` for detailed steps

