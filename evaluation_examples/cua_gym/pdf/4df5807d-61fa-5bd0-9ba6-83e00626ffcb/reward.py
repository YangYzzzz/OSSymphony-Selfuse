"""
Reward Script: PDF Portfolio Bundle Verification
Task ID: pdf_aw_012
Domain: pdf
Scoring:
  Component 1 (0.25): 8 embedded files present in portfolio
  Component 2 (0.25): Collection structure with 'Pleadings' and 'Evidence' folders
  Component 3 (0.25): Correct folder assignments (plea_* -> Pleadings, evid_* -> Evidence)
  Component 4 (0.25): Cover page lists all 8 document names
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_012'
BUNDLE_PATH = os.path.join(WORKDIR, 'legal', 'case_bundle.pdf')

# Expected files
EXPECTED_PLEADINGS = {'plea_complaint.pdf', 'plea_answer.pdf', 'plea_motion.pdf'}
EXPECTED_EVIDENCE = {'evid_photo_01.pdf', 'evid_photo_02.pdf', 'evid_transcript.pdf',
                     'evid_report.pdf', 'evid_diagram.pdf'}
ALL_EXPECTED = EXPECTED_PLEADINGS | EXPECTED_EVIDENCE


def get_folder_name_for_file(fspec):
    """Extract the folder name from a filespec's /CI dictionary."""
    try:
        ci = fspec['/CI']
        folder_ref = ci['/F']
        return str(folder_ref['/Name'])
    except Exception:
        return None


def collect_folder_names(folder_node, names=None):
    """Recursively collect all folder names from the Collection/Folders tree."""
    if names is None:
        names = set()
    try:
        name = str(folder_node['/Name'])
        names.add(name)
    except Exception:
        pass
    # Check for child folders
    if '/Child' in folder_node:
        child = folder_node['/Child']
        collect_folder_names(child, names)
        # Traverse siblings via /Next
        node = child
        while '/Next' in node:
            node = node['/Next']
            collect_folder_names(node, names)
    return names


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load with pikepdf for portfolio/collection structure inspection
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    root = pdf.Root

    # Component 1: 8 embedded files present (0.25 points)
    try:
        embedded_names = set()
        if '/Names' in root and '/EmbeddedFiles' in root['/Names']:
            ef_names = root['/Names']['/EmbeddedFiles']
            if '/Names' in ef_names:
                name_list = list(ef_names['/Names'])
                for i in range(0, len(name_list), 2):
                    embedded_names.add(str(name_list[i]))

        if embedded_names == ALL_EXPECTED:
            print(f"PASS: Component 1 - All 8 expected files embedded: {sorted(embedded_names)} (0.25 pts)")
            total_score += 0.25
        else:
            missing = ALL_EXPECTED - embedded_names
            extra = embedded_names - ALL_EXPECTED
            print(f"FAIL: Component 1 - Embedded files mismatch. Found {len(embedded_names)}: {sorted(embedded_names)}")
            if missing:
                print(f"  Missing: {sorted(missing)}")
            if extra:
                print(f"  Extra: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Collection structure with 'Pleadings' and 'Evidence' folders (0.25 points)
    try:
        if '/Collection' in root and '/Folders' in root['/Collection']:
            folder_root = root['/Collection']['/Folders']
            all_folder_names = collect_folder_names(folder_root)
            # Remove the root folder name (e.g., "Case Bundle") - we care about sub-folders
            has_pleadings = 'Pleadings' in all_folder_names
            has_evidence = 'Evidence' in all_folder_names
            if has_pleadings and has_evidence:
                print(f"PASS: Component 2 - Portfolio has 'Pleadings' and 'Evidence' folders (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Missing folders. Found: {sorted(all_folder_names)}. "
                      f"Pleadings: {has_pleadings}, Evidence: {has_evidence}")
        else:
            print("FAIL: Component 2 - No Collection/Folders structure found in PDF")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Correct folder assignments (0.25 points)
    # plea_* files -> Pleadings folder, evid_* files -> Evidence folder
    try:
        if '/Names' in root and '/EmbeddedFiles' in root['/Names']:
            ef_names = root['/Names']['/EmbeddedFiles']
            if '/Names' in ef_names:
                name_list = list(ef_names['/Names'])
                folder_assignments = {}
                for i in range(0, len(name_list), 2):
                    fname = str(name_list[i])
                    fspec = name_list[i + 1]
                    folder_name = get_folder_name_for_file(fspec)
                    folder_assignments[fname] = folder_name

                correct_count = 0
                total_checks = 0
                for fname in ALL_EXPECTED:
                    if fname in folder_assignments:
                        total_checks += 1
                        assigned = folder_assignments[fname]
                        if fname.startswith('plea_') and assigned == 'Pleadings':
                            correct_count += 1
                        elif fname.startswith('evid_') and assigned == 'Evidence':
                            correct_count += 1
                        else:
                            expected_folder = 'Pleadings' if fname.startswith('plea_') else 'Evidence'
                            print(f"  WRONG: {fname} assigned to '{assigned}', expected '{expected_folder}'")

                if correct_count == len(ALL_EXPECTED) and total_checks == len(ALL_EXPECTED):
                    print(f"PASS: Component 3 - All 8 files correctly assigned to folders (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 - {correct_count}/{len(ALL_EXPECTED)} files correctly assigned")
            else:
                print("FAIL: Component 3 - No embedded file names found")
        else:
            print("FAIL: Component 3 - No embedded files structure")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    pdf.close()

    # Component 4: Cover page lists all 8 document names (0.25 points)
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        if len(doc) < 1:
            print("FAIL: Component 4 - No pages in PDF (no cover page)")
        else:
            page = doc[0]
            text = page.get_text('text').lower()

            # Check that each of the 8 file names appears on the cover page
            found_names = set()
            for fname in ALL_EXPECTED:
                # Check for the filename (with or without .pdf extension)
                name_no_ext = fname.replace('.pdf', '')
                if fname.lower() in text or name_no_ext.lower() in text:
                    found_names.add(fname)

            if found_names == ALL_EXPECTED:
                print(f"PASS: Component 4 - Cover page lists all 8 document names (0.25 pts)")
                total_score += 0.25
            else:
                missing = ALL_EXPECTED - found_names
                print(f"FAIL: Component 4 - Cover page missing {len(missing)} document names: {sorted(missing)}")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(BUNDLE_PATH):
    print(f"File not found: {BUNDLE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(BUNDLE_PATH)
