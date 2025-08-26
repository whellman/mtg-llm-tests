#!/usr/bin/env python3
"""
Script to verify and summarize structured output types across all scenarios
"""

import yaml
from pathlib import Path
from collections import Counter

def analyze_scenarios():
    """Analyze all scenarios and summarize structured output types"""
    
    scenario_dir = Path('/home/wes/Development/Clineified/mtg-llm-tests/scenarios')
    yaml_files = list(scenario_dir.glob('**/*.yaml'))
    
    output_types = Counter()
    category_subcategory_types = {}
    
    print("Analyzing structured output types across all scenarios...")
    print("=" * 60)
    
    for yaml_file in yaml_files:
        if '_structured' in yaml_file.name:
            continue
            
        try:
            with open(yaml_file, 'r') as f:
                scenario_data = yaml.safe_load(f)
            
            output_type = scenario_data.get('output_type', 'unknown')
            category = scenario_data.get('category', 'unknown')
            subcategory = scenario_data.get('subcategory', 'unknown')
            
            output_types[output_type] += 1
            
            # Track by category/subcategory
            cat_sub = f"{category}/{subcategory}"
            if cat_sub not in category_subcategory_types:
                category_subcategory_types[cat_sub] = Counter()
            category_subcategory_types[cat_sub][output_type] += 1
            
        except Exception as e:
            print("Error reading {}: {}".format(yaml_file, e))
    
    print("OUTPUT TYPE DISTRIBUTION:")
    print("-" * 30)
    for output_type, count in output_types.most_common():
        print("  {:<20} {:>3}".format(output_type + ":", count))
    
    print("\nCATEGORY/SUBCATEGORY BREAKDOWN:")
    print("-" * 40)
    for cat_sub, types in sorted(category_subcategory_types.items()):
        print("  {}".format(cat_sub))
        for output_type, count in types.most_common():
            print("    {:<18} {:>2}".format(output_type + ":", count))
        print()
    
    print("SUMMARY:")
    print("-" * 20)
    print("  Total scenarios: {}".format(sum(output_types.values())))
    print("  Unique output types: {}".format(len(output_types)))
    print("  Files processed: {}".format(len(yaml_files)))

if __name__ == "__main__":
    analyze_scenarios()