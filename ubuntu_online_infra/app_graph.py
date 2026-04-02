import json
from typing import Dict, List
import logging

import networkx as nx
import matplotlib.pyplot as plt

logger = logging.getLogger("desktopenv.task_generator")

# APP 初始化信息
APP_CONFIG_PATH = "evaluation_examples/ubuntu_online_rollout/config/app_config.json"
APP_CONFIG_DICT: Dict = json.load(open(APP_CONFIG_PATH, "r"))

APP_SET_CONFIG_DICT = APP_CONFIG_DICT.get("app", {})
EXCLUDED_APP_LIST = APP_CONFIG_DICT.get("excluded", [])
for e in EXCLUDED_APP_LIST:
    if e in APP_SET_CONFIG_DICT:
        del APP_SET_CONFIG_DICT[e]

# For backward compatibility keep a semantic alias
APP_SETUP_DICT = APP_SET_CONFIG_DICT

# Build a directed application graph from config
APP_GRAPH: Dict[str, List[str]] = {}
TYPE_TO_APPS: Dict[str, List[str]] = {}

for app_name, cfg in APP_SETUP_DICT.items():
    # explicit directed edges from related_app
    rel_apps = cfg.get("related_app", []) or []
    APP_GRAPH[app_name] = [a for a in rel_apps if a in APP_SETUP_DICT]

    # index related_type for implicit edges
    rel_types = cfg.get("related_type", []) or []
    for t in rel_types:
        TYPE_TO_APPS.setdefault(t, []).append(app_name)

# add implicit directed edges based on shared related_type
for t, apps in TYPE_TO_APPS.items():
    if len(apps) <= 1:
        continue
    for src in apps:
        for dst in apps:
            if src == dst:
                continue
            if dst not in APP_GRAPH[src]:
                APP_GRAPH[src].append(dst)
                APP_GRAPH[dst].append(src)  # 有向图 -> 无向图 这部分


if __name__ == "__main__":
    G = nx.Graph()
    for app, neighbors in APP_GRAPH.items():
        for n in neighbors:
            G.add_edge(app, n)

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.6)
    nx.draw(G, pos, with_labels=True, node_size=800, font_size=8)
    plt.tight_layout()
    plt.savefig("app_graph.png", dpi=300)
