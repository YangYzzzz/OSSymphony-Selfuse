"""
Reward Script: C++ Hardware Simulation Framework in VSCode
Task ID: vscode_gf4_055
Domain: vscode
Scoring:
  Component 1 (0.20): gpio.hpp — GPIO template class with read, write, toggle, callback
  Component 2 (0.20): uart.hpp — UART simulator with send, receive, interrupt buffer
  Component 3 (0.20): rtos.hpp — Cooperative RTOS with create_task, yield, sleep_ms
  Component 4 (0.15): blinky.cpp — Application using GPIO and RTOS
  Component 5 (0.15): CMakeLists.txt — FetchContent for Google Test + test targets
  Component 6 (0.10): Test files — test_gpio.cpp and test_uart.cpp with gtest
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-embedded-sim')


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    total_score = 0.0

    # Component 1: gpio.hpp (0.20 points)
    # Must have GPIO template class with read(), write(), toggle(), and on_change callback
    try:
        gpio_path = os.path.join(PROJECT_DIR, 'src', 'hal', 'gpio.hpp')
        content = read_file(gpio_path)
        if content is None:
            print("FAIL: Component 1 — src/hal/gpio.hpp not found")
        else:
            score_1 = 0.0
            # Check template class with Pin and Direction parameters
            if re.search(r'template\s*<', content) and re.search(r'class\s+GPIO', content):
                score_1 += 0.05
                print("PASS: Component 1a — GPIO template class found")
            else:
                print("FAIL: Component 1a — GPIO template class not found")

            # Check read() method
            if re.search(r'bool\s+read\s*\(', content):
                score_1 += 0.05
                print("PASS: Component 1b — read() method found")
            else:
                print("FAIL: Component 1b — read() method not found")

            # Check write(bool) method
            if re.search(r'void\s+write\s*\(\s*bool', content):
                score_1 += 0.05
                print("PASS: Component 1c — write(bool) method found")
            else:
                print("FAIL: Component 1c — write(bool) method not found")

            # Check toggle() method
            if re.search(r'void\s+toggle\s*\(', content):
                score_1 += 0.025
                print("PASS: Component 1d — toggle() method found")
            else:
                print("FAIL: Component 1d — toggle() method not found")

            # Check callback on state change
            if re.search(r'(on_change|callback|set_on_change|onChange)', content) and \
               re.search(r'std::function', content):
                score_1 += 0.025
                print("PASS: Component 1e — state change callback found")
            else:
                print("FAIL: Component 1e — state change callback not found")

            total_score += score_1
            print(f"  Component 1 subtotal: {score_1}/0.20")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: uart.hpp (0.20 points)
    # Must have UART simulator with send(), receive(timeout_ms), and interrupt-driven RX buffer
    try:
        uart_path = os.path.join(PROJECT_DIR, 'src', 'hal', 'uart.hpp')
        content = read_file(uart_path)
        if content is None:
            print("FAIL: Component 2 — src/hal/uart.hpp not found")
        else:
            score_2 = 0.0
            # Check UART class exists
            if re.search(r'class\s+UART', content):
                score_2 += 0.04
                print("PASS: Component 2a — UART class found")
            else:
                print("FAIL: Component 2a — UART class not found")

            # Check send method (accepts bytes/vector/string)
            if re.search(r'void\s+send\s*\(', content):
                score_2 += 0.04
                print("PASS: Component 2b — send() method found")
            else:
                print("FAIL: Component 2b — send() method not found")

            # Check receive method with timeout
            if re.search(r'receive\s*\(', content) and re.search(r'timeout', content):
                score_2 += 0.04
                print("PASS: Component 2c — receive(timeout) method found")
            else:
                print("FAIL: Component 2c — receive(timeout) method not found")

            # Check interrupt-driven RX buffer (queue/buffer + mutex/lock + callback)
            has_buffer = bool(re.search(r'(rx_buffer|rxBuffer|rx_queue)', content))
            has_interrupt = bool(re.search(r'(interrupt|on_rx|rx_callback|set_rx_interrupt)', content))
            if has_buffer and has_interrupt:
                score_2 += 0.08
                print("PASS: Component 2d — interrupt-driven RX buffer found")
            elif has_buffer:
                score_2 += 0.04
                print("PARTIAL: Component 2d — RX buffer found but no interrupt mechanism")
            else:
                print("FAIL: Component 2d — interrupt-driven RX buffer not found")

            total_score += score_2
            print(f"  Component 2 subtotal: {score_2}/0.20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: rtos.hpp (0.20 points)
    # Must have cooperative RTOS with Task struct, create_task, yield, sleep_ms
    try:
        rtos_path = os.path.join(PROJECT_DIR, 'src', 'scheduler', 'rtos.hpp')
        content = read_file(rtos_path)
        if content is None:
            print("FAIL: Component 3 — src/scheduler/rtos.hpp not found")
        else:
            score_3 = 0.0
            # Check Task struct with name, function, priority, stack_size
            if re.search(r'struct\s+Task', content):
                task_has_fields = 0
                if re.search(r'(std::string|string)\s+\w*name', content):
                    task_has_fields += 1
                if re.search(r'(std::function|function)', content):
                    task_has_fields += 1
                if re.search(r'priority', content):
                    task_has_fields += 1
                if re.search(r'stack_size', content):
                    task_has_fields += 1
                if task_has_fields >= 3:
                    score_3 += 0.05
                    print(f"PASS: Component 3a — Task struct with {task_has_fields}/4 required fields")
                else:
                    print(f"PARTIAL: Component 3a — Task struct found but only {task_has_fields}/4 fields")
            else:
                print("FAIL: Component 3a — Task struct not found")

            # Check RTOS/Scheduler class
            if re.search(r'class\s+(RTOS|Scheduler|RTOSScheduler)', content):
                score_3 += 0.03
                print("PASS: Component 3b — RTOS/Scheduler class found")
            else:
                print("FAIL: Component 3b — RTOS/Scheduler class not found")

            # Check create_task method with name, fn, priority, stack_size params
            if re.search(r'create_task\s*\(', content):
                score_3 += 0.04
                print("PASS: Component 3c — create_task() method found")
            else:
                print("FAIL: Component 3c — create_task() method not found")

            # Check yield method
            if re.search(r'void\s+yield\s*\(', content):
                score_3 += 0.04
                print("PASS: Component 3d — yield() method found")
            else:
                print("FAIL: Component 3d — yield() method not found")

            # Check sleep_ms method
            if re.search(r'sleep_ms\s*\(', content):
                score_3 += 0.04
                print("PASS: Component 3e — sleep_ms() method found")
            else:
                print("FAIL: Component 3e — sleep_ms() method not found")

            total_score += score_3
            print(f"  Component 3 subtotal: {score_3}/0.20")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: blinky.cpp (0.15 points)
    # Must use GPIO and RTOS to simulate LED blinking
    try:
        blinky_path = os.path.join(PROJECT_DIR, 'src', 'app', 'blinky.cpp')
        content = read_file(blinky_path)
        if content is None:
            print("FAIL: Component 4 — src/app/blinky.cpp not found")
        else:
            score_4 = 0.0
            # Check includes GPIO header
            if re.search(r'#include.*gpio\.hpp', content):
                score_4 += 0.05
                print("PASS: Component 4a — includes gpio.hpp")
            else:
                print("FAIL: Component 4a — does not include gpio.hpp")

            # Check includes RTOS header
            if re.search(r'#include.*rtos\.hpp', content):
                score_4 += 0.05
                print("PASS: Component 4b — includes rtos.hpp")
            else:
                print("FAIL: Component 4b — does not include rtos.hpp")

            # Check uses GPIO and RTOS (instantiation/usage)
            uses_gpio = bool(re.search(r'GPIO\s*<', content))
            uses_rtos = bool(re.search(r'(RTOS|rtos)', content))
            if uses_gpio and uses_rtos:
                score_4 += 0.05
                print("PASS: Component 4c — uses GPIO and RTOS")
            elif uses_gpio or uses_rtos:
                score_4 += 0.025
                print(f"PARTIAL: Component 4c — uses {'GPIO' if uses_gpio else 'RTOS'} only")
            else:
                print("FAIL: Component 4c — does not use GPIO or RTOS")

            total_score += score_4
            print(f"  Component 4 subtotal: {score_4}/0.15")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: CMakeLists.txt (0.15 points)
    # Must use FetchContent for Google Test and define test targets
    try:
        cmake_path = os.path.join(PROJECT_DIR, 'CMakeLists.txt')
        content = read_file(cmake_path)
        if content is None:
            print("FAIL: Component 5 — CMakeLists.txt not found")
        else:
            score_5 = 0.0
            # Check FetchContent for Google Test
            has_fetch = bool(re.search(r'FetchContent', content, re.IGNORECASE))
            has_gtest = bool(re.search(r'googletest|gtest', content, re.IGNORECASE))
            if has_fetch and has_gtest:
                score_5 += 0.075
                print("PASS: Component 5a — FetchContent for Google Test found")
            elif has_gtest:
                score_5 += 0.03
                print("PARTIAL: Component 5a — Google Test referenced but no FetchContent")
            else:
                print("FAIL: Component 5a — Google Test + FetchContent not found")

            # Check test targets defined
            has_test_target = bool(re.search(r'add_executable\s*\(\s*test_', content))
            has_enable_testing = bool(re.search(r'enable_testing', content, re.IGNORECASE))
            if has_test_target and has_enable_testing:
                score_5 += 0.075
                print("PASS: Component 5b — test targets and enable_testing found")
            elif has_test_target:
                score_5 += 0.05
                print("PARTIAL: Component 5b — test targets found but no enable_testing")
            else:
                print("FAIL: Component 5b — test targets not found")

            total_score += score_5
            print(f"  Component 5 subtotal: {score_5}/0.15")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Test files (0.10 points)
    # Must have test_gpio.cpp and test_uart.cpp with gtest includes
    try:
        score_6 = 0.0
        tests_dir = os.path.join(PROJECT_DIR, 'tests')

        # Check test_gpio.cpp
        gpio_test = read_file(os.path.join(tests_dir, 'test_gpio.cpp'))
        if gpio_test and re.search(r'#include.*gtest', gpio_test) and \
           re.search(r'TEST\s*\(', gpio_test):
            score_6 += 0.05
            print("PASS: Component 6a — test_gpio.cpp with gtest found")
        else:
            print(f"FAIL: Component 6a — test_gpio.cpp {'not found' if gpio_test is None else 'missing gtest content'}")

        # Check test_uart.cpp
        uart_test = read_file(os.path.join(tests_dir, 'test_uart.cpp'))
        if uart_test and re.search(r'#include.*gtest', uart_test) and \
           re.search(r'TEST\s*\(', uart_test):
            score_6 += 0.05
            print("PASS: Component 6b — test_uart.cpp with gtest found")
        else:
            print(f"FAIL: Component 6b — test_uart.cpp {'not found' if uart_test is None else 'missing gtest content'}")

        total_score += score_6
        print(f"  Component 6 subtotal: {score_6}/0.10")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
