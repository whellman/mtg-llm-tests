# runner.py
from models.hf_transformer import HFTransformerModel
from evaluators import get_evaluator
import yaml, glob

model_name = "meta-llama/Llama-2-7b-chat-hf"
model = HFTransformerModel(model_name)
for file in glob.glob("scenarios/**/*.yaml", recursive=True):
    with open(file) as f:
        scenario = yaml.safe_load(f)
    output = model.run(scenario["prompt"])
    evaluator = get_evaluator(scenario["evaluator"])
    result = evaluator(output, scenario["expected_output"])
    print(f"{scenario['id']}: {'PASS' if result else 'FAIL'}")
