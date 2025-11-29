# 🔧 EC2 Installation Fix - Amazon Linux 2023

## ⚠️ **Issues Found:**

1. `python3.13` not found - Amazon Linux 2023 might come with Python 3.11 or 3.12
2. `tesseract` package not found - Need to use correct package name

## ✅ **Solution:**

### **Step 1: Check Available Python Version**

```bash
# Check what Python version is available
python3 --version
```

**Amazon Linux 2023 typically comes with Python 3.11 or 3.12.**

### **Step 2: Install Python and Dependencies (Correct Commands)**

**For Amazon Linux 2023:**
```bash
# Update system
sudo yum update -y

# Install Python 3 (whatever version is available, likely 3.11)
sudo yum install -y python3 python3-pip python3-devel git curl gcc g++ make

# Install Tesseract OCR (correct package name)
sudo yum install -y tesseract tesseract-devel

# Install build tools (needed for some Python packages)
sudo yum groupinstall -y "Development Tools"
```

### **Step 3: Verify Installations**

```bash
# Check Python version
python3 --version

# Check pip
pip3 --version

# Check Tesseract
tesseract --version

# Check git
git --version
```

---

## 🔄 **Alternative: If You Need Python 3.13**

If you specifically need Python 3.13, you'll need to compile from source:

```bash
# Install prerequisites
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel readline-devel sqlite-devel

# Download and compile Python 3.13
cd /tmp
wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
tar xzf Python-3.13.0.tgz
cd Python-3.13.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Create symlink
sudo ln -sf /usr/local/bin/python3.13 /usr/bin/python3.13
```

**However, Python 3.11 or 3.12 should work fine for this project!**

---

## ✅ **Recommended: Use Default Python (Easier)**

Since Amazon Linux 2023 likely has Python 3.11 or 3.12, let's use that:

```bash
# Install available Python version
sudo yum install -y python3 python3-pip python3-devel git curl gcc g++ make

# Install Tesseract
sudo yum install -y tesseract tesseract-devel

# Verify
python3 --version
pip3 --version
tesseract --version
```

---

## 📋 **After Installation:**

Once Python and Tesseract are installed, you can:

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install requirements:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 🎯 **Quick Fix Commands:**

Run these commands on your EC2 instance:

```bash
# Update system
sudo yum update -y

# Install Python 3 (default version)
sudo yum install -y python3 python3-pip python3-devel git curl gcc g++ make

# Install Tesseract
sudo yum install -y tesseract tesseract-devel

# Verify
python3 --version
pip3 --version
tesseract --version
```

**This should work!** ✅





