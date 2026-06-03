"""
Reward Script: Go Testing Project with Table-Driven Tests and Benchmarks
Task ID: vscode_gf6_010
Domain: vscode
Scoring:
  Component 1 (0.25): calculator_test.go exists with table-driven tests using t.Run() and testify/assert
  Component 2 (0.25): Each function (Add, Subtract, Multiply, Divide, Sqrt) has >= 5 subtests
  Component 3 (0.20): benchmark_test.go exists with BenchmarkAdd, BenchmarkMultiply, BenchmarkSqrt
  Component 4 (0.15): .vscode/tasks.json has two required test tasks
  Component 5 (0.15): go.mod has testify dependency
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-testing')
TASK_ID = 'vscode_gf6_010'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: calculator_test.go exists with table-driven tests using t.Run() and testify/assert (0.25 pts)
    test_file = os.path.join(PROJECT, 'pkg', 'calculator', 'calculator_test.go')
    test_content = None
    try:
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                test_content = f.read()

            has_trun = 't.Run(' in test_content
            has_testify = 'testify/assert' in test_content or 'assert.' in test_content
            has_struct = 'struct' in test_content  # table-driven pattern uses struct

            if has_trun and has_testify and has_struct:
                print(f"PASS: Component 1 — calculator_test.go has t.Run(), testify/assert, and struct-based table tests (0.25 pts)")
                total_score += 0.25
            else:
                missing = []
                if not has_trun:
                    missing.append('t.Run()')
                if not has_testify:
                    missing.append('testify/assert')
                if not has_struct:
                    missing.append('struct (table-driven)')
                print(f"FAIL: Component 1 — calculator_test.go missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 1 — calculator_test.go does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each of 5 functions has >= 5 subtests (0.25 pts, 0.05 per function)
    try:
        if test_content is not None:
            functions_to_check = ['TestAdd', 'TestSubtract', 'TestMultiply', 'TestDivide', 'TestSqrt']
            funcs_passing = 0

            for func_name in functions_to_check:
                # Find the function block
                pattern = rf'func\s+{func_name}\s*\(.*?\)\s*\{{(.*?)^\}}'
                match = re.search(pattern, test_content, re.DOTALL | re.MULTILINE)
                if match:
                    func_body = match.group(1)
                    # Count t.Run calls (subtests) or struct entries like {"name", ...}
                    trun_count = func_body.count('t.Run(')
                    # Also count struct entries as backup (lines with braces inside slice literal)
                    struct_entries = len(re.findall(r'\{["\']', func_body))
                    subtest_count = max(trun_count, struct_entries)

                    if subtest_count >= 5:
                        funcs_passing += 1
                        print(f"  PASS: {func_name} has {subtest_count} subtests (>= 5)")
                    else:
                        print(f"  FAIL: {func_name} has {subtest_count} subtests (< 5)")
                else:
                    print(f"  FAIL: {func_name} function not found")

            comp2_score = funcs_passing * 0.05
            if funcs_passing == 5:
                print(f"PASS: Component 2 — all 5 test functions have >= 5 subtests ({comp2_score} pts)")
            else:
                print(f"PARTIAL: Component 2 — {funcs_passing}/5 functions have >= 5 subtests ({comp2_score} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — no test file to analyze")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: benchmark_test.go exists with BenchmarkAdd, BenchmarkMultiply, BenchmarkSqrt (0.20 pts)
    bench_file = os.path.join(PROJECT, 'pkg', 'calculator', 'benchmark_test.go')
    try:
        if os.path.exists(bench_file):
            with open(bench_file, 'r') as f:
                bench_content = f.read()

            required_benchmarks = ['BenchmarkAdd', 'BenchmarkMultiply', 'BenchmarkSqrt']
            found_benchmarks = []
            for bm in required_benchmarks:
                if re.search(rf'func\s+{bm}\s*\(', bench_content):
                    found_benchmarks.append(bm)

            if len(found_benchmarks) == 3:
                print(f"PASS: Component 3 — benchmark_test.go has all 3 required benchmarks (0.20 pts)")
                total_score += 0.20
            else:
                missing = set(required_benchmarks) - set(found_benchmarks)
                partial = len(found_benchmarks) / 3.0 * 0.20
                print(f"PARTIAL: Component 3 — missing benchmarks: {missing} ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — benchmark_test.go does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/tasks.json has two required test tasks (0.15 pts)
    tasks_file = os.path.join(PROJECT, '.vscode', 'tasks.json')
    try:
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r') as f:
                # Handle JSONC (strip comments)
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_config = json.loads(content_clean)

            tasks_list = tasks_config.get('tasks', [])
            has_test_all = False
            has_bench = False

            for task in tasks_list:
                cmd = task.get('command', '') or task.get('label', '')
                # Check for 'go test ./...' task
                if 'go test' in cmd and './...' in cmd and '-bench' not in cmd:
                    has_test_all = True
                # Check for benchmark task
                if 'go test' in cmd and '-bench' in cmd and './pkg/calculator' in cmd:
                    has_bench = True

            comp4_score = 0.0
            if has_test_all:
                comp4_score += 0.075
            if has_bench:
                comp4_score += 0.075

            if has_test_all and has_bench:
                print(f"PASS: Component 4 — tasks.json has both test tasks (0.15 pts)")
            else:
                missing = []
                if not has_test_all:
                    missing.append("'go test ./...'")
                if not has_bench:
                    missing.append("'go test -bench=. ./pkg/calculator/'")
                print(f"PARTIAL: Component 4 — missing tasks: {', '.join(missing)} ({comp4_score} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 — .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: go.mod has testify dependency (0.15 pts)
    gomod_file = os.path.join(PROJECT, 'go.mod')
    try:
        if os.path.exists(gomod_file):
            with open(gomod_file, 'r') as f:
                gomod_content = f.read()

            if 'stretchr/testify' in gomod_content:
                print(f"PASS: Component 5 — go.mod has testify dependency (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — go.mod does not contain testify dependency")
        else:
            print(f"FAIL: Component 5 — go.mod does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
