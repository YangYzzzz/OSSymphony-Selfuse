"""
Reward Script: Multi-cursor step number comment insertion
Task ID: vscode_rf_038
Domain: vscode
Scoring:
  - Component 1 (0.4): All 20 lines (10-29) have // Step N: prefix
  - Component 2 (0.3): Step numbers are sequential 1-20
  - Component 3 (0.3): Original code preserved after prefix
  Gate: Lines outside 10-29 must be unchanged (precondition, not scored)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_038'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'debug', 'steps.js')

# Known original code for lines 10-29 (0-indexed: lines[9:29])
ORIGINAL_LINES_10_29 = [
    '  let data = JSON.parse(JSON.stringify(rawData));\n',
    '  data = data.filter(record => record.timestamp !== null);\n',
    '  data = data.map(r => ({ ...r, timestamp: new Date(r.timestamp) }));\n',
    '  data.sort((a, b) => a.timestamp - b.timestamp);\n',
    '  data = data.filter(r => r.value >= 0 && r.value <= 1000);\n',
    '  let mean = data.reduce((s, r) => s + r.value, 0) / data.length;\n',
    '  let stdDev = Math.sqrt(data.reduce((s, r) => s + (r.value - mean) ** 2, 0) / data.length);\n',
    '  data = data.filter(r => Math.abs(r.value - mean) <= 3 * stdDev);\n',
    '  data = data.map(r => ({ ...r, normalized: (r.value - mean) / stdDev }));\n',
    '  data = data.map(r => ({ ...r, sensorId: r.sensorId.trim().toUpperCase() }));\n',
    '  let grouped = {};\n',
    '  data.forEach(r => { grouped[r.sensorId] = grouped[r.sensorId] || []; grouped[r.sensorId].push(r); });\n',
    '  Object.keys(grouped).forEach(k => { grouped[k].sort((a, b) => a.timestamp - b.timestamp); });\n',
    '  data = data.map(r => ({ ...r, hour: r.timestamp.getHours() }));\n',
    '  data = data.map(r => ({ ...r, dayOfWeek: r.timestamp.getDay() }));\n',
    '  let duplicates = new Set();\n',
    '  data = data.filter(r => { let key = r.sensorId + "-" + r.timestamp.getTime(); if (duplicates.has(key)) return false; duplicates.add(key); return true; });\n',
    '  data = data.map(r => ({ ...r, quality: r.value > mean ? "high" : "low" }));\n',
    '  data = data.map((r, i) => ({ ...r, index: i + 1 }));\n',
    '  let summary = { total: data.length, sensors: Object.keys(grouped).length, avgValue: mean.toFixed(2) };\n',
]

# Known lines outside the target range that must remain unchanged
HEADER_LINES = [
    '/**\n',
    ' * Data Pipeline Processor\n',
    ' * Processes raw sensor data through a sequential cleaning pipeline.\n',
    ' */\n',
    '\n',
    'const fs = require("fs");\n',
    'const path = require("path");\n',
    '\n',
    'function processPipeline(rawData) {\n',
]

FOOTER_LINES = [
    '  return { processedData: data, summary: summary, groups: grouped };\n',
    '}\n',
    '\n',
    'module.exports = { processPipeline };\n',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(lines) < 29:
        print(f"FAIL: File has only {len(lines)} lines, expected at least 33")
        print("REWARD: 0.0")
        return 0.0

    # GATE: Lines outside 10-29 must be unchanged (precondition, not scored)
    try:
        gate_issues = []
        for i, expected in enumerate(HEADER_LINES):
            if i < len(lines) and lines[i] != expected:
                gate_issues.append(f"Header line {i+1} changed")
                break
        footer_start = 29  # 0-indexed
        for i, expected in enumerate(FOOTER_LINES):
            actual_idx = footer_start + i
            if actual_idx < len(lines) and lines[actual_idx] != expected:
                gate_issues.append(f"Footer line {actual_idx+1} changed")
                break
        if len(gate_issues) > 0:
            print("GATE: File structure corrupted outside target lines — returning 0.0")
            print("REWARD: 0.0")
            return 0.0
        else:
            print("GATE: Lines outside 10-29 unchanged — OK")
    except Exception as e:
        print(f"GATE ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 20 lines (10-29) have // Step N: prefix (0.4 points)
    try:
        prefix_count = 0
        step_pattern = re.compile(r'^// Step \d+:\s')
        for i in range(9, 29):  # 0-indexed lines 10-29
            line = lines[i]
            if step_pattern.match(line):
                prefix_count += 1

        if prefix_count == 20:
            print(f"PASS: Component 1 — All 20 lines have // Step N: prefix (0.4 pts)")
            total_score += 0.4
        elif prefix_count > 0:
            partial = round(0.4 * (prefix_count / 20), 2)
            print(f"PARTIAL: Component 1 — {prefix_count}/20 lines have prefix ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No lines have // Step N: prefix (0 of 20)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Step numbers are sequential 1-20 (0.3 points)
    try:
        correct_numbers = 0
        number_pattern = re.compile(r'^// Step (\d+):')
        for idx, i in enumerate(range(9, 29)):
            expected_num = idx + 1
            line = lines[i]
            m = number_pattern.match(line)
            if m and int(m.group(1)) == expected_num:
                correct_numbers += 1

        if correct_numbers == 20:
            print(f"PASS: Component 2 — All step numbers sequential 1-20 (0.3 pts)")
            total_score += 0.3
        elif correct_numbers > 0:
            partial = round(0.3 * (correct_numbers / 20), 2)
            print(f"PARTIAL: Component 2 — {correct_numbers}/20 correct numbers ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No correct step numbers")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original code preserved after prefix (0.3 points)
    # Each golden line should contain the original code content after the "// Step N: " prefix
    try:
        preserved_count = 0
        for idx, i in enumerate(range(9, 29)):
            line = lines[i]
            original = ORIGINAL_LINES_10_29[idx].rstrip('\n')
            # The original code (with its leading spaces) should appear in the line after the prefix
            prefix_match = re.match(r'^// Step \d+:\s*', line)
            if prefix_match:
                # Get the part after prefix
                remainder = line[prefix_match.end():].rstrip('\n')
                # The original line stripped of leading whitespace
                original_code = original.lstrip()
                if original_code and original_code in remainder:
                    preserved_count += 1
                elif original.strip() in line:
                    preserved_count += 1

        if preserved_count == 20:
            print(f"PASS: Component 3 — Original code preserved on all 20 lines (0.3 pts)")
            total_score += 0.3
        elif preserved_count > 0:
            partial = round(0.3 * (preserved_count / 20), 2)
            print(f"PARTIAL: Component 3 — {preserved_count}/20 lines preserved ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Original code not preserved")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
