"""
AWS S3 Handler
Manages document storage and retrieval in S3
"""

import boto3
import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class S3Handler:
    """Handles S3 operations for document storage"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        
        # Load bucket configuration
        try:
            if os.path.exists("aws_config.json"):
                with open("aws_config.json", "r") as f:
                    config = json.load(f)
                    self.buckets = config.get("buckets", {})
            else:
                # Default bucket names
                account_id = os.getenv("AWS_ACCOUNT_ID", "597088017095")
                self.buckets = {
                    "raw_docs": f"doc-anomaly-raw-docs-{account_id}",
                    "processed": f"doc-anomaly-processed-{account_id}",
                    "embeddings": f"doc-anomaly-embeddings-{account_id}",
                    "ml_models": f"doc-anomaly-ml-models-{account_id}"
                }
        except Exception as e:
            logger.warning(f"Could not load aws_config.json: {e}")
            account_id = os.getenv("AWS_ACCOUNT_ID", "597088017095")
            self.buckets = {
                "raw_docs": f"doc-anomaly-raw-docs-{account_id}",
                "processed": f"doc-anomaly-processed-{account_id}",
                "embeddings": f"doc-anomaly-embeddings-{account_id}",
                "ml_models": f"doc-anomaly-ml-models-{account_id}"
            }
    
    def upload_document(self, file_path: str, document_id: str, bucket_type: str = "raw_docs") -> Optional[str]:
        """
        Upload document to S3
        
        Args:
            file_path: Local file path
            document_id: Unique document ID
            bucket_type: Type of bucket (raw_docs, processed, embeddings, ml_models)
            
        Returns:
            S3 object key if successful, None otherwise
        """
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                logger.error(f"Unknown bucket type: {bucket_type}")
                return None
            
            # Create S3 key: documents/{document_id}/{filename}
            file_name = Path(file_path).name
            s3_key = f"documents/{document_id}/{file_name}"
            
            # Upload file
            self.s3_client.upload_file(file_path, bucket_name, s3_key)
            
            # Get object URL
            s3_url = f"s3://{bucket_name}/{s3_key}"
            
            logger.info(f"Uploaded {file_name} to {s3_url}")
            return s3_key
            
        except Exception as e:
            logger.error(f"Error uploading document to S3: {e}")
            return None
    
    def download_document(self, s3_key: str, local_path: str, bucket_type: str = "raw_docs") -> bool:
        """
        Download document from S3
        
        Args:
            s3_key: S3 object key
            local_path: Local file path to save
            bucket_type: Type of bucket
            
        Returns:
            True if successful, False otherwise
        """
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                logger.error(f"Unknown bucket type: {bucket_type}")
                return False
            
            # Ensure local directory exists
            os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else ".", exist_ok=True)
            
            # Download file
            self.s3_client.download_file(bucket_name, s3_key, local_path)
            
            logger.info(f"Downloaded {s3_key} to {local_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading document from S3: {e}")
            return False
    
    def store_embedding(self, document_id: str, embedding: list, metadata: Dict[str, Any] = None) -> bool:
        """
        Store document embedding in S3
        
        Args:
            document_id: Document ID
            embedding: Vector embedding
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        try:
            bucket_name = self.buckets.get("embeddings")
            s3_key = f"embeddings/{document_id}.json"
            
            data = {
                "document_id": document_id,
                "embedding": embedding,
                "metadata": metadata or {}
            }
            
            # Upload as JSON
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json.dumps(data),
                ContentType="application/json"
            )
            
            logger.info(f"Stored embedding for {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")
            return False
    
    def get_embedding(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document embedding from S3"""
        try:
            bucket_name = self.buckets.get("embeddings")
            s3_key = f"embeddings/{document_id}.json"
            
            response = self.s3_client.get_object(Bucket=bucket_name, Key=s3_key)
            data = json.loads(response['Body'].read())
            
            return data
            
        except Exception as e:
            logger.error(f"Error retrieving embedding: {e}")
            return None
    
    def delete_document(self, s3_key: str, bucket_type: str = "raw_docs") -> bool:
        """Delete document from S3"""
        try:
            bucket_name = self.buckets.get(bucket_type)
            self.s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
            logger.info(f"Deleted {s3_key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False





