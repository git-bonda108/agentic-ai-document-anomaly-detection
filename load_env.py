"""
Load environment variables from .env file
"""

import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ Loaded environment variables from .env file")
    else:
        print("⚠️  .env file not found, using system environment variables")
    
    # Set required variables
    required_vars = {
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'AWS_REGION': os.getenv('AWS_REGION', 'us-east-1'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }
    
    for key, value in required_vars.items():
        if value:
            os.environ[key] = value
        elif key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'OPENAI_API_KEY']:
            print(f"⚠️  {key} not set")
    
    return required_vars

# Auto-load on import
load_environment()





