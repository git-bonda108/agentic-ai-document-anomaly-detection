"""
Validation Agent
Validates anomalies against business rules and thresholds
Generates validation summary and recommendations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.enhanced_base_agent import EnhancedBaseAgent

class ValidationAgent(EnhancedBaseAgent):
    """
    Validates detected anomalies against business rules and thresholds
    Generates validation summary with recommendations
    """
    
    def __init__(self):
        super().__init__("ValidationAgent")
        
        # Default thresholds (will be loaded from DynamoDB)
        self.business_rules = {
            "date_variance_days": 30,
            "amount_variance_percent": 5,
            "schedule_miss_tolerance_days": 5,
            "surplus_payment_threshold_percent": 10,
            "missed_payment_grace_days": 10,
            "lease_payment_variance_percent": 3
        }
        
        # Load business rules from DynamoDB
        self._load_business_rules()
    
    def _load_business_rules(self):
        """Load business rules from DynamoDB"""
        if self.dynamodb_handler:
            try:
                rules = self.dynamodb_handler.get_business_rules()
                for rule_id, rule_data in rules.items():
                    if isinstance(rule_data, dict) and "rule_value" in rule_data:
                        self.business_rules[rule_id] = rule_data["rule_value"]
                    else:
                        self.business_rules[rule_id] = rule_data
                self.logger.info(f"Loaded {len(rules)} business rules from DynamoDB")
            except Exception as e:
                self.logger.warning(f"Could not load business rules from DynamoDB: {e}")
    
    def validate(self, anomalies: List[Dict[str, Any]], document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate anomalies against business rules
        
        Args:
            anomalies: List of detected anomalies
            document_data: Document data with extracted fields
            
        Returns:
            Dict containing validation results and summary
        """
        try:
            doc_id = document_data.get("document_id")
            doc_type = document_data.get("document_type", "UNKNOWN")
            
            self.logger.info(f"Validating {len(anomalies)} anomalies for {doc_type} document: {doc_id}")
            
            validated_anomalies = []
            valid_anomalies = []  # Within thresholds
            invalid_anomalies = []  # Exceed thresholds - action required
            recommendations = []
            
            for anomaly in anomalies:
                validation_result = self._validate_single_anomaly(anomaly, document_data)
                validated_anomalies.append({
                    **anomaly,
                    "validation": validation_result
                })
                
                if validation_result["is_valid"]:
                    valid_anomalies.append(validation_result)
                else:
                    invalid_anomalies.append(validation_result)
                    recommendations.extend(validation_result.get("recommendations", []))
            
            # Generate summary
            summary = self._generate_validation_summary(
                validated_anomalies, valid_anomalies, invalid_anomalies, doc_type
            )
            
            # Risk assessment
            risk_level = self._assess_risk(validated_anomalies, invalid_anomalies)
            
            validation_result = {
                "document_id": doc_id,
                "document_type": doc_type,
                "validation_timestamp": datetime.utcnow().isoformat(),
                "total_anomalies": len(anomalies),
                "valid_anomalies": len(valid_anomalies),
                "invalid_anomalies": len(invalid_anomalies),
                "risk_level": risk_level,
                "validated_anomalies": validated_anomalies,
                "summary": summary,
                "recommendations": list(set(recommendations)),  # Remove duplicates
                "validation_status": "COMPLETED"
            }
            
            self.log_action("VALIDATION", doc_id, "SUCCESS",
                          f"Validated {len(anomalies)} anomalies, {len(invalid_anomalies)} require action")
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error validating anomalies: {e}")
            return {"error": f"Validation failed: {str(e)}"}
    
    def _validate_single_anomaly(self, anomaly: Dict[str, Any], document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single anomaly against business rules"""
        anomaly_type = anomaly.get("type", "")
        subtype = anomaly.get("subtype", "")
        severity = anomaly.get("severity", "LOW")
        confidence = anomaly.get("confidence", 0.0)
        
        is_valid = True  # Within acceptable thresholds
        recommendations = []
        threshold_used = None
        
        # Date mismatch validation
        if "DATE_MISMATCH" in anomaly_type:
            variance_days = anomaly.get("variance_days", 999)
            threshold = self.business_rules.get("date_variance_days", 30)
            threshold_used = f"{threshold} days"
            
            if variance_days > threshold:
                is_valid = False
                recommendations.append(f"Review date mismatch: {anomaly.get('description', '')}")
            else:
                is_valid = True
        
        # Amount discrepancy validation
        elif "AMOUNT_DISCREPANCY" in anomaly_type or "SURPLUS_PAYMENT" in anomaly_type or "MISSED_PAYMENT" in anomaly_type:
            variance_percent = anomaly.get("variance_percent") or anomaly.get("surplus_percent") or anomaly.get("shortfall_percent", 0)
            
            if "SURPLUS_PAYMENT" in anomaly_type:
                threshold = self.business_rules.get("surplus_payment_threshold_percent", 10)
                threshold_used = f"{threshold}%"
            elif "LEASE_AMOUNT" in subtype:
                threshold = self.business_rules.get("lease_payment_variance_percent", 3)
                threshold_used = f"{threshold}%"
            else:
                threshold = self.business_rules.get("amount_variance_percent", 5)
                threshold_used = f"{threshold}%"
            
            if variance_percent > threshold:
                is_valid = False
                recommendations.append(f"Amount variance {variance_percent:.1f}% exceeds threshold {threshold}%")
            else:
                is_valid = True
        
        # Schedule miss validation
        elif "SCHEDULE_MISS" in anomaly_type:
            days_late = anomaly.get("days_late", 0)
            threshold = self.business_rules.get("schedule_miss_tolerance_days", 5)
            threshold_used = f"{threshold} days"
            
            if days_late > threshold:
                is_valid = False
                recommendations.append(f"Payment is {days_late} days late - investigate")
            else:
                is_valid = True
        
        # High severity anomalies are always invalid
        elif severity == "HIGH":
            is_valid = False
            recommendations.append(f"High severity anomaly requires immediate review: {anomaly.get('description', '')}")
        
        # Low confidence anomalies need review
        elif confidence < 0.5:
            is_valid = None  # Uncertain
            recommendations.append(f"Low confidence anomaly ({confidence:.1%}) - verify manually")
        
        return {
            "is_valid": is_valid,
            "threshold_used": threshold_used,
            "recommendations": recommendations,
            "validation_notes": f"Anomaly type: {anomaly_type}, Severity: {severity}, Confidence: {confidence:.1%}"
        }
    
    def _generate_validation_summary(self, validated_anomalies: List[Dict], 
                                     valid_anomalies: List[Dict],
                                     invalid_anomalies: List[Dict],
                                     doc_type: str) -> Dict[str, Any]:
        """Generate validation summary"""
        summary = {
            "document_type": doc_type,
            "total_anomalies": len(validated_anomalies),
            "within_thresholds": len(valid_anomalies),
            "exceeds_thresholds": len(invalid_anomalies),
            "anomaly_breakdown": {},
            "severity_distribution": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        }
        
        # Count by type
        for anomaly in validated_anomalies:
            anomaly_type = anomaly.get("type", "UNKNOWN")
            summary["anomaly_breakdown"][anomaly_type] = summary["anomaly_breakdown"].get(anomaly_type, 0) + 1
            
            severity = anomaly.get("severity", "LOW")
            summary["severity_distribution"][severity] = summary["severity_distribution"].get(severity, 0) + 1
        
        return summary
    
    def _assess_risk(self, validated_anomalies: List[Dict], invalid_anomalies: List[Dict]) -> str:
        """Assess overall risk level"""
        if not validated_anomalies:
            return "NONE"
        
        high_severity_count = sum(1 for a in validated_anomalies if a.get("severity") == "HIGH")
        invalid_count = len(invalid_anomalies)
        
        if high_severity_count > 0 or invalid_count > 3:
            return "HIGH"
        elif invalid_count > 0 or high_severity_count == 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method - validates anomalies from document data"""
        anomalies = document_data.get("anomalies", [])
        if isinstance(anomalies, dict):
            anomalies = anomalies.get("details", [])
        
        return self.validate(anomalies, document_data)





