"""
Reward Script: Determine PDF encryption status and write result to file
Task ID: pdf_mbc_018
Domain: pdf
Scoring:
  Component 1 (0.35) - encryption_status.txt exists and contains 'ENCRYPTED'
  Component 2 (0.35) - encryption_status.txt mentions AES-256 or the encryption algorithm
  Component 3 (0.30) - Content format matches expected structure (two-line format with method)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_018'

STATUS_FILE = os.path.join(WORKDIR, 'Documents', 'encryption_status.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: encryption_status.txt must exist (gate, not scored)
    if not os.path.exists(STATUS_FILE):
        print(f"CRITICAL: File not found: {STATUS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(STATUS_FILE, 'r').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {STATUS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    content_stripped = content.strip()
    content_upper = content_stripped.upper()

    # Component 1: File contains 'ENCRYPTED' (0.35 points)
    # This checks that the script correctly identified the PDF as encrypted.
    # Initial env has no encryption_status.txt, so this fails there.
    try:
        if 'ENCRYPTED' in content_upper and 'NOT ENCRYPTED' not in content_upper:
            print(f"PASS: Component 1 -- File contains 'ENCRYPTED' (0.35 pts)")
            total_score += 0.35
        elif 'NOT ENCRYPTED' in content_upper:
            print(f"FAIL: Component 1 -- File says 'NOT ENCRYPTED', but PDF is encrypted")
        else:
            print(f"FAIL: Component 1 -- 'ENCRYPTED' not found in content: {content_stripped!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: File mentions the encryption algorithm (AES-256) (0.35 points)
    # The task context specifies AES-256 encryption. The output should mention
    # the algorithm. Accept variations like 'AES-256', 'AES256', 'AES 256'.
    try:
        aes_found = False
        # Check for AES-256 in various formats
        aes_patterns = ['AES-256', 'AES256', 'AES 256', 'AES_256']
        for pattern in aes_patterns:
            if pattern in content_upper.replace('-', '').replace(' ', '').replace('_', ''):
                aes_found = True
                break
        # Also check raw content for the patterns with original casing
        if not aes_found:
            for pattern in aes_patterns:
                if pattern.lower() in content_stripped.lower():
                    aes_found = True
                    break

        if aes_found:
            print(f"PASS: Component 2 -- File mentions AES-256 encryption (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- AES-256 not found in content: {content_stripped!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Content structure - has multiple lines or structured output (0.30 points)
    # The golden file has 'ENCRYPTED' on first line and encryption method on second line.
    # Accept any structured format that has both the status and the method.
    try:
        lines = [l.strip() for l in content_stripped.splitlines() if l.strip()]
        # Need at least some structured content (not just a single word)
        # Must have the encryption status AND encryption method info
        has_encrypted_status = any('ENCRYPTED' in line.upper() and 'NOT' not in line.upper() for line in lines)
        has_method_info = any(
            'AES' in line.upper() or 'ENCRYPT' in line.upper().replace('ENCRYPTED', '')
            for line in lines
        )
        # Check that both pieces of info are present in a meaningful way
        if has_encrypted_status and has_method_info and len(content_stripped) > 10:
            print(f"PASS: Component 3 -- Structured output with status and method info (0.30 pts)")
            total_score += 0.30
        elif has_encrypted_status and len(lines) >= 2:
            # Partial: has structure but method info unclear
            print(f"PARTIAL: Component 3 -- Has structure but method info unclear (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Content lacks structured format: {content_stripped!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
