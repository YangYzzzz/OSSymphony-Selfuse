"""
Reward Script: Extract Introduction section from PDF and save as training_intro document
Task ID: osworld_multi_apps_pdf_to_gdocs_012
Domain: multi_apps (Chrome/Google Drive)
Scoring:
  Component 1: training_intro.docx file exists AND contains Introduction heading (0.4 pts)
  Component 2: Document contains at least 3 of 5 Introduction subsections (1.1-1.5) (0.3 pts)
  Component 3: Document contains substantial Introduction content — all 5 subsections (0.3 pts)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_012'

# Canonical file paths to check (could be stored locally as .docx)
CANDIDATE_PATHS = [
    os.path.join(WORKDIR, 'training_intro.docx'),
    os.path.join(WORKDIR, 'Documents', 'training_intro.docx'),
    os.path.join(WORKDIR, 'Desktop', 'training_intro.docx'),
    os.path.join(WORKDIR, 'Downloads', 'training_intro.docx'),
]

# Expected Introduction subsection headings from PDF section 1
EXPECTED_SUBSECTIONS = [
    '1.1',  # Welcome to Acme Corporation
    '1.2',  # Our Mission and Values
    '1.3',  # Scope and Purpose of This Manual
    '1.4',  # How to Use This Manual
    '1.5',  # Organizational Structure
]

# Key content snippets that should appear in the Introduction section
KEY_CONTENT_SNIPPETS = [
    'acme corporation',     # company name, appears in intro
    'mission',              # mission section
    'introduction',         # section heading
]


def find_docx_file():
    """Find the training_intro.docx file in candidate locations."""
    for path in CANDIDATE_PATHS:
        if os.path.exists(path):
            return path
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Gate: find the output file ---
    file_path = find_docx_file()

    # Component 1: File exists AND contains the Introduction heading (0.4 points)
    # This FAILS on initial_env (no such file) and PASSES on golden_env.
    try:
        if file_path is None:
            print(f"FAIL: Component 1 — training_intro.docx not found in any candidate location")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Try to load the document
        try:
            doc = Document(file_path)
        except Exception as e:
            print(f"FAIL: Component 1 — Cannot load {file_path}: {e}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Extract all paragraph text for analysis
        all_text = [para.text.strip() for para in doc.paragraphs]
        all_text_lower = [t.lower() for t in all_text]
        combined_text = ' '.join(all_text)
        combined_lower = combined_text.lower()

        # Check that document contains "Introduction" (section heading)
        has_introduction_heading = any(
            'introduction' in t for t in all_text_lower
        )

        # Check for specific heading text "1. Introduction" or similar
        has_intro_number = any(
            ('1.' in t and 'introduction' in t.lower()) or
            t.lower().strip() == 'introduction'
            for t in all_text
        )

        if has_introduction_heading and has_intro_number:
            print(f"PASS: Component 1 — File {file_path} found and contains 'Introduction' heading (0.4 pts)")
            total_score += 0.4
        elif has_introduction_heading:
            print(f"PASS: Component 1 — File {file_path} found and contains introduction content (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — File found at {file_path} but does not contain Introduction heading")
            print(f"  Found headings: {[t for t in all_text if t][:5]}")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document contains at least 3 of 5 Introduction subsections (0.3 points)
    # Subsections 1.1, 1.2, 1.3, 1.4, 1.5 should appear in doc
    # This FAILS on initial_env (no file) and PASSES on golden_env (has all subsections).
    try:
        if file_path is None:
            print(f"FAIL: Component 2 — No file to check")
        else:
            found_subsections = []
            for subsec in EXPECTED_SUBSECTIONS:
                if any(subsec in t for t in all_text):
                    found_subsections.append(subsec)

            if len(found_subsections) >= 3:
                print(f"PASS: Component 2 — Found {len(found_subsections)}/5 subsections: {found_subsections} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Only found {len(found_subsections)}/5 subsections: {found_subsections}")
                print(f"  Expected at least 3 of: {EXPECTED_SUBSECTIONS}")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document contains substantial content — all 5 subsections present (0.3 points)
    # This FAILS on initial_env (no file) and PASSES on golden_env (all 5 subsections present).
    try:
        if file_path is None:
            print(f"FAIL: Component 3 — No file to check")
        else:
            all_subsections_found = all(
                any(subsec in t for t in all_text)
                for subsec in EXPECTED_SUBSECTIONS
            )

            # Also verify the content is substantially from Introduction section
            # by checking for Acme Corporation references and mission text
            has_acme_content = 'acme corporation' in combined_lower
            has_mission_content = 'mission' in combined_lower
            has_organizational_content = 'organizational' in combined_lower or 'organisation' in combined_lower

            # Count non-empty paragraphs to ensure content is substantial (not just headings)
            non_empty_paragraphs = len([t for t in all_text if len(t) > 50])

            if all_subsections_found and has_acme_content and non_empty_paragraphs >= 5:
                print(f"PASS: Component 3 — All 5 subsections present, Acme content confirmed, "
                      f"{non_empty_paragraphs} substantial paragraphs (0.3 pts)")
                total_score += 0.3
            elif all_subsections_found:
                print(f"PASS: Component 3 — All 5 subsections present (0.3 pts)")
                total_score += 0.3
            else:
                missing = [s for s in EXPECTED_SUBSECTIONS
                           if not any(s in t for t in all_text)]
                print(f"FAIL: Component 3 — Missing subsections: {missing}")
                print(f"  has_acme_content={has_acme_content}, "
                      f"non_empty_paragraphs={non_empty_paragraphs}")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
