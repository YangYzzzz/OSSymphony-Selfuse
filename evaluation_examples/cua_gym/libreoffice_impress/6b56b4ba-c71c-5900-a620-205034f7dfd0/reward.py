"""
Reward Script: Configure print settings for handouts in LibreOffice Impress
Task ID: impress_el_014
Domain: libreoffice_impress
Scoring:
  Component 1: Content type set to Handouts (Content=2)         — 0.20 points
  Component 2: SlidesPerHandout set to 6                        — 0.20 points
  Component 3: PageOrientation set to Landscape (1)             — 0.20 points
  Component 4: Date printing enabled (Date=true)                — 0.20 points
  Component 5: Page number printing enabled (PageName=true)     — 0.20 points
"""

import os
import re

CONFIG_PATH = '/home/user/.config/libreoffice/4/user/registrymodifications.xcu'
TASK_ID = 'impress_el_014'


def parse_impress_print_settings(config_path):
    """
    Parse LibreOffice registrymodifications.xcu for Impress Print settings.
    Returns a dict of setting_name -> value (as string).
    """
    settings = {}
    if not os.path.exists(config_path):
        return settings

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match lines like:
    # <item oor:path="/org.openoffice.Office.Impress/Print"><prop oor:name="Content" ...><value>2</value></prop></item>
    pattern = r'<item\s+oor:path="/org\.openoffice\.Office\.Impress/Print">\s*<prop\s+oor:name="([^"]+)"[^>]*>\s*<value>([^<]*)</value>'
    for match in re.finditer(pattern, content):
        name = match.group(1)
        value = match.group(2)
        settings[name] = value

    return settings


def verify_task():
    """
    Verify that LibreOffice Impress print settings are configured for:
    - Handouts (Content=2)
    - 6 slides per page (SlidesPerHandout=6)
    - Landscape orientation (PageOrientation=1)
    - Date printing enabled (Date=true)
    - Page number printing enabled (PageName=true)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings from registrymodifications.xcu
    try:
        settings = parse_impress_print_settings(CONFIG_PATH)
        print(f"INFO: Found {len(settings)} Impress Print settings")
        for k, v in settings.items():
            print(f"  {k} = {v}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse config file {CONFIG_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Content type is Handouts (Content=2) — 0.20 points
    try:
        content_val = settings.get('Content', None)
        if content_val is not None and str(content_val).strip() == '2':
            print(f"PASS: Component 1 — Content type is Handouts (Content={content_val}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected Content=2 (Handouts), found: {content_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SlidesPerHandout is 6 — 0.20 points
    try:
        slides_per = settings.get('SlidesPerHandout', None)
        if slides_per is not None and str(slides_per).strip() == '6':
            print(f"PASS: Component 2 — SlidesPerHandout={slides_per} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected SlidesPerHandout=6, found: {slides_per}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PageOrientation is Landscape (1) — 0.20 points
    try:
        orientation = settings.get('PageOrientation', None)
        if orientation is not None and str(orientation).strip() == '1':
            print(f"PASS: Component 3 — PageOrientation=Landscape ({orientation}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected PageOrientation=1 (Landscape), found: {orientation}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Date printing enabled (Date=true) — 0.20 points
    try:
        date_val = settings.get('Date', None)
        if date_val is not None and str(date_val).strip().lower() == 'true':
            print(f"PASS: Component 4 — Date printing enabled (Date={date_val}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected Date=true, found: {date_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page number printing enabled (PageName=true) — 0.20 points
    try:
        pagename_val = settings.get('PageName', None)
        if pagename_val is not None and str(pagename_val).strip().lower() == 'true':
            print(f"PASS: Component 5 — Page number printing enabled (PageName={pagename_val}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Expected PageName=true, found: {pagename_val}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
