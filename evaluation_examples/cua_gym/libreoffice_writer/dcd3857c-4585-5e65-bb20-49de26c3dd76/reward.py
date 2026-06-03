"""
Reward Script: Convert master document to single regular Writer document
Task ID: writer_rm_079
Domain: libreoffice_writer
Scoring:
  Component 1: File is regular ODT (not master .odm) — 0.15
  Component 2: No linked sections (subdocument links removed) — 0.20
  Component 3: No placeholder text remaining — 0.15
  Component 4: Chapter 1 content embedded — 0.125
  Component 5: Chapter 2 content embedded — 0.125
  Component 6: Chapter 3 content embedded — 0.125
  Component 7: Chapter 4 content embedded — 0.125
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_079'


def extract_all_text(doc):
    """Extract all text from an ODF document."""
    from odf.text import P
    all_text = []
    for p in doc.getElementsByType(P):
        t = ''
        for node in p.childNodes:
            if hasattr(node, 'data'):
                t += node.data
            elif hasattr(node, 'childNodes'):
                for c in node.childNodes:
                    if hasattr(c, 'data'):
                        t += c.data
        all_text.append(t)
    return all_text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P, Section
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is regular ODT with correct mimetype (0.15 points)
    # A master document has mimetype 'application/vnd.oasis.opendocument.text-master'
    # A regular document has mimetype 'application/vnd.oasis.opendocument.text'
    try:
        mimetype = doc.getMediaType()
        if mimetype == 'application/vnd.oasis.opendocument.text':
            print(f"PASS: Component 1 — File is regular ODT (mimetype: {mimetype}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected regular ODT mimetype, found: {mimetype}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No linked sections / subdocument links (0.20 points)
    # The original master document had 4 linked sections referencing subdocuments.
    # The converted document should have NO linked sections.
    try:
        sections = doc.getElementsByType(Section)
        # Check for sections that have link attributes (xlink:href)
        linked_sections = 0
        for s in sections:
            attrs = s.attributes
            # Check if any attribute contains xlink or href (subdoc link)
            for key, val in attrs.items():
                if 'href' in str(key).lower() or 'link' in str(key).lower():
                    linked_sections += 1
                    break

        if len(sections) == 0:
            print(f"PASS: Component 2 — No sections found, no subdocument links (0.20 pts)")
            total_score += 0.20
        elif linked_sections == 0:
            # Sections exist but none are linked — acceptable
            print(f"PASS: Component 2 — {len(sections)} sections but none are linked (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Found {linked_sections} linked sections (subdoc links remain)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Extract all text for content checks
    try:
        all_text = extract_all_text(doc)
        full_text = ' '.join(all_text)
        non_empty = [t for t in all_text if t.strip()]
    except Exception as e:
        print(f"ERROR: Cannot extract text: {e}")
        full_text = ''
        non_empty = []

    # Component 3: No placeholder text remaining (0.15 points)
    # The master doc had placeholders like "[Content from Chapter1_Introduction.odt]"
    try:
        has_placeholder = '[Content from' in full_text
        if not has_placeholder:
            print(f"PASS: Component 3 — No placeholder text found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Placeholder text still present in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Components 4-7: Chapter content embedded (0.125 each)
    # Each chapter has distinctive signature text that must be present
    chapter_checks = [
        (4, "Chapter 1 (Introduction)", "rapid advancement of quantum computing poses an unprecedented threat", 0.125),
        (5, "Chapter 2 (Lattice-Based)", "CRYSTALS-Kyber Key Encapsulation Mechanism", 0.125),
        (6, "Chapter 3 (Alternative Approaches)", "SPHINCS+ Stateless Hash-Based Signatures", 0.125),
        (7, "Chapter 4 (Recommendations)", "Transitioning to quantum-resistant cryptography requires careful planning", 0.125),
    ]

    for comp_num, label, signature, points in chapter_checks:
        try:
            if signature in full_text:
                print(f"PASS: Component {comp_num} — {label} content found ('{signature[:50]}...') ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component {comp_num} — {label} content NOT found (missing: '{signature[:50]}...')")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
