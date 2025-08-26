#!/usr/bin/env python3
"""
Comprehensive test for enhanced structured output functionality
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.outlines_model import OutlinesModel

def test_enhanced_structured_output():
    """Test enhanced structured output functionality"""
    print("Testing enhanced structured output...")
    
    try:
        # Initialize with a small model for testing
        model = OutlinesModel("facebook/opt-125m")
        
        # Test 1: Card selection with dynamic options
        print("\n1. Testing card selection...")
        prompt = "Choose the best green card for a draft."
        result = model.run(
            prompt, 
            output_type="card_selection", 
            options=["Lightning Bolt", "Serra Angel", "Llanowar Elves", "Forest"]
        )
        print(f"   Card selection result: {result}")
        
        # Test 2: Multiple choice
        print("\n2. Testing multiple choice...")
        prompt = "What is the color of Llanowar Elves?"
        result = model.run(
            prompt, 
            output_type="multiple_choice", 
            choices=["Red", "Blue", "Green", "White", "Black"]
        )
        print(f"   Multiple choice result: {result}")
        
        # Test 3: Numeric range
        print("\n3. Testing numeric range...")
        prompt = "How much damage does a 3/3 creature deal when attacking?"
        result = model.run(
            prompt, 
            output_type="numeric_range", 
            min_val=0, 
            max_val=3
        )
        print(f"   Numeric range result: {result}")
        
        # Test 4: MTG phase
        print("\n4. Testing phase identification...")
        prompt = "What is the first phase of your turn?"
        result = model.run(prompt, output_type="phase")
        print(f"   Phase result: {result}")
        
        # Test 5: Card type
        print("\n5. Testing card type identification...")
        prompt = "What type of card is Serra Angel?"
        result = model.run(prompt, output_type="card_type")
        print(f"   Card type result: {result}")
        
        # Test 6: Boolean
        print("\n6. Testing boolean output...")
        prompt = "Is Serra Angel a creature?"
        result = model.run(prompt, output_type="boolean")
        print(f"   Boolean result: {result}")
        
        # Test 7: Simple numeric
        print("\n7. Testing simple numeric...")
        prompt = "What is 5 + 3?"
        result = model.run(prompt, output_type="numeric")
        print(f"   Numeric result: {result}")
        
        print("\nEnhanced structured output test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing enhanced structured output: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_structured_output()
    sys.exit(0 if success else 1)