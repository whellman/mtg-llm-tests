# runner.py
from models.openai_model import OpenAIModel
from evaluators import get_evaluator
import yaml, glob

model = OpenAIModel()
for file in glob.glob("scenarios/**/*.yaml", recursive=True):
    with open(file) as f:
        scenario = yaml.safe_load(f)
    output = model.run(scenario["prompt"])
    evaluator = get_evaluator(scenario["evaluator"])
    result = evaluator(output, scenario["expected_output"])
    print(f"{scenario['id']}: {'PASS' if result else 'FAIL'}")

