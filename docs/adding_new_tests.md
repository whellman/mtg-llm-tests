# Adding New Tests with Structured Output

When creating new test scenarios, you can now specify structured output requirements to improve reliability.

## Enhanced Scenario Format

```yaml
id: example_test_001
category: example
subcategory: example_type
description: "Test description"
prompt: "Your question here?"
expected_output: "Expected answer"
evaluator: exact|contains|semantic|numeric|boolean
# Optional: specify output type for structured generation
output_type: simple|numeric|explanation  # Optional, auto-detected if not specified
```

## Output Type Guidelines

- **simple**: For yes/no, true/false, single words (default for short expected outputs)
- **numeric**: For number answers (auto-detected for digit-only expected outputs)  
- **explanation**: For detailed textual explanations (default for longer expected outputs)
- **boolean**: For yes/no questions (auto-detected for yes/no expected outputs)

## Evaluator Selection

Choose the most appropriate evaluator:
- **exact**: Case-insensitive exact string match
- **contains**: Case-insensitive substring match
- **semantic**: Fuzzy similarity matching (80% threshold)
- **numeric**: Numeric value comparison
- **boolean**: Boolean value comparison (yes/no, true/false)

## Example Scenarios

### Simple Boolean
```yaml
id: card_types_001
category: rules
subcategory: card_types
description: "Test card type interactions"
prompt: "Can Dispel counter a Sorcery?"
expected_output: "no"
evaluator: boolean
output_type: simple
```

### Numeric Answer
```yaml
id: combat_math_001
category: combat
subcategory: combat_math
description: "Test combat damage calculation"
prompt: "How much damage do you take when blocking a 6/6 with a 3/3?"
expected_output: "3"
evaluator: numeric
output_type: numeric
```

### Detailed Explanation
```yaml
id: rules_explanation_001
category: rules
subcategory: explanations
description: "Test rule explanations"
prompt: "Explain how protection works in MTG"
expected_output: "Protection prevents damage, prevents targeting, prevents blocking, and prevents enchanting/equipping."
evaluator: semantic
output_type: explanation
```

These structured specifications help the testing framework generate and evaluate responses more reliably.