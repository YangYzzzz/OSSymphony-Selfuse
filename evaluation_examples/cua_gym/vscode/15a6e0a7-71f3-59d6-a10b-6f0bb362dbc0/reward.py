"""
Reward Script: TypeScript Dependency Graph Analyzer
Task ID: vscode_gf4_072
Domain: vscode
Scoring:
  Component 1: package.json with required deps (0.15)
  Component 2: src/analyzer.ts with DependencyAnalyzer class (0.20)
  Component 3: src/graph.ts with DependencyGraph class and methods (0.20)
  Component 4: src/reporter.ts with JSON/DOT/ASCII formats (0.15)
  Component 5: src/cli.ts CLI interface (0.10)
  Component 6: Jest tests (>= 15 tests) (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-dependency-graph')
TASK_ID = 'vscode_gf4_072'


def read_file(path):
    """Read file content, return None if missing."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: package.json with required dependencies (0.15 points)
    # =========================================================================
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        pkg_content = read_file(pkg_path)
        if pkg_content is None:
            print("FAIL: Component 1 — package.json not found")
        else:
            pkg = json.loads(pkg_content)
            all_deps = {}
            all_deps.update(pkg.get('dependencies', {}))
            all_deps.update(pkg.get('devDependencies', {}))

            required_deps = ['typescript', '@types/node', 'glob', 'madge', 'jest', '@types/jest', 'ts-jest']
            found = [d for d in required_deps if d in all_deps]
            missing = [d for d in required_deps if d not in all_deps]

            if len(found) >= 5:  # At least 5 of 7 required deps
                print(f"PASS: Component 1 — package.json has {len(found)}/{len(required_deps)} required deps (0.15 pts)")
                if missing:
                    print(f"  NOTE: Missing deps: {missing}")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — package.json only has {len(found)}/{len(required_deps)} required deps. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: src/analyzer.ts with DependencyAnalyzer class (0.20 points)
    # =========================================================================
    try:
        analyzer_path = os.path.join(PROJECT_DIR, 'src', 'analyzer.ts')
        content = read_file(analyzer_path)
        if content is None:
            print("FAIL: Component 2 — src/analyzer.ts not found")
        else:
            checks = []
            # Must have DependencyAnalyzer class
            if re.search(r'class\s+DependencyAnalyzer', content):
                checks.append('DependencyAnalyzer class')
            # Must have analyze method with entryPoint parameter
            if re.search(r'analyze\s*\(\s*\w+\s*:\s*string', content):
                checks.append('analyze(entryPoint: string)')
            # Must use TypeScript compiler API
            if 'typescript' in content.lower() or "import * as ts from" in content or "ts.createSourceFile" in content:
                checks.append('TypeScript compiler API')
            # Must have buildGraph returning Map
            if re.search(r'buildGraph\s*\(', content):
                checks.append('buildGraph()')

            if len(checks) >= 3:
                print(f"PASS: Component 2 — src/analyzer.ts has: {', '.join(checks)} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — src/analyzer.ts only has {len(checks)}/3 required features: {checks}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: src/graph.ts with DependencyGraph class and methods (0.20 points)
    # =========================================================================
    try:
        graph_path = os.path.join(PROJECT_DIR, 'src', 'graph.ts')
        content = read_file(graph_path)
        if content is None:
            print("FAIL: Component 3 — src/graph.ts not found")
        else:
            required_methods = {
                'addEdge': r'addEdge\s*\(',
                'findCycles': r'findCycles\s*\(',
                'shortestPath': r'shortestPath\s*\(',
                'topologicalSort': r'topologicalSort\s*\(',
                'transitiveDeps': r'transitiveDeps\s*\(',
            }
            found_methods = []
            for name, pattern in required_methods.items():
                if re.search(pattern, content):
                    found_methods.append(name)

            has_class = bool(re.search(r'class\s+DependencyGraph', content))

            if has_class and len(found_methods) >= 4:
                print(f"PASS: Component 3 — src/graph.ts has DependencyGraph with methods: {', '.join(found_methods)} (0.20 pts)")
                total_score += 0.20
            else:
                missing = [m for m in required_methods if m not in found_methods]
                print(f"FAIL: Component 3 — class={has_class}, found methods={found_methods}, missing={missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: src/reporter.ts with JSON, DOT, ASCII formats (0.15 points)
    # =========================================================================
    try:
        reporter_path = os.path.join(PROJECT_DIR, 'src', 'reporter.ts')
        content = read_file(reporter_path)
        if content is None:
            print("FAIL: Component 4 — src/reporter.ts not found")
        else:
            formats_found = []
            if re.search(r'(generateJSON|json|JSON)', content) and re.search(r'JSON\.stringify', content):
                formats_found.append('JSON')
            if re.search(r'(generateDOT|dot|DOT)', content) and re.search(r'digraph', content):
                formats_found.append('DOT')
            if re.search(r'(generateASCII|ascii|ASCII|tree)', content, re.IGNORECASE):
                formats_found.append('ASCII')

            if len(formats_found) >= 2:
                print(f"PASS: Component 4 — src/reporter.ts supports formats: {', '.join(formats_found)} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — src/reporter.ts only has formats: {formats_found}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: src/cli.ts CLI interface (0.10 points)
    # =========================================================================
    try:
        cli_path = os.path.join(PROJECT_DIR, 'src', 'cli.ts')
        content = read_file(cli_path)
        if content is None:
            print("FAIL: Component 5 — src/cli.ts not found")
        else:
            has_cli_features = []
            if re.search(r'process\.argv', content):
                has_cli_features.append('argv parsing')
            if re.search(r'import.*Analyzer|import.*analyzer', content):
                has_cli_features.append('analyzer import')
            if re.search(r'import.*Reporter|import.*reporter', content):
                has_cli_features.append('reporter import')

            if len(has_cli_features) >= 2:
                print(f"PASS: Component 5 — src/cli.ts has CLI features: {', '.join(has_cli_features)} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — src/cli.ts only has {has_cli_features}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================================
    # Component 6: Jest tests (>= 15 tests) (0.20 points)
    # =========================================================================
    try:
        tests_dir = os.path.join(PROJECT_DIR, 'tests')
        if not os.path.isdir(tests_dir):
            # Also check __tests__ directory
            tests_dir = os.path.join(PROJECT_DIR, '__tests__')

        if not os.path.isdir(tests_dir):
            print("FAIL: Component 6 — no tests/ or __tests__/ directory found")
        else:
            test_files = [f for f in os.listdir(tests_dir) if f.endswith('.test.ts') or f.endswith('.spec.ts')]
            if not test_files:
                print("FAIL: Component 6 — no test files found in tests/")
            else:
                total_tests = 0
                for tf in test_files:
                    tf_path = os.path.join(tests_dir, tf)
                    content = read_file(tf_path)
                    if content:
                        # Count test() or it() calls
                        test_count = len(re.findall(r'\b(?:test|it)\s*\(', content))
                        total_tests += test_count

                if total_tests >= 15:
                    print(f"PASS: Component 6 — found {total_tests} tests across {len(test_files)} files (0.20 pts)")
                    total_score += 0.20
                elif total_tests >= 10:
                    partial = 0.10
                    print(f"PARTIAL: Component 6 — found {total_tests}/15 tests ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 6 — only found {total_tests}/15 tests")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
