#!/usr/bin/env python3
"""
Script to automatically update all scenario files with structured output types
"""

import yaml
import re
from pathlib import Path

def extract_card_options(prompt):
    """Extract card options from draft pick prompts"""
    # Look for patterns like "between X, Y, and Z" or "choose from X, Y, Z"
    options_match = re.search(r'(?:between|from|choice between|choice of|options:?)\\s+([^.?]+)', prompt, re.IGNORECASE)
    if options_match:
        options_text = options_match.group(1)
        # Split by commas and clean up
        options = []
        for opt in re.split(r',\\s*(?:and\\s+)?', options_text):
            cleaned_opt = opt.strip()
            # Remove quotes
            if cleaned_opt.startswith('"') and cleaned_opt.endswith('"'):
                cleaned_opt = cleaned_opt[1:-1]
            elif cleaned_opt.startswith("'") and cleaned_opt.endswith("'"):
                cleaned_opt = cleaned_opt[1:-1]
            if cleaned_opt:
                options.append(cleaned_opt)
        return options
    return []

def determine_output_type_and_params(scenario_data):
    """Determine appropriate output type and parameters for a scenario"""
    
    category = scenario_data.get('category', '')
    subcategory = scenario_data.get('subcategory', '')
    expected_output = scenario_data.get('expected_output', '').strip()
    prompt = scenario_data.get('prompt', '')
    
    # Draft pick scenarios - card selection
    if category == 'draft' and subcategory == 'pick_decision':
        options = extract_card_options(prompt)
        if options:
            return 'card_selection', {}
    
    # Combat math scenarios - numeric with ranges
    if category == 'combat' and subcategory == 'combat_math':
        # Extract numbers from expected output to set reasonable range
        numbers = re.findall(r'\\d+', expected_output)
        if numbers:
            expected_num = int(numbers[0])
            min_val = 0
            max_val = max(20, expected_num + 10)  # Reasonable upper bound
            return 'numeric_range', {'min_val': min_val, 'max_val': max_val}
    
    # Boolean questions
    expected_lower = expected_output.lower()
    if expected_lower in ['yes', 'no', 'true', 'false', 'y', 'n']:
        return 'boolean', {}
    
    # Numeric answers
    if expected_output.isdigit() or (expected_output.startswith('-') and expected_output[1:].isdigit()):
        return 'numeric', {}
    
    # Card type identification - multiple choice
    if category == 'rules' and subcategory == 'card_types' and 'type' in prompt.lower():
        return 'card_type', {}
    
    # Phase identification
    if category == 'rules' and 'phase' in subcategory:
        return 'phase', {}
    
    # Mana cost scenarios
    if category == 'rules' and subcategory == 'mana_costs':
        return 'mana_cost', {}
    
    # Simple short answers
    if len(expected_output) <= 20:
        return 'simple', {}
    
    # Default to explanation for longer answers
    return 'explanation', {}

def update_scenario_file(file_path):
    """Update a single scenario file with structured output type"""
    
    try:
        # Read the existing file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if already has output_type
        if 'output_type:' in content:
            print("  ✓ Already has output_type: {}".format(file_path))
            return False
        
        # Parse YAML data safely
        try:
            scenario_data = yaml.safe_load(content)
        except Exception as e:
            print("  ⚠️  YAML parse warning for {}: {}".format(file_path, e))
            # Try to parse basic fields manually
            scenario_data = {}
            for line in content.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    scenario_data[key] = value
        
        # Determine output type and parameters
        output_type, params = determine_output_type_and_params(scenario_data)
        
        # Add output_type to the content
        if 'evaluator:' in content:
            # Insert before evaluator line
            lines = content.strip().split('\n')
            new_lines = []
            for line in lines:
                if line.strip().startswith('evaluator:'):
                    # Insert output_type line before evaluator
                    new_lines.append("output_type: {}".format(output_type))
                    # Add parameters if needed
                    for key, value in params.items():
                        if isinstance(value, str):
                            new_lines.append('{}: "{}"'.format(key, value))
                        else:
                            new_lines.append("{}: {}".format(key, value))
                new_lines.append(line)
            updated_content = '\n'.join(new_lines) + '\n'
        else:
            # Append at the end
            updated_content = content.rstrip() + '\noutput_type: {}\n'.format(output_type)
            # Add parameters if needed
            for key, value in params.items():
                if isinstance(value, str):
                    updated_content += '{}: "{}"\n'.format(key, value)
                else:
                    updated_content += "{}: {}\n".format(key, value)
        
        # Write updated content
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("  🔄 Updated: {} -> {}".format(file_path, output_type))
        return True
        
    except Exception as e:
        print("  ❌ Error updating {}: {}".format(file_path, e))
        return False

def main():
    """Main function to update all scenario files"""
    
    print("Updating all scenario files with structured output types...")
    print("=" * 60)
    
    # Find all scenario files
    scenario_dir = Path('/home/wes/Development/Clineified/mtg-llm-tests/scenarios')
    yaml_files = list(scenario_dir.glob('**/*.yaml'))
    
    updated_count = 0
    skipped_count = 0
    
    for yaml_file in yaml_files:
        # Skip the structured test files we already created
        if '_structured' in yaml_file.name:
            print("  → Skipping structured test file: {}".format(yaml_file))
            skipped_count += 1
            continue
            
        if update_scenario_file(yaml_file):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("=" * 60)
    print("Summary:")
    print("  Updated: {} files".format(updated_count))
    print("  Skipped: {} files".format(skipped_count))
    print("Total: {} files processed".format(len(yaml_files)))

if __name__ == "__main__":
    main()