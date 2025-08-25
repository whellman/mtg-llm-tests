from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
from typing import List, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class HFTransformerModel:
    def __init__(self, model_name: str):
        hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        if not hf_token:
            raise RuntimeError("Missing HUGGINGFACE_HUB_TOKEN environment variable")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto", use_auth_token=hf_token)

        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=100,
            temperature=0.7,
            return_full_text=False,
        )

    def run(self, prompt: str) -> str:
        """Run inference on a single prompt"""
        result = self.pipeline(prompt)
        return result[0]["generated_text"].strip()
    
    def run_batch(self, prompts: List[str]) -> List[str]:
        """Run batch inference on multiple prompts"""
        results = self.pipeline(prompts)
        return [result[0]["generated_text"].strip() for result in results]
