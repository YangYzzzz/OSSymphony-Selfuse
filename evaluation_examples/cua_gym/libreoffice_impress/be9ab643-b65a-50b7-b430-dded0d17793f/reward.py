"""
Reward Script: Animate horizontal bar chart on slide 3 with Wipe animation
Task ID: impress_ma_089
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Timing/animation exists on slide 3 targeting the chart
  Component 2 (0.25): Animation is Wipe entrance (presetID=22, presetClass=entr)
  Component 3 (0.20): Direction is From Left (presetSubtype=2, wipe(left))
  Component 4 (0.15): 6 individual category animations (by element in category)
  Component 5 (0.15): First bar = clickEffect, subsequent = afterEffect
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_089'

# Namespaces used in OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def get_chart_spid(pptx_path, slide_num=3):
    """Find the shape id of the chart on the specified slide."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_num}.xml') as f:
            root = ET.parse(f).getroot()
    # Look for graphicFrame elements that contain a chart
    sp_tree = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cSld/'
                        '{http://schemas.openxmlformats.org/presentationml/2006/main}spTree')
    if sp_tree is None:
        sp_tree = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}spTree')

    # Search all elements for graphicFrame with chart reference
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'graphicFrame':
            # Check if it contains a chart
            chart_ref = elem.find('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart')
            if chart_ref is None:
                chart_ref = elem.find('.//{http://schemas.openxmlformats.org/drawingml/2006/chartDrawing}chart')
            # Also check for any chart namespace reference
            has_chart = False
            for sub in elem.iter():
                if 'chart' in sub.tag.lower():
                    has_chart = True
                    break
            if has_chart:
                # Get the spid from cNvPr
                for sub in elem.iter():
                    sub_tag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                    if sub_tag == 'cNvPr':
                        return sub.get('id')
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.namelist()  # validate it's a zip
    except Exception as e:
        print(f"CRITICAL: Cannot open as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 3 XML for timing/animation data
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                slide3_xml = f.read().decode('utf-8')
                slide3_root = ET.fromstring(slide3_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide3.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the timing element
    timing = slide3_root.find('.//p:timing', NS)

    # Get chart shape id for reference
    chart_spid = get_chart_spid(file_path, 3)
    print(f"INFO: Chart shape ID on slide 3: {chart_spid}")

    # Collect all cTn elements with presetID (these are the animation nodes)
    anim_nodes = []
    if timing is not None:
        for ctn in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
            preset_id = ctn.get('presetID')
            if preset_id is not None:
                anim_nodes.append(ctn)

    # Collect animEffect elements
    anim_effects = []
    if timing is not None:
        for ae in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}animEffect'):
            anim_effects.append(ae)

    # Collect spTgt elements to check what shape is targeted
    sp_targets = []
    if timing is not None:
        for sptgt in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
            sp_targets.append(sptgt)

    # Check bldLst for chart build info
    bld_graphics = []
    if timing is not None:
        for bg in timing.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}bldGraphic'):
            bld_graphics.append(bg)

    print(f"INFO: Found {len(anim_nodes)} animation nodes, {len(anim_effects)} animEffect elements")
    print(f"INFO: Found {len(sp_targets)} spTgt elements, {len(bld_graphics)} bldGraphic elements")

    # Component 1: Timing/animation exists on slide 3 targeting the chart (0.25 points)
    try:
        has_timing = timing is not None
        has_anim_nodes = len(anim_nodes) > 0

        # Check that at least one animation targets the chart shape
        targets_chart = False
        if chart_spid is not None:
            for sptgt in sp_targets:
                if sptgt.get('spid') == chart_spid:
                    targets_chart = True
                    break

        if has_timing and has_anim_nodes and targets_chart:
            print(f"PASS: Component 1 -- Timing element with animations targeting chart (spid={chart_spid}) found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- timing={has_timing}, anim_nodes={len(anim_nodes)}, targets_chart={targets_chart}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Animation is Wipe entrance (presetID=22, presetClass=entr) (0.25 points)
    try:
        wipe_entrance_count = 0
        for node in anim_nodes:
            pid = node.get('presetID')
            pclass = node.get('presetClass')
            if pid == '22' and pclass == 'entr':
                wipe_entrance_count += 1

        # Also verify animEffect has wipe filter
        wipe_filter_count = 0
        for ae in anim_effects:
            filt = ae.get('filter', '')
            if 'wipe' in filt.lower():
                wipe_filter_count += 1

        if wipe_entrance_count >= 1 and wipe_filter_count >= 1:
            print(f"PASS: Component 2 -- Wipe entrance animation found ({wipe_entrance_count} nodes, {wipe_filter_count} wipe filters) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- wipe_entrance_count={wipe_entrance_count}, wipe_filter_count={wipe_filter_count}")
            # List what presetIDs and classes were found
            for node in anim_nodes:
                print(f"  Found: presetID={node.get('presetID')}, presetClass={node.get('presetClass')}, presetSubtype={node.get('presetSubtype')}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Direction is From Left (presetSubtype=2, wipe(left)) (0.20 points)
    try:
        from_left_count = 0
        for node in anim_nodes:
            if node.get('presetSubtype') == '2':
                from_left_count += 1

        wipe_left_count = 0
        for ae in anim_effects:
            filt = ae.get('filter', '')
            if 'wipe(left)' in filt.lower():
                wipe_left_count += 1

        if from_left_count >= 1 and wipe_left_count >= 1:
            print(f"PASS: Component 3 -- From Left direction confirmed ({from_left_count} subtype=2, {wipe_left_count} wipe(left)) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- from_left_count={from_left_count}, wipe_left_count={wipe_left_count}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 6 individual category animations (by element in category) (0.15 points)
    try:
        # Check graphicEl references with bldStep="ptInCat" and distinct categoryIdx values
        category_indices = set()
        for sptgt in sp_targets:
            for gel in sptgt.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}chart'):
                bld_step = gel.get('bldStep')
                cat_idx = gel.get('categoryIdx')
                if bld_step == 'ptInCat' and cat_idx is not None:
                    category_indices.add(cat_idx)

        num_categories = len(category_indices)

        # Also check bldGraphic exists for the chart
        has_bld_graphic = len(bld_graphics) > 0

        if num_categories >= 6 and has_bld_graphic:
            print(f"PASS: Component 4 -- {num_categories} individual category animations (indices: {sorted(category_indices)}) with bldGraphic (0.15 pts)")
            total_score += 0.15
        elif num_categories >= 4:
            partial = 0.15 * (num_categories / 6)
            print(f"PARTIAL: Component 4 -- {num_categories}/6 categories animated ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Only {num_categories} category animations found (need 6), bldGraphic={has_bld_graphic}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: First bar = clickEffect, subsequent = afterEffect (0.15 points)
    try:
        node_types = []
        for node in anim_nodes:
            nt = node.get('nodeType')
            if nt in ('clickEffect', 'afterEffect'):
                node_types.append(nt)

        first_is_click = len(node_types) > 0 and node_types[0] == 'clickEffect'
        subsequent_after = all(nt == 'afterEffect' for nt in node_types[1:]) if len(node_types) > 1 else False

        if first_is_click and subsequent_after and len(node_types) >= 2:
            print(f"PASS: Component 5 -- Trigger sequence correct: first=clickEffect, {len(node_types)-1} afterEffect (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- node_types={node_types}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
persist_app_state()
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
