"""
Reward Script: Go streaming data processing framework
Task ID: vscode_gf4_092
Domain: vscode
Scoring:
  C1 (0.10) - go.mod with correct module name
  C2 (0.15) - source.go: Source interface, FileSource, ChannelSource
  C3 (0.15) - transform.go: Map, Filter, FlatMap, Window
  C4 (0.15) - sink.go: FileSink, ChannelSink, MetricsSink
  C5 (0.15) - pipeline.go: From/Transform/To/Run builder
  C6 (0.15) - parallel.go: ParallelPipeline with fan-out/fan-in + workers
  C7 (0.15) - 15+ tests that compile and pass
"""

import os
import re

WORKDIR = '/home/user/projects/go-stream-processor'
GO_BIN = '/home/user/go-sdk/go/bin/go'


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ""


def verify_task():
    total_score = 0.0

    # ── Component 1: go.mod exists with module github.com/user/go-stream (0.10) ──
    try:
        gomod = read_file(os.path.join(WORKDIR, 'go.mod'))
        if gomod and 'module github.com/user/go-stream' in gomod:
            print("PASS: C1 — go.mod has module github.com/user/go-stream (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: C1 — go.mod missing or wrong module. Content: {gomod[:200]}")
    except Exception as e:
        print(f"ERROR: C1 — {e}")

    # ── Component 2: source.go — Source interface, FileSource, ChannelSource (0.15) ──
    try:
        src = read_file(os.path.join(WORKDIR, 'pkg', 'stream', 'source.go'))
        if not src:
            print("FAIL: C2 — source.go not found")
        else:
            checks = 0
            # Source interface with Next() and Close()
            if re.search(r'type\s+Source\s+interface', src) and 'Next()' in src and 'Close()' in src:
                checks += 1
            # FileSource struct
            if re.search(r'type\s+FileSource\s+struct', src):
                checks += 1
            # ChannelSource struct
            if re.search(r'type\s+ChannelSource\s+struct', src):
                checks += 1

            if checks == 3:
                print("PASS: C2 — source.go has Source interface, FileSource, ChannelSource (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                pts = 0.10
                print(f"PARTIAL: C2 — source.go has {checks}/3 required elements ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: C2 — source.go has only {checks}/3 required elements")
    except Exception as e:
        print(f"ERROR: C2 — {e}")

    # ── Component 3: transform.go — Map, Filter, FlatMap, Window (0.15) ──
    try:
        tf = read_file(os.path.join(WORKDIR, 'pkg', 'stream', 'transform.go'))
        if not tf:
            print("FAIL: C3 — transform.go not found")
        else:
            checks = 0
            # Transform interface
            if re.search(r'type\s+Transform\s+interface', tf):
                checks += 1
            # Map function/type
            if re.search(r'func\s+Map\s*\(', tf) or re.search(r'type\s+MapTransform\s+struct', tf):
                checks += 1
            # Filter function/type
            if re.search(r'func\s+Filter\s*\(', tf) or re.search(r'type\s+FilterTransform\s+struct', tf):
                checks += 1
            # FlatMap function/type
            if re.search(r'func\s+FlatMap\s*\(', tf) or re.search(r'type\s+FlatMapTransform\s+struct', tf):
                checks += 1
            # Window function/type
            if re.search(r'func\s+Window\s*\(', tf) or re.search(r'type\s+WindowTransform\s+struct', tf):
                checks += 1

            if checks >= 5:
                print("PASS: C3 — transform.go has Transform interface + Map/Filter/FlatMap/Window (0.15 pts)")
                total_score += 0.15
            elif checks >= 3:
                pts = round(0.15 * checks / 5, 2)
                print(f"PARTIAL: C3 — transform.go has {checks}/5 required elements ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: C3 — transform.go has only {checks}/5 required elements")
    except Exception as e:
        print(f"ERROR: C3 — {e}")

    # ── Component 4: sink.go — FileSink, ChannelSink, MetricsSink (0.15) ──
    try:
        sk = read_file(os.path.join(WORKDIR, 'pkg', 'stream', 'sink.go'))
        if not sk:
            print("FAIL: C4 — sink.go not found")
        else:
            checks = 0
            # Sink interface
            if re.search(r'type\s+Sink\s+interface', sk):
                checks += 1
            # FileSink
            if re.search(r'type\s+FileSink\s+struct', sk):
                checks += 1
            # ChannelSink
            if re.search(r'type\s+ChannelSink\s+struct', sk):
                checks += 1
            # MetricsSink
            if re.search(r'type\s+MetricsSink\s+struct', sk):
                checks += 1

            if checks >= 4:
                print("PASS: C4 — sink.go has Sink interface + FileSink/ChannelSink/MetricsSink (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                pts = round(0.15 * checks / 4, 2)
                print(f"PARTIAL: C4 — sink.go has {checks}/4 required elements ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: C4 — sink.go has only {checks}/4 required elements")
    except Exception as e:
        print(f"ERROR: C4 — {e}")

    # ── Component 5: pipeline.go — From/Transform/To/Run builder (0.15) ──
    try:
        pl = read_file(os.path.join(WORKDIR, 'pkg', 'stream', 'pipeline.go'))
        if not pl:
            print("FAIL: C5 — pipeline.go not found")
        else:
            checks = 0
            # Pipeline struct
            if re.search(r'type\s+Pipeline\s+struct', pl):
                checks += 1
            # From function
            if re.search(r'func\s+From\s*\(', pl):
                checks += 1
            # Transform method on builder
            if re.search(r'func\s+\([^)]+\)\s+Transform\s*\(', pl):
                checks += 1
            # To method
            if re.search(r'func\s+\([^)]+\)\s+To\s*\(', pl):
                checks += 1
            # Run method with context
            if re.search(r'func\s+\([^)]+\)\s+Run\s*\(\s*ctx', pl) or re.search(r'func\s+\([^)]+\)\s+Run\s*\(', pl):
                checks += 1

            if checks >= 5:
                print("PASS: C5 — pipeline.go has Pipeline builder with From/Transform/To/Run (0.15 pts)")
                total_score += 0.15
            elif checks >= 3:
                pts = round(0.15 * checks / 5, 2)
                print(f"PARTIAL: C5 — pipeline.go has {checks}/5 required elements ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: C5 — pipeline.go has only {checks}/5 required elements")
    except Exception as e:
        print(f"ERROR: C5 — {e}")

    # ── Component 6: parallel.go — ParallelPipeline with fan-out/fan-in (0.15) ──
    try:
        pp = read_file(os.path.join(WORKDIR, 'pkg', 'stream', 'parallel.go'))
        if not pp:
            print("FAIL: C6 — parallel.go not found")
        else:
            checks = 0
            # ParallelPipeline struct
            if re.search(r'type\s+ParallelPipeline\s+struct', pp):
                checks += 1
            # workers field or parameter
            if 'workers' in pp.lower():
                checks += 1
            # goroutine usage (fan-out)
            if 'go func' in pp:
                checks += 1
            # sync package (for WaitGroup or Mutex — fan-in coordination)
            if 'sync.' in pp:
                checks += 1
            # Run method
            if re.search(r'func\s+\([^)]+\)\s+Run\s*\(', pp):
                checks += 1

            if checks >= 5:
                print("PASS: C6 — parallel.go has ParallelPipeline with fan-out/fan-in and workers (0.15 pts)")
                total_score += 0.15
            elif checks >= 3:
                pts = round(0.15 * checks / 5, 2)
                print(f"PARTIAL: C6 — parallel.go has {checks}/5 required elements ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: C6 — parallel.go has only {checks}/5 required elements")
    except Exception as e:
        print(f"ERROR: C6 — {e}")

    # ── Component 7: 15+ tests that compile and pass (0.15) ──
    try:
        # Count test functions across all _test.go files
        test_dir = os.path.join(WORKDIR, 'pkg', 'stream')
        test_files = [f for f in os.listdir(test_dir) if f.endswith('_test.go')] if os.path.isdir(test_dir) else []

        if not test_files:
            # Also check root-level tests
            root_tests = [f for f in os.listdir(WORKDIR) if f.endswith('_test.go')] if os.path.isdir(WORKDIR) else []
            if root_tests:
                test_files = root_tests
                test_dir = WORKDIR

        total_test_funcs = 0
        for tf_name in test_files:
            content = read_file(os.path.join(test_dir, tf_name))
            # Count func Test... functions
            funcs = re.findall(r'func\s+(Test\w+)\s*\(', content)
            total_test_funcs += len(funcs)

        if total_test_funcs >= 15:
            # Now actually run the tests to check they pass
            go_test_result = os.popen(
                f'export PATH=/home/user/go-sdk/go/bin:$PATH && '
                f'cd {WORKDIR} && '
                f'{GO_BIN} test -count=1 ./... 2>&1'
            ).read()

            if 'FAIL' not in go_test_result or 'ok' in go_test_result:
                # Check more carefully: go test outputs "ok" for passing, "FAIL" for failing
                lines = go_test_result.strip().split('\n')
                has_fail = any(l.startswith('FAIL') for l in lines)
                has_ok = any(l.startswith('ok') for l in lines)

                if has_ok and not has_fail:
                    print(f"PASS: C7 — {total_test_funcs} test functions found and all pass (0.15 pts)")
                    total_score += 0.15
                elif has_ok and has_fail:
                    # Some pass, some fail
                    print(f"PARTIAL: C7 — {total_test_funcs} tests found but some fail (0.07 pts)")
                    total_score += 0.07
                else:
                    print(f"FAIL: C7 — tests do not pass. Output: {go_test_result[:300]}")
            else:
                print(f"FAIL: C7 — tests failed. Output: {go_test_result[:300]}")
        elif total_test_funcs > 0:
            pts = round(0.15 * min(total_test_funcs, 15) / 15, 2)
            print(f"PARTIAL: C7 — only {total_test_funcs}/15 test functions found ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: C7 — no test files or test functions found")
    except Exception as e:
        print(f"ERROR: C7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# ── Entry point ──
if not os.path.isdir(WORKDIR):
    print(f"Project directory not found: {WORKDIR}")
    print("REWARD: 0.0")
elif not os.path.exists(os.path.join(WORKDIR, 'go.mod')):
    # No go.mod means project not initialized — score 0
    print("FAIL: go.mod not found — project not initialized")
    print("REWARD: 0.0")
else:
    verify_task()
