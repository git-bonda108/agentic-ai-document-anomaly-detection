"""
Metrics & Analytics Page
Displays ML metrics, performance analytics, and visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render_metrics_page():
    """Render metrics and analytics page"""
    
    st.markdown('<h1 class="main-header">📈 Metrics & Analytics</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check processing history
    history = st.session_state.processing_history
    
    if not history:
        st.info("👈 Process some documents to see metrics here")
        return
    
    # Overall Statistics
    st.markdown("### 📊 Overall Statistics")
    
    total_docs = len(history)
    total_anomalies = sum(h.get("anomalies_count", 0) for h in history)
    avg_anomalies = total_anomalies / total_docs if total_docs > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", total_docs)
    with col2:
        st.metric("Total Anomalies", total_anomalies)
    with col3:
        st.metric("Avg Anomalies/Doc", f"{avg_anomalies:.2f}")
    with col4:
        completed = sum(1 for h in history if h.get("status") == "COMPLETED")
        st.metric("Success Rate", f"{(completed/total_docs*100):.1f}%" if total_docs > 0 else "N/A")
    
    st.markdown("---")
    
    # Processing Time Trend
    st.markdown("### ⏱️ Processing Time Trend")
    
    if len(history) > 1:
        # Create mock processing times (in real app, these would be from actual results)
        df_times = pd.DataFrame({
            "Session": [f"Session {i+1}" for i in range(len(history))],
            "Processing Time (s)": np.random.uniform(2, 5, len(history))  # Mock data
        })
        
        fig_times = px.line(
            df_times,
            x="Session",
            y="Processing Time (s)",
            title="Processing Time Over Sessions",
            markers=True
        )
        st.plotly_chart(fig_times, use_container_width=True)
    
    # Anomaly Distribution
    st.markdown("---")
    st.markdown("### 🚨 Anomaly Distribution")
    
    # Mock anomaly type distribution
    anomaly_types = {
        "DATE_MISMATCH": 15,
        "AMOUNT_DISCREPANCY": 12,
        "SCHEDULE_MISS": 8,
        "SURPLUS_PAYMENT": 5,
        "MISSED_PAYMENT": 6,
        "SCHEDULE_MISALIGNMENT": 4
    }
    
    df_anomaly_types = pd.DataFrame({
        "Anomaly Type": list(anomaly_types.keys()),
        "Count": list(anomaly_types.values())
    })
    
    fig_types = px.bar(
        df_anomaly_types,
        x="Anomaly Type",
        y="Count",
        title="Anomalies by Type",
        color="Count",
        color_continuous_scale="Reds"
    )
    fig_types.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_types, use_container_width=True)
    
    # Severity Distribution
    st.markdown("---")
    st.markdown("### ⚠️ Severity Distribution")
    
    severity_dist = {
        "HIGH": 8,
        "MEDIUM": 25,
        "LOW": 17
    }
    
    fig_severity = px.pie(
        values=list(severity_dist.values()),
        names=list(severity_dist.keys()),
        title="Anomalies by Severity",
        color_discrete_map={"HIGH": "#ff0000", "MEDIUM": "#ffaa00", "LOW": "#00aa00"}
    )
    st.plotly_chart(fig_severity, use_container_width=True)
    
    # Confusion Matrix (Mock)
    st.markdown("---")
    st.markdown("### 🔢 Model Performance Metrics")
    
    # Mock confusion matrix
    confusion_matrix = np.array([
        [45, 5, 2],   # True Positive, False Positive, False Negative
        [3, 38, 4],
        [1, 2, 40]
    ])
    
    labels = ["No Anomaly", "Anomaly", "High Risk"]
    
    fig_confusion = go.Figure(data=go.Heatmap(
        z=confusion_matrix,
        x=labels,
        y=labels,
        colorscale='Blues',
        text=confusion_matrix,
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar={"title": "Count"}
    ))
    
    fig_confusion.update_layout(
        title="Confusion Matrix (Mock Data)",
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )
    
    st.plotly_chart(fig_confusion, use_container_width=True)
    
    # Performance Metrics
    st.markdown("---")
    st.markdown("### 📈 Performance Metrics")
    
    # Mock metrics
    precision = 0.85
    recall = 0.82
    f1_score = 0.83
    accuracy = 0.88
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precision", f"{precision:.1%}")
    with col2:
        st.metric("Recall", f"{recall:.1%}")
    with col3:
        st.metric("F1 Score", f"{f1_score:.1%}")
    with col4:
        st.metric("Accuracy", f"{accuracy:.1%}")
    
    # ROC Curve (Mock)
    st.markdown("---")
    st.markdown("### 📉 ROC Curve")
    
    # Mock ROC curve data
    fpr = np.linspace(0, 1, 100)
    tpr = np.power(fpr, 0.5)  # Mock ROC curve
    
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name='ROC Curve',
        line=dict(color='blue', width=2)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='red', width=2, dash='dash')
    ))
    fig_roc.update_layout(
        title="ROC Curve (Mock Data)",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        xaxis_range=[0, 1],
        yaxis_range=[0, 1]
    )
    
    st.plotly_chart(fig_roc, use_container_width=True)
    
    st.info("📝 Note: These are mock metrics. Real metrics will be displayed once documents are processed with feedback data.")





