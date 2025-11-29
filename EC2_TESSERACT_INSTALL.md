# 🔧 Installing Tesseract on Amazon Linux 2023

## ⚠️ **Problem:**

Tesseract is **not available** in Amazon Linux 2023 default repositories.

## ✅ **Solution Options:**

### **Option 1: Build Tesseract from Source (Recommended)**

```bash
# Install build dependencies
sudo yum install -y gcc gcc-c++ make autoconf automake libtool pkgconfig
sudo yum install -y libpng-devel libjpeg-devel libtiff-devel zlib-devel

# Install Leptonica (required by Tesseract)
cd /tmp
wget http://www.leptonica.org/source/leptonica-1.83.1.tar.gz
tar -xzf leptonica-1.83.1.tar.gz
cd leptonica-1.83.1
./configure
make
sudo make install
sudo ldconfig

# Install Tesseract
cd /tmp
wget https://github.com/tesseract-ocr/tesseract/archive/5.3.2.tar.gz
tar -xzf 5.3.2.tar.gz
cd tesseract-5.3.2
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

# Verify installation
tesseract --version
```

### **Option 2: Use Docker (Alternative)**

If building from source is too complex, we can make Tesseract optional and use it only when needed via Docker or skip OCR features.

### **Option 3: Install via Amazon Linux Extras or Alternative Repo**

```bash
# Try Amazon Linux extras
sudo amazon-linux-extras install epel -y
sudo yum install -y tesseract

# If that doesn't work, try:
sudo dnf install -y epel-release
sudo yum install -y tesseract
```

---

## 🎯 **Quick Fix: Make Tesseract Optional (Recommended for Now)**

Since Tesseract is complex to install on Amazon Linux 2023, let's:

1. **Install Python and other dependencies first**
2. **Make Tesseract optional** - the system will work without it
3. **Install Tesseract later** if needed

---

## ✅ **Recommended Steps:**

### **Step 1: Install Everything Else (Skip Tesseract for Now)**

```bash
# Update system
sudo yum update -y

# Install Python and build tools
sudo yum install -y python3 python3-pip python3-devel git curl
sudo yum install -y gcc g++ make
sudo yum groupinstall -y "Development Tools"

# Verify Python
python3 --version
pip3 --version
```

### **Step 2: Proceed Without Tesseract (For Now)**

The document processing system can work without Tesseract initially. OCR features will be disabled, but other features will work.

### **Step 3: Install Tesseract Later (Optional)**

We can install Tesseract from source later or make it optional in the code.

---

## 📋 **Next Steps:**

1. **Install Python and dependencies (without Tesseract)**
2. **Copy code to EC2**
3. **Set up environment**
4. **Test the system**
5. **Install Tesseract from source later if needed**

---

## 🔄 **Alternative: Try This Simpler Method First**

```bash
# Try to enable EPEL via dnf (Amazon Linux 2023 uses dnf under the hood)
sudo dnf install -y epel-release

# Then try installing Tesseract
sudo yum install -y tesseract tesseract-devel
```

---

**For now, let's proceed with installing Python and other dependencies, and make Tesseract optional!**





