"""
Reward Script: Set custom XMP metadata on dataset_description.pdf
Task ID: pdf_mbc_016
Domain: pdf (libreoffice_calc domain label, but actual PDF task)
Scoring:
  - Component 1: dc:rights == 'CC BY-NC 4.0'          (0.35 pts)
  - Component 2: dc:language contains 'en-US'          (0.35 pts)
  - Component 3: dc:publisher contains 'Open Science Foundation' (0.30 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_016'
FILE_PATH = os.path.join(WORKDIR, 'Research', 'dataset_description.pdf')


def verify_task(file_path):
    """
    Verify XMP metadata was correctly set on the PDF.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable by pikepdf
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read XMP metadata
    try:
        meta_ctx = pdf.open_metadata()
        meta = meta_ctx.__enter__()
    except Exception as e:
        print(f"CRITICAL: Cannot read XMP metadata: {e}")
        pdf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: dc:rights == 'CC BY-NC 4.0' (0.35 points)
    try:
        dc_rights = meta.get('dc:rights', '')
        # pikepdf may return the value directly as a string
        rights_str = str(dc_rights).strip() if dc_rights else ''
        if rights_str == 'CC BY-NC 4.0':
            print(f"PASS: Component 1 -- dc:rights = '{rights_str}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- expected dc:rights = 'CC BY-NC 4.0', found: '{rights_str}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: dc:language contains 'en-US' (0.35 points)
    try:
        dc_language = meta.get('dc:language', '')
        lang_str = str(dc_language).strip() if dc_language else ''
        # pikepdf returns language as a list like ['en-US'] or as a string
        if 'en-US' in lang_str:
            print(f"PASS: Component 2 -- dc:language contains 'en-US' (value: {lang_str}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- expected dc:language to contain 'en-US', found: '{lang_str}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: dc:publisher contains 'Open Science Foundation' (0.30 points)
    try:
        dc_publisher = meta.get('dc:publisher', '')
        pub_str = str(dc_publisher).strip() if dc_publisher else ''
        # pikepdf returns publisher as a list like ['Open Science Foundation'] or string
        if 'Open Science Foundation' in pub_str:
            print(f"PASS: Component 3 -- dc:publisher contains 'Open Science Foundation' (value: {pub_str}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- expected dc:publisher to contain 'Open Science Foundation', found: '{pub_str}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Cleanup
    try:
        meta_ctx.__exit__(None, None, None)
    except Exception:
        pass
    pdf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
