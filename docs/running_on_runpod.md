# Running MTG LLM Tests on RunPod GPU

## Prerequisites

1. **Hugging Face Token**: You'll need a Hugging Face account and API token
2. **GPU Instance**: RunPod instance with sufficient VRAM (16GB+ recommended)
3. **Python Environment**: Python 3.8+ with required dependencies

## Setup Instructions

### 1. Spin up RunPod Instance
- Choose a GPU instance (recommended: A100, RTX 3090, or similar)
- Select a container with Python 3.8+ and CUDA support
- Allocate at least 16GB VRAM for larger models

### 2. Clone the Repository
```bash
git clone <repository-url>
cd mtg-llm-tests
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file or export the Hugging Face token:
```bash
export HUGGINGFACE_HUB_TOKEN="your_hf_token_here"
```

Or create `.env` file:
```bash
echo "HUGGINGFACE_HUB_TOKEN=your_hf_token_here" > .env
```

## Running Tests

### Basic Usage

#### Run with Structured Output (Recommended)
```bash
python runner.py --structured --format detailed
```

#### Run with Regular Output
```bash
python runner.py --format detailed
```

### Advanced Options

#### Specify Model
```bash
python runner.py --structured --model "mistralai/Mistral-7B-Instruct-v0.3" --format detailed
```

#### Adjust Batch Size
```bash
python runner.py --structured --batch-size 8 --format detailed
```

#### JSON Output for Machine Processing
```bash
python runner.py --structured --format json
```

#### Simple Output Format
```bash
python runner.py --structured --format simple
```

### Example Commands

#### Quick Test Run
```bash
python runner.py --structured --model "facebook/opt-125m" --batch-size 2 --format detailed
```

#### Full Test Suite with Default Model
```bash
python runner.py --structured --batch-size 4 --format detailed
```

#### Production Run with Large Model
```bash
python runner.py --structured --model "mistralai/Mistral-7B-Instruct-v0.3" --batch-size 8 --format json > results.json
```

## Key Features When Using --structured

- **Card Selection Constraints**: Draft scenarios force exact card choices
- **Numeric Range Validation**: Combat math scenarios constrained to valid ranges
- **MTG-Specific Enums**: Phase, card type, and zone identification validated
- **Boolean Constraints**: Yes/no questions forced to true/false
- **Improved Reliability**: Eliminates invalid answer formats

## Monitoring and Troubleshooting

### Check GPU Usage
```bash
nvidia-smi
```

### Monitor Memory Usage
```bash
watch -n 1 nvidia-smi
```

### Common Issues

1. **Out of Memory**: Reduce batch size or use smaller model
2. **Token Issues**: Verify HUGGINGFACE_HUB_TOKEN is set correctly
3. **Model Loading**: Some models may require additional dependencies

### Performance Tips

- Use `--batch-size 4-8` for optimal GPU utilization
- Larger batch sizes for larger VRAM (8-16 for 24GB+)
- Smaller models like `opt-125m` for testing
- Monitor GPU memory to avoid OOM errors

## Output Formats

### Detailed Format
Shows comprehensive test results with prompts and outputs

### Simple Format  
Shows PASS/FAIL status only

### JSON Format
Machine-readable output for automated processing

## Example Output

```bash
python runner.py --structured --format detailed

combat_math_001: PASS
  Prompt: You are in a combat scenario where your opponent has a 6/6 creature with trample. If you block with a 3/3 creature, how much damage will you take?
  Expected: 3
  Actual: 3
  Similarity: 1.00

--- SUMMARY ---
Total tests: 64
Passed: 64
Failed: 0
Pass rate: 100.00%
Total time: 125.45 seconds
Model: mistralai/Mistral-7B-Instruct-v0.3
```