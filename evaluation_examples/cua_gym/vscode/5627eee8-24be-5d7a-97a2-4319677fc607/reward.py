"""
Reward Script: Distributed Counter using CRDTs in Go
Task ID: vscode_gf4_044
Domain: vscode
Scoring:
  C1 (0.10) - go.mod with correct module path
  C2 (0.20) - gcounter.go with required methods
  C3 (0.20) - pncounter.go using two GCounters
  C4 (0.15) - gossip.go with gossip protocol simulator
  C5 (0.10) - cmd/simulator/main.go with 3-node simulation
  C6 (0.10) - Test files with CRDT property tests
  C7 (0.15) - go test ./... passes
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-distributed-counter')


def read_file(path):
    """Read file content, return None if missing."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    total_score = 0.0

    # Component 1: go.mod with correct module path (0.10 points)
    try:
        gomod = read_file(os.path.join(PROJECT_DIR, 'go.mod'))
        if gomod and 'module github.com/user/go-distributed-counter' in gomod:
            print(f"PASS: Component 1 - go.mod has correct module path (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 - go.mod missing or wrong module path. Content: {gomod!r:.200}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: gcounter.go with required struct and methods (0.20 points)
    try:
        gc_path = os.path.join(PROJECT_DIR, 'pkg', 'crdt', 'gcounter.go')
        gc_content = read_file(gc_path)
        if gc_content is None:
            print("FAIL: Component 2 - gcounter.go not found")
        else:
            sub_score = 0.0
            # Check for GCounter struct
            if re.search(r'type\s+GCounter\s+struct', gc_content):
                sub_score += 0.04
            # Check for Increment method with nodeID parameter
            if re.search(r'func\s+\([^)]*GCounter\)\s+Increment\s*\(\s*\w+\s+string\s*\)', gc_content):
                sub_score += 0.04
            # Check for Value method returning int64
            if re.search(r'func\s+\([^)]*GCounter\)\s+Value\s*\(\s*\)\s+int64', gc_content):
                sub_score += 0.04
            # Check for Merge method
            if re.search(r'func\s+\([^)]*GCounter\)\s+Merge\s*\(', gc_content):
                sub_score += 0.04
            # Check for MarshalJSON and UnmarshalJSON
            if re.search(r'func\s+\([^)]*GCounter\)\s+MarshalJSON', gc_content) and \
               re.search(r'func\s+\([^)]*GCounter\)\s+UnmarshalJSON', gc_content):
                sub_score += 0.04

            if sub_score > 0:
                print(f"PASS: Component 2 - gcounter.go has required methods ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 - gcounter.go missing required methods")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: pncounter.go using two GCounters (0.20 points)
    try:
        pn_path = os.path.join(PROJECT_DIR, 'pkg', 'crdt', 'pncounter.go')
        pn_content = read_file(pn_path)
        if pn_content is None:
            print("FAIL: Component 3 - pncounter.go not found")
        else:
            sub_score = 0.0
            # Check for PNCounter struct
            if re.search(r'type\s+PNCounter\s+struct', pn_content):
                sub_score += 0.04
            # Check it uses GCounter (two of them for P and N)
            if re.search(r'\*?GCounter', pn_content):
                sub_score += 0.04
            # Check for Increment method
            if re.search(r'func\s+\([^)]*PNCounter\)\s+Increment\s*\(', pn_content):
                sub_score += 0.04
            # Check for Decrement method
            if re.search(r'func\s+\([^)]*PNCounter\)\s+Decrement\s*\(', pn_content):
                sub_score += 0.04
            # Check for Value and Merge methods
            if re.search(r'func\s+\([^)]*PNCounter\)\s+Value\s*\(\s*\)', pn_content) and \
               re.search(r'func\s+\([^)]*PNCounter\)\s+Merge\s*\(', pn_content):
                sub_score += 0.04

            if sub_score > 0:
                print(f"PASS: Component 3 - pncounter.go has required structure ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 - pncounter.go missing required structure")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: gossip.go with gossip protocol simulator (0.15 points)
    try:
        gossip_path = os.path.join(PROJECT_DIR, 'pkg', 'sync', 'gossip.go')
        gossip_content = read_file(gossip_path)
        if gossip_content is None:
            print("FAIL: Component 4 - gossip.go not found")
        else:
            sub_score = 0.0
            # Check for Node struct
            if re.search(r'type\s+Node\s+struct', gossip_content):
                sub_score += 0.05
            # Check for GossipSimulator or similar coordinator struct
            if re.search(r'type\s+\w*(Gossip|Simulator|gossip|simulator)\w*\s+struct', gossip_content):
                sub_score += 0.05
            # Check for periodic exchange / merge / gossip mechanism
            if re.search(r'(exchange|merge|gossip|Exchange|Merge|Gossip)', gossip_content) and \
               re.search(r'(ticker|Ticker|interval|Interval|periodic|time\.)', gossip_content):
                sub_score += 0.05

            if sub_score > 0:
                print(f"PASS: Component 4 - gossip.go has gossip protocol ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 - gossip.go missing gossip protocol elements")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: cmd/simulator/main.go with 3-node simulation (0.10 points)
    try:
        main_path = os.path.join(PROJECT_DIR, 'cmd', 'simulator', 'main.go')
        main_content = read_file(main_path)
        if main_content is None:
            print("FAIL: Component 5 - cmd/simulator/main.go not found")
        else:
            sub_score = 0.0
            # Check for package main
            if re.search(r'package\s+main', main_content):
                sub_score += 0.02
            # Check for func main
            if re.search(r'func\s+main\s*\(\s*\)', main_content):
                sub_score += 0.02
            # Check for 3 nodes (look for node creation patterns)
            node_refs = re.findall(r'NewNode|node[_-]?[123]|Node\s*\{', main_content, re.IGNORECASE)
            if len(node_refs) >= 3:
                sub_score += 0.03
            # Check for concurrent operations (goroutines)
            if re.search(r'go\s+func|goroutine|sync\.WaitGroup|wg\.Add', main_content):
                sub_score += 0.03

            if sub_score > 0:
                print(f"PASS: Component 5 - main.go has 3-node simulation ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 5 - main.go missing simulation elements")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Test files with CRDT property tests (0.10 points)
    try:
        test_content_all = ""
        for test_name in ['gcounter_test.go', 'pncounter_test.go']:
            tp = os.path.join(PROJECT_DIR, 'pkg', 'crdt', test_name)
            tc = read_file(tp)
            if tc:
                test_content_all += tc

        if len(test_content_all) == 0:
            print("FAIL: Component 6 - No test files found in pkg/crdt/")
        else:
            sub_score = 0.0
            # Check for commutativity test
            if re.search(r'(commutativity|Commutativity|commutative|Commutative)', test_content_all, re.IGNORECASE):
                sub_score += 0.033
            # Check for associativity test
            if re.search(r'(associativity|Associativity|associative|Associative)', test_content_all, re.IGNORECASE):
                sub_score += 0.033
            # Check for idempotency test
            if re.search(r'(idempotency|Idempotency|idempotent|Idempotent)', test_content_all, re.IGNORECASE):
                sub_score += 0.034

            if sub_score > 0:
                print(f"PASS: Component 6 - CRDT property tests found ({sub_score:.3f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 6 - Test files exist but no CRDT property tests (commutativity/associativity/idempotency)")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: go test ./... passes (0.15 points)
    try:
        go_bin = None
        for candidate in ['/home/user/go-sdk/bin/go', '/usr/local/go/bin/go', '/usr/bin/go', '/snap/bin/go']:
            if os.path.exists(candidate):
                go_bin = candidate
                break

        if go_bin is None:
            print("FAIL: Component 7 - Go binary not found on system")
        else:
            go_dir = os.path.dirname(go_bin)
            cmd = (
                f'export PATH="{go_dir}:$PATH" && '
                f'export HOME="/home/user" && '
                f'export GOPATH="/home/user/go" && '
                f'cd "{PROJECT_DIR}" && '
                f'"{go_bin}" test ./... 2>&1'
            )
            pipe = os.popen(cmd)
            output = pipe.read()
            rc = pipe.close()
            # os.popen returns None on success (exit code 0)
            if rc is None:
                print(f"PASS: Component 7 - go test ./... passed (0.15 pts)")
                print(f"  output: {output.strip()}")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 - go test ./... failed (rc={rc})")
                print(f"  output: {output.strip()}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
