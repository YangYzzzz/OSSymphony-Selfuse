"""
Reward Script: Accept tracked changes in Section 1, reject in Section 2
Task ID: writer_rm_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Section 1 changes accepted (inserted text is normal, no revisions remain)
  Component 2 (0.40): Section 2 changes rejected (original text restored, no revisions remain)
  Component 3 (0.30): Section 3 tracked changes still present (2 insertions remain)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_034'


def get_section_paragraphs(doc):
    """Split document paragraphs into sections based on Section headings."""
    sections = {}
    current_section = 'preamble'
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith('Section 1'):
            current_section = 'Section 1'
            continue
        elif text.startswith('Section 2'):
            current_section = 'Section 2'
            continue
        elif text.startswith('Section 3'):
            current_section = 'Section 3'
            continue
        if current_section not in sections:
            sections[current_section] = []
        sections[current_section].append(para)
    return sections


def count_revisions_in_section(doc, section_name):
    """Count tracked insertions and deletions in paragraphs belonging to a section."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    current_section = 'preamble'
    total_ins = 0
    total_del = 0

    for para_elem in body.findall('.//w:p', ns):
        # Determine which section this paragraph belongs to
        all_texts = []
        for t in para_elem.findall('.//w:t', ns):
            all_texts.append(t.text or '')
        for t in para_elem.findall('.//w:delText', ns):
            all_texts.append(t.text or '')
        full_text = ''.join(all_texts)

        if 'Section 1' in full_text and full_text.strip().startswith('Section 1'):
            current_section = 'Section 1'
            continue
        elif 'Section 2' in full_text and full_text.strip().startswith('Section 2'):
            current_section = 'Section 2'
            continue
        elif 'Section 3' in full_text and full_text.strip().startswith('Section 3'):
            current_section = 'Section 3'
            continue

        if current_section == section_name:
            total_ins += len(para_elem.findall('.//w:ins', ns))
            total_del += len(para_elem.findall('.//w:del', ns))

    return total_ins, total_del


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sections = get_section_paragraphs(doc)

    # Component 1: Section 1 changes accepted (0.30 points)
    # After accepting, the inserted text should be normal text and no tracked changes remain.
    # Expected: "Comprehensive Strategic" in title, "March 1, 2026" date, executive summary sentence present
    try:
        s1_ins, s1_del = count_revisions_in_section(doc, 'Section 1')
        s1_paras = sections.get('Section 1', [])
        s1_text = ' '.join(p.text for p in s1_paras)

        sub_score = 0.0

        # No tracked changes should remain in Section 1
        if s1_ins == 0 and s1_del == 0:
            sub_score += 0.10
            print(f"PASS: Section 1 has no remaining tracked changes")
        else:
            print(f"FAIL: Section 1 still has tracked changes (ins={s1_ins}, del={s1_del})")

        # Accepted insertion 1: "Comprehensive Strategic" in title paragraph
        if 'Comprehensive Strategic' in s1_text:
            sub_score += 0.07
            print(f"PASS: Section 1 contains 'Comprehensive Strategic' (accepted)")
        else:
            print(f"FAIL: Section 1 missing 'Comprehensive Strategic'")

        # Accepted insertion 2: "March 1, 2026" date
        if 'March 1, 2026' in s1_text:
            sub_score += 0.07
            print(f"PASS: Section 1 contains 'March 1, 2026' (accepted)")
        else:
            print(f"FAIL: Section 1 missing 'March 1, 2026'")

        # Accepted insertion 3: Executive summary sentence
        if 'executive summary' in s1_text.lower():
            sub_score += 0.06
            print(f"PASS: Section 1 contains executive summary sentence (accepted)")
        else:
            print(f"FAIL: Section 1 missing executive summary sentence")

        total_score += sub_score
        print(f"  Component 1 subtotal: {sub_score:.2f}/0.30")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section 2 changes rejected (0.40 points)
    # After rejecting, the original (deleted) text should be restored, inserted text removed.
    # Expected: "$245,000", "$128,500", "critical for successful adoption", "written approval from the CFO", "30 days"
    try:
        s2_ins, s2_del = count_revisions_in_section(doc, 'Section 2')
        s2_paras = sections.get('Section 2', [])
        s2_text = ' '.join(p.text for p in s2_paras)

        sub_score = 0.0

        # No tracked changes should remain in Section 2
        if s2_ins == 0 and s2_del == 0:
            sub_score += 0.08
            print(f"PASS: Section 2 has no remaining tracked changes")
        else:
            print(f"FAIL: Section 2 still has tracked changes (ins={s2_ins}, del={s2_del})")

        # Rejected change 1: Original "$245,000" restored, not "$198,000"
        if '$245,000' in s2_text and '$198,000' not in s2_text:
            sub_score += 0.08
            print(f"PASS: Section 2 has original '$245,000' (rejected change)")
        else:
            print(f"FAIL: Section 2 budget not correctly rejected (text: ...{[t for t in ['$245,000','$198,000'] if t in s2_text]})")

        # Rejected change 2: Original "$128,500" restored, not "$95,000"
        if '$128,500' in s2_text and '$95,000' not in s2_text:
            sub_score += 0.08
            print(f"PASS: Section 2 has original '$128,500' (rejected change)")
        else:
            print(f"FAIL: Section 2 infrastructure not correctly rejected")

        # Rejected change 3: Original "critical for successful adoption" restored
        if 'critical for successful adoption' in s2_text and 'deferred to the next fiscal year' not in s2_text:
            sub_score += 0.08
            print(f"PASS: Section 2 has original training text (rejected change)")
        else:
            print(f"FAIL: Section 2 training text not correctly rejected")

        # Rejected change 4: Original "written approval from the CFO" and "30 days" restored
        if 'written approval from the CFO' in s2_text and '30 days' in s2_text:
            sub_score += 0.08
            print(f"PASS: Section 2 has original approval requirements (rejected change)")
        else:
            print(f"FAIL: Section 2 approval requirements not correctly rejected")

        total_score += sub_score
        print(f"  Component 2 subtotal: {sub_score:.2f}/0.40")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Section 3 tracked changes still present AND sections 1/2 processed (0.30 points)
    # This is a compound check: Section 3 must still have tracked changes, but ONLY scores
    # when Section 1 or Section 2 have been processed (no tracked changes remain in them).
    # This ensures we're measuring selective action, not just the initial state.
    try:
        s3_ins, s3_del = count_revisions_in_section(doc, 'Section 3')

        sub_score = 0.0

        # Gate: at least one of Section 1 or Section 2 must have been processed
        # (no tracked changes remaining). If both still have tracked changes, this is
        # likely the initial state and we should not award points.
        s1_processed = (s1_ins == 0 and s1_del == 0)
        s2_processed = (s2_ins == 0 and s2_del == 0)

        if not (s1_processed or s2_processed):
            print(f"FAIL: Component 3 gate — neither Section 1 nor Section 2 has been processed")
            print(f"  Component 3 subtotal: 0.00/0.30")
        else:
            # Section 3 should still have tracked insertions
            if s3_ins >= 2:
                sub_score += 0.15
                print(f"PASS: Section 3 has {s3_ins} tracked insertions (expected >= 2)")
            elif s3_ins == 1:
                sub_score += 0.07
                print(f"PARTIAL: Section 3 has {s3_ins} tracked insertion (expected 2)")
            else:
                print(f"FAIL: Section 3 has {s3_ins} tracked insertions (expected 2)")

            # Verify the specific tracked insertion content is present
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            body = doc.element.body
            current_section = 'preamble'
            s3_insert_texts = []
            for para_elem in body.findall('.//w:p', ns):
                all_texts = []
                for t in para_elem.findall('.//w:t', ns):
                    all_texts.append(t.text or '')
                for t in para_elem.findall('.//w:delText', ns):
                    all_texts.append(t.text or '')
                full_text = ''.join(all_texts)
                if full_text.strip().startswith('Section 1'):
                    current_section = 'Section 1'
                    continue
                elif full_text.strip().startswith('Section 2'):
                    current_section = 'Section 2'
                    continue
                elif full_text.strip().startswith('Section 3'):
                    current_section = 'Section 3'
                    continue

                if current_section == 'Section 3':
                    for ins in para_elem.findall('.//w:ins', ns):
                        for t in ins.findall('.//w:t', ns):
                            if t.text:
                                s3_insert_texts.append(t.text.strip())

            has_data_migration = any('data migration' in t for t in s3_insert_texts)
            has_risk_assessment = any('risk assessment' in t for t in s3_insert_texts)

            if has_data_migration and has_risk_assessment:
                sub_score += 0.15
                print(f"PASS: Section 3 tracked insertions contain expected content")
            elif has_data_migration or has_risk_assessment:
                sub_score += 0.07
                print(f"PARTIAL: Section 3 has one of two expected tracked insertions")
            else:
                print(f"FAIL: Section 3 tracked insertions missing expected content (found: {s3_insert_texts})")

            total_score += sub_score
            print(f"  Component 3 subtotal: {sub_score:.2f}/0.30")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice
def persist_app_state(domain):
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
