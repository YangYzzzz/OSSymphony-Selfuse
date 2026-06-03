"""
Reward Script: Go Feature Flag System Implementation
Task ID: vscode_gf6_095
Domain: vscode
Scoring:
  1. flag.go struct definition (0.15)
  2. evaluator.go with Evaluate + consistent hashing (0.20)
  3. loader.go with LoadFromFile (0.10)
  4. flags.json with 3 feature flags (0.15)
  5. middleware feature_flags.go (0.10)
  6. Test file covering rollout logic (0.10)
  7. .vscode/tasks.json (0.05)
  8. Go tests pass (0.15)
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-feature-flags')


def verify_task():
    total_score = 0.0

    # Component 1: pkg/flags/flag.go with FeatureFlag struct (0.15 pts)
    try:
        flag_go = os.path.join(PROJECT, 'pkg', 'flags', 'flag.go')
        if not os.path.isfile(flag_go):
            print("FAIL: Component 1 -- pkg/flags/flag.go does not exist")
        else:
            with open(flag_go, 'r') as f:
                content = f.read()

            has_struct = 'type FeatureFlag struct' in content
            has_name = re.search(r'Name\s+string', content) is not None
            has_enabled = re.search(r'Enabled\s+bool', content) is not None
            has_rollout = re.search(r'RolloutPercentage\s+int', content) is not None
            has_variants = re.search(r'Variants\s+map\[string\]string', content) is not None
            has_feature_flags_map = 'FeatureFlags' in content and 'map[string]' in content

            fields_ok = has_name and has_enabled and has_rollout and has_variants
            if has_struct and fields_ok and has_feature_flags_map:
                print(f"PASS: Component 1 -- flag.go has FeatureFlag struct with all required fields (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_struct:
                    missing.append("FeatureFlag struct")
                if not has_name:
                    missing.append("Name field")
                if not has_enabled:
                    missing.append("Enabled field")
                if not has_rollout:
                    missing.append("RolloutPercentage field")
                if not has_variants:
                    missing.append("Variants field")
                if not has_feature_flags_map:
                    missing.append("FeatureFlags map type")
                print(f"FAIL: Component 1 -- flag.go missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: pkg/flags/evaluator.go with Evaluate using consistent hashing (0.20 pts)
    try:
        eval_go = os.path.join(PROJECT, 'pkg', 'flags', 'evaluator.go')
        if not os.path.isfile(eval_go):
            print("FAIL: Component 2 -- pkg/flags/evaluator.go does not exist")
        else:
            with open(eval_go, 'r') as f:
                content = f.read()

            has_evaluate_func = re.search(r'func\s+.*Evaluate\(', content) is not None
            has_hash_import = 'hash' in content
            has_rollout_check = re.search(r'%\s*100', content) is not None
            has_enabled_check = re.search(r'\.Enabled', content) is not None

            if has_evaluate_func and has_hash_import and has_rollout_check and has_enabled_check:
                print(f"PASS: Component 2 -- evaluator.go has Evaluate with consistent hashing (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_evaluate_func:
                    missing.append("Evaluate function")
                if not has_hash_import:
                    missing.append("hash import")
                if not has_rollout_check:
                    missing.append("% 100 rollout check")
                if not has_enabled_check:
                    missing.append(".Enabled check")
                print(f"FAIL: Component 2 -- evaluator.go missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: pkg/flags/loader.go with LoadFromFile (0.10 pts)
    try:
        loader_go = os.path.join(PROJECT, 'pkg', 'flags', 'loader.go')
        if not os.path.isfile(loader_go):
            print("FAIL: Component 3 -- pkg/flags/loader.go does not exist")
        else:
            with open(loader_go, 'r') as f:
                content = f.read()

            has_load_func = re.search(r'func\s+LoadFromFile\(', content) is not None
            has_json_unmarshal = 'json.Unmarshal' in content or 'json.Decode' in content or 'json.NewDecoder' in content
            has_os_read = 'os.ReadFile' in content or 'os.Open' in content or 'ioutil.ReadFile' in content

            if has_load_func and has_json_unmarshal and has_os_read:
                print(f"PASS: Component 3 -- loader.go has LoadFromFile reading JSON (0.10 pts)")
                total_score += 0.10
            else:
                missing = []
                if not has_load_func:
                    missing.append("LoadFromFile function")
                if not has_json_unmarshal:
                    missing.append("JSON parsing")
                if not has_os_read:
                    missing.append("file reading")
                print(f"FAIL: Component 3 -- loader.go missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: flags.json with 3 feature flags (0.15 pts)
    try:
        flags_json = os.path.join(PROJECT, 'flags.json')
        if not os.path.isfile(flags_json):
            print("FAIL: Component 4 -- flags.json does not exist")
        else:
            with open(flags_json, 'r') as f:
                data = json.load(f)

            # Should be a list (or dict) of flag definitions
            if isinstance(data, list):
                flag_count = len(data)
            elif isinstance(data, dict):
                flag_count = len(data)
            else:
                flag_count = 0

            # Verify each flag has required fields and different rollout percentages
            has_valid_flags = False
            if flag_count >= 3:
                rollout_pcts = set()
                valid_count = 0
                items = data if isinstance(data, list) else list(data.values())
                for item in items:
                    if isinstance(item, dict) and 'name' in item and 'enabled' in item and 'rollout_percentage' in item:
                        valid_count += 1
                        rollout_pcts.add(item['rollout_percentage'])
                has_valid_flags = (valid_count >= 3) and len(rollout_pcts) >= 2  # different rollout percentages

            if flag_count >= 3 and has_valid_flags:
                print(f"PASS: Component 4 -- flags.json has {flag_count} valid flags with varied rollout (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- flags.json has {flag_count} flags, valid={has_valid_flags}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: internal/middleware/feature_flags.go (0.10 pts)
    try:
        middleware_go = os.path.join(PROJECT, 'internal', 'middleware', 'feature_flags.go')
        if not os.path.isfile(middleware_go):
            print("FAIL: Component 5 -- internal/middleware/feature_flags.go does not exist")
        else:
            with open(middleware_go, 'r') as f:
                content = f.read()

            has_http = 'net/http' in content
            has_context = 'context' in content
            has_middleware_func = re.search(r'func\s+\w*[Mm]iddleware', content) is not None
            has_context_value = 'context.WithValue' in content or 'WithValue' in content

            if has_http and has_context and has_middleware_func and has_context_value:
                print(f"PASS: Component 5 -- feature_flags.go middleware adds evaluator to context (0.10 pts)")
                total_score += 0.10
            else:
                missing = []
                if not has_http:
                    missing.append("net/http import")
                if not has_context:
                    missing.append("context usage")
                if not has_middleware_func:
                    missing.append("middleware function")
                if not has_context_value:
                    missing.append("context.WithValue")
                print(f"FAIL: Component 5 -- feature_flags.go missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Test file covering rollout logic (0.10 pts)
    try:
        test_file = os.path.join(PROJECT, 'pkg', 'flags', 'evaluator_test.go')
        if not os.path.isfile(test_file):
            print("FAIL: Component 6 -- evaluator_test.go does not exist")
        else:
            with open(test_file, 'r') as f:
                content = f.read()

            has_testing = '"testing"' in content
            has_test_funcs = len(re.findall(r'func\s+Test\w+\(', content)) >= 3

            # Check for tests covering different rollout scenarios
            tests_zero = bool(re.search(r'(?i)(zero|0)\s*(%|percent|Percent|Rollout)', content))
            tests_hundred = bool(re.search(r'(?i)(hundred|100)\s*(%|percent|Percent|Rollout)', content))
            tests_fifty = bool(re.search(r'(?i)(fifty|50)\s*(%|percent|Percent|Rollout)', content))
            tests_99 = bool(re.search(r'(?i)(ninety.?nine|99)\s*(%|percent|Percent|Rollout)', content))
            rollout_coverage = sum([tests_zero, tests_hundred, tests_fifty, tests_99])

            if has_testing and has_test_funcs and rollout_coverage >= 2:
                print(f"PASS: Component 6 -- test file covers rollout logic ({rollout_coverage} scenarios) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- test file: testing={has_testing}, test_funcs={has_test_funcs}, rollout_coverage={rollout_coverage}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: .vscode/tasks.json with test task (0.05 pts)
    try:
        tasks_json = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_json):
            print("FAIL: Component 7 -- .vscode/tasks.json does not exist")
        else:
            with open(tasks_json, 'r') as f:
                content = f.read()

            # Strip comments for JSON parsing
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            data = json.loads(content_clean)

            has_tasks = 'tasks' in data and len(data['tasks']) > 0
            has_test_command = False
            if has_tasks:
                has_test_command = any(
                    'go test' in t.get('command', '') or 'test' in t.get('label', '').lower()
                    for t in data['tasks']
                )

            if has_tasks and has_test_command:
                print(f"PASS: Component 7 -- tasks.json has test task (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 -- tasks.json: has_tasks={has_tasks}, has_test_cmd={has_test_command}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: Go tests pass (0.15 pts)
    try:
        go_bin = '/home/user/go-sdk/go/bin/go'
        if not os.path.isfile(go_bin):
            for candidate in ['/usr/local/go/bin/go', '/usr/bin/go']:
                if os.path.isfile(candidate):
                    go_bin = candidate
                    break

        if os.path.isfile(go_bin):
            cmd = f'cd {PROJECT} && PATH={os.path.dirname(go_bin)}:$PATH {go_bin} test ./... 2>&1'
            stream = os.popen(cmd)
            output = stream.read()
            exit_code = stream.close()  # None means success (exit code 0)
            if exit_code is None:
                print(f"PASS: Component 8 -- go test ./... passed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 8 -- go test failed: {output.strip()}")
        else:
            print(f"FAIL: Component 8 -- go binary not found")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
