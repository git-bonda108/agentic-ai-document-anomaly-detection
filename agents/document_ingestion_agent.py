"""
Document Ingestion Agent
Handles document upload, routing, and initial processing
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import PyPDF2
import docx
from PIL import Image

# Make pytesseract optional
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    pytesseract = None

from .base_agent import BaseAgent

class DocumentIngestionAgent(BaseAgent):
    """Handles document ingestion and initial processing"""
    
    def __init__(self):
        super().__init__("DocumentIngestionAgent")
        self.supported_formats = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.tiff']
    
    def process(self, document_path: str) -> Dict[str, Any]:
        """
        Process uploaded document and extract basic information
        
        Args:
            document_path: Path to the document file
            
        Returns:
            Dict containing document metadata and extracted text
        """
        try:
            self.logger.info(f"Processing document: {document_path}")
            
            # Validate file
            if not self._validate_document(document_path):
                return {"error": "Invalid document format or corrupted file"}
            
            # Generate document ID
            doc_id = self._generate_document_id(document_path)
            
            # Extract text content
            text_content = self._extract_text(document_path)
            
            # Extract metadata
            metadata = self._extract_metadata(document_path)
            
            # Determine document type
            doc_type = self._classify_document(text_content, metadata)
            
            result = {
                "document_id": doc_id,
                "document_type": doc_type,
                "file_path": document_path,
                "text_content": text_content,
                "metadata": metadata,
                "processing_status": "SUCCESS"
            }
            
            self.log_action("DOCUMENT_INGESTION", doc_id, "SUCCESS", 
                          f"Processed {doc_type} document", 1.0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing document {document_path}: {str(e)}")
            self.log_action("DOCUMENT_INGESTION", "UNKNOWN", "ERROR", str(e))
            return {"error": f"Processing failed: {str(e)}"}
    
    def _validate_document(self, document_path: str) -> bool:
        """Validate document format and integrity"""
        try:
            if not os.path.exists(document_path):
                return False
            
            file_extension = Path(document_path).suffix.lower()
            if file_extension not in self.supported_formats:
                return False
            
            # Check file size (max 50MB)
            file_size = os.path.getsize(document_path)
            if file_size > 50 * 1024 * 1024:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _generate_document_id(self, document_path: str) -> str:
        """Generate unique document ID based on file content hash"""
        try:
            with open(document_path, 'rb') as f:
                file_content = f.read()
                file_hash = hashlib.md5(file_content).hexdigest()
                return f"DOC_{file_hash[:12]}"
        except Exception:
            return f"DOC_{hash(document_path) % 1000000:06d}"
    
    def _extract_text(self, document_path: str) -> str:
        """Extract text content from document"""
        file_extension = Path(document_path).suffix.lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_pdf_text(document_path)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_docx_text(document_path)
            elif file_extension in ['.jpg', '.jpeg', '.png', '.tiff']:
                return self._extract_image_text(document_path)
            else:
                return ""
        except Exception as e:
            self.logger.error(f"Error extracting text from {document_path}: {str(e)}")
            return ""
    
    def _extract_pdf_text(self, document_path: str) -> str:
        """Extract text from PDF document"""
        text = ""
        try:
            with open(document_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            self.logger.error(f"Error extracting PDF text: {str(e)}")
        return text.strip()
    
    def _extract_docx_text(self, document_path: str) -> str:
        """Extract text from DOCX document"""
        try:
            doc = docx.Document(document_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def _extract_image_text(self, document_path: str) -> str:
        """Extract text from image using OCR"""
        if not TESSERACT_AVAILABLE:
            self.logger.warning("Tesseract OCR not available. Image text extraction disabled.")
            return ""
        
        try:
            image = Image.open(document_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting image text: {str(e)}")
            return ""
    
    def _extract_metadata(self, document_path: str) -> Dict[str, Any]:
        """Extract document metadata"""
        try:
            stat = os.stat(document_path)
            return {
                "file_name": Path(document_path).name,
                "file_size": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime,
                "file_extension": Path(document_path).suffix.lower()
            }
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {str(e)}")
            return {}
    
    def _classify_document(self, text_content: str, metadata: Dict[str, Any]) -> str:
        """Classify document type based on content and filename"""
        text_lower = text_content.lower()
        filename_lower = metadata.get("file_name", "").lower()
        
        # Invoice indicators
        invoice_keywords = ['invoice', 'bill', 'payment due', 'amount due', 'total amount']
        if any(keyword in text_lower or keyword in filename_lower for keyword in invoice_keywords):
            return "INVOICE"
        
        # Contract indicators
        contract_keywords = ['contract', 'agreement', 'lease', 'terms and conditions', 'party']
        if any(keyword in text_lower or keyword in filename_lower for keyword in contract_keywords):
            return "CONTRACT"
        
        # Purchase Order indicators
        po_keywords = ['purchase order', 'po number', 'po#', 'order number']
        if any(keyword in text_lower or keyword in filename_lower for keyword in po_keywords):
            return "PURCHASE_ORDER"
        
        # Receipt indicators
        receipt_keywords = ['receipt', 'payment received', 'thank you for payment']
        if any(keyword in text_lower or keyword in filename_lower for keyword in receipt_keywords):
            return "RECEIPT"
        
        return "UNKNOWN"

