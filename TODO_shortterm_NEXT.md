Structured output overhaul. We don't need to worry about any other model methodology for now if we can get our HF tranformers to reliably work with structured output.

Evaluators need to be updated, either before structured overhaul (an easy bandaid is case-insensitivity) or after (at which point the whole way tests are evaluated will probably need to be adjusted or overhauled, to deal with output structure--do we define this somehow in the yaml of the test, or do we robustly support a handful of explicitly-known structures?).

✓ Added OutlinesModel wrapper for structured output generation
✓ Updated evaluators with case-insensitive comparison and specialized evaluators (numeric, boolean)
✓ Modified runner to support --structured flag
✓ Created documentation for structured output usage
✓ Updated some scenario files to use better evaluators

Next steps:
- Test the structured output implementation with actual models
- Update more scenario files to use appropriate evaluators
- Consider adding output type specification directly in scenario YAML files