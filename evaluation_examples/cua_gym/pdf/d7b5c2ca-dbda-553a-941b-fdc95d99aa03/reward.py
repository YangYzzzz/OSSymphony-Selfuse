"""
Reward Script: Extract embedded font list from PDF and save report
Task ID: pdf_gf2_043
Domain: pdf
Scoring:
  Component 1 (0.15): font_report.txt exists and is non-empty
  Component 2 (0.25): Report lists all 13 unique fonts by name
  Component 3 (0.30): Correct embedded vs referenced status with WARNING flags
  Component 4 (0.15): Correct font type for each font
  Component 5 (0.15): Correct encoding for each font
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_043'

# Ground truth: the 13 unique fonts from the PDF, with their properties
# Derived from task description: extract fonts using doc.get_page_fonts()
EXPECTED_FONTS = {
    'Courier':                {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'DejaVu Sans Bold':       {'type': 'Type0', 'encoding': 'Identity-H',     'embedded': True},
    'DejaVu Sans Book':       {'type': 'Type0', 'encoding': 'Identity-H',     'embedded': True},
    'DejaVu Serif Book':      {'type': 'Type0', 'encoding': 'Identity-H',     'embedded': True},
    'Helvetica':              {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Helvetica-Bold':         {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Helvetica-BoldOblique':  {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Helvetica-Oblique':      {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Symbol':                 {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Times-Bold':             {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Times-Italic':           {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'Times-Roman':            {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
    'ZapfDingbats':           {'type': 'Type1', 'encoding': 'WinAnsiEncoding', 'embedded': False},
}

TOTAL_FONTS = len(EXPECTED_FONTS)  # 13


def verify_task(report_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: font_report.txt exists and is non-empty (0.15 points)
    try:
        if not os.path.exists(report_path):
            print(f"FAIL: Component 1 — font_report.txt does not exist at {report_path}")
            print("REWARD: 0.0")
            return 0.0

        with open(report_path, 'r') as f:
            content = f.read()

        if len(content.strip()) == 0:
            print(f"FAIL: Component 1 — font_report.txt is empty")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 — font_report.txt exists and is non-empty ({len(content)} chars) (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')
    content_lower = content.lower()

    # Component 2: Report lists all 13 unique font names (0.25 points)
    # Each font found earns proportional credit
    try:
        fonts_found = 0
        fonts_missing = []
        for font_name in EXPECTED_FONTS:
            if font_name in content:
                fonts_found += 1
            else:
                fonts_missing.append(font_name)

        if fonts_found == TOTAL_FONTS:
            print(f"PASS: Component 2 — All {TOTAL_FONTS} font names present (0.25 pts)")
            total_score += 0.25
        elif fonts_found > 0:
            partial = 0.25 * (fonts_found / TOTAL_FONTS)
            print(f"PARTIAL: Component 2 — {fonts_found}/{TOTAL_FONTS} fonts found ({partial:.3f} pts). Missing: {fonts_missing}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No expected font names found in report")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct embedded/referenced status with WARNING flags (0.30 points)
    # Non-embedded fonts must have 'WARNING: not embedded' or similar warning
    # Embedded fonts should indicate embedded status
    try:
        status_correct = 0
        status_total = TOTAL_FONTS
        for font_name, props in EXPECTED_FONTS.items():
            if font_name not in content:
                continue
            # Find the line containing this font name
            font_line = None
            for line in lines:
                if font_name in line:
                    # Make sure it's an exact match (not a substring of another font)
                    # e.g. 'Helvetica' should not match 'Helvetica-Bold' line
                    # Check that the font name is either at start or preceded by whitespace
                    idx = line.find(font_name)
                    if idx >= 0:
                        # Check no alphanumeric/hyphen immediately after
                        end_idx = idx + len(font_name)
                        if end_idx < len(line) and (line[end_idx].isalpha() or line[end_idx] == '-'):
                            continue
                        font_line = line
                        break

            if font_line is None:
                continue

            font_line_lower = font_line.lower()
            if props['embedded']:
                # Should indicate embedded, and should NOT have warning
                if 'embed' in font_line_lower and 'not embedded' not in font_line_lower and 'warning' not in font_line_lower:
                    status_correct += 1
                else:
                    print(f"  DETAIL: {font_name} — expected 'Embedded', line: {font_line.strip()}")
            else:
                # Should have WARNING about not embedded
                if 'warning' in font_line_lower and 'not embedded' in font_line_lower:
                    status_correct += 1
                else:
                    print(f"  DETAIL: {font_name} — expected WARNING not embedded, line: {font_line.strip()}")

        if status_correct == status_total:
            print(f"PASS: Component 3 — All {status_total} fonts have correct embedded/referenced status (0.30 pts)")
            total_score += 0.30
        elif status_correct > 0:
            partial = 0.30 * (status_correct / status_total)
            print(f"PARTIAL: Component 3 — {status_correct}/{status_total} fonts have correct status ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No fonts have correct embedded/referenced status")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct font type for each font (0.15 points)
    try:
        type_correct = 0
        type_total = TOTAL_FONTS
        for font_name, props in EXPECTED_FONTS.items():
            if font_name not in content:
                continue
            for line in lines:
                if font_name in line:
                    idx = line.find(font_name)
                    end_idx = idx + len(font_name)
                    if end_idx < len(line) and (line[end_idx].isalpha() or line[end_idx] == '-'):
                        continue
                    if props['type'] in line:
                        type_correct += 1
                    break

        if type_correct == type_total:
            print(f"PASS: Component 4 — All {type_total} fonts have correct type (0.15 pts)")
            total_score += 0.15
        elif type_correct > 0:
            partial = 0.15 * (type_correct / type_total)
            print(f"PARTIAL: Component 4 — {type_correct}/{type_total} fonts have correct type ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No fonts have correct type")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Correct encoding for each font (0.15 points)
    try:
        enc_correct = 0
        enc_total = TOTAL_FONTS
        for font_name, props in EXPECTED_FONTS.items():
            if font_name not in content:
                continue
            for line in lines:
                if font_name in line:
                    idx = line.find(font_name)
                    end_idx = idx + len(font_name)
                    if end_idx < len(line) and (line[end_idx].isalpha() or line[end_idx] == '-'):
                        continue
                    if props['encoding'] in line:
                        enc_correct += 1
                    break

        if enc_correct == enc_total:
            print(f"PASS: Component 5 — All {enc_total} fonts have correct encoding (0.15 pts)")
            total_score += 0.15
        elif enc_correct > 0:
            partial = 0.15 * (enc_correct / enc_total)
            print(f"PARTIAL: Component 5 — {enc_correct}/{enc_total} fonts have correct encoding ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No fonts have correct encoding")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
report_path = f'{WORKDIR}/Documents/font_report.txt'
if not os.path.exists(report_path):
    print(f"File not found: {report_path}")
    print("REWARD: 0.0")
else:
    verify_task(report_path)
