"""
Enhanced Base Agent Class with OpenAI GPT-4o and AWS Integration
Extends base agent with GPT-4o capabilities and AWS persistence
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
import os
from datetime import datetime

# AWS imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aws.s3_handler import S3Handler
from aws.dynamodb_handler import DynamoDBHandler
from aws.cloudwatch_handler import CloudWatchHandler
from config.openai_config import OpenAIConfig

class EnhancedBaseAgent(ABC):
    """Enhanced base class for all agents with GPT-4o and AWS integration"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = self._setup_logger()
        
        # Initialize AWS services
        try:
            self.s3_handler = S3Handler()
            self.dynamodb_handler = DynamoDBHandler()
            self.cloudwatch_handler = CloudWatchHandler()
        except Exception as e:
            self.logger.warning(f"AWS services not available: {e}")
            self.s3_handler = None
            self.dynamodb_handler = None
            self.cloudwatch_handler = None
        
        # Initialize OpenAI
        try:
            self.openai_config = OpenAIConfig()
            if not self.openai_config.is_configured():
                self.logger.warning("OpenAI API key not configured")
        except Exception as e:
            self.logger.warning(f"OpenAI not available: {e}")
            self.openai_config = None
        
        # Context storage for contract-invoice relationships
        self.context_store = {}
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the agent"""
        logger = logging.getLogger(f"{self.agent_name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # File handler
            file_handler = logging.FileHandler('doc_processing.log', encoding='utf-8')
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def log_action(self, action: str, document_id: str = None, 
                   status: str = "SUCCESS", details: str = "", 
                   confidence_score: float = None):
        """Log agent actions to CloudWatch and local logs"""
        log_message = f"Action: {action}, Document: {document_id}, Status: {status}"
        if details:
            log_message += f", Details: {details}"
        
        self.logger.info(log_message)
        
        # Log to CloudWatch if available
        if self.cloudwatch_handler:
            try:
                self.cloudwatch_handler.log_message(
                    self.agent_name.lower().replace("agent", ""),
                    log_message,
                    status
                )
            except Exception as e:
                self.logger.warning(f"CloudWatch logging failed: {e}")
    
    def store_document_in_s3(self, document_path: str, document_id: str) -> Optional[str]:
        """Upload document to S3"""
        if not self.s3_handler:
            self.logger.warning("S3 handler not available")
            return None
        
        try:
            s3_key = self.s3_handler.upload_document(document_path, document_id, "raw_docs")
            if s3_key:
                self.log_action("S3_UPLOAD", document_id, "SUCCESS", f"Uploaded to S3: {s3_key}")
            return s3_key
        except Exception as e:
            self.logger.error(f"Error uploading to S3: {e}")
            return None
    
    def store_metadata_in_dynamodb(self, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Store document metadata in DynamoDB"""
        if not self.dynamodb_handler:
            self.logger.warning("DynamoDB handler not available")
            return False
        
        try:
            success = self.dynamodb_handler.store_document_metadata(document_id, metadata)
            if success:
                self.log_action("DYNAMODB_STORE", document_id, "SUCCESS", "Metadata stored")
            return success
        except Exception as e:
            self.logger.error(f"Error storing metadata: {e}")
            return False
    
    def extract_with_gpt4o(self, text: str, extraction_prompt: str, 
                           expected_fields: list) -> Dict[str, Any]:
        """Extract structured data using GPT-4o"""
        if not self.openai_config:
            self.logger.warning("OpenAI not configured, falling back to regex")
            return {}
        
        try:
            extracted = self.openai_config.extract_with_gpt4o(
                text, extraction_prompt, expected_fields
            )
            self.log_action("GPT4O_EXTRACTION", None, "SUCCESS", 
                          f"Extracted {len(extracted)} fields")
            return extracted
        except Exception as e:
            self.logger.error(f"Error with GPT-4o extraction: {e}")
            return {}
    
    def analyze_with_gpt4o(self, text: str, analysis_prompt: str) -> Dict[str, Any]:
        """Analyze document using GPT-4o"""
        if not self.openai_config:
            self.logger.warning("OpenAI not configured")
            return {}
        
        try:
            result = self.openai_config.analyze_with_gpt4o(text, analysis_prompt)
            self.log_action("GPT4O_ANALYSIS", None, "SUCCESS")
            return result
        except Exception as e:
            self.logger.error(f"Error with GPT-4o analysis: {e}")
            return {}
    
    def store_context(self, key: str, value: Any):
        """Store context in memory (for contract-invoice relationships)"""
        self.context_store[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logger.info(f"Stored context: {key}")
    
    def get_context(self, key: str) -> Optional[Any]:
        """Retrieve context from memory"""
        if key in self.context_store:
            return self.context_store[key]["value"]
        return None
    
    def store_contract_invoice_mapping(self, contract_id: str, invoice_id: str, 
                                      mapping_data: Dict[str, Any]) -> bool:
        """Store contract-invoice relationship in DynamoDB"""
        if not self.dynamodb_handler:
            return False
        
        try:
            success = self.dynamodb_handler.store_contract_invoice_mapping(
                contract_id, invoice_id, mapping_data
            )
            return success
        except Exception as e:
            self.logger.error(f"Error storing contract-invoice mapping: {e}")
            return False
    
    def get_invoices_for_contract(self, contract_id: str) -> List[Dict[str, Any]]:
        """Get all invoices associated with a contract"""
        if not self.dynamodb_handler:
            return []
        
        try:
            return self.dynamodb_handler.get_invoices_for_contract(contract_id)
        except Exception as e:
            self.logger.error(f"Error retrieving invoices for contract: {e}")
            return []
    
    @abstractmethod
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process document data - to be implemented by each agent"""
        pass





