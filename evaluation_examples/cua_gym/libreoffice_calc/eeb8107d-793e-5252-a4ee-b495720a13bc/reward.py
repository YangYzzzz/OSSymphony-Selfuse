"""
Reward Script: Network Traffic Analyzer Script Verification
Task ID: os_gf5_027
Domain: os (Python scripting)
Scoring:
  - Component 1 (0.15): Script exists with Scapy import
  - Component 2 (0.20): Uses sniff(count=30)
  - Component 3 (0.20): Protocol counting (TCP, UDP, ICMP, Other)
  - Component 4 (0.20): Top 3 source IPs identification
  - Component 5 (0.15): Formatted summary output strings
  - Component 6 (0.10): Permission error handling
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'os_gf5_027'


def verify_task(file_path):
    """
    Verify that traffic_analyzer.py meets all task requirements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) < 50:
        print(f"CRITICAL: File is too short ({len(content)} chars), likely empty/stub")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Script imports Scapy and has shebang or is a proper Python script (0.15 points)
    try:
        has_scapy_import = bool(re.search(r'from\s+scapy', content) or re.search(r'import\s+scapy', content))
        if has_scapy_import:
            print(f"PASS: Component 1 — Scapy import found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — No Scapy import found in script")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Uses sniff() with count=30 (0.20 points)
    try:
        # Match sniff(...count=30...) in various forms
        has_sniff_30 = bool(re.search(r'sniff\s*\(.*count\s*=\s*30', content, re.DOTALL))
        if has_sniff_30:
            print(f"PASS: Component 2 — sniff(count=30) found (0.20 pts)")
            total_score += 0.20
        else:
            # Check for sniff with any count
            has_sniff = bool(re.search(r'sniff\s*\(', content))
            if has_sniff:
                print(f"FAIL: Component 2 — sniff() found but count=30 not specified")
            else:
                print(f"FAIL: Component 2 — No sniff() call found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Protocol counting for TCP, UDP, ICMP, Other (0.20 points)
    try:
        protocols_found = 0
        for proto in ['TCP', 'UDP', 'ICMP', 'Other']:
            # Check for protocol string references in counting logic
            if re.search(rf'["\']({proto})["\']', content):
                protocols_found += 1

        # Also check for protocol classification logic (haslayer or similar)
        has_classification = bool(
            re.search(r'haslayer\s*\(\s*TCP\s*\)', content) or
            re.search(r'haslayer\s*\(\s*UDP\s*\)', content) or
            re.search(r'haslayer\s*\(\s*ICMP\s*\)', content)
        )

        if protocols_found >= 4 and has_classification:
            print(f"PASS: Component 3 — All 4 protocol categories found with classification logic (0.20 pts)")
            total_score += 0.20
        elif protocols_found >= 4:
            print(f"PARTIAL: Component 3 — Protocol strings found but no haslayer classification (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Only {protocols_found}/4 protocol categories found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Top 3 source IPs identification (0.20 points)
    try:
        # Check for Counter or sorting logic with most_common or sorted
        has_ip_extraction = bool(re.search(r'\.src', content) or re.search(r'\[IP\]', content))
        has_top_3 = bool(
            re.search(r'most_common\s*\(\s*3\s*\)', content) or
            re.search(r'top.*3', content, re.IGNORECASE) or
            re.search(r'\[:3\]', content)
        )

        if has_ip_extraction and has_top_3:
            print(f"PASS: Component 4 — Source IP extraction and top 3 logic found (0.20 pts)")
            total_score += 0.20
        elif has_ip_extraction:
            print(f"PARTIAL: Component 4 — IP extraction found but no top-3 selection (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No source IP extraction logic found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Formatted summary output with expected format (0.15 points)
    try:
        has_protocol_breakdown = bool(re.search(r'Protocol\s+Breakdown', content))
        has_top_source_ips = bool(re.search(r'Top\s+Source\s+IP', content, re.IGNORECASE))
        has_packet_format = bool(re.search(r'packet', content, re.IGNORECASE))

        if has_protocol_breakdown and has_top_source_ips:
            print(f"PASS: Component 5 — Formatted summary with Protocol Breakdown and Top Source IPs (0.15 pts)")
            total_score += 0.15
        elif has_protocol_breakdown or has_top_source_ips:
            print(f"PARTIAL: Component 5 — Partial summary format (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 — No formatted summary output found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Permission error handling (0.10 points)
    try:
        has_permission_handling = bool(
            re.search(r'PermissionError', content) or
            re.search(r'permission', content, re.IGNORECASE) or
            re.search(r'root\s+privilege', content, re.IGNORECASE) or
            re.search(r'sudo', content, re.IGNORECASE)
        )

        if has_permission_handling:
            print(f"PASS: Component 6 — Permission error handling found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — No permission error handling found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/traffic_analyzer.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
