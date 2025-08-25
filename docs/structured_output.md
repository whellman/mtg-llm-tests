# Structured Output with Outlines

This document explains how to use structured output generation with the Outlines library to improve test reliability.

## Overview

Many LLM failures in MTG testing are due to poor output structure rather than incorrect reasoning. By using Outlines to constrain model outputs to specific formats, we can reduce these structural failures and get more reliable test results.

## How It Works

The `OutlinesModel` class wraps existing Hugging Face transformers and uses Outlines to constrain outputs to specific schemas:

- **Simple answers**: Yes/no, short responses
- **Numeric answers**: Single numbers
- **Explanations**: Detailed textual explanations

## Usage

To run tests with structured output:

```bash
python runner.py --structured --format detailed
```

## Benefits

1. **Reduced structural failures**: Models are forced to output in expected formats
2. **More reliable evaluation**: Evaluator functions can be more precise
3. **Better batch processing**: Consistent output formats enable better batch handling

## Schema Definitions

The system automatically detects appropriate output schemas based on expected outputs:
- Single words like "yes"/"no" → Simple schema
- Numbers → Numeric schema  
- Longer text → Explanation schema

## Custom Schemas

You can define custom Pydantic models in `models/outlines_model.py` for more complex structured outputs.