#!/usr/bin/env python3
"""
Script to fix draft scenarios to use card_selection output type
"""

import yaml
from pathlib import Path

def fix_draft_scenarios():
    """Fix draft scenarios to use card_selection output type"""
    
    draft_dir = Path('/home/wes/Development/Clineified/mtg-llm-tests/scenarios/draft')
    draft_files = list(draft_dir.glob('*.yaml'))
    
    updated_count = 0
    
    for draft_file in draft_files:
        if '_structured' in draft_file.name:
            continue
            
        try:
            # Read the file
            with open(draft_file, 'r') as f:
                content = f.read()
            
            # Check if it contains card choices and is currently simple/boolean
            if ('choice between' in content or 'choice of' in content) and ('output_type: simple' in content or 'output_type: boolean' in content):
                # Replace with card_selection
                if 'output_type: simple' in content:
                    updated_content = content.replace('output_type: simple', 'output_type: card_selection')
                else:
                    updated_content = content.replace('output_type: boolean', 'output_type: card_selection')
                
                # Write back
                with open(draft_file, 'w') as f:
                    f.write(updated_content)
                
                print("  🔄 Fixed draft scenario: {} -> card_selection".format(draft_file.name))
                updated_count += 1
            
        except Exception as e:
            print("  ❌ Error fixing {}: {}".format(draft_file.name, e))
    
    print("Fixed {} draft scenarios".format(updated_count))

if __name__ == "__main__":
    print("Fixing draft scenarios for card selection...")
    fix_draft_scenarios()