"""
Observability Page
Displays agent execution traces, token usage, and performance metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def render_observability_page():
    """Render observability dashboard page"""
    
    st.markdown('<h1 class="main-header">👁️ Observability Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Agent Status
    st.markdown("### 🤖 Agent Status")
    
    agents_status = {
        "Orchestrator Manager": {"status": "✅ Active", "last_activity": "2 minutes ago"},
        "Document Ingestion": {"status": "✅ Active", "last_activity": "5 minutes ago"},
        "Extraction Agent": {"status": "✅ Active", "last_activity": "3 minutes ago"},
        "Contract-Invoice Agent": {"status": "✅ Active", "last_activity": "8 minutes ago"},
        "Anomaly Detection": {"status": "✅ Active", "last_activity": "4 minutes ago"},
        "Validation Agent": {"status": "✅ Active", "last_activity": "6 minutes ago"}
    }
    
    df_agents = pd.DataFrame({
        "Agent": list(agents_status.keys()),
        "Status": [v["status"] for v in agents_status.values()],
        "Last Activity": [v["last_activity"] for v in agents_status.values()]
    })
    
    st.dataframe(df_agents, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Token Usage (Mock - would come from OpenAI API)
    st.markdown("### 💰 Token Usage (OpenAI GPT-4o)")
    
    # Mock token usage data
    token_data = {
        "Date": pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D').strftime('%Y-%m-%d'),
        "Prompt Tokens": [1250, 1380, 1120, 1560, 1450, 1620, 1340],
        "Completion Tokens": [320, 380, 290, 410, 360, 430, 340],
        "Total Tokens": [1570, 1760, 1410, 1970, 1810, 2050, 1680]
    }
    
    df_tokens = pd.DataFrame(token_data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tokens (7 days)", f"{sum(df_tokens['Total Tokens']):,}")
        st.metric("Avg Tokens/Day", f"{sum(df_tokens['Total Tokens'])/7:.0f}")
    
    with col2:
        # Estimate cost (GPT-4o pricing: $2.50 per 1M input tokens, $10 per 1M output tokens)
        total_input_cost = (sum(df_tokens['Prompt Tokens']) / 1_000_000) * 2.50
        total_output_cost = (sum(df_tokens['Completion Tokens']) / 1_000_000) * 10
        total_cost = total_input_cost + total_output_cost
        
        st.metric("Estimated Cost (7 days)", f"${total_cost:.2f}")
        st.metric("Avg Cost/Day", f"${total_cost/7:.2f}")
    
    fig_tokens = px.line(
        df_tokens,
        x="Date",
        y=["Prompt Tokens", "Completion Tokens", "Total Tokens"],
        title="Token Usage Over Time",
        labels={"value": "Tokens", "variable": "Token Type"}
    )
    st.plotly_chart(fig_tokens, use_container_width=True)
    
    st.markdown("---")
    
    # Agent Execution Times
    st.markdown("### ⏱️ Agent Execution Times")
    
    execution_times = {
        "Agent": ["Ingestion", "Extraction", "Contract-Invoice", "Anomaly Detection", "Validation", "Orchestrator"],
        "Avg Time (s)": [0.5, 1.2, 0.8, 0.9, 0.6, 2.5],
        "Max Time (s)": [0.8, 1.8, 1.2, 1.5, 1.0, 4.0]
    }
    
    df_exec = pd.DataFrame(execution_times)
    
    fig_exec = px.bar(
        df_exec,
        x="Agent",
        y=["Avg Time (s)", "Max Time (s)"],
        title="Agent Execution Times",
        barmode="group",
        labels={"value": "Time (seconds)"}
    )
    st.plotly_chart(fig_exec, use_container_width=True)
    
    st.markdown("---")
    
    # CloudWatch Logs (Mock)
    st.markdown("### 📊 CloudWatch Logs")
    
    logs = [
        {"Timestamp": "2024-01-15 10:23:45", "Agent": "Orchestrator", "Level": "INFO", "Message": "Processing document DOC_12345"},
        {"Timestamp": "2024-01-15 10:23:46", "Agent": "Ingestion", "Level": "INFO", "Message": "Document uploaded to S3"},
        {"Timestamp": "2024-01-15 10:23:48", "Agent": "Extraction", "Level": "INFO", "Message": "Extracted 12 fields using GPT-4o"},
        {"Timestamp": "2024-01-15 10:23:50", "Agent": "Anomaly Detection", "Level": "WARNING", "Message": "Detected 3 anomalies"},
        {"Timestamp": "2024-01-15 10:23:52", "Agent": "Validation", "Level": "INFO", "Message": "Validation completed - Risk: MEDIUM"},
    ]
    
    df_logs = pd.DataFrame(logs)
    st.dataframe(df_logs, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Performance Metrics
    st.markdown("### 📈 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents Processed", "47")
        st.metric("Success Rate", "98.5%")
    with col2:
        st.metric("Avg Processing Time", "2.8s")
        st.metric("Error Rate", "1.5%")
    with col3:
        st.metric("HITL Queue Size", len(st.session_state.orchestrator.get_hitl_queue()) if hasattr(st.session_state, 'orchestrator') else 0)
        st.metric("Feedback Received", "12")
    
    st.info("📝 Note: Some metrics are mock data. Real metrics will appear after AWS CloudWatch integration is configured.")





