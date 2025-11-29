# Document Anomaly Detection System
## ML-Powered Human-in-the-Loop Solution on AWS

---

## Executive Summary

The Document Anomaly Detection System is an enterprise-grade, ML-powered solution designed to automatically detect anomalies between lease contracts and invoices. The system leverages OpenAI GPT-4o for intelligent document processing, XGBoost for machine learning-based anomaly detection, and reinforcement learning with human feedback to continuously improve accuracy. Deployed on AWS infrastructure, it provides real-time observability, scalable batch processing, and a seamless human-in-the-loop workflow for validation and model improvement.

---

## 1. Problem Statement

### 1.1 Business Challenge

Organizations processing large volumes of lease contracts and invoices face significant challenges:

- **Manual Review Overhead**: Manual review of contract-invoice pairs is time-consuming, error-prone, and expensive.
- **Anomaly Detection Complexity**: Identifying discrepancies requires deep domain knowledge and careful cross-referencing of:
  - Date mismatches (payment dates, lease start/end dates)
  - Amount discrepancies (rental fees, total amounts, deposits)
  - Schedule misses (missing payment schedules, duplicate entries)
  - Surplus/missed payments (overpayments, underpayments)
  - Schedule misalignment (payment dates vs. lease terms)
- **Scalability Issues**: Manual processes don't scale with increasing document volume.
- **Inconsistent Detection**: Human reviewers may miss subtle anomalies or apply inconsistent criteria.
- **Lack of Learning**: Manual processes don't learn from past corrections, leading to repeated errors.

### 1.2 Technical Requirements

The solution must:

- Process multiple document formats (PDF, DOCX, images)
- Perform semantic understanding of contract and invoice content
- Cross-reference documents intelligently
- Detect anomalies with high accuracy
- Provide human feedback mechanisms for continuous improvement
- Scale to handle batch processing of large document sets
- Offer real-time observability into system operations
- Integrate seamlessly with AWS infrastructure

---

## 2. Solution Overview

### 2.1 Architecture Approach

The solution employs a **multi-agent, event-driven architecture** with the following design principles:

- **Agentic AI**: Specialized agents handle distinct responsibilities (ingestion, extraction, anomaly detection, validation)
- **Orchestration**: Central orchestrator manages workflow, context, and agent coordination
- **ML-Powered**: XGBoost model learns from labeled data and human feedback
- **Reinforcement Learning**: Human-in-the-loop feedback continuously improves model performance
- **Cloud-Native**: Built on AWS for scalability, reliability, and cost-effectiveness
- **Observable**: Real-time monitoring of agent actions, costs, and performance metrics

### 2.2 Core Capabilities

#### **2.2.1 Intelligent Document Processing**
- Multi-format support (PDF, DOCX, images with OCR)
- Semantic extraction using GPT-4o
- Automatic document classification (contract vs. invoice)
- Metadata extraction (dates, amounts, parties, terms)

#### **2.2.2 Anomaly Detection**
- Contract-invoice comparison
- Detection of:
  - Date mismatches
  - Amount discrepancies
  - Schedule misses
  - Surplus/missed payments
  - Schedule misalignments
- Confidence scoring for each anomaly

#### **2.2.3 Machine Learning & Reinforcement Learning**
- XGBoost classifier for supervised learning
- Training on labeled anomaly data
- Reinforcement learning from human feedback
- Model versioning and retraining pipeline
- Performance metrics (F1, Precision, Recall, Confusion Matrix)

#### **2.2.4 Human-in-the-Loop (HITL)**
- Feedback collection interface
- Per-anomaly feedback (Correct/False Positive/False Negative)
- Correction notes and adjustments
- Automatic model updates from feedback
- HITL queue management

#### **2.2.5 Business Rules Validation**
- Configurable business thresholds
- Rule-based validation of detected anomalies
- Severity assessment
- Validation summaries and recommendations

---

## 3. AWS Workflow

### 3.1 Infrastructure Components

