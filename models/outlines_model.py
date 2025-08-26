from transformers import AutoTokenizer, AutoModelForCausalLM
from models.base_model import BaseModel
import outlines
import os
from typing import List, Union
from dotenv import load_dotenv
from pydantic import BaseModel as PydanticBaseModel

# Load environment variables from .env file
load_dotenv()

class SimpleAnswer(PydanticBaseModel):
    """Simple yes/no or short answer"""
    answer: str

class NumericAnswer(PydanticBaseModel):
    """Numeric answer"""
    value: int

class ExplanationAnswer(PydanticBaseModel):
    """Detailed explanation"""
    explanation: str

class OutlinesModel(BaseModel):
    def __init__(self, model_name: str):
        hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        if not hf_token:
            raise RuntimeError("Missing HUGGINGFACE_HUB_TOKEN environment variable")

        # Load the base model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            torch_dtype="auto", 
            device_map="auto", 
            use_auth_token=hf_token
        )
        
        # Create outlines model wrapper
        self.outlines_model = outlines.from_transformers(self.model, self.tokenizer)

    def run(self, prompt: str, output_type: str = "simple") -> str:
        """Run inference with structured output constraints"""
        
        # Define output schema based on expected type
        if output_type == "numeric":
            schema = NumericAnswer
            prompt_suffix = "\n\nAnswer with ONLY the number. No explanation, no JSON, just the number:"
        elif output_type == "explanation":
            schema = ExplanationAnswer
            prompt_suffix = "\n\nProvide a clear, concise explanation:"
        else:  # simple/default
            schema = SimpleAnswer
            prompt_suffix = "\n\nAnswer with ONLY the answer. No explanation, no JSON, just the answer:"
        
        # Create generator with structured output
        generator = outlines.generator.Generator(self.outlines_model, schema)
        
        # Run generation
        full_prompt = prompt + prompt_suffix
        result = generator(full_prompt)
        
        # Extract the answer based on schema
        if hasattr(result, 'answer'):
            return result.answer.strip()
        elif hasattr(result, 'value'):
            return str(result.value)
        elif hasattr(result, 'explanation'):
            return result.explanation.strip()
        else:
            # Handle case where result might be a string representation
            result_str = str(result)
            # Try to extract from JSON-like string if needed
            if result_str.startswith('{') and result_str.endswith('}'):
                import json
                try:
                    result_dict = json.loads(result_str)
                    if 'answer' in result_dict:
                        return str(result_dict['answer']).strip()
                    elif 'value' in result_dict:
                        return str(result_dict['value'])
                except:
                    pass
            return result_str.strip()
    
    def run_batch(self, prompts: List[str], output_types: List[str] = None) -> List[str]:
        """Run batch inference with structured output constraints"""
        if output_types is None:
            output_types = ["simple"] * len(prompts)
        
        results = []
        for prompt, output_type in zip(prompts, output_types):
            result = self.run(prompt, output_type)
            results.append(result)
        
        return results