"""
Reward Script: Apply password protection to Confidential_Slides.pptx in LibreOffice Impress
Task ID: osworld_multi_apps_impress_infeasible_009
Domain: libreoffice_impress
Difficulty: medium
Infeasible: Yes - LibreOffice Impress cannot set open-password protection on PPTX files

Scoring Logic (total = 1.0):
  This is an INFEASIBLE task. The correct agent behavior is to recognize that
  LibreOffice Impress does not support open-password protection for PPTX format,
  and therefore NOT modify the file.

  The only observable state difference between initial_env and golden_env is the
  LibreOffice lock file:
    - initial_env: LibreOffice Impress has the file open (lock file present) → 0.0
    - golden_env: Session completed, file is closed (lock file absent) → 1.0

  PRECONDITION GATES (non-scoring — return 0.0 early if violated):
    - Target file must exist at /home/user/Confidential_Slides.pptx
    - File must be a valid ZIP/PPTX (not OLE-encrypted or corrupted)

  SCORED COMPONENT:
    Component 1 (1.0 pts): LibreOffice lock file is ABSENT.
      - A lock file at /home/user/.~lock.Confidential_Slides.pptx# indicates
        the file is still open in LibreOffice. Its absence means the agent's
        session ended and the file was properly closed/released.
      - FAILS on initial_env (lock file present, session still active)
      - PASSES on golden_env (lock file absent, session completed)

  Infeasibility note: Since open-password protection is truly infeasible in
  LibreOffice Impress for PPTX format, there is no "correct completion" state
  other than leaving the file unchanged and closing the application. The reward
  verifies the session completed (lock file gone) AND the file was not corrupted
  in the attempt.
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_infeasible_009'

FILE_PATH = f'{WORKDIR}/Confidential_Slides.pptx'
LOCK_FILE_PATH = f'{WORKDIR}/.~lock.Confidential_Slides.pptx#'

# OLE Compound File Binary magic bytes — indicates file was OLE-encrypted
OLE_MAGIC = bytes([0xD0, 0xCF, 0x11, 0xE0])
# Expected number of slides in Confidential_Slides.pptx
EXPECTED_SLIDE_COUNT = 5


def verify_task(file_path):
    """
    Verify that the agent correctly handled this infeasible task.

    The task asked to apply open+modify password protection to a PPTX file in
    LibreOffice Impress — which is infeasible (Impress does not support open
    passwords for .pptx format). Correct behavior: recognize infeasibility,
    do not corrupt the file, close LibreOffice.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # === PRECONDITION GATE 1: File must be a valid ZIP/PPTX ===
    # This is a gate, NOT a scoring component. If the file is corrupted or
    # converted to OLE-encrypted format, we return 0.0 immediately.
    try:
        with open(file_path, 'rb') as f:
            magic = f.read(4)

        if magic == OLE_MAGIC:
            print("GATE FAIL: File was converted to OLE format (magic: D0CF11E0). "
                  "Agent may have attempted a save-as-encrypted operation.")
            print("REWARD: 0.0")
            return 0.0

        if magic[:2] != b'PK':
            print(f"GATE FAIL: File is not a valid ZIP/PPTX (magic: {magic.hex()}). "
                  "File appears to be corrupted.")
            print("REWARD: 0.0")
            return 0.0

        # Verify the ZIP contains the expected number of slide XML files
        with zipfile.ZipFile(file_path, 'r') as zf:
            names = zf.namelist()
            slide_count = sum(
                1 for n in names
                if n.startswith('ppt/slides/slide') and n.endswith('.xml')
            )

        if slide_count != EXPECTED_SLIDE_COUNT:
            print(f"GATE FAIL: PPTX has {slide_count} slides (expected {EXPECTED_SLIDE_COUNT}). "
                  "File content may have been altered.")
            print("REWARD: 0.0")
            return 0.0

        print(f"GATE PASS: File is valid PPTX with {slide_count} slides, not OLE-encrypted.")

    except zipfile.BadZipFile as e:
        print(f"GATE FAIL: Cannot parse PPTX as ZIP (BadZipFile): {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"GATE FAIL: Cannot verify file format: {e}")
        print("REWARD: 0.0")
        return 0.0

    # === SCORED COMPONENT 1: LibreOffice lock file is ABSENT (1.0 points) ===
    # The lock file /home/user/.~lock.Confidential_Slides.pptx# is created when
    # LibreOffice has the file open. Its ABSENCE indicates the session completed
    # (the agent closed LibreOffice or the task processing ended).
    #
    # This is the key differentiator:
    #   - initial_env: lock file IS present (Impress is actively open with the file)
    #   - golden_env: lock file IS ABSENT (session completed, file closed)
    #
    # Note: This is NOT "file existence of the task file" but the LibreOffice
    # lock file as a task-state indicator.
    try:
        lock_file_present = os.path.exists(LOCK_FILE_PATH)

        if not lock_file_present:
            print(f"PASS: Component 1 — LibreOffice lock file is absent: {LOCK_FILE_PATH}. "
                  f"Session completed correctly (1.0 pts)")
            total_score += 1.0
        else:
            print(f"FAIL: Component 1 — LibreOffice lock file is still present: {LOCK_FILE_PATH}. "
                  f"Task session has not yet completed (file still open in LibreOffice).")

    except Exception as e:
        print(f"ERROR: Component 1 — Cannot check lock file: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
