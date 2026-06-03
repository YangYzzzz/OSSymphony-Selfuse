"""
Reward Script: Git bisect to find bad commit and create bug_report.txt
Task ID: vscode_gf6_016
Domain: vscode
Scoring:
  Component 1: bug_report.txt exists and is non-empty (0.15 pts)
  Component 2: Contains a valid git SHA matching a real commit (0.30 pts)
  Component 3: Contains the commit message of the identified commit (0.30 pts)
  Component 4: Contains a meaningful description of the bug (0.25 pts) — LLM judge
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_016'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'git-bisect-debug')
BUG_REPORT_PATH = os.path.join(PROJECT_DIR, 'bug_report.txt')


def get_commit_map():
    """Build a map of abbreviated SHA -> (full_sha, commit_message) from the git log."""
    commit_map = {}
    try:
        log_path = '/tmp/_reward_git_log.txt'
        os.system(f'cd {PROJECT_DIR} && git log --format="%H %s" > {log_path} 2>/dev/null')
        with open(log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    full_sha, msg = parts
                    commit_map[full_sha] = msg
    except Exception as e:
        print(f"ERROR: Could not read git log: {e}")
    return commit_map


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: bug_report.txt exists and is non-empty (0.15 points)
    try:
        if os.path.isfile(BUG_REPORT_PATH):
            with open(BUG_REPORT_PATH, 'r') as f:
                content = f.read().strip()
            if len(content) > 10:
                print(f"PASS: Component 1 — bug_report.txt exists with {len(content)} chars (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — bug_report.txt exists but too short ({len(content)} chars)")
        else:
            print(f"FAIL: Component 1 — bug_report.txt not found at {BUG_REPORT_PATH}")
            # Early exit - no point checking other components
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read bug report content for remaining checks
    with open(BUG_REPORT_PATH, 'r') as f:
        report_content = f.read()

    # Build commit map from git log
    commit_map = get_commit_map()
    if not commit_map:
        print("ERROR: Could not build commit map from git log")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Contains a valid git SHA matching a real commit (0.30 points)
    # Find all hex strings >= 7 chars (abbreviated or full SHA)
    matched_sha = None
    matched_message = None
    try:
        hex_patterns = re.findall(r'\b([0-9a-f]{7,40})\b', report_content.lower())
        for hex_str in hex_patterns:
            for full_sha, msg in commit_map.items():
                if full_sha.startswith(hex_str) or hex_str == full_sha:
                    matched_sha = full_sha
                    matched_message = msg
                    break
            if matched_sha:
                break

        if matched_sha:
            print(f"PASS: Component 2 — Found valid commit SHA {matched_sha[:12]}... (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — No valid git SHA found in bug_report.txt. "
                  f"Found hex strings: {hex_patterns[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains the commit message of the identified commit (0.30 points)
    try:
        if matched_sha and matched_message:
            # Check if the commit message (or significant keywords from it) appears in the report
            msg_lower = matched_message.lower().strip()
            report_lower = report_content.lower()

            # Strategy: check if the full commit message is in the report, or if major keywords match
            if msg_lower in report_lower:
                print(f"PASS: Component 3 — Full commit message found: '{matched_message}' (0.30 pts)")
                total_score += 0.30
            else:
                # Check keyword overlap: split message into words, check if most are present
                msg_words = [w for w in re.findall(r'[a-z]+', msg_lower) if len(w) > 2]
                if msg_words:
                    matches = sum(1 for w in msg_words if w in report_lower)
                    ratio = matches / len(msg_words)
                    if ratio >= 0.7:
                        print(f"PASS: Component 3 — Commit message keywords match "
                              f"({matches}/{len(msg_words)} words, {ratio:.0%}) (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 3 — Commit message keyword match too low "
                              f"({matches}/{len(msg_words)} words, {ratio:.0%}). "
                              f"Expected: '{matched_message}'")
                else:
                    print(f"FAIL: Component 3 — Could not parse commit message words")
        else:
            print(f"FAIL: Component 3 — No matched commit to check message against")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Contains a description of the bug/change (0.25 points)
    # JUSTIFICATION: The task asks for a "one-line description of the change that introduced the bug".
    # This is open-ended/subjective — the agent may describe it in many valid ways.
    # We use LLM judge for this semantic check.
    try:
        import sys
        sys.path.insert(0, '/tmp')
        from reward_judge import call_llm_judge

        llm_score = call_llm_judge(
            task_instruction="Create bug_report.txt containing the SHA of the bad commit, the commit message, and a one-line description of the change that introduced the bug.",
            success_criteria=(
                "The bug report contains a meaningful description of what changed to introduce the bug. "
                "The bug involves calculate_tax() returning incorrect results for amounts over 10000, "
                "specifically a change in the tax bracket multiplier. The description should convey "
                "the nature of the code change (e.g., multiplier changed, bracket logic modified). "
                "Score 1.0 if description is clear and accurate, 0.5 if vague but present, 0.0 if missing."
            ),
            state_excerpt=report_content,
        )
        if llm_score > 0.0:
            awarded = 0.25 * llm_score
            print(f"PASS: Component 4 — LLM judge scored description {llm_score:.2f} ({awarded:.3f} pts)")
            total_score += awarded
        else:
            print(f"FAIL: Component 4 — LLM judge scored description 0.0")
    except Exception as e:
        print(f"WARN: Component 4 (LLM judge unavailable) — {e}")
        # Fallback: programmatic keyword check for description-like content
        # The description should mention the nature of the tax calculation bug
        desc_keywords = ['tax', 'bracket', 'multiplier', 'rate', 'amount', 'calculation', 'change', 'incorrect', 'bug']
        found_kw = [kw for kw in desc_keywords if kw in report_content.lower()]
        if len(found_kw) >= 3:
            print(f"  FALLBACK PASS: Found description keywords {found_kw} (0.25 pts)")
            total_score += 0.25
        elif len(found_kw) >= 2:
            print(f"  FALLBACK PARTIAL: Found some keywords {found_kw} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"  FALLBACK FAIL: Insufficient description keywords found: {found_kw}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
