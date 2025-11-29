"""
Results Dashboard Page
Displays processing results, anomalies, and validation summaries
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def render_results_page():
    """Render results dashboard page"""
    
    st.markdown('<h1 class="main-header">📊 Results Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if there are results
    if st.session_state.current_results is None:
        st.info("👈 Upload and process a document to see results here")
        return
    
    results = st.session_state.current_results
    
    if results.get("workflow_status") != "COMPLETED":
        st.error(f"❌ Processing Status: {results.get('workflow_status')}")
        if "error" in results:
            st.error(f"Error: {results['error']}")
        return
    
    # Document Information
    st.markdown("### 📄 Document Information")
    doc_info = results.get("document_info", {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Document ID", doc_info.get("document_id", "N/A"))
    with col2:
        st.metric("Document Type", doc_info.get("document_type", "N/A"))
    with col3:
        st.metric("Processing Time", f"{results.get('processing_time', 0):.2f}s")
    with col4:
        st.metric("Status", "✅ Completed")
    
    st.markdown("---")
    
    # Extracted Data
    st.markdown("### 🔍 Extracted Data")
    extracted_data = results.get("extracted_data", {})
    
    if extracted_data:
        # Format extracted data as DataFrame
        df_data = []
        for field_name, field_value in extracted_data.items():
            if isinstance(field_value, tuple):
                value, confidence = field_value
            elif isinstance(field_value, dict):
                value = field_value.get("value", "")
                confidence = field_value.get("confidence", 0.0)
            else:
                value = field_value
                confidence = 0.0
            
            df_data.append({
                "Field": field_name.replace("_", " ").title(),
                "Value": str(value),
                "Confidence": f"{confidence:.1%}" if isinstance(confidence, (int, float)) else "N/A"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No extracted data available")
    
    st.markdown("---")
    
    # Anomalies Section
    anomalies_data = results.get("anomalies", {})
    anomalies_count = anomalies_data.get("count", 0)
    anomalies_list = anomalies_data.get("details", [])
    
    st.markdown(f"### 🚨 Anomalies Detected: {anomalies_count}")
    
    if anomalies_count > 0:
        # Anomaly Statistics
        col1, col2, col3 = st.columns(3)
        
        # Count by severity
        severity_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for anomaly in anomalies_list:
            severity = anomaly.get("severity", "LOW")
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        with col1:
            st.metric("High Severity", severity_count["HIGH"], delta=None)
        with col2:
            st.metric("Medium Severity", severity_count["MEDIUM"], delta=None)
        with col3:
            st.metric("Low Severity", severity_count["LOW"], delta=None)
        
        # Anomaly visualization
        if len(anomalies_list) > 0:
            # Severity pie chart
            fig_severity = px.pie(
                values=list(severity_count.values()),
                names=list(severity_count.keys()),
                title="Anomalies by Severity",
                color_discrete_map={"HIGH": "#ff0000", "MEDIUM": "#ffaa00", "LOW": "#00aa00"}
            )
            st.plotly_chart(fig_severity, use_container_width=True)
            
            # Anomaly types bar chart
            anomaly_types = {}
            for anomaly in anomalies_list:
                anomaly_type = anomaly.get("type", "UNKNOWN")
                anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
            
            if anomaly_types:
                fig_types = px.bar(
                    x=list(anomaly_types.keys()),
                    y=list(anomaly_types.values()),
                    title="Anomalies by Type",
                    labels={"x": "Anomaly Type", "y": "Count"}
                )
                st.plotly_chart(fig_types, use_container_width=True)
        
        # Detailed Anomaly List
        st.markdown("#### 📋 Anomaly Details")
        for i, anomaly in enumerate(anomalies_list, 1):
            severity = anomaly.get("severity", "LOW")
            css_class = f"anomaly-{severity.lower()}"
            
            with st.expander(f"Anomaly {i}: {anomaly.get('type', 'Unknown')} - {severity} Severity"):
                st.markdown(
                    f'<div class="{css_class}">',
                    unsafe_allow_html=True
                )
                st.markdown(f"**Type:** {anomaly.get('type', 'N/A')}")
                st.markdown(f"**Subtype:** {anomaly.get('subtype', 'N/A')}")
                st.markdown(f"**Severity:** {severity}")
                st.markdown(f"**Confidence:** {anomaly.get('confidence', 0):.1%}")
                st.markdown(f"**Description:** {anomaly.get('description', 'No description')}")
                
                # Additional details
                if "contract_amount" in anomaly:
                    st.markdown(f"**Contract Amount:** ${anomaly.get('contract_amount', 0):,.2f}")
                if "invoice_amount" in anomaly:
                    st.markdown(f"**Invoice Amount:** ${anomaly.get('invoice_amount', 0):,.2f}")
                if "variance_percent" in anomaly:
                    st.markdown(f"**Variance:** {anomaly.get('variance_percent', 0):.1f}%")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ No anomalies detected!")
    
    st.markdown("---")
    
    # Validation Summary
    validation = results.get("validation")
    if validation:
        st.markdown("### ✅ Validation Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Anomalies", validation.get("total_anomalies", 0))
        with col2:
            st.metric("Within Thresholds", validation.get("within_thresholds", 0))
        with col3:
            st.metric("Exceeds Thresholds", validation.get("exceeds_thresholds", 0))
        
        risk_level = validation.get("risk_level", "NONE")
        risk_color = {
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "NONE": "⚪"
        }
        st.markdown(f"**Risk Level:** {risk_color.get(risk_level, '⚪')} {risk_level}")
        
        # Recommendations
        recommendations = validation.get("recommendations", [])
        if recommendations:
            st.markdown("#### 💡 Recommendations")
            for rec in recommendations:
                st.info(f"• {rec}")
    
    # Processing timestamp
    st.markdown("---")
    timestamp = results.get("timestamp", datetime.now().isoformat())
    st.caption(f"Processing completed at: {timestamp}")





