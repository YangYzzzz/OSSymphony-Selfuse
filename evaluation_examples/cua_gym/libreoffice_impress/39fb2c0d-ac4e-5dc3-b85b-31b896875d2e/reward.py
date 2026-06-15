"""
Reward Script: Slide reveal animation on slide 8 — 'page turn' story effect
Task ID: impress_gf2_044
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35) — WhiteOverlay has exit animation moving right (fly out to right)
  Component 2 (0.15) — WhiteOverlay exit animation duration ~1.2s and triggered on click
  Component 3 (0.35) — NarrationBox has fade entrance animation
  Component 4 (0.15) — NarrationBox animation triggered after previous with delay
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_044'

# Namespaces used in OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def get_shape_id_by_name(slide_xml_content, name):
    """Find the spid for a shape by its name in the slide XML."""
    pattern = r'cNvPr id="(\d+)" name="' + re.escape(name) + r'"'
    m = re.search(pattern, slide_xml_content)
    if m:
        return m.group(1)
    return None


def parse_timing_xml(pptx_path, slide_number):
    """Extract the timing (animation) XML element from a specific slide."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_path = f'ppt/slides/slide{slide_number}.xml'
        try:
            with zf.open(slide_path) as f:
                content = f.read().decode()
                root = ET.fromstring(content)
                timing = root.find('.//p:timing', NS)
                return timing, content
        except KeyError:
            return None, None


