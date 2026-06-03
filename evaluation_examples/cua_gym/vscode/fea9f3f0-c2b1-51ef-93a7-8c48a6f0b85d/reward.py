"""
Reward Script: VSCode Node.js performance refactoring with worker_threads
Task ID: vscode_gf6_027
Domain: vscode
Scoring:
  Component 1: clinic installed globally (0.10)
  Component 2: autocannon installed globally (0.10)
  Component 3: processor.js uses worker_threads (0.35)
  Component 4: processNumbers returns a Promise (0.15)
  Component 5: package.json has benchmark script (0.15)
  Component 6: .vscode/tasks.json has Benchmark API task (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'node-perf')
TASK_ID = 'vscode_gf6_027'

# NVM setup: node/npm are under nvm
NVM_BIN = '/home/user/.nvm/versions/node/v18.20.8/bin'


def verify_task():
    total_score = 0.0

    # Component 1: clinic installed globally (0.10 points)
    try:
        clinic_path = os.path.join(NVM_BIN, 'clinic')
        if os.path.exists(clinic_path):
            # Verify it's actually the clinic package, not just any file
            npm_modules = '/home/user/.nvm/versions/node/v18.20.8/lib/node_modules/clinic'
            if os.path.isdir(npm_modules):
                print(f"PASS: Component 1 — clinic installed globally (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — clinic binary exists but module dir not found")
        else:
            print(f"FAIL: Component 1 — clinic not found at {clinic_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: autocannon installed globally (0.10 points)
    try:
        autocannon_path = os.path.join(NVM_BIN, 'autocannon')
        if os.path.exists(autocannon_path):
            npm_modules = '/home/user/.nvm/versions/node/v18.20.8/lib/node_modules/autocannon'
            if os.path.isdir(npm_modules):
                print(f"PASS: Component 2 — autocannon installed globally (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — autocannon binary exists but module dir not found")
        else:
            print(f"FAIL: Component 2 — autocannon not found at {autocannon_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: processor.js uses worker_threads (0.35 points)
    processor_path = os.path.join(PROJECT, 'src', 'workers', 'processor.js')
    try:
        if not os.path.exists(processor_path):
            print(f"FAIL: Component 3 — processor.js not found")
        else:
            with open(processor_path, 'r') as f:
                content = f.read()

            # Check for worker_threads import/require
            has_worker_threads = bool(re.search(r"require\s*\(\s*['\"]worker_threads['\"]\s*\)", content))
            # Check for Worker usage
            has_worker = 'Worker' in content and 'isMainThread' in content
            # Check for parentPort (worker communication)
            has_parent_port = 'parentPort' in content

            if has_worker_threads and has_worker and has_parent_port:
                print(f"PASS: Component 3 — processor.js uses worker_threads with Worker, isMainThread, parentPort (0.35 pts)")
                total_score += 0.35
            else:
                missing = []
                if not has_worker_threads:
                    missing.append("worker_threads require")
                if not has_worker:
                    missing.append("Worker/isMainThread")
                if not has_parent_port:
                    missing.append("parentPort")
                print(f"FAIL: Component 3 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: processNumbers returns a Promise (0.15 points)
    try:
        if os.path.exists(processor_path):
            with open(processor_path, 'r') as f:
                content = f.read()

            # The refactored processNumbers should return a Promise
            has_promise = bool(re.search(r'new\s+Promise', content))
            # Also check that processNumbers function exists and wraps the worker
            has_process_numbers = bool(re.search(r'function\s+processNumbers', content))
            # Check for new Worker creation inside the function
            has_new_worker = bool(re.search(r'new\s+Worker\s*\(', content))

            if has_promise and has_process_numbers and has_new_worker:
                print(f"PASS: Component 4 — processNumbers returns Promise wrapping Worker (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_promise:
                    missing.append("new Promise")
                if not has_process_numbers:
                    missing.append("processNumbers function")
                if not has_new_worker:
                    missing.append("new Worker()")
                print(f"FAIL: Component 4 — Missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 4 — processor.js not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: package.json has benchmark script (0.15 points)
    pkg_path = os.path.join(PROJECT, 'package.json')
    try:
        if not os.path.exists(pkg_path):
            print(f"FAIL: Component 5 — package.json not found")
        else:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)

            scripts = pkg.get('scripts', {})
            benchmark_script = scripts.get('benchmark', '')

            if benchmark_script and 'autocannon' in benchmark_script.lower():
                print(f"PASS: Component 5 — package.json has benchmark script with autocannon: '{benchmark_script}' (0.15 pts)")
                total_score += 0.15
            elif benchmark_script:
                print(f"FAIL: Component 5 — benchmark script exists but doesn't use autocannon: '{benchmark_script}'")
            else:
                print(f"FAIL: Component 5 — No 'benchmark' script in package.json. Scripts: {list(scripts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json has Benchmark API task (0.15 points)
    tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
    try:
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 6 — .vscode/tasks.json not found")
        else:
            with open(tasks_path, 'r') as f:
                # Handle JSONC (comments)
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_config = json.loads(content_clean)

            tasks = tasks_config.get('tasks', [])
            benchmark_task = None
            for task in tasks:
                label = task.get('label', '')
                if 'benchmark' in label.lower() and 'api' in label.lower():
                    benchmark_task = task
                    break

            if benchmark_task:
                # The task exists with the right label — award points
                task_type = benchmark_task.get('type', '')
                if benchmark_task.get('label', ''):
                    print(f"PASS: Component 6 — tasks.json has '{benchmark_task.get('label')}' task (type={task_type}) (0.15 pts)")
                    total_score += 0.15
            else:
                task_labels = [t.get('label', 'unknown') for t in tasks]
                print(f"FAIL: Component 6 — No 'Benchmark API' task found. Tasks: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
