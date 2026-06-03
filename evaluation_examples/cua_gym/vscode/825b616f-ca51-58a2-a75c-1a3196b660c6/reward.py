"""
Reward Script: Go Event Sourcing Implementation
Task ID: vscode_gf6_089
Domain: vscode
Scoring:
  Component 1 (0.15): aggregate.go exists with AggregateRoot struct, version, uncommittedEvents, Apply method
  Component 2 (0.15): event_store.go exists with EventStore interface and InMemory implementation
  Component 3 (0.20): account.go exists with 3 event types and 3 command methods with validation
  Component 4 (0.15): projections.go exists with AccountBalance read model and RebuildFromEvents
  Component 5 (0.15): account_test.go exists with >= 5 assertions testing event sourcing flow
  Component 6 (0.10): .vscode/tasks.json exists with go test task
  Component 7 (0.10): go test ./... passes
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-event-sourcing')
TASK_ID = 'vscode_gf6_089'


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: aggregate.go (0.15 points)
    # Must have AggregateRoot struct with id, version, uncommittedEvents fields and Apply method
    try:
        content = read_file(os.path.join(PROJECT, 'pkg', 'eventsource', 'aggregate.go'))
        if content is None:
            print("FAIL: Component 1 — pkg/eventsource/aggregate.go not found")
        else:
            has_struct = 'AggregateRoot' in content and 'struct' in content
            has_version = 'version' in content.lower()
            has_uncommitted = 'uncommitted' in content.lower() and 'DomainEvent' in content
            has_apply = re.search(r'func\s+\([^)]*AggregateRoot\)\s+Apply', content) is not None
            checks_passed = sum([has_struct, has_version, has_uncommitted, has_apply])
            if checks_passed == 4:
                print(f"PASS: Component 1 — aggregate.go has AggregateRoot with all required elements (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                partial = 0.15 * checks_passed / 4
                print(f"PARTIAL: Component 1 — aggregate.go has {checks_passed}/4 elements ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — aggregate.go missing key elements (struct={has_struct}, version={has_version}, uncommitted={has_uncommitted}, apply={has_apply})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: event_store.go (0.15 points)
    # Must have EventStore interface with AppendEvents/LoadEvents and InMemory implementation
    try:
        content = read_file(os.path.join(PROJECT, 'pkg', 'eventsource', 'event_store.go'))
        if content is None:
            print("FAIL: Component 2 — pkg/eventsource/event_store.go not found")
        else:
            has_interface = re.search(r'type\s+EventStore\s+interface', content) is not None
            has_append = 'AppendEvents' in content
            has_load = 'LoadEvents' in content
            has_inmemory = re.search(r'type\s+\w*[Ii]n[Mm]emory\w*\s+struct', content) is not None
            checks_passed = sum([has_interface, has_append, has_load, has_inmemory])
            if checks_passed == 4:
                print(f"PASS: Component 2 — event_store.go has EventStore interface and InMemory implementation (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                partial = 0.15 * checks_passed / 4
                print(f"PARTIAL: Component 2 — event_store.go has {checks_passed}/4 elements ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — event_store.go missing key elements (interface={has_interface}, append={has_append}, load={has_load}, inmemory={has_inmemory})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: account.go (0.20 points)
    # Must have Account aggregate with 3 event types and 3 command methods with validation
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'domain', 'account', 'account.go'))
        if content is None:
            print("FAIL: Component 3 — internal/domain/account/account.go not found")
        else:
            # Check for 3 event types
            has_opened = re.search(r'type\s+Account\s*Opened\s+struct', content) is not None
            has_deposited = re.search(r'type\s+Money\s*Deposited\s+struct', content) is not None
            has_withdrawn = re.search(r'type\s+Money\s*Withdrawn\s+struct', content) is not None
            event_count = sum([has_opened, has_deposited, has_withdrawn])

            # Check for 3 command methods (Open, Deposit, Withdraw) on Account
            has_open_cmd = re.search(r'func\s+\([^)]*Account\)\s+Open\s*\(', content) is not None
            has_deposit_cmd = re.search(r'func\s+\([^)]*Account\)\s+Deposit\s*\(', content) is not None
            has_withdraw_cmd = re.search(r'func\s+\([^)]*Account\)\s+Withdraw\s*\(', content) is not None
            cmd_count = sum([has_open_cmd, has_deposit_cmd, has_withdraw_cmd])

            # Check for validation (error returns)
            has_validation = content.count('error') >= 3  # multiple error checks

            total_checks = event_count + cmd_count + (1 if has_validation else 0)
            if total_checks == 7:
                print(f"PASS: Component 3 — account.go has 3 events, 3 commands, and validation (0.20 pts)")
                total_score += 0.20
            elif total_checks >= 4:
                partial = 0.20 * total_checks / 7
                print(f"PARTIAL: Component 3 — account.go has {total_checks}/7 elements ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — account.go missing elements (events={event_count}/3, cmds={cmd_count}/3, validation={has_validation})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: projections.go (0.15 points)
    # Must have AccountBalance read model with RebuildFromEvents
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'domain', 'account', 'projections.go'))
        if content is None:
            print("FAIL: Component 4 — internal/domain/account/projections.go not found")
        else:
            has_balance_struct = re.search(r'type\s+AccountBalance\s+struct', content) is not None
            has_rebuild = re.search(r'func\s+\([^)]*AccountBalance\)\s+RebuildFromEvents', content) is not None
            has_balance_field = 'Balance' in content
            checks_passed = sum([has_balance_struct, has_rebuild, has_balance_field])
            if checks_passed == 3:
                print(f"PASS: Component 4 — projections.go has AccountBalance with RebuildFromEvents (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 1:
                partial = 0.15 * checks_passed / 3
                print(f"PARTIAL: Component 4 — projections.go has {checks_passed}/3 elements ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — projections.go missing key elements")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: account_test.go (0.15 points)
    # Must have test file with >= 5 assertions testing event sourcing flow
    try:
        content = read_file(os.path.join(PROJECT, 'tests', 'account_test.go'))
        if content is None:
            print("FAIL: Component 5 — tests/account_test.go not found")
        else:
            has_testing_import = '"testing"' in content
            has_test_func = re.search(r'func\s+Test\w+\s*\(\s*t\s+\*testing\.T\s*\)', content) is not None
            # Count assertions (t.Error, t.Errorf, t.Fatal, t.Fatalf, or if-check-then-t.Error patterns)
            assertion_count = len(re.findall(r't\.(Error|Errorf|Fatal|Fatalf)\s*\(', content))
            has_enough_assertions = assertion_count >= 5

            # Check flow: open, deposit, withdraw
            has_open_test = re.search(r'\.\s*Open\s*\(', content) is not None
            has_deposit_test = re.search(r'\.\s*Deposit\s*\(', content) is not None
            has_withdraw_test = re.search(r'\.\s*Withdraw\s*\(', content) is not None
            has_full_flow = has_open_test and has_deposit_test and has_withdraw_test

            checks = sum([has_testing_import, has_test_func, has_enough_assertions, has_full_flow])
            if checks == 4:
                print(f"PASS: Component 5 — account_test.go has full flow test with {assertion_count} assertions (0.15 pts)")
                total_score += 0.15
            elif checks >= 2:
                partial = 0.15 * checks / 4
                print(f"PARTIAL: Component 5 — test file has {checks}/4 criteria ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — test file missing (import={has_testing_import}, func={has_test_func}, assertions={assertion_count}>=5={has_enough_assertions}, flow={has_full_flow})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json (0.10 points)
    # Must have a task configuration with go test
    try:
        content = read_file(os.path.join(PROJECT, '.vscode', 'tasks.json'))
        if content is None:
            print("FAIL: Component 6 — .vscode/tasks.json not found")
        else:
            try:
                tasks_config = json.loads(content)
                has_tasks = 'tasks' in tasks_config and len(tasks_config['tasks']) > 0
                # Check that at least one task has "go test" in the command
                has_go_test = has_tasks and any(
                    'go test' in (task.get('command', '') or '') or
                    'go test' in ' '.join(task.get('args', []))
                    for task in tasks_config.get('tasks', [])
                )
                if has_tasks and has_go_test:
                    print(f"PASS: Component 6 — .vscode/tasks.json has go test task (0.10 pts)")
                    total_score += 0.10
                elif has_tasks:
                    print(f"PARTIAL: Component 6 — tasks.json has tasks but no 'go test' command (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 6 — tasks.json has no tasks array or is empty")
            except json.JSONDecodeError:
                # Try stripping comments (JSONC)
                stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                try:
                    tasks_config = json.loads(stripped)
                    if 'tasks' in tasks_config and len(tasks_config['tasks']) > 0:
                        print(f"PASS: Component 6 — .vscode/tasks.json has tasks (JSONC, 0.10 pts)")
                        total_score += 0.10
                    else:
                        print(f"FAIL: Component 6 — tasks.json parsed but no tasks found")
                except:
                    print(f"FAIL: Component 6 — tasks.json is not valid JSON/JSONC")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: go test ./... passes (0.10 points)
    # Run the Go tests to verify they compile and pass
    try:
        # Find go binary
        go_bin = None
        for candidate in ['/home/user/go-sdk/go/bin/go', '/usr/local/go/bin/go', '/usr/bin/go']:
            if os.path.exists(candidate):
                go_bin = candidate
                break

        if go_bin is None:
            print("FAIL: Component 7 — go binary not found on system")
        else:
            env_prefix = f'PATH={os.path.dirname(go_bin)}:$PATH GOPATH={WORKDIR}/go'
            cmd = f'cd {PROJECT} && {env_prefix} {go_bin} test ./... 2>&1'
            pipe = os.popen(cmd)
            output = pipe.read()
            exit_code = pipe.close()  # None means success (exit code 0)
            if exit_code is None:
                print(f"PASS: Component 7 — 'go test ./...' passes (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — 'go test ./...' failed: {output.strip()}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
