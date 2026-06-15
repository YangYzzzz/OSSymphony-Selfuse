"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps sprinkling lonely single lines at the top or bottom of pages in my novel draft. How can I apply widow control = 2 lines and orphan control = 2 lines to every paragraph that’s in the Body Text style, all in one shot?
Generated: 2025-09-10 12:39:15
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
import lxml.etree as ET


def verify_widow_orphan_control(docx_path: str) -> float:
    """Verify that every paragraph in the DOCX having the Body Text style
    (styleId="BodyText" or name "Body Text") is configured with widow control = 2
    and orphan control = 2 lines.  Progressive scoring:
      • 0.4 points  – Body Text style itself defines widow=2 & orphan=2
      • 0-0.6 points – Proportion of Body-Text paragraphs inheriting / overriding
                        these settings (ratio * 0.6)
      • Total score capped at 1.0
    Returns the score and prints a detailed breakdown.
    """

    print(f"Verifying widow/orphan control in: {docx_path}")
    score = 0.0

    if not os.path.exists(docx_path):
        print("✗ File not found")
        return 0.0

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    try:
        with zipfile.ZipFile(docx_path) as z:
            # ---------- 1. STYLE-LEVEL CHECK ---------- #
            styles_root = ET.fromstring(z.read("word/styles.xml"))

            # Collect possible Body Text styleIds
            style_ids = set()
            for elem in styles_root.xpath("//w:style[@w:type='paragraph']", namespaces=ns):
                sid = elem.get(f"{{{ns['w']}}}styleId")
                name_el = elem.find(".//w:name", namespaces=ns)
                name_val = name_el.get(f"{{{ns['w']}}}val") if name_el is not None else ""
                if sid in {"BodyText", "Body Text"} or name_val == "Body Text":
                    style_ids.add(sid)

            # Fallback to common id if nothing detected
            if not style_ids:
                style_ids = {"BodyText"}
            print(f"Detected Body Text style IDs: {style_ids}")

            def _extract_widow_orphan(style_elem):
                ppr = style_elem.find(".//w:pPr", namespaces=ns)
                if ppr is None:
                    return None, None
                widow_el = ppr.find(".//w:widow", namespaces=ns)
                orphan_el = ppr.find(".//w:orphans", namespaces=ns)
                widow_val = (widow_el.get(f"{{{ns['w']}}}val") if widow_el is not None else None)
                orphan_val = (orphan_el.get(f"{{{ns['w']}}}val") if orphan_el is not None else None)
                return widow_val, orphan_val

            style_widow = style_orphan = None
            for sid in style_ids:
                match = styles_root.xpath(
                    f"//w:style[@w:type='paragraph'][@w:styleId='{sid}']",
                    namespaces=ns,
                )
                if match:
                    style_widow, style_orphan = _extract_widow_orphan(match[0])
                    break

            # If still None, try matching by name “Body Text”
            if style_widow is None or style_orphan is None:
                match = styles_root.xpath(
                    "//w:style[@w:type='paragraph'][w:name/@w:val='Body Text']",
                    namespaces=ns,
                )
                if match:
                    style_widow, style_orphan = _extract_widow_orphan(match[0])

            style_correct = style_widow == "2" and style_orphan == "2"
            if style_correct:
                score += 0.4
                print("✓ Body Text style defines widow=2 and orphan=2 (0.4 points)")
            else:
                print("✗ Body Text style does not correctly define widow/orphan settings")

            # ---------- 2. PARAGRAPH-LEVEL CHECK ---------- #
            doc_root = ET.fromstring(z.read("word/document.xml"))
            body_paras = doc_root.xpath("//w:p[w:pPr/w:pStyle]", namespaces=ns)

            total_body = 0
            correct_body = 0
            for p in body_paras:
                p_style = p.find(".//w:pPr/w:pStyle", namespaces=ns)
                sid = (
                    p_style.get(f"{{{ns['w']}}}val") if p_style is not None else ""
                )
                if sid in style_ids or sid in {"BodyText", "Body Text"}:
                    total_body += 1
                    ppr = p.find(".//w:pPr", namespaces=ns)
                    widow_el = ppr.find(".//w:widow", namespaces=ns) if ppr is not None else None
                    orphan_el = ppr.find(".//w:orphans", namespaces=ns) if ppr is not None else None
                    # Inherit from style when paragraph-level val missing
                    widow_val = (
                        widow_el.get(f"{{{ns['w']}}}val")
                        if widow_el is not None
                        else style_widow
                    )
                    orphan_val = (
                        orphan_el.get(f"{{{ns['w']}}}val")
                        if orphan_el is not None
                        else style_orphan
                    )
                    if widow_val == "2" and orphan_val == "2":
                        correct_body += 1

            if total_body == 0:
                print("✗ No paragraphs with Body Text style found")
            else:
                ratio = correct_body / total_body
                para_score = 0.6 * ratio  # up to 0.6 pts
                score += para_score
                print(
                    f"Body Text paragraphs: {correct_body}/{total_body} \
                        correct – (+{para_score:.2f} points)"
                )

            final_score = min(round(score, 3), 1.0)
            print(f"Total Score: {final_score}")
            return final_score

    except Exception as e:
        print("✗ Error during verification:", e)
        return 0.0


# ----------------- MAIN -----------------
if __name__ == "__main__":
    DOCX_FILE = (
        "/home/user/libreoffice_keeps_sprinkling_lonely_single_lines_at_the_top_or_bottom_of_pages_in_my_novel_draft_how.docx"
    )
    reward = verify_widow_orphan_control(DOCX_FILE)
    print(f"REWARD: {reward}")

