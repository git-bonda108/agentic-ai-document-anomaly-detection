"""
Upload & Process Page
Document upload and processing interface
"""

import streamlit as st
import os
import time
from datetime import datetime

def render_upload_page():
    """Render upload and processing page"""
    
    st.markdown('<h1 class="main-header">📄 Upload & Process Document</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png'],
            help="Upload invoices or contracts for anomaly detection"
        )
    
    with col2:
        st.markdown("### 📋 Supported Formats")
        st.markdown("- PDF Documents")
        st.markdown("- Microsoft Word (.docx, .doc)")
        st.markdown("- Images (.jpg, .jpeg, .png)")
        st.markdown("**Max Size:** 50 MB")
    
    if uploaded_file is not None:
        # Display file info
        st.markdown("---")
        st.markdown("### 📄 File Information")
        
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filename", uploaded_file.name)
        with col2:
            st.metric("Size", f"{uploaded_file.size / 1024:.2f} KB")
        with col3:
            st.metric("Type", uploaded_file.type or "Unknown")
        
        # Save uploaded file temporarily
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(upload_dir, f"{timestamp}_{uploaded_file.name}")
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File saved: {file_path}")
        
        # Process button
        st.markdown("---")
        if st.button("🚀 Process Document", type="primary", use_container_width=True):
            process_document(file_path)
    
    # Processing history
    if st.session_state.processing_history:
        st.markdown("---")
        st.markdown("### 📜 Recent Processing")
        for i, history_item in enumerate(reversed(st.session_state.processing_history[-5:])):
            with st.expander(f"Session: {history_item.get('session_id', 'N/A')} - {history_item.get('timestamp', 'N/A')}"):
                st.json(history_item)

def process_document(file_path: str):
    """Process uploaded document"""
    
    orchestrator = st.session_state.orchestrator
    
    # Create progress container
    progress_container = st.container()
    status_container = st.container()
    results_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    # Processing steps
    steps = [
        "📥 Document Ingestion...",
        "🔍 Data Extraction...",
        "🚨 Anomaly Detection...",
        "✅ Validation...",
        "📊 Generating Summary..."
    ]
    
    try:
        # Step 1: Document Ingestion
        status_text.text(steps[0])
        progress_bar.progress(10)
        time.sleep(0.5)
        
        # Step 2: Data Extraction
        status_text.text(steps[1])
        progress_bar.progress(30)
        time.sleep(0.5)
        
        # Step 3: Anomaly Detection
        status_text.text(steps[2])
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Step 4: Validation
        status_text.text(steps[3])
        progress_bar.progress(70)
        time.sleep(0.5)
        
        # Actual processing
        status_text.text("🤖 Processing with Orchestrator...")
        result = orchestrator.process_document(file_path)
        
        # Step 5: Summary
        status_text.text(steps[4])
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Store results
        st.session_state.current_results = result
        st.session_state.processing_history.append({
            "session_id": result.get("session_id"),
            "timestamp": datetime.now().isoformat(),
            "document_id": result.get("document_info", {}).get("document_id"),
            "status": result.get("workflow_status"),
            "anomalies_count": result.get("anomalies", {}).get("count", 0)
        })
        
        # Display results
        with results_container:
            status_text.text("✅ Processing Complete!")
            progress_bar.progress(100)
            
            st.markdown("### ✅ Processing Results")
            
            if result.get("workflow_status") == "COMPLETED":
                doc_info = result.get("document_info", {})
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Document ID", doc_info.get("document_id", "N/A")[:12])
                with col2:
                    st.metric("Document Type", doc_info.get("document_type", "N/A"))
                with col3:
                    st.metric("Anomalies", result.get("anomalies", {}).get("count", 0))
                with col4:
                    st.metric("Processing Time", f"{result.get('processing_time', 0):.2f}s")
                
                # Show if HITL required
                if result.get("requires_hitl"):
                    st.warning("⚠️ This document requires Human-in-the-Loop review. Please check the Human Feedback page.")
                
                st.success("✅ Document processed successfully! Check Results Dashboard for details.")
                
                # Quick anomaly summary
                anomalies = result.get("anomalies", {}).get("details", [])
                if anomalies:
                    st.markdown("### 🚨 Quick Anomaly Summary")
                    for anomaly in anomalies[:5]:  # Show first 5
                        severity = anomaly.get("severity", "LOW")
                        css_class = f"anomaly-{severity.lower()}"
                        st.markdown(
                            f'<div class="{css_class}">'
                            f'<strong>{anomaly.get("type", "Unknown")}</strong>: '
                            f'{anomaly.get("description", "No description")} '
                            f'(Confidence: {anomaly.get("confidence", 0):.1%})'
                            f'</div>',
                            unsafe_allow_html=True
                        )
            else:
                st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        status_text.text("❌ Processing Failed")
        import traceback
        st.exception(e)





