"""
Training Management Page
Manages model training, retraining, and versioning
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_training_page():
    """Render training management page"""
    
    st.markdown('<h1 class="main-header">🧠 Training Management</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Current Model Status
    st.markdown("### 📊 Current Model Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Version", "v1.0.0")
        st.metric("Training Date", "2024-01-10")
    with col2:
        st.metric("F1 Score", "0.85")
        st.metric("Precision", "0.82")
    with col3:
        st.metric("Recall", "0.88")
        st.metric("Accuracy", "0.91")
    
    st.markdown("---")
    
    # Training Data Statistics
    st.markdown("### 📚 Training Data Statistics")
    
    training_stats = {
        "Total Samples": 500,
        "Training Set": 350,
        "Validation Set": 75,
        "Test Set": 75,
        "Anomalies Labeled": 245,
        "Normal Samples": 255,
        "Human Feedback Samples": 47
    }
    
    df_stats = pd.DataFrame({
        "Metric": list(training_stats.keys()),
        "Value": list(training_stats.values())
    })
    
    st.dataframe(df_stats, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Retraining Section
    st.markdown("### 🔄 Model Retraining")
    
    st.info("💡 The system automatically retrains when enough human feedback is collected.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Manual Retraining")
        st.markdown("**Status:** Not recommended - system auto-retrains")
        
        if st.button("🚀 Trigger Manual Retraining", disabled=True):
            st.success("Retraining triggered!")
    
    with col2:
        st.markdown("#### Auto-Retraining Settings")
        auto_retrain_threshold = st.number_input(
            "Feedback samples needed for auto-retrain:",
            min_value=10,
            max_value=100,
            value=25,
            step=5
        )
        st.info(f"Current feedback samples: 47")
        st.success(f"✅ Ready for retraining! (Exceeds threshold of {auto_retrain_threshold})")
    
    st.markdown("---")
    
    # Model Version History
    st.markdown("### 📜 Model Version History")
    
    versions = [
        {"Version": "v1.0.0", "Date": "2024-01-10", "F1": "0.85", "Status": "✅ Current"},
        {"Version": "v0.9.0", "Date": "2024-01-05", "F1": "0.82", "Status": "Archive"},
        {"Version": "v0.8.0", "Date": "2024-01-01", "F1": "0.78", "Status": "Archive"}
    ]
    
    df_versions = pd.DataFrame(versions)
    st.dataframe(df_versions, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Feedback Impact
    st.markdown("### 📈 Feedback Impact Analysis")
    
    st.markdown("#### Recent Feedback Summary")
    feedback_summary = {
        "Feedback Type": ["Correct", "Incorrect", "Partial", "Threshold Adjustment"],
        "Count": [28, 12, 5, 2],
        "Impact": ["+2% F1", "-1% Precision", "Neutral", "Threshold Updated"]
    }
    
    df_feedback = pd.DataFrame(feedback_summary)
    st.dataframe(df_feedback, use_container_width=True, hide_index=True)
    
    st.success("✅ Model is continuously improving based on human feedback!")

