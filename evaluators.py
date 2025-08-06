def exact(output, expected):
    return output.strip() == expected.strip()

def semantic(output, expected):
    # Use embeddings or fuzzy matching
    ...

def get_evaluator(name):
    return {"exact": exact, "semantic": semantic}[name]

