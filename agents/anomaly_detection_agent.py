"""
Anomaly Detection Agent
Detects anomalies across multiple parameters as specified in requirements
"""

from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
import re
from .base_agent import BaseAgent

class AnomalyDetectionAgent(BaseAgent):
    """Detects anomalies in document data"""
    
    def __init__(self):
        super().__init__("AnomalyDetectionAgent")
        
        # Business thresholds for anomaly detection
        self.thresholds = {
            'date_variance_days': 30,  # Allow 30 days variance
            'amount_variance_percent': 10,  # Allow 10% variance
            'duplicate_similarity_threshold': 0.8,  # 80% similarity for duplicates
            'lease_payment_variance_percent': 5,  # 5% variance for lease payments
            'po_amount_variance_percent': 15  # 15% variance for PO amounts
        }
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in document data
        
        Args:
            document_data: Document data with extracted fields
            
        Returns:
            Dict containing detected anomalies
        """
        try:
            doc_id = document_data.get("document_id")
            doc_type = document_data.get("document_type", "UNKNOWN")
            extracted_fields = document_data.get("extracted_fields", {})
            
            self.logger.info(f"Detecting anomalies in {doc_type} document: {doc_id}")
            
            anomalies = []
            
            if doc_type == "INVOICE":
                anomalies.extend(self._detect_invoice_anomalies(doc_id, extracted_fields))
            elif doc_type == "CONTRACT":
                anomalies.extend(self._detect_contract_anomalies(doc_id, extracted_fields))
            elif doc_type == "PURCHASE_ORDER":
                anomalies.extend(self._detect_po_anomalies(doc_id, extracted_fields))
            
            # Cross-document anomaly detection
            anomalies.extend(self._detect_cross_document_anomalies(doc_id, extracted_fields))
            
            # Duplicate detection
            duplicates = self._detect_duplicates(doc_id, extracted_fields)
            anomalies.extend(duplicates)
            
            # Store anomalies
            for anomaly in anomalies:
                self.store_anomaly(
                    doc_id, 
                    anomaly['type'], 
                    anomaly['severity'], 
                    anomaly['description'], 
                    anomaly['confidence']
                )
            
            result = {
                "document_id": doc_id,
                "document_type": doc_type,
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies,
                "detection_status": "SUCCESS"
            }
            
            self.log_action("ANOMALY_DETECTION", doc_id, "SUCCESS", 
                          f"Detected {len(anomalies)} anomalies", 
                          max([a['confidence'] for a in anomalies]) if anomalies else 0.0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            self.log_action("ANOMALY_DETECTION", doc_id, "ERROR", str(e))
            return {"error": f"Anomaly detection failed: {str(e)}"}
    
    def _detect_invoice_anomalies(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Detect anomalies specific to invoices"""
        anomalies = []
        
        # Extract field values
        invoice_date = self._get_field_value(fields, 'invoice_date')
        due_date = self._get_field_value(fields, 'due_date')
        amount = self._get_field_value(fields, 'total_amount')
        po_number = self._get_field_value(fields, 'po_number')
        
        # 1. Date mismatch detection
        if invoice_date and due_date:
            date_anomaly = self._check_date_anomaly(invoice_date, due_date, "invoice to due date")
            if date_anomaly:
                anomalies.append(date_anomaly)
        
        # 2. Amount validation
        if amount:
            amount_anomaly = self._check_amount_anomaly(amount, "invoice amount")
            if amount_anomaly:
                anomalies.append(amount_anomaly)
        
        # 3. PO mismatch (will be checked against related documents)
        if po_number:
            po_anomaly = self._check_po_format(po_number)
            if po_anomaly:
                anomalies.append(po_anomaly)
        
        # 4. Invoice number validation
        invoice_number = self._get_field_value(fields, 'invoice_number')
        if invoice_number:
            invoice_anomaly = self._check_invoice_number_format(invoice_number)
            if invoice_anomaly:
                anomalies.append(invoice_anomaly)
        
        return anomalies
    
    def _detect_contract_anomalies(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Detect anomalies specific to contracts"""
        anomalies = []
        
        # Extract field values
        effective_date = self._get_field_value(fields, 'effective_date')
        expiration_date = self._get_field_value(fields, 'expiration_date')
        lease_amount = self._get_field_value(fields, 'lease_amount')
        lease_term = self._get_field_value(fields, 'lease_term')
        
        # 1. Lease schedule discrepancies
        if effective_date and expiration_date and lease_term:
            schedule_anomaly = self._check_lease_schedule_anomaly(
                effective_date, expiration_date, lease_term
            )
            if schedule_anomaly:
                anomalies.append(schedule_anomaly)
        
        # 2. Lease amount validation
        if lease_amount:
            amount_anomaly = self._check_lease_amount_anomaly(lease_amount)
            if amount_anomaly:
                anomalies.append(amount_anomaly)
        
        # 3. Contract term validation
        if lease_term:
            term_anomaly = self._check_lease_term_anomaly(lease_term)
            if term_anomaly:
                anomalies.append(term_anomaly)
        
        return anomalies
    
    def _detect_po_anomalies(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Detect anomalies specific to purchase orders"""
        anomalies = []
        
        # Extract field values
        po_number = self._get_field_value(fields, 'po_number')
        po_date = self._get_field_value(fields, 'po_date')
        amount = self._get_field_value(fields, 'total_amount')
        
        # 1. PO format validation
        if po_number:
            po_anomaly = self._check_po_format(po_number)
            if po_anomaly:
                anomalies.append(po_anomaly)
        
        # 2. PO date validation
        if po_date:
            date_anomaly = self._check_po_date_anomaly(po_date)
            if date_anomaly:
                anomalies.append(date_anomaly)
        
        # 3. PO amount validation
        if amount:
            amount_anomaly = self._check_amount_anomaly(amount, "PO amount")
            if amount_anomaly:
                anomalies.append(amount_anomaly)
        
        return anomalies
    
    def _detect_cross_document_anomalies(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Detect anomalies by comparing across related documents"""
        anomalies = []
        
        # Get related documents from database
        related_docs = self._get_related_documents(doc_id, fields)
        
        for related_doc in related_docs:
            # PO mismatch detection
            po_anomaly = self._check_po_mismatch(doc_id, fields, related_doc)
            if po_anomaly:
                anomalies.append(po_anomaly)
            
            # Amount mismatch detection
            amount_anomaly = self._check_amount_mismatch(doc_id, fields, related_doc)
            if amount_anomaly:
                anomalies.append(amount_anomaly)
            
            # Date mismatch detection
            date_anomaly = self._check_date_mismatch(doc_id, fields, related_doc)
            if date_anomaly:
                anomalies.append(date_anomaly)
        
        return anomalies
    
    def _detect_duplicates(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Detect duplicate or similar documents"""
        anomalies = []
        
        # Get all documents from database
        all_docs = self._get_all_documents()
        
        for other_doc in all_docs:
            if other_doc['document_id'] == doc_id:
                continue
            
            similarity = self._calculate_document_similarity(fields, other_doc['fields'])
            
            if similarity > self.thresholds['duplicate_similarity_threshold']:
                anomalies.append({
                    'type': 'DUPLICATE_DOCUMENT',
                    'severity': 'HIGH',
                    'description': f"Document is {similarity:.1%} similar to document {other_doc['document_id']}",
                    'confidence': similarity
                })
        
        return anomalies
    
    def _check_date_anomaly(self, date1: str, date2: str, context: str) -> Optional[Dict[str, Any]]:
        """Check for date anomalies"""
        try:
            d1 = self._parse_date(date1)
            d2 = self._parse_date(date2)
            
            if d1 and d2:
                diff_days = abs((d2 - d1).days)
                
                if diff_days > self.thresholds['date_variance_days']:
                    return {
                        'type': 'DATE_MISMATCH',
                        'severity': 'MEDIUM',
                        'description': f"{context} variance is {diff_days} days, exceeds threshold of {self.thresholds['date_variance_days']} days",
                        'confidence': min(1.0, diff_days / (self.thresholds['date_variance_days'] * 2))
                    }
        except Exception:
            pass
        
        return None
    
    def _check_amount_anomaly(self, amount: str, context: str) -> Optional[Dict[str, Any]]:
        """Check for amount anomalies"""
        try:
            numeric_amount = float(amount.replace(',', '').replace('$', ''))
            
            # Check for unrealistic amounts
            if numeric_amount <= 0:
                return {
                    'type': 'INVALID_AMOUNT',
                    'severity': 'HIGH',
                    'description': f"{context} is {amount}, which is invalid (zero or negative)",
                    'confidence': 1.0
                }
            
            # Check for extremely large amounts (potential data entry error)
            if numeric_amount > 10000000:  # 10 million
                return {
                    'type': 'UNUSUAL_AMOUNT',
                    'severity': 'MEDIUM',
                    'description': f"{context} is {amount}, which is unusually large",
                    'confidence': 0.7
                }
        except ValueError:
            return {
                'type': 'INVALID_AMOUNT_FORMAT',
                'severity': 'HIGH',
                'description': f"{context} format is invalid: {amount}",
                'confidence': 1.0
            }
        
        return None
    
    def _check_po_format(self, po_number: str) -> Optional[Dict[str, Any]]:
        """Check PO number format"""
        # Standard PO format validation
        if not re.match(r'^[A-Z]{2,4}\d{4,8}$', po_number):
            return {
                'type': 'PO_FORMAT_ANOMALY',
                'severity': 'MEDIUM',
                'description': f"PO number format is non-standard: {po_number}",
                'confidence': 0.8
            }
        
        return None
    
    def _check_lease_schedule_anomaly(self, start_date: str, end_date: str, term: str) -> Optional[Dict[str, Any]]:
        """Check lease schedule consistency"""
        try:
            start = self._parse_date(start_date)
            end = self._parse_date(end_date)
            term_months = int(re.findall(r'\d+', term)[0])
            
            if start and end:
                calculated_months = (end.year - start.year) * 12 + (end.month - start.month)
                
                if abs(calculated_months - term_months) > 2:  # Allow 2 month variance
                    return {
                        'type': 'LEASE_SCHEDULE_DISCREPANCY',
                        'severity': 'HIGH',
                        'description': f"Lease term mismatch: calculated {calculated_months} months vs stated {term_months} months",
                        'confidence': 0.9
                    }
        except Exception:
            pass
        
        return None
    
    def _check_po_mismatch(self, doc_id: str, fields: Dict[str, Tuple[str, float]], related_doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check PO number mismatch between documents"""
        current_po = self._get_field_value(fields, 'po_number')
        related_po = self._get_field_value(related_doc['fields'], 'po_number')
        
        if current_po and related_po and current_po != related_po:
            return {
                'type': 'PO_MISMATCH',
                'severity': 'HIGH',
                'description': f"PO mismatch: current document has {current_po}, related document has {related_po}",
                'confidence': 0.9
            }
        
        return None
    
    def _check_amount_mismatch(self, doc_id: str, fields: Dict[str, Tuple[str, float]], related_doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check amount mismatch between documents"""
        current_amount = self._get_field_value(fields, 'total_amount')
        related_amount = self._get_field_value(related_doc['fields'], 'total_amount')
        
        if current_amount and related_amount:
            try:
                curr_val = float(current_amount.replace(',', '').replace('$', ''))
                rel_val = float(related_amount.replace(',', '').replace('$', ''))
                
                variance = abs(curr_val - rel_val) / rel_val * 100
                
                if variance > self.thresholds['amount_variance_percent']:
                    return {
                        'type': 'AMOUNT_MISMATCH',
                        'severity': 'HIGH',
                        'description': f"Amount variance: {variance:.1f}% between documents ({current_amount} vs {related_amount})",
                        'confidence': min(1.0, variance / 20)  # Normalize to 0-1
                    }
            except ValueError:
                pass
        
        return None
    
    def _check_date_mismatch(self, doc_id: str, fields: Dict[str, Tuple[str, float]], related_doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check date mismatch between documents"""
        current_date = self._get_field_value(fields, 'invoice_date') or self._get_field_value(fields, 'effective_date')
        related_date = self._get_field_value(related_doc['fields'], 'invoice_date') or self._get_field_value(related_doc['fields'], 'effective_date')
        
        if current_date and related_date:
            return self._check_date_anomaly(current_date, related_date, "cross-document date")
        
        return None
    
    def _get_field_value(self, fields: Dict[str, Tuple[str, float]], field_name: str) -> Optional[str]:
        """Get field value from extracted fields"""
        if field_name in fields:
            value, confidence = fields[field_name]
            return value if confidence > 0.5 else None
        return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        try:
            # Try different date formats
            formats = [
                '%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d',
                '%d/%m/%Y', '%d-%m-%Y',
                '%B %d, %Y', '%b %d, %Y',
                '%d %B %Y', '%d %b %Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Try to extract date from string with regex
            date_match = re.search(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})', date_str)
            if date_match:
                date_part = date_match.group(1)
                for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(date_part, fmt)
                    except ValueError:
                        continue
        
        except Exception:
            pass
        
        return None
    
    def _get_related_documents(self, doc_id: str, fields: Dict[str, Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Get related documents based on common fields like PO number"""
        # This would query the database for related documents
        # For now, return empty list - would be implemented with actual database queries
        return []
    
    def _get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from database for duplicate detection"""
        # This would query the database for all documents
        # For now, return empty list - would be implemented with actual database queries
        return []
    
    def _calculate_document_similarity(self, fields1: Dict[str, Tuple[str, float]], fields2: Dict[str, Tuple[str, float]]) -> float:
        """Calculate similarity between two documents"""
        # Simple similarity calculation based on field matches
        common_fields = set(fields1.keys()) & set(fields2.keys())
        
        if not common_fields:
            return 0.0
        
        matches = 0
        for field in common_fields:
            val1, _ = fields1[field]
            val2, _ = fields2[field]
            if val1 == val2:
                matches += 1
        
        return matches / len(common_fields)
    
    def _check_invoice_number_format(self, invoice_number: str) -> Optional[Dict[str, Any]]:
        """Check invoice number format"""
        if not re.match(r'^[A-Z0-9\-]{3,15}$', invoice_number):
            return {
                'type': 'INVOICE_FORMAT_ANOMALY',
                'severity': 'LOW',
                'description': f"Invoice number format is unusual: {invoice_number}",
                'confidence': 0.6
            }
        return None
    
    def _check_lease_amount_anomaly(self, lease_amount: str) -> Optional[Dict[str, Any]]:
        """Check lease amount for anomalies"""
        return self._check_amount_anomaly(lease_amount, "lease amount")
    
    def _check_lease_term_anomaly(self, lease_term: str) -> Optional[Dict[str, Any]]:
        """Check lease term for anomalies"""
        try:
            term_match = re.search(r'(\d+)', lease_term)
            if term_match:
                months = int(term_match.group(1))
                
                # Check for unrealistic lease terms
                if months < 1 or months > 600:  # 1 month to 50 years
                    return {
                        'type': 'UNUSUAL_LEASE_TERM',
                        'severity': 'MEDIUM',
                        'description': f"Lease term is unusual: {lease_term}",
                        'confidence': 0.8
                    }
        except Exception:
            pass
        
        return None
    
    def _check_po_date_anomaly(self, po_date: str) -> Optional[Dict[str, Any]]:
        """Check PO date for anomalies"""
        try:
            date_obj = self._parse_date(po_date)
            if date_obj:
                # Check if PO date is in the future
                if date_obj > datetime.now():
                    return {
                        'type': 'FUTURE_PO_DATE',
                        'severity': 'MEDIUM',
                        'description': f"PO date is in the future: {po_date}",
                        'confidence': 0.9
                    }
                
                # Check if PO date is too old (more than 2 years)
                if date_obj < datetime.now() - timedelta(days=730):
                    return {
                        'type': 'OLD_PO_DATE',
                        'severity': 'LOW',
                        'description': f"PO date is very old: {po_date}",
                        'confidence': 0.6
                    }
        except Exception:
            pass
        
        return None

