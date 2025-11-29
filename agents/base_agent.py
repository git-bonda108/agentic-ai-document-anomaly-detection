"""
Base Agent Class for DOC Anomaly Detection System
Provides common functionality for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime
import sqlite3
from pathlib import Path

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_name: str, db_path: str = "doc_anomaly.db"):
        self.agent_name = agent_name
        self.db_path = db_path
        self.logger = self._setup_logger()
        self._init_database()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the agent"""
        logger = logging.getLogger(f"{self.agent_name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _init_database(self):
        """Initialize SQLite database for agent data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create agent logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                document_id TEXT,
                status TEXT,
                details TEXT,
                confidence_score REAL
            )
        ''')
        
        # Create extracted data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                field_name TEXT NOT NULL,
                field_value TEXT,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create anomaly results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomaly_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                anomaly_type TEXT NOT NULL,
                severity TEXT,
                description TEXT,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @abstractmethod
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process document data - to be implemented by each agent"""
        pass
    
    def log_action(self, action: str, document_id: str = None, 
                   status: str = "SUCCESS", details: str = "", 
                   confidence_score: float = None):
        """Log agent actions to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO agent_logs 
            (agent_name, action, document_id, status, details, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.agent_name, action, document_id, status, details, confidence_score))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Action: {action}, Document: {document_id}, Status: {status}")
    
    def store_extracted_data(self, document_id: str, field_name: str, 
                           field_value: str, confidence_score: float):
        """Store extracted data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO extracted_data 
            (document_id, agent_name, field_name, field_value, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (document_id, self.agent_name, field_name, field_value, confidence_score))
        
        conn.commit()
        conn.close()
    
    def store_anomaly(self, document_id: str, anomaly_type: str, 
                     severity: str, description: str, confidence_score: float):
        """Store anomaly detection results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO anomaly_results 
            (document_id, agent_name, anomaly_type, severity, description, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (document_id, self.agent_name, anomaly_type, severity, description, confidence_score))
        
        conn.commit()
        conn.close()
        
        self.logger.warning(f"Anomaly detected: {anomaly_type} - {description}")
    
    def get_document_data(self, document_id: str) -> Dict[str, Any]:
        """Retrieve all extracted data for a document"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT field_name, field_value, confidence_score, agent_name
            FROM extracted_data 
            WHERE document_id = ?
            ORDER BY timestamp DESC
        ''', (document_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        data = {}
        for row in results:
            field_name, field_value, confidence, agent = row
            if field_name not in data or confidence > data[field_name].get('confidence', 0):
                data[field_name] = {
                    'value': field_value,
                    'confidence': confidence,
                    'extracted_by': agent
                }
        
        return data
    
    def get_anomalies(self, document_id: str) -> List[Dict[str, Any]]:
        """Retrieve all anomalies for a document"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT anomaly_type, severity, description, confidence_score, agent_name, timestamp
            FROM anomaly_results 
            WHERE document_id = ?
            ORDER BY timestamp DESC
        ''', (document_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        anomalies = []
        for row in results:
            anomalies.append({
                'type': row[0],
                'severity': row[1],
                'description': row[2],
                'confidence': row[3],
                'detected_by': row[4],
                'timestamp': row[5]
            })
        
        return anomalies

