"""
Reward Script: Container security scanning pipeline script verification
Task ID: os_gff_075
Domain: os (shell scripting)
Scoring:
  Component 1: Script exists and is executable (0.15)
  Component 2: Script has valid bash shebang and structure (0.10)
  Component 3: Script reads images from /opt/security/images.txt (0.15)
  Component 4: Script invokes trivy with correct flags (0.20)
  Component 5: Script generates per-image JSON output references (0.10)
  Component 6: Script produces an aggregated summary (0.15)
  Component 7: Script exits 1 on CRITICAL vulnerabilities (0.15)
"""

import os
import stat
import re

SCRIPT_PATH = '/opt/security/scan_images.sh'


def verify_task():
    """
    Verify that /opt/security/scan_images.sh is a correct container security
    scanning pipeline script. Returns float 0.0-1.0.
    """
    total_score = 0.0

    # ---- Precondition: script file must exist ----
    if not os.path.isfile(SCRIPT_PATH):
        print(f"CRITICAL: Script not found at {SCRIPT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read script content once
    try:
        with open(SCRIPT_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read script: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) < 20:
        print("CRITICAL: Script is too short / empty")
        print("REWARD: 0.0")
        return 0.0

    # ---- Component 1: Script is executable (0.15 points) ----
    try:
        mode = stat.S_IMODE(os.stat(SCRIPT_PATH).st_mode)
        # Check that at least owner-execute bit is set
        if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            print(f"PASS: Component 1 — Script is executable (mode={oct(mode)}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Script is not executable (mode={oct(mode)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Valid bash shebang and basic structure (0.10 points) ----
    try:
        has_shebang = content.strip().startswith('#!/bin/bash') or content.strip().startswith('#!/usr/bin/env bash')
        # Check for balanced control structures (basic validation)
        has_while_or_for = bool(re.search(r'\b(while|for)\b', content))
        has_done = bool(re.search(r'\bdone\b', content))
        has_if = bool(re.search(r'\bif\b', content))
        has_fi = bool(re.search(r'\bfi\b', content))

        structure_ok = has_shebang and has_while_or_for and has_done
        if_ok = (not has_if) or (has_if and has_fi)  # if present, must have matching fi

        if structure_ok and if_ok:
            print(f"PASS: Component 2 — Valid bash shebang and balanced control structures (0.10 pts)")
            total_score += 0.10
        elif has_shebang:
            print(f"PARTIAL: Component 2 — Has shebang but structure issues (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 2 — Missing shebang or broken structure")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: Reads from /opt/security/images.txt (0.15 points) ----
    try:
        images_ref = '/opt/security/images.txt'
        if images_ref in content or 'images.txt' in content:
            # Verify it reads line-by-line (while/read or for loop with cat)
            reads_lines = bool(
                re.search(r'while\s.*read\b', content) or
                re.search(r'for\s+\w+\s+in\s+.*\$\(cat', content) or
                re.search(r'readarray', content) or
                re.search(r'mapfile', content) or
                re.search(r'<\s*"\$', content) or
                re.search(r'<\s*/opt/security/images\.txt', content)
            )
            if reads_lines:
                print(f"PASS: Component 3 — Script reads images from {images_ref} line by line (0.15 pts)")
                total_score += 0.15
            elif images_ref in content:
                print(f"PARTIAL: Component 3 — References {images_ref} but line-by-line read not detected (0.07 pts)")
                total_score += 0.07
        else:
            print(f"FAIL: Component 3 — No reference to {images_ref} in script")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: Invokes trivy with correct flags (0.20 points) ----
    try:
        has_trivy = bool(re.search(r'\btrivy\b', content))
        has_format_json = bool(re.search(r'--format\s+json', content))
        has_severity = bool(re.search(r'--severity\s+\S*HIGH\S*CRITICAL|--severity\s+\S*CRITICAL\S*HIGH', content))
        has_output_flag = bool(re.search(r'--output', content))

        checks_passed = sum([has_trivy, has_format_json, has_severity, has_output_flag])
        if checks_passed == 4:
            print(f"PASS: Component 4 — trivy with --format json, --severity HIGH,CRITICAL, --output (0.20 pts)")
            total_score += 0.20
        elif checks_passed >= 2:
            partial = round(0.20 * checks_passed / 4, 2)
            print(f"PARTIAL: Component 4 — {checks_passed}/4 trivy flags present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — trivy invocation missing or lacks key flags")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Generates per-image JSON reports (0.10 points) ----
    try:
        # Script should produce per-image JSON files with dynamic names
        has_per_image_json = bool(
            re.search(r'scan_.*\.json', content) or
            re.search(r'\$.*\.json', content)
        )
        has_dynamic_output = bool(
            re.search(r'--output\s+["\$]', content) or
            re.search(r'--output\s+\S*\$', content)
        )
        if has_per_image_json and has_dynamic_output:
            print(f"PASS: Component 5 — Per-image JSON report generation detected (0.10 pts)")
            total_score += 0.10
        elif has_per_image_json or has_dynamic_output:
            print(f"PARTIAL: Component 5 — JSON report pattern partially detected (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — No per-image JSON report generation detected")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ---- Component 6: Aggregates results into a summary (0.15 points) ----
    try:
        has_summary_file = bool(re.search(r'summary', content, re.IGNORECASE))
        has_total_count = bool(
            re.search(r'TOTAL|total.*image|Total', content) and
            (re.search(r'HIGH', content) or re.search(r'CRITICAL', content))
        )
        has_printf_or_echo = bool(
            re.search(r'(printf|echo).*HIGH', content) or
            re.search(r'(printf|echo).*CRITICAL', content)
        )
        agg_checks = sum([has_summary_file, has_total_count, has_printf_or_echo])
        if agg_checks >= 2:
            print(f"PASS: Component 6 — Summary aggregation found (0.15 pts)")
            total_score += 0.15
        elif agg_checks == 1:
            print(f"PARTIAL: Component 6 — Partial summary aggregation (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 6 — No summary aggregation detected")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ---- Component 7: Exits with code 1 on CRITICAL vulnerabilities (0.15 points) ----
    try:
        has_exit_1 = bool(re.search(r'exit\s+1', content))
        has_critical_check = bool(
            re.search(r'CRITICAL', content) and
            (re.search(r'CRITICAL_FOUND|critical_found', content, re.IGNORECASE) or
             re.search(r'if\s.*CRITICAL', content) or
             re.search(r'critical.*-gt\s*0', content, re.IGNORECASE))
        )
        if has_exit_1 and has_critical_check:
            print(f"PASS: Component 7 — Script exits 1 when CRITICAL vulnerabilities found (0.15 pts)")
            total_score += 0.15
        elif has_exit_1:
            print(f"PARTIAL: Component 7 — exit 1 found but CRITICAL-conditional logic unclear (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 7 — No conditional exit 1 on CRITICAL detected")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
