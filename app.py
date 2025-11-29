"""
DOC Anomaly Detection System - Flask Web Interface
Enterprise-friendly web interface for document processing and anomaly detection
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import logging

from orchestrator import DocumentProcessingOrchestrator

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'doc_anomaly_detection_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png', 'tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize orchestrator
orchestrator = DocumentProcessingOrchestrator()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_anomalies_for_display(anomalies):
    """Format anomalies for HTML display"""
    if not anomalies:
        return []
    
    formatted = []
    for anomaly in anomalies:
        severity_color = {
            'HIGH': 'danger',
            'MEDIUM': 'warning', 
            'LOW': 'info'
        }.get(anomaly.get('severity', 'LOW'), 'info')
        
        formatted.append({
            'type': anomaly.get('type', 'Unknown'),
            'severity': anomaly.get('severity', 'LOW'),
            'description': anomaly.get('description', 'No description'),
            'confidence': f"{anomaly.get('confidence', 0):.1%}",
            'color_class': severity_color
        })
    
    return formatted

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and processing"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Secure the filename
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                # Save file
                file.save(filepath)
                
                # Process document
                logger.info(f"Processing uploaded file: {filename}")
                result = orchestrator.process_document(filepath)
                
                # Redirect to results page
                return redirect(url_for('results', session_id=result['session_id']))
                
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload PDF, DOCX, or image files.', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/results/<session_id>')
def results(session_id):
    """Display processing results"""
    # In a real implementation, you would retrieve results from database
    # For now, we'll show a placeholder
    return render_template('results.html', session_id=session_id)

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for document processing"""
    try:
        data = request.get_json()
        document_path = data.get('document_path')
        
        if not document_path:
            return jsonify({'error': 'document_path is required'}), 400
        
        # Validate document path
        validation = orchestrator.validate_document_path(document_path)
        if not validation['valid']:
            return jsonify({'error': validation['error']}), 400
        
        # Process document
        result = orchestrator.process_document(document_path)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch_process', methods=['POST'])
def api_batch_process():
    """API endpoint for batch document processing"""
    try:
        data = request.get_json()
        document_paths = data.get('document_paths', [])
        
        if not document_paths:
            return jsonify({'error': 'document_paths is required'}), 400
        
        # Validate all document paths
        for path in document_paths:
            validation = orchestrator.validate_document_path(path)
            if not validation['valid']:
                return jsonify({'error': f'Invalid path: {path} - {validation["error"]}'}), 400
        
        # Process documents
        result = orchestrator.batch_process_documents(document_paths)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API batch processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary')
def api_summary():
    """API endpoint for processing summary"""
    try:
        summary = orchestrator.get_processing_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f"API summary error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Processing dashboard"""
    return render_template('dashboard.html')

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 50MB.', 'error')
    return redirect(url_for('upload_file'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the app on port 8080 (avoiding macOS AirPlay on 5000)
    app.run(debug=True, host='0.0.0.0', port=8080)
