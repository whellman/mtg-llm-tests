#!/usr/bin/env python3
"""
Test script for structured output functionality
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.outlines_model import OutlinesModel

def test_structured_output():
    """Test basic structured output functionality"""
    print("Testing structured output...")
    
    try:
        # Test with a simple model (this will be slow but should work for basic testing)
        model = OutlinesModel("facebook/opt-125m")  # Small model for testing
        
        # Test simple answer
        prompt = "What is 2+2?"
        result = model.run(prompt, output_type="numeric")
        print(f"Numeric answer: {result}")
        
        # Test boolean answer
        prompt = "Is 5 greater than 3?"
        result = model.run(prompt, output_type="boolean")
        print(f"Boolean answer: {result}")
        
        # Test card selection with dynamic options
        prompt = "Choose the best card for a green/white deck from these options."
        result = model.run(prompt, output_type="card_selection", options=["Lightning Bolt", "Serra Angel", "Llanowar Elves"])
        print(f"Card selection: {result}")
        
        # Test multiple choice
        prompt = "What is the capital of France?"
        result = model.run(prompt, output_type="multiple_choice", choices=["London", "Paris", "Berlin", "Madrid"])
        print(f"Multiple choice: {result}")
        
        # Test numeric range
        prompt = "How much damage do you take when a 6/6 trample attacks you and you block with a 3/3?"
        result = model.run(prompt, output_type="numeric_range", min_val=0, max_val=10)
        print(f"Numeric range: {result}")
        
        print("Structured output test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing structured output: {e}")
        return False

if __name__ == "__main__":
    success = test_structured_output()
    sys.exit(0 if success else 1)