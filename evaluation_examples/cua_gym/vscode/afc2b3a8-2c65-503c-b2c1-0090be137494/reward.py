"""
Reward Script: Python Metrics Collector Project
Task ID: vscode_gf4_076
Domain: vscode
Scoring:
  - Component 1: venv exists with required packages (0.15)
  - Component 2: cpu.py collector module with CPUCollector and CPUMetrics (0.10)
  - Component 3: memory.py collector module with MemoryCollector and MemoryMetrics (0.10)
  - Component 4: disk.py collector module with DiskCollector and per-partition usage (0.10)
  - Component 5: network.py collector module with NetworkCollector and bytes_sent/recv per interface (0.10)
  - Component 6: exporter.py with MetricsExporter using prometheus-client Gauges/Counters and FastAPI /metrics (0.15)
  - Component 7: aggregator.py with time-series aggregation min/max/avg/p95 (0.15)
  - Component 8: At least 10 tests exist (0.15)
"""

import os
import ast
import sys
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-metrics-collector')
SRC = os.path.join(PROJECT, 'src')
COLLECTORS = os.path.join(SRC, 'collectors')


def check_file_has_class(file_path, class_name):
    """Parse a Python file and check if it defines a class with the given name."""
    with open(file_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return True
    return False


def check_file_has_method(file_path, class_name, method_name):
    """Parse a Python file and check if a class defines a specific method."""
    with open(file_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                    return True
    return False


def check_file_has_dataclass(file_path, class_name):
    """Check if file defines a dataclass with the given name."""
    with open(file_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Check for @dataclass decorator or just class fields
            return True
    return False


def check_class_has_field(file_path, class_name, field_name):
    """Check if a dataclass-like class has a specific field name."""
    with open(file_path, 'r') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    if item.target.id == field_name:
                        return True
    return False


def count_test_functions(tests_dir):
    """Count the number of test functions (def test_*) across all test files."""
    count = 0
    if not os.path.isdir(tests_dir):
        return 0
    for fname in os.listdir(tests_dir):
        if fname.startswith('test_') and fname.endswith('.py'):
            fpath = os.path.join(tests_dir, fname)
            try:
                with open(fpath, 'r') as f:
                    source = f.read()
                tree = ast.parse(source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        count += 1
            except Exception:
                pass
    return count


def check_file_contains_string(file_path, target_string):
    """Check if a file contains a specific string."""
    with open(file_path, 'r') as f:
        return target_string in f.read()


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: venv exists with required packages (0.15 points)
    # Only scores if venv was CREATED (not present in initial state)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        venv_exists = os.path.isdir(venv_dir)
        if venv_exists:
            # Check for key packages by looking at site-packages
            site_packages = None
            lib_dir = os.path.join(venv_dir, 'lib')
            if os.path.isdir(lib_dir):
                for d in os.listdir(lib_dir):
                    sp = os.path.join(lib_dir, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break

            if site_packages:
                pkg_dirs = os.listdir(site_packages)
                pkg_names = [d.lower().replace('-', '_').split('.')[0] for d in pkg_dirs]
                has_prometheus = any('prometheus' in p for p in pkg_names)
                has_psutil = any('psutil' in p for p in pkg_names)
                has_fastapi = any('fastapi' in p for p in pkg_names)
                has_pytest = any('pytest' in p and p != '_pytest' for p in pkg_names)

                installed_count = sum([has_prometheus, has_psutil, has_fastapi, has_pytest])
                if installed_count >= 3:
                    print(f"PASS: Component 1 — venv exists with {installed_count}/4 key packages (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 1 — venv exists but only {installed_count}/4 key packages found")
            else:
                print("FAIL: Component 1 — venv exists but no site-packages found")
        else:
            print("FAIL: Component 1 — venv directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: cpu.py with CPUCollector class and collect() method, CPUMetrics dataclass (0.10 pts)
    try:
        cpu_path = os.path.join(COLLECTORS, 'cpu.py')
        if not os.path.isfile(cpu_path):
            print("FAIL: Component 2 — src/collectors/cpu.py does not exist")
        else:
            has_collector = check_file_has_class(cpu_path, 'CPUCollector')
            has_collect = check_file_has_method(cpu_path, 'CPUCollector', 'collect')
            has_metrics = check_file_has_class(cpu_path, 'CPUMetrics')
            has_usage = check_class_has_field(cpu_path, 'CPUMetrics', 'usage_percent')
            has_load = check_class_has_field(cpu_path, 'CPUMetrics', 'load_avg')
            has_cores = check_class_has_field(cpu_path, 'CPUMetrics', 'core_count')
            has_freq = check_class_has_field(cpu_path, 'CPUMetrics', 'frequency')

            checks = [has_collector, has_collect, has_metrics, has_usage, has_load, has_cores, has_freq]
            if all(checks):
                print("PASS: Component 2 — cpu.py has CPUCollector.collect() and CPUMetrics with all fields (0.10 pts)")
                total_score += 0.10
            elif has_collector and has_collect and has_metrics:
                print(f"PARTIAL: Component 2 — cpu.py has core structure but missing some fields ({sum(checks)}/7)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 2 — cpu.py missing key classes/methods ({sum(checks)}/7 checks)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: memory.py with MemoryCollector, MemoryMetrics (0.10 pts)
    try:
        mem_path = os.path.join(COLLECTORS, 'memory.py')
        if not os.path.isfile(mem_path):
            print("FAIL: Component 3 — src/collectors/memory.py does not exist")
        else:
            has_collector = check_file_has_class(mem_path, 'MemoryCollector')
            has_collect = check_file_has_method(mem_path, 'MemoryCollector', 'collect')
            has_metrics = check_file_has_class(mem_path, 'MemoryMetrics')
            has_total = check_class_has_field(mem_path, 'MemoryMetrics', 'total')
            has_available = check_class_has_field(mem_path, 'MemoryMetrics', 'available')
            has_percent = check_class_has_field(mem_path, 'MemoryMetrics', 'percent')
            has_swap = check_class_has_field(mem_path, 'MemoryMetrics', 'swap_used')

            checks = [has_collector, has_collect, has_metrics, has_total, has_available, has_percent, has_swap]
            if all(checks):
                print("PASS: Component 3 — memory.py has MemoryCollector.collect() and MemoryMetrics with all fields (0.10 pts)")
                total_score += 0.10
            elif has_collector and has_collect and has_metrics:
                print(f"PARTIAL: Component 3 — memory.py has core structure but missing some fields ({sum(checks)}/7)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 3 — memory.py missing key classes/methods ({sum(checks)}/7 checks)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: disk.py with DiskCollector and per-partition usage (0.10 pts)
    try:
        disk_path = os.path.join(COLLECTORS, 'disk.py')
        if not os.path.isfile(disk_path):
            print("FAIL: Component 4 — src/collectors/disk.py does not exist")
        else:
            has_collector = check_file_has_class(disk_path, 'DiskCollector')
            has_collect = check_file_has_method(disk_path, 'DiskCollector', 'collect')
            # Check for per-partition concept: either a PartitionUsage class or similar
            has_partition_class = check_file_has_class(disk_path, 'PartitionUsage') or \
                                 check_file_has_class(disk_path, 'DiskMetrics')
            has_psutil_ref = check_file_contains_string(disk_path, 'psutil')

            checks = [has_collector, has_collect, has_partition_class, has_psutil_ref]
            if all(checks):
                print("PASS: Component 4 — disk.py has DiskCollector.collect() with per-partition usage (0.10 pts)")
                total_score += 0.10
            elif has_collector and has_collect:
                print(f"PARTIAL: Component 4 — disk.py has DiskCollector but incomplete ({sum(checks)}/4)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — disk.py missing key classes ({sum(checks)}/4 checks)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: network.py with NetworkCollector, bytes_sent/recv per interface (0.10 pts)
    try:
        net_path = os.path.join(COLLECTORS, 'network.py')
        if not os.path.isfile(net_path):
            print("FAIL: Component 5 — src/collectors/network.py does not exist")
        else:
            has_collector = check_file_has_class(net_path, 'NetworkCollector')
            has_collect = check_file_has_method(net_path, 'NetworkCollector', 'collect')
            has_bytes_sent = check_file_contains_string(net_path, 'bytes_sent')
            has_bytes_recv = check_file_contains_string(net_path, 'bytes_recv')
            has_psutil_ref = check_file_contains_string(net_path, 'psutil')

            checks = [has_collector, has_collect, has_bytes_sent, has_bytes_recv, has_psutil_ref]
            if all(checks):
                print("PASS: Component 5 — network.py has NetworkCollector.collect() with bytes_sent/recv (0.10 pts)")
                total_score += 0.10
            elif has_collector and has_collect:
                print(f"PARTIAL: Component 5 — network.py has NetworkCollector but incomplete ({sum(checks)}/5)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — network.py missing key classes ({sum(checks)}/5 checks)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: exporter.py with MetricsExporter, prometheus-client Gauges/Counters, FastAPI /metrics (0.15 pts)
    try:
        exporter_path = os.path.join(SRC, 'exporter.py')
        if not os.path.isfile(exporter_path):
            print("FAIL: Component 6 — src/exporter.py does not exist")
        else:
            has_exporter = check_file_has_class(exporter_path, 'MetricsExporter')
            has_fastapi = check_file_contains_string(exporter_path, 'FastAPI')
            has_gauge = check_file_contains_string(exporter_path, 'Gauge')
            has_counter = check_file_contains_string(exporter_path, 'Counter')
            has_metrics_endpoint = check_file_contains_string(exporter_path, '/metrics')
            has_scrape_interval = check_file_contains_string(exporter_path, 'scrape_interval')

            checks = [has_exporter, has_fastapi, has_gauge, has_counter, has_metrics_endpoint, has_scrape_interval]
            if all(checks):
                print("PASS: Component 6 — exporter.py has MetricsExporter with Gauges/Counters, FastAPI /metrics, and scrape interval (0.15 pts)")
                total_score += 0.15
            elif has_exporter and has_fastapi and has_metrics_endpoint:
                print(f"PARTIAL: Component 6 — exporter.py has core structure but missing some features ({sum(checks)}/6)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 6 — exporter.py missing key structure ({sum(checks)}/6 checks)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: aggregator.py with time-series aggregation min/max/avg/p95 (0.15 pts)
    try:
        agg_path = os.path.join(SRC, 'aggregator.py')
        if not os.path.isfile(agg_path):
            print("FAIL: Component 7 — src/aggregator.py does not exist")
        else:
            # Check for aggregation class and key stats
            has_agg_class = check_file_has_class(agg_path, 'TimeSeriesAggregator') or \
                            check_file_has_class(agg_path, 'Aggregator') or \
                            check_file_has_class(agg_path, 'MetricsAggregator')
            has_result_class = check_file_has_class(agg_path, 'AggregationResult') or \
                               check_file_has_class(agg_path, 'AggregatedMetrics')

            has_min = check_file_contains_string(agg_path, 'min')
            has_max = check_file_contains_string(agg_path, 'max')
            has_avg = check_file_contains_string(agg_path, 'avg') or check_file_contains_string(agg_path, 'mean')
            has_p95 = check_file_contains_string(agg_path, 'p95') or check_file_contains_string(agg_path, '0.95') or check_file_contains_string(agg_path, '95')

            checks = [has_agg_class, has_min, has_max, has_avg, has_p95]
            if all(checks):
                print("PASS: Component 7 — aggregator.py has time-series aggregation with min/max/avg/p95 (0.15 pts)")
                total_score += 0.15
            elif has_agg_class and sum([has_min, has_max, has_avg, has_p95]) >= 2:
                print(f"PARTIAL: Component 7 — aggregator.py has aggregation class but missing some stats ({sum(checks)}/5)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 7 — aggregator.py missing key structure ({sum(checks)}/5 checks)")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: At least 10 test functions exist (0.15 pts)
    try:
        tests_dir = os.path.join(PROJECT, 'tests')
        test_count = count_test_functions(tests_dir)
        if test_count >= 10:
            print(f"PASS: Component 8 — {test_count} test functions found (>= 10 required) (0.15 pts)")
            total_score += 0.15
        elif test_count >= 5:
            print(f"PARTIAL: Component 8 — {test_count} test functions found (>= 10 required)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 8 — only {test_count} test functions found (>= 10 required)")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
