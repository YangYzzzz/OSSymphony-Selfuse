"""
Reward Script: Create a 'List Number' style numbered list for six installation steps
Task ID: writer_bs_056
Domain: libreoffice_writer
Scoring:
  Component 1: All 6 paragraphs under 'Installation Procedure' use 'List Number' style (0.30)
  Component 2: All 6 paragraphs have numbering (numPr with numId) (0.30)
  Component 3: Numbering format is 'Step %1.' (0.25)
  Component 4: Left indent is approximately 2.0cm (~720000 EMU) (0.15)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_056'


def persist_app_state(domain: str):
    """Best-effort save any unsaved GUI state."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_installation_paragraphs(doc):
    """Find the 6 paragraphs between 'Installation Procedure' and the next heading."""
    paras = doc.paragraphs
    start_idx = None
    end_idx = None

    for i, p in enumerate(paras):
        if 'Installation Procedure' in p.text and p.style.name.startswith('Heading'):
            start_idx = i + 1
            continue
        if start_idx is not None and p.style.name.startswith('Heading'):
            end_idx = i
            break

    if start_idx is None:
        return []

    if end_idx is None:
        end_idx = len(paras)

    return paras[start_idx:end_idx]


def get_numbering_format(doc, num_id):
    """Look up the lvlText for a given numId at ilvl=0."""
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    try:
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return None
        numbering_xml = numbering_part._element

        # Find abstractNumId for this numId
        abstract_num_id = None
        for num in numbering_xml.findall(".//{" + ns + "}num"):
            if num.get("{" + ns + "}numId") == str(num_id):
                abs_ref = num.find("{" + ns + "}abstractNumId")
                if abs_ref is not None:
                    abstract_num_id = abs_ref.get("{" + ns + "}val")
                break

        if abstract_num_id is None:
            return None

        # Find the abstractNum and get lvlText for ilvl=0
        for abs_num in numbering_xml.findall(".//{" + ns + "}abstractNum"):
            if abs_num.get("{" + ns + "}abstractNumId") == abstract_num_id:
                for lvl in abs_num.findall("{" + ns + "}lvl"):
                    if lvl.get("{" + ns + "}ilvl") == "0":
                        lvl_text_el = lvl.find("{" + ns + "}lvlText")
                        if lvl_text_el is not None:
                            return lvl_text_el.get("{" + ns + "}val")
        return None
    except Exception:
        return None


def get_num_id(para):
    """Extract the numId from a paragraph's numPr element, or None."""
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    num_pr_list = para._element.findall(".//{" + ns + "}numPr")
    if not num_pr_list:
        return None
    for num_pr in num_pr_list:
        num_id_el = num_pr.find("{" + ns + "}numId")
        if num_id_el is not None:
            val = num_id_el.get("{" + ns + "}val")
            if val and val != "0":
                return val
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the 6 installation procedure paragraphs
    install_paras = get_installation_paragraphs(doc)
    if len(install_paras) < 6:
        print(f"CRITICAL: Expected 6 installation paragraphs, found {len(install_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Use only the first 6
    install_paras = install_paras[:6]
    print(f"INFO: Found {len(install_paras)} installation paragraphs")

    # Component 1: All 6 paragraphs use 'List Number' style variant (0.30 points)
    try:
        list_number_count = 0
        for p in install_paras:
            style_name = p.style.name if p.style else ""
            if "List Number" in style_name:
                list_number_count += 1
        if list_number_count == 6:
            print(f"PASS: Component 1 -- All 6 paragraphs use 'List Number' style (0.30 pts)")
            total_score += 0.30
        elif list_number_count > 0:
            partial = 0.30 * (list_number_count / 6)
            print(f"PARTIAL: Component 1 -- {list_number_count}/6 paragraphs use 'List Number' style ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No paragraphs use 'List Number' style")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 6 paragraphs have numbering (numPr with valid numId) (0.30 points)
    try:
        numbered_count = 0
        num_ids_found = []
        for p in install_paras:
            nid = get_num_id(p)
            if nid is not None:
                numbered_count += 1
                num_ids_found.append(nid)
        if numbered_count == 6:
            print(f"PASS: Component 2 -- All 6 paragraphs have numbering (numIds: {num_ids_found}) (0.30 pts)")
            total_score += 0.30
        elif numbered_count > 0:
            partial = 0.30 * (numbered_count / 6)
            print(f"PARTIAL: Component 2 -- {numbered_count}/6 paragraphs have numbering ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No paragraphs have numbering")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Numbering format is 'Step %1.' (0.25 points)
    try:
        if num_ids_found:
            # Check the first numbered paragraph's format
            lvl_text = get_numbering_format(doc, num_ids_found[0])
            if lvl_text is not None and "Step" in lvl_text and "%1" in lvl_text:
                print(f"PASS: Component 3 -- Numbering format is '{lvl_text}' (0.25 pts)")
                total_score += 0.25
            elif lvl_text is not None:
                print(f"FAIL: Component 3 -- Numbering format is '{lvl_text}', expected 'Step %1.'")
            else:
                print(f"FAIL: Component 3 -- Could not determine numbering format")
        else:
            print(f"FAIL: Component 3 -- No numbered paragraphs to check format")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Left indent approximately 2.0cm (~720000 EMU, tolerance +/- 100000) (0.15 points)
    try:
        indent_ok_count = 0
        for p in install_paras:
            left_indent = p.paragraph_format.left_indent
            if left_indent is not None and abs(left_indent - 720000) < 200000:
                indent_ok_count += 1
        if indent_ok_count == 6:
            print(f"PASS: Component 4 -- All 6 paragraphs have ~2.0cm left indent (0.15 pts)")
            total_score += 0.15
        elif indent_ok_count > 0:
            partial = 0.15 * (indent_ok_count / 6)
            print(f"PARTIAL: Component 4 -- {indent_ok_count}/6 paragraphs have correct indent ({partial:.2f} pts)")
            total_score += partial
        else:
            indent_vals = [p.paragraph_format.left_indent for p in install_paras]
            print(f"FAIL: Component 4 -- Paragraphs do not have ~2.0cm indent (values: {indent_vals})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
