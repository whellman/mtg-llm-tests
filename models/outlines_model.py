from transformers import AutoTokenizer, AutoModelForCausalLM
from models.base_model import BaseModel
import outlines
import os
from typing import List, Union, Dict, Any, Optional
from dotenv import load_dotenv
from models.structured_schemas import SCHEMA_REGISTRY, SchemaFactory
import json
import re

# Load environment variables from .env file
load_dotenv()

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

    def run(self, prompt: str, output_type: str = "simple", **kwargs) -> str:
        """Run inference with structured output constraints"""
        
        # Handle dynamic schema creation for specific scenarios
        if output_type == "card_selection" and "options" in kwargs:
            schema = SchemaFactory.create_card_selection_schema(kwargs["options"])
            prompt_suffix = f"\\n\\nChoose exactly one card from these options: {', '.join(kwargs['options'])}. Answer with ONLY the card name."
        elif output_type == "multiple_choice" and "choices" in kwargs:
            schema = SchemaFactory.create_multiple_choice_schema(kwargs["choices"])
            prompt_suffix = f"\\n\\nChoose from these options: {', '.join(kwargs['choices'])}. Answer with ONLY the selected option."
        elif output_type == "numeric_range" and "min_val" in kwargs and "max_val" in kwargs:
            schema = SchemaFactory.create_numeric_range_schema(kwargs["min_val"], kwargs["max_val"])
            prompt_suffix = f"\\n\\nAnswer with a number between {kwargs['min_val']} and {kwargs['max_val']}. No explanation, just the number."
        elif output_type == "boolean":
            schema = SchemaFactory.create_boolean_schema()
            prompt_suffix = "\\n\\nAnswer with ONLY 'yes' or 'no'. No explanation, just the answer:"
        elif output_type in SCHEMA_REGISTRY:
            schema = SCHEMA_REGISTRY[output_type]
            prompt_suffixes = {
                "numeric": "\\n\\nAnswer with ONLY the number. No explanation, no JSON, just the number:",
                "explanation": "\\n\\nProvide a clear, concise explanation:",
                "boolean": "\\n\\nAnswer with ONLY 'true' or 'false'. No explanation, just the boolean value:",
                "simple": "\\n\\nAnswer with ONLY the answer. No explanation, no JSON, just the answer:",
                "card_selection": "\\n\\nAnswer with ONLY the card name. No explanation, just the card name:",
                "draft_pick": "\\n\\nAnswer with ONLY the card name you would pick. No explanation, just the card name:",
                "combat_assignment": "\\n\\nAnswer with the damage assignment number. No explanation, just the number:",
                "mana_cost": "\\n\\nAnswer with the mana cost in standard format (e.g., '2WW'). No explanation, just the cost:",
                "phase": "\\n\\nAnswer with the phase name. No explanation, just the phase:",
                "card_type": "\\n\\nAnswer with the card type. No explanation, just the type:",
                "zone": "\\n\\nAnswer with the zone name. No explanation, just the zone:",
            }
            prompt_suffix = prompt_suffixes.get(output_type, "\\n\\nAnswer appropriately. No explanation, just the answer:")
        else:
            # Fallback to simple answer
            schema = SCHEMA_REGISTRY["simple"]
            prompt_suffix = "\\n\\nAnswer with ONLY the answer. No explanation, no JSON, just the answer:"
        
        # Create generator with structured output
        generator = outlines.generator.Generator(self.outlines_model, schema)
        
        # Run generation
        full_prompt = prompt + prompt_suffix
        try:
            result = generator(full_prompt)
            return self._extract_answer(result, output_type)
        except Exception as e:
            # Fallback to unstructured generation if outlines fails
            print(f"Warning: Structured generation failed, falling back to unstructured: {e}")
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(**inputs, max_new_tokens=100)
            result_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract just the answer part
            answer_part = result_text[len(full_prompt):].strip()
            return self._extract_answer_from_text(answer_part, output_type)
    
    def _extract_answer(self, result: Any, output_type: str) -> str:
        """Extract answer from structured output result"""
        # Handle different schema fields
        if hasattr(result, 'answer'):
            answer_value = result.answer
            # Handle boolean conversion - now using "yes"/"no" literals
            if isinstance(answer_value, str) and answer_value in ["yes", "no"]:
                return answer_value
            elif isinstance(answer_value, str) and answer_value in ["true", "false"]:
                # Convert "true"/"false" to "yes"/"no"
                return "yes" if answer_value == "true" else "no"
            elif isinstance(answer_value, bool):
                # Convert boolean to "yes"/"no"
                return "yes" if answer_value else "no"
            return str(answer_value).strip()
        elif hasattr(result, 'value'):
            return str(result.value)
        elif hasattr(result, 'selected_card'):
            return str(result.selected_card).strip()
        elif hasattr(result, 'pick'):
            return str(result.pick).strip()
        elif hasattr(result, 'damage_assignment'):
            return str(result.damage_assignment)
        elif hasattr(result, 'mana_cost'):
            return str(result.mana_cost).strip()
        elif hasattr(result, 'phase'):
            return str(result.phase).strip()
        elif hasattr(result, 'card_type'):
            return str(result.card_type).strip()
        elif hasattr(result, 'zone'):
            return str(result.zone).strip()
        elif hasattr(result, 'explanation'):
            return str(result.explanation).strip()
        else:
            # Handle case where result might be a string representation
            result_str = str(result)
            return self._extract_answer_from_text(result_str, output_type)
    
    def _extract_answer_from_text(self, text: str, output_type: str) -> str:
        """Extract answer from raw text output"""
        text = text.strip()
        
        # Try to extract from JSON-like string if needed
        if text.startswith('{') and text.endswith('}'):
            try:
                result_dict = json.loads(text)
                # Try common field names
                for key in ['answer', 'value', 'selected_card', 'pick', 'damage_assignment', 'mana_cost', 'phase', 'card_type', 'zone', 'explanation']:
                    if key in result_dict:
                        return str(result_dict[key]).strip()
            except:
                pass
        
        # For numeric outputs, extract the first number
        if output_type in ["numeric", "combat_assignment", "numeric_range"]:
            numbers = re.findall(r'-?\\d+', text)
            if numbers:
                return numbers[0]
        
        # For boolean outputs, normalize
        if output_type == "boolean":
            text_lower = text.lower()
            if text_lower in ["true", "yes", "y", "1"]:
                return "true"
            elif text_lower in ["false", "no", "n", "0"]:
                return "false"
        
        return text
    
    def run_batch(self, prompts: List[str], output_types: List[str] = None, kwargs_list=None) -> List[str]:
        """Run batch inference with structured output constraints"""
        if output_types is None:
            output_types = ["simple"] * len(prompts)
        
        # Handle kwargs for each prompt
        if kwargs_list is None:
            kwargs_list = [{}] * len(prompts)
        elif len(kwargs_list) != len(prompts):
            kwargs_list = [kwargs_list[0] if kwargs_list else {}] * len(prompts)
        
        results = []
        for prompt, output_type, kwargs in zip(prompts, output_types, kwargs_list):
            result = self.run(prompt, output_type, **kwargs)
            results.append(result)
        
        return results