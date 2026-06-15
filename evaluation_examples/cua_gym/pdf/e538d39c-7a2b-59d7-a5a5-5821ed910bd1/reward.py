"""
Reward Script: Extract abstract from PDF paper
Task ID: pdf_res_005
Domain: pdf
Scoring:
  - Component 1 (0.4): abstract.txt exists and starts with expected opening text
  - Component 2 (0.3): abstract.txt contains key phrases from the abstract body
  - Component 3 (0.3): abstract.txt contains ONLY the abstract (no headings, no intro text)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_005'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    file_path = os.path.join(WORKDIR, 'papers', 'abstract.txt')

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: abstract.txt not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Strip whitespace for checks
    content_stripped = content.strip()

    if len(content_stripped) == 0:
        print("CRITICAL: abstract.txt is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: abstract.txt contains the opening sentence of the abstract (0.4 points)
    # The abstract starts with "Reinforcement learning (RL) has emerged as a powerful paradigm"
    try:
        opening_phrase = "Reinforcement learning (RL) has emerged as a powerful paradigm"
        if opening_phrase in content_stripped:
            print(f"PASS: Component 1 — Opening sentence found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected opening '{opening_phrase[:50]}...', not found in content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: abstract.txt contains key phrases from the abstract body (0.3 points)
    # Check for multiple distinctive phrases that appear in the abstract
    try:
        key_phrases = [
            "Markov Decision Processes",
            "Proximal Policy Optimization",
            "sample efficiency and asymptotic reward",
        ]
        found_count = 0
        for phrase in key_phrases:
            if phrase in content_stripped:
                found_count += 1

        if found_count == len(key_phrases):
            print(f"PASS: Component 2 — All {len(key_phrases)} key phrases found (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            partial = round(0.3 * found_count / len(key_phrases), 2)
            print(f"PARTIAL: Component 2 — {found_count}/{len(key_phrases)} key phrases found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — None of the key phrases found in abstract.txt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: abstract.txt contains ONLY the abstract, no extra sections (0.3 points)
    # The abstract should NOT contain section headings or content from other parts of the paper
    try:
        forbidden_markers = [
            "1. Introduction",
            "Introduction\n",
            "Keywords:",
            "Keywords\n",
            "2. Background",
            "References",
        ]
        found_markers = [m.strip() for m in forbidden_markers if m in content_stripped]

        if len(found_markers) > 0:
            print(f"FAIL: Component 3 — Found forbidden marker '{found_markers[0]}' in abstract.txt")
        else:
            # Also check that content is reasonable length (not the entire paper)
            # The abstract should be roughly 100-2000 characters
            if 50 < len(content_stripped) < 3000:
                print(f"PASS: Component 3 — Content is clean abstract only, {len(content_stripped)} chars (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Content length {len(content_stripped)} chars is outside expected range (50-3000)")
        # (no else needed — failure already printed above)
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
