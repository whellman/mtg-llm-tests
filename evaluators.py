import difflib

def exact(output, expected):
    return output.strip() == expected.strip()

def contains(output, expected):
    return expected.strip() in output.strip()

def semantic(output, expected):
    # Simple fuzzy matching using SequenceMatcher
    # FIXME: This is a placeholder for a more sophisticated semantic evaluation
    ratio = difflib.SequenceMatcher(None, output.strip(), expected.strip()).ratio()
    return ratio > 0.8  # Consider "semantic match" if similarity > 80%

def get_evaluator(name):
    return {"exact": exact, "contains": contains, "semantic": semantic}[name]
