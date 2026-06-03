"""
Reward Script: Go Raft Consensus Implementation
Task ID: vscode_gf4_062
Domain: vscode (Go project)
Scoring:
  - go.mod with correct module name (0.10)
  - state.go: RaftNode struct + Follower/Candidate/Leader states (0.15)
  - log.go: LogEntry + Log with AppendEntry/GetEntry/CommitUpTo (0.15)
  - rpc.go: RequestVote + AppendEntries RPC types (0.10)
  - node.go: election timeout, vote counting, heartbeat goroutines (0.15)
  - cluster.go: Cluster struct managing nodes + RPC routing (0.10)
  - test file with leader election + log replication tests (0.10)
  - go vet passes (0.05)
  - go test passes (0.10)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-raft-consensus')
PKG_DIR = os.path.join(PROJECT_DIR, 'pkg', 'raft')
GO_BIN = '/home/user/go-sdk/bin/go'


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: go.mod exists with correct module name (0.10 points)
    try:
        gomod_path = os.path.join(PROJECT_DIR, 'go.mod')
        gomod = read_file(gomod_path)
        if gomod:
            # Check module declaration
            if re.search(r'module\s+github\.com/user/go-raft\b', gomod):
                print(f"PASS: Component 1 — go.mod has module github.com/user/go-raft (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — go.mod module declaration not matching 'github.com/user/go-raft'")
                print(f"  Content: {gomod[:200]}")
        else:
            print(f"FAIL: Component 1 — go.mod not found at {gomod_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: state.go defines RaftNode with Follower/Candidate/Leader (0.15 points)
    try:
        state_go = read_file(os.path.join(PKG_DIR, 'state.go'))
        if not state_go:
            print("FAIL: Component 2 — state.go not found")
        else:
            checks = 0
            max_checks = 4
            if re.search(r'type\s+RaftNode\s+struct', state_go):
                checks += 1
            else:
                print("  DETAIL: RaftNode struct not found in state.go")
            if re.search(r'Follower\b', state_go):
                checks += 1
            else:
                print("  DETAIL: Follower state not found in state.go")
            if re.search(r'Candidate\b', state_go):
                checks += 1
            else:
                print("  DETAIL: Candidate state not found in state.go")
            if re.search(r'Leader\b', state_go):
                checks += 1
            else:
                print("  DETAIL: Leader state not found in state.go")

            if checks == max_checks:
                print(f"PASS: Component 2 — state.go has RaftNode + all 3 states (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                partial = round(0.15 * checks / max_checks, 2)
                print(f"PARTIAL: Component 2 — state.go has {checks}/{max_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — state.go missing key elements ({checks}/{max_checks})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: log.go has LogEntry + Log with required methods (0.15 points)
    try:
        log_go = read_file(os.path.join(PKG_DIR, 'log.go'))
        if not log_go:
            print("FAIL: Component 3 — log.go not found")
        else:
            checks = 0
            max_checks = 5
            if re.search(r'type\s+LogEntry\s+struct', log_go):
                checks += 1
            else:
                print("  DETAIL: LogEntry struct not found in log.go")
            if re.search(r'type\s+Log\s+struct', log_go):
                checks += 1
            else:
                print("  DETAIL: Log struct not found in log.go")
            if re.search(r'func\s+\([^)]*Log\)\s+AppendEntry', log_go):
                checks += 1
            else:
                print("  DETAIL: AppendEntry method not found in log.go")
            if re.search(r'func\s+\([^)]*Log\)\s+GetEntry', log_go):
                checks += 1
            else:
                print("  DETAIL: GetEntry method not found in log.go")
            if re.search(r'func\s+\([^)]*Log\)\s+CommitUpTo', log_go):
                checks += 1
            else:
                print("  DETAIL: CommitUpTo method not found in log.go")

            if checks == max_checks:
                print(f"PASS: Component 3 — log.go has LogEntry + Log + all 3 methods (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                partial = round(0.15 * checks / max_checks, 2)
                print(f"PARTIAL: Component 3 — log.go has {checks}/{max_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — log.go missing key elements ({checks}/{max_checks})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: rpc.go has RequestVote and AppendEntries types (0.10 points)
    try:
        rpc_go = read_file(os.path.join(PKG_DIR, 'rpc.go'))
        if not rpc_go:
            print("FAIL: Component 4 — rpc.go not found")
        else:
            checks = 0
            max_checks = 4
            if re.search(r'type\s+RequestVoteArgs\s+struct', rpc_go):
                checks += 1
            else:
                print("  DETAIL: RequestVoteArgs struct not found")
            if re.search(r'type\s+RequestVoteReply\s+struct', rpc_go):
                checks += 1
            else:
                print("  DETAIL: RequestVoteReply struct not found")
            if re.search(r'type\s+AppendEntriesArgs\s+struct', rpc_go):
                checks += 1
            else:
                print("  DETAIL: AppendEntriesArgs struct not found")
            if re.search(r'type\s+AppendEntriesReply\s+struct', rpc_go):
                checks += 1
            else:
                print("  DETAIL: AppendEntriesReply struct not found")

            if checks == max_checks:
                print(f"PASS: Component 4 — rpc.go has all 4 RPC types (0.10 pts)")
                total_score += 0.10
            elif checks >= 2:
                partial = round(0.10 * checks / max_checks, 2)
                print(f"PARTIAL: Component 4 — rpc.go has {checks}/{max_checks} types ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — rpc.go missing RPC types ({checks}/{max_checks})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: node.go has election timeout, vote counting, heartbeat with goroutines (0.15 points)
    try:
        node_go = read_file(os.path.join(PKG_DIR, 'node.go'))
        if not node_go:
            print("FAIL: Component 5 — node.go not found")
        else:
            checks = 0
            max_checks = 4
            # Election timeout (timer or timeout pattern)
            if re.search(r'(ElectionTimeout|electionTimeout|election.*[Tt]imeout|randomElectionTimeout)', node_go):
                checks += 1
            else:
                print("  DETAIL: Election timeout logic not found in node.go")
            # Vote counting
            if re.search(r'(votes?\s*[\+:]|vote.*count|VoteGranted|majority)', node_go):
                checks += 1
            else:
                print("  DETAIL: Vote counting logic not found in node.go")
            # Heartbeat sending
            if re.search(r'(heartbeat|Heartbeat|HeartbeatInterval)', node_go):
                checks += 1
            else:
                print("  DETAIL: Heartbeat logic not found in node.go")
            # Goroutines (go keyword for concurrent operations)
            if re.search(r'\bgo\s+func\b', node_go):
                checks += 1
            else:
                print("  DETAIL: Goroutine usage not found in node.go")

            if checks == max_checks:
                print(f"PASS: Component 5 — node.go has election/vote/heartbeat/goroutines (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                partial = round(0.15 * checks / max_checks, 2)
                print(f"PARTIAL: Component 5 — node.go has {checks}/{max_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — node.go missing key elements ({checks}/{max_checks})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: cluster.go manages nodes and routes RPCs (0.10 points)
    try:
        cluster_go = read_file(os.path.join(PKG_DIR, 'cluster.go'))
        if not cluster_go:
            print("FAIL: Component 6 — cluster.go not found")
        else:
            checks = 0
            max_checks = 3
            if re.search(r'type\s+Cluster\s+struct', cluster_go):
                checks += 1
            else:
                print("  DETAIL: Cluster struct not found")
            if re.search(r'(SendRequestVote|RequestVote|routeRPC)', cluster_go):
                checks += 1
            else:
                print("  DETAIL: RequestVote RPC routing not found")
            if re.search(r'(SendAppendEntries|AppendEntries|routeRPC)', cluster_go):
                checks += 1
            else:
                print("  DETAIL: AppendEntries RPC routing not found")

            if checks == max_checks:
                print(f"PASS: Component 6 — cluster.go has Cluster + RPC routing (0.10 pts)")
                total_score += 0.10
            elif checks >= 1:
                partial = round(0.10 * checks / max_checks, 2)
                print(f"PARTIAL: Component 6 — cluster.go has {checks}/{max_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — cluster.go missing key elements")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Test file with leader election and log replication tests (0.10 points)
    try:
        # Look for test files in pkg/raft/
        test_files = [f for f in os.listdir(PKG_DIR) if f.endswith('_test.go')] if os.path.isdir(PKG_DIR) else []
        if not test_files:
            print("FAIL: Component 7 — No _test.go files found in pkg/raft/")
        else:
            test_content = ''
            for tf in test_files:
                test_content += read_file(os.path.join(PKG_DIR, tf))

            checks = 0
            max_checks = 2
            # Check for leader election test
            if re.search(r'(TestLeaderElection|test.*leader.*election|leader.*elect)', test_content, re.IGNORECASE):
                checks += 1
            else:
                print("  DETAIL: Leader election test not found")
            # Check for log replication test
            if re.search(r'(TestLogReplication|test.*log.*replic|log.*replic)', test_content, re.IGNORECASE):
                checks += 1
            else:
                print("  DETAIL: Log replication test not found")

            if checks == max_checks:
                print(f"PASS: Component 7 — Test file has leader election + log replication tests (0.10 pts)")
                total_score += 0.10
            elif checks >= 1:
                partial = round(0.10 * checks / max_checks, 2)
                print(f"PARTIAL: Component 7 — Test file has {checks}/{max_checks} test types ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 7 — Test file missing required test functions")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: go vet passes (0.05 points)
    try:
        go_bin = GO_BIN if os.path.exists(GO_BIN) else 'go'
        vet_result = os.popen(f'cd {PROJECT_DIR} && {go_bin} vet ./... 2>&1').read()
        # go vet returns empty output on success
        if vet_result.strip() == '' or 'no Go files' not in vet_result:
            # Verify by checking exit code
            exit_code = os.system(f'cd {PROJECT_DIR} && {go_bin} vet ./... > /dev/null 2>&1')
            if exit_code == 0:
                print(f"PASS: Component 8 — go vet passes (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 8 — go vet failed with exit code {exit_code}")
                print(f"  Output: {vet_result[:300]}")
        else:
            print(f"FAIL: Component 8 — go vet issues: {vet_result[:300]}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: go test passes (0.10 points)
    try:
        go_bin = GO_BIN if os.path.exists(GO_BIN) else 'go'
        test_output = os.popen(f'cd {PROJECT_DIR} && {go_bin} test ./... -timeout 30s 2>&1').read()
        exit_code = os.system(f'cd {PROJECT_DIR} && {go_bin} test ./... -timeout 30s > /dev/null 2>&1')
        if exit_code == 0:
            print(f"PASS: Component 9 — go test ./... passes (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 9 — go test failed with exit code {exit_code}")
            print(f"  Output: {test_output[:500]}")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
