#!/usr/bin/env python3
"""
Runner script for MTG LLM tests with machine-compilable output options.
"""

from models.hf_transformer import HFTransformerModel
from models.outlines_model import OutlinesModel
from evaluators import get_evaluator
import yaml
import glob
import json
import argparse
import time
import sys
from torch.utils.data import DataLoader, Dataset
import torch
import difflib

class ScenarioDataset(Dataset):
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def __len__(self):
        return len(self.scenarios)

    def __getitem__(self, idx):
        return self.scenarios[idx]

def collate_fn(batch):
    return batch

def calculate_similarity(output, expected):
    """Calculate similarity ratio between output and expected text."""
    return difflib.SequenceMatcher(None, output.strip(), expected.strip()).ratio()

def run_tests(model_name="mistralai/Mistral-7B-Instruct-v0.3", output_format="simple", batch_size=4, use_structured=False):
    """Run all tests and output results in specified format."""
    
    start_time = time.time()
    
    # Initialize model
    if use_structured:
        model = OutlinesModel(model_name)
    else:
        model = HFTransformerModel(model_name)
    
    # Collect all scenarios
    scenarios = []
    for file in glob.glob("scenarios/**/*.yaml", recursive=True):
        with open(file) as f:
            scenario = yaml.safe_load(f)
        scenarios.append(scenario)

    # Create dataset and dataloader
    dataset = ScenarioDataset(scenarios)
    dataloader = DataLoader(dataset, batch_size=batch_size, collate_fn=collate_fn)

    # Store results for machine output
    results = []
    passed = 0
    total = 0

    # Process scenarios in batches
    for batch in dataloader:
        # Extract prompts and output types from the batch
        prompts = [scenario["prompt"] for scenario in batch]
        output_types = []
        for scenario in batch:
            # Determine output type based on expected output characteristics
            expected = scenario["expected_output"].strip().lower()
            if expected in ["yes", "no"] or len(expected) <= 10:
                output_types.append("simple")
            elif expected.isdigit():
                output_types.append("numeric")
            else:
                output_types.append("explanation")
        
        # Run batch inference
        batch_start = time.time()
        if use_structured:
            outputs = model.run_batch(prompts, output_types)
        else:
            outputs = model.run_batch(prompts)
        batch_time = time.time() - batch_start
        
        # Evaluate each result
        for scenario, output in zip(batch, outputs):
            evaluator = get_evaluator(scenario["evaluator"])
            result = evaluator(output, scenario["expected_output"])
            
            # Calculate similarity for all cases
            similarity = calculate_similarity(output, scenario["expected_output"])
            
            total += 1
            if result:
                passed += 1
            
            test_result = {
                "id": scenario["id"],
                "category": scenario.get("category", "unknown"),
                "subcategory": scenario.get("subcategory", "unknown"),
                "prompt": scenario["prompt"],
                "expected_output": scenario["expected_output"],
                "actual_output": output,
                "evaluator": scenario["evaluator"],
                "passed": bool(result),
                "similarity": similarity,
                "batch_time": batch_time / len(prompts) if len(prompts) > 0 else 0
            }
            
            results.append(test_result)
            
            if output_format == "simple":
                print(f"{scenario['id']}: {'PASS' if result else 'FAIL'}")
            elif output_format == "detailed":
                print(f"{scenario['id']}: {'PASS' if result else 'FAIL'}")
                print(f"  Prompt: {scenario['prompt']}")
                print(f"  Expected: {scenario['expected_output']}")
                print(f"  Actual: {output}")
                print(f"  Similarity: {similarity:.2f}")
                print()

    # Summary statistics
    total_time = time.time() - start_time
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    if output_format == "json":
        # Machine-compilable JSON output
        summary = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": pass_rate,
                "total_time_seconds": total_time,
                "model_name": model_name
            },
            "results": results
        }
        json.dump(summary, sys.stdout, indent=2)
    elif output_format in ["simple", "detailed"]:
        print(f"\n--- SUMMARY ---")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Pass rate: {pass_rate:.2f}%")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Model: {model_name}")
    
    return results, passed, total

def main():
    parser = argparse.ArgumentParser(description="Run MTG LLM tests")
    parser.add_argument("--format", choices=["simple", "detailed", "json"], 
                        default="simple", help="Output format")
    parser.add_argument("--model", default="mistralai/Mistral-7B-Instruct-v0.3",
                        help="Model name to use")
    parser.add_argument("--batch-size", type=int, default=4,
                        help="Batch size for inference")
    parser.add_argument("--structured", action="store_true",
                        help="Use structured output generation with outlines")
    
    args = parser.parse_args()
    
    try:
        results, passed, total = run_tests(
            model_name=args.model,
            output_format=args.format,
            batch_size=args.batch_size,
            use_structured=args.structured
        )
        
        if passed < total:
            sys.exit(1)  # Exit with error code if any tests failed
        else:
            sys.exit(0)  # Exit successfully if all tests passed
            
    except Exception as e:
        print(f"Error running tests: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
