import difflib
import re

def exact(output, expected):
    return output.strip().lower() == expected.strip().lower()

def contains(output, expected):
    return expected.strip().lower() in output.strip().lower()

def semantic(output, expected):
    # Simple fuzzy matching using SequenceMatcher
    # FIXME: This is a placeholder for a more sophisticated semantic evaluation
    ratio = difflib.SequenceMatcher(None, output.strip().lower(), expected.strip().lower()).ratio()
    return ratio > 0.8  # Consider "semantic match" if similarity > 80%

def numeric_comparison(output, expected):
    """Compare numeric values, handling various formats"""
    # Extract numbers from both strings
    output_nums = re.findall(r'-?\d+', output)
    expected_nums = re.findall(r'-?\d+', expected)
    
    if not output_nums or not expected_nums:
        return False
    
    try:
        return int(output_nums[0]) == int(expected_nums[0])
    except ValueError:
        return False

def boolean_comparison(output, expected):
    """Handle yes/no, true/false comparisons"""
    output_clean = output.strip().lower()
    expected_clean = expected.strip().lower()
    
    # Normalize boolean values
    yes_values = {"yes", "true", "y", "1"}
    no_values = {"no", "false", "n", "0"}
    
    output_bool = True if output_clean in yes_values else False if output_clean in no_values else None
    expected_bool = True if expected_clean in yes_values else False if expected_clean in no_values else None
    
    if output_bool is None or expected_bool is None:
        return output_clean == expected_clean
    
    return output_bool == expected_bool

def get_evaluator(name):
    evaluators = {
        "exact": exact,
        "contains": contains,
        "semantic": semantic,
        "numeric": numeric_comparison,
        "boolean": boolean_comparison
    }
    return evaluators.get(name, exact)
