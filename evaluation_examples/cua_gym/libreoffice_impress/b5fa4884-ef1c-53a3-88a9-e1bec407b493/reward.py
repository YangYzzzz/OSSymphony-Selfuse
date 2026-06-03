"""
Reward Script: Apply Fade entrance animation to bulleted list on slide 2
Task ID: impress_ma_053
Domain: libreoffice_impress
Scoring:
  Component 1 (0.2): Timing/animation element exists on slide 2
  Component 2 (0.3): Animation type is Fade entrance (presetID=10, presetClass=entr, filter=fade)
  Component 3 (0.3): All 5 bullet paragraphs animated separately (paragraph ranges 0-4)
  Component 4 (0.2): Animations target the content placeholder and are click-triggered
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_053'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_content_placeholder_spid(root):
    """Find the shape ID of the content placeholder on slide 2."""
    for sp in root.findall(f'.//{{{P_NS}}}sp'):
        nvSpPr = sp.find(f'{{{P_NS}}}nvSpPr')
        if nvSpPr is not None:
            cNvPr = nvSpPr.find(f'{{{P_NS}}}cNvPr')
            if cNvPr is not None:
                name = cNvPr.get('name', '')
                if 'Content' in name or 'content' in name:
                    return cNvPr.get('id')
    return None


def verify_task(file_path):
    """
    Verify that slide 2 has a Fade entrance animation applied to the
    bulleted list with each bullet appearing one at a time on click.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load slide 2 XML from the pptx zip
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        slide2_xml = zf.open('ppt/slides/slide2.xml').read()
        root = ET.fromstring(slide2_xml)
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load slide2 XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify the content placeholder spid
    content_spid = get_content_placeholder_spid(root)
    print(f"INFO: Content placeholder spid = {content_spid}")

    # Component 1: Timing/animation element exists on slide 2 (0.2 points)
    try:
        timing = root.find(f'.//{{{P_NS}}}timing')
        if timing is not None:
            # Check there is at least one animation node
            cTns = timing.findall(f'.//{{{P_NS}}}cTn[@presetID]')
            if len(cTns) > 0:
                print(f"PASS: Component 1 — Timing element with {len(cTns)} animation node(s) found on slide 2 (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 1 — Timing element exists but no animation nodes with presetID")
        else:
            print("FAIL: Component 1 — No timing element found on slide 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Animation type is Fade entrance (0.3 points)
    try:
        timing = root.find(f'.//{{{P_NS}}}timing')
        if timing is None:
            print("FAIL: Component 2 — No timing element")
        else:
            cTns = timing.findall(f'.//{{{P_NS}}}cTn[@presetID]')
            fade_entrance_count = 0
            for ctn in cTns:
                pid = ctn.get('presetID')
                pcls = ctn.get('presetClass')
                if pid == '10' and pcls == 'entr':
                    fade_entrance_count += 1

            # Also verify the animEffect filter is 'fade'
            animEffects = timing.findall(f'.//{{{P_NS}}}animEffect')
            fade_filter_count = sum(
                1 for ae in animEffects
                if ae.get('filter') == 'fade' and ae.get('transition') == 'in'
            )

            if fade_entrance_count >= 1 and fade_filter_count >= 1:
                # Partial: at least some fade entrance animations exist
                if fade_entrance_count >= 5 and fade_filter_count >= 5:
                    print(f"PASS: Component 2 — {fade_entrance_count} Fade entrance animations with fade filter (0.3 pts)")
                    total_score += 0.3
                else:
                    partial = 0.15
                    print(f"PARTIAL: Component 2 — {fade_entrance_count} Fade entrance, {fade_filter_count} fade filters (expected 5 each) ({partial} pts)")
                    total_score += partial
            else:
                print(f"FAIL: Component 2 — Found {fade_entrance_count} Fade entrance, {fade_filter_count} fade filters (expected >= 1 each)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 bullet paragraphs animated separately (0.3 points)
    try:
        timing = root.find(f'.//{{{P_NS}}}timing')
        if timing is None:
            print("FAIL: Component 3 — No timing element")
        else:
            # Find all paragraph range targets within the timing element
            pRgs = timing.findall(f'.//{{{P_NS}}}pRg')
            # Each paragraph should have at least one pRg targeting it
            # The animEffect and set elements each have their own pRg, so we expect pairs
            targeted_paragraphs = set()
            for prg in pRgs:
                st = prg.get('st')
                end = prg.get('end')
                if st == end:  # Individual paragraph targeting
                    targeted_paragraphs.add(int(st))

            expected_paragraphs = {0, 1, 2, 3, 4}
            if targeted_paragraphs >= expected_paragraphs:
                print(f"PASS: Component 3 — All 5 paragraphs (0-4) targeted individually (0.3 pts)")
                total_score += 0.3
            elif len(targeted_paragraphs) > 0:
                # Partial credit based on how many paragraphs are targeted
                covered = len(targeted_paragraphs & expected_paragraphs)
                partial = round(0.3 * covered / 5, 2)
                print(f"PARTIAL: Component 3 — {covered}/5 paragraphs targeted: {sorted(targeted_paragraphs)} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No individual paragraph targets found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Animations target the content placeholder and are click-triggered (0.2 points)
    try:
        timing = root.find(f'.//{{{P_NS}}}timing')
        if timing is None:
            print("FAIL: Component 4 — No timing element")
        else:
            # Check spTgt targets
            spTgts = timing.findall(f'.//{{{P_NS}}}spTgt')
            target_spids = set(sp.get('spid') for sp in spTgts)

            # Check that animations target the content placeholder
            targets_content = False
            if content_spid and content_spid in target_spids:
                targets_content = True
            elif len(target_spids) == 1:
                # If we couldn't find content_spid but there's only one target,
                # it's likely the content placeholder
                targets_content = True

            # Check for click-triggered (nodeType=clickEffect)
            cTns = timing.findall(f'.//{{{P_NS}}}cTn[@presetID]')
            click_effects = sum(1 for ctn in cTns if ctn.get('nodeType') == 'clickEffect')

            if targets_content and click_effects >= 5:
                print(f"PASS: Component 4 — Animations target content placeholder (spid={content_spid or target_spids}) with {click_effects} click effects (0.2 pts)")
                total_score += 0.2
            elif targets_content and click_effects >= 1:
                partial = 0.1
                print(f"PARTIAL: Component 4 — Targets content placeholder but only {click_effects} click effects (expected 5) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — targets_content={targets_content}, click_effects={click_effects}, target_spids={target_spids}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
