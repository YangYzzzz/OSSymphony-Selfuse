"""
Reward Script: Complete BFS function in graph_search.py, run script, save traversal_output.txt
Task ID: osworld_multi_apps_vscode_run_capture_010
Domain: multi_apps (VSCode + OS)
Scoring:
  - Component 1: traversal_output.txt exists on Desktop (0.3 pts)
  - Component 2: BFS function in graph_search.py is implemented (not just 'pass') (0.3 pts)
  - Component 3: traversal_output.txt contains valid BFS traversal from start node (0.4 pts)
"""

import os
from collections import deque

DESKTOP = '/home/user/Desktop'
GRAPH_SCRIPT = os.path.join(DESKTOP, 'graph_search.py')
EDGES_FILE = os.path.join(DESKTOP, 'edges.txt')
START_FILE = os.path.join(DESKTOP, 'start_node.txt')
OUTPUT_FILE = os.path.join(DESKTOP, 'traversal_output.txt')
TASK_ID = 'osworld_multi_apps_vscode_run_capture_010'


def build_graph_from_edges(edges_file):
    """Build adjacency list from edges file."""
    graph = {}
    with open(edges_file, 'r') as f:
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


def compute_valid_bfs_orders(graph, start):
    """
    Compute all valid BFS orderings from the start node.
    BFS order is valid if:
      - start node is first
      - all nodes are visited exactly once
      - for any node at distance d, all nodes at distance d-1 must appear before it
    We compute the BFS levels (sets), and check the actual ordering respects level order.
    Returns: (bfs_levels dict {node: level}, all_nodes set)
    """
    visited = set([start])
    queue = deque([start])
    levels = {start: 0}
    level_num = 0

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                levels[neighbor] = levels[node] + 1
                queue.append(neighbor)

    return levels, visited


def is_valid_bfs_order(traversal_nodes, graph, start):
    """
    Check if the traversal_nodes list is a valid BFS order.
    Valid BFS means:
      1. First node is the start node
      2. All reachable nodes are included exactly once
      3. All nodes appear in non-decreasing level order (BFS level)
    """
    if not traversal_nodes or traversal_nodes[0] != start:
        return False

    levels, reachable = compute_valid_bfs_orders(graph, start)

    # All reachable nodes must be in traversal, and no extras
    if set(traversal_nodes) != reachable:
        return False

    # Check level order is non-decreasing
    last_level = -1
    for node in traversal_nodes:
        node_level = levels.get(node, -1)
        if node_level < last_level:
            return False
        last_level = node_level

    return True


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: verify required input files exist (gate — not scored)
    if not os.path.isfile(EDGES_FILE):
        print(f"CRITICAL: edges.txt not found at {EDGES_FILE}")
        print("REWARD: 0.0")
        return 0.0
    if not os.path.isfile(START_FILE):
        print(f"CRITICAL: start_node.txt not found at {START_FILE}")
        print("REWARD: 0.0")
        return 0.0
    if not os.path.isfile(GRAPH_SCRIPT):
        print(f"CRITICAL: graph_search.py not found at {GRAPH_SCRIPT}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: traversal_output.txt exists on Desktop (0.3 points)
    # This fails on initial_env (file doesn't exist) and passes on golden_env
    try:
        if os.path.isfile(OUTPUT_FILE):
            output_size = os.path.getsize(OUTPUT_FILE)
            if output_size > 0:
                print(f"PASS: Component 1 — traversal_output.txt exists and is non-empty ({output_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — traversal_output.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 — traversal_output.txt not found at {OUTPUT_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: BFS function in graph_search.py is actually implemented (0.3 points)
    # Initial state: bfs() function body is just 'pass'
    # Golden state: bfs() has actual logic with deque/queue/visited
    try:
        with open(GRAPH_SCRIPT, 'r') as f:
            script_content = f.read()

        # Extract the bfs function body for inspection
        bfs_body = ''
        if 'def bfs(' in script_content:
            bfs_start = script_content.find('def bfs(')
            next_def = script_content.find('\ndef ', bfs_start + 1)
            if next_def == -1:
                bfs_body = script_content[bfs_start:]
            else:
                bfs_body = script_content[bfs_start:next_def]

        # Check that the bfs function has actual implementation beyond just 'pass'
        # Look for key BFS indicators: queue, deque, visited, while, append, return
        has_queue_or_deque = 'queue' in bfs_body.lower() or 'deque' in bfs_body.lower()
        has_visited = 'visited' in bfs_body.lower() or 'seen' in bfs_body.lower()
        has_loop = 'while ' in bfs_body or 'for ' in bfs_body
        has_return = 'return ' in bfs_body

        # Identify if the function is a non-empty stub (just 'pass')
        non_comment_lines = [line.strip() for line in bfs_body.split('\n')
                             if line.strip()
                             and not line.strip().startswith('#')
                             and not line.strip().startswith('"""')
                             and not line.strip().startswith("'")
                             and not line.strip().startswith('def ')]
        stub_only = all(l == 'pass' for l in non_comment_lines if l)

        if has_queue_or_deque and has_visited and has_loop and has_return and not stub_only:
            print(f"PASS: Component 2 — BFS function in graph_search.py has a proper implementation (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — BFS function in graph_search.py appears to be a stub or missing key BFS logic")
            print(f"  has_queue_or_deque={has_queue_or_deque}, has_visited={has_visited}, "
                  f"has_loop={has_loop}, has_return={has_return}, stub_only={stub_only}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: traversal_output.txt contains valid BFS traversal from start node (0.4 points)
    # This verifies the actual correctness of the BFS output
    try:
        # Read the start node
        with open(START_FILE, 'r') as f:
            start_node = f.read().strip()

        # Read the traversal output
        with open(OUTPUT_FILE, 'r') as f:
            traversal_lines = [line.strip() for line in f.readlines() if line.strip()]

        if not traversal_lines:
            print(f"FAIL: Component 3 — traversal_output.txt is empty")
        else:
            # Build the graph from edges.txt
            graph = build_graph_from_edges(EDGES_FILE)

            # Check if the traversal is a valid BFS order
            if is_valid_bfs_order(traversal_lines, graph, start_node):
                nodes_str = ', '.join(traversal_lines)
                print(f"PASS: Component 3 — Valid BFS traversal from '{start_node}': [{nodes_str}] (0.4 pts)")
                total_score += 0.4
            else:
                # Compute what a valid BFS would produce (for debugging)
                levels, reachable = compute_valid_bfs_orders(graph, start_node)
                actual_str = ', '.join(traversal_lines)
                print(f"FAIL: Component 3 — traversal_output.txt does not contain a valid BFS order")
                print(f"  Start node: '{start_node}'")
                print(f"  Actual output: [{actual_str}]")
                print(f"  Reachable nodes: {sorted(reachable)}")
                print(f"  Node levels: {levels}")
    except FileNotFoundError as e:
        print(f"FAIL: Component 3 — Required file not found: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