#### **3.1.1 Amazon S3**
- **Purpose**: Document storage
- **Buckets**:
  - `doc-anomaly-raw-docs-{account-id}`: Raw uploaded documents
  - `doc-anomaly-processed-{account-id}`: Processed documents
  - `doc-anomaly-embeddings-{account-id}`: Document embeddings
  - `doc-anomaly-models-{account-id}`: Trained ML models
- **Usage**: Central repository for all document-related data

#### **3.1.2 Amazon DynamoDB**
- **Purpose**: Metadata, feedback, and results storage
- **Tables**:
  - `doc-anomaly-metadata-{account-id}`: Document metadata
  - `doc-anomaly-anomalies-{account-id}`: Detected anomalies
  - `doc-anomaly-feedback-{account-id}`: Human feedback
  - `doc-anomaly-business-rules-{account-id}`: Business rules
  - `doc-anomaly-validation-{account-id}`: Validation results
  - `doc-anomaly-contracts-{account-id}`: Contract-invoice mappings
- **Usage**: Fast, scalable access to structured data

#### **3.1.3 Amazon CloudWatch**
- **Purpose**: Logging and monitoring
- **Log Groups**: Agent-specific log groups for observability
- **Metrics**: Custom metrics for performance, costs, token usage
- **Usage**: Real-time monitoring and troubleshooting

#### **3.1.4 Amazon EC2**
- **Purpose**: Application hosting
- **Instance**: t3.medium or t3.large (recommended)
- **Service**: Streamlit application running on port 8501
- **Usage**: Web interface for users

### 3.2 Document Processing Workflow

```
1. Document Upload
   ↓
2. S3 Storage (raw-docs bucket)
   ↓
3. Document Ingestion Agent
   ├─ Extract text content
   ├─ Classify document type
   └─ Generate document ID
   ↓
4. Extraction Agent (GPT-4o)
   ├─ Semantic extraction
   ├─ Key field identification
   └─ Relationship mapping
   ↓
5. Orchestrator Manager
   ├─ Match contracts with invoices
   ├─ Coordinate agent workflow
   └─ Manage context
   ↓
6. Contract-Invoice Comparison Agent
   ├─ Date comparison
   ├─ Amount comparison
   ├─ Schedule comparison
   └─ Anomaly detection
   ↓
7. ML Model (XGBoost)
   ├─ Anomaly classification
   ├─ Confidence scoring
   └─ Feature importance
   ↓
8. Validation Agent
   ├─ Business rules check
   ├─ Threshold validation
   └─ Severity assessment
   ↓
9. Results Storage
   ├─ DynamoDB (anomalies, metadata)
   ├─ S3 (processed documents)
   └─ CloudWatch (logs, metrics)
   ↓
10. Human Review (HITL)
    ├─ Feedback collection
    ├─ Corrections
    └─ Model updates
```

### 3.3 Batch Processing Workflow

```
1. User selects S3 folder
   ↓
2. Batch Ingestion Agent
   ├─ List all documents in folder
   ├─ Group by type (contracts/invoices)
   └─ Queue for processing
   ↓
3. Process in batches (configurable size)
   ├─ Parallel processing (optional)
   └─ Progress tracking
   ↓
4. Standard processing workflow
   (same as single document)
   ↓
5. Batch results aggregation
   ├─ Summary statistics
   ├─ Anomaly counts
   └─ Export capabilities
```

### 3.4 Training & Reinforcement Learning Workflow

```
1. Collect Labeled Data
   ├─ From HITL feedback
   ├─ Historical anomalies
   └─ Manual labels
   ↓
2. Feature Extraction
   ├─ Anomaly features
   ├─ Document features
   └─ Context features
   ↓
3. Train XGBoost Model
   ├─ Train/test split
   ├─ Hyperparameter tuning
   └─ Model evaluation
   ↓
4. Performance Metrics
   ├─ F1 Score
   ├─ Precision/Recall
   ├─ Confusion Matrix
   └─ Feature Importance
   ↓
5. Model Deployment
   ├─ Version management
   ├─ A/B testing (optional)
   └─ Rollback capability
   ↓
6. Reinforcement Learning
   ├─ Collect new feedback
   ├─ Update model
   └─ Evaluate improvement
```

---

## 4. Tech Stack

