"""
Reward Script: Add figure captions and Table of Figures to Lab_Report.docx
Task ID: writer_pd_007
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): Caption text for Figure 1 present
  Component 2 (0.15): Caption text for Figure 2 present
  Component 3 (0.15): Caption text for Figure 3 present
  Component 4 (0.15): Caption text for Figure 4 present
  Component 5 (0.20): SEQ Figure field codes present (automatic caption numbering)
  Component 6 (0.20): Table of Figures (TOC field with type "Figure") on last page
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_007'

# Expected caption texts (after automatic caption insertion)
EXPECTED_CAPTIONS = [
    "Figure 1: Experimental Setup",
    "Figure 2: Raw Data Distribution",
    "Figure 3: Analysis Results",
    "Figure 4: Comparison Chart",
]


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts for caption searching
    all_para_texts = [p.text.strip() for p in doc.paragraphs]

    # =========================================================================
    # Components 1-4: Each caption text is present as a paragraph (0.15 each)
    # These captions do NOT exist in the initial file, only in the golden file.
    # =========================================================================
    for idx, expected_caption in enumerate(EXPECTED_CAPTIONS):
        comp_num = idx + 1
        weight = 0.15
        try:
            # Check if any paragraph contains this caption text
            # Use flexible matching: the paragraph text should contain the expected caption
            found = False
            for pt in all_para_texts:
                if expected_caption in pt:
                    found = True
                    break
            if found:
                print(f"PASS: Component {comp_num} -- Caption '{expected_caption}' found ({weight} pts)")
                total_score += weight
            else:
                print(f"FAIL: Component {comp_num} -- Caption '{expected_caption}' not found in any paragraph")
        except Exception as e:
            print(f"ERROR: Component {comp_num} -- {e}")

    # =========================================================================
    # Component 5: SEQ Figure field codes (automatic caption numbering) (0.20)
    # In the initial file there are 0 instrText elements.
    # In the golden file there should be 4 SEQ Figure field codes.
    # =========================================================================
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        body = doc.element.body
        instr_texts = body.findall('.//w:instrText', ns)
        seq_figure_count = 0
        for it in instr_texts:
            if it.text and 'SEQ' in it.text and 'Figure' in it.text:
                seq_figure_count += 1

        if seq_figure_count >= 4:
            print(f"PASS: Component 5 -- Found {seq_figure_count} SEQ Figure field codes (0.20 pts)")
            total_score += 0.20
        elif seq_figure_count > 0:
            # Partial credit: proportional to how many were found
            partial = 0.20 * (seq_figure_count / 4.0)
            print(f"PARTIAL: Component 5 -- Found {seq_figure_count}/4 SEQ Figure fields ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- No SEQ Figure field codes found (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # =========================================================================
    # Component 6: Table of Figures TOC field (0.20)
    # Initial file has no TOC instrText. Golden file has TOC \h \z \c "Figure".
    # =========================================================================
    try:
        tof_found = False
        for it in instr_texts:
            if it.text and 'TOC' in it.text and 'Figure' in it.text:
                tof_found = True
                break

        if not tof_found:
            # Also check for Table of Figures content in the last paragraphs
            # (the TOF might be rendered as plain text with figure entries)
            # Look for the "List of Figures" section with actual figure entries
            list_of_figures_idx = None
            for i, pt in enumerate(all_para_texts):
                if pt == 'List of Figures':
                    list_of_figures_idx = i
                    break

            if list_of_figures_idx is not None:
                # Check if there's content after "List of Figures" that lists figure entries
                remaining = all_para_texts[list_of_figures_idx + 1:]
                figure_entries = [t for t in remaining if t.startswith('Figure') and ':' in t]
                if len(figure_entries) >= 4:
                    tof_found = True

        if tof_found:
            print(f"PASS: Component 6 -- Table of Figures found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 6 -- No Table of Figures (TOC with Figure type) found")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
