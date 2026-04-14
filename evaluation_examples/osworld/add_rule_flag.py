root_dir = "/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/osworld/examples"
import os, json

for domain in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, domain)):
        for task in os.listdir(os.path.join(root_dir, domain)):
            if task.endswith(".json"):
                with open(os.path.join(root_dir, domain, task), "r") as f:
                    data = json.load(f)
                data["evaluator"]["need_rule_judge"] = True
                with open(os.path.join(root_dir, domain, task), "w") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
