#!/usr/bin/env python3
"""
Lightweight test for structured output logic without loading models
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.structured_schemas import SchemaFactory, SCHEMA_REGISTRY
import json

def test_schema_generation():
    """Test dynamic schema generation"""
    print("Testing schema generation...")
    
    try:
        # Test card selection schema
        card_options = ["Lightning Bolt", "Serra Angel", "Llanowar Elves"]
        CardSelectionSchema = SchemaFactory.create_card_selection_schema(card_options)
        
        # Test that the schema has the right constraints
        schema_dict = CardSelectionSchema.model_json_schema()
        print(f"Card selection schema enum: {schema_dict['properties']['selected_card']['enum']}")
        
        # Test multiple choice schema
        choices = ["Red", "Blue", "Green"]
        MultipleChoiceSchema = SchemaFactory.create_multiple_choice_schema(choices)
        schema_dict = MultipleChoiceSchema.model_json_schema()
        print(f"Multiple choice schema enum: {schema_dict['properties']['answer']['enum']}")
        
        # Test numeric range schema
        NumericRangeSchema = SchemaFactory.create_numeric_range_schema(0, 10)
        schema_dict = NumericRangeSchema.model_json_schema()
        print(f"Numeric range min: {schema_dict['properties']['value']['minimum']}")
        print(f"Numeric range max: {schema_dict['properties']['value']['maximum']}")
        
        print("Schema generation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing schema generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_registry():
    """Test schema registry"""
    print("\nTesting schema registry...")
    
    try:
        # Test that all expected schemas are registered
        expected_schemas = [
            "simple", "numeric", "boolean", "explanation", "card_selection",
            "multiple_card_selection", "combat_assignment", "mana_cost",
            "phase", "turn_step", "card_type", "zone", "priority", "draft_pick"
        ]
        
        for schema_name in expected_schemas:
            if schema_name in SCHEMA_REGISTRY:
                print(f"  ✓ {schema_name} schema found")
            else:
                print(f"  ✗ {schema_name} schema missing")
                return False
        
        print("Schema registry test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing schema registry: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_schema_generation()
    success2 = test_schema_registry()
    sys.exit(0 if (success1 and success2) else 1)