import os
import json

root_dir = "/nvme/yangbowen/InternGUIFramework/evaluation_examples/macos/examples"
result = {}
for domain in os.listdir(root_dir):
    domain_path = os.path.join(root_dir, domain)
    for task in os.listdir(domain_path):
        task_name = task.split(".")[0]
        if domain not in result.keys():
            result[domain] = []
        result[domain].append(task_name)

with open("/nvme/yangbowen/InternGUIFramework/evaluation_examples/macos/test_all.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)
