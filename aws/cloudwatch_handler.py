"""
AWS CloudWatch Handler
Manages logging and metrics in CloudWatch
"""

import boto3
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CloudWatchHandler:
    """Handles CloudWatch logging and metrics"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region = region_name
        self.logs_client = boto3.client('logs', region_name=region_name)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)
        
        # Agent log groups
        self.log_groups = {
            "orchestrator": "/aws/doc-anomaly/orchestrator",
            "ingestion": "/aws/doc-anomaly/ingestion",
            "extraction": "/aws/doc-anomaly/extraction",
            "contract-invoice": "/aws/doc-anomaly/contract-invoice",
            "anomaly-detection": "/aws/doc-anomaly/anomaly-detection",
            "validation": "/aws/doc-anomaly/validation"
        }
    
    def log_message(self, agent_name: str, message: str, level: str = "INFO"):
        """
        Log message to CloudWatch
        
        Args:
            agent_name: Name of the agent
            message: Log message
            level: Log level (INFO, WARNING, ERROR)
        """
        try:
            log_group = self.log_groups.get(agent_name.lower(), self.log_groups["orchestrator"])
            
            # Create log stream if needed (using timestamp)
            log_stream = f"{agent_name}-{datetime.utcnow().strftime('%Y%m%d')}"
            
            # Put log event
            timestamp = int(datetime.utcnow().timestamp() * 1000)  # milliseconds
            
            try:
                self.logs_client.create_log_stream(
                    logGroupName=log_group,
                    logStreamName=log_stream
                )
            except self.logs_client.exceptions.ResourceAlreadyExistsException:
                pass  # Stream already exists
            
            self.logs_client.put_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
                logEvents=[{
                    'timestamp': timestamp,
                    'message': f"[{level}] {message}"
                }]
            )
            
        except Exception as e:
            # Fallback to local logging if CloudWatch fails
            logger.warning(f"CloudWatch logging failed: {e}")
            logger.info(f"[{agent_name}] {message}")
    
    def put_metric(self, metric_name: str, value: float, unit: str = "Count", 
                   dimensions: Optional[Dict[str, str]] = None):
        """
        Put custom metric to CloudWatch
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            dimensions: Additional dimensions
        """
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
            
            if dimensions:
                metric_data['Dimensions'] = [
                    {'Name': k, 'Value': v} for k, v in dimensions.items()
                ]
            
            self.cloudwatch.put_metric_data(
                Namespace='DOC_Anomaly_Detection',
                MetricData=[metric_data]
            )
            
        except Exception as e:
            logger.warning(f"Failed to put metric to CloudWatch: {e}")





