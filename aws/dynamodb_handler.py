"""
AWS DynamoDB Handler
Manages data storage in DynamoDB tables
"""

import boto3
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class DynamoDBHandler:
    """Handles DynamoDB operations"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region = region_name
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        
        # Load table configuration
        try:
            if os.path.exists("aws_config.json"):
                with open("aws_config.json", "r") as f:
                    config = json.load(f)
                    self.tables = config.get("tables", {})
            else:
                # Default table names
                self.tables = {
                    "documents": "DocumentMetadata",
                    "contract_invoice_mapping": "ContractInvoiceMapping",
                    "anomalies": "AnomalyResults",
                    "business_rules": "BusinessRules",
                    "human_feedback": "HumanFeedback",
                    "validation_results": "ValidationResults"
                }
        except Exception as e:
            logger.warning(f"Could not load aws_config.json: {e}")
            self.tables = {
                "documents": "DocumentMetadata",
                "contract_invoice_mapping": "ContractInvoiceMapping",
                "anomalies": "AnomalyResults",
                "business_rules": "BusinessRules",
                "human_feedback": "HumanFeedback",
                "validation_results": "ValidationResults"
            }
    
    def store_document_metadata(self, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Store document metadata"""
        try:
            table = self.dynamodb.Table(self.tables["documents"])
            
            item = {
                "document_id": document_id,
                **metadata,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            logger.info(f"Stored metadata for {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing document metadata: {e}")
            return False
    
    def get_document_metadata(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document metadata"""
        try:
            table = self.dynamodb.Table(self.tables["documents"])
            response = table.get_item(Key={"document_id": document_id})
            
            if "Item" in response:
                return response["Item"]
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document metadata: {e}")
            return None
    
    def store_contract_invoice_mapping(self, contract_id: str, invoice_id: str, mapping_data: Dict[str, Any]) -> bool:
        """Store contract-invoice relationship"""
        try:
            table = self.dynamodb.Table(self.tables["contract_invoice_mapping"])
            
            item = {
                "contract_id": contract_id,
                "invoice_id": invoice_id,
                **mapping_data,
                "mapped_at": datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            logger.info(f"Stored mapping: {contract_id} -> {invoice_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing contract-invoice mapping: {e}")
            return False
    
    def get_invoices_for_contract(self, contract_id: str) -> List[Dict[str, Any]]:
        """Get all invoices for a contract"""
        try:
            table = self.dynamodb.Table(self.tables["contract_invoice_mapping"])
            from boto3.dynamodb.conditions import Key
            response = table.query(
                KeyConditionExpression=Key('contract_id').eq(contract_id)
            )
            
            return response.get("Items", [])
            
        except Exception as e:
            logger.error(f"Error retrieving invoices for contract: {e}")
            return []
    
    def store_anomaly(self, document_id: str, anomaly: Dict[str, Any]) -> bool:
        """Store anomaly result"""
        try:
            table = self.dynamodb.Table(self.tables["anomalies"])
            
            timestamp = datetime.utcnow().isoformat()
            
            # Convert floats to Decimal for DynamoDB
            processed_anomaly = self._convert_floats_to_decimal(anomaly)
            
            item = {
                "document_id": document_id,
                "anomaly_timestamp": timestamp,
                **processed_anomaly,
                "created_at": timestamp
            }
            
            table.put_item(Item=item)
            logger.info(f"Stored anomaly for {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing anomaly: {e}")
            return False
    
    def get_anomalies_for_document(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all anomalies for a document"""
        try:
            table = self.dynamodb.Table(self.tables["anomalies"])
            from boto3.dynamodb.conditions import Key
            response = table.query(
                KeyConditionExpression=Key('document_id').eq(document_id)
            )
            
            return sorted(response.get("Items", []), 
                         key=lambda x: x.get("anomaly_timestamp", ""), 
                         reverse=True)
            
        except Exception as e:
            logger.error(f"Error retrieving anomalies: {e}")
            return []
    
    def get_business_rules(self) -> Dict[str, Any]:
        """Get all business rules"""
        try:
            table = self.dynamodb.Table(self.tables["business_rules"])
            response = table.scan()
            
            rules = {}
            for item in response.get("Items", []):
                rules[item["rule_id"]] = item
            
            return rules
            
        except Exception as e:
            logger.error(f"Error retrieving business rules: {e}")
            return {}
    
    def store_human_feedback(self, document_id: str, feedback: Dict[str, Any]) -> bool:
        """Store human feedback"""
        try:
            table = self.dynamodb.Table(self.tables["human_feedback"])
            
            timestamp = datetime.utcnow().isoformat()
            
            item = {
                "document_id": document_id,
                "feedback_timestamp": timestamp,
                **feedback,
                "created_at": timestamp
            }
            
            table.put_item(Item=item)
            logger.info(f"Stored feedback for {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing feedback: {e}")
            return False
    
    def get_feedback_for_document(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all feedback for a document"""
        try:
            table = self.dynamodb.Table(self.tables["human_feedback"])
            from boto3.dynamodb.conditions import Key
            response = table.query(
                KeyConditionExpression=Key('document_id').eq(document_id)
            )
            
            return sorted(response.get("Items", []), 
                         key=lambda x: x.get("feedback_timestamp", ""), 
                         reverse=True)
            
        except Exception as e:
            logger.error(f"Error retrieving feedback: {e}")
            return []
    
    def store_validation_result(self, document_id: str, validation_result: Dict[str, Any]) -> bool:
        """Store validation result"""
        try:
            table = self.dynamodb.Table(self.tables["validation_results"])
            
            timestamp = datetime.utcnow().isoformat()
            
            item = {
                "document_id": document_id,
                "validation_timestamp": timestamp,
                **validation_result,
                "created_at": timestamp
            }
            
            table.put_item(Item=item)
            logger.info(f"Stored validation result for {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing validation result: {e}")
            return False
    
    def get_validation_results_for_document(self, document_id: str) -> List[Dict[str, Any]]:
        """Get validation results for a document"""
        try:
            table = self.dynamodb.Table(self.tables["validation_results"])
            from boto3.dynamodb.conditions import Key
            response = table.query(
                KeyConditionExpression=Key('document_id').eq(document_id)
            )
            
            return sorted(response.get("Items", []), 
                         key=lambda x: x.get("validation_timestamp", ""), 
                         reverse=True)
            
        except Exception as e:
            logger.error(f"Error retrieving validation results: {e}")
            return []
    
    def _convert_floats_to_decimal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert float values to Decimal for DynamoDB compatibility"""
        result = {}
        for key, value in data.items():
            if isinstance(value, float):
                result[key] = Decimal(str(value))
            elif isinstance(value, dict):
                result[key] = self._convert_floats_to_decimal(value)
            elif isinstance(value, list):
                result[key] = [
                    Decimal(str(v)) if isinstance(v, float) else v 
                    for v in value
                ]
            else:
                result[key] = value
        return result

