"""
DOC Anomaly Detection System - Streamlit Main App
Multi-page application for document processing and anomaly detection
"""

import streamlit as st
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except:
    pass  # dotenv not required if environment variables already set

# Configure Streamlit page
st.set_page_config(
    page_title="DOC Anomaly Detection System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "orchestrator" not in st.session_state:
    from agents.orchestrator_manager import OrchestratorManager
    st.session_state.orchestrator = OrchestratorManager()

if "processing_history" not in st.session_state:
    st.session_state.processing_history = []

if "current_results" not in st.session_state:
    st.session_state.current_results = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .anomaly-high {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ff0000;
    }
    .anomaly-medium {
        background-color: #fff4cc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffaa00;
    }
    .anomaly-low {
        background-color: #ccffcc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #00aa00;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 🤖 DOC Anomaly Detection")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📄 Upload & Process", "📦 Batch Processing (S3)", "📊 Results Dashboard", 
     "👤 Human Feedback", "📈 Metrics & Analytics", "👁️ Observability", "🧠 Training Management"],
    key="navigation"
)

# Route to appropriate page
if page == "📄 Upload & Process":
    from streamlit_app.pages.upload_page import render_upload_page
    render_upload_page()
elif page == "📦 Batch Processing (S3)":
    from streamlit_app.pages.batch_processing_page import render_batch_processing_page
    render_batch_processing_page()
elif page == "📊 Results Dashboard":
    from streamlit_app.pages.results_page import render_results_page
    render_results_page()
elif page == "👤 Human Feedback":
    from streamlit_app.pages.feedback_page import render_feedback_page
    render_feedback_page()
elif page == "📈 Metrics & Analytics":
    from streamlit_app.pages.metrics_page import render_metrics_page
    render_metrics_page()
elif page == "👁️ Observability":
    from streamlit_app.pages.observability_page import render_observability_page
    render_observability_page()
elif page == "🧠 Training Management":
    from streamlit_app.pages.training_page import render_training_page
    render_training_page()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Status:** ✅ Operational")
st.sidebar.markdown("**Version:** 1.0.0")
st.sidebar.markdown("**Powered by:** OpenAI GPT-4o + AWS")

