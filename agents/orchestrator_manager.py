"""
Orchestrator Manager
Coordinates multi-agent workflow, manages context, and handles Human-in-the-Loop
"""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from agents.enhanced_base_agent import EnhancedBaseAgent
from agents.document_ingestion_agent import DocumentIngestionAgent
from agents.extraction_agent import ExtractionAgent
from agents.anomaly_detection_agent import AnomalyDetectionAgent

# We'll create these in Batch 3
# from agents.contract_invoice_agent import ContractInvoiceComparisonAgent
# from agents.validation_agent import ValidationAgent

class OrchestratorManager(EnhancedBaseAgent):
    """
    Orchestrator Manager coordinates all agents and manages:
    - Multi-agent workflow
    - Contract-Invoice context management
    - Human-in-the-Loop queue
    - Agent execution order
    """
    
    def __init__(self):
        super().__init__("OrchestratorManager")
        
        # Initialize agents
        self.ingestion_agent = DocumentIngestionAgent()
        self.extraction_agent = ExtractionAgent()
        self.anomaly_agent = AnomalyDetectionAgent()
        
        # Will be initialized in Batch 3
        self.contract_invoice_agent = None
        self.validation_agent = None
        
        # HITL queue for human review
        self.hitl_queue = []
        
        # Confidence threshold for auto-approval vs HITL
        self.auto_approve_threshold = 0.85  # 85% confidence threshold
        
        # Workflow definition
        self.workflow_steps = [
            ("DOCUMENT_INGESTION", self.ingestion_agent),
            ("DATA_EXTRACTION", self.extraction_agent),
            ("ANOMALY_DETECTION", self.anomaly_agent),
        ]
    
    def process_document(self, document_path: str, document_type: str = None) -> Dict[str, Any]:
        """
        Process a document through the complete workflow
        
        Args:
            document_path: Path to the document file
            document_type: Optional document type hint (INVOICE, CONTRACT)
            
        Returns:
            Dict containing complete processing results
        """
        session_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Starting document processing session: {session_id}")
        self.log_action("WORKFLOW_START", None, "STARTED", f"Session: {session_id}")
        
        try:
            # Initialize processing context
            processing_context = {
                "session_id": session_id,
                "start_time": datetime.now(),
                "document_path": document_path,
                "workflow_status": "STARTED",
                "requires_hitl": False
            }
            
            # Step 1: Document Ingestion
            self.logger.info("Executing: DOCUMENT_INGESTION")
            current_data = self.ingestion_agent.process(document_path)
            
            if "error" in current_data:
                processing_context["workflow_status"] = "FAILED"
                processing_context["error"] = current_data["error"]
                processing_context["failed_step"] = "DOCUMENT_INGESTION"
                return self._format_results(processing_context)
            
            doc_id = current_data.get("document_id")
            doc_type = current_data.get("document_type", "UNKNOWN")
            
            processing_context["document_id"] = doc_id
            processing_context["document_type"] = doc_type
            processing_context["document_ingestion_result"] = current_data
            
            # Store document in S3
            if self.s3_handler:
                s3_key = self.store_document_in_s3(document_path, doc_id)
                if s3_key:
                    current_data["s3_key"] = s3_key
            
            # Store metadata in DynamoDB
            metadata = {
                "document_type": doc_type,
                "file_path": document_path,
                "uploaded_at": datetime.utcnow().isoformat()
            }
            if self.dynamodb_handler:
                self.store_metadata_in_dynamodb(doc_id, metadata)
            
            # Step 2: Data Extraction
            self.logger.info("Executing: DATA_EXTRACTION")
            current_data = self.extraction_agent.process(current_data)
            
            if "error" in current_data:
                processing_context["workflow_status"] = "FAILED"
                processing_context["error"] = current_data["error"]
                processing_context["failed_step"] = "DATA_EXTRACTION"
                return self._format_results(processing_context)
            
            processing_context["data_extraction_result"] = current_data
            extracted_fields = current_data.get("extracted_fields", {})
            
            # Step 3: Context Management (for contracts)
            if doc_type == "CONTRACT":
                self._store_contract_context(doc_id, extracted_fields)
            
            # Step 4: Contract-Invoice Comparison (if invoice)
            if doc_type == "INVOICE" and self.contract_invoice_agent:
                self.logger.info("Executing: CONTRACT_INVOICE_COMPARISON")
                contract_data = self._find_related_contract(doc_id, extracted_fields)
                if contract_data:
                    comparison_result = self.contract_invoice_agent.compare(
                        contract_data, current_data
                    )
                    processing_context["contract_invoice_comparison"] = comparison_result
                    # Merge comparison anomalies with extraction results
                    if "anomalies" in comparison_result:
                        current_data.setdefault("anomalies", []).extend(
                            comparison_result["anomalies"]
                        )
            
            # Step 5: Anomaly Detection
            self.logger.info("Executing: ANOMALY_DETECTION")
            current_data = self.anomaly_agent.process(current_data)
            
            if "error" in current_data:
                processing_context["workflow_status"] = "FAILED"
                processing_context["error"] = current_data["error"]
                processing_context["failed_step"] = "ANOMALY_DETECTION"
                return self._format_results(processing_context)
            
            anomalies = current_data.get("anomalies", [])
            processing_context["anomaly_detection_result"] = current_data
            
            # Store anomalies in DynamoDB
            if self.dynamodb_handler and anomalies:
                for anomaly in anomalies:
                    self.dynamodb_handler.store_anomaly(doc_id, anomaly)
            
            # Step 6: Validation (if validation agent available)
            if self.validation_agent and anomalies:
                self.logger.info("Executing: VALIDATION")
                validation_result = self.validation_agent.validate(
                    anomalies, current_data
                )
                processing_context["validation_result"] = validation_result
                
                # Store validation in DynamoDB
                if self.dynamodb_handler:
                    self.dynamodb_handler.store_validation_result(doc_id, validation_result)
            
            # Step 7: Determine if HITL required
            confidence_scores = [
                a.get("confidence", 0.0) for a in anomalies
            ]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 1.0
            
            if avg_confidence < self.auto_approve_threshold or len(anomalies) > 5:
                processing_context["requires_hitl"] = True
                self._queue_for_hitl(session_id, doc_id, processing_context)
                self.logger.info(f"Document {doc_id} queued for Human-in-the-Loop review")
            
            # Finalize
            processing_context["end_time"] = datetime.now()
            processing_context["processing_duration"] = (
                processing_context["end_time"] - processing_context["start_time"]
            ).total_seconds()
            processing_context["workflow_status"] = "COMPLETED"
            
            self.log_action("WORKFLOW_COMPLETE", doc_id, "SUCCESS", 
                          f"Processed in {processing_context['processing_duration']:.2f}s")
            
            return self._format_results(processing_context)
            
        except Exception as e:
            self.logger.error(f"Fatal error in processing session {session_id}: {e}")
            import traceback
            traceback.print_exc()
            return {
                "session_id": session_id,
                "workflow_status": "FAILED",
                "error": f"Fatal error: {str(e)}",
                "processing_time": 0
            }
    
    def _store_contract_context(self, contract_id: str, extracted_fields: Dict[str, Any]):
        """Store contract context for later invoice comparison"""
        contract_context = {
            "contract_id": contract_id,
            "lease_amount": self._get_field_value(extracted_fields, "lease_amount"),
            "effective_date": self._get_field_value(extracted_fields, "effective_date"),
            "expiration_date": self._get_field_value(extracted_fields, "expiration_date"),
            "lease_term": self._get_field_value(extracted_fields, "lease_term"),
            "payment_schedule": self._extract_payment_schedule(extracted_fields),
            "extracted_at": datetime.utcnow().isoformat()
        }
        
        # Store in memory
        self.store_context(f"contract_{contract_id}", contract_context)
        
        # Store in DynamoDB
        if self.dynamodb_handler:
            self.dynamodb_handler.store_document_metadata(contract_id, {
                "document_type": "CONTRACT",
                "contract_context": contract_context
            })
        
        self.logger.info(f"Stored contract context for {contract_id}")
    
    def _find_related_contract(self, invoice_id: str, extracted_fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find related contract for an invoice"""
        # Try to find contract by PO number or other identifiers
        po_number = self._get_field_value(extracted_fields, "po_number")
        vendor = self._get_field_value(extracted_fields, "vendor_name")
        
        # Search in context store first
        for key, context_data in self.context_store.items():
            if key.startswith("contract_"):
                contract_context = context_data["value"]
                # Simple matching logic - can be enhanced
                if po_number and po_number in str(contract_context):
                    self.logger.info(f"Found related contract via PO: {contract_context['contract_id']}")
                    return contract_context
        
        # Search in DynamoDB
        if self.dynamodb_handler:
            # Query contracts by PO or vendor
            # This is a simplified version - can be enhanced with proper queries
            pass
        
        return None
    
    def _extract_payment_schedule(self, extracted_fields: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract payment schedule from contract fields"""
        # This would parse payment schedule information
        # For now, return empty list
        return []
    
    def _get_field_value(self, fields: Dict[str, Any], field_name: str) -> Optional[str]:
        """Extract field value from extracted_fields dict"""
        if field_name in fields:
            field_data = fields[field_name]
            if isinstance(field_data, tuple):
                return field_data[0]  # Return value, not confidence
            elif isinstance(field_data, dict):
                return field_data.get("value")
            else:
                return field_data
        return None
    
    def _queue_for_hitl(self, session_id: str, document_id: str, processing_context: Dict[str, Any]):
        """Queue document for Human-in-the-Loop review"""
        hitl_item = {
            "session_id": session_id,
            "document_id": document_id,
            "queued_at": datetime.utcnow().isoformat(),
            "processing_context": processing_context,
            "status": "PENDING",
            "priority": "NORMAL"
        }
        
        self.hitl_queue.append(hitl_item)
        self.logger.info(f"Queued {document_id} for HITL (queue size: {len(self.hitl_queue)})")
    
    def get_hitl_queue(self) -> List[Dict[str, Any]]:
        """Get current HITL queue"""
        return self.hitl_queue
    
    def process_hitl_feedback(self, document_id: str, feedback: Dict[str, Any]) -> bool:
        """
        Process human feedback and update system
        
        Args:
            document_id: Document ID
            feedback: Feedback dictionary with:
                - feedback_type: CORRECT, INCORRECT, PARTIAL
                - anomalies_feedback: List of anomaly-specific feedback
                - thresholds_adjustment: Optional threshold adjustments
                
        Returns:
            True if successful
        """
        try:
            # Store feedback in DynamoDB
            if self.dynamodb_handler:
                self.dynamodb_handler.store_human_feedback(document_id, feedback)
            
            # Update HITL queue
            for item in self.hitl_queue:
                if item["document_id"] == document_id:
                    item["status"] = "REVIEWED"
                    item["feedback"] = feedback
                    item["reviewed_at"] = datetime.utcnow().isoformat()
                    break
            
            # If feedback indicates threshold adjustments needed
            if "thresholds_adjustment" in feedback:
                self._update_thresholds(feedback["thresholds_adjustment"])
            
            self.log_action("HITL_FEEDBACK", document_id, "SUCCESS", 
                          f"Feedback type: {feedback.get('feedback_type')}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing HITL feedback: {e}")
            return False
    
    def _update_thresholds(self, adjustments: Dict[str, Any]):
        """Update business thresholds based on feedback"""
        # This would update thresholds in DynamoDB BusinessRules table
        # For now, just log it
        self.logger.info(f"Threshold adjustments requested: {adjustments}")
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method required by base class - delegates to process_document"""
        document_path = document_data.get("document_path") or document_data.get("file_path")
        if not document_path:
            return {"error": "document_path or file_path required"}
        return self.process_document(document_path)
    
    def _format_results(self, processing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Format processing results for output"""
        if processing_context["workflow_status"] == "COMPLETED":
            ingestion = processing_context.get("document_ingestion_result", {})
            extraction = processing_context.get("data_extraction_result", {})
            anomaly = processing_context.get("anomaly_detection_result", {})
            validation = processing_context.get("validation_result", {})
            
            return {
                "session_id": processing_context["session_id"],
                "workflow_status": "COMPLETED",
                "document_info": {
                    "document_id": ingestion.get("document_id"),
                    "document_type": ingestion.get("document_type"),
                    "file_path": processing_context["document_path"]
                },
                "extracted_data": extraction.get("extracted_fields", {}),
                "anomalies": {
                    "count": len(anomaly.get("anomalies", [])),
                    "details": anomaly.get("anomalies", [])
                },
                "validation": validation if validation else None,
                "requires_hitl": processing_context.get("requires_hitl", False),
                "processing_time": processing_context["processing_duration"],
                "timestamp": processing_context["start_time"].isoformat()
            }
        else:
            return {
                "session_id": processing_context["session_id"],
                "workflow_status": processing_context["workflow_status"],
                "error": processing_context.get("error", "Unknown error"),
                "failed_step": processing_context.get("failed_step"),
                "processing_time": processing_context.get("processing_duration", 0),
                "timestamp": processing_context["start_time"].isoformat()
            }

