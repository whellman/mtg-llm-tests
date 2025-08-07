# runner.py
from models.hf_transformer import HFTransformerModel
from evaluators import get_evaluator
import yaml
import glob
from torch.utils.data import DataLoader, Dataset
import torch

class ScenarioDataset(Dataset):
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def __len__(self):
        return len(self.scenarios)

    def __getitem__(self, idx):
        return self.scenarios[idx]

def collate_fn(batch):
    return batch

model_name = "meta-llama/Llama-2-7b-chat-hf"
model = HFTransformerModel(model_name)

# Collect all scenarios
scenarios = []
for file in glob.glob("scenarios/**/*.yaml", recursive=True):
    with open(file) as f:
        scenario = yaml.safe_load(f)
    scenarios.append(scenario)

# Create dataset and dataloader
dataset = ScenarioDataset(scenarios)
dataloader = DataLoader(dataset, batch_size=4, collate_fn=collate_fn)

# Process scenarios in batches
for batch in dataloader:
    for scenario in batch:
        output = model.run(scenario["prompt"])
        evaluator = get_evaluator(scenario["evaluator"])
        result = evaluator(output, scenario["expected_output"])
        print(f"{scenario['id']}: {'PASS' if result else 'FAIL'}")
