"""
Extraction Agent
Extracts key fields from documents with confidence scoring
"""

import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from .base_agent import BaseAgent

class ExtractionAgent(BaseAgent):
    """Extracts structured data from document text"""
    
    def __init__(self):
        super().__init__("ExtractionAgent")
        
        # Define extraction patterns
        self.patterns = {
            'invoice_number': [
                r'invoice\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'inv\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'invoice\s*no\.?\s*:?\s*([A-Z0-9\-]+)',
                r'bill\s*#?\s*:?\s*([A-Z0-9\-]+)'
            ],
            'po_number': [
                r'purchase\s*order\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'po\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'po\s*number\s*:?\s*([A-Z0-9\-]+)',
                r'order\s*#?\s*:?\s*([A-Z0-9\-]+)'
            ],
            'date': [
                r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'(\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})',
                r'([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})',
                r'(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})'
            ],
            'amount': [
                r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'total\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'amount\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'due\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            ],
            'vendor': [
                r'from\s*:?\s*([A-Za-z\s&.,]+?)(?:\n|$)',
                r'vendor\s*:?\s*([A-Za-z\s&.,]+?)(?:\n|$)',
                r'bill\s*to\s*:?\s*([A-Za-z\s&.,]+?)(?:\n|$)'
            ],
            'lease_amount': [
                r'lease\s*payment\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'monthly\s*payment\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'rent\s*:?\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            ],
            'lease_term': [
                r'lease\s*term\s*:?\s*(\d+)\s*(?:months?|years?)',
                r'term\s*:?\s*(\d+)\s*(?:months?|years?)',
                r'duration\s*:?\s*(\d+)\s*(?:months?|years?)'
            ]
        }
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data from document
        
        Args:
            document_data: Document data from ingestion agent
            
        Returns:
            Dict containing extracted fields with confidence scores
        """
        try:
            doc_id = document_data.get("document_id")
            text_content = document_data.get("text_content", "")
            doc_type = document_data.get("document_type", "UNKNOWN")
            
            self.logger.info(f"Extracting data from {doc_type} document: {doc_id}")
            
            # Extract fields based on document type
            extracted_fields = {}
            
            if doc_type == "INVOICE":
                extracted_fields = self._extract_invoice_fields(text_content)
            elif doc_type == "CONTRACT":
                extracted_fields = self._extract_contract_fields(text_content)
            elif doc_type == "PURCHASE_ORDER":
                extracted_fields = self._extract_po_fields(text_content)
            else:
                # Generic extraction for unknown types
                extracted_fields = self._extract_generic_fields(text_content)
            
            # Store extracted data
            for field_name, (value, confidence) in extracted_fields.items():
                if value:
                    self.store_extracted_data(doc_id, field_name, value, confidence)
            
            result = {
                "document_id": doc_id,
                "document_type": doc_type,
                "extracted_fields": extracted_fields,
                "extraction_status": "SUCCESS"
            }
            
            self.log_action("DATA_EXTRACTION", doc_id, "SUCCESS", 
                          f"Extracted {len(extracted_fields)} fields", 
                          sum(conf for _, conf in extracted_fields.values() if conf) / len(extracted_fields))
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error extracting data: {str(e)}")
            self.log_action("DATA_EXTRACTION", doc_id, "ERROR", str(e))
            return {"error": f"Extraction failed: {str(e)}"}
    
    def _extract_invoice_fields(self, text: str) -> Dict[str, Tuple[str, float]]:
        """Extract fields specific to invoices"""
        fields = {}
        
        # Invoice number
        invoice_num = self._extract_with_patterns(text, self.patterns['invoice_number'])
        fields['invoice_number'] = invoice_num
        
        # PO number
        po_num = self._extract_with_patterns(text, self.patterns['po_number'])
        fields['po_number'] = po_num
        
        # Invoice date
        invoice_date = self._extract_date_field(text, ['invoice date', 'bill date', 'date'])
        fields['invoice_date'] = invoice_date
        
        # Due date
        due_date = self._extract_date_field(text, ['due date', 'payment due', 'due by'])
        fields['due_date'] = due_date
        
        # Amount
        amount = self._extract_amount_field(text, ['total', 'amount due', 'invoice total'])
        fields['total_amount'] = amount
        
        # Vendor
        vendor = self._extract_with_patterns(text, self.patterns['vendor'])
        fields['vendor_name'] = vendor
        
        return fields
    
    def _extract_contract_fields(self, text: str) -> Dict[str, Tuple[str, float]]:
        """Extract fields specific to contracts"""
        fields = {}
        
        # Contract number
        contract_num = self._extract_with_patterns(text, [
            r'contract\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'agreement\s*#?\s*:?\s*([A-Z0-9\-]+)'
        ])
        fields['contract_number'] = contract_num
        
        # Effective date
        effective_date = self._extract_date_field(text, ['effective date', 'start date', 'commencement'])
        fields['effective_date'] = effective_date
        
        # Expiration date
        expiration_date = self._extract_date_field(text, ['expiration date', 'end date', 'termination'])
        fields['expiration_date'] = expiration_date
        
        # Lease amount
        lease_amount = self._extract_with_patterns(text, self.patterns['lease_amount'])
        fields['lease_amount'] = lease_amount
        
        # Lease term
        lease_term = self._extract_with_patterns(text, self.patterns['lease_term'])
        fields['lease_term'] = lease_term
        
        # Parties
        parties = self._extract_parties(text)
        fields['parties'] = parties
        
        return fields
    
    def _extract_po_fields(self, text: str) -> Dict[str, Tuple[str, float]]:
        """Extract fields specific to purchase orders"""
        fields = {}
        
        # PO number
        po_num = self._extract_with_patterns(text, self.patterns['po_number'])
        fields['po_number'] = po_num
        
        # PO date
        po_date = self._extract_date_field(text, ['order date', 'po date', 'date'])
        fields['po_date'] = po_date
        
        # Amount
        amount = self._extract_amount_field(text, ['total amount', 'order total', 'total'])
        fields['total_amount'] = amount
        
        # Vendor
        vendor = self._extract_with_patterns(text, self.patterns['vendor'])
        fields['vendor_name'] = vendor
        
        return fields
    
    def _extract_generic_fields(self, text: str) -> Dict[str, Tuple[str, float]]:
        """Extract common fields from any document"""
        fields = {}
        
        # Try to find any numbers that could be document numbers
        numbers = re.findall(r'[A-Z]*\d{3,}', text)
        if numbers:
            fields['document_number'] = (numbers[0], 0.7)
        
        # Extract dates
        dates = self._extract_dates(text)
        if dates:
            fields['document_date'] = (dates[0], 0.8)
        
        # Extract amounts
        amounts = self._extract_amounts(text)
        if amounts:
            fields['amount'] = (amounts[0], 0.8)
        
        return fields
    
    def _extract_with_patterns(self, text: str, patterns: List[str]) -> Tuple[str, float]:
        """Extract field using multiple regex patterns"""
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                value = matches[0].strip()
                if value:
                    return (value, 0.9)
        return ("", 0.0)
    
    def _extract_date_field(self, text: str, keywords: List[str]) -> Tuple[str, float]:
        """Extract date field using keywords"""
        text_lower = text.lower()
        
        for keyword in keywords:
            # Find the line containing the keyword
            lines = text.split('\n')
            for line in lines:
                if keyword.lower() in line.lower():
                    dates = re.findall(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})', line)
                    if dates:
                        return (dates[0], 0.9)
        
        # Fallback: find any date in the document
        dates = re.findall(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})', text)
        if dates:
            return (dates[0], 0.6)
        
        return ("", 0.0)
    
    def _extract_amount_field(self, text: str, keywords: List[str]) -> Tuple[str, float]:
        """Extract amount field using keywords"""
        text_lower = text.lower()
        
        for keyword in keywords:
            # Find the line containing the keyword
            lines = text.split('\n')
            for line in lines:
                if keyword.lower() in line.lower():
                    amounts = re.findall(r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                    if amounts:
                        return (amounts[-1], 0.9)  # Take the last (usually total) amount
        
        # Fallback: find the largest amount in the document
        amounts = re.findall(r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        if amounts:
            # Convert to float and find the largest
            numeric_amounts = []
            for amount in amounts:
                try:
                    numeric_amounts.append((amount, float(amount.replace(',', ''))))
                except ValueError:
                    continue
            
            if numeric_amounts:
                largest = max(numeric_amounts, key=lambda x: x[1])
                return (largest[0], 0.7)
        
        return ("", 0.0)
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract all dates from text"""
        date_patterns = [
            r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        
        return dates
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Extract all amounts from text"""
        amounts = re.findall(r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        return amounts
    
    def _extract_parties(self, text: str) -> Tuple[str, float]:
        """Extract parties involved in contract"""
        # Look for "between" or "party" keywords
        party_patterns = [
            r'between\s+([A-Za-z\s&.,]+?)\s+and\s+([A-Za-z\s&.,]+?)(?:\n|$)',
            r'party\s+([A-Za-z\s&.,]+?)(?:\n|$)'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                if isinstance(matches[0], tuple):
                    parties = " and ".join(matches[0])
                else:
                    parties = matches[0]
                return (parties.strip(), 0.8)
        
        return ("", 0.0)

