#!/bin/bash
# Quick copy script for streamlit_app to EC2

cd ~/Downloads

echo "Copying streamlit_app to EC2..."
scp -i doc-anomaly-key.pem -r "/Users/macbook/Documents/DOC ANOMALY DETECTION SYSTEM/streamlit_app" ec2-user@13.219.178.111:~/DOC\ ANOMALY\ DETECTION\ SYSTEM/

echo "Done! Now SSH to EC2 and run:"
echo "cd 'DOC ANOMALY DETECTION SYSTEM'"
echo "source venv/bin/activate"
echo "streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0"





