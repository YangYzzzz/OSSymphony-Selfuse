"""
Reward Script: Hierarchical Go Configuration Manager
Task ID: vscode_gf4_067
Domain: vscode
Scoring:
  1. go.mod with correct module path and YAML/TOML deps (0.10)
  2. source.go: ConfigSource interface with Load and Watch (0.15)
  3. FileProvider supporting YAML/JSON/TOML (0.15)
  4. EnvProvider with prefix-based env reading (0.10)
  5. RemoteProvider stub with HTTP polling (0.10)
  6. merger.go: DeepMerge function (0.10)
  7. config.go: Config struct with typed getters (0.15)
  8. 12+ test functions across all test files (0.05)
  9. go test ./... passes (0.10)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-configuration-manager')


def read_file(path):
    """Read a file and return its content, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def count_test_functions(directory):
    """Recursively count Go test functions (func Test...) in _test.go files."""
    count = 0
    for root, dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith('_test.go'):
                content = read_file(os.path.join(root, fname))
                if content:
                    count += len(re.findall(r'func\s+Test\w+\s*\(', content))
    return count


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT):
        print(f"CRITICAL: Project directory not found: {PROJECT}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: go.mod with correct module path and parsing deps (0.10)
    try:
        gomod = read_file(os.path.join(PROJECT, 'go.mod'))
        if gomod is None:
            print("FAIL: Component 1 — go.mod not found")
        else:
            has_module = 'module github.com/user/go-config' in gomod
            # Check for YAML and TOML parsing dependencies
            has_yaml = 'yaml' in gomod.lower()
            has_toml = 'toml' in gomod.lower() or 'BurntSushi' in gomod
            if has_module and has_yaml and has_toml:
                print(f"PASS: Component 1 — go.mod has correct module + YAML/TOML deps (0.10 pts)")
                total_score += 0.10
            elif has_module:
                print(f"PARTIAL: Component 1 — go.mod has module but missing deps (yaml={has_yaml}, toml={has_toml}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 1 — go.mod missing correct module path")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: source.go defines ConfigSource interface with Load and Watch (0.15)
    try:
        source = read_file(os.path.join(PROJECT, 'pkg', 'config', 'source.go'))
        if source is None:
            print("FAIL: Component 2 — pkg/config/source.go not found")
        else:
            has_interface = bool(re.search(r'type\s+ConfigSource\s+interface', source))
            has_load = bool(re.search(r'Load\s*\(\s*\)\s*\(?\s*map\[string\]interface\{\}', source))
            has_watch = bool(re.search(r'Watch\s*\(\s*\w*\s*chan\s+ConfigEvent', source))
            if has_interface and has_load and has_watch:
                print(f"PASS: Component 2 — ConfigSource interface with Load and Watch (0.15 pts)")
                total_score += 0.15
            elif has_interface:
                sub = 0.05
                if has_load:
                    sub += 0.05
                if has_watch:
                    sub += 0.05
                print(f"PARTIAL: Component 2 — interface found but methods incomplete (Load={has_load}, Watch={has_watch}) ({sub} pts)")
                total_score += sub
            else:
                print(f"FAIL: Component 2 — ConfigSource interface not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: FileProvider supporting YAML/JSON/TOML (0.15)
    try:
        fp = read_file(os.path.join(PROJECT, 'pkg', 'config', 'providers', 'file_provider.go'))
        if fp is None:
            print("FAIL: Component 3 — pkg/config/providers/file_provider.go not found")
        else:
            has_struct = bool(re.search(r'type\s+FileProvider\s+struct', fp))
            has_load = bool(re.search(r'func\s+\(\s*\w+\s+\*?FileProvider\s*\)\s+Load\s*\(', fp))
            has_yaml = bool(re.search(r'\.yaml|\.yml', fp, re.IGNORECASE))
            has_json = bool(re.search(r'\.json', fp))
            has_toml = bool(re.search(r'\.toml', fp, re.IGNORECASE))
            formats_count = sum([has_yaml, has_json, has_toml])
            if has_struct and has_load and formats_count >= 2:
                print(f"PASS: Component 3 — FileProvider with YAML={has_yaml}, JSON={has_json}, TOML={has_toml} (0.15 pts)")
                total_score += 0.15
            elif has_struct and has_load:
                print(f"PARTIAL: Component 3 — FileProvider exists but limited formats ({formats_count}/3) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 3 — FileProvider struct/Load not found (struct={has_struct}, load={has_load})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: EnvProvider with prefix-based env reading (0.10)
    try:
        ep = read_file(os.path.join(PROJECT, 'pkg', 'config', 'providers', 'env_provider.go'))
        if ep is None:
            print("FAIL: Component 4 — pkg/config/providers/env_provider.go not found")
        else:
            has_struct = bool(re.search(r'type\s+EnvProvider\s+struct', ep))
            has_prefix = 'Prefix' in ep or 'prefix' in ep
            has_load = bool(re.search(r'func\s+\(\s*\w+\s+\*?EnvProvider\s*\)\s+Load\s*\(', ep))
            has_environ = 'os.Environ' in ep or 'os.Getenv' in ep
            if has_struct and has_load and has_prefix and has_environ:
                print(f"PASS: Component 4 — EnvProvider with prefix and env reading (0.10 pts)")
                total_score += 0.10
            elif has_struct and has_load:
                print(f"PARTIAL: Component 4 — EnvProvider exists but incomplete (prefix={has_prefix}, environ={has_environ}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — EnvProvider struct/Load not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: RemoteProvider stub with HTTP (0.10)
    try:
        rp = read_file(os.path.join(PROJECT, 'pkg', 'config', 'providers', 'remote_provider.go'))
        if rp is None:
            print("FAIL: Component 5 — pkg/config/providers/remote_provider.go not found")
        else:
            has_struct = bool(re.search(r'type\s+RemoteProvider\s+struct', rp))
            has_load = bool(re.search(r'func\s+\(\s*\w+\s+\*?RemoteProvider\s*\)\s+Load\s*\(', rp))
            has_http = 'net/http' in rp or 'http.' in rp
            if has_struct and has_load and has_http:
                print(f"PASS: Component 5 — RemoteProvider stub with HTTP polling (0.10 pts)")
                total_score += 0.10
            elif has_struct:
                print(f"PARTIAL: Component 5 — RemoteProvider struct found but incomplete (load={has_load}, http={has_http}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — RemoteProvider struct not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: merger.go with DeepMerge (0.10)
    try:
        merger = read_file(os.path.join(PROJECT, 'pkg', 'config', 'merger.go'))
        if merger is None:
            print("FAIL: Component 6 — pkg/config/merger.go not found")
        else:
            has_func = bool(re.search(r'func\s+DeepMerge\s*\(', merger)) or bool(re.search(r'func\s+\w*[Mm]erge\s*\(', merger))
            has_recursive = 'map[string]interface{}' in merger
            if has_func and has_recursive:
                print(f"PASS: Component 6 — DeepMerge function with recursive merge (0.10 pts)")
                total_score += 0.10
            elif has_func:
                print(f"PARTIAL: Component 6 — merge function found but may not be recursive (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 — no merge function found in merger.go")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: config.go with Config struct and typed getters (0.15)
    try:
        cfg = read_file(os.path.join(PROJECT, 'pkg', 'config', 'config.go'))
        if cfg is None:
            print("FAIL: Component 7 — pkg/config/config.go not found")
        else:
            has_struct = bool(re.search(r'type\s+Config\s+struct', cfg))
            has_get = bool(re.search(r'func\s+\(\s*\w+\s+\*?Config\s*\)\s+Get\s*\(\s*\w+\s+string\s*\)', cfg))
            has_get_string = bool(re.search(r'func\s+\(\s*\w+\s+\*?Config\s*\)\s+GetString\s*\(', cfg))
            has_get_int = bool(re.search(r'func\s+\(\s*\w+\s+\*?Config\s*\)\s+GetInt\s*\(', cfg))
            has_get_bool = bool(re.search(r'func\s+\(\s*\w+\s+\*?Config\s*\)\s+GetBool\s*\(', cfg))
            has_must_get = bool(re.search(r'func\s+\(\s*\w+\s+\*?Config\s*\)\s+MustGet\s*\(', cfg))
            getters = sum([has_get, has_get_string, has_get_int, has_get_bool, has_must_get])
            if has_struct and getters >= 4:
                print(f"PASS: Component 7 — Config struct with {getters}/5 getters (0.15 pts)")
                total_score += 0.15
            elif has_struct and getters >= 2:
                pts = 0.07
                print(f"PARTIAL: Component 7 — Config struct with {getters}/5 getters ({pts} pts)")
                total_score += pts
            elif has_struct:
                print(f"PARTIAL: Component 7 — Config struct found but few getters ({getters}/5) (0.03 pts)")
                total_score += 0.03
            else:
                print(f"FAIL: Component 7 — Config struct not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: 12+ test functions across all test files (0.05)
    try:
        test_count = count_test_functions(PROJECT)
        if test_count >= 12:
            print(f"PASS: Component 8 — {test_count} test functions found (>= 12) (0.05 pts)")
            total_score += 0.05
        elif test_count >= 6:
            print(f"PARTIAL: Component 8 — {test_count} test functions found (< 12) (0.02 pts)")
            total_score += 0.02
        else:
            print(f"FAIL: Component 8 — only {test_count} test functions found (need >= 12)")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: go test ./... passes (0.10)
    # NOTE: Must use os.popen to invoke Go compiler — no Python library can run Go tests.
    try:
        go_bin = None
        for candidate in ['/home/user/go-sdk/bin/go', '/usr/local/go/bin/go', '/usr/bin/go']:
            if os.path.isfile(candidate):
                go_bin = candidate
                break

        if go_bin is None:
            print("FAIL: Component 9 — Go binary not found on system")
        else:
            go_root = os.path.dirname(os.path.dirname(go_bin))
            cmd = (
                f"cd {PROJECT} && "
                f"PATH={os.path.dirname(go_bin)}:$PATH "
                f"GOROOT={go_root} "
                f"HOME=/home/user "
                f"{go_bin} test ./... 2>&1; echo EXITCODE=$?"
            )
            output = os.popen(cmd).read()
            lines = output.strip().split('\n')
            exit_line = [l for l in lines if l.startswith('EXITCODE=')]
            exit_code = int(exit_line[-1].split('=')[1]) if exit_line else 1
            if exit_code == 0:
                print(f"PASS: Component 9 — go test ./... passes (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 9 — go test ./... failed (rc={exit_code})")
                for line in lines[:10]:
                    print(f"  {line}")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
