"""
Initial Setup: BFS graph search task with VSCode
Task ID: osworld_multi_apps_vscode_run_capture_010
Domain: multi_apps (VSCode + terminal)

Creates:
  - /home/user/Desktop/graph_search.py  (with unimplemented BFS function)
  - /home/user/Desktop/edges.txt        (graph edge pairs)
  - /home/user/Desktop/start_node.txt   (BFS start node label)
"""

import os
import shlex
import subprocess
import time

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_010'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # --- edges.txt: graph edge pairs (undirected) ---
    edges_content = """\
A B
A C
B D
B E
C F
D G
E G
F G
"""
    edges_path = os.path.join(DESKTOP, 'edges.txt')
    with open(edges_path, 'w') as f:
        f.write(edges_content)
    print(f'Created: {edges_path}')

    # --- start_node.txt: BFS start node ---
    start_path = os.path.join(DESKTOP, 'start_node.txt')
    with open(start_path, 'w') as f:
        f.write('A\n')
    print(f'Created: {start_path}')

    # --- graph_search.py: unimplemented BFS ---
    graph_search_content = '''\
"""
Graph Search Script
Reads a graph from edges.txt (edge pairs, one per line),
then performs BFS from a start node read from start_node.txt,
and saves the traversal order to traversal_output.txt.
"""

import os
from collections import deque

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
EDGES_FILE = os.path.join(DESKTOP, "edges.txt")
START_FILE = os.path.join(DESKTOP, "start_node.txt")
OUTPUT_FILE = os.path.join(DESKTOP, "traversal_output.txt")


def build_graph(edges_file):
    """Build adjacency list from edges file."""
    graph = {}
    with open(edges_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                u, v = parts
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append(v)
                graph[v].append(u)
    return graph


def bfs(graph, start):
    """
    Perform BFS traversal from the start node.
    Returns a list of nodes in BFS visit order.

    TODO: Implement this function.
    """
    # Unimplemented — student must complete this
    pass


def main():
    # Load start node
    with open(START_FILE, "r") as f:
        start_node = f.read().strip()

    # Build graph
    graph = build_graph(EDGES_FILE)

    # Run BFS
    order = bfs(graph, start_node)

    # Save result
    with open(OUTPUT_FILE, "w") as f:
        for node in order:
            f.write(node + "\\n")

    print(f"BFS traversal from {start_node}: {order}")
    print(f"Result saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
'''
    graph_path = os.path.join(DESKTOP, 'graph_search.py')
    with open(graph_path, 'w') as f:
        f.write(graph_search_content)
    print(f'Created: {graph_path}')

    # Ensure traversal_output.txt does NOT exist (it should be created by the agent)
    output_path = os.path.join(DESKTOP, 'traversal_output.txt')
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f'Removed pre-existing: {output_path}')

    # GUI-ready startup: open VSCode with graph_search.py
    launch_gui(f'code "{graph_path}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with graph_search.py and DISPLAY=:0')


create_initial()
