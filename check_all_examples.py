"""
    检查所有的任务的 config 和 postconfig 是否存在 Permission Denied 的问题
    TODO: Yang
"""

import os
import json
root_dir = "/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/examples"

"""
  "config": [
    {
      "type": "execute",
      "parameters": {
        "command": "echo {CLIENT_PASSWORD} | sudo -S mkdir /home/test1",
        "shell": true
      }
    }
  ]
"""
for sub_domain in os.listdir(root_dir):
    sub_domain_dir = os.path.join(root_dir, sub_domain)
    for task_name in os.listdir(sub_domain_dir):
        with open(os.path.join(sub_domain_dir, task_name)) as f:
            task_file = json.load(f)
        # if "config" in task_file:
        #     config = task_file["config"]
        #     # post_config = task_file["post_config"]
        #     for c in config:
        #         if c["type"] == "execute":
        #             print(f"domain: {sub_domain}, task: {task_name}, command: {c['parameters']['command']}")
        # else:
        #     print(f"===================\ndomain: {sub_domain}, task: {task_name} no config\n=====================")

        if "evaluator" in task_file and "postconfig" in task_file["evaluator"]:
            config = task_file["evaluator"]["postconfig"]
            # post_config = task_file["post_config"]
            for c in config:
                if c["type"] == "execute":
                    print(f"domain: {sub_domain}, task: {task_name}, command: {c['parameters']['command']}")