#!/usr/bin/env python3
"""
Test script for structured output functionality
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.outlines_model import OutlinesModel
from pydantic import BaseModel

def test_structured_output():
    """Test basic structured output functionality"""
    print("Testing structured output...")
    
    try:
        # Test with a simple model (this will be slow but should work for basic testing)
        model = OutlinesModel("facebook/opt-125m")  # Small model for testing
        
        # Test simple answer
        prompt = "What is 2+2?"
        result = model.run(prompt, output_type="numeric")
        print(f"Simple answer: {result}")
        
        # Test boolean answer
        prompt = "Is 5 greater than 3?"
        result = model.run(prompt, output_type="simple")
        print(f"Boolean answer: {result}")
        
        print("Structured output test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing structured output: {e}")
        return False

if __name__ == "__main__":
    success = test_structured_output()
    sys.exit(0 if success else 1)