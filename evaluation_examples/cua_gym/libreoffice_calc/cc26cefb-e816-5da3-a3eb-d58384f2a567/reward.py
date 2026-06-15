"""
Reward Script: Fix references section in grant_proposal.docx to comply with Vancouver citation style
Task ID: osworld_multi_apps_misc_047
Domain: libreoffice_writer
Scoring:
  Component 1: Reference 1 uses abbreviated journal "N Engl J Med" and no extra doi/PMID (0.2 pts)
  Component 2: Reference 2 uses correct volume/issue format "2023;147(8):612-625" (0.2 pts)
  Component 3: Reference 3 uses abbreviated journal "J Am Coll Cardiol", includes issue number, no trailing info (0.2 pts)
  Component 4: Reference 4 uses abbreviated journal "Nat Med", correct Vancouver format, no extra URL (0.2 pts)
  Component 5: Reference 5 uses abbreviated journal "Eur Heart J", correct punctuation (0.2 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_047'
FILE_PATH = '/home/user/Desktop/proposals/grant_proposal.docx'


def verify_task(file_path):
    """
    Verify that grant_proposal.docx references section has been corrected to Vancouver citation style.
    Vancouver style requirements:
      - Authors. Title. Abbreviated journal name. Year;Volume(Issue):Pages.
      - No doi, PMID, impact factor, URLs, publisher names in parentheses, or other trailing info
      - Volume/issue formatted as Year;Vol(Issue):Pages (no "Vol.", "No.", "pp.", etc.)

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

    # Collect all paragraph texts for inspection
    paragraphs = [p.text.strip() for p in doc.paragraphs]

    # Find the references section - look for paragraphs that start with "1.", "2.", etc.
    ref_paras = []
    in_refs = False
    for para_text in paragraphs:
        if 'references' in para_text.lower() and len(para_text) < 50:
            in_refs = True
            continue
        if in_refs and para_text:
            # Collect numbered reference lines
            if re.match(r'^\d+\.', para_text):
                ref_paras.append(para_text)

    print(f"Found {len(ref_paras)} reference entries")
    for i, r in enumerate(ref_paras, 1):
        print(f"  Ref {i}: {r[:120]}")

    if len(ref_paras) < 5:
        print(f"FAIL: Expected at least 5 references, found {len(ref_paras)}")
        print(f"REWARD: {total_score}")
        return total_score

    # ----------------------------------------------------------------
    # Component 1: Reference 1 - journal abbreviated to "N Engl J Med", no doi/PMID/trailing info
    # Initial:  "...The New England Journal of Medicine. 2023;388(14):1285-1298. doi:10.1056/... PMID: ..."
    # Golden:   "...N Engl J Med. 2023;388(14):1285-1298."
    # ----------------------------------------------------------------
    try:
        ref1 = ref_paras[0]
        has_abbreviated_journal = 'N Engl J Med' in ref1
        has_no_doi = 'doi' not in ref1.lower() and 'DOI' not in ref1
        has_no_pmid = 'PMID' not in ref1 and 'pmid' not in ref1.lower()
        has_no_full_name = 'New England Journal of Medicine' not in ref1
        # Check correct volume format: 2023;388(14):1285-1298
        has_correct_vol_format = bool(re.search(r'2023;388\(14\):1285-1298', ref1))

        ref1_pass = has_abbreviated_journal and has_no_doi and has_no_pmid and has_correct_vol_format
        if ref1_pass:
            print(f"PASS: Component 1 — Ref 1 uses 'N Engl J Med', correct format, no extra info (0.2 pts)")
            total_score += 0.2
        else:
            issues = []
            if not has_abbreviated_journal:
                issues.append(f"journal not abbreviated (found full name or wrong abbrev)")
            if not has_no_doi:
                issues.append("contains doi")
            if not has_no_pmid:
                issues.append("contains PMID")
            if not has_correct_vol_format:
                issues.append("volume format incorrect (expected '2023;388(14):1285-1298')")
            print(f"FAIL: Component 1 — Ref 1 issues: {'; '.join(issues)}")
            print(f"  Actual: {ref1[:120]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Reference 2 - correct volume/issue format "2023;147(8):612-625"
    # Initial:  "...Circulation. Vol. 147, No. 8 (2023):pp. 612-625."
    # Golden:   "...Circulation. 2023;147(8):612-625."
    # ----------------------------------------------------------------
    try:
        ref2 = ref_paras[1]
        has_correct_format = bool(re.search(r'2023;147\(8\):612-625', ref2))
        has_no_vol_prefix = 'Vol.' not in ref2 and 'Vol ' not in ref2
        has_no_no_prefix = 'No.' not in ref2 and 'No ' not in ref2
        has_no_pp = 'pp.' not in ref2.lower()

        ref2_pass = has_correct_format and has_no_vol_prefix and has_no_no_prefix
        if ref2_pass:
            print(f"PASS: Component 2 — Ref 2 uses correct volume/issue format '2023;147(8):612-625' (0.2 pts)")
            total_score += 0.2
        else:
            issues = []
            if not has_correct_format:
                issues.append("volume/issue format incorrect (expected '2023;147(8):612-625')")
            if not has_no_vol_prefix:
                issues.append("contains 'Vol.' prefix")
            if not has_no_no_prefix:
                issues.append("contains 'No.' prefix")
            print(f"FAIL: Component 2 — Ref 2 issues: {'; '.join(issues)}")
            print(f"  Actual: {ref2[:120]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Reference 3 - abbreviated journal, includes issue number, no trailing info
    # Initial:  "...Journal of the American College of Cardiology. 2022;80:445-462. Impact factor: 24.0. Highly cited paper."
    # Golden:   "...J Am Coll Cardiol. 2022;80(4):445-462."
    # ----------------------------------------------------------------
    try:
        ref3 = ref_paras[2]
        has_abbreviated_journal = 'J Am Coll Cardiol' in ref3
        has_no_full_name = 'Journal of the American College of Cardiology' not in ref3
        has_correct_format = bool(re.search(r'2022;80\(4\):445-462', ref3))
        has_no_trailing_info = 'Impact factor' not in ref3 and 'Highly cited' not in ref3

        ref3_pass = has_abbreviated_journal and has_correct_format and has_no_trailing_info
        if ref3_pass:
            print(f"PASS: Component 3 — Ref 3 uses 'J Am Coll Cardiol', correct issue '(4)', no trailing info (0.2 pts)")
            total_score += 0.2
        else:
            issues = []
            if not has_abbreviated_journal:
                issues.append("journal not abbreviated to 'J Am Coll Cardiol'")
            if not has_correct_format:
                issues.append("volume/issue format incorrect (expected '2022;80(4):445-462')")
            if not has_no_trailing_info:
                issues.append("contains trailing info (impact factor or 'highly cited')")
            print(f"FAIL: Component 3 — Ref 3 issues: {'; '.join(issues)}")
            print(f"  Actual: {ref3[:150]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Reference 4 - abbreviated journal "Nat Med", correct format, no extra URL/info
    # Initial:  "...Nature Medicine. 2023, Volume 29, Issue 3, March 2023: pages 678-691. Epub ahead of print available at: https://..."
    # Golden:   "...Nat Med. 2023;29(3):678-691."
    # ----------------------------------------------------------------
    try:
        ref4 = ref_paras[3]
        has_abbreviated_journal = 'Nat Med' in ref4
        has_no_full_name = 'Nature Medicine' not in ref4
        has_correct_format = bool(re.search(r'2023;29\(3\):678-691', ref4))
        has_no_url = 'http' not in ref4 and 'doi.org' not in ref4
        has_no_extra = 'Epub' not in ref4 and 'ahead of print' not in ref4 and 'Volume 29' not in ref4

        ref4_pass = has_abbreviated_journal and has_correct_format and has_no_url and has_no_extra
        if ref4_pass:
            print(f"PASS: Component 4 — Ref 4 uses 'Nat Med', correct format '2023;29(3):678-691', no extra URL/info (0.2 pts)")
            total_score += 0.2
        else:
            issues = []
            if not has_abbreviated_journal:
                issues.append("journal not abbreviated to 'Nat Med'")
            if not has_correct_format:
                issues.append("volume/issue format incorrect (expected '2023;29(3):678-691')")
            if not has_no_url:
                issues.append("contains URL")
            if not has_no_extra:
                issues.append("contains extra info (Epub, 'ahead of print', or 'Volume 29')")
            print(f"FAIL: Component 4 — Ref 4 issues: {'; '.join(issues)}")
            print(f"  Actual: {ref4[:150]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: Reference 5 - abbreviated journal "Eur Heart J", correct punctuation
    # Initial:  "...European Heart Journal (Oxford University Press). 2022:43(44);4218-4231."
    # Golden:   "...Eur Heart J. 2022;43(44):4218-4231."
    # ----------------------------------------------------------------
    try:
        ref5 = ref_paras[4]
        has_abbreviated_journal = 'Eur Heart J' in ref5
        has_no_full_name = 'European Heart Journal' not in ref5
        has_no_publisher = 'Oxford University Press' not in ref5
        # Correct Vancouver format: Year;Vol(Issue):Pages  (semicolon before volume, colon before pages)
        has_correct_format = bool(re.search(r'2022;43\(44\):4218-4231', ref5))

        ref5_pass = has_abbreviated_journal and has_no_publisher and has_correct_format
        if ref5_pass:
            print(f"PASS: Component 5 — Ref 5 uses 'Eur Heart J', correct format '2022;43(44):4218-4231', no publisher (0.2 pts)")
            total_score += 0.2
        else:
            issues = []
            if not has_abbreviated_journal:
                issues.append("journal not abbreviated to 'Eur Heart J'")
            if not has_no_publisher:
                issues.append("contains publisher name '(Oxford University Press)'")
            if not has_correct_format:
                issues.append("punctuation/format incorrect (expected '2022;43(44):4218-4231')")
            print(f"FAIL: Component 5 — Ref 5 issues: {'; '.join(issues)}")
            print(f"  Actual: {ref5[:150]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