def find_anim_nodes_for_spid(timing_el, spid):
    """Find all animation nodes targeting a specific shape id."""
    results = []
    if timing_el is None:
        return results
    # Find all elements that have spTgt with matching spid
    for spTgt in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
        if spTgt.get('spid') == spid:
            # Walk up to the parent behavior container
            results.append(spTgt)
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    timing_el, slide_content = parse_timing_xml(file_path, 8)

    if timing_el is None:
        print("FAIL: No timing/animation XML found on slide 8")
        print("REWARD: 0.0")
        return 0.0

    timing_xml = ET.tostring(timing_el, encoding='unicode')

    # Get shape IDs
    overlay_spid = get_shape_id_by_name(slide_content, 'WhiteOverlay')
    narration_spid = get_shape_id_by_name(slide_content, 'NarrationBox')

    if not overlay_spid:
        print("FAIL: Could not find WhiteOverlay shape on slide 8")
        print("REWARD: 0.0")
        return 0.0

    if not narration_spid:
        print("FAIL: Could not find NarrationBox shape on slide 8")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: WhiteOverlay spid={overlay_spid}, NarrationBox spid={narration_spid}")

    # Component 1: WhiteOverlay has exit animation moving right (0.35 points)
    # The animation should move ppt_x from current position to off-screen right
    try:
        has_exit_right = False
        # Look for <anim> targeting the overlay that moves ppt_x to the right
        for anim_el in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}anim'):
            # Check if this anim targets the WhiteOverlay
            tgtEl = anim_el.find('.//p:spTgt', NS)
            if tgtEl is not None and tgtEl.get('spid') == overlay_spid:
                # Check the attribute being animated
                attrName = anim_el.find('.//p:attrName', NS)
                if attrName is not None and 'ppt_x' in (attrName.text or ''):
                    # Check the value list for rightward movement
                    tavs = anim_el.findall('.//p:tav', NS)
                    for tav in tavs:
                        val = tav.find('.//p:strVal', NS)
                        if val is not None:
                            v = val.get('val', '')
                            # Exit right: end value should move to right (1+#ppt_w/2 or similar positive offset)
                            if '1+' in v or 'ppt_w' in v:
                                has_exit_right = True

        if has_exit_right:
            print(f"PASS: Component 1 — WhiteOverlay has exit animation moving right (0.35 pts)")
            total_score += 0.35
        else:
            # Also check for animEffect with fly-out pattern or animMotion
            # Some implementations use animEffect transition="out" filter="wipe" dir="r"
            has_alt_exit = False
            for anim_effect in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}animEffect'):
                tgtEl = anim_effect.find('.//p:spTgt', NS)
                if tgtEl is not None and tgtEl.get('spid') == overlay_spid:
                    transition = anim_effect.get('transition', '')
                    filter_val = anim_effect.get('filter', '')
                    if transition == 'out':
                        has_alt_exit = True

            if has_alt_exit:
                print(f"PASS: Component 1 — WhiteOverlay has exit animation effect (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — WhiteOverlay missing exit-right animation")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: WhiteOverlay animation duration ~1200ms and triggered on click (0.15 points)
    try:
        overlay_duration_ok = False
        overlay_on_click = False

        # Check duration: look for anim or cTn with dur targeting overlay
        for anim_el in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}anim'):
            tgtEl = anim_el.find('.//p:spTgt', NS)
            if tgtEl is not None and tgtEl.get('spid') == overlay_spid:
                dur_attr = anim_el.get('dur')
                if dur_attr:
                    try:
                        dur_val = int(dur_attr)
                        # Accept duration in range 800-1600ms (centered on 1200)
                        if 800 <= dur_val <= 1600:
                            overlay_duration_ok = True
                    except ValueError:
                        pass

        # Check on-click trigger: the main sequence should have onClick condition
        # The seq element with nextCondLst containing onClick is the trigger
        for seq in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}seq'):
            nextCondLst = seq.find('p:nextCondLst', NS)
            if nextCondLst is not None:
                for cond in nextCondLst.findall('p:cond', NS):
                    if cond.get('evt') == 'onClick':
                        overlay_on_click = True

        if overlay_duration_ok and overlay_on_click:
            print(f"PASS: Component 2 — WhiteOverlay duration ~1.2s and on-click trigger (0.15 pts)")
            total_score += 0.15
        elif overlay_duration_ok:
            print(f"PARTIAL: Component 2 — Duration OK but on-click trigger not confirmed (0.075 pts)")
            total_score += 0.075
        elif overlay_on_click:
            print(f"PARTIAL: Component 2 — On-click trigger OK but duration not matched (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 2 — duration_ok={overlay_duration_ok}, on_click={overlay_on_click}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: NarrationBox has fade entrance animation (0.35 points)
    try:
        has_fade_entrance = False

        # Look for animEffect with transition="in" filter="fade" targeting narration box
        for anim_effect in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}animEffect'):
            tgtEl = anim_effect.find('.//p:spTgt', NS)
            if tgtEl is not None and tgtEl.get('spid') == narration_spid:
                transition = anim_effect.get('transition', '')
                filter_val = anim_effect.get('filter', '')
                if transition == 'in' and 'fade' in filter_val.lower():
                    has_fade_entrance = True

        if has_fade_entrance:
            print(f"PASS: Component 3 — NarrationBox has fade entrance animation (0.35 pts)")
            total_score += 0.35
        else:
            # Check for set visibility=visible which is part of entrance
            has_visibility_set = False
            for set_el in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}set'):
                tgtEl = set_el.find('.//p:spTgt', NS)
                if tgtEl is not None and tgtEl.get('spid') == narration_spid:
                    attrName = set_el.find('.//p:attrName', NS)
                    to_el = set_el.find('.//p:strVal', NS)
                    if (attrName is not None and 'visibility' in (attrName.text or '') and
                            to_el is not None and to_el.get('val') == 'visible'):
                        has_visibility_set = True

            if has_visibility_set:
                # Partial: has visibility entrance but not specifically fade
                print(f"PARTIAL: Component 3 — NarrationBox has entrance but not specifically fade (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — NarrationBox missing fade entrance animation")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: NarrationBox animation triggered after previous (after WhiteOverlay) with delay (0.15 points)
    try:
        narration_after_prev = False

        # The narration animation should be in a separate <par> with a delay matching
        # or exceeding the overlay duration (indicating "after previous")
        # In OOXML, "after previous" means the narration's parent <par> has
        # stCondLst with a delay equal to the overlay animation duration
        for par_el in timing_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}par'):
            # Check if this par contains the narration box animation
            has_narration = False
            for spTgt in par_el.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
                if spTgt.get('spid') == narration_spid:
                    has_narration = True
                    break

            if has_narration:
                # Check for delay in stCondLst
                cTn = par_el.find('p:cTn', NS)
                if cTn is not None:
                    stCondLst = cTn.find('p:stCondLst', NS)
                    if stCondLst is not None:
                        for cond in stCondLst.findall('p:cond', NS):
                            delay = cond.get('delay', '0')
                            try:
                                delay_val = int(delay)
                                # Should have a positive delay (after previous animation)
                                if delay_val > 0:
                                    narration_after_prev = True
                                    print(f"  INFO: NarrationBox animation delay={delay_val}ms")
                            except ValueError:
                                pass

        if narration_after_prev:
            print(f"PASS: Component 4 — NarrationBox triggered after previous with delay (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — NarrationBox not properly sequenced after WhiteOverlay")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice
def persist_app_state(domain):
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
