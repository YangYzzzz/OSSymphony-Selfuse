"""
Reward Script: Convert .txt files in ~/Documents/ShortStories into a single EPUB named ShortStories.epub
Task ID: osworld_multi_apps_misc_068
Domain: os (multi-app: Chrome + file conversion tool)
Scoring:
  Component 1: ShortStories.epub exists at ~/Documents/ShortStories.epub (0.4 pts)
  Component 2: EPUB has valid mimetype (application/epub+zip) (0.2 pts)
  Component 3: EPUB contains content from all 4 source .txt files (0.4 pts)
Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_068'

# Expected EPUB path per task instructions: named after the folder (ShortStories.epub) in ~/Documents/
EPUB_PATH = os.path.join(WORKDIR, 'Documents', 'ShortStories.epub')

# Source text files that should all be included in the EPUB
SOURCE_DIR = os.path.join(WORKDIR, 'Documents', 'ShortStories')
EXPECTED_SOURCE_FILES = [
    'The_Beginning.txt',
    'Middle_Ground.txt',
    'The_Twist.txt',
    'Final_Chapter.txt',
]

# Key phrases from each source file to verify inclusion in EPUB
# These are the opening phrases / distinct content from each .txt file
STORY_MARKERS = {
    'The_Beginning.txt': 'grandmother',        # "tucked behind the loose brick in her grandmother's attic"
    'Middle_Ground.txt': 'ferry',              # "on a creaking ferry crossing to the island"
    'The_Twist.txt': 'silver birch',           # "a calm woodland of silver birch and pine"
    'Final_Chapter.txt': 'Keepers',            # "the Keepers were a loose network of archivists"
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ShortStories.epub file exists at ~/Documents/ShortStories.epub (0.4 points)
    # This is the primary deliverable — the task explicitly asks for a file named after the folder
    try:
        epub_exists = os.path.isfile(EPUB_PATH)
        if epub_exists:
            epub_size = os.path.getsize(EPUB_PATH)
            if epub_size > 100:  # must be non-trivial
                print(f"PASS: Component 1 — ShortStories.epub exists at {EPUB_PATH} (size: {epub_size} bytes) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — ShortStories.epub exists but is too small ({epub_size} bytes), possibly empty")
        else:
            print(f"FAIL: Component 1 — ShortStories.epub not found at {EPUB_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: EPUB has valid EPUB mimetype (application/epub+zip) (0.2 points)
    # A valid EPUB must have a 'mimetype' entry as the first file, containing exactly 'application/epub+zip'
    try:
        if os.path.isfile(EPUB_PATH):
            with zipfile.ZipFile(EPUB_PATH, 'r') as zf:
                namelist = zf.namelist()
                if 'mimetype' in namelist:
                    mimetype_content = zf.read('mimetype').decode('utf-8').strip()
                    if mimetype_content == 'application/epub+zip':
                        print(f"PASS: Component 2 — EPUB has valid mimetype 'application/epub+zip' (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 2 — EPUB mimetype is '{mimetype_content}', expected 'application/epub+zip'")
                else:
                    print(f"FAIL: Component 2 — EPUB has no 'mimetype' entry. Entries found: {namelist[:5]}")
        else:
            print("FAIL: Component 2 — Cannot check mimetype, EPUB file not found")
    except zipfile.BadZipFile:
        print(f"FAIL: Component 2 — File at {EPUB_PATH} is not a valid ZIP/EPUB archive")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: EPUB contains content from all 4 source .txt files (0.4 points)
    # We verify by checking that the EPUB's extracted text contains key phrases from each story.
    # 0.1 points per story file found — partial credit allowed.
    try:
        if os.path.isfile(EPUB_PATH):
            with zipfile.ZipFile(EPUB_PATH, 'r') as zf:
                # Concatenate all text-like EPUB content (xhtml/html files)
                epub_text_content = []
                for entry in zf.namelist():
                    if entry.endswith(('.xhtml', '.html', '.htm', '.txt', '.ncx', '.opf')):
                        try:
                            raw = zf.read(entry).decode('utf-8', errors='replace')
                            epub_text_content.append(raw)
                        except Exception:
                            pass
                combined_text = '\n'.join(epub_text_content)

                stories_found = 0
                for story_file, marker in STORY_MARKERS.items():
                    if marker.lower() in combined_text.lower():
                        print(f"  PASS: Story '{story_file}' content found (marker: '{marker}')")
                        stories_found += 1
                    else:
                        print(f"  FAIL: Story '{story_file}' content NOT found (missing marker: '{marker}')")

                # Award 0.1 per story found (up to 0.4 for all 4)
                if stories_found == 4:
                    print(f"PASS: Component 3 — All 4 stories present in EPUB (0.4 pts)")
                    total_score += 0.4
                elif stories_found == 3:
                    print(f"PARTIAL: Component 3 — 3/4 stories present in EPUB (0.3 pts)")
                    total_score += 0.3
                elif stories_found == 2:
                    print(f"PARTIAL: Component 3 — 2/4 stories present in EPUB (0.2 pts)")
                    total_score += 0.2
                elif stories_found == 1:
                    print(f"PARTIAL: Component 3 — 1/4 stories present in EPUB (0.1 pts)")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 3 — No story content found in EPUB (0.0 pts)")
        else:
            print("FAIL: Component 3 — Cannot check content, EPUB file not found")
    except zipfile.BadZipFile:
        print(f"FAIL: Component 3 — File at {EPUB_PATH} is not a valid ZIP/EPUB archive")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
