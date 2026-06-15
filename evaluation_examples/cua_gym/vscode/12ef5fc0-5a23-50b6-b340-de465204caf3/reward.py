"""
Reward Script: VSCode Go fx dependency injection setup
Task ID: vscode_gf6_082
Domain: vscode
Scoring:
  C1: go.mod contains fx and zap dependencies (0.15)
  C2: user_module.go has fx.Module "user" with 3 providers (0.15)
  C3: db_module.go has database provider with lifecycle hooks (0.15)
  C4: cmd/server/main.go uses fx.New with modules and zap (0.15)
  C5: Test file uses fxtest.New() (0.10)
  C6: .vscode/tasks.json has build/test/run tasks (0.10)
  C7: go build ./... passes (0.10)
  C8: go test ./... passes (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-fx-di')


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def run_go_command(cmd_str):
    """Run a go command using os.popen and return (returncode, output).
    Uses os.system for return code and os.popen for output capture."""
    env_prefix = (
        'export PATH=/home/user/go-sdk/go/bin:$PATH && '
        'export GOPATH=/home/user/go && '
        'export HOME=/home/user && '
        f'cd {PROJECT} && '
    )
    try:
        # Capture output
        stream = os.popen(f'{env_prefix}{cmd_str} 2>&1')
        output = stream.read()
        retcode = stream.close()
        # os.popen close() returns None on success, or exit status
        if retcode is None:
            retcode = 0
        else:
            retcode = retcode >> 8  # extract exit code
        return retcode, output
    except Exception as e:
        return -1, str(e)


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: go.mod has fx and zap dependencies (0.15 points)
    try:
        gomod = read_file(os.path.join(PROJECT, 'go.mod'))
        if gomod is None:
            print("FAIL: Component 1 -- go.mod not found")
        else:
            has_fx = 'go.uber.org/fx' in gomod
            has_zap = 'go.uber.org/zap' in gomod
            if has_fx and has_zap:
                print(f"PASS: Component 1 -- go.mod has fx and zap dependencies (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- go.mod missing: fx={has_fx}, zap={has_zap}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: user_module.go has fx.Module "user" with 3 providers (0.15 points)
    try:
        user_mod = read_file(os.path.join(PROJECT, 'internal', 'module', 'user_module.go'))
        if user_mod is None:
            print("FAIL: Component 2 -- internal/module/user_module.go not found")
        else:
            has_fx_module = bool(re.search(r'fx\.Module\s*\(\s*"user"', user_mod))
            has_repo = 'NewUserRepository' in user_mod
            has_svc = 'NewUserService' in user_mod
            has_handler = 'NewUserHandler' in user_mod
            providers_count = sum([has_repo, has_svc, has_handler])

            if has_fx_module and providers_count == 3:
                print(f"PASS: Component 2 -- user_module.go has fx.Module 'user' with 3 providers (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- fx.Module('user')={has_fx_module}, providers={providers_count}/3")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: db_module.go has database provider with lifecycle hooks (0.15 points)
    try:
        db_mod = read_file(os.path.join(PROJECT, 'internal', 'module', 'db_module.go'))
        if db_mod is None:
            print("FAIL: Component 3 -- internal/module/db_module.go not found")
        else:
            has_fx_provide = 'fx.Provide' in db_mod or 'fx.Module' in db_mod
            has_new_database = 'NewDatabase' in db_mod

            # Check that the database implementation has lifecycle hooks
            # Look in any file under internal/ for fx.Hook or lc.Append
            lifecycle_found = any(
                ('fx.Hook' in (read_file(os.path.join(root, fname)) or '')
                 or 'lc.Append' in (read_file(os.path.join(root, fname)) or '')
                 or 'fx.Lifecycle' in (read_file(os.path.join(root, fname)) or ''))
                for root, dirs, files in os.walk(os.path.join(PROJECT, 'internal'))
                for fname in files
                if fname.endswith('.go')
            )

            if has_fx_provide and has_new_database and lifecycle_found:
                print(f"PASS: Component 3 -- db_module.go provides NewDatabase with lifecycle hooks (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- fx.Provide={has_fx_provide}, NewDatabase={has_new_database}, lifecycle={lifecycle_found}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: cmd/server/main.go uses fx.New with modules and zap (0.15 points)
    try:
        main_go = read_file(os.path.join(PROJECT, 'cmd', 'server', 'main.go'))
        if main_go is None:
            print("FAIL: Component 4 -- cmd/server/main.go not found")
        else:
            has_fx_new = 'fx.New(' in main_go
            has_fx_invoke = 'fx.Invoke' in main_go
            has_zap_import = 'go.uber.org/zap' in main_go
            # Check zap is used as provider (zap.New... or fx.Provide with zap)
            has_zap_provider = bool(re.search(r'zap\.New\w+', main_go))

            if has_fx_new and has_fx_invoke and has_zap_import and has_zap_provider:
                print(f"PASS: Component 4 -- main.go uses fx.New with Invoke and zap logger (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- fx.New={has_fx_new}, fx.Invoke={has_fx_invoke}, zap_import={has_zap_import}, zap_provider={has_zap_provider}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Test file uses fxtest.New() (0.10 points)
    try:
        test_found = any(
            'fxtest.New' in (read_file(os.path.join(root, fname)) or '')
            for root, dirs, files in os.walk(PROJECT)
            for fname in files
            if fname.endswith('_test.go')
        )

        if test_found:
            print(f"PASS: Component 5 -- test file using fxtest.New() found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- no test file with fxtest.New() found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: .vscode/tasks.json has build, test, run tasks (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        tasks_content = read_file(tasks_path)
        if tasks_content is None:
            print("FAIL: Component 6 -- .vscode/tasks.json not found")
        else:
            tasks_json = json.loads(tasks_content)
            task_labels = set()
            for task in tasks_json.get('tasks', []):
                label = task.get('label', '').lower()
                task_labels.add(label)

            has_build = 'build' in task_labels
            has_test = 'test' in task_labels
            has_run = 'run' in task_labels

            if has_build and has_test and has_run:
                print(f"PASS: Component 6 -- tasks.json has build, test, run tasks (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- build={has_build}, test={has_test}, run={has_run}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: go build ./... passes AND there are actual packages (0.10 points)
    # Gate: cmd/server/main.go must exist (task-introduced) to avoid scoring empty projects
    try:
        main_exists = os.path.isfile(os.path.join(PROJECT, 'cmd', 'server', 'main.go'))
        if not main_exists:
            print(f"FAIL: Component 7 -- cmd/server/main.go does not exist, nothing to build")
        else:
            retcode, output = run_go_command('go build ./...')
            if retcode == 0:
                print(f"PASS: Component 7 -- go build ./... passes (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 -- go build failed (rc={retcode}): {output[:200]}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: go test ./... passes (0.10 points)
    try:
        retcode, output = run_go_command('go test ./...')
        if retcode == 0:
            print(f"PASS: Component 8 -- go test ./... passes (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 8 -- go test failed (rc={retcode}): {output[:200]}")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
