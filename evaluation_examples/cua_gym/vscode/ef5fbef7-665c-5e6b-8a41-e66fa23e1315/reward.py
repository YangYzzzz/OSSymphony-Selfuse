"""
Reward Script: Traffic Light State Machine with XState
Task ID: vscode_gf4_039
Domain: vscode
Scoring:
  Component 1: package.json with correct deps (0.15)
  Component 2: tsconfig.json valid config (0.10)
  Component 3: State machine definition (0.25)
  Component 4: Service file with control functions (0.15)
  Component 5: Test file with state transition tests (0.20)
  Component 6: Machine JSON visualization file (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'ts-state-machine')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json has correct dependencies (0.15 points)
    try:
        pkg_path = os.path.join(PROJECT, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        required_deps = {'xstate'}
        required_dev_deps = {'@xstate/test', 'typescript', 'jest', '@types/jest', 'ts-jest'}

        actual_deps = set(pkg.get('dependencies', {}).keys())
        actual_dev_deps = set(pkg.get('devDependencies', {}).keys())
        all_actual = actual_deps | actual_dev_deps

        # xstate must be a dependency
        has_xstate = 'xstate' in all_actual
        # All dev deps must be present (can be in deps or devDeps)
        has_dev_deps = required_dev_deps.issubset(all_actual)
        # jest config should be present (either in package.json or jest.config)
        has_jest_config = 'jest' in pkg or os.path.exists(os.path.join(PROJECT, 'jest.config.js')) or os.path.exists(os.path.join(PROJECT, 'jest.config.ts'))

        if has_xstate and has_dev_deps:
            print(f"PASS: Component 1 — package.json has all required deps (0.15 pts)")
            total_score += 0.15
        elif has_xstate:
            print(f"PARTIAL: Component 1 — xstate present but missing some dev deps. Actual: {all_actual}")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — missing deps. Expected xstate + dev deps. Found: {all_actual}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — package.json not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tsconfig.json is valid TypeScript configuration (0.10 points)
    try:
        tsconfig_path = os.path.join(PROJECT, 'tsconfig.json')
        with open(tsconfig_path, 'r') as f:
            tsconfig = json.load(f)

        compiler_opts = tsconfig.get('compilerOptions', {})
        has_compiler_opts = bool(compiler_opts)
        has_strict_or_target = 'strict' in compiler_opts or 'target' in compiler_opts
        has_module = 'module' in compiler_opts

        if has_compiler_opts and has_strict_or_target and has_module:
            print(f"PASS: Component 2 — tsconfig.json valid with compilerOptions (0.10 pts)")
            total_score += 0.10
        elif has_compiler_opts:
            print(f"PARTIAL: Component 2 — tsconfig.json has compilerOptions but missing strict/target/module")
            total_score += 0.05
        else:
            print(f"FAIL: Component 2 — tsconfig.json missing compilerOptions")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — tsconfig.json not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: State machine definition with correct states and transitions (0.25 points)
    try:
        # Search for the machine file in src/
        machine_file = None
        src_dir = os.path.join(PROJECT, 'src')
        if os.path.isdir(src_dir):
            for fname in os.listdir(src_dir):
                if 'machine' in fname.lower() and fname.endswith('.ts'):
                    machine_file = os.path.join(src_dir, fname)
                    break

        if machine_file is None:
            print(f"FAIL: Component 3 — no machine .ts file found in src/")
        else:
            with open(machine_file, 'r') as f:
                content = f.read()

            # Check for createMachine usage
            uses_create_machine = 'createMachine' in content

            # Check states exist
            has_red = bool(re.search(r"['\"]red['\"]", content))
            has_green = bool(re.search(r"['\"]green['\"]", content))
            has_yellow = bool(re.search(r"['\"]yellow['\"]", content))
            all_states = has_red and has_green and has_yellow

            # Check events (may be quoted or unquoted keys in TS)
            has_timer = 'TIMER' in content
            has_emergency = 'EMERGENCY' in content

            # Check transitions: red->green on TIMER, green->yellow on TIMER, green->red on EMERGENCY, yellow->red on TIMER
            # We check that the content has the right state names and events
            has_all_events = has_timer and has_emergency

            if uses_create_machine and all_states and has_all_events:
                print(f"PASS: Component 3 — machine has createMachine, all 3 states, TIMER and EMERGENCY events (0.25 pts)")
                total_score += 0.25
            elif uses_create_machine and all_states:
                print(f"PARTIAL: Component 3 — machine has createMachine and states but missing events")
                total_score += 0.15
            elif all_states:
                print(f"PARTIAL: Component 3 — states present but no createMachine")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — machine definition incomplete. createMachine={uses_create_machine}, states={has_red}/{has_green}/{has_yellow}, events={has_timer}/{has_emergency}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Service file with control functions (0.15 points)
    try:
        service_file = None
        src_dir = os.path.join(PROJECT, 'src')
        if os.path.isdir(src_dir):
            for fname in os.listdir(src_dir):
                if 'service' in fname.lower() and fname.endswith('.ts'):
                    service_file = os.path.join(src_dir, fname)
                    break

        if service_file is None:
            print(f"FAIL: Component 4 — no service .ts file found in src/")
        else:
            with open(service_file, 'r') as f:
                content = f.read()

            # Check for interpret/start usage
            has_interpret = 'interpret' in content
            has_start = '.start()' in content or 'start(' in content

            # Check for exported control functions
            has_export_funcs = content.count('export function') >= 2 or content.count('export const') >= 2

            # Check imports machine
            imports_machine = 'trafficLight' in content.lower() or 'machine' in content.lower()

            if has_interpret and has_start and has_export_funcs and imports_machine:
                print(f"PASS: Component 4 — service file has interpret, start, exports and imports machine (0.15 pts)")
                total_score += 0.15
            elif has_export_funcs and imports_machine:
                print(f"PARTIAL: Component 4 — service has exports but missing interpret/start")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 — service incomplete. interpret={has_interpret}, start={has_start}, exports={has_export_funcs}, imports_machine={imports_machine}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Test file with state transition tests (0.20 points)
    try:
        test_file = None
        tests_dir = os.path.join(PROJECT, 'tests')
        if os.path.isdir(tests_dir):
            for fname in os.listdir(tests_dir):
                if 'test' in fname.lower() and fname.endswith('.ts'):
                    test_file = os.path.join(tests_dir, fname)
                    break

        # Also check src/ or root for test files
        if test_file is None:
            for search_dir in [os.path.join(PROJECT, 'src'), PROJECT]:
                if os.path.isdir(search_dir):
                    for fname in os.listdir(search_dir):
                        if 'test' in fname.lower() and fname.endswith('.ts'):
                            test_file = os.path.join(search_dir, fname)
                            break
                if test_file:
                    break

        if test_file is None:
            print(f"FAIL: Component 5 — no test .ts file found")
        else:
            with open(test_file, 'r') as f:
                content = f.read()

            # Check test framework usage
            has_describe = 'describe(' in content
            has_test_or_it = 'test(' in content or 'it(' in content
            has_expect = 'expect(' in content

            # Check for state transition testing
            tests_red = bool(re.search(r"['\"]red['\"]", content))
            tests_green = bool(re.search(r"['\"]green['\"]", content))
            tests_yellow = bool(re.search(r"['\"]yellow['\"]", content))
            tests_timer = bool(re.search(r"['\"]TIMER['\"]", content))
            tests_emergency = bool(re.search(r"['\"]EMERGENCY['\"]", content))

            # Check for @xstate/test model-based testing
            has_model_testing = 'createModel' in content or '@xstate/test' in content

            all_transitions = tests_red and tests_green and tests_yellow and tests_timer and tests_emergency
            if has_describe and has_test_or_it and has_expect and all_transitions and has_model_testing:
                print(f"PASS: Component 5 — comprehensive tests with model-based testing (0.20 pts)")
                total_score += 0.20
            elif has_describe and has_test_or_it and has_expect and all_transitions:
                print(f"PARTIAL: Component 5 — tests cover transitions but no model-based testing")
                total_score += 0.15
            elif has_describe and has_test_or_it and has_expect:
                print(f"PARTIAL: Component 5 — test file exists with basic structure but missing transition coverage")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — test file incomplete. describe={has_describe}, test/it={has_test_or_it}, expect={has_expect}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Machine JSON visualization file (0.15 points)
    try:
        json_file = None
        # Search in src/, output/, and project root
        for search_dir in [os.path.join(PROJECT, 'src'), os.path.join(PROJECT, 'output'), PROJECT]:
            if os.path.isdir(search_dir):
                for fname in os.listdir(search_dir):
                    if fname.endswith('.json') and 'machine' in fname.lower():
                        json_file = os.path.join(search_dir, fname)
                        break
            if json_file:
                break

        # Also check for any JSON with traffic light machine definition
        if json_file is None:
            for search_dir in [os.path.join(PROJECT, 'src'), os.path.join(PROJECT, 'output'), PROJECT]:
                if os.path.isdir(search_dir):
                    for fname in os.listdir(search_dir):
                        if fname.endswith('.json') and fname != 'package.json' and fname != 'package-lock.json' and fname != 'tsconfig.json':
                            candidate = os.path.join(search_dir, fname)
                            try:
                                with open(candidate, 'r') as f:
                                    data = json.load(f)
                                if 'states' in data or 'initial' in data:
                                    json_file = candidate
                                    break
                            except Exception:
                                pass
                if json_file:
                    break

        if json_file is None:
            print(f"FAIL: Component 6 — no machine JSON visualization file found")
        else:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Verify JSON has state machine structure
            has_states = 'states' in data
            has_initial = 'initial' in data

            if has_states and has_initial:
                states = data['states']
                has_red_state = 'red' in states
                has_green_state = 'green' in states
                has_yellow_state = 'yellow' in states

                if has_red_state and has_green_state and has_yellow_state:
                    print(f"PASS: Component 6 — JSON visualization has all 3 states (0.15 pts)")
                    total_score += 0.15
                elif has_red_state or has_green_state or has_yellow_state:
                    print(f"PARTIAL: Component 6 — JSON has states but missing some: red={has_red_state}, green={has_green_state}, yellow={has_yellow_state}")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 6 — JSON has states/initial keys but no red/green/yellow states")
            else:
                print(f"FAIL: Component 6 — JSON file doesn't contain state machine structure (states={has_states}, initial={has_initial})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
