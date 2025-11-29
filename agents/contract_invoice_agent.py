"""
Contract-Invoice Comparison Agent
Specialized agent for detecting anomalies between lease contracts and invoices
Uses GPT-4o for context-aware comparison
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re
from agents.enhanced_base_agent import EnhancedBaseAgent

class ContractInvoiceComparisonAgent(EnhancedBaseAgent):
    """
    Compares lease contracts with invoices to detect:
    - Date mismatches
    - Amount discrepancies
    - Schedule misses (missing payments)
    - Surplus payments (overpayments)
    - Missed payments (underpayments)
    - Schedule misalignment
    """
    
    def __init__(self):
        super().__init__("ContractInvoiceComparisonAgent")
    
    def compare(self, contract_data: Dict[str, Any], invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare contract and invoice to detect anomalies
        
        Args:
            contract_data: Contract document data with extracted fields
            invoice_data: Invoice document data with extracted fields
            
        Returns:
            Dict containing comparison results and detected anomalies
        """
        try:
            contract_id = contract_data.get("contract_id") or contract_data.get("document_id")
            invoice_id = invoice_data.get("document_id")
            
            self.logger.info(f"Comparing contract {contract_id} with invoice {invoice_id}")
            
            # Extract fields
            contract_fields = contract_data.get("extracted_fields", {})
            invoice_fields = invoice_data.get("extracted_fields", {})
            
            # Detect anomalies
            anomalies = []
            
            # 1. Date Mismatches
            date_anomalies = self._detect_date_mismatches(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(date_anomalies)
            
            # 2. Amount Discrepancies
            amount_anomalies = self._detect_amount_discrepancies(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(amount_anomalies)
            
            # 3. Schedule Misses
            schedule_anomalies = self._detect_schedule_misses(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(schedule_anomalies)
            
            # 4. Surplus Payments
            surplus_anomalies = self._detect_surplus_payments(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(surplus_anomalies)
            
            # 5. Missed Payments
            missed_anomalies = self._detect_missed_payments(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(missed_anomalies)
            
            # 6. Schedule Misalignment
            misalignment_anomalies = self._detect_schedule_misalignment(contract_fields, invoice_fields, contract_id, invoice_id)
            anomalies.extend(misalignment_anomalies)
            
            # Use GPT-4o for semantic analysis if available
            if self.openai_config and anomalies:
                semantic_analysis = self._analyze_with_gpt4o(contract_data, invoice_data, anomalies)
                if semantic_analysis:
                    anomalies.extend(semantic_analysis)
            
            # Store comparison in DynamoDB
            if self.dynamodb_handler and contract_id and invoice_id:
                self.store_contract_invoice_mapping(contract_id, invoice_id, {
                    "anomalies_count": len(anomalies),
                    "compared_at": datetime.utcnow().isoformat()
                })
            
            result = {
                "contract_id": contract_id,
                "invoice_id": invoice_id,
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies,
                "comparison_status": "SUCCESS"
            }
            
            self.log_action("CONTRACT_INVOICE_COMPARISON", invoice_id, "SUCCESS",
                          f"Detected {len(anomalies)} anomalies")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error comparing contract and invoice: {e}")
            return {"error": f"Comparison failed: {str(e)}"}
    
    def _detect_date_mismatches(self, contract_fields: Dict, invoice_fields: Dict, 
                                contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect date mismatches between contract and invoice"""
        anomalies = []
        
        contract_effective = self._get_field_value(contract_fields, "effective_date")
        contract_expiration = self._get_field_value(contract_fields, "expiration_date")
        invoice_date = self._get_field_value(invoice_fields, "invoice_date")
        invoice_due = self._get_field_value(invoice_fields, "due_date")
        
        # Check if invoice date is outside contract effective period
        if contract_effective and invoice_date:
            contract_start = self._parse_date(contract_effective)
            invoice_dt = self._parse_date(invoice_date)
            
            if contract_start and invoice_dt:
                if invoice_dt < contract_start:
                    anomalies.append({
                        "type": "DATE_MISMATCH",
                        "subtype": "INVOICE_BEFORE_CONTRACT_START",
                        "severity": "HIGH",
                        "description": f"Invoice date {invoice_date} is before contract effective date {contract_effective}",
                        "confidence": 0.95,
                        "contract_date": contract_effective,
                        "invoice_date": invoice_date
                    })
        
        if contract_expiration and invoice_date:
            contract_end = self._parse_date(contract_expiration)
            invoice_dt = self._parse_date(invoice_date)
            
            if contract_end and invoice_dt:
                if invoice_dt > contract_end:
                    anomalies.append({
                        "type": "DATE_MISMATCH",
                        "subtype": "INVOICE_AFTER_CONTRACT_END",
                        "severity": "HIGH",
                        "description": f"Invoice date {invoice_date} is after contract expiration date {contract_expiration}",
                        "confidence": 0.95,
                        "contract_date": contract_expiration,
                        "invoice_date": invoice_date
                    })
        
        return anomalies
    
    def _detect_amount_discrepancies(self, contract_fields: Dict, invoice_fields: Dict,
                                     contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect amount discrepancies between contract and invoice"""
        anomalies = []
        
        lease_amount = self._get_field_value(contract_fields, "lease_amount")
        invoice_amount = self._get_field_value(invoice_fields, "total_amount")
        
        if lease_amount and invoice_amount:
            lease_val = self._parse_amount(lease_amount)
            invoice_val = self._parse_amount(invoice_amount)
            
            if lease_val and invoice_val:
                variance_percent = abs((invoice_val - lease_val) / lease_val * 100)
                
                # Threshold: 5% variance for lease payments
                threshold = 5.0
                
                if variance_percent > threshold:
                    anomalies.append({
                        "type": "AMOUNT_DISCREPANCY",
                        "subtype": "LEASE_AMOUNT_MISMATCH",
                        "severity": "MEDIUM" if variance_percent < 15 else "HIGH",
                        "description": f"Invoice amount ${invoice_val:,.2f} differs from lease amount ${lease_val:,.2f} by {variance_percent:.1f}%",
                        "confidence": min(1.0, variance_percent / (threshold * 2)),
                        "contract_amount": lease_val,
                        "invoice_amount": invoice_val,
                        "variance_percent": variance_percent
                    })
        
        return anomalies
    
    def _detect_schedule_misses(self, contract_fields: Dict, invoice_fields: Dict,
                                contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect missing payments in schedule"""
        anomalies = []
        
        # This would check if invoice matches expected payment schedule
        # For now, simplified version
        contract_effective = self._get_field_value(contract_fields, "effective_date")
        invoice_date = self._get_field_value(invoice_fields, "invoice_date")
        lease_term = self._get_field_value(contract_fields, "lease_term")
        
        if contract_effective and invoice_date and lease_term:
            contract_start = self._parse_date(contract_effective)
            invoice_dt = self._parse_date(invoice_date)
            
            if contract_start and invoice_dt:
                days_diff = (invoice_dt - contract_start).days
                
                # Expected monthly payments - check if this matches expected payment number
                expected_payment_number = (days_diff // 30) + 1
                
                # If this is a significant gap, flag as schedule miss
                days_since_last_payment = days_diff % 30
                if days_since_last_payment > 40:  # More than 10 days late
                    anomalies.append({
                        "type": "SCHEDULE_MISS",
                        "subtype": "MISSING_PAYMENT",
                        "severity": "HIGH",
                        "description": f"Invoice appears {days_since_last_payment - 30} days late based on expected monthly schedule",
                        "confidence": 0.8,
                        "days_late": days_since_last_payment - 30
                    })
        
        return anomalies
    
    def _detect_surplus_payments(self, contract_fields: Dict, invoice_fields: Dict,
                                 contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect surplus payments (overpayments)"""
        anomalies = []
        
        lease_amount = self._get_field_value(contract_fields, "lease_amount")
        invoice_amount = self._get_field_value(invoice_fields, "total_amount")
        
        if lease_amount and invoice_amount:
            lease_val = self._parse_amount(lease_amount)
            invoice_val = self._parse_amount(invoice_amount)
            
            if lease_val and invoice_val and invoice_val > lease_val:
                surplus = invoice_val - lease_val
                surplus_percent = (surplus / lease_val) * 100
                
                # Threshold: 10% surplus
                if surplus_percent > 10:
                    anomalies.append({
                        "type": "SURPLUS_PAYMENT",
                        "subtype": "OVERPAYMENT",
                        "severity": "MEDIUM" if surplus_percent < 20 else "HIGH",
                        "description": f"Invoice amount ${invoice_val:,.2f} exceeds lease amount ${lease_val:,.2f} by ${surplus:,.2f} ({surplus_percent:.1f}%)",
                        "confidence": 0.9,
                        "surplus_amount": surplus,
                        "surplus_percent": surplus_percent
                    })
        
        return anomalies
    
    def _detect_missed_payments(self, contract_fields: Dict, invoice_fields: Dict,
                                contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect missed payments (underpayments)"""
        anomalies = []
        
        lease_amount = self._get_field_value(contract_fields, "lease_amount")
        invoice_amount = self._get_field_value(invoice_fields, "total_amount")
        
        if lease_amount and invoice_amount:
            lease_val = self._parse_amount(lease_amount)
            invoice_val = self._parse_amount(invoice_amount)
            
            if lease_val and invoice_val and invoice_val < lease_val:
                shortfall = lease_val - invoice_val
                shortfall_percent = (shortfall / lease_val) * 100
                
                # Threshold: 10% shortfall
                if shortfall_percent > 10:
                    anomalies.append({
                        "type": "MISSED_PAYMENT",
                        "subtype": "UNDERPAYMENT",
                        "severity": "HIGH",
                        "description": f"Invoice amount ${invoice_val:,.2f} is less than lease amount ${lease_val:,.2f} by ${shortfall:,.2f} ({shortfall_percent:.1f}%)",
                        "confidence": 0.9,
                        "shortfall_amount": shortfall,
                        "shortfall_percent": shortfall_percent
                    })
        
        return anomalies
    
    def _detect_schedule_misalignment(self, contract_fields: Dict, invoice_fields: Dict,
                                      contract_id: str, invoice_id: str) -> List[Dict[str, Any]]:
        """Detect payment schedule misalignment"""
        anomalies = []
        
        # This would check if invoice payment dates align with contract payment schedule
        # Simplified version for now
        contract_effective = self._get_field_value(contract_fields, "effective_date")
        invoice_date = self._get_field_value(invoice_fields, "invoice_date")
        
        if contract_effective and invoice_date:
            contract_start = self._parse_date(contract_effective)
            invoice_dt = self._parse_date(invoice_date)
            
            if contract_start and invoice_dt:
                # Expected payment dates (monthly on same day)
                expected_day = contract_start.day
                actual_day = invoice_dt.day
                
                if abs(expected_day - actual_day) > 5:  # More than 5 days off
                    anomalies.append({
                        "type": "SCHEDULE_MISALIGNMENT",
                        "subtype": "PAYMENT_DATE_MISMATCH",
                        "severity": "MEDIUM",
                        "description": f"Invoice date {invoice_date} does not align with expected monthly payment schedule (expected around day {expected_day})",
                        "confidence": 0.7,
                        "expected_day": expected_day,
                        "actual_day": actual_day
                    })
        
        return anomalies
    
    def _analyze_with_gpt4o(self, contract_data: Dict, invoice_data: Dict, 
                            detected_anomalies: List[Dict]) -> List[Dict[str, Any]]:
        """Use GPT-4o for semantic analysis of contract-invoice relationship"""
        if not self.openai_config:
            return []
        
        try:
            contract_text = contract_data.get("text_content", "")
            invoice_text = invoice_data.get("text_content", "")
            
            analysis_prompt = f"""Analyze the relationship between this lease contract and invoice.
            Already detected anomalies: {len(detected_anomalies)}
            
            Look for:
            1. Payment schedule mismatches
            2. Amount calculation errors
            3. Date alignment issues
            4. Terms and conditions discrepancies
            5. Additional anomalies not yet detected
            
            Return any additional anomalies found as a JSON list."""
            
            result = self.analyze_with_gpt4o(
                f"Contract: {contract_text[:2000]}\n\nInvoice: {invoice_text[:2000]}",
                analysis_prompt
            )
            
            # Parse GPT-4o response for additional anomalies
            # This is simplified - actual implementation would parse JSON response
            return []
            
        except Exception as e:
            self.logger.error(f"Error in GPT-4o analysis: {e}")
            return []
    
    def _get_field_value(self, fields: Dict[str, Any], field_name: str) -> Optional[str]:
        """Extract field value"""
        if field_name in fields:
            field_data = fields[field_name]
            if isinstance(field_data, tuple):
                return field_data[0]
            elif isinstance(field_data, dict):
                return field_data.get("value")
            else:
                return field_data
        return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y",
            "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _parse_amount(self, amount_str: str) -> Optional[float]:
        """Parse amount string to float"""
        if not amount_str:
            return None
        
        # Remove currency symbols and commas
        cleaned = amount_str.replace("$", "").replace(",", "").strip()
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method required by base class - not used for comparison agent"""
        # This agent is called directly via compare() method
        return {"status": "This agent uses compare() method instead"}