### 4.1 Core Technologies

#### **4.1.1 AI/ML Frameworks**
- **OpenAI GPT-4o**: LLM for semantic extraction, document understanding, and intelligent comparison
- **XGBoost**: Gradient boosting classifier for supervised anomaly detection
- **scikit-learn**: Machine learning utilities, evaluation metrics
- **pandas/numpy**: Data manipulation and processing

#### **4.1.2 AWS Services**
- **S3**: Object storage for documents and models
- **DynamoDB**: NoSQL database for metadata and results
- **CloudWatch**: Logging, monitoring, and metrics
- **EC2**: Compute for hosting Streamlit application
- **IAM**: Access control and security

#### **4.1.3 Application Framework**
- **Streamlit**: Web application framework for UI
- **Python 3.9+**: Primary programming language
- **FastAPI/Flask**: RESTful API (optional for future expansion)

#### **4.1.4 Document Processing**
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX processing
- **PIL/Pillow**: Image processing
- **pytesseract**: OCR for image-based documents (optional)

#### **4.1.5 Data & Visualization**
- **Plotly**: Interactive visualizations
- **matplotlib/seaborn**: Static charts and graphs
- **pandas**: Data analysis and manipulation

### 4.2 Development Tools

- **Git**: Version control
- **Virtual Environment**: Python isolation
- **dotenv**: Environment variable management
- **boto3**: AWS SDK for Python

### 4.3 Deployment

- **Systemd**: Service management on EC2
- **Nginx**: Reverse proxy (optional)
- **SSH**: Secure remote access

---

## 5. Individual Functionalities

### 5.1 Document Ingestion Agent

**Purpose**: Handle document upload, validation, and initial processing

**Key Functions**:
- File format validation (PDF, DOCX, images)
- File size checks (max 50MB)
- Text extraction from documents
- Document classification (contract/invoice)
- Document ID generation (hash-based)
- Metadata extraction (file size, upload time, format)

**Output**: Document metadata and raw text content

---

### 5.2 Extraction Agent

**Purpose**: Intelligent extraction of key information using GPT-4o

**Key Functions**:
- Semantic understanding of document content
- Key field extraction:
  - Dates (lease start, end, payment dates)
  - Amounts (rental fees, deposits, totals)
  - Parties (lessor, lessee)
  - Terms (payment frequency, lease duration)
- Relationship identification
- Context preservation

**Technologies**: OpenAI GPT-4o API

**Output**: Structured extracted data with confidence scores

---

### 5.3 Orchestrator Manager

**Purpose**: Central coordination of multi-agent workflow

**Key Functions**:
- Agent coordination and task delegation
- Context management across agents
- Contract-invoice matching logic
- HITL queue management
- Workflow state tracking
- Error handling and retry logic

**Output**: Coordinated workflow results and context

---

### 5.4 Contract-Invoice Comparison Agent

**Purpose**: Specialized anomaly detection between contracts and invoices

**Key Functions**:
- **Date Mismatch Detection**:
  - Payment dates vs. lease terms
  - Invoice dates vs. contract dates
  - Late payment identification
- **Amount Discrepancy Detection**:
  - Rental fee mismatches
  - Deposit amount differences
  - Total amount validation
- **Schedule Miss Detection**:
  - Missing payment schedules
  - Duplicate payment entries
  - Extra payment identification
- **Payment Anomaly Detection**:
  - Surplus payments (overpayments)
  - Missed payments (underpayments)
- **Schedule Alignment Check**:
  - Payment frequency validation
  - Date alignment verification

**Output**: List of detected anomalies with details and confidence scores

---

### 5.5 Validation Agent

**Purpose**: Business rules and threshold validation

**Key Functions**:
- Business threshold checking:
  - Amount thresholds (tolerance levels)
  - Date threshold (grace periods)
  - Schedule threshold (allowed misses)
- Rule-based validation:
  - Lease type-specific rules
  - Company-specific policies
- Severity assessment:
  - Critical anomalies
  - Warning-level anomalies
  - Informational anomalies
- Summary generation:
  - Validation summary
  - Recommendations
  - Action items

