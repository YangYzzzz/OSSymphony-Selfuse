"""
Reward Script: Compile memoir chapters into a single EPUB file
Task ID: osworld_multi_apps_misc_073
Domain: os (multi-app: Chrome + file system + EPUB creation)

Scoring:
  Component 1: EPUB file exists at the expected path              (0.4 pts)
  Component 2: EPUB is a valid EPUB3 package with proper structure (0.3 pts)
  Component 3: EPUB contains all 5 source chapters as content     (0.3 pts)
  Total: 1.0

NOTE: The task requires creating A_Life_Lived.epub or A Life Lived.epub
in ~/Documents/Memoir/A_Life_Lived/ by combining all 5 .txt files.
Initial state has only the 5 .txt files (no EPUB).
Golden state has the EPUB plus the original .txt files.
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_073'
MEMOIR_DIR = f'{WORKDIR}/Documents/Memoir/A_Life_Lived'

# Possible EPUB filenames the agent might produce
EPUB_CANDIDATES = [
    'A_Life_Lived.epub',
    'A Life Lived.epub',
]

EXPECTED_CHAPTERS = ['prologue', 'chapter_01', 'chapter_02', 'chapter_03', 'epilogue']


def find_epub(dir_path):
    """Find an EPUB file in the given directory matching expected names."""
    if not os.path.isdir(dir_path):
        return None
    for candidate in EPUB_CANDIDATES:
        full_path = os.path.join(dir_path, candidate)
        if os.path.isfile(full_path):
            return full_path
    # Fallback: find any .epub in the dir
    for fname in os.listdir(dir_path):
        if fname.endswith('.epub'):
            return os.path.join(dir_path, fname)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: EPUB file exists in the correct directory (0.4 points)
    # This FAILS on initial_env (no EPUB present) and PASSES on golden_env.
    try:
        epub_path = find_epub(MEMOIR_DIR)
        if epub_path is not None:
            print(f"PASS: Component 1 — EPUB file found at {epub_path} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No EPUB file found in {MEMOIR_DIR}")
            # No point continuing — file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check for EPUB: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: EPUB is a valid ZIP with required EPUB3 structure (0.3 points)
    # Checks: valid ZIP, has mimetype='application/epub+zip', has META-INF/container.xml,
    # and has an OPF file with a <dc:title> indicating a memoir/book title.
    try:
        with zipfile.ZipFile(epub_path, 'r') as zf:
            namelist = zf.namelist()

            # Check mimetype file is present and correct (required by EPUB spec)
            has_mimetype = 'mimetype' in namelist
            if has_mimetype:
                mime_content = zf.read('mimetype').decode('utf-8', errors='replace').strip()
                valid_mimetype = mime_content == 'application/epub+zip'
            else:
                valid_mimetype = False

            # Check META-INF/container.xml is present
            has_container = 'META-INF/container.xml' in namelist

            # Look for an OPF file anywhere in the archive
            opf_files = [n for n in namelist if n.endswith('.opf') or n.endswith('content.opf')]
            has_opf = len(opf_files) > 0

            if valid_mimetype and has_container and has_opf:
                print(f"PASS: Component 2 — Valid EPUB3 structure: mimetype OK, container.xml present, OPF found ({opf_files[0]}) (0.3 pts)")
                total_score += 0.3
            else:
                issues = []
                if not valid_mimetype:
                    issues.append(f"mimetype missing or wrong (has_mimetype={has_mimetype}, valid={valid_mimetype})")
                if not has_container:
                    issues.append("META-INF/container.xml missing")
                if not has_opf:
                    issues.append("No OPF package file found")
                print(f"FAIL: Component 2 — Invalid EPUB structure: {'; '.join(issues)}")
    except zipfile.BadZipFile as e:
        print(f"FAIL: Component 2 — EPUB is not a valid ZIP/EPUB archive: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not validate EPUB structure: {e}")

    # Component 3: EPUB contains all 5 chapter files as content items (0.3 points)
    # Each of the 5 source .txt files should be represented as an XHTML chapter.
    # This FAILS on initial_env and PASSES on golden_env.
    try:
        with zipfile.ZipFile(epub_path, 'r') as zf:
            namelist = zf.namelist()
            # Look for each expected chapter name as part of any XHTML/HTML/NCX/OPF entry
            content_text = ' '.join(namelist).lower()

            chapters_found = []
            chapters_missing = []
            for chapter in EXPECTED_CHAPTERS:
                # Check if chapter name appears in any entry (xhtml or referenced in opf/ncx)
                chapter_lower = chapter.lower().replace('_', '').replace('-', '')
                found_in_names = any(
                    chapter_lower in name.lower().replace('_', '').replace('-', '')
                    for name in namelist
                )
                if found_in_names:
                    chapters_found.append(chapter)
                else:
                    # Also check OPF manifest text for references to this chapter
                    opf_files = [n for n in namelist if n.endswith('.opf')]
                    opf_matches = [
                        opf_file for opf_file in opf_files
                        if chapter_lower in zf.read(opf_file).decode('utf-8', errors='replace').lower().replace('_', '').replace('-', '')
                    ]
                    if len(opf_matches) > 0:
                        chapters_found.append(chapter)
                    else:
                        chapters_missing.append(chapter)

            if len(chapters_missing) == 0:
                print(f"PASS: Component 3 — All 5 chapters found in EPUB: {chapters_found} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Missing chapters in EPUB: {chapters_missing} (found: {chapters_found})")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify chapter content: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
