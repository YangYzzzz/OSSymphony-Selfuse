"""
Reward Script: Verify AutoCorrect entry 'sig1' with formatted signature
Task ID: writer_frd_052
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): AutoCorrect .dat file exists and contains 'sig1' entry in DocumentList.xml
  Component 2 (0.30): sig1.xml contains bold text 'Dr. Robert Chen'
  Component 3 (0.20): sig1.xml contains italic text 'Director of Research'
  Component 4 (0.20): Entry is formatted text (sig1.xml present, not plain text only)
"""

import os
import glob
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_052'

# LibreOffice autocorrect .dat files are stored here
AUTOCORR_DIR = os.path.expanduser('~/.config/libreoffice/4/user/autocorr')


def find_autocorr_dat():
    """Find the autocorrect .dat file (could be any locale)."""
    if not os.path.isdir(AUTOCORR_DIR):
        return None
    dat_files = glob.glob(os.path.join(AUTOCORR_DIR, 'acor_*.dat'))
    for dat_file in dat_files:
        try:
            with zipfile.ZipFile(dat_file, 'r') as z:
                if 'DocumentList.xml' in z.namelist():
                    return dat_file
        except Exception:
            continue
    return None


def verify_task():
    """
    Verify that an AutoCorrect entry 'sig1' has been created with formatted signature.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    dat_path = find_autocorr_dat()

    # Component 1: AutoCorrect .dat exists with 'sig1' entry in DocumentList.xml (0.30 points)
    try:
        if dat_path is None:
            print("FAIL: Component 1 -- No autocorrect .dat file found in %s" % AUTOCORR_DIR)
        else:
            with zipfile.ZipFile(dat_path, 'r') as z:
                doc_list = z.read('DocumentList.xml').decode('utf-8')
            # Check that 'sig1' appears as an abbreviated-name in DocumentList.xml
            if 'abbreviated-name="sig1"' in doc_list:
                print("PASS: Component 1 -- 'sig1' entry found in DocumentList.xml (0.30 pts)")
                total_score += 0.30
            else:
                print("FAIL: Component 1 -- 'sig1' not found in DocumentList.xml. Content: %s" % doc_list[:500])
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)

    # Component 2: sig1.xml contains bold text 'Dr. Robert Chen' (0.30 points)
    try:
        if dat_path is None:
            print("FAIL: Component 2 -- No autocorrect .dat file")
        else:
            with zipfile.ZipFile(dat_path, 'r') as z:
                if 'sig1.xml' not in z.namelist():
                    print("FAIL: Component 2 -- sig1.xml not found in .dat archive")
                else:
                    sig1_content = z.read('sig1.xml').decode('utf-8')
                    # Check for bold formatting and the name text
                    has_bold = 'font-weight="bold"' in sig1_content or 'fo:font-weight="bold"' in sig1_content
                    has_name = 'Dr. Robert Chen' in sig1_content
                    if has_bold and has_name:
                        print("PASS: Component 2 -- Bold 'Dr. Robert Chen' found in sig1.xml (0.30 pts)")
                        total_score += 0.30
                    elif has_name and not has_bold:
                        print("FAIL: Component 2 -- 'Dr. Robert Chen' found but NOT bold")
                    elif has_bold and not has_name:
                        print("FAIL: Component 2 -- Bold formatting found but 'Dr. Robert Chen' text missing")
                    else:
                        print("FAIL: Component 2 -- Neither bold nor 'Dr. Robert Chen' found in sig1.xml")
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: sig1.xml contains italic text 'Director of Research' (0.20 points)
    try:
        if dat_path is None:
            print("FAIL: Component 3 -- No autocorrect .dat file")
        else:
            with zipfile.ZipFile(dat_path, 'r') as z:
                if 'sig1.xml' not in z.namelist():
                    print("FAIL: Component 3 -- sig1.xml not found in .dat archive")
                else:
                    sig1_content = z.read('sig1.xml').decode('utf-8')
                    has_italic = 'font-style="italic"' in sig1_content or 'fo:font-style="italic"' in sig1_content
                    has_title = 'Director of Research' in sig1_content
                    if has_italic and has_title:
                        print("PASS: Component 3 -- Italic 'Director of Research' found in sig1.xml (0.20 pts)")
                        total_score += 0.20
                    elif has_title and not has_italic:
                        print("FAIL: Component 3 -- 'Director of Research' found but NOT italic")
                    elif has_italic and not has_title:
                        print("FAIL: Component 3 -- Italic formatting found but 'Director of Research' text missing")
                    else:
                        print("FAIL: Component 3 -- Neither italic nor 'Director of Research' found in sig1.xml")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Entry is formatted text, not plain text (sig1.xml exists as separate file) (0.20 points)
    try:
        if dat_path is None:
            print("FAIL: Component 4 -- No autocorrect .dat file")
        else:
            with zipfile.ZipFile(dat_path, 'r') as z:
                namelist = z.namelist()
                # Formatted text entries have a corresponding .xml file (sig1.xml)
                # Plain text entries only appear in DocumentList.xml with a name attribute
                if 'sig1.xml' in namelist:
                    # Verify it's a proper XML document with office:body content
                    sig1_content = z.read('sig1.xml').decode('utf-8')
                    if '<office:body>' in sig1_content or 'office:document-content' in sig1_content:
                        print("PASS: Component 4 -- sig1.xml is a formatted text entry (0.20 pts)")
                        total_score += 0.20
                    else:
                        print("FAIL: Component 4 -- sig1.xml exists but does not appear to be a formatted text document")
                else:
                    print("FAIL: Component 4 -- sig1.xml not found; entry may be plain text only")
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


verify_task()