**Configuration**: Business rules stored in DynamoDB

**Output**: Validation results with summaries and recommendations

---

### 5.6 Training Agent

**Purpose**: ML model training and reinforcement learning

**Key Functions**:
- **Supervised Learning**:
  - Feature extraction from labeled data
  - XGBoost model training
  - Hyperparameter tuning
  - Model evaluation
- **Reinforcement Learning**:
  - Feedback processing
  - Reward calculation from feedback
  - Model updates from feedback
  - Incremental learning
- **Model Management**:
  - Version control
  - Model persistence (pickle/S3)
  - Performance tracking
  - A/B testing support

**Metrics**:
- Accuracy, Precision, Recall, F1 Score
- Confusion Matrix
- ROC/PR Curves
- Feature Importance

**Output**: Trained model and performance metrics

---

### 5.7 Batch Ingestion Agent

**Purpose**: Process multiple documents from S3 folders

**Key Functions**:
- S3 folder scanning
- Document listing and filtering
- Batch grouping (by type, size)
- Parallel processing support
- Progress tracking
- Error handling per document
- Result aggregation

**Configuration**:
- Batch size (configurable)
- Parallel workers (optional)
- Retry logic

**Output**: Batch processing results and summaries

---

### 5.8 Human-in-the-Loop (HITL) System

**Purpose**: Collect and process human feedback for model improvement

**Key Functions**:
- **Feedback Collection**:
  - Per-anomaly feedback (Correct/False Positive/False Negative)
  - Overall prediction feedback
  - Correction notes
  - Adjustment requests
- **Feedback Processing**:
  - Feedback storage (DynamoDB)
  - Reward calculation
  - Training data preparation
  - Model update triggering
- **HITL Queue Management**:
  - Queue display
  - Priority handling
  - Status tracking

**Integration**: Orchestrator Manager coordinates HITL workflow

**Output**: Feedback records and model update triggers

---

### 5.9 Observability System

**Purpose**: Real-time monitoring and logging

**Key Functions**:
- **Agent Status Monitoring**:
  - Agent health checks
  - Processing status
  - Error rates
- **Cost Tracking**:
  - OpenAI API token usage
  - AWS service costs
  - Per-document costs
- **Performance Metrics**:
  - Processing times
  - Throughput
  - Latency
- **Logging**:
  - Agent actions
  - Decision logs
  - Error logs
  - Debug information

**Technologies**: CloudWatch Logs and Metrics

**Output**: Dashboards and reports

---

### 5.10 Streamlit User Interface

**Purpose**: Web-based user interface for all functionalities

**Pages**:
1. **Upload & Process**: Single document upload and processing
2. **Batch Processing (S3)**: Process entire S3 folders
3. **Results Dashboard**: View all results and anomalies
4. **Human Feedback**: Provide feedback on detected anomalies
5. **Metrics & Analytics**: View ML performance metrics
6. **Observability**: Monitor system status and costs
7. **Training Management**: Train, retrain, and manage models

**Features**:
- Interactive visualizations
- Real-time updates
- Export capabilities
- Responsive design

---

## 6. Machine Learning Approach

### 6.1 Model Architecture

**Primary Model**: XGBoost Classifier
- **Type**: Gradient Boosting Decision Tree
- **Purpose**: Binary and multi-class anomaly classification
- **Features**:
  - Anomaly type features
  - Date difference features
  - Amount difference features
  - Document similarity features
  - Historical pattern features

### 6.2 Training Data

- **Source**: 
  - Human-labeled anomalies (HITL feedback)
  - Historical anomaly data
  - Manually curated datasets
- **Preprocessing**:
  - Feature engineering
  - Normalization
  - Handling missing values

### 6.3 Reinforcement Learning

- **Method**: Feedback-based model updates
- **Reward Signal**: Human feedback (Correct = positive, Incorrect = negative)
- **Update Frequency**: Batch updates after threshold feedback volume
- **Incremental Learning**: Continuous improvement from new feedback

### 6.4 Evaluation Metrics

