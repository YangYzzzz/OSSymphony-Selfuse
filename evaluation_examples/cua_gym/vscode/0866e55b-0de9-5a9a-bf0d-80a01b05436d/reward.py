"""
Reward Script: Java Design Patterns in Maven project
Task ID: vscode_gf4_036
Domain: vscode
Scoring:
  - Observer pattern implementation (0.15)
  - Builder pattern implementation (0.15)
  - Strategy pattern implementation (0.15)
  - Decorator pattern implementation (0.15)
  - JUnit 5 test files with sufficient @Test methods (0.20)
  - .vscode/tasks.json with mvn test task (0.10)
  - mvn test passes (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'java-design-patterns')
SRC_MAIN = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'patterns')
SRC_TEST = os.path.join(PROJECT, 'src', 'test', 'java', 'com', 'patterns')


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def check_observer_pattern():
    """
    Check Observer pattern: EventManager<T>, EventListener<T> interface, UserService.
    Returns score 0.0-1.0 for this component.
    """
    obs_dir = os.path.join(SRC_MAIN, 'observer')
    if not os.path.isdir(obs_dir):
        print("FAIL: Observer — directory not found")
        return 0.0

    score = 0.0
    total_checks = 3

    # EventListener interface
    el_content = read_file(os.path.join(obs_dir, 'EventListener.java'))
    if 'interface EventListener' in el_content:
        score += 1
        print("PASS: Observer — EventListener interface found")
    else:
        print("FAIL: Observer — EventListener interface missing")

    # EventManager with generic type
    em_content = read_file(os.path.join(obs_dir, 'EventManager.java'))
    if 'class EventManager' in em_content and ('subscribe' in em_content or 'notify' in em_content):
        score += 1
        print("PASS: Observer — EventManager class with subscribe/notify found")
    else:
        print("FAIL: Observer — EventManager class missing or incomplete")

    # UserService using EventManager
    us_content = read_file(os.path.join(obs_dir, 'UserService.java'))
    if 'class UserService' in us_content and 'EventManager' in us_content:
        score += 1
        print("PASS: Observer — UserService using EventManager found")
    else:
        print("FAIL: Observer — UserService missing or not using EventManager")

    return score / total_checks


def check_builder_pattern():
    """
    Check Builder pattern: Pizza class with PizzaBuilder (fluent interface).
    Returns score 0.0-1.0 for this component.
    """
    builder_dir = os.path.join(SRC_MAIN, 'builder')
    if not os.path.isdir(builder_dir):
        print("FAIL: Builder — directory not found")
        return 0.0

    score = 0.0
    total_checks = 3

    # Find Pizza file (could also be named differently)
    pizza_content = ''
    for fname in os.listdir(builder_dir):
        if fname.endswith('.java'):
            content = read_file(os.path.join(builder_dir, fname))
            if 'class Pizza' in content or 'Pizza' in fname:
                pizza_content += content

    if not pizza_content:
        print("FAIL: Builder — No Pizza class found")
        return 0.0

    # Pizza class exists
    if 'class Pizza' in pizza_content:
        score += 1
        print("PASS: Builder — Pizza class found")
    else:
        print("FAIL: Builder — Pizza class missing")

    # PizzaBuilder inner/nested class
    if 'PizzaBuilder' in pizza_content or 'Builder' in pizza_content:
        score += 1
        print("PASS: Builder — PizzaBuilder found")
    else:
        print("FAIL: Builder — PizzaBuilder missing")

    # Fluent interface (methods returning builder type)
    if 'return this' in pizza_content:
        score += 1
        print("PASS: Builder — Fluent interface (return this) found")
    else:
        print("FAIL: Builder — Fluent interface missing")

    return score / total_checks


def check_strategy_pattern():
    """
    Check Strategy pattern: SortStrategy interface, BubbleSortStrategy, QuickSortStrategy, Sorter.
    Returns score 0.0-1.0 for this component.
    """
    strat_dir = os.path.join(SRC_MAIN, 'strategy')
    if not os.path.isdir(strat_dir):
        print("FAIL: Strategy — directory not found")
        return 0.0

    score = 0.0
    total_checks = 4

    all_content = {}
    if os.path.isdir(strat_dir):
        for fname in os.listdir(strat_dir):
            if fname.endswith('.java'):
                all_content[fname] = read_file(os.path.join(strat_dir, fname))

    combined = ' '.join(all_content.values())

    # SortStrategy interface
    if 'interface SortStrategy' in combined:
        score += 1
        print("PASS: Strategy — SortStrategy interface found")
    else:
        print("FAIL: Strategy — SortStrategy interface missing")

    # BubbleSortStrategy
    if 'class BubbleSortStrategy' in combined and 'SortStrategy' in combined:
        score += 1
        print("PASS: Strategy — BubbleSortStrategy found")
    else:
        print("FAIL: Strategy — BubbleSortStrategy missing")

    # QuickSortStrategy
    if 'class QuickSortStrategy' in combined and 'SortStrategy' in combined:
        score += 1
        print("PASS: Strategy — QuickSortStrategy found")
    else:
        print("FAIL: Strategy — QuickSortStrategy missing")

    # Sorter context class
    if 'class Sorter' in combined:
        score += 1
        print("PASS: Strategy — Sorter context class found")
    else:
        print("FAIL: Strategy — Sorter context class missing")

    return score / total_checks


def check_decorator_pattern():
    """
    Check Decorator pattern: Coffee interface, SimpleCoffee, MilkDecorator, SugarDecorator.
    Returns score 0.0-1.0 for this component.
    """
    deco_dir = os.path.join(SRC_MAIN, 'decorator')
    if not os.path.isdir(deco_dir):
        print("FAIL: Decorator — directory not found")
        return 0.0

    score = 0.0
    total_checks = 4

    all_content = {}
    for fname in os.listdir(deco_dir):
        if fname.endswith('.java'):
            all_content[fname] = read_file(os.path.join(deco_dir, fname))

    combined = ' '.join(all_content.values())

    # Coffee interface
    if 'interface Coffee' in combined:
        score += 1
        print("PASS: Decorator — Coffee interface found")
    else:
        print("FAIL: Decorator — Coffee interface missing")

    # SimpleCoffee
    if 'class SimpleCoffee' in combined and ('Coffee' in combined):
        score += 1
        print("PASS: Decorator — SimpleCoffee found")
    else:
        print("FAIL: Decorator — SimpleCoffee missing")

    # MilkDecorator
    if 'class MilkDecorator' in combined and 'Coffee' in combined:
        score += 1
        print("PASS: Decorator — MilkDecorator found")
    else:
        print("FAIL: Decorator — MilkDecorator missing")

    # SugarDecorator
    if 'class SugarDecorator' in combined and 'Coffee' in combined:
        score += 1
        print("PASS: Decorator — SugarDecorator found")
    else:
        print("FAIL: Decorator — SugarDecorator missing")

    return score / total_checks


def check_test_files():
    """
    Check JUnit 5 test files: at least 3 test classes with at least 3 @Test methods each.
    Returns score 0.0-1.0 for this component.
    """
    if not os.path.isdir(SRC_TEST):
        print("FAIL: Tests — src/test directory not found")
        return 0.0

    # Walk all test files
    test_files = []
    for root, dirs, files in os.walk(SRC_TEST):
        for fname in files:
            if fname.endswith('Test.java') or fname.endswith('Tests.java'):
                test_files.append(os.path.join(root, fname))

    if not test_files:
        print("FAIL: Tests — no test files found")
        return 0.0

    # Count test files with >= 3 @Test methods
    qualifying_files = 0
    for tf in test_files:
        content = read_file(tf)
        test_count = content.count('@Test')
        if test_count >= 3:
            qualifying_files += 1
            print(f"PASS: Tests — {os.path.basename(tf)} has {test_count} @Test methods")
        else:
            print(f"INFO: Tests — {os.path.basename(tf)} has {test_count} @Test methods (need >= 3)")

    print(f"INFO: Tests — {qualifying_files} qualifying test files (need >= 3)")

    if qualifying_files >= 4:
        return 1.0
    elif qualifying_files >= 3:
        return 0.75
    elif qualifying_files >= 2:
        return 0.5
    elif qualifying_files >= 1:
        return 0.25
    else:
        return 0.0


def check_tasks_json():
    """
    Check .vscode/tasks.json has mvn test task.
    Returns score 0.0-1.0 for this component.
    """
    tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
    if not os.path.exists(tasks_path):
        print("FAIL: tasks.json — file not found")
        return 0.0

    try:
        with open(tasks_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        tasks_config = json.loads(content_clean)
    except Exception as e:
        print(f"FAIL: tasks.json — cannot parse: {e}")
        return 0.0

    tasks = tasks_config.get('tasks', [])
    for task in tasks:
        cmd = task.get('command', '')
        label = task.get('label', '')
        # Check if any task runs mvn test
        if 'mvn test' in cmd or 'mvn test' in label:
            print(f"PASS: tasks.json — found mvn test task (label: {label})")
            return 1.0

    print("FAIL: tasks.json — no mvn test task found")
    return 0.0


def check_mvn_test():
    """
    Run mvn test and check it passes.
    Returns score 0.0-1.0 for this component.
    """
    import subprocess as sp
    import glob as globmod
    # Find mvn binary — may be installed via sdkman or system package
    mvn_bin = 'mvn'
    sdkman_candidates = globmod.glob('/home/user/.sdkman/candidates/maven/*/bin/mvn')
    if sdkman_candidates:
        mvn_bin = sdkman_candidates[0]
    elif os.path.exists('/usr/share/maven/bin/mvn'):
        mvn_bin = '/usr/share/maven/bin/mvn'

    # Also find JAVA_HOME
    env = os.environ.copy()
    java_homes = globmod.glob('/home/user/.sdkman/candidates/java/*/') + globmod.glob('/usr/lib/jvm/java-*/')
    if java_homes:
        env['JAVA_HOME'] = java_homes[0].rstrip('/')
        env['PATH'] = os.path.join(env['JAVA_HOME'], 'bin') + ':' + env.get('PATH', '')

    try:
        result = sp.run(
            [mvn_bin, 'test', '-B'],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        output = result.stdout + result.stderr

        if result.returncode == 0 and 'BUILD SUCCESS' in output:
            # Ensure tests actually ran (not just 0 tests = success)
            # Look for "Tests run: N" where N > 0
            import re as _re
            tests_run_match = _re.search(r'Tests run:\s*(\d+)', output)
            if tests_run_match and int(tests_run_match.group(1)) > 0:
                print(f"PASS: mvn test — BUILD SUCCESS with {tests_run_match.group(1)} tests")
                return 1.0
            else:
                print("FAIL: mvn test — BUILD SUCCESS but no tests ran")
                return 0.0
        elif 'BUILD FAILURE' in output:
            # Check if compilation succeeded but tests failed
            if 'Compilation failure' in output:
                print("FAIL: mvn test — compilation failure")
                return 0.0
            else:
                print("FAIL: mvn test — tests failed but compiled")
                return 0.3
        else:
            print(f"FAIL: mvn test — return code {result.returncode}")
            return 0.0
    except Exception as e:
        print(f"ERROR: mvn test — {e}")
        return 0.0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Observer pattern (0.15 points)
    try:
        obs_score = check_observer_pattern()
        component_score = 0.15 * obs_score
        if obs_score > 0:
            print(f"  -> Observer: {component_score:.3f}/0.15 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: Observer — {e}")

    # Component 2: Builder pattern (0.15 points)
    try:
        build_score = check_builder_pattern()
        component_score = 0.15 * build_score
        if build_score > 0:
            print(f"  -> Builder: {component_score:.3f}/0.15 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: Builder — {e}")

    # Component 3: Strategy pattern (0.15 points)
    try:
        strat_score = check_strategy_pattern()
        component_score = 0.15 * strat_score
        if strat_score > 0:
            print(f"  -> Strategy: {component_score:.3f}/0.15 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: Strategy — {e}")

    # Component 4: Decorator pattern (0.15 points)
    try:
        deco_score = check_decorator_pattern()
        component_score = 0.15 * deco_score
        if deco_score > 0:
            print(f"  -> Decorator: {component_score:.3f}/0.15 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: Decorator — {e}")

    # Component 5: JUnit 5 tests (0.20 points)
    try:
        test_score = check_test_files()
        component_score = 0.20 * test_score
        if test_score > 0:
            print(f"  -> Tests: {component_score:.3f}/0.20 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: Tests — {e}")

    # Component 6: .vscode/tasks.json (0.10 points)
    try:
        tasks_score = check_tasks_json()
        component_score = 0.10 * tasks_score
        if tasks_score > 0:
            print(f"  -> tasks.json: {component_score:.3f}/0.10 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: tasks.json — {e}")

    # Component 7: mvn test passes (0.10 points)
    try:
        mvn_score = check_mvn_test()
        component_score = 0.10 * mvn_score
        if mvn_score > 0:
            print(f"  -> mvn test: {component_score:.3f}/0.10 pts")
        total_score += component_score
    except Exception as e:
        print(f"ERROR: mvn test — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
