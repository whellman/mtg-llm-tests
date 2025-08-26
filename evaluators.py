import difflib
import re
import json

def _clean_response(response):
    """Clean response to extract actual answer from JSON if needed"""
    response = response.strip()
    # If it looks like JSON, try to extract the answer
    if response.startswith('{') and response.endswith('}'):
        try:
            data = json.loads(response)
            # Try common JSON field names
            for key in ['answer', 'value', 'explanation']:
                if key in data:
                    return str(data[key])
        except:
            pass
    return response

def exact(output, expected):
    # Clean the output to handle JSON responses
    clean_output = _clean_response(output)
    return clean_output.strip().lower() == expected.strip().lower()

def contains(output, expected):
    # Clean the output to handle JSON responses
    clean_output = _clean_response(output)
    return expected.strip().lower() in clean_output.strip().lower()

def _clean_response(response):
    """Clean response to extract actual answer from JSON if needed"""
    response = response.strip()
    # If it looks like JSON, try to extract the answer
    if response.startswith('{') and response.endswith('}'):
        try:
            import json
            data = json.loads(response)
            # Try common JSON field names
            for key in ['answer', 'value', 'explanation']:
                if key in data:
                    return str(data[key])
        except:
            pass
    return response

def semantic(output, expected):
    # Simple fuzzy matching using SequenceMatcher
    # FIXME: This is a placeholder for a more sophisticated semantic evaluation
    clean_output = _clean_response(output)
    ratio = difflib.SequenceMatcher(None, clean_output.strip().lower(), expected.strip().lower()).ratio()
    return ratio > 0.8  # Consider "semantic match" if similarity > 80%

def numeric_comparison(output, expected):
    """Compare numeric values, handling various formats"""
    # Clean the output to handle JSON responses
    clean_output = _clean_response(output)
    
    # Extract numbers from both strings
    output_nums = re.findall(r'-?\d+', clean_output)
    expected_nums = re.findall(r'-?\d+', expected)
    
    if not output_nums or not expected_nums:
        return False
    
    try:
        return int(output_nums[0]) == int(expected_nums[0])
    except ValueError:
        return False

def boolean_comparison(output, expected):
    """Handle yes/no, true/false comparisons"""
    # Clean the output to handle JSON responses
    clean_output = _clean_response(output)
    output_clean = clean_output.strip().lower()
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
