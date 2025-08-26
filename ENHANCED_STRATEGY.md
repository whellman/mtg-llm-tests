# Enhanced Structured Output Strategy

## Current Status
Pass rate: 37.5% (24/64) - significant improvement from previous iterations

## Key Issues Identified
1. **"It depends" responses** - LLMs providing nuanced answers instead of definitive choices
2. **Inconsistent boolean handling** - Some scenarios still failing
3. **Draft pick confusion** - Models sometimes choosing wrong cards despite constraints
4. **Complex rule questions** - MTG-specific knowledge gaps causing errors

## Implemented Solutions

### 1. System Prompt / Role Setting
Added strong system prompt establishing testing context:
```
You are a Magic: The Gathering expert AI evaluator. You are taking a test about MTG rules, strategy, and gameplay.

IMPORTANT INSTRUCTIONS:
- Answer each question with a SINGLE, DEFINITIVE response
- Do not say "it depends," "both," or provide nuanced explanations
- Choose ONE clear answer from the available options
- For draft picks, choose exactly one card from the provided list
- For yes/no questions, answer ONLY "yes" or "no"
- For numeric questions, provide ONLY the number
- Follow the specific format requested for each question type
```

### 2. Enhanced Prompt Engineering
- Clearer instructions for each output type
- Explicit "NO EXPLANATIONS" directives
- Stronger constraint language ("EXACTLY ONE", "ONLY")
- Reduced ambiguity in question framing

### 3. Stricter Multiple-Choice Constraints
Updated scenarios to use explicit multiple-choice format:
- `output_type: multiple_choice` with `choices: [...]`
- `evaluator: exact` for precise matching
- Literal validation through Outlines schemas

### 4. Improved Error Handling
- Better fallback mechanisms
- Enhanced answer extraction logic
- More robust boolean normalization

## Next Steps for Further Improvement

### 1. Expand Multiple-Choice Coverage
Convert more ambiguous scenarios to explicit multiple-choice format:
- Draft pick decisions → card selection with exact options
- Strategic questions → predefined answer choices
- Rule interpretations → specific MTG terminology options

### 2. Enhance Combat Math Constraints
- Add more specific numeric ranges
- Implement MTG-specific value validations
- Create combat scenario templates

### 3. Refine MTG Knowledge Base
- Add reference materials for complex rules
- Create scenario-specific context priming
- Implement rule lookup capabilities

### 4. Advanced Outlines Features
Explore additional Outlines capabilities:
- Regular expression constraints for specific formats
- Context-free grammars for complex structures
- Function calling for structured data extraction

## Expected Impact
These enhancements should address the core issues:
- Eliminate "it depends" responses through role setting
- Improve constraint enforcement with multiple-choice format
- Increase pass rates through better prompt engineering
- Reduce ambiguity through systematic question structuring

## Monitoring Strategy
- Track pass rate improvements
- Monitor specific failure patterns
- Identify remaining edge cases
- Measure constraint effectiveness