"""
Reward Script: Extract English text from mixed-content PDF
Task ID: pdf_res_056
Domain: pdf
Scoring:
  - Component 1 (0.15): english_text.txt exists at /home/user/papers/
  - Component 2 (0.15): File has substantial content (non-trivial size)
  - Component 3 (0.35): Contains key English phrases from the paper
  - Component 4 (0.15): Multiple paragraphs of readable text
  - Component 5 (0.20): Mathematical notation is filtered out
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_056'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'english_text.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: english_text.txt exists (0.15 points)
    # This is the primary task output — it does NOT exist in initial_env
    try:
        if os.path.exists(OUTPUT_FILE):
            print(f"PASS: Component 1 — {OUTPUT_FILE} exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — {OUTPUT_FILE} does not exist")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load file content (precondition for all remaining checks)
    try:
        content = open(OUTPUT_FILE, 'r', encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: File has substantial content (0.15 points)
    # Golden file is ~13727 bytes. We check for minimum reasonable size.
    try:
        char_count = len(content)
        line_count = len(content.splitlines())
        non_empty_lines = len([l for l in content.splitlines() if l.strip()])
        if char_count >= 2000 and non_empty_lines >= 30:
            print(f"PASS: Component 2 — File has {char_count} chars, {non_empty_lines} non-empty lines (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — File too small: {char_count} chars, {non_empty_lines} non-empty lines (need >=2000 chars, >=30 lines)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains key English phrases from the paper (0.35 points)
    # The paper is about convergence of stochastic gradient methods in deep learning.
    # These phrases MUST appear in the extracted English text.
    try:
        key_phrases = [
            'convergence',
            'stochastic gradient',
            'deep learning',
            'non-convex',
            'optimization',
            'neural network',
            'learning rate',
        ]
        content_lower = content.lower()
        found_count = 0
        for phrase in key_phrases:
            if phrase in content_lower:
                found_count += 1

        # Award proportional credit: need at least 5 of 7 for full marks
        if found_count >= 5:
            pts = 0.35
        elif found_count >= 3:
            pts = 0.20
        elif found_count >= 1:
            pts = 0.10
        else:
            pts = 0.0

        if pts > 0:
            print(f"PASS: Component 3 — Found {found_count}/{len(key_phrases)} key phrases ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 — Found {found_count}/{len(key_phrases)} key phrases (need at least 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Multiple paragraphs of readable text (0.15 points)
    # The golden file has ~10 paragraph blocks. Check for structure.
    try:
        # Split on double newlines to find paragraph blocks
        paragraphs = re.split(r'\n\s*\n', content.strip())
        para_count = len(paragraphs)

        # Also check that paragraphs have reasonable length (not just single words)
        substantial_paras = [p for p in paragraphs if len(p.strip()) > 100]

        if para_count >= 5 and len(substantial_paras) >= 3:
            print(f"PASS: Component 4 — {para_count} paragraphs, {len(substantial_paras)} substantial ones (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — {para_count} paragraphs, {len(substantial_paras)} substantial (need >=5 paras, >=3 substantial)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Mathematical notation is filtered out (0.20 points)
    # The task asks to save ONLY English sentences, filtering out formulas/math notation.
    # Check that common math patterns are absent or minimal.
    try:
        # Check for LaTeX-style commands (e.g., \frac, \sum, \int, \alpha)
        latex_commands = re.findall(r'\\[a-z]{3,}', content)

        # Check for standalone math expressions (e.g., "x_i", "theta_k", "f(x) = ...")
        # These are inline formula fragments that should be removed
        # We look for patterns like "= \sum", "x^2", "\in R^d" etc.
        heavy_math_lines = 0
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Count lines that are predominantly mathematical
            # A line is "math-heavy" if it has multiple math symbols and few English words
            math_symbols = len(re.findall(r'[=∑∫∏∂∇≤≥±×÷∈∉⊂⊃∀∃αβγδεζηθλμσωΣΠ]', stripped))
            if math_symbols >= 3:
                heavy_math_lines += 1

        # Also check for LaTeX-like delimiters
        latex_delimiters = len(re.findall(r'\$\$?|\\[\[\]\(\)]', content))

        total_math_indicators = len(latex_commands) + heavy_math_lines + latex_delimiters
        if total_math_indicators <= 5:
            print(f"PASS: Component 5 — Low math content: {len(latex_commands)} LaTeX commands, {heavy_math_lines} math-heavy lines, {latex_delimiters} delimiters (0.20 pts)")
            total_score += 0.20
        elif total_math_indicators <= 15:
            pts = 0.10
            print(f"PARTIAL: Component 5 — Some math remaining: {total_math_indicators} indicators ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 5 — Too much math: {total_math_indicators} indicators (LaTeX: {len(latex_commands)}, heavy lines: {heavy_math_lines}, delimiters: {latex_delimiters})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
