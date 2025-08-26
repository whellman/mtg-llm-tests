# Adding New Tests with Structured Output

When creating new test scenarios, you can now specify structured output requirements to improve reliability and constrain model outputs to specific formats.

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
output_type: simple|numeric|explanation|boolean|card_selection|multiple_choice|combat_assignment|mana_cost|phase|card_type|zone  # Optional, auto-detected if not specified
# Optional: additional parameters for dynamic schema generation
choices: ["option1", "option2", "option3"]  # For multiple_choice
min_val: 0  # For numeric_range
max_val: 100  # For numeric_range
```

## Output Type Guidelines

### Basic Types
- **simple**: For yes/no, true/false, single words (default for short expected outputs)
- **numeric**: For number answers (auto-detected for digit-only expected outputs)  
- **explanation**: For detailed textual explanations (default for longer expected outputs)
- **boolean**: For yes/no questions (auto-detected for yes/no expected outputs)

### MTG-Specific Types
- **card_selection**: Forces selection from specific card options (auto-detected for draft scenarios)
- **multiple_choice**: Forces selection from provided choices
- **combat_assignment**: Numeric output for combat damage assignment
- **mana_cost**: MTG mana cost format (e.g., "2WW", "3B")
- **phase**: MTG game phase names
- **card_type**: MTG card types
- **zone**: MTG game zones
- **numeric_range**: Numeric output constrained to a specific range

### Dynamic Schema Types
- **numeric_range**: Specify `min_val` and `max_val` for constrained numeric output
- **multiple_choice**: Specify `choices` list for constrained selection
- **card_selection**: Options extracted automatically from draft prompts, or specify `options`

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
output_type: boolean
```

### Numeric Answer with Range Constraint
```yaml
id: combat_math_001
category: combat
subcategory: combat_math
description: "Test combat damage calculation with range constraint"
prompt: "How much damage do you take when blocking a 6/6 with a 3/3?"
expected_output: "3"
evaluator: numeric
output_type: numeric_range
min_val: 0
max_val: 6
```

### Card Selection (Draft Pick)
```yaml
id: draft_pick_001
category: draft
subcategory: pick_decision
description: "Test draft pick with card selection constraint"
prompt: "In a green/white draft, choose the best card from Millstone, Serra Angel, and Llanowar Elves."
expected_output: "Llanowar Elves"
evaluator: exact
output_type: card_selection
```

### Multiple Choice Question
```yaml
id: card_types_002
category: rules
subcategory: card_types
description: "Test card type identification with multiple choice"
prompt: "What type of card is Serra Angel?"
expected_output: "creature"
evaluator: exact
output_type: multiple_choice
choices: ["creature", "instant", "sorcery", "enchantment", "artifact", "land", "planeswalker"]
```

### MTG Phase Identification
```yaml
id: phase_id_001
category: rules
subcategory: phases
description: "Test phase identification"
prompt: "During which phase do you untap your permanents?"
expected_output: "untap"
evaluator: exact
output_type: phase
```

### MTG Card Type Identification
```yaml
id: card_type_id_001
category: rules
subcategory: card_types
description: "Test card type identification"
prompt: "What type of card is Lightning Bolt?"
expected_output: "instant"
evaluator: exact
output_type: card_type
```

These structured specifications help the testing framework generate and evaluate responses more reliably by constraining the model's output to specific formats and valid options.