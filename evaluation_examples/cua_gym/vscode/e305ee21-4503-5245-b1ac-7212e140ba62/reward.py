"""
Reward Script: C++ Development Environment Setup in VSCode
Task ID: vscode_wf_062
Domain: vscode
Scoring:
  Component 1 (0.20): C/C++ and CMake Tools extensions installed
  Component 2 (0.15): CMakeLists.txt with executable, test, GTest
  Component 3 (0.10): src/main.cpp and tests/test_main.cpp exist with content
  Component 4 (0.20): launch.json with GDB debug config and preLaunchTask
  Component 5 (0.20): tasks.json with cmake configure, build, test tasks
  Component 6 (0.15): settings.json with intelliSenseMode and clang-format
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_062'


def verify_task():
    total_score = 0.0

    # Component 1: Extensions installed (0.20 points)
    # Both ms-vscode.cpptools and ms-vscode.cmake-tools must be installed
    # Check by reading the extensions directory on disk
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = [d.lower() for d in os.listdir(ext_dir) if os.path.isdir(os.path.join(ext_dir, d))]
        else:
            ext_folders = []

        cpptools_installed = any('ms-vscode.cpptools' in d for d in ext_folders)
        cmake_tools_installed = any('ms-vscode.cmake-tools' in d for d in ext_folders)

        if cpptools_installed and cmake_tools_installed:
            print(f"PASS: Component 1 — Both cpptools and cmake-tools extensions installed (0.20 pts)")
            total_score += 0.20
        elif cpptools_installed or cmake_tools_installed:
            print(f"PARTIAL: Component 1 — Only one extension installed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Neither C++ extension installed. Found: {ext_folders}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CMakeLists.txt exists with required content (0.15 points)
    # Must have: project, executable (main), test, GTest linkage
    try:
        cmake_path = os.path.join(PROJECT, 'CMakeLists.txt')
        if not os.path.exists(cmake_path):
            print(f"FAIL: Component 2 — CMakeLists.txt not found")
        else:
            with open(cmake_path, 'r') as f:
                cmake_content = f.read().lower()

            has_project = 'project(' in cmake_content
            has_executable = 'add_executable(' in cmake_content
            has_gtest = 'gtest' in cmake_content
            has_test = 'add_test(' in cmake_content or 'enable_testing()' in cmake_content

            checks_passed = sum([has_project, has_executable, has_gtest, has_test])

            if checks_passed == 4:
                print(f"PASS: Component 2 — CMakeLists.txt has project, executable, GTest, test (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                partial = round(0.15 * checks_passed / 4, 2)
                print(f"PARTIAL: Component 2 — CMakeLists.txt has {checks_passed}/4 items ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — CMakeLists.txt missing key content. project={has_project}, exec={has_executable}, gtest={has_gtest}, test={has_test}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Source files exist with C++ content (0.10 points)
    # src/main.cpp and tests/test_main.cpp must exist with actual code
    try:
        main_cpp = os.path.join(PROJECT, 'src', 'main.cpp')
        test_cpp = os.path.join(PROJECT, 'tests', 'test_main.cpp')

        main_exists = os.path.exists(main_cpp)
        test_exists = os.path.exists(test_cpp)

        main_has_content = False
        test_has_content = False

        if main_exists:
            with open(main_cpp, 'r') as f:
                content = f.read()
            main_has_content = '#include' in content and 'main' in content

        if test_exists:
            with open(test_cpp, 'r') as f:
                content = f.read()
            test_has_content = '#include' in content and ('TEST(' in content or 'test' in content.lower())

        if main_has_content and test_has_content:
            print(f"PASS: Component 3 — Both src/main.cpp and tests/test_main.cpp exist with C++ content (0.10 pts)")
            total_score += 0.10
        elif main_has_content or test_has_content:
            print(f"PARTIAL: Component 3 — Only one source file valid (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Source files missing or empty. main={main_exists}/{main_has_content}, test={test_exists}/{test_has_content}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: launch.json with GDB debug config (0.20 points)
    # Must have: type=cppdbg, MIMode=gdb, preLaunchTask containing "cmake build"
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 4 — launch.json not found")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch = json.loads(content_clean)

            configs = launch.get('configurations', [])
            # Count GDB configs and those with cmake build preLaunchTask
            gdb_count = sum(
                1 for cfg in configs
                if cfg.get('type') == 'cppdbg' and cfg.get('MIMode', '').lower() == 'gdb'
            )
            prelaunch_count = sum(
                1 for cfg in configs
                if cfg.get('type') == 'cppdbg'
                and cfg.get('MIMode', '').lower() == 'gdb'
                and 'cmake' in cfg.get('preLaunchTask', '').lower()
                and 'build' in cfg.get('preLaunchTask', '').lower()
            )

            if gdb_count > 0 and prelaunch_count > 0:
                print(f"PASS: Component 4 — launch.json has GDB config with cmake build preLaunchTask (0.20 pts)")
                total_score += 0.20
            elif gdb_count > 0:
                print(f"PARTIAL: Component 4 — GDB config found but preLaunchTask missing/wrong (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — No GDB debug configuration found in launch.json")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json with cmake configure, build, test tasks (0.20 points)
    # Must have tasks labeled: cmake configure, cmake build, cmake test
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 5 — tasks.json not found")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(content_clean)

            task_labels = set()
            for task in tasks_data.get('tasks', []):
                label = task.get('label', '').lower().strip()
                task_labels.add(label)

            has_configure = any('configure' in l and 'cmake' in l for l in task_labels)
            has_build = any('build' in l and 'cmake' in l for l in task_labels)
            has_test = any('test' in l and ('cmake' in l or 'ctest' in l) for l in task_labels)

            found_count = sum([has_configure, has_build, has_test])

            if found_count == 3:
                print(f"PASS: Component 5 — tasks.json has cmake configure, build, and test tasks (0.20 pts)")
                total_score += 0.20
            elif found_count >= 1:
                partial = round(0.20 * found_count / 3, 2)
                print(f"PARTIAL: Component 5 — {found_count}/3 cmake tasks found ({partial} pts). Labels: {task_labels}")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — No cmake tasks found. Labels: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: settings.json with intelliSenseMode and clang-format (0.15 points)
    # Must have: C_Cpp.default.intelliSenseMode set and clang-format referenced
    try:
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 6 — .vscode/settings.json not found")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            has_intellisense = 'C_Cpp.default.intelliSenseMode' in settings
            # Check for clang-format in any setting value
            settings_str = json.dumps(settings).lower()
            has_clangformat = 'clangformat' in settings_str or 'clang-format' in settings_str or 'clang_format' in settings_str

            has_include_path = 'C_Cpp.default.includePath' in settings

            checks = sum([has_intellisense, has_clangformat, has_include_path])

            if checks == 3:
                print(f"PASS: Component 6 — settings.json has intelliSenseMode, clang-format, includePath (0.15 pts)")
                total_score += 0.15
            elif checks >= 1:
                partial = round(0.15 * checks / 3, 2)
                print(f"PARTIAL: Component 6 — {checks}/3 settings found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — settings.json missing C++ settings")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
