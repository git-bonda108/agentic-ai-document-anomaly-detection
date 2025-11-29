"""
Document Processing Orchestrator
Coordinates the agentic AI workflow for document processing and anomaly detection
"""

import os
import uuid
from typing import Dict, Any, List
from datetime import datetime
import logging

from agents import DocumentIngestionAgent, ExtractionAgent, AnomalyDetectionAgent

class DocumentProcessingOrchestrator:
    """Orchestrates the document processing workflow using specialized agents"""
    
    def __init__(self):
        self.setup_logging()
        
        # Initialize agents
        self.ingestion_agent = DocumentIngestionAgent()
        self.extraction_agent = ExtractionAgent()
        self.anomaly_agent = AnomalyDetectionAgent()
        
        # Processing workflow
        self.workflow_steps = [
            ("DOCUMENT_INGESTION", self.ingestion_agent),
            ("DATA_EXTRACTION", self.extraction_agent),
            ("ANOMALY_DETECTION", self.anomaly_agent)
        ]
    
    def setup_logging(self):
        """Setup logging for the orchestrator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('doc_processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("Orchestrator")
    
    def process_document(self, document_path: str) -> Dict[str, Any]:
        """
        Process a document through the complete workflow
        
        Args:
            document_path: Path to the document file
            
        Returns:
            Dict containing complete processing results
        """
        session_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Starting document processing session: {session_id}")
        
        try:
            # Initialize processing context
            processing_context = {
                "session_id": session_id,
                "start_time": datetime.now(),
                "document_path": document_path,
                "workflow_status": "STARTED"
            }
            
            # Execute workflow steps
            current_data = None
            for step_name, agent in self.workflow_steps:
                self.logger.info(f"Executing step: {step_name}")
                
                try:
                    if step_name == "DOCUMENT_INGESTION":
                        current_data = agent.process(document_path)
                    else:
                        current_data = agent.process(current_data)
                    
                    if "error" in current_data:
                        processing_context["workflow_status"] = "FAILED"
                        processing_context["error"] = current_data["error"]
                        processing_context["failed_step"] = step_name
                        break
                    
                    processing_context[f"{step_name.lower()}_result"] = current_data
                    
                except Exception as e:
                    self.logger.error(f"Error in step {step_name}: {str(e)}")
                    processing_context["workflow_status"] = "FAILED"
                    processing_context["error"] = str(e)
                    processing_context["failed_step"] = step_name
                    break
            
            # Finalize processing context
            processing_context["end_time"] = datetime.now()
            processing_context["processing_duration"] = (
                processing_context["end_time"] - processing_context["start_time"]
            ).total_seconds()
            
            if processing_context["workflow_status"] != "FAILED":
                processing_context["workflow_status"] = "COMPLETED"
            
            self.logger.info(f"Processing session {session_id} completed with status: {processing_context['workflow_status']}")
            
            return self._format_results(processing_context)
            
        except Exception as e:
            self.logger.error(f"Fatal error in processing session {session_id}: {str(e)}")
            return {
                "session_id": session_id,
                "workflow_status": "FAILED",
                "error": f"Fatal error: {str(e)}",
                "processing_time": 0
            }
    
    def batch_process_documents(self, document_paths: List[str]) -> Dict[str, Any]:
        """
        Process multiple documents in batch
        
        Args:
            document_paths: List of document file paths
            
        Returns:
            Dict containing batch processing results
        """
        batch_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Starting batch processing: {batch_id} with {len(document_paths)} documents")
        
        batch_results = {
            "batch_id": batch_id,
            "total_documents": len(document_paths),
            "processed_documents": 0,
            "failed_documents": 0,
            "start_time": datetime.now(),
            "results": []
        }
        
        for i, doc_path in enumerate(document_paths):
            self.logger.info(f"Processing document {i+1}/{len(document_paths)}: {doc_path}")
            
            try:
                result = self.process_document(doc_path)
                batch_results["results"].append(result)
                
                if result["workflow_status"] == "COMPLETED":
                    batch_results["processed_documents"] += 1
                else:
                    batch_results["failed_documents"] += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing document {doc_path}: {str(e)}")
                batch_results["results"].append({
                    "document_path": doc_path,
                    "workflow_status": "FAILED",
                    "error": str(e)
                })
                batch_results["failed_documents"] += 1
        
        batch_results["end_time"] = datetime.now()
        batch_results["processing_duration"] = (
            batch_results["end_time"] - batch_results["start_time"]
        ).total_seconds()
        
        self.logger.info(f"Batch processing {batch_id} completed: {batch_results['processed_documents']} successful, {batch_results['failed_documents']} failed")
        
        return batch_results
    
    def get_processing_summary(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get summary of processing results
        
        Args:
            session_id: Optional session ID to get specific results
            
        Returns:
            Dict containing processing summary
        """
        # This would query the database for processing summaries
        # For now, return a placeholder
        return {
            "total_documents_processed": 0,
            "successful_processing": 0,
            "failed_processing": 0,
            "total_anomalies_detected": 0,
            "anomaly_types": {},
            "processing_trends": {}
        }
    
    def _format_results(self, processing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Format the processing results for output"""
        if processing_context["workflow_status"] == "COMPLETED":
            # Extract key information from each step
            ingestion_result = processing_context.get("document_ingestion_result", {})
            extraction_result = processing_context.get("data_extraction_result", {})
            anomaly_result = processing_context.get("anomaly_detection_result", {})
            
            return {
                "session_id": processing_context["session_id"],
                "workflow_status": "COMPLETED",
                "document_info": {
                    "document_id": ingestion_result.get("document_id"),
                    "document_type": ingestion_result.get("document_type"),
                    "file_path": processing_context["document_path"]
                },
                "extracted_data": extraction_result.get("extracted_fields", {}),
                "anomalies": {
                    "count": len(anomaly_result.get("anomalies", [])),
                    "details": anomaly_result.get("anomalies", [])
                },
                "processing_time": processing_context["processing_duration"],
                "timestamp": processing_context["start_time"].isoformat()
            }
        else:
            return {
                "session_id": processing_context["session_id"],
                "workflow_status": processing_context["workflow_status"],
                "error": processing_context.get("error", "Unknown error"),
                "failed_step": processing_context.get("failed_step"),
                "processing_time": processing_context["processing_duration"],
                "timestamp": processing_context["start_time"].isoformat()
            }
    
    def validate_document_path(self, document_path: str) -> Dict[str, Any]:
        """Validate if document path exists and is accessible"""
        if not os.path.exists(document_path):
            return {
                "valid": False,
                "error": "Document file does not exist"
            }
        
        if not os.path.isfile(document_path):
            return {
                "valid": False,
                "error": "Path is not a file"
            }
        
        # Check file size
        file_size = os.path.getsize(document_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return {
                "valid": False,
                "error": "File size exceeds 50MB limit"
            }
        
        return {
            "valid": True,
            "file_size": file_size,
            "file_name": os.path.basename(document_path)
        }

