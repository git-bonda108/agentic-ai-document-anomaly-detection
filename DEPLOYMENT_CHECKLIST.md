# ✅ EC2 Deployment Checklist

## 📋 **Before You Start**

- [ ] AWS Console access ready (bond-admin / Krsna&2022)
- [ ] Region: us-east-1
- [ ] EC2 service access enabled

---

## 🚀 **Step-by-Step Checklist**

### **Step 1: Launch EC2 Instance**
- [ ] Go to EC2 Console
- [ ] Click "Launch Instance"
- [ ] Name: `doc-anomaly-detection`
- [ ] AMI: Amazon Linux 2023 or Ubuntu 22.04
- [ ] Instance Type: t3.medium (minimum) or t3.large (recommended)
- [ ] Key Pair: Create and download `doc-anomaly-key.pem`
- [ ] Security Group: Port 8501 open to 0.0.0.0/0
- [ ] Launch instance
- [ ] Wait for "Running" status
- [ ] Note Public IPv4 address

### **Step 2: Connect to EC2**
- [ ] Open Terminal on Mac
- [ ] Navigate to Downloads: `cd ~/Downloads`
- [ ] Set key permissions: `chmod 400 doc-anomaly-key.pem`
- [ ] Connect: `ssh -i doc-anomaly-key.pem ec2-user@<PUBLIC_IP>`
- [ ] Successfully connected ✓

### **Step 3: Install System Dependencies**
- [ ] Update system: `sudo yum update -y` (Amazon Linux) or `sudo apt-get update` (Ubuntu)
- [ ] Install Python 3.13
- [ ] Install pip: `python3.13 -m pip --version`
- [ ] Install Tesseract: `sudo yum install tesseract` or `sudo apt-get install tesseract-ocr`
- [ ] Install git: `git --version`
- [ ] Verify all installed ✓

### **Step 4: Copy Code to EC2**
- [ ] **Option A: SCP**
  - [ ] From Mac: `scp -i doc-anomaly-key.pem -r "DOC ANOMALY DETECTION SYSTEM" ec2-user@<PUBLIC_IP>:~/`
- [ ] **Option B: Git**
  - [ ] Push code to Git repo
  - [ ] On EC2: `git clone <repo-url>`
- [ ] Code copied successfully ✓

### **Step 5: Set Up Python Environment**
- [ ] Navigate to project: `cd "DOC ANOMALY DETECTION SYSTEM"`
- [ ] Create venv: `python3.13 -m venv venv`
- [ ] Activate: `source venv/bin/activate`
- [ ] Upgrade pip: `pip install --upgrade pip`
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Install XGBoost: `pip install xgboost`
- [ ] Verify: `pip list | grep -E "streamlit|openai|boto3|xgboost"`
- [ ] All dependencies installed ✓

### **Step 6: Configure Environment**
- [ ] Create .env file: `nano .env`
- [ ] Paste credentials (see EC2_DEPLOYMENT_STEPS.md)
- [ ] Save file (Ctrl+X, Y, Enter)
- [ ] OR export variables
- [ ] Test AWS connection: `python -c "from aws.s3_handler import S3Handler; print('OK')"`
- [ ] Configuration verified ✓

### **Step 7: Test Streamlit (Quick)**
- [ ] Run: `nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &`
- [ ] Check logs: `tail -f streamlit.log`
- [ ] Access: `http://<PUBLIC_IP>:8501`
- [ ] App loads successfully ✓

### **Step 8: Set Up System Service**
- [ ] Create service file: `sudo nano /etc/systemd/system/streamlit.service`
- [ ] Paste service config (see EC2_DEPLOYMENT_STEPS.md)
- [ ] Adjust paths in service file
- [ ] Reload systemd: `sudo systemctl daemon-reload`
- [ ] Enable service: `sudo systemctl enable streamlit`
- [ ] Start service: `sudo systemctl start streamlit`
- [ ] Check status: `sudo systemctl status streamlit`
- [ ] Service running ✓

### **Step 9: Set Up Public Access**
- [ ] Get public IP: `curl http://169.254.169.254/latest/meta-data/public-ipv4`
- [ ] Test access from browser: `http://<PUBLIC_IP>:8501`
- [ ] **Optional: Nginx reverse proxy**
  - [ ] Install Nginx
  - [ ] Configure reverse proxy
  - [ ] Access via port 80
- [ ] Public access working ✓

### **Step 10: Verify Full Functionality**
- [ ] Upload & Process: Upload sample document
- [ ] Results Dashboard: View results and anomalies
- [ ] Batch Processing: Test S3 folder processing
- [ ] Human Feedback: Provide feedback
- [ ] Metrics: View performance metrics
- [ ] Observability: Check agent status
- [ ] Training: View training management
- [ ] All features working ✓

---

## 🎯 **Expected Results**

### **After Deployment:**
- ✅ Streamlit accessible at: `http://<EC2_PUBLIC_IP>:8501`
- ✅ All 7 pages functional
- ✅ Document processing working
- ✅ AWS services connected (S3, DynamoDB, CloudWatch)
- ✅ GPT-4o integration working
- ✅ Batch processing from S3 working
- ✅ ML training with XGBoost ready
- ✅ Reinforcement learning from feedback working
- ✅ Human-in-the-loop functional

### **Public URL Format:**
- Direct: `http://<EC2_PUBLIC_IP>:8501`
- With Nginx: `http://<EC2_PUBLIC_IP>` (port 80)
- With domain: `http://your-domain.com:8501`

---

## 📋 **ML/RL Implementation Status**

### **✅ Implemented:**
- ✅ TrainingAgent with model training
- ✅ XGBoost support (upgraded)
- ✅ Reinforcement learning from feedback
- ✅ Human-in-the-loop feedback collection
- ✅ Model versioning
- ✅ Training metrics (F1, Precision, Recall)

### **✅ Features:**
- ✅ Supervised learning from labeled data
- ✅ RL updates from human feedback
- ✅ Active learning capability
- ✅ Model retraining pipeline
- ✅ Performance tracking

---

## ⚠️ **Common Issues & Solutions**

### **Issue: Can't connect to EC2**
**Solution:**
- Check Security Group: SSH (port 22) open to your IP
- Check key file permissions: `chmod 400 doc-anomaly-key.pem`
- Verify public IP is correct

### **Issue: Streamlit not accessible**
**Solution:**
- Check Security Group: Port 8501 open to 0.0.0.0/0
- Check service running: `sudo systemctl status streamlit`
- Check logs: `sudo journalctl -u streamlit -n 50`

### **Issue: AWS connection fails**
**Solution:**
- Verify .env file exists and has credentials
- Check IAM permissions
- Test: `aws sts get-caller-identity`

### **Issue: XGBoost not found**
**Solution:**
- Install: `pip install xgboost`
- Verify: `python -c "import xgboost; print('OK')"`

---

## ✅ **Completion Criteria**

**Deployment is complete when:**
- [ ] Streamlit accessible at public URL
- [ ] All pages load correctly
- [ ] Document processing works
- [ ] AWS services connected
- [ ] Can upload and process documents
- [ ] Can batch process from S3
- [ ] Can provide feedback
- [ ] Can view metrics

---

**🎉 Once all checkboxes are complete, your system is deployed and ready!**





