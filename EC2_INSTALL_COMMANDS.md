# ✅ EC2 Installation Commands - Ready to Run

## 🎯 **Run These Commands on Your EC2 Instance:**

### **Step 1: Update System**
```bash
sudo yum update -y
```

### **Step 2: Install Python and Dependencies**
```bash
sudo yum install -y python3 python3-pip python3-devel git curl
sudo yum install -y gcc g++ make
sudo yum groupinstall -y "Development Tools"
```

### **Step 3: Verify Installations**
```bash
python3 --version
pip3 --version
git --version
```

**Expected Output:**
- Python 3.11 or 3.12 (not 3.13 - that's fine!)
- pip3 version
- git version

---

## ✅ **Tesseract is OPTIONAL**

**Note:** Tesseract OCR is **NOT required** for the system to work!
- ✅ PDF processing works without Tesseract
- ✅ DOCX processing works without Tesseract
- ⚠️  Image OCR will be disabled (but PDFs/DOCX work fine)

**The system is ready to proceed without Tesseract!**

---

## 📋 **Next Steps:**

1. ✅ Install Python (commands above)
2. ✅ Copy code to EC2 (Step 4 from deployment guide)
3. ✅ Set up virtual environment
4. ✅ Install Python dependencies
5. ✅ Configure environment variables
6. ✅ Run Streamlit

---

## 🚀 **After Installing Python:**

Continue with **Step 4: Copy Code to EC2** from `EC2_DEPLOYMENT_STEPS.md`

---

**Run the installation commands above, then continue!** ✅





