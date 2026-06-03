"""
Reward Script: Resolve broken hyperlinks in reading_list.odt
Task ID: osworld_multi_apps_web_references_009
Domain: libreoffice_writer (ODT file with hyperlinks)
Scoring:
  - Component 1: Broken URL ref 3 (AlexNet/NeurIPS) replaced with valid URL  — 0.30
  - Component 2: Broken URL ref 5 (XGBoost) replaced with valid URL           — 0.30
  - Component 3: Broken URL ref 7 (AdaGrad/JMLR) replaced with valid URL      — 0.30
  - Component 4: Summary/fix note appended to document                        — 0.10
  Total: 1.00
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_web_references_009'
FILE_PATH = f'{WORKDIR}/reading_list.odt'

# Known broken URLs in the initial_env (these must NOT appear in golden_env)
BROKEN_URLS = [
    'https://papers.nips.cc/paper/2012/hash/wrong-url.html',
    'https://dl.acm.org/doi/invalid/10.1145/wrong',
    'https://jmlr.org/papers/volume12/gone.html',
]

# Known working URLs that should remain unchanged
WORKING_URLS_UNCHANGED = [
    'https://arxiv.org/abs/1706.03762',
    'https://arxiv.org/abs/2001.08361',
    'https://openreview.net/forum?id=HJzdEWY7',
    'https://aclanthology.org/N19-1423',
    'https://arxiv.org/abs/2103.00020',
]

# Expected valid replacement patterns for the 3 broken URLs
# We check that broken URLs are replaced with something valid (not the original broken URL)
# and also validate against the known correct replacement URLs
EXPECTED_REPLACEMENTS = {
    # ref 3: AlexNet NeurIPS paper — should point to papers.nips.cc with correct hash
    'ref3': {
        'broken': 'https://papers.nips.cc/paper/2012/hash/wrong-url.html',
        'expected_domain': 'papers.nips.cc',
        'expected_contains': 'c399862d3b9d6b76c8436e924a68c45b',
    },
    # ref 5: XGBoost ACM paper
    'ref5': {
        'broken': 'https://dl.acm.org/doi/invalid/10.1145/wrong',
        'expected_domain': 'dl.acm.org',
        'expected_contains': '2939672.2939785',
    },
    # ref 7: AdaGrad JMLR paper
    'ref7': {
        'broken': 'https://jmlr.org/papers/volume12/gone.html',
        'expected_domain': 'jmlr.org',
        'expected_contains': 'duchi',
    },
}


def extract_hrefs_from_odt(file_path):
    """Extract all hyperlink hrefs from an ODT file using lxml."""
    with zipfile.ZipFile(file_path) as zf:
        with zf.open('content.xml') as f:
            content = f.read()
    root = etree.fromstring(content)
    hrefs = []
    for a in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}a'):
        href = a.get('{http://www.w3.org/1999/xlink}href', '')
        all_text = ''.join(a.itertext())
        hrefs.append({'href': href, 'text': all_text})
    return hrefs


def extract_all_text_from_odt(file_path):
    """Extract all paragraph text from an ODT file using lxml."""
    with zipfile.ZipFile(file_path) as zf:
        with zf.open('content.xml') as f:
            content = f.read()
    root = etree.fromstring(content)
    paragraphs = []
    for p in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
        t = ''.join(p.itertext()).strip()
        if t:
            paragraphs.append(t)
    return paragraphs


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be parseable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        hrefs = extract_hrefs_from_odt(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    href_values = [h['href'] for h in hrefs]
    print(f"Found {len(hrefs)} hyperlinks in document:")
    for h in hrefs:
        print(f"  href={h['href']!r}")

    # Component 1: Broken URL ref 3 (AlexNet/NeurIPS) replaced (0.30 points)
    # The broken URL 'https://papers.nips.cc/paper/2012/hash/wrong-url.html' must be gone,
    # replaced with a valid NeurIPS URL containing the correct paper hash.
    try:
        broken_3 = EXPECTED_REPLACEMENTS['ref3']['broken']
        still_broken_3 = broken_3 in href_values
        if still_broken_3:
            print(f"FAIL: Component 1 — Broken AlexNet URL still present: {broken_3}")
        else:
            # Check if the replacement contains the expected paper hash or valid nips.cc URL
            nips_replacements = [h for h in href_values
                                 if 'papers.nips.cc' in h and h != broken_3]
            if nips_replacements:
                replacement = nips_replacements[0]
                expected_contains = EXPECTED_REPLACEMENTS['ref3']['expected_contains']
                if expected_contains in replacement:
                    print(f"PASS: Component 1 — AlexNet URL correctly replaced with: {replacement} (0.30 pts)")
                    total_score += 0.30
                else:
                    # Accept any non-broken nips.cc URL as partial success
                    # (agent may have found a slightly different valid URL)
                    print(f"PASS: Component 1 — AlexNet URL replaced (nips.cc URL found): {replacement} (0.30 pts)")
                    total_score += 0.30
            else:
                # Check if broken URL removed even if no nips.cc replacement (e.g., arxiv version)
                print(f"FAIL: Component 1 — Broken AlexNet URL removed but no valid replacement URL found among hrefs")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Broken URL ref 5 (XGBoost) replaced (0.30 points)
    # The broken URL 'https://dl.acm.org/doi/invalid/10.1145/wrong' must be gone,
    # replaced with a valid ACM DOI URL.
    try:
        broken_5 = EXPECTED_REPLACEMENTS['ref5']['broken']
        still_broken_5 = broken_5 in href_values
        if still_broken_5:
            print(f"FAIL: Component 2 — Broken XGBoost URL still present: {broken_5}")
        else:
            acm_replacements = [h for h in href_values
                                if 'dl.acm.org' in h and h != broken_5 and 'invalid' not in h]
            if acm_replacements:
                replacement = acm_replacements[0]
                expected_contains = EXPECTED_REPLACEMENTS['ref5']['expected_contains']
                if expected_contains in replacement:
                    print(f"PASS: Component 2 — XGBoost URL correctly replaced with: {replacement} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"PASS: Component 2 — XGBoost URL replaced (valid acm.org URL found): {replacement} (0.30 pts)")
                    total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Broken XGBoost URL removed but no valid ACM replacement found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Broken URL ref 7 (AdaGrad/JMLR) replaced (0.30 points)
    # The broken URL 'https://jmlr.org/papers/volume12/gone.html' must be gone,
    # replaced with the correct JMLR paper URL.
    try:
        broken_7 = EXPECTED_REPLACEMENTS['ref7']['broken']
        still_broken_7 = broken_7 in href_values
        if still_broken_7:
            print(f"FAIL: Component 3 — Broken AdaGrad JMLR URL still present: {broken_7}")
        else:
            jmlr_replacements = [h for h in href_values
                                 if 'jmlr.org' in h and h != broken_7 and 'gone.html' not in h]
            if jmlr_replacements:
                replacement = jmlr_replacements[0]
                expected_contains = EXPECTED_REPLACEMENTS['ref7']['expected_contains']
                if expected_contains in replacement:
                    print(f"PASS: Component 3 — AdaGrad JMLR URL correctly replaced with: {replacement} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"PASS: Component 3 — AdaGrad JMLR URL replaced (valid jmlr.org URL found): {replacement} (0.30 pts)")
                    total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Broken AdaGrad URL removed but no valid JMLR replacement found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Summary note appended to document (0.10 points)
    # Task requires adding a note listing which URLs were fixed.
    try:
        paragraphs = extract_all_text_from_odt(file_path)
        full_text = ' '.join(paragraphs).lower()
        # Check for a note mentioning broken/fixed/replaced URLs near the end
        has_fix_note = (
            ('broken' in full_text or 'fixed' in full_text or 'replaced' in full_text)
            and ('url' in full_text or 'link' in full_text or 'http' in full_text)
        )
        if has_fix_note:
            print(f"PASS: Component 4 — Summary note about fixed URLs found in document (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No summary note about fixed URLs found in document")
            print(f"      Last paragraph: {paragraphs[-1][:100] if paragraphs else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Verify that working URLs were not accidentally changed
    try:
        for url in WORKING_URLS_UNCHANGED:
            if url not in href_values:
                print(f"WARN: Expected working URL no longer present: {url}")
    except Exception as e:
        print(f"WARN: Could not verify unchanged URLs: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
