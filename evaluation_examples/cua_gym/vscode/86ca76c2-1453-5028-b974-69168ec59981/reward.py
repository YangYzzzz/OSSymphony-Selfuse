"""
Reward Script: Lua Scripting Engine Integration for Rust
Task ID: vscode_gf4_093
Domain: vscode
Scoring:
  Component 1 (0.20): Cargo.toml has mlua (lua54, vendored), serde, serde_json, thiserror
  Component 2 (0.20): src/engine.rs exists with ScriptEngine, load_script, call_function, register_api
  Component 3 (0.15): src/api/filesystem.rs with fs.read, fs.write, fs.list Lua bindings
  Component 4 (0.10): src/api/http.rs with http.get Lua binding
  Component 5 (0.10): src/sandbox.rs with timeout-based execution limits
  Component 6 (0.10): scripts/ directory has 3+ .lua example files
  Component 7 (0.15): cargo test passes 10+ tests
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'rust-scripting-engine')


def read_file(path):
    """Safely read a file, return None on failure."""
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

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT):
        print(f"CRITICAL: Project directory not found: {PROJECT}")
        print("REWARD: 0.0")
        return 0.0

    # ================================================================
    # Component 1: Cargo.toml has required dependencies (0.20 points)
    # ================================================================
    try:
        cargo_toml = read_file(os.path.join(PROJECT, 'Cargo.toml'))
        if cargo_toml is None:
            print("FAIL: Component 1 - Cargo.toml not found")
        else:
            deps_found = 0
            total_deps = 4

            # Check mlua with lua54 and vendored features
            if re.search(r'mlua\s*=', cargo_toml):
                if 'lua54' in cargo_toml and 'vendored' in cargo_toml:
                    deps_found += 1
                    print("PASS: Component 1a - mlua with lua54 and vendored features found")
                else:
                    print("FAIL: Component 1a - mlua found but missing lua54/vendored features")
            else:
                print("FAIL: Component 1a - mlua dependency not found")

            # Check serde
            if re.search(r'\bserde\b\s*=', cargo_toml):
                deps_found += 1
                print("PASS: Component 1b - serde dependency found")
            else:
                print("FAIL: Component 1b - serde dependency not found")

            # Check serde_json
            if re.search(r'serde_json\s*=', cargo_toml):
                deps_found += 1
                print("PASS: Component 1c - serde_json dependency found")
            else:
                print("FAIL: Component 1c - serde_json dependency not found")

            # Check thiserror
            if re.search(r'thiserror\s*=', cargo_toml):
                deps_found += 1
                print("PASS: Component 1d - thiserror dependency found")
            else:
                print("FAIL: Component 1d - thiserror dependency not found")

            if deps_found == total_deps:
                print(f"PASS: Component 1 - All {total_deps} dependencies found (0.20 pts)")
                total_score += 0.20
            else:
                partial = 0.20 * (deps_found / total_deps)
                print(f"PARTIAL: Component 1 - {deps_found}/{total_deps} dependencies found ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # ================================================================
    # Component 2: src/engine.rs with ScriptEngine struct and methods (0.20 points)
    # ================================================================
    try:
        engine_rs = read_file(os.path.join(PROJECT, 'src', 'engine.rs'))
        if engine_rs is None:
            print("FAIL: Component 2 - src/engine.rs not found")
        else:
            checks_passed = 0
            total_checks = 4

            # Check ScriptEngine struct
            if re.search(r'struct\s+ScriptEngine', engine_rs):
                checks_passed += 1
                print("PASS: Component 2a - ScriptEngine struct found")
            else:
                print("FAIL: Component 2a - ScriptEngine struct not found")

            # Check load_script method
            if re.search(r'fn\s+load_script', engine_rs):
                checks_passed += 1
                print("PASS: Component 2b - load_script method found")
            else:
                print("FAIL: Component 2b - load_script method not found")

            # Check call_function method
            if re.search(r'fn\s+call_function', engine_rs):
                checks_passed += 1
                print("PASS: Component 2c - call_function method found")
            else:
                print("FAIL: Component 2c - call_function method not found")

            # Check register_api method
            if re.search(r'fn\s+register_api', engine_rs):
                checks_passed += 1
                print("PASS: Component 2d - register_api method found")
            else:
                print("FAIL: Component 2d - register_api method not found")

            if checks_passed == total_checks:
                print(f"PASS: Component 2 - All engine.rs methods present (0.20 pts)")
                total_score += 0.20
            else:
                partial = 0.20 * (checks_passed / total_checks)
                print(f"PARTIAL: Component 2 - {checks_passed}/{total_checks} checks passed ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ================================================================
    # Component 3: src/api/filesystem.rs with fs.read, fs.write, fs.list (0.15 points)
    # ================================================================
    try:
        fs_rs = read_file(os.path.join(PROJECT, 'src', 'api', 'filesystem.rs'))
        if fs_rs is None:
            print("FAIL: Component 3 - src/api/filesystem.rs not found")
        else:
            fs_checks = 0
            total_fs = 3

            # Check for fs.read registration (string "read" being set on table)
            if re.search(r'["\'](read|fs\.read)["\']', fs_rs) or re.search(r'read_fn|read_to_string', fs_rs):
                fs_checks += 1
                print("PASS: Component 3a - fs.read function found")
            else:
                print("FAIL: Component 3a - fs.read function not found")

            # Check for fs.write registration
            if re.search(r'["\'](write|fs\.write)["\']', fs_rs) or re.search(r'write_fn|fs::write', fs_rs):
                fs_checks += 1
                print("PASS: Component 3b - fs.write function found")
            else:
                print("FAIL: Component 3b - fs.write function not found")

            # Check for fs.list registration
            if re.search(r'["\'](list|fs\.list)["\']', fs_rs) or re.search(r'list_fn|read_dir', fs_rs):
                fs_checks += 1
                print("PASS: Component 3c - fs.list function found")
            else:
                print("FAIL: Component 3c - fs.list function not found")

            if fs_checks == total_fs:
                print(f"PASS: Component 3 - All filesystem API functions present (0.15 pts)")
                total_score += 0.15
            else:
                partial = 0.15 * (fs_checks / total_fs)
                print(f"PARTIAL: Component 3 - {fs_checks}/{total_fs} fs functions ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ================================================================
    # Component 4: src/api/http.rs with http.get (0.10 points)
    # ================================================================
    try:
        http_rs = read_file(os.path.join(PROJECT, 'src', 'api', 'http.rs'))
        if http_rs is None:
            print("FAIL: Component 4 - src/api/http.rs not found")
        else:
            # Must have http.get that returns status and body
            has_get = re.search(r'["\'](get|http\.get)["\']', http_rs) or re.search(r'get_fn|http_get', http_rs)
            has_status = 'status' in http_rs
            has_body = 'body' in http_rs

            if has_get and has_status and has_body:
                print("PASS: Component 4 - http.get with status and body found (0.10 pts)")
                total_score += 0.10
            elif has_get:
                print("PARTIAL: Component 4 - http.get found but missing status/body fields (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 4 - http.get function not found in http.rs")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # ================================================================
    # Component 5: src/sandbox.rs with timeout-based execution limits (0.10 points)
    # ================================================================
    try:
        sandbox_rs = read_file(os.path.join(PROJECT, 'src', 'sandbox.rs'))
        if sandbox_rs is None:
            print("FAIL: Component 5 - src/sandbox.rs not found")
        else:
            has_timeout = 'timeout' in sandbox_rs.lower() or 'Timeout' in sandbox_rs
            has_thread = 'thread' in sandbox_rs
            has_memory = 'memory' in sandbox_rs.lower() or 'Memory' in sandbox_rs

            if has_timeout and has_thread:
                if has_memory:
                    print("PASS: Component 5 - sandbox.rs has timeout (thread) and memory limits (0.10 pts)")
                    total_score += 0.10
                else:
                    print("PASS: Component 5 - sandbox.rs has timeout via thread (0.10 pts)")
                    total_score += 0.10
            elif has_timeout:
                print("PARTIAL: Component 5 - sandbox.rs has timeout but no thread-based execution (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 5 - sandbox.rs lacks timeout-based execution limits")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # ================================================================
    # Component 6: scripts/ directory has 3+ .lua example files (0.10 points)
    # ================================================================
    try:
        scripts_dir = os.path.join(PROJECT, 'scripts')
        if not os.path.isdir(scripts_dir):
            print("FAIL: Component 6 - scripts/ directory not found")
        else:
            lua_files = [f for f in os.listdir(scripts_dir) if f.endswith('.lua')]
            if len(lua_files) >= 3:
                print(f"PASS: Component 6 - {len(lua_files)} .lua scripts found: {lua_files} (0.10 pts)")
                total_score += 0.10
            elif len(lua_files) > 0:
                partial = 0.10 * (len(lua_files) / 3)
                print(f"PARTIAL: Component 6 - {len(lua_files)}/3 .lua scripts found ({partial:.2f} pts)")
                total_score += partial
            else:
                print("FAIL: Component 6 - No .lua files found in scripts/")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # ================================================================
    # Component 7: cargo test passes 10+ tests (0.15 points)
    # ================================================================
    try:
        # Count #[test] annotations in all .rs source files as proxy for test count
        test_count = 0
        for root, dirs, files in os.walk(os.path.join(PROJECT, 'src')):
            for fname in files:
                if fname.endswith('.rs'):
                    content = read_file(os.path.join(root, fname))
                    if content:
                        test_count += len(re.findall(r'#\[test\]', content))

        if test_count >= 10:
            print(f"PASS: Component 7 - {test_count} #[test] annotations found (>= 10) (0.15 pts)")
            total_score += 0.15
        elif test_count > 0:
            partial = 0.15 * min(test_count / 10, 1.0)
            print(f"PARTIAL: Component 7 - {test_count}/10 #[test] annotations found ({partial:.2f} pts)")
            total_score += partial
        else:
            print("FAIL: Component 7 - No #[test] annotations found")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
