#!/bin/bash
# Start the DOC Anomaly Detection System with remote sharing

echo "🚀 Starting DOC Anomaly Detection System..."
echo "=" 
echo ""
echo "⏳ Initializing... please wait 10-15 seconds"
echo ""

source venv/bin/activate
python run_gradio.py --mode remote 2>&1 | tee gradio_output.log








