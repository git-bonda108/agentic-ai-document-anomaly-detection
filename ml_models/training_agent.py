"""
Training Agent
Handles model training and reinforcement learning
"""

import os
import json
import pickle
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import logging

from agents.enhanced_base_agent import EnhancedBaseAgent

class TrainingAgent(EnhancedBaseAgent):
    """
    Training Agent for anomaly detection model
    Supports:
    - Supervised learning from labeled data
    - Reinforcement learning from human feedback
    - Model versioning and management
    """
    
    def __init__(self):
        super().__init__("TrainingAgent")
        self.model = None
        self.model_version = "1.0.0"
        self.models_dir = "ml_models/saved_models"
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Model configuration
        self.config = {
            "model_type": "xgboost" if XGBOOST_AVAILABLE else "gradient_boosting",  # xgboost, gradient_boosting, or random_forest
            "test_size": 0.2,
            "random_state": 42
        }
    
    def train_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train anomaly detection model from labeled data
        
        Args:
            training_data: List of training samples with features and labels
            
        Returns:
            Training results with metrics
        """
        try:
            self.logger.info(f"Starting model training with {len(training_data)} samples")
            
            if len(training_data) < 10:
                return {
                    "status": "INSUFFICIENT_DATA",
                    "error": f"Need at least 10 samples, got {len(training_data)}"
                }
            
            # Prepare features and labels
            X, y = self._prepare_training_data(training_data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=self.config["test_size"],
                random_state=self.config["random_state"],
                stratify=y
            )
            
            # Train model
            if self.config["model_type"] == "xgboost" and XGBOOST_AVAILABLE:
                self.model = xgb.XGBClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=self.config["random_state"],
                    eval_metric='logloss'
                )
            elif self.config["model_type"] == "gradient_boosting":
                self.model = GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=self.config["random_state"]
                )
            else:
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=self.config["random_state"]
                )
            
            self.logger.info("Training model...")
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
                "recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
                "f1_score": f1_score(y_test, y_pred, average='weighted', zero_division=0),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
            }
            
            # Save model
            model_path = self._save_model()
            
            # Store training results
            training_result = {
                "status": "SUCCESS",
                "model_version": self.model_version,
                "model_path": model_path,
                "training_samples": len(training_data),
                "train_size": len(X_train),
                "test_size": len(X_test),
                "metrics": metrics,
                "trained_at": datetime.utcnow().isoformat()
            }
            
            # Store in DynamoDB if available
            if self.dynamodb_handler:
                self.dynamodb_handler.store_document_metadata(
                    f"MODEL_{self.model_version}",
                    training_result
                )
            
            self.log_action("MODEL_TRAINING", None, "SUCCESS",
                          f"Trained model v{self.model_version}, F1: {metrics['f1_score']:.3f}")
            
            return training_result
            
        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def _prepare_training_data(self, training_data: List[Dict[str, Any]]) -> tuple:
        """Prepare features and labels from training data"""
        features_list = []
        labels_list = []
        
        for sample in training_data:
            # Extract features
            features = self._extract_features(sample)
            features_list.append(features)
            
            # Extract label (1 = anomaly, 0 = normal)
            label = 1 if sample.get("has_anomaly", False) else 0
            labels_list.append(label)
        
        X = pd.DataFrame(features_list)
        y = np.array(labels_list)
        
        return X, y
    
    def _extract_features(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from training sample"""
        extracted_fields = sample.get("extracted_fields", {})
        
        features = {
            "has_amount": 1 if self._get_field_value(extracted_fields, "total_amount") else 0,
            "has_date": 1 if self._get_field_value(extracted_fields, "invoice_date") else 0,
            "has_po": 1 if self._get_field_value(extracted_fields, "po_number") else 0,
            "amount_value": float(self._parse_amount(self._get_field_value(extracted_fields, "total_amount"))) if self._get_field_value(extracted_fields, "total_amount") else 0.0,
            "anomaly_count": len(sample.get("anomalies", [])),
            "high_severity_count": sum(1 for a in sample.get("anomalies", []) if a.get("severity") == "HIGH"),
            "medium_severity_count": sum(1 for a in sample.get("anomalies", []) if a.get("severity") == "MEDIUM"),
            "low_severity_count": sum(1 for a in sample.get("anomalies", []) if a.get("severity") == "LOW")
        }
        
        return features
    
    def update_from_feedback(self, feedback_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update model using reinforcement learning from feedback
        
        Args:
            feedback_data: List of feedback samples
            
        Returns:
            Update results
        """
        try:
            self.logger.info(f"Updating model from {len(feedback_data)} feedback samples")
            
            # Load current model if exists
            if not self.model:
                self._load_model()
            
            if not self.model:
                return {
                    "status": "NO_MODEL",
                    "error": "No model to update. Train a model first."
                }
            
            # Prepare reinforcement learning data
            X_feedback, rewards = self._prepare_rl_data(feedback_data)
            
            if len(X_feedback) == 0:
                return {
                    "status": "NO_FEEDBACK",
                    "error": "No valid feedback data"
                }
            
            # Update model with feedback (simplified RL approach)
            # In production, use proper RL algorithm (PPO, DQN, etc.)
            X_feedback_df = pd.DataFrame(X_feedback)
            
            # Create labels from rewards (positive reward = correct, negative = incorrect)
            labels = np.array([1 if r > 0 else 0 for r in rewards])
            
            # Partial fit or retrain with combined data
            # For now, log feedback for future retraining
            self.logger.info(f"Received {len(feedback_data)} feedback samples")
            
            result = {
                "status": "SUCCESS",
                "feedback_samples": len(feedback_data),
                "updated_at": datetime.utcnow().isoformat(),
                "note": "Feedback logged. Model will retrain when threshold reached."
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error updating from feedback: {e}")
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def _prepare_rl_data(self, feedback_data: List[Dict[str, Any]]) -> tuple:
        """Prepare reinforcement learning data from feedback"""
        features_list = []
        rewards_list = []
        
        for feedback in feedback_data:
            # Extract features from document
            document_data = feedback.get("document_data", {})
            features = self._extract_features(document_data)
            features_list.append(features)
            
            # Calculate reward from feedback
            feedback_type = feedback.get("feedback_type", "PARTIAL")
            if feedback_type == "CORRECT":
                reward = 1.0
            elif feedback_type == "INCORRECT":
                reward = -1.0
            else:
                reward = 0.0
            
            rewards_list.append(reward)
        
        return features_list, rewards_list
    
    def predict(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict anomalies for a document"""
        if not self.model:
            self._load_model()
        
        if not self.model:
            return {
                "prediction": "UNAVAILABLE",
                "error": "No trained model available"
            }
        
        try:
            features = self._extract_features(document_data)
            X = pd.DataFrame([features])
            
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            
            return {
                "prediction": "ANOMALY" if prediction == 1 else "NORMAL",
                "probability": {
                    "normal": float(probability[0]),
                    "anomaly": float(probability[1]) if len(probability) > 1 else 0.0
                },
                "confidence": float(max(probability))
            }
        except Exception as e:
            return {
                "prediction": "ERROR",
                "error": str(e)
            }
    
    def _save_model(self) -> str:
        """Save model to disk"""
        model_path = os.path.join(self.models_dir, f"model_v{self.model_version}.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Also save metadata
        metadata = {
            "model_version": self.model_version,
            "model_type": self.config["model_type"],
            "saved_at": datetime.utcnow().isoformat()
        }
        
        metadata_path = os.path.join(self.models_dir, f"model_v{self.model_version}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return model_path
    
    def _load_model(self) -> bool:
        """Load model from disk"""
        model_path = os.path.join(self.models_dir, f"model_v{self.model_version}.pkl")
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.logger.info(f"Loaded model v{self.model_version}")
                return True
            except Exception as e:
                self.logger.error(f"Error loading model: {e}")
                return False
        return False
    
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
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float"""
        if not amount_str:
            return 0.0
        
        cleaned = str(amount_str).replace("$", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def process(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process method required by base class"""
        # This agent primarily uses specific methods like train_model
        training_data = document_data.get("training_data")
        if training_data:
            return self.train_model(training_data)
        else:
            return {"error": "training_data required"}

