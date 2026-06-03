"""
Reward Script: Save NDA document as Writer template (.ott)
Task ID: writer_legal_080
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) - OTT file exists and is a valid ZIP archive
  Component 2 (0.35) - OTT mimetype is application/vnd.oasis.opendocument.text-template
  Component 3 (0.30) - OTT contains NDA content matching the source document
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_080'

def verify_task():
    """
    Verify that the NDA document has been saved as a .ott template file.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ott_path = os.path.join(WORKDIR, f'{TASK_ID}.ott')

    # Precondition: source docx must still exist (not corrupted/deleted)
    docx_path = os.path.join(WORKDIR, f'{TASK_ID}.docx')
    if not os.path.exists(docx_path):
        print(f"PRECONDITION FAIL: Source docx not found at {docx_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: OTT file exists and is a valid ZIP archive (0.35 points)
    # This FAILS on initial (no .ott) -> PASSES on golden (has .ott)
    try:
        if os.path.exists(ott_path) and os.path.getsize(ott_path) > 0:
            try:
                with zipfile.ZipFile(ott_path, 'r') as z:
                    namelist = z.namelist()
                    if len(namelist) > 0:
                        print(f"PASS: Component 1 - OTT file exists and is valid ZIP ({os.path.getsize(ott_path)} bytes, {len(namelist)} entries) (0.35 pts)")
                        total_score += 0.35
                    else:
                        print(f"FAIL: Component 1 - OTT file is empty ZIP archive")
            except zipfile.BadZipFile:
                print(f"FAIL: Component 1 - OTT file exists but is not a valid ZIP")
        else:
            print(f"FAIL: Component 1 - OTT file not found at {ott_path}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: OTT mimetype is correct ODF text-template (0.35 points)
    # This FAILS on initial (no .ott) -> PASSES on golden (correct mimetype)
    try:
        if os.path.exists(ott_path):
            with zipfile.ZipFile(ott_path, 'r') as z:
                if 'mimetype' in z.namelist():
                    mimetype = z.read('mimetype').decode('utf-8').strip()
                    if mimetype == 'application/vnd.oasis.opendocument.text-template':
                        print(f"PASS: Component 2 - Correct OTT mimetype: {mimetype} (0.35 pts)")
                        total_score += 0.35
                    elif mimetype == 'application/vnd.oasis.opendocument.text':
                        print(f"FAIL: Component 2 - File is ODT (document), not OTT (template). Mimetype: {mimetype}")
                    else:
                        print(f"FAIL: Component 2 - Wrong mimetype: {mimetype}")
                else:
                    print(f"FAIL: Component 2 - No mimetype entry in OTT archive")
        else:
            print(f"FAIL: Component 2 - OTT file not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: OTT contains NDA content (0.30 points)
    # Verify the template actually has NDA content, not an empty template
    # This FAILS on initial (no .ott) -> PASSES on golden (has NDA content in .ott)
    try:
        if os.path.exists(ott_path):
            with zipfile.ZipFile(ott_path, 'r') as z:
                if 'content.xml' in z.namelist():
                    content_xml = z.read('content.xml').decode('utf-8')
                    # Extract text from content.xml
                    text_portions = re.findall(r'>([^<]+)<', content_xml)
                    full_text = ' '.join(t.strip() for t in text_portions if t.strip()).lower()

                    # Check for key NDA phrases that must be present
                    nda_markers = [
                        'non-disclosure agreement',
                        'confidential information',
                        'receiving party',
                        'disclosing party',
                    ]
                    found_count = sum(1 for marker in nda_markers if marker in full_text)

                    if found_count >= 3:
                        print(f"PASS: Component 3 - OTT contains NDA content ({found_count}/{len(nda_markers)} key phrases found) (0.30 pts)")
                        total_score += 0.30
                    elif found_count >= 1:
                        partial = round(0.30 * found_count / len(nda_markers), 2)
                        print(f"PARTIAL: Component 3 - OTT has some NDA content ({found_count}/{len(nda_markers)} phrases). ({partial} pts)")
                        total_score += partial
                    else:
                        print(f"FAIL: Component 3 - OTT does not contain NDA content (0/{len(nda_markers)} key phrases)")
                else:
                    print(f"FAIL: Component 3 - No content.xml in OTT archive")
        else:
            print(f"FAIL: Component 3 - OTT file not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
