"""
Reward Script: VSCode C++ Pool Allocator Project
Task ID: vscode_gf4_037
Domain: vscode (C++ project)
Scoring:
  Component 1: allocator.hpp with PoolAllocator template (0.25)
  Component 2: allocator_benchmark.cpp with chrono + comparison (0.20)
  Component 3: test_allocator.cpp with Google Test cases (0.20)
  Component 4: CMakeLists.txt with FetchContent + targets (0.20)
  Component 5: cmake build + ctest pass (0.15)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'cpp-memory-allocator')

def verify_task():
    total_score = 0.0

    # Component 1: src/allocator.hpp with PoolAllocator template (0.25 points)
    try:
        hpp_path = os.path.join(PROJECT, 'src', 'allocator.hpp')
        if not os.path.isfile(hpp_path):
            print("FAIL: Component 1 -- src/allocator.hpp does not exist")
        else:
            with open(hpp_path, 'r') as f:
                content = f.read()

            checks = 0
            # Check template class PoolAllocator
            if re.search(r'template\s*<', content) and 'PoolAllocator' in content:
                checks += 1
            else:
                print("FAIL: Component 1a -- no PoolAllocator template class found")

            # Check allocate method
            if re.search(r'\b(T\s*\*|value_type\s*\*)\s*allocate\s*\(', content) or re.search(r'allocate\s*\(', content):
                # More specific: method named allocate that returns pointer
                if 'allocate' in content and 'deallocate' in content:
                    checks += 1
                else:
                    print("FAIL: Component 1b -- allocate/deallocate methods not found")
            else:
                print("FAIL: Component 1b -- allocate method not found")

            # Check deallocate method
            if re.search(r'void\s+deallocate\s*\(', content):
                checks += 1
            else:
                print("FAIL: Component 1c -- deallocate method not found")

            # Check reset method
            if re.search(r'void\s+reset\s*\(', content):
                checks += 1
            else:
                print("FAIL: Component 1d -- reset method not found")

            # Check free list mechanism
            if 'free_list' in content or 'free_list_' in content or 'freeList' in content:
                checks += 1
            else:
                print("FAIL: Component 1e -- no free list mechanism found")

            score_1 = 0.25 * (checks / 5)
            if checks == 5:
                print(f"PASS: Component 1 -- allocator.hpp has PoolAllocator with all methods and free list (0.25 pts)")
            else:
                print(f"PARTIAL: Component 1 -- allocator.hpp has {checks}/5 required elements ({score_1:.3f} pts)")
            total_score += score_1
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: src/allocator_benchmark.cpp with chrono + comparison (0.20 points)
    try:
        bench_path = os.path.join(PROJECT, 'src', 'allocator_benchmark.cpp')
        if not os.path.isfile(bench_path):
            print("FAIL: Component 2 -- src/allocator_benchmark.cpp does not exist")
        else:
            with open(bench_path, 'r') as f:
                content = f.read()

            checks = 0
            # Check high_resolution_clock usage
            if 'high_resolution_clock' in content or 'chrono' in content:
                checks += 1
            else:
                print("FAIL: Component 2a -- no chrono/high_resolution_clock usage")

            # Check PoolAllocator usage
            if 'PoolAllocator' in content:
                checks += 1
            else:
                print("FAIL: Component 2b -- no PoolAllocator usage")

            # Check std::allocator usage
            if 'std::allocator' in content:
                checks += 1
            else:
                print("FAIL: Component 2c -- no std::allocator comparison")

            # Check 100k allocations
            if '100000' in content or '100\'000' in content or '100_000' in content:
                checks += 1
            else:
                print("FAIL: Component 2d -- no 100k allocation count found")

            score_2 = 0.20 * (checks / 4)
            if checks == 4:
                print(f"PASS: Component 2 -- allocator_benchmark.cpp has chrono + PoolAllocator + std::allocator + 100k (0.20 pts)")
            else:
                print(f"PARTIAL: Component 2 -- {checks}/4 required elements ({score_2:.3f} pts)")
            total_score += score_2
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: tests/test_allocator.cpp with Google Test cases (0.20 points)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_allocator.cpp')
        if not os.path.isfile(test_path):
            print("FAIL: Component 3 -- tests/test_allocator.cpp does not exist")
        else:
            with open(test_path, 'r') as f:
                content = f.read()

            checks = 0
            # Check gtest include
            if 'gtest/gtest.h' in content or 'gtest.h' in content:
                checks += 1
            else:
                print("FAIL: Component 3a -- no Google Test include")

            # Check TEST macros (at least 3 test cases)
            test_cases = re.findall(r'TEST\s*\(', content)
            if len(test_cases) >= 3:
                checks += 1
            else:
                print(f"FAIL: Component 3b -- found {len(test_cases)} TEST cases, expected >= 3")

            # Check allocate/deallocate cycle test
            if re.search(r'(allocat|dealloc)', content, re.IGNORECASE):
                checks += 1
            else:
                print("FAIL: Component 3c -- no allocate/deallocate test")

            # Check reuse of freed blocks test
            if re.search(r'(reuse|freed|free)', content, re.IGNORECASE):
                checks += 1
            else:
                print("FAIL: Component 3d -- no block reuse test")

            score_3 = 0.20 * (checks / 4)
            if checks == 4:
                print(f"PASS: Component 3 -- test_allocator.cpp has gtest with >= 3 test cases covering required scenarios (0.20 pts)")
            else:
                print(f"PARTIAL: Component 3 -- {checks}/4 required elements ({score_3:.3f} pts)")
            total_score += score_3
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: CMakeLists.txt with FetchContent + targets (0.20 points)
    try:
        cmake_path = os.path.join(PROJECT, 'CMakeLists.txt')
        if not os.path.isfile(cmake_path):
            print("FAIL: Component 4 -- CMakeLists.txt does not exist")
        else:
            with open(cmake_path, 'r') as f:
                content = f.read()

            checks = 0
            # Check FetchContent for googletest (task-introduced change)
            has_fetchcontent = 'FetchContent' in content and 'googletest' in content.lower()
            if has_fetchcontent:
                checks += 1
            else:
                print("FAIL: Component 4a -- no FetchContent for googletest")

            # Check benchmark target (task-introduced change)
            has_benchmark = bool(re.search(r'add_executable\s*\(\s*\w*benchmark', content, re.IGNORECASE))
            if has_benchmark:
                checks += 1
            else:
                print("FAIL: Component 4b -- no benchmark executable target")

            # Check test target (task-introduced change)
            has_test = bool(re.search(r'add_executable\s*\(\s*\w*test', content, re.IGNORECASE))
            if has_test:
                checks += 1
            else:
                print("FAIL: Component 4c -- no test executable target")

            # Only score if at least one task-introduced change is present
            # C++20 is a precondition (exists in initial), so we don't count it separately
            if checks == 0:
                score_4 = 0.0
                print("FAIL: Component 4 -- no task-introduced CMake changes found")
            else:
                score_4 = 0.20 * (checks / 3)
                if checks == 3:
                    print(f"PASS: Component 4 -- CMakeLists.txt has FetchContent + benchmark + test targets (0.20 pts)")
                else:
                    print(f"PARTIAL: Component 4 -- {checks}/3 required elements ({score_4:.3f} pts)")
            total_score += score_4
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: cmake build + ctest pass (0.15 points)
    try:
        build_dir = os.path.join(PROJECT, 'build')
        # Check build directory exists and has compiled artifacts
        if not os.path.isdir(build_dir):
            print("FAIL: Component 5 -- build directory does not exist")
        else:
            # Check benchmark binary exists
            benchmark_exists = False
            test_exists = False
            for root, dirs, files in os.walk(build_dir):
                for f in files:
                    fpath = os.path.join(root, f)
                    if 'benchmark' in f.lower() and os.access(fpath, os.X_OK):
                        benchmark_exists = True
                    if 'test_allocator' in f.lower() and os.access(fpath, os.X_OK):
                        test_exists = True

            checks = 0
            if benchmark_exists:
                checks += 1
            else:
                print("FAIL: Component 5a -- no benchmark binary found in build/")

            if test_exists:
                checks += 1
            else:
                print("FAIL: Component 5b -- no test_allocator binary found in build/")

            # Check CTestTestfile exists (indicates tests were discovered)
            ctest_file = os.path.join(build_dir, 'CTestTestfile.cmake')
            if os.path.isfile(ctest_file):
                checks += 1
            else:
                print("FAIL: Component 5c -- no CTestTestfile.cmake (tests not discovered)")

            score_5 = 0.15 * (checks / 3)
            if checks == 3:
                print(f"PASS: Component 5 -- build produced benchmark + test binaries and test discovery (0.15 pts)")
            else:
                print(f"PARTIAL: Component 5 -- {checks}/3 build artifacts ({score_5:.3f} pts)")
            total_score += score_5
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
