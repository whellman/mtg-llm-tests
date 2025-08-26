Structured output overhaul. We don't need to worry about any other model methodology for now if we can get our HF tranformers to reliably work with structured output.

Evaluators need to be updated, either before structured overhaul (an easy bandaid is case-insensitivity) or after (at which point the whole way tests are evaluated will probably need to be adjusted or overhauled, to deal with output structure--do we define this somehow in the yaml of the test, or do we robustly support a handful of explicitly-known structures?).

✓ Added OutlinesModel wrapper for structured output generation
✓ Updated evaluators with case-insensitive comparison and specialized evaluators (numeric, boolean)
✓ Modified runner to support --structured flag
✓ Created documentation for structured output usage
✓ Updated some scenario files to use better evaluators
✓ Implemented comprehensive structured schemas for MTG-specific scenarios
✓ Added dynamic schema generation with card selection constraints
✓ Enhanced runner with auto-detection of output types
✓ Created enhanced documentation with MTG-specific examples
✓ Added comprehensive test scenarios demonstrating new capabilities

**COMPLETED: Full structured output overhaul with MTG-specific constraints**

The structured output system now provides comprehensive constraints for MTG testing:
- Dynamic schema generation for card selection from exact options
- MTG-specific schemas (phases, card types, zones, combat math)
- Auto-detection of scenario types and appropriate constraints
- Range constraints for numeric answers
- Enum validation for categorical answers
- Backward compatibility with existing scenarios

Next steps:
- Test the enhanced structured output with actual models on GPU instances
- Convert more existing scenario files to use structured output
- Add more MTG-specific schema types as needed
- Monitor test reliability improvements