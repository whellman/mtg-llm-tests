#!/usr/bin/env python3
"""
Test script to verify boolean extraction fix
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_boolean_extraction():
    """Test that boolean extraction works correctly"""
    print("Testing boolean extraction fix...")
    
    try:
        # Test the extraction logic
        from models.outlines_model import OutlinesModel
        import json
        
        # Create a mock boolean result
        class MockBooleanResult:
            def __init__(self, value):
                self.answer = value
        
        # Test True -> "true"
        model = OutlinesModel.__new__(OutlinesModel)  # Create without calling __init__
        result_true = MockBooleanResult(True)
        extracted_true = model._extract_answer(result_true, "boolean")
        print(f"✓ True -> '{extracted_true}' (expected: 'true')")
        assert extracted_true == "true", f"Expected 'true', got '{extracted_true}'"
        
        # Test False -> "false"
        result_false = MockBooleanResult(False)
        extracted_false = model._extract_answer(result_false, "boolean")
        print(f"✓ False -> '{extracted_false}' (expected: 'false')")
        assert extracted_false == "false", f"Expected 'false', got '{extracted_false}'"
        
        print("✓ Boolean extraction fix verified!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing boolean extraction: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_boolean_extraction()
    sys.exit(0 if success else 1)