"""
Reward Script: Change file encoding to UTF-8
Task ID: vscode_stu_044
Domain: vscode
Scoring:
  Component 1 (0.5): File bytes are valid UTF-8 (not latin-1 single-byte)
  Component 2 (0.3): Non-ASCII chars use multi-byte UTF-8 sequences
  Component 3 (0.2): File content integrity - French text preserved correctly
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_044'


def verify_task(file_path):
    """
    Verify that file encoding has been changed to UTF-8.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load raw bytes
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File bytes decode as valid UTF-8 (0.5 points)
    # In the initial state, the file is latin-1 encoded and contains bytes
    # like 0xe9 that are NOT valid UTF-8 on their own. After conversion to
    # UTF-8, all bytes must form valid UTF-8 sequences.
    try:
        decoded_text = raw.decode('utf-8')
        print(f"PASS: Component 1 — File decodes as valid UTF-8 (0.5 pts)")
        total_score += 0.5
    except UnicodeDecodeError as e:
        print(f"FAIL: Component 1 — File does NOT decode as valid UTF-8: {e}")
        # If not valid UTF-8, we cannot proceed with content checks reliably
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Non-ASCII characters are multi-byte UTF-8 sequences (0.3 points)
    # In latin-1, accented chars like e (U+00E9) are single byte 0xe9.
    # In UTF-8, the same char is two bytes: 0xc3 0xa9.
    # We verify that known French accented characters from the file are
    # encoded as multi-byte UTF-8, not single-byte latin-1.
    try:
        # Count non-ASCII bytes in the raw data
        non_ascii_bytes = [b for b in raw if b > 127]

        # In UTF-8, bytes 0xc0-0xdf are lead bytes of 2-byte sequences
        # and 0x80-0xbf are continuation bytes.
        # In latin-1, accented chars like e9, e8, f4, c9 appear as
        # standalone bytes > 127 that are NOT followed by continuation bytes.

        # Check for the presence of UTF-8 multi-byte sequences
        # Specifically, look for 0xc3 (lead byte for U+00C0-U+00FF range in UTF-8)
        # which is the lead byte for common French accented characters
        has_utf8_multibyte = b'\xc3' in raw

        # Also verify no isolated latin-1 high bytes exist
        # In latin-1, bytes like 0xe9 appear alone (not as part of a multi-byte sequence)
        # Check that all bytes > 127 are part of valid UTF-8 multi-byte sequences
        # by looking for specific latin-1 patterns that would be invalid in UTF-8
        has_isolated_latin1 = False
        i = 0
        while i < len(raw):
            b = raw[i]
            if 0x80 <= b <= 0xbf:
                # Continuation byte without a lead byte - this shouldn't happen in valid UTF-8
                # but we already verified UTF-8 validity in Component 1
                pass
            elif 0xc0 <= b <= 0xdf:
                # 2-byte UTF-8 sequence - skip next byte
                i += 2
                continue
            elif 0xe0 <= b <= 0xef:
                # 3-byte UTF-8 sequence - skip next 2 bytes
                i += 3
                continue
            elif 0xf0 <= b <= 0xf7:
                # 4-byte UTF-8 sequence - skip next 3 bytes
                i += 4
                continue
            i += 1

        if has_utf8_multibyte and len(non_ascii_bytes) > 0:
            print(f"PASS: Component 2 — Found UTF-8 multi-byte sequences "
                  f"({len(non_ascii_bytes)} non-ASCII bytes with 0xc3 lead bytes) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No UTF-8 multi-byte sequences found "
                  f"(non-ASCII bytes: {len(non_ascii_bytes)}, has 0xc3: {has_utf8_multibyte})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content integrity - French text preserved correctly (0.2 points)
    # Verify that key French strings from the file are present and correct
    # after the encoding change. These strings contain accented characters
    # that must survive the latin-1 -> UTF-8 conversion.
    try:
        expected_strings = [
            "Universit\u00e9 de Montr\u00e9al",        # Universite de Montreal
            "\u00c9milie Th\u00e9r\u00e8se Dub\u00e9",  # Emilie Therese Dube
            "Fr\u00e9d\u00e9ric Gagn\u00e9",            # Frederic Gagne
            "Am\u00e9lie Lafreni\u00e8re",               # Amelie Lafreniere
            "S\u00e9bastien Pr\u00e9vost",               # Sebastien Prevost
            "Val\u00e9rie C\u00f4t\u00e9",               # Valerie Cote
            "Ren\u00e9 Beaupr\u00e9",                    # Rene Beaupre
            "\u00c9chec",                                 # Echec (Fail)
        ]

        found_count = 0
        for expected in expected_strings:
            if expected in decoded_text:
                found_count += 1
            else:
                print(f"  WARN: Expected string not found: {expected!r}")

        if found_count == len(expected_strings):
            print(f"PASS: Component 3 — All {len(expected_strings)} French text "
                  f"strings preserved correctly after encoding change (0.2 pts)")
            total_score += 0.2
        elif found_count > 0:
            partial = round(0.2 * (found_count / len(expected_strings)), 2)
            print(f"PARTIAL: Component 3 — {found_count}/{len(expected_strings)} "
                  f"French strings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No expected French text strings found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
