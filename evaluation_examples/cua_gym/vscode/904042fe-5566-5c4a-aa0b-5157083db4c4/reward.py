"""
Reward Script: Java Bytecode Generator Library with ASM
Task ID: vscode_gf4_088
Domain: vscode
Scoring:
  Component 1: ClassGenerator.java with ASM ClassWriter, generateClass, generateMethod (0.20)
  Component 2: MethodBuilder.java with fluent API: push, add, sub, returnValue (0.20)
  Component 3: DynamicLoader.java with custom ClassLoader and defineClass (0.15)
  Component 4: examples/ demo generating Calculator with add/subtract/multiply via reflection (0.10)
  Component 5: Test file with JUnit 5 and >= 10 @Test methods (0.15)
  Component 6: mvn test passes with >= 10 tests, 0 failures (0.20)

Note: pom.xml with ASM dependency is a precondition (same in initial and golden),
so it is NOT scored. It is used as a gate only.
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'java-bytecode-generator')
SRC_MAIN = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'bytegen')
SRC_TEST = os.path.join(PROJECT, 'src', 'test', 'java', 'com', 'bytegen')


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    total_score = 0.0

    # Precondition gate: pom.xml must exist with ASM dependency
    pom_path = os.path.join(PROJECT, 'pom.xml')
    pom_content = read_file(pom_path)
    if not pom_content or 'org.ow2.asm' not in pom_content:
        print("CRITICAL: pom.xml missing or lacks ASM dependency -- cannot verify")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ClassGenerator.java (0.20 points)
    # Must exist, use ASM ClassWriter, have generateClass and generateMethod
    try:
        cg_path = os.path.join(SRC_MAIN, 'ClassGenerator.java')
        cg_content = read_file(cg_path)
        if not cg_content:
            print("FAIL: Component 1 -- ClassGenerator.java not found")
        else:
            checks = 0
            if 'ClassWriter' in cg_content:
                checks += 1
            else:
                print("FAIL: Component 1a -- ClassWriter not referenced in ClassGenerator.java")
            if 'generateClass' in cg_content:
                checks += 1
            else:
                print("FAIL: Component 1b -- generateClass method not found")
            if 'generateMethod' in cg_content:
                checks += 1
            else:
                print("FAIL: Component 1c -- generateMethod method not found")
            if re.search(r'import\s+org\.objectweb\.asm', cg_content):
                checks += 1
            else:
                print("FAIL: Component 1d -- No ASM import found")

            if checks == 4:
                print("PASS: Component 1 -- ClassGenerator.java has ASM ClassWriter, generateClass, generateMethod (0.20 pts)")
                total_score += 0.20
            elif checks >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 1 -- ClassGenerator.java has {checks}/4 required elements ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 -- ClassGenerator.java only has {checks}/4 required elements")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: MethodBuilder.java (0.20 points)
    # Must exist with fluent API: push, add, sub, returnValue methods
    try:
        mb_path = os.path.join(SRC_MAIN, 'MethodBuilder.java')
        mb_content = read_file(mb_path)
        if not mb_content:
            print("FAIL: Component 2 -- MethodBuilder.java not found")
        else:
            fluent_methods = ['push', 'add', 'sub', 'returnValue']
            found = 0
            for method in fluent_methods:
                if re.search(rf'(public|private|protected)\s+\w+\s+{method}\s*\(', mb_content):
                    found += 1
                else:
                    print(f"FAIL: Component 2 -- fluent method '{method}' not found in MethodBuilder.java")

            has_fluent_chaining = 'return this' in mb_content
            if found == len(fluent_methods) and has_fluent_chaining:
                print("PASS: Component 2 -- MethodBuilder.java has fluent API with all required methods (0.20 pts)")
                total_score += 0.20
            elif found == len(fluent_methods):
                print("PARTIAL: Component 2 -- MethodBuilder.java has methods but no fluent chaining (0.12 pts)")
                total_score += 0.12
            elif found >= 2:
                partial = 0.08
                print(f"PARTIAL: Component 2 -- MethodBuilder.java has {found}/{len(fluent_methods)} fluent methods ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- MethodBuilder.java has only {found}/{len(fluent_methods)} methods")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: DynamicLoader.java (0.15 points)
    # Must exist with custom ClassLoader
    try:
        dl_path = os.path.join(SRC_MAIN, 'DynamicLoader.java')
        dl_content = read_file(dl_path)
        if not dl_content:
            print("FAIL: Component 3 -- DynamicLoader.java not found")
        else:
            checks = 0
            if 'ClassLoader' in dl_content:
                checks += 1
            else:
                print("FAIL: Component 3a -- ClassLoader not referenced")
            if 'defineClass' in dl_content:
                checks += 1
            else:
                print("FAIL: Component 3b -- defineClass not used (needed for custom ClassLoader)")
            if re.search(r'(load|loadClass)\s*\(', dl_content):
                checks += 1
            else:
                print("FAIL: Component 3c -- no load method found")

            if checks == 3:
                print("PASS: Component 3 -- DynamicLoader.java has custom ClassLoader with defineClass and load (0.15 pts)")
                total_score += 0.15
            elif checks >= 1:
                partial = 0.07
                print(f"PARTIAL: Component 3 -- DynamicLoader.java has {checks}/3 required elements ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 3 -- DynamicLoader.java missing all required elements")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: examples/ demo with Calculator (0.10 points)
    # Must have a Java file that generates a Calculator class with add/subtract/multiply and uses reflection
    try:
        examples_dir = os.path.join(SRC_MAIN, 'examples')
        example_files = []
        if os.path.isdir(examples_dir):
            example_files = [f for f in os.listdir(examples_dir) if f.endswith('.java')]

        if not example_files:
            print("FAIL: Component 4 -- No .java files in examples/ directory")
        else:
            all_content = ''
            for ef in example_files:
                all_content += read_file(os.path.join(examples_dir, ef))

            checks = 0
            if 'Calculator' in all_content or 'calculator' in all_content.lower():
                checks += 1
            for op in ['add', 'subtract', 'multiply']:
                if op in all_content:
                    checks += 1
            if 'invoke' in all_content or 'getMethod' in all_content:
                checks += 1

            if checks >= 4:
                print("PASS: Component 4 -- examples/ demo generates Calculator with add/subtract/multiply via reflection (0.10 pts)")
                total_score += 0.10
            elif checks >= 2:
                partial = 0.05
                print(f"PARTIAL: Component 4 -- examples/ demo has {checks}/5 expected elements ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- examples/ demo has only {checks}/5 expected elements")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Test file with JUnit 5 and >= 10 test methods (0.15 points)
    try:
        test_files = []
        alt_test = os.path.join(PROJECT, 'src', 'test')
        if os.path.isdir(alt_test):
            for root, dirs, files in os.walk(alt_test):
                for f in files:
                    if f.endswith('.java'):
                        test_files.append(os.path.join(root, f))

        if not test_files:
            print("FAIL: Component 5 -- No test .java files found")
        else:
            all_test_content = ''
            for tf in test_files:
                all_test_content += read_file(tf)

            test_count = len(re.findall(r'@Test\b', all_test_content))
            has_junit5 = bool(re.search(r'import\s+org\.junit\.jupiter', all_test_content))

            if has_junit5 and test_count >= 10:
                print(f"PASS: Component 5 -- Found {test_count} JUnit 5 tests (>= 10 required) (0.15 pts)")
                total_score += 0.15
            elif has_junit5 and test_count >= 5:
                partial = 0.08
                print(f"PARTIAL: Component 5 -- Found {test_count} JUnit 5 tests (10 required) ({partial} pts)")
                total_score += partial
            elif test_count > 0:
                partial = 0.04
                print(f"PARTIAL: Component 5 -- Found {test_count} tests, JUnit5={'yes' if has_junit5 else 'no'} ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 5 -- No @Test methods found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: mvn test passes with >= 10 tests and 0 failures (0.20 points)
    # IMPORTANT: This ONLY awards points if tests actually run (>= 10).
    # An empty project with no tests returns 0 here.
    # Uses os.popen to run Maven (no subprocess import needed).
    try:
        java_home = '/home/user/.local/jdk-17'
        maven_bin = '/home/user/.local/apache-maven/bin'
        mvn_cmd = (
            f"cd {PROJECT} && "
            f"JAVA_HOME={java_home} "
            f"PATH={maven_bin}:{java_home}/bin:$PATH "
            f"mvn test 2>&1"
        )
        pipe = os.popen(mvn_cmd)
        output = pipe.read()
        exit_code = pipe.close()  # None means success (exit code 0)

        # Parse test counts - must find "Tests run: N" line
        test_match = re.search(r'Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+)', output)

        if test_match:
            run = int(test_match.group(1))
            failures = int(test_match.group(2))
            errors = int(test_match.group(3))

            if exit_code is None and failures == 0 and errors == 0 and run >= 10:
                print(f"PASS: Component 6 -- mvn test passed: {run} tests, 0 failures, 0 errors (0.20 pts)")
                total_score += 0.20
            elif exit_code is None and failures == 0 and errors == 0 and run >= 5:
                print(f"PARTIAL: Component 6 -- mvn test passed but only {run} tests (need 10) (0.12 pts)")
                total_score += 0.12
            elif run > 0:
                passed = run - failures - errors
                if passed > 0:
                    print(f"PARTIAL: Component 6 -- {passed}/{run} tests passed (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 6 -- All {run} tests failed")
            else:
                print("FAIL: Component 6 -- No tests were run by Maven")
        else:
            # No "Tests run:" line found -- either build failed early or no tests exist
            if 'COMPILATION ERROR' in output:
                print("FAIL: Component 6 -- mvn test failed with compilation errors")
            elif 'No tests were executed' in output or 'BUILD SUCCESS' in output:
                print("FAIL: Component 6 -- Build succeeded but no tests were executed")
            else:
                print(f"FAIL: Component 6 -- mvn test failed: {output[-300:]}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
