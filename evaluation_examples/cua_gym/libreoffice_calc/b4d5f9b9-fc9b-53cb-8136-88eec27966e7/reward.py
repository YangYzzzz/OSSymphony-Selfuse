"""
Reward Script: Save Kubernetes Pod documentation as k8s_pods.docx
Task ID: osworld_multi_apps_web_to_doc_009
Domain: libreoffice_writer (multi_apps)
Scoring:
  Component 1: k8s_pods.docx exists on Desktop                     (gate)
  Component 2: Document starts with 'Pods' as Heading 1            (0.25 pts)
  Component 3: Document has at least 5 expected section headings    (0.35 pts)
  Component 4: Document has substantial content (>=30 paragraphs)  (0.20 pts)
  Component 5: Document does NOT contain 'What's next' section      (0.20 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_009'
FILE_PATH = '/home/user/Desktop/k8s_pods.docx'

# Expected section headings from Kubernetes Pods documentation
EXPECTED_HEADINGS = [
    'Pods',
    'What is a Pod?',
    'Using Pods',
    'Pod update and replacement',
    'Resource sharing and communication',
    'Container probes',
    'Static Pods',
    'Pod lifecycle',
]

# Sections that must NOT appear (content is cut before 'What\'s next')
EXCLUDED_SECTIONS = ["What's next", "Whats next"]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load document {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraph text and style info
    paragraphs = [(p.style.name, p.text.strip()) for p in doc.paragraphs]
    headings = [(style, text) for style, text in paragraphs if 'Heading' in style]
    all_text_lower = ' '.join(text for _, text in paragraphs).lower()

    # Component 1: Document starts with 'Pods' as Heading 1 (0.25 points)
    try:
        # The very first paragraph should be 'Pods' with Heading 1 style
        # Check first 3 headings for Pods Heading 1
        pods_heading_match = next(
            ((style, text) for style, text in headings[:3]
             if text == 'Pods' and 'Heading 1' in style),
            None
        )
        if pods_heading_match is not None:
            print("PASS: Component 1 — Document starts with 'Pods' as Heading 1 (0.25 pts)")
            total_score += 0.25
        else:
            first_heading = headings[0] if headings else ('None', 'None')
            print(f"FAIL: Component 1 — Expected 'Pods' as Heading 1, found: {first_heading}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document contains at least 5 expected section headings (0.35 points)
    try:
        heading_texts = [text for _, text in headings]
        found_headings = [h for h in EXPECTED_HEADINGS if h in heading_texts]
        num_found = len(found_headings)
        # Scale the score: need >= 5 to get full points
        if num_found >= 5:
            print(f"PASS: Component 2 — Found {num_found}/{len(EXPECTED_HEADINGS)} expected headings (0.35 pts)")
            print(f"  Found headings: {found_headings}")
            total_score += 0.35
        elif num_found >= 3:
            partial = 0.20
            print(f"PARTIAL: Component 2 — Found only {num_found}/{len(EXPECTED_HEADINGS)} expected headings ({partial} pts)")
            print(f"  Found headings: {found_headings}")
            print(f"  Missing: {[h for h in EXPECTED_HEADINGS if h not in heading_texts]}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {num_found}/{len(EXPECTED_HEADINGS)} expected headings found")
            print(f"  Missing headings: {[h for h in EXPECTED_HEADINGS if h not in heading_texts]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document has substantial content (at least 30 paragraphs) (0.20 points)
    try:
        non_empty_paragraphs = [text for _, text in paragraphs if text]
        num_paras = len(non_empty_paragraphs)
        # Check for substantial Kubernetes content
        k8s_keywords = ['kubernetes', 'pod', 'container', 'kubelet', 'node']
        k8s_keyword_count = sum(1 for kw in k8s_keywords if kw in all_text_lower)
        if num_paras >= 30 and k8s_keyword_count >= 3:
            print(f"PASS: Component 3 — Document has {num_paras} non-empty paragraphs with K8s content (0.20 pts)")
            total_score += 0.20
        elif num_paras >= 15:
            partial = 0.10
            print(f"PARTIAL: Component 3 — Document has {num_paras} paragraphs but expected >= 30 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Document has too few paragraphs ({num_paras}), expected >= 30")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Document does NOT contain 'What's next' section (0.20 points)
    try:
        # Check that the document was cut off before 'What's next'
        # Check headings for 'what...next' pattern
        whats_next_in_headings = any(
            "what" in text.lower() and "next" in text.lower()
            for _, text in headings
        )
        # Also check in all text
        whats_next_in_body = "what's next" in all_text_lower or "whats next" in all_text_lower

        if not whats_next_in_headings and not whats_next_in_body:
            print("PASS: Component 4 — Document correctly excludes 'What's next' section (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 4 — Document contains 'What's next' section which should have been excluded")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against canonical path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
