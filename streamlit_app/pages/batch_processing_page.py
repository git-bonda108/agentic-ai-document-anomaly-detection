"""
Batch Processing Page
Process documents from S3 folder
"""

import os
import streamlit as st
import boto3
from typing import List
from agents.batch_ingestion_agent import BatchIngestionAgent
import pandas as pd

def render_batch_processing_page():
    """Render batch processing page"""
    
    st.markdown('<h1 class="main-header">📦 Batch Processing from S3</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize batch agent if not in session
    if "batch_agent" not in st.session_state:
        st.session_state.batch_agent = BatchIngestionAgent()
    
    batch_agent = st.session_state.batch_agent
    
    # S3 Configuration
    st.markdown("### ⚙️ S3 Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get bucket name from config or input
        try:
            import json
            if os.path.exists("aws_config.json"):
                with open("aws_config.json", "r") as f:
                    config = json.load(f)
                    default_bucket = config.get("buckets", {}).get("raw_docs", "")
            else:
                default_bucket = f"doc-anomaly-raw-docs-597088017095"
        except:
            default_bucket = f"doc-anomaly-raw-docs-597088017095"
        
        bucket_name = st.text_input(
            "S3 Bucket Name",
            value=default_bucket,
            help="S3 bucket containing documents to process"
        )
    
    with col2:
        folder_path = st.text_input(
            "S3 Folder Path (Prefix)",
            value="documents/",
            help="Folder path in S3 (e.g., 'documents/' or 'invoices/2024/')"
        )
    
    # List documents in S3 folder
    if st.button("🔍 List Documents in S3 Folder", type="secondary"):
        if bucket_name and folder_path:
            list_s3_documents(bucket_name, folder_path)
        else:
            st.error("Please provide bucket name and folder path")
    
    st.markdown("---")
    
    # Batch Processing
    st.markdown("### 🚀 Batch Processing")
    
    recursive = st.checkbox("Process subfolders recursively", value=True)
    max_workers = st.slider("Parallel Workers", min_value=1, max_value=10, value=3)
    
    if st.button("▶️ Process All Documents in S3 Folder", type="primary", use_container_width=True):
        if bucket_name and folder_path:
            process_s3_folder_batch(bucket_name, folder_path, recursive, max_workers)
        else:
            st.error("Please provide bucket name and folder path")
    
    st.markdown("---")
    
    # Batch Processing History
    if "batch_results" in st.session_state and st.session_state.batch_results:
        st.markdown("### 📊 Batch Processing Results")
        
        results = st.session_state.batch_results
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Documents", results.get("total_documents", 0))
        with col2:
            st.metric("Processed", results.get("processed", 0))
        with col3:
            st.metric("Failed", results.get("failed", 0))
        with col4:
            success_rate = (results.get("processed", 0) / results.get("total_documents", 1)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        # Results table
        if results.get("results"):
            df_results = pd.DataFrame(results["results"])
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            # Download results
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name=f"batch_results_{results.get('batch_id', 'unknown')}.csv",
                mime="text/csv"
            )

def list_s3_documents(bucket_name: str, folder_path: str):
    """List documents in S3 folder"""
    try:
        s3_client = boto3.client('s3')
        
        # List objects
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder_path
        )
        
        if 'Contents' in response:
            objects = response['Contents']
            
            st.success(f"✅ Found {len(objects)} objects in {bucket_name}/{folder_path}")
            
            # Display as table
            df = pd.DataFrame([{
                "Key": obj['Key'],
                "Size (KB)": f"{obj['Size'] / 1024:.2f}",
                "Modified": obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S")
            } for obj in objects])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No documents found in {bucket_name}/{folder_path}")
            
    except Exception as e:
        st.error(f"❌ Error listing S3 documents: {e}")

def process_s3_folder_batch(bucket_name: str, folder_path: str, recursive: bool, max_workers: int):
    """Process all documents in S3 folder"""
    
    batch_agent = st.session_state.batch_agent
    batch_agent.max_workers = max_workers
    
    # Progress container
    progress_container = st.container()
    status_container = st.container()
    results_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        status_text.text("📦 Starting batch processing...")
        progress_bar.progress(10)
        
        # Process folder
        status_text.text(f"🔍 Scanning S3 folder: {bucket_name}/{folder_path}...")
        progress_bar.progress(20)
        
        results = batch_agent.process_s3_folder(bucket_name, folder_path, recursive)
        progress_bar.progress(100)
        
        # Store results
        st.session_state.batch_results = results
        
        # Display results
        with results_container:
            if results.get("status") == "COMPLETED":
                status_text.text("✅ Batch processing complete!")
                
                st.success(f"""
                **Batch Processing Complete!**
                - Total Documents: {results.get('total_documents', 0)}
                - Successfully Processed: {results.get('processed', 0)}
                - Failed: {results.get('failed', 0)}
                """)
                
                # Show individual results
                if results.get("results"):
                    st.markdown("#### 📋 Individual Document Results")
                    for result in results["results"][:10]:  # Show first 10
                        if result.get("status") == "SUCCESS":
                            st.success(f"✅ {result.get('s3_key', 'N/A')} - {result.get('anomalies_count', 0)} anomalies")
                        else:
                            st.error(f"❌ {result.get('s3_key', 'N/A')} - {result.get('error', 'Unknown error')}")
                    
                    if len(results["results"]) > 10:
                        st.info(f"... and {len(results['results']) - 10} more results")
            else:
                status_text.text("⚠️ Batch processing completed with issues")
                st.warning(f"Status: {results.get('status')} - {results.get('error', 'Unknown error')}")
                
    except Exception as e:
        status_text.text("❌ Batch processing failed")
        st.error(f"❌ Error during batch processing: {str(e)}")
        import traceback
        st.exception(e)