- **F1 Score**: Harmonic mean of precision and recall
- **Precision**: Ratio of true positives to all positives
- **Recall**: Ratio of true positives to all actual positives
- **Accuracy**: Overall correctness
- **Confusion Matrix**: Detailed classification breakdown

---

## 7. Deployment Architecture

### 7.1 AWS Infrastructure

```
┌─────────────────────────────────────────┐
│           AWS Cloud                      │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │         Amazon EC2                 │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Streamlit Application       │  │  │
│  │  │  - Multi-agent system        │  │  │
│  │  │  - GPT-4o integration        │  │  │
│  │  │  - XGBoost models            │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │         Amazon S3                   │  │
│  │  - Raw documents                   │  │
│  │  - Processed documents             │  │
│  │  - ML models                       │  │
│  │  - Embeddings                      │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │      Amazon DynamoDB                │  │
│  │  - Metadata                        │  │
│  │  - Anomalies                       │  │
│  │  - Feedback                        │  │
│  │  - Business rules                   │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │      Amazon CloudWatch              │  │
│  │  - Logs                            │  │
│  │  - Metrics                         │  │
│  │  - Dashboards                     │  │
│  └────────────────────────────────────┘  │
│                                          │
└─────────────────────────────────────────┘
           │
           │ Internet
           │
┌─────────────────────────────────────────┐
│        User Browser                     │
│  http://<EC2_PUBLIC_IP>:8501          │
└─────────────────────────────────────────┘
```

### 7.2 Security

- **IAM Roles**: Least privilege access
- **Encryption**: S3 encryption at rest, HTTPS in transit
- **Key Management**: Environment variables, AWS Secrets Manager (optional)
- **Network Security**: Security groups with restricted access

---

## 8. Performance & Scalability

### 8.1 Performance Characteristics

- **Single Document Processing**: ~10-30 seconds (depending on document size)
- **Batch Processing**: Configurable batch size, parallel processing support
- **ML Inference**: <1 second per document
- **API Response**: Real-time streaming updates

### 8.2 Scalability

- **Horizontal Scaling**: Multiple EC2 instances (load balancer)
- **Vertical Scaling**: Upgrade EC2 instance type
- **S3**: Virtually unlimited storage
- **DynamoDB**: Auto-scaling based on load
- **Batch Processing**: Handles 1000+ documents per batch

---

## 9. Cost Optimization

### 9.1 Cost Components

- **EC2**: ~$30-60/month (t3.medium/large)
- **S3**: ~$0.023/GB/month storage + transfer costs
- **DynamoDB**: ~$0.25/million reads, $1.25/million writes
- **CloudWatch**: ~$0.50/GB log ingestion
- **OpenAI API**: Pay-per-use, varies by usage

### 9.2 Optimization Strategies

- Use EC2 Spot Instances for development
- S3 lifecycle policies for old documents
- DynamoDB on-demand billing
- CloudWatch log retention policies
- Batch API calls to OpenAI for efficiency

---

## 10. Future Enhancements

### 10.1 Planned Features

- **Multi-language Support**: Process documents in multiple languages
- **Advanced OCR**: Improved image document processing
- **Real-time Processing**: WebSocket-based real-time updates
- **API Integration**: RESTful API for programmatic access
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Predictive analytics and trends
- **Integration**: Connect with accounting systems (QuickBooks, SAP)

### 10.2 Model Improvements

- **Deep Learning**: Neural network models for complex patterns
- **Ensemble Methods**: Combine multiple models
- **Active Learning**: Intelligent data labeling
- **Transfer Learning**: Leverage pre-trained models

---

## Conclusion

The Document Anomaly Detection System provides a comprehensive, scalable, and intelligent solution for detecting anomalies between lease contracts and invoices. By combining OpenAI GPT-4o's semantic understanding with XGBoost's classification power and human-in-the-loop feedback, it delivers high accuracy while continuously improving. Deployed on AWS, it offers enterprise-grade scalability, reliability, and observability.

The system's multi-agent architecture, ML-powered detection, and seamless HITL workflow make it a production-ready solution for organizations processing large volumes of lease documents.

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Contact**: System Administrator  
**Documentation**: See `EC2_DEPLOYMENT_STEPS.md` for deployment instructions





