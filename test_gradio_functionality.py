#!/usr/bin/env python3
"""
Test script to verify Gradio application functionality
Tests document processing with sample files
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    try:
        import gradio as gr
        print("  ✅ gradio")
        
        import pandas as pd
        print("  ✅ pandas")
        
        from orchestrator import DocumentProcessingOrchestrator
        print("  ✅ DocumentProcessingOrchestrator")
        
        from agents import DocumentIngestionAgent, ExtractionAgent, AnomalyDetectionAgent
        print("  ✅ All agents")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_orchestrator():
    """Test orchestrator initialization"""
    print("\n🧪 Testing orchestrator...")
    try:
        from orchestrator import DocumentProcessingOrchestrator
        orchestrator = DocumentProcessingOrchestrator()
        print("  ✅ Orchestrator initialized")
        return True
    except Exception as e:
        print(f"  ❌ Orchestrator error: {e}")
        return False

def test_sample_processing():
    """Test document processing with sample file"""
    print("\n🧪 Testing document processing...")
    try:
        from orchestrator import DocumentProcessingOrchestrator
        
        # Find a sample document
        sample_dir = Path("sample_data")
        sample_files = list(sample_dir.glob("*.pdf"))
        
        if not sample_files:
            print("  ⚠️  No sample files found")
            return False
        
        sample_file = sample_files[0]
        print(f"  📄 Testing with: {sample_file.name}")
        
        orchestrator = DocumentProcessingOrchestrator()
        result = orchestrator.process_document(str(sample_file))
        
        # Check result structure
        if result.get("workflow_status") == "COMPLETED":
            print("  ✅ Document processed successfully")
            print(f"  📊 Document ID: {result.get('document_info', {}).get('document_id')}")
            print(f"  📋 Fields extracted: {len(result.get('extracted_data', {}))}")
            print(f"  🚨 Anomalies found: {result.get('anomalies', {}).get('count', 0)}")
            return True
        else:
            print(f"  ❌ Processing failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"  ❌ Processing error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gradio_app():
    """Test Gradio app structure"""
    print("\n🧪 Testing Gradio app...")
    try:
        from gradio_app import demo, process_document
        print("  ✅ Gradio app imported")
        print("  ✅ Process function available")
        return True
    except Exception as e:
        print(f"  ❌ Gradio app error: {e}")
        return False

def test_server_running():
    """Test if Gradio server is running"""
    print("\n🧪 Testing server status...")
    try:
        import requests
        response = requests.get("http://localhost:7860", timeout=5)
        if response.status_code == 200:
            print("  ✅ Gradio server is running on port 7860")
            print("  🌐 Access at: http://localhost:7860")
            return True
        else:
            print(f"  ⚠️  Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ⚠️  Gradio server is not running")
        print("  💡 Launch with: python run_gradio.py --mode remote")
        return False
    except ImportError:
        print("  ⚠️  requests library not installed (optional)")
        return False
    except Exception as e:
        print(f"  ⚠️  Server check error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🤖 DOC ANOMALY DETECTION SYSTEM - FUNCTIONALITY TEST")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Orchestrator", test_orchestrator),
        ("Sample Processing", test_sample_processing),
        ("Gradio App", test_gradio_app),
        ("Server Status", test_server_running)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is fully functional.")
        print("\n🚀 Launch commands:")
        print("  • Local: python run_gradio.py --mode local")
        print("  • Remote: python run_gradio.py --mode remote")
        print("  • Enterprise: python run_gradio.py --mode enterprise --port 8080")
    else:
        print("⚠️  Some tests failed. Please review errors above.")
    
    print("=" * 70)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




