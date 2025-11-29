# 🤖 DOC Anomaly Detection System

**Enterprise-grade Agentic AI System** for intelligent document processing and anomaly detection in leasing contracts and invoices.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![AWS](https://img.shields.io/badge/AWS-Enabled-orange.svg)](https://aws.amazon.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com/)

---

## 🚀 **Quick Deploy to Streamlit Cloud**

### **Main File:** `streamlit_app/app.py` ✅

**3 Steps to Deploy:**
1. Go to: https://share.streamlit.io/
2. Select repo: `git-bonda108/agentic-ai-document-anomaly-detection`
3. **Main file path:** `streamlit_app/app.py` ← **USE THIS!**

**Add Secrets (in Streamlit Cloud → Advanced settings):**
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
OPENAI_API_KEY=your_key
```

📖 **Full deployment guide:** See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Anomaly Detection](#anomaly-detection)
- [AWS Integration](#aws-integration)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **DOC Anomaly Detection System** is a production-ready, agentic AI solution that automatically processes leasing contracts and invoices to detect anomalies, discrepancies, and compliance issues. Built with **OpenAI GPT-4o** and **AWS-native services**, it provides:

- **Intelligent Document Processing** - Multi-format support (PDF, DOCX, images)
- **Advanced Anomaly Detection** - 6+ anomaly types with ML-powered classification
- **Human-in-the-Loop (HITL)** - Reinforcement learning from human feedback
- **Full Observability** - Complete agent monitoring, token usage, and cost tracking
- **Batch Processing** - Process entire S3 folders automatically
- **Enterprise-Ready** - Scalable, secure, and production-tested

---

## ✨ Key Features

### 🤖 **Agentic AI Architecture**
- **8 Specialized Agents** working autonomously:
  - `OrchestratorManager` - Central workflow coordinator
  - `DocumentIngestionAgent` - Document upload and validation
  - `ExtractionAgent` - GPT-4o powered field extraction
  - `ContractInvoiceComparisonAgent` - Cross-document anomaly detection
  - `AnomalyDetectionAgent` - General anomaly detection
  - `ValidationAgent` - Business rules validation
  - `BatchIngestionAgent` - S3 folder batch processing
  - `TrainingAgent` - ML model training and RL

### 📊 **Anomaly Detection Types**
1. **Date Mismatches** - Invoice vs Contract date discrepancies
2. **Amount Discrepancies** - Payment amount validation
3. **Schedule Misses** - Missing scheduled payments
4. **Surplus Payments** - Overpayments detected
5. **Missed Payments** - Underpayments identified
6. **Schedule Misalignment** - Payment date mismatches
7. **PO Mismatches** - Purchase order inconsistencies
8. **Format Issues** - Non-standard document formats

### 🎨 **Streamlit Interface**
- **7 Interactive Pages**:
  - 📄 Upload & Process - Single document processing
  - 📦 Batch Processing (S3) - Process S3 folders
  - 📊 Results Dashboard - Anomaly visualization
  - 👤 Human Feedback - HITL feedback collection
  - 📈 Metrics & Analytics - Performance metrics
  - 👁️ Observability - Agent monitoring
  - 🧠 Training Management - Model training

### ☁️ **AWS Integration**
- **S3** - Document storage (raw, processed, embeddings, models)
- **DynamoDB** - Metadata, feedback, business rules, results
- **CloudWatch** - Logging, metrics, observability
- **EC2** - Deployment-ready infrastructure

### 🧠 **Machine Learning**
- **XGBoost Classifier** - Supervised anomaly detection
- **Reinforcement Learning** - Model updates from human feedback
- **Model Versioning** - Track and manage model versions
- **Performance Metrics** - F1 score, precision, recall, confusion matrix

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit Web Interface                     │
│  (Upload | Batch | Results | Feedback | Metrics)        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            Orchestrator Manager                          │
│  (Workflow Coordination | Context Management | HITL)    │
└──────┬──────────┬──────────┬──────────┬────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Ingestion │ │Extraction│ │Contract- │ │Anomaly  │
│  Agent   │ │  Agent   │ │ Invoice  │ │Detection│
│          │ │ (GPT-4o) │ │  Agent   │ │  Agent   │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Validation Agent                            │
│         (Business Rules | Thresholds)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    AWS Services                          │
│  S3 (Storage) | DynamoDB (Data) | CloudWatch (Logs)     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- AWS Account with IAM credentials (optional, for scalability)
- OpenAI API Key (GPT-4o access)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/git-bonda108/agentic-ai-document-anomaly-detection.git
cd agentic-ai-document-anomaly-detection
```

### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file:
```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
OPENAI_API_KEY=your_openai_key
```

### 4. Set Up AWS Infrastructure
```bash
python setup_aws_infrastructure.py
```

### 5. Launch Streamlit App
```bash
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
```

### 6. Access Application
Open browser: `http://localhost:8501`

---

## 📦 Installation

### System Requirements
- **OS**: macOS, Linux, or Windows
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd "DOC ANOMALY DETECTION SYSTEM"
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Install optional dependencies (for OCR):**
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Amazon Linux 2023 (optional - OCR not required)
# Tesseract not available in default repos
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# OpenAI API
OPENAI_API_KEY=sk-proj-...

# Optional: Custom S3 Bucket Names
S3_RAW_BUCKET=doc-anomaly-raw-docs-597088017095
S3_PROCESSED_BUCKET=doc-anomaly-processed-597088017095
S3_EMBEDDINGS_BUCKET=doc-anomaly-embeddings-597088017095
S3_ML_MODELS_BUCKET=doc-anomaly-ml-models-597088017095
```

### AWS IAM Permissions

Required IAM permissions:
- **S3**: `s3:GetObject`, `s3:PutObject`, `s3:ListBucket`
- **DynamoDB**: `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Query`, `dynamodb:Scan`
- **CloudWatch**: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

See `AWS_ACCESS_REQUIREMENTS.md` for detailed permissions.

---

## 📖 Usage

### Single Document Processing

1. **Navigate to "📄 Upload & Process"**
2. **Upload a document** (PDF, DOCX, or image)
3. **Click "Process Document"**
4. **View results** in "📊 Results Dashboard"

### Batch Processing from S3

1. **Upload documents to S3:**
   ```bash
   aws s3 cp document.pdf s3://doc-anomaly-raw-docs-597088017095/documents/
   ```

2. **Navigate to "📦 Batch Processing (S3)"**
3. **Enter bucket name and folder path**
4. **Click "Process All Documents in S3 Folder"**
5. **Monitor progress** and view batch results

### Human Feedback (HITL)

1. **Process documents** to generate anomalies
2. **Navigate to "👤 Human Feedback"**
3. **Review detected anomalies**
4. **Provide feedback** (Correct/Incorrect/Needs Review)
5. **System automatically updates** from feedback

### Model Training

1. **Collect feedback** through HITL interface
2. **Navigate to "🧠 Training Management"**
3. **Review training data** statistics
4. **Click "Train Model"** when ready
5. **Monitor training progress** and metrics

---

## 🔍 Anomaly Detection

### Detected Anomaly Types

| Anomaly Type | Description | Example |
|-------------|-------------|---------|
| **Date Mismatch** | Invoice date doesn't match contract schedule | Invoice dated 2024-01-15, but contract expects 2024-01-01 |
| **Amount Discrepancy** | Payment amount differs from contract | Invoice shows $1,200, contract specifies $1,000 |
| **Schedule Miss** | Missing scheduled payment | Contract requires monthly payment, but invoice missing |
| **Surplus Payment** | Overpayment detected | Invoice shows $1,500, but contract requires $1,000 |
| **Missed Payment** | Underpayment detected | Invoice shows $800, but contract requires $1,000 |
| **Schedule Misalignment** | Payment date doesn't match schedule | Payment on wrong day of month |

### Business Rules

Configurable thresholds in DynamoDB:
- **Date Variance Tolerance**: 30 days
- **Amount Variance Tolerance**: 5%
- **Schedule Miss Tolerance**: 5 days
- **Surplus Payment Threshold**: 10%
- **Missed Payment Grace Period**: 10 days
- **Lease Payment Variance**: 3%

---

## ☁️ AWS Integration

### S3 Buckets

- **Raw Documents**: `doc-anomaly-raw-docs-597088017095`
- **Processed Documents**: `doc-anomaly-processed-597088017095`
- **Embeddings**: `doc-anomaly-embeddings-597088017095`
- **ML Models**: `doc-anomaly-ml-models-597088017095`

### DynamoDB Tables

- **DocumentMetadata** - Document information and status
- **ContractInvoiceMapping** - Contract-invoice relationships
- **AnomalyResults** - Detected anomalies
- **BusinessRules** - Configurable thresholds
- **HumanFeedback** - HITL feedback data
- **ValidationResults** - Validation outcomes

### CloudWatch Logs

- `/aws/doc-anomaly/orchestrator`
- `/aws/doc-anomaly/ingestion`
- `/aws/doc-anomaly/extraction`
- `/aws/doc-anomaly/contract-invoice`
- `/aws/doc-anomaly/anomaly-detection`
- `/aws/doc-anomaly/validation`

---

## 🚀 Deployment

### Local Development

```bash
streamlit run streamlit_app/app.py
```

### EC2 Deployment

1. **Launch EC2 instance** (Amazon Linux 2023)
2. **Install dependencies:**
   ```bash
   sudo yum install -y python3 python3-pip git
   ```
3. **Copy project to EC2:**
   ```bash
   scp -i key.pem -r "DOC ANOMALY DETECTION SYSTEM" ec2-user@<IP>:~/
   ```
4. **Set up on EC2:**
   ```bash
   cd "DOC ANOMALY DETECTION SYSTEM"
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Run Streamlit:**
   ```bash
   streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
   ```
6. **Configure Security Group** - Open port 8501

See `EC2_DEPLOYMENT_STEPS.md` for detailed instructions.

---

## 📚 Documentation

### Key Documents

- **`ARCHITECTURE.md`** - System architecture overview
- **`FINAL_STATUS.md`** - Implementation status and features
- **`EC2_DEPLOYMENT_STEPS.md`** - EC2 deployment guide
- **`AWS_ACCESS_REQUIREMENTS.md`** - IAM permissions needed
- **`AWS_CREDENTIALS_SETUP.md`** - AWS credential configuration

### Code Structure

```
DOC ANOMALY DETECTION SYSTEM/
├── agents/              # AI agents
│   ├── orchestrator_manager.py
│   ├── document_ingestion_agent.py
│   ├── extraction_agent.py
│   ├── contract_invoice_agent.py
│   ├── validation_agent.py
│   ├── batch_ingestion_agent.py
│   └── ...
├── aws/                 # AWS service handlers
│   ├── s3_handler.py
│   ├── dynamodb_handler.py
│   └── cloudwatch_handler.py
├── config/              # Configuration
│   └── openai_config.py
├── ml_models/           # ML training
│   └── training_agent.py
├── streamlit_app/       # Streamlit interface
│   ├── app.py
│   └── pages/
│       ├── upload_page.py
│       ├── batch_processing_page.py
│       ├── results_page.py
│       ├── feedback_page.py
│       ├── metrics_page.py
│       ├── observability_page.py
│       └── training_page.py
├── sample_data/         # Test documents
├── requirements.txt     # Dependencies
└── setup_aws_infrastructure.py
```

---

## 🧪 Testing

### Sample Documents

Test with provided sample documents:
- `sample_data/invoice_001_normal.pdf` - Normal invoice
- `sample_data/invoice_002_normal.pdf` - Normal invoice
- `sample_data/invoice_003_anomalies.pdf` - Invoice with anomalies
- `sample_data/contract_001_normal.pdf` - Normal contract
- `sample_data/contract_002_normal.pdf` - Normal contract

### Test AWS Access

```bash
python test_aws_access.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check documentation in `/docs` folder
- Review `FINAL_STATUS.md` for current features

---

## 🎉 Acknowledgments

- **OpenAI** - GPT-4o API
- **AWS** - Cloud infrastructure
- **Streamlit** - Web framework
- **XGBoost** - ML framework

---

**Built with ❤️ for Enterprise Document Intelligence**

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** November 2025
