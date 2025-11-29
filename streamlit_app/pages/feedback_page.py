"""
Human Feedback Page
Collects and processes human feedback on predictions
"""

import streamlit as st
from datetime import datetime

def render_feedback_page():
    """Render human feedback page"""
    
    st.markdown('<h1 class="main-header">👤 Human Feedback</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if there are results to provide feedback on
    if st.session_state.current_results is None:
        st.info("👈 Process a document first to provide feedback")
        return
    
    results = st.session_state.current_results
    doc_id = results.get("document_info", {}).get("document_id", "N/A")
    anomalies = results.get("anomalies", {}).get("details", [])
    
    st.markdown(f"### 📄 Document: {doc_id}")
    st.markdown(f"**Anomalies Detected:** {len(anomalies)}")
    
    # HITL Queue Status
    orchestrator = st.session_state.orchestrator
    hitl_queue = orchestrator.get_hitl_queue()
    
    if hitl_queue:
        st.markdown("---")
        st.markdown("### ⏳ Human-in-the-Loop Queue")
        st.info(f"There are {len(hitl_queue)} documents pending review")
        
        for item in hitl_queue:
            if item.get("status") == "PENDING":
                with st.expander(f"Document: {item.get('document_id')} - Pending Review"):
                    st.json(item.get("processing_context", {}))
    
    st.markdown("---")
    
    # Feedback Section
    if len(anomalies) > 0:
        st.markdown("### 📝 Provide Feedback on Anomalies")
        
        # Overall feedback
        st.markdown("#### Overall Prediction Feedback")
        overall_feedback = st.radio(
            "How accurate are the detected anomalies?",
            ["✅ Correct - All anomalies are valid",
             "❌ Incorrect - No anomalies or false positives",
             "⚠️ Partial - Some anomalies are correct, some are not"],
            key="overall_feedback"
        )
        
        # Detailed feedback per anomaly
        st.markdown("---")
        st.markdown("#### Detailed Anomaly Feedback")
        
        feedback_items = []
        
        for i, anomaly in enumerate(anomalies):
            with st.expander(f"Anomaly {i+1}: {anomaly.get('type', 'Unknown')} - {anomaly.get('severity', 'N/A')}"):
                st.markdown(f"**Description:** {anomaly.get('description', 'N/A')}")
                st.markdown(f"**Confidence:** {anomaly.get('confidence', 0):.1%}")
                
                anomaly_feedback = st.radio(
                    "Is this anomaly correct?",
                    ["✅ Correct", "❌ Incorrect", "⚠️ Needs Adjustment"],
                    key=f"anomaly_feedback_{i}"
                )
                
                if anomaly_feedback == "⚠️ Needs Adjustment":
                    adjustment_note = st.text_area(
                        "What adjustment is needed?",
                        key=f"adjustment_{i}"
                    )
                    feedback_items.append({
                        "anomaly_index": i,
                        "anomaly_id": anomaly.get("type"),
                        "feedback": "ADJUSTMENT_NEEDED",
                        "note": adjustment_note
                    })
                else:
                    feedback_items.append({
                        "anomaly_index": i,
                        "anomaly_id": anomaly.get("type"),
                        "feedback": "CORRECT" if "✅" in anomaly_feedback else "INCORRECT"
                    })
        
        # Threshold adjustments
        st.markdown("---")
        st.markdown("#### 📊 Threshold Adjustments (Optional)")
        adjust_thresholds = st.checkbox("I want to adjust business thresholds")
        
        threshold_adjustments = {}
        if adjust_thresholds:
            col1, col2 = st.columns(2)
            with col1:
                threshold_adjustments["date_variance_days"] = st.number_input(
                    "Date Variance (days)",
                    min_value=0,
                    max_value=365,
                    value=30,
                    step=1
                )
                threshold_adjustments["amount_variance_percent"] = st.number_input(
                    "Amount Variance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0,
                    step=0.1
                )
            with col2:
                threshold_adjustments["surplus_payment_threshold_percent"] = st.number_input(
                    "Surplus Payment Threshold (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=10.0,
                    step=0.1
                )
                threshold_adjustments["schedule_miss_tolerance_days"] = st.number_input(
                    "Schedule Miss Tolerance (days)",
                    min_value=0,
                    max_value=90,
                    value=5,
                    step=1
                )
        
        # Submit feedback
        st.markdown("---")
        if st.button("💾 Submit Feedback", type="primary", use_container_width=True):
            submit_feedback(doc_id, overall_feedback, feedback_items, threshold_adjustments)
    else:
        st.success("✅ No anomalies detected - nothing to review!")
        st.info("If you believe there should be anomalies, you can still provide feedback below.")
        
        feedback_type = st.radio(
            "Should there be anomalies?",
            ["No, correct - no anomalies",
             "Yes, but system missed them"],
            key="no_anomaly_feedback"
        )
        
        if feedback_type == "Yes, but system missed them":
            missed_anomalies = st.text_area(
                "Describe the missed anomalies:",
                placeholder="Describe what anomalies should have been detected..."
            )
            
            if st.button("💾 Submit Feedback", type="primary"):
                submit_feedback(doc_id, "MISSED_ANOMALIES", [{"note": missed_anomalies}], {})

def submit_feedback(document_id: str, overall_feedback: str, 
                   detailed_feedback: list, threshold_adjustments: dict):
    """Submit feedback to orchestrator"""
    
    orchestrator = st.session_state.orchestrator
    
    feedback_data = {
        "feedback_type": "CORRECT" if "✅" in overall_feedback else ("INCORRECT" if "❌" in overall_feedback else "PARTIAL"),
        "overall_feedback": overall_feedback,
        "detailed_feedback": detailed_feedback,
        "thresholds_adjustment": threshold_adjustments if threshold_adjustments else None,
        "submitted_at": datetime.utcnow().isoformat()
    }
    
    try:
        success = orchestrator.process_hitl_feedback(document_id, feedback_data)
        
        if success:
            st.success("✅ Feedback submitted successfully!")
            st.info("Your feedback will be used to improve the system.")
        else:
            st.error("❌ Failed to submit feedback")
            
    except Exception as e:
        st.error(f"❌ Error submitting feedback: {str(e)}")





