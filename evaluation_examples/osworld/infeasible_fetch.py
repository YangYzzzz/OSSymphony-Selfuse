import os 
import json

root_dir = "/nvme/yangbowen/yangbowen/InternGUIFramework/evaluation_examples/osworld/examples"

result_data = {}
for domain in os.listdir(root_dir):
    domain_path = os.path.join(root_dir, domain)
    for task in os.listdir(domain_path):
        task_path = os.path.join(domain_path, task)
        with open(task_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "evaluator" in data:
            if "func" in data["evaluator"]:
                if isinstance(data["evaluator"]["func"], str) and "infeasible" == data["evaluator"]["func"]:
                    if domain in result_data.keys():
                        result_data[domain].append(task)
                    else:
                        result_data[domain] = [task]
with open("/nvme/yangbowen/yangbowen/InternGUIFramework/evaluation_examples/osworld/test_infeasible.json", "w") as f:
    json.dump(result_data, f, indent=4)