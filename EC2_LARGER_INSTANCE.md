# 🚀 Create New Larger EC2 Instance (t3.large with 80GB)

## ✅ **Solution: Create New Instance with More Storage**

Instead of waiting 6 hours, create a new larger instance!

## 📋 **Step 1: Launch New Instance**

**In AWS Console:**

1. **Go to**: EC2 → **Launch Instances**
2. **Name**: `doc-anomaly-detection-v2` (or similar)
3. **AMI**: Amazon Linux 2023 (same as before)
4. **Instance Type**: **t3.large** (2 vCPU, 8 GB RAM)
5. **Key Pair**: Use same key (`doc-anomaly-key`)
6. **Network Settings**: 
   - Same security group (or create new one)
   - **Port 8501** open to **0.0.0.0/0**
   - **SSH (port 22)** open
7. **Configure Storage**:
   - **Volume size**: **80 GB** (or more!)
   - **Volume type**: gp3
8. **Launch Instance**

---

## 📋 **Step 2: Copy Code to New Instance**

**On your Mac:**

```bash
# Get new instance's public IP from AWS Console
# Example: 54.123.45.67 (replace with actual IP)

cd ~/Downloads

# Copy code to new instance
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM" ec2-user@<NEW_IP>:~/
```

---

## 📋 **Step 3: Set Up on New Instance**

**SSH to new instance:**

```bash
ssh -i doc-anomaly-key.pem ec2-user@<NEW_IP>
```

**On EC2:**

```bash
# Navigate to project
cd "DOC ANOMALY DETECTION SYSTEM"

# Remove old venv (if copied)
rm -rf venv

# Create new venv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Create .env file
nano .env
# (paste credentials)

# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📋 **Alternative: Install Without XGBoost GPU Packages**

**If you want to use current instance (40GB), skip heavy GPU packages:**

**On EC2 (current instance):**

```bash
# Install essential packages only (no GPU packages)
pip install --no-cache-dir streamlit openai boto3 pandas numpy python-dotenv PyPDF2 python-docx Pillow plotly matplotlib seaborn scikit-learn

# Install XGBoost CPU-only (much smaller, no CUDA)
pip install --no-cache-dir xgboost --no-binary :all:

# OR skip XGBoost for now
# System will work without ML features
```

---

## 🎯 **Recommended:**

**Option 1**: Create new t3.large instance with 80GB (clean start)  
**Option 2**: Install without GPU packages on current instance (quick fix)

---

## 📋 **Quick Decision:**

- **Want full ML features?** → Create new instance (80GB)
- **Just want Streamlit running?** → Install without GPU packages

---

**Create new instance or install without GPU packages?** 🚀





