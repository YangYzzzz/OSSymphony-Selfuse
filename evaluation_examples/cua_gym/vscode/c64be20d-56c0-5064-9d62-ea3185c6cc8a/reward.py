"""
Reward Script: Java Reactive Streams project with Spring WebFlux and Reactor
Task ID: vscode_gf4_050
Domain: vscode
Scoring:
  C1: FluxPipeline.java with 6+ Flux operators (0.20)
  C2: MonoService.java with WebClient HTTP calls (0.15)
  C3: DataStreamProcessor.java with Publisher + Sinks (0.15)
  C4: BackpressureDemo.java with 3 strategies (0.15)
  C5: 4+ JUnit 5 test files with StepVerifier (0.15)
  C6: .vscode/tasks.json with Maven build/test (0.10)
  C7: pom.xml with WebFlux + Reactor deps (0.10)
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'java-reactive-streams')
SRC_MAIN = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'reactive')
SRC_TEST = os.path.join(PROJECT, 'src', 'test', 'java', 'com', 'reactive')


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    total_score = 0.0

    # Component 1: FluxPipeline.java with 6+ Flux operators (0.20 pts)
    try:
        fp_path = os.path.join(SRC_MAIN, 'FluxPipeline.java')
        content = read_file(fp_path)
        if not content:
            print("FAIL: Component 1 — FluxPipeline.java not found")
        else:
            # Check for at least 6 of the required operators
            required_operators = ['map', 'filter', 'flatMap', 'reduce', 'buffer', 'window']
            found_ops = []
            for op in required_operators:
                # Match operator usage like .map(, .filter(, etc. or method names containing the op
                if re.search(r'\.' + op + r'\s*\(', content):
                    found_ops.append(op)
            if len(found_ops) >= 6:
                print(f"PASS: Component 1 — FluxPipeline.java has all 6 operators: {found_ops} (0.20 pts)")
                total_score += 0.20
            elif len(found_ops) >= 4:
                partial = round(0.20 * len(found_ops) / 6, 2)
                print(f"PARTIAL: Component 1 — FluxPipeline.java has {len(found_ops)}/6 operators: {found_ops} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — FluxPipeline.java has only {len(found_ops)}/6 operators: {found_ops}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: MonoService.java with WebClient-based reactive HTTP calls (0.15 pts)
    try:
        ms_path = os.path.join(SRC_MAIN, 'MonoService.java')
        content = read_file(ms_path)
        if not content:
            print("FAIL: Component 2 — MonoService.java not found")
        else:
            has_webclient = 'WebClient' in content
            has_mono = 'Mono' in content
            has_http_method = bool(re.search(r'\.(get|post|put|delete)\s*\(', content))
            checks_passed = sum([has_webclient, has_mono, has_http_method])
            if checks_passed == 3:
                print(f"PASS: Component 2 — MonoService.java has WebClient ({has_webclient}), Mono ({has_mono}), HTTP methods ({has_http_method}) (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                partial = round(0.15 * checks_passed / 3, 2)
                print(f"PARTIAL: Component 2 — {checks_passed}/3 checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — MonoService.java missing key elements: WebClient={has_webclient}, Mono={has_mono}, HTTP={has_http_method}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: DataStreamProcessor.java with Publisher + Reactor Sinks (0.15 pts)
    try:
        dsp_path = os.path.join(SRC_MAIN, 'DataStreamProcessor.java')
        content = read_file(dsp_path)
        if not content:
            print("FAIL: Component 3 — DataStreamProcessor.java not found")
        else:
            has_publisher = bool(re.search(r'implements\s+Publisher', content))
            has_sinks = 'Sinks' in content
            has_emit = bool(re.search(r'(tryEmitNext|emitNext|emit)', content))
            checks_passed = sum([has_publisher, has_sinks, has_emit])
            if checks_passed == 3:
                print(f"PASS: Component 3 — DataStreamProcessor.java implements Publisher with Sinks (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                partial = round(0.15 * checks_passed / 3, 2)
                print(f"PARTIAL: Component 3 — {checks_passed}/3 checks: Publisher={has_publisher}, Sinks={has_sinks}, emit={has_emit} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — DataStreamProcessor.java missing key elements: Publisher={has_publisher}, Sinks={has_sinks}, emit={has_emit}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: BackpressureDemo.java with 3 strategies (Buffer, Drop, Latest) (0.15 pts)
    try:
        bp_path = os.path.join(SRC_MAIN, 'BackpressureDemo.java')
        content = read_file(bp_path)
        if not content:
            print("FAIL: Component 4 — BackpressureDemo.java not found")
        else:
            strategies = {
                'Buffer': bool(re.search(r'onBackpressureBuffer', content)),
                'Drop': bool(re.search(r'onBackpressureDrop', content)),
                'Latest': bool(re.search(r'onBackpressureLatest', content)),
            }
            found_count = sum(strategies.values())
            if found_count == 3:
                print(f"PASS: Component 4 — BackpressureDemo.java has all 3 strategies: {strategies} (0.15 pts)")
                total_score += 0.15
            elif found_count >= 2:
                partial = round(0.15 * found_count / 3, 2)
                print(f"PARTIAL: Component 4 — {found_count}/3 strategies: {strategies} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — BackpressureDemo.java has only {found_count}/3 strategies: {strategies}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: At least 4 JUnit 5 test files with StepVerifier (0.15 pts)
    try:
        if not os.path.isdir(SRC_TEST):
            print("FAIL: Component 5 — test directory not found")
        else:
            test_files = [f for f in os.listdir(SRC_TEST) if f.endswith('Test.java')]
            valid_test_files = 0
            for tf in test_files:
                tf_content = read_file(os.path.join(SRC_TEST, tf))
                # Must have JUnit 5 annotations AND StepVerifier usage
                has_junit5 = bool(re.search(r'@Test|org\.junit\.jupiter', tf_content))
                has_stepverifier = 'StepVerifier' in tf_content
                if has_junit5 and has_stepverifier:
                    valid_test_files += 1
                    print(f"  TEST OK: {tf} — JUnit5={has_junit5}, StepVerifier={has_stepverifier}")
                elif has_junit5:
                    # Partial: has tests but no StepVerifier
                    valid_test_files += 0.5
                    print(f"  TEST PARTIAL: {tf} — JUnit5={has_junit5}, StepVerifier={has_stepverifier}")

            if valid_test_files >= 4:
                print(f"PASS: Component 5 — {valid_test_files} valid test files found (0.15 pts)")
                total_score += 0.15
            elif valid_test_files >= 2:
                partial = round(0.15 * valid_test_files / 4, 2)
                print(f"PARTIAL: Component 5 — {valid_test_files}/4 valid test files ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — only {valid_test_files}/4 valid test files found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json with Maven build and test tasks (0.10 pts)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        content = read_file(tasks_path)
        if not content:
            print("FAIL: Component 6 — .vscode/tasks.json not found")
        else:
            try:
                tasks_json = json.loads(content)
            except json.JSONDecodeError:
                # Try stripping JSONC comments
                cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_json = json.loads(cleaned)

            tasks_list = tasks_json.get('tasks', [])
            has_build = False
            has_test = False
            for task in tasks_list:
                cmd = task.get('command', '')
                args = task.get('args', [])
                label = task.get('label', '').lower()
                group = task.get('group', '')
                # Check for maven build task
                if 'mvn' in cmd or 'maven' in label:
                    if 'compile' in args or 'install' in args or 'build' in label or group == 'build' or (isinstance(group, dict) and group.get('kind') == 'build'):
                        has_build = True
                    if 'test' in args or 'test' in label or (isinstance(group, dict) and group.get('kind') == 'test'):
                        has_test = True

            if has_build and has_test:
                print(f"PASS: Component 6 — tasks.json has Maven build ({has_build}) and test ({has_test}) tasks (0.10 pts)")
                total_score += 0.10
            elif has_build or has_test:
                print(f"PARTIAL: Component 6 — tasks.json: build={has_build}, test={has_test} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 — tasks.json missing Maven build/test tasks")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: pom.xml has Spring WebFlux and Reactor dependencies (0.10 pts)
    try:
        pom_path = os.path.join(PROJECT, 'pom.xml')
        content = read_file(pom_path)
        if not content:
            print("FAIL: Component 7 — pom.xml not found")
        else:
            # pom.xml exists in both initial and golden; we check for actual source files
            # being present alongside it, which is the task-introduced change.
            # But pom.xml deps are a precondition. Instead, verify that the 4 main
            # source files exist (which is the task-introduced change) combined with
            # pom.xml having the right deps.
            has_webflux = bool(re.search(r'spring-boot-starter-webflux|spring-webflux', content))
            has_reactor = bool(re.search(r'reactor-core|reactor-test', content))

            # The key task-introduced change here: source files exist alongside correct deps
            main_files = ['FluxPipeline.java', 'MonoService.java', 'DataStreamProcessor.java', 'BackpressureDemo.java']
            existing_main = sum(1 for f in main_files if os.path.isfile(os.path.join(SRC_MAIN, f)))

            if has_webflux and has_reactor and existing_main >= 4:
                print(f"PASS: Component 7 — pom.xml has WebFlux={has_webflux}, Reactor={has_reactor}, and {existing_main} source files exist (0.10 pts)")
                total_score += 0.10
            elif existing_main >= 4 and (has_webflux or has_reactor):
                print(f"PARTIAL: Component 7 — deps partial: WebFlux={has_webflux}, Reactor={has_reactor} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 — WebFlux={has_webflux}, Reactor={has_reactor}, source_files={existing_main}/4")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
