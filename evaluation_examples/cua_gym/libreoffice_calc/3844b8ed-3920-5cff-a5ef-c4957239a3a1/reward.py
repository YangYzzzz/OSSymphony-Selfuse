"""
Reward Script: Convert travel text files to EPUB ebook
Task ID: osworld_multi_apps_misc_074
Domain: os (multi-apps)
Scoring:
  Component 1: EPUB file exists in the correct location (0.3 pts)
  Component 2: EPUB has valid EPUB structure and mimetype (0.3 pts)
  Component 3: EPUB contains content from all 4 source text files (0.4 pts)
Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_074'
ESSAYS_DIR = '/home/user/Documents/Essays/Travel_Chronicles'

# Accept both possible EPUB filenames (with space or underscore)
EPUB_NAMES = ['Travel_Chronicles.epub', 'Travel Chronicles.epub']


def verify_task():
    """
    Verify that the user converted all .txt files in ~/Documents/Essays/Travel_Chronicles
    to a single EPUB file named Travel_Chronicles.epub (or 'Travel Chronicles.epub').
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Determine the actual epub path
    epub_path = None
    for name in EPUB_NAMES:
        candidate = os.path.join(ESSAYS_DIR, name)
        if os.path.isfile(candidate):
            epub_path = candidate
            break

    # Also check for any .epub files in the directory
    if epub_path is None:
        try:
            entries = os.listdir(ESSAYS_DIR)
            for entry in entries:
                if entry.lower().endswith('.epub'):
                    epub_path = os.path.join(ESSAYS_DIR, entry)
                    print(f"INFO: Found EPUB with name: {entry}")
                    break
        except Exception as e:
            print(f"ERROR: Cannot list directory {ESSAYS_DIR}: {e}")

    # Component 1: EPUB file exists in the Travel_Chronicles directory (0.3 points)
    # This FAILS on initial_env (no epub), PASSES on golden_env
    try:
        if epub_path is not None and os.path.isfile(epub_path):
            print(f"PASS: Component 1 — EPUB file exists at {epub_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No EPUB file found in {ESSAYS_DIR}")
            print(f"  Checked: {[os.path.join(ESSAYS_DIR, n) for n in EPUB_NAMES]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no epub found, no point continuing
    if epub_path is None or not os.path.isfile(epub_path):
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: EPUB file is a valid EPUB (ZIP with correct mimetype) (0.3 points)
    # This FAILS on initial_env (no epub), PASSES on golden_env
    try:
        if not zipfile.is_zipfile(epub_path):
            print(f"FAIL: Component 2 — File at {epub_path} is not a valid ZIP/EPUB")
        else:
            with zipfile.ZipFile(epub_path, 'r') as z:
                names = z.namelist()
                # Check for required EPUB structure files
                has_mimetype = 'mimetype' in names
                has_container = 'META-INF/container.xml' in names

                if has_mimetype:
                    mimetype_content = z.read('mimetype').decode('utf-8', errors='ignore').strip()
                    valid_mimetype = (mimetype_content == 'application/epub+zip')
                else:
                    valid_mimetype = False

                # Check for at least one content file (html/xhtml/opf)
                has_content_file = any(
                    n.endswith('.html') or n.endswith('.xhtml') or n.endswith('.opf')
                    for n in names
                )

                if valid_mimetype and has_container and has_content_file:
                    print(f"PASS: Component 2 — EPUB has valid structure (mimetype=application/epub+zip, container.xml present, content files present) (0.3 pts)")
                    total_score += 0.3
                elif valid_mimetype:
                    print(f"FAIL: Component 2 — EPUB mimetype is correct but missing container.xml or content files")
                    print(f"  has_container={has_container}, has_content_file={has_content_file}")
                else:
                    print(f"FAIL: Component 2 — EPUB mimetype not 'application/epub+zip', found: '{mimetype_content if has_mimetype else 'no mimetype file'}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: EPUB contains content from all 4 source text files (0.4 points)
    # The 4 source files are: rome.txt, tokyo.txt, nyc.txt, cape_town.txt
    # We check that content from each essay is present in the EPUB
    # This FAILS on initial_env (no epub), PASSES on golden_env
    try:
        # Keywords that should appear in each essay's content
        # Based on what we know: rome, tokyo, nyc/new york city, cape_town
        city_keywords = {
            'rome': ['rome', 'roman', 'pantheon', 'colosseum', 'trastevere', 'italy', 'eternal city'],
            'tokyo': ['tokyo', 'japanese', 'shinjuku', 'shibuya', 'akihabara', 'japan'],
            'nyc': ['new york', 'manhattan', 'brooklyn', 'times square', 'central park', 'nyc'],
            'cape_town': ['cape town', 'table mountain', 'africa', 'south africa', 'atlantic', 'cape'],
        }

        # Read all text content from EPUB
        with zipfile.ZipFile(epub_path, 'r') as z:
            all_epub_text = ''
            for name in z.namelist():
                if name.endswith('.html') or name.endswith('.xhtml') or name.endswith('.htm'):
                    try:
                        content = z.read(name).decode('utf-8', errors='ignore').lower()
                        all_epub_text += content
                    except Exception:
                        pass
                elif name.endswith('.opf') or name.endswith('.ncx'):
                    try:
                        content = z.read(name).decode('utf-8', errors='ignore').lower()
                        all_epub_text += content
                    except Exception:
                        pass

        # Also count the number of content HTML files (should be >= 4 essays)
        with zipfile.ZipFile(epub_path, 'r') as z:
            html_files = [n for n in z.namelist() if n.endswith('.html') or n.endswith('.xhtml') or n.endswith('.htm')]
            num_html = len(html_files)

        cities_found = {}
        for city, keywords in city_keywords.items():
            found = any(kw in all_epub_text for kw in keywords)
            cities_found[city] = found

        num_cities_found = sum(1 for v in cities_found.values() if v)
        print(f"INFO: Component 3 — Cities found in EPUB: {cities_found}")
        print(f"INFO: Component 3 — HTML/XHTML files in EPUB: {num_html}")

        if num_cities_found == 4:
            print(f"PASS: Component 3 — All 4 travel essays (rome, tokyo, nyc, cape_town) found in EPUB (0.4 pts)")
            total_score += 0.4
        elif num_cities_found >= 3:
            # Partial credit: 3 out of 4 essays present
            print(f"PARTIAL: Component 3 — {num_cities_found}/4 travel essays found in EPUB (0.3 pts)")
            if num_cities_found >= 3:
                total_score += 0.3
        elif num_cities_found >= 2:
            # Partial credit: 2 out of 4 essays present
            print(f"PARTIAL: Component 3 — {num_cities_found}/4 travel essays found in EPUB (0.2 pts)")
            if num_cities_found >= 2:
                total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Only {num_cities_found}/4 travel essays content found in EPUB")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
