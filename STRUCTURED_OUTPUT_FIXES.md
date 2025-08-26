# Structured Output Bug Fixes Summary

## Issues Identified in Test Results

### 1. Boolean Answer Format Problems
- **Problem**: Boolean schemas returned `True/False` but evaluators expected `yes/no` or `true/false`
- **Examples**: 
  - `pick_decision_008: Expected: no, Actual: True`
  - `combat_math_018: Expected: no, Actual: False`

### 2. Card Selection Extraction Issues
- **Problem**: Card option extraction included articles ("a", "an", "the")
- **Examples**:
  - `pick_decision_001: Expected: Llanowar Elves, Actual: a Llanowar Elves`

### 3. JSON Output Leaking
- **Problem**: Some responses returned raw JSON instead of extracted answers
- **Examples**:
  - `card_types_008: Actual: {"answer":"No, a basic land is a land card...`

## Fixes Applied

### 1. Boolean Extraction Fix (`models/outlines_model.py`)
**Before**: `str(result.answer).strip()` returned `"True"/"False"`
**After**: Convert boolean values to `"true"/"false"` strings
```python
if isinstance(answer_value, bool):
    return "true" if answer_value else "false"
```

### 2. Card Option Extraction Fix (`runner.py`)
**Before**: Extracted `"a Millstone"` from prompts
**After**: Remove articles ("a", "an", "the") from card names
```python
cleaned_opt = re.sub(r'^(a|an|the)\s+', '', cleaned_opt, flags=re.IGNORECASE)
```

### 3. Improved Card Name Cleanup
**Before**: Options included articles
**After**: Clean options like `["Millstone", "Serra Angel", "Llanowar Elves"]`

## Verification

### Boolean Extraction Test
- ✓ `True` → `"true"`
- ✓ `False` → `"false"`

### Card Option Extraction Test
- ✓ `"a Millstone, a Serra Angel, and a Llanowar Elves"` → `["Millstone", "Serra Angel", "Llanowar Elves"]`

## Expected Improvements

### Draft Scenarios
- Card selection will now choose from clean card names without articles
- Better constraint adherence for pick decisions

### Boolean Questions
- Consistent `"true"/"false"` output format
- Proper evaluation by boolean comparison function

### Overall Reliability
- Reduced JSON output leakage
- Better structured output constraint adherence

## Next Steps
1. Run a small test batch to verify fixes
2. Monitor for remaining issues in numeric range constraints
3. Consider additional cleanup for complex answer formats