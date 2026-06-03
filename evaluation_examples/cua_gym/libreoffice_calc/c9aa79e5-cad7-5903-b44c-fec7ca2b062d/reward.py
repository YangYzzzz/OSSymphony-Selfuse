"""
Reward Script: Create CMakeLists.txt for C++ project with pthread linking
Task ID: vscode_lang_081
Domain: vscode (file-based verification)
Scoring:
  Component 1 (0.20) - CMakeLists.txt exists and is parseable
  Component 2 (0.20) - cmake_minimum_required command present
  Component 3 (0.15) - project() command defines project
  Component 4 (0.20) - add_executable(myapp src/main.cpp) defined
  Component 5 (0.10) - find_package(Threads REQUIRED) present
  Component 6 (0.15) - target_link_libraries links myapp to Threads::Threads
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_081'
CMAKE_PATH = os.path.join(WORKDIR, 'projects', 'cppapp', 'CMakeLists.txt')


def verify_task(file_path):
    """
    Verify CMakeLists.txt creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: CMakeLists.txt not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize content for matching: collapse whitespace variations
    content_lower = content.lower()

    # Component 1: CMakeLists.txt has meaningful CMake content (0.20 points)
    # This checks that the file is not empty and contains cmake-like directives
    try:
        has_cmake_content = (
            len(content.strip()) > 20
            and ('cmake' in content_lower or 'add_executable' in content_lower or 'project' in content_lower)
        )
        if has_cmake_content:
            print(f"PASS: Component 1 - CMakeLists.txt has valid CMake content ({len(content.strip())} chars) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - CMakeLists.txt is empty or has no CMake content")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: cmake_minimum_required command present (0.20 points)
    try:
        # Match cmake_minimum_required(VERSION X.Y) with flexible whitespace
        cmake_min_pattern = re.compile(
            r'cmake_minimum_required\s*\(\s*VERSION\s+[\d.]+\s*\)',
            re.IGNORECASE
        )
        if cmake_min_pattern.search(content):
            match = cmake_min_pattern.search(content)
            print(f"PASS: Component 2 - cmake_minimum_required found: {match.group().strip()} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - cmake_minimum_required(VERSION X.Y) not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: project() command defines the project (0.15 points)
    try:
        # Match project(myapp ...) - the project name should be myapp or similar
        project_pattern = re.compile(
            r'project\s*\(\s*myapp[\s\))]',
            re.IGNORECASE
        )
        if project_pattern.search(content):
            print(f"PASS: Component 3 - project(myapp) found (0.15 pts)")
            total_score += 0.15
        else:
            # Also check for any project() call
            generic_project = re.compile(r'project\s*\(', re.IGNORECASE)
            if generic_project.search(content):
                print(f"FAIL: Component 3 - project() found but does not name 'myapp'")
            else:
                print(f"FAIL: Component 3 - No project() command found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: add_executable(myapp src/main.cpp) defined (0.20 points)
    try:
        # Match add_executable(myapp src/main.cpp) with flexible whitespace
        add_exec_pattern = re.compile(
            r'add_executable\s*\(\s*myapp\s+src/main\.cpp\s*\)',
            re.IGNORECASE
        )
        if add_exec_pattern.search(content):
            print(f"PASS: Component 4 - add_executable(myapp src/main.cpp) found (0.20 pts)")
            total_score += 0.20
        else:
            # Check for add_executable with myapp but different source
            partial_pattern = re.compile(r'add_executable\s*\(\s*myapp', re.IGNORECASE)
            if partial_pattern.search(content):
                print(f"FAIL: Component 4 - add_executable(myapp ...) found but not with 'src/main.cpp'")
            else:
                print(f"FAIL: Component 4 - No add_executable(myapp ...) found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: find_package(Threads REQUIRED) present (0.10 points)
    try:
        find_threads_pattern = re.compile(
            r'find_package\s*\(\s*Threads\s+REQUIRED\s*\)',
            re.IGNORECASE
        )
        if find_threads_pattern.search(content):
            print(f"PASS: Component 5 - find_package(Threads REQUIRED) found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - find_package(Threads REQUIRED) not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: target_link_libraries links myapp to Threads::Threads (0.15 points)
    try:
        # Match target_link_libraries(myapp ... Threads::Threads ...)
        link_pattern = re.compile(
            r'target_link_libraries\s*\(\s*myapp\s+.*?Threads::Threads',
            re.IGNORECASE | re.DOTALL
        )
        if link_pattern.search(content):
            print(f"PASS: Component 6 - target_link_libraries(myapp ... Threads::Threads) found (0.15 pts)")
            total_score += 0.15
        else:
            # Check for any target_link_libraries with myapp
            partial_link = re.compile(r'target_link_libraries\s*\(\s*myapp', re.IGNORECASE)
            if partial_link.search(content):
                print(f"FAIL: Component 6 - target_link_libraries(myapp ...) found but not linking Threads::Threads")
            else:
                print(f"FAIL: Component 6 - No target_link_libraries(myapp ...) found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CMAKE_PATH):
    print(f"File not found: {CMAKE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CMAKE_PATH)
