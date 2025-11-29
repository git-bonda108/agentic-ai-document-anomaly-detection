"""
Batch Ingestion Agent
Processes multiple documents from S3 folder
Handles batch processing and folder monitoring
"""

import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3
from botocore.exceptions import ClientError

from agents.enhanced_base_agent import EnhancedBaseAgent
from agents.orchestrator_manager import OrchestratorManager

class BatchIngestionAgent(EnhancedBaseAgent):
    """
    Processes documents in batch from S3 folder
    Supports:
    - Batch processing of all documents in S3 folder
    - Folder monitoring for new documents
    - Parallel processing with configurable workers
    """
    
    def __init__(self, max_workers: int = 3):
        super().__init__("BatchIngestionAgent")
        self.max_workers = max_workers
        self.orchestrator = OrchestratorManager()
        
        # Supported document extensions
        self.supported_extensions = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.tiff']
    
    def process_s3_folder(self, bucket_name: str, folder_path: str, 
                          recursive: bool = True) -> Dict[str, Any]:
        """
        Process all documents in S3 folder
        
        Args:
            bucket_name: S3 bucket name
            folder_path: S3 folder path (prefix)
            recursive: Process subfolders recursively
            
        Returns:
            Dict containing batch processing results
        """
        try:
            self.logger.info(f"Starting batch processing from S3: {bucket_name}/{folder_path}")
            
            # List all objects in folder
            s3_objects = self._list_s3_objects(bucket_name, folder_path, recursive)
            
            if not s3_objects:
                return {
                    "status": "NO_DOCUMENTS",
                    "message": f"No documents found in {bucket_name}/{folder_path}",
                    "processed": 0,
                    "failed": 0,
                    "total": 0
                }
            
            # Filter for supported document types
            document_keys = [
                obj for obj in s3_objects
                if any(obj.lower().endswith(ext) for ext in self.supported_extensions)
            ]
            
            total_docs = len(document_keys)
            self.logger.info(f"Found {total_docs} documents to process")
            
            if total_docs == 0:
                return {
                    "status": "NO_SUPPORTED_DOCUMENTS",
                    "message": "No supported document types found",
                    "processed": 0,
                    "failed": 0,
                    "total": 0
                }
            
            # Process documents
            batch_id = f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            results = {
                "batch_id": batch_id,
                "bucket_name": bucket_name,
                "folder_path": folder_path,
                "total_documents": total_docs,
                "processed": 0,
                "failed": 0,
                "start_time": datetime.utcnow().isoformat(),
                "results": []
            }
            
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_key = {
                    executor.submit(self._process_s3_document, bucket_name, key): key
                    for key in document_keys
                }
                
                for future in as_completed(future_to_key):
                    key = future_to_key[future]
                    try:
                        result = future.result()
                        if result.get("status") == "SUCCESS":
                            results["processed"] += 1
                        else:
                            results["failed"] += 1
                        results["results"].append(result)
                    except Exception as e:
                        self.logger.error(f"Error processing {key}: {e}")
                        results["failed"] += 1
                        results["results"].append({
                            "s3_key": key,
                            "status": "ERROR",
                            "error": str(e)
                        })
            
            results["end_time"] = datetime.utcnow().isoformat()
            results["status"] = "COMPLETED"
            
            self.log_action("BATCH_PROCESSING", None, "SUCCESS",
                          f"Processed {results['processed']}/{results['total_documents']} documents")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in batch processing: {e}")
            return {
                "status": "ERROR",
                "error": str(e),
                "processed": 0,
                "failed": 0,
                "total": 0
            }
    
    def _list_s3_objects(self, bucket_name: str, prefix: str, recursive: bool = True) -> List[str]:
        """List all S3 objects with given prefix"""
        try:
            if not self.s3_handler:
                # Fallback: use boto3 directly
                s3_client = boto3.client('s3')
            else:
                s3_client = self.s3_handler.s3_client
            
            objects = []
            paginator = s3_client.get_paginator('list_objects_v2')
            
            page_iterator = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix
            )
            
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        # Skip if folder itself
                        if not key.endswith('/'):
                            if recursive or '/' not in key[len(prefix):]:
                                objects.append(key)
            
            return objects
            
        except Exception as e:
            self.logger.error(f"Error listing S3 objects: {e}")
            return []
    
    def _process_s3_document(self, bucket_name: str, s3_key: str) -> Dict[str, Any]:
        """
        Download and process a single S3 document
        
        Args:
            bucket_name: S3 bucket name
            s3_key: S3 object key
            
        Returns:
            Processing result
        """
        try:
            # Download document to temp file
            temp_dir = "temp_downloads"
            os.makedirs(temp_dir, exist_ok=True)
            
            filename = os.path.basename(s3_key)
            local_path = os.path.join(temp_dir, filename)
            
            # Download from S3
            if self.s3_handler:
                success = self.s3_handler.download_document(s3_key, local_path, "raw_docs")
            else:
                # Fallback: use boto3 directly
                s3_client = boto3.client('s3')
                s3_client.download_file(bucket_name, s3_key, local_path)
                success = True
            
            if not success:
                return {
                    "s3_key": s3_key,
                    "status": "DOWNLOAD_FAILED",
                    "error": "Failed to download from S3"
                }
            
            # Process document
            result = self.orchestrator.process_document(local_path)
            
            # Add S3 metadata
            result["s3_key"] = s3_key
            result["s3_bucket"] = bucket_name
            
            # Clean up temp file
            try:
                os.remove(local_path)
            except:
                pass
            
            if result.get("workflow_status") == "COMPLETED":
                return {
                    "s3_key": s3_key,
                    "status": "SUCCESS",
                    "document_id": result.get("document_info", {}).get("document_id"),
                    "anomalies_count": result.get("anomalies", {}).get("count", 0),
                    "processing_time": result.get("processing_time", 0)
                }
            else:
                return {
                    "s3_key": s3_key,
                    "status": "PROCESSING_FAILED",
                    "error": result.get("error", "Unknown error")
                }
                
        except Exception as e:
            self.logger.error(f"Error processing S3 document {s3_key}: {e}")
            return {
                "s3_key": s3_key,
                "status": "ERROR",
                "error": str(e)
            }
    
    def watch_s3_folder(self, bucket_name: str, folder_path: str, 
                       interval_seconds: int = 60) -> None:
        """
        Continuously monitor S3 folder for new documents
        
        Args:
            bucket_name: S3 bucket name
            folder_path: S3 folder path
            interval_seconds: Check interval in seconds
        """
        processed_keys = set()
        
        self.logger.info(f"Starting S3 folder watcher: {bucket_name}/{folder_path}")
        
        while True:
            try:
                # List objects in folder
                current_objects = set(self._list_s3_objects(bucket_name, folder_path))
                
                # Find new objects
                new_objects = current_objects - processed_keys
                
                if new_objects:
                    self.logger.info(f"Found {len(new_objects)} new documents")
                    
                    # Process new documents
                    for s3_key in new_objects:
                        self.logger.info(f"Processing new document: {s3_key}")
                        result = self._process_s3_document(bucket_name, s3_key)
                        processed_keys.add(s3_key)
                
                # Wait before next check
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                self.logger.info("S3 folder watcher stopped")
                break
            except Exception as e:
                self.logger.error(f"Error in folder watcher: {e}")
                time.sleep(interval_seconds)
    
    def batch_process_documents(self, s3_keys: List[str], bucket_name: str) -> Dict[str, Any]:
        """
        Process a list of S3 documents
        
        Args:
            s3_keys: List of S3 object keys
            bucket_name: S3 bucket name
            
        Returns:
            Batch processing results
        """
        total_docs = len(s3_keys)
        results = {
            "total_documents": total_docs,
            "processed": 0,
            "failed": 0,
            "start_time": datetime.utcnow().isoformat(),
            "results": []
        }
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_key = {
                executor.submit(self._process_s3_document, bucket_name, key): key
                for key in s3_keys
            }
            
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    result = future.result()
                    if result.get("status") == "SUCCESS":
                        results["processed"] += 1
                    else:
                        results["failed"] += 1
                    results["results"].append(result)
                except Exception as e:
                    self.logger.error(f"Error processing {key}: {e}")
                    results["failed"] += 1
        
        results["end_time"] = datetime.utcnow().isoformat()
        return results
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method required by base class"""
        # This agent primarily uses specific methods like process_s3_folder
        bucket_name = document_data.get("bucket_name")
        folder_path = document_data.get("folder_path", "")
        
        if bucket_name and folder_path:
            return self.process_s3_folder(bucket_name, folder_path)
        else:
            return {"error": "bucket_name and folder_path required"}





