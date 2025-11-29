# DOC ANOMALY DETECTION SYSTEM - Agentic AI Architecture

## Executive Summary
Based on the provided executive summary, we're building an agentic AI system that processes invoices and contracts to detect anomalies across multiple parameters including PO mismatch, date mismatches, lease schedule discrepancies, and duplicates.

## System Architecture

### Core Agents

1. **Document Ingestion Agent**
   - Handles document upload and routing
   - Supports PDF, DOCX, and image formats
   - Validates document integrity

2. **Extraction Agent**
   - Extracts key fields: Invoice #, PO #, Dates, Amounts, Vendor Info
   - Uses OCR for image-based documents
   - Provides confidence scoring for extracted data

3. **Validation Agent**
   - Cross-validates extracted data against business rules
   - Checks format consistency
   - Validates data completeness

4. **Anomaly Detection Agent**
   - PO Mismatch Detection
   - Date Consistency Validation
   - Lease Schedule Discrepancy Analysis
   - Duplicate Detection

5. **Contract Analysis Agent**
   - Specialized for leasing contracts
   - Extracts lease terms, payment schedules
   - Validates against master data

6. **Quality Review Agent**
   - Final validation and anomaly scoring
   - Risk assessment
   - Recommendation generation

7. **Learning Agent**
   - Improves through feedback
   - Adapts thresholds based on historical data
   - Updates extraction patterns

### Workflow Pipeline
```
UPLOAD → EXTRACT → VALIDATE → DETECT → REVIEW → APPROVE
```

### Technology Stack (Enterprise-Friendly)
- **Core**: Python 3.13
- **Document Processing**: PyPDF2, python-docx, Pillow
- **OCR**: pytesseract
- **ML/AI**: scikit-learn, pandas, numpy
- **Interface**: Simple Flask web app (avoiding Streamlit for HP compatibility)
- **Database**: SQLite (lightweight, no external dependencies)

### Key Features
- Autonomous document processing
- Multi-parameter anomaly detection
- Business rule validation
- Confidence scoring
- Audit trail
- Learning capabilities

### Anomaly Detection Parameters
1. **PO Mismatch**: Invoice PO vs Contract PO
2. **Date Mismatch**: Invoice date vs Expected date ranges
3. **Lease Schedule Discrepancies**: Payment amounts vs Contract terms
4. **Duplicates**: Similar documents or line items
5. **Amount Validation**: Invoice amounts vs PO amounts
6. **Vendor Validation**: Invoice vendor vs Contract vendor

