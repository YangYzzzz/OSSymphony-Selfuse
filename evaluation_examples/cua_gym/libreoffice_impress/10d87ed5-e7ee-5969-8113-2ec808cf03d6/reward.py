"""
Reward Script: Animation sequence on slide 1
Task ID: impress_ma_086
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.20): Timing/animation element exists on slide 1
  - Component 2 (0.25): Acme Corp text has Fly In from Top entrance, On Click trigger
  - Component 3 (0.25): Innovation Redefined has Fade entrance, After Previous, 0.5s delay
  - Component 4 (0.20): Logo has Bounce entrance, After Previous, 0.5s delay
  - Component 5 (0.10): Correct animation sequence order (CompanyName -> Tagline -> Logo)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_086'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def get_shape_name_map(slide_xml_root):
    """Map shape id -> shape name from slide XML."""
    shape_map = {}
    # sp elements
    for sp in slide_xml_root.findall('.//p:cSld/p:spTree/p:sp', NS):
        cNvPr = sp.find('.//p:nvSpPr/p:cNvPr', NS)
        if cNvPr is not None:
            sid = cNvPr.get('id')
            name = cNvPr.get('name', '')
            shape_map[sid] = name
    # pic elements
    for pic in slide_xml_root.findall('.//p:cSld/p:spTree/p:pic', NS):
        cNvPr = pic.find('.//p:nvPicPr/p:cNvPr', NS)
        if cNvPr is not None:
            sid = cNvPr.get('id')
            name = cNvPr.get('name', '')
            shape_map[sid] = name
    return shape_map


def parse_animations(slide_xml_root):
    """
    Parse animation entries from the timing tree.
    Returns list of dicts with: spid, presetID, presetClass, presetSubtype, nodeType, delay_ms
    in sequence order.
    """
    animations = []
    timing = slide_xml_root.find('.//p:timing', NS)
    if timing is None:
        return animations

    # The main sequence is at: timing > tnLst > par > cTn > childTnLst > seq > cTn > childTnLst
    # Each top-level <p:par> inside that childTnLst is one animation step
    main_seq_ctn = timing.find(
        './/p:tnLst/p:par/p:cTn/p:childTnLst/p:seq/p:cTn', NS
    )
    if main_seq_ctn is None:
        return animations

    child_list = main_seq_ctn.find('p:childTnLst', NS)
    if child_list is None:
        return animations

    for top_par in child_list.findall('p:par', NS):
        # Drill down to the innermost p:cTn that has presetID
        # Structure: par > cTn > childTnLst > par > cTn > childTnLst > par > cTn(presetID)
        anim_ctn = None
        for ctn in top_par.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cTn'):
            if ctn.get('presetID') is not None:
                anim_ctn = ctn
                break

        if anim_ctn is None:
            continue

        preset_id = anim_ctn.get('presetID')
        preset_class = anim_ctn.get('presetClass')
        preset_subtype = anim_ctn.get('presetSubtype', '0')
        node_type = anim_ctn.get('nodeType', '')

        # Get target shape id
        spid = None
        tgt_el = anim_ctn.find('.//p:tgtEl/p:spTgt', NS)
        if tgt_el is not None:
            spid = tgt_el.get('spid')
        else:
            # Search in child behaviors
            for sp_tgt in anim_ctn.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}spTgt'):
                spid = sp_tgt.get('spid')
                break

        # Get delay from the parent cTn's stCondLst
        # The delay is on the intermediate par's cTn, not the presetID cTn
        delay_ms = 0
        # Navigate: top_par > cTn > childTnLst > par > cTn (this one has the delay)
        outer_ctn = top_par.find('p:cTn', NS)
        if outer_ctn is not None:
            inner_child = outer_ctn.find('p:childTnLst', NS)
            if inner_child is not None:
                inner_par = inner_child.find('p:par', NS)
                if inner_par is not None:
                    inner_ctn = inner_par.find('p:cTn', NS)
                    if inner_ctn is not None:
                        st_cond = inner_ctn.find('.//p:stCondLst/p:cond', NS)
                        if st_cond is not None:
                            delay_val = st_cond.get('delay', '0')
                            try:
                                delay_ms = int(delay_val)
                            except ValueError:
                                delay_ms = 0

        animations.append({
            'spid': spid,
            'presetID': preset_id,
            'presetClass': preset_class,
            'presetSubtype': preset_subtype,
            'nodeType': node_type,
            'delay_ms': delay_ms,
        })

    return animations


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load slide1 XML from pptx zip
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide1.xml') as f:
                slide_root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load slide1 XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    shape_map = get_shape_name_map(slide_root)
    print(f"INFO: Shape map: {shape_map}")

    animations = parse_animations(slide_root)
    print(f"INFO: Found {len(animations)} animations")
    for i, a in enumerate(animations):
        shape_name = shape_map.get(a['spid'], 'unknown')
        print(f"  Anim {i+1}: spid={a['spid']}({shape_name}), presetID={a['presetID']}, "
              f"class={a['presetClass']}, subtype={a['presetSubtype']}, "
              f"nodeType={a['nodeType']}, delay={a['delay_ms']}ms")

    # Component 1: Timing/animation element exists on slide 1 (0.20 points)
    # Must have at least 3 entrance animations
    try:
        timing_el = slide_root.find('.//p:timing', NS)
        if timing_el is not None and len(animations) >= 3:
            entrance_anims = [a for a in animations if a['presetClass'] == 'entr']
            if len(entrance_anims) >= 3:
                print(f"PASS: Component 1 - Found {len(entrance_anims)} entrance animations on slide 1 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 - Found {len(entrance_anims)} entrance animations, need >= 3")
        else:
            if timing_el is None:
                print("FAIL: Component 1 - No timing element found on slide 1")
            else:
                print(f"FAIL: Component 1 - Only {len(animations)} animations, need >= 3")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Build lookup by shape name for easier checking
    anim_by_shape = {}
    for a in animations:
        shape_name = shape_map.get(a['spid'], '')
        anim_by_shape[shape_name] = a

    # Component 2: Acme Corp (CompanyName) has Fly In from Top entrance, On Click (0.25 points)
    # presetID=2 (Fly In), presetClass=entr, presetSubtype=4 (from top), nodeType=clickEffect
    try:
        company_anim = anim_by_shape.get('CompanyName')
        if company_anim is None:
            # Try finding by spid targeting shape with "Acme Corp" text
            for a in animations:
                sname = shape_map.get(a['spid'], '')
                if 'company' in sname.lower() or 'acme' in sname.lower():
                    company_anim = a
                    break

        if company_anim is None:
            print("FAIL: Component 2 - No animation found for CompanyName/Acme Corp shape")
        else:
            checks_passed = 0
            max_checks = 3

            # Check entrance class
            if company_anim['presetClass'] == 'entr':
                checks_passed += 1
            else:
                print(f"  DETAIL: CompanyName presetClass={company_anim['presetClass']}, expected 'entr'")

            # Check Fly In (presetID=2) with from-top direction (subtype=4)
            if company_anim['presetID'] == '2':
                checks_passed += 1
            else:
                print(f"  DETAIL: CompanyName presetID={company_anim['presetID']}, expected '2' (Fly In)")

            # Check On Click trigger
            if company_anim['nodeType'] == 'clickEffect':
                checks_passed += 1
            else:
                print(f"  DETAIL: CompanyName nodeType={company_anim['nodeType']}, expected 'clickEffect'")

            if checks_passed == max_checks:
                print(f"PASS: Component 2 - CompanyName has Fly In entrance, On Click trigger (0.25 pts)")
                total_score += 0.25
            elif checks_passed >= 2:
                partial = 0.15
                print(f"PARTIAL: Component 2 - CompanyName {checks_passed}/{max_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 - CompanyName only {checks_passed}/{max_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Innovation Redefined (Tagline) has Fade entrance, After Previous, 0.5s delay (0.25 points)
    # presetID=10 (Fade), presetClass=entr, nodeType=afterEffect, delay=500ms
    try:
        tagline_anim = anim_by_shape.get('Tagline')
        if tagline_anim is None:
            for a in animations:
                sname = shape_map.get(a['spid'], '')
                if 'tagline' in sname.lower() or 'innovation' in sname.lower():
                    tagline_anim = a
                    break

        if tagline_anim is None:
            print("FAIL: Component 3 - No animation found for Tagline/Innovation Redefined shape")
        else:
            checks_passed = 0
            max_checks = 3

            # Check Fade entrance (presetID=10, class=entr)
            if tagline_anim['presetClass'] == 'entr' and tagline_anim['presetID'] == '10':
                checks_passed += 1
            else:
                print(f"  DETAIL: Tagline presetID={tagline_anim['presetID']} (expected 10), class={tagline_anim['presetClass']}")

            # Check After Previous trigger
            if tagline_anim['nodeType'] == 'afterEffect':
                checks_passed += 1
            else:
                print(f"  DETAIL: Tagline nodeType={tagline_anim['nodeType']}, expected 'afterEffect'")

            # Check 0.5s delay (500ms)
            if tagline_anim['delay_ms'] == 500:
                checks_passed += 1
            else:
                print(f"  DETAIL: Tagline delay={tagline_anim['delay_ms']}ms, expected 500ms")

            if checks_passed == max_checks:
                print(f"PASS: Component 3 - Tagline has Fade entrance, After Previous, 0.5s delay (0.25 pts)")
                total_score += 0.25
            elif checks_passed >= 2:
                partial = 0.15
                print(f"PARTIAL: Component 3 - Tagline {checks_passed}/{max_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 - Tagline only {checks_passed}/{max_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Logo has Bounce entrance, After Previous, 0.5s delay (0.20 points)
    # presetID=26 (Bounce), presetClass=entr, nodeType=afterEffect, delay=500ms
    try:
        logo_anim = anim_by_shape.get('Logo')
        if logo_anim is None:
            for a in animations:
                sname = shape_map.get(a['spid'], '')
                if 'logo' in sname.lower():
                    logo_anim = a
                    break

        if logo_anim is None:
            print("FAIL: Component 4 - No animation found for Logo shape")
        else:
            checks_passed = 0
            max_checks = 3

            # Check Bounce entrance (presetID=26, class=entr)
            if logo_anim['presetClass'] == 'entr' and logo_anim['presetID'] == '26':
                checks_passed += 1
            else:
                print(f"  DETAIL: Logo presetID={logo_anim['presetID']} (expected 26), class={logo_anim['presetClass']}")

            # Check After Previous trigger
            if logo_anim['nodeType'] == 'afterEffect':
                checks_passed += 1
            else:
                print(f"  DETAIL: Logo nodeType={logo_anim['nodeType']}, expected 'afterEffect'")

            # Check 0.5s delay (500ms)
            if logo_anim['delay_ms'] == 500:
                checks_passed += 1
            else:
                print(f"  DETAIL: Logo delay={logo_anim['delay_ms']}ms, expected 500ms")

            if checks_passed == max_checks:
                print(f"PASS: Component 4 - Logo has Bounce entrance, After Previous, 0.5s delay (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 2:
                partial = 0.12
                print(f"PARTIAL: Component 4 - Logo {checks_passed}/{max_checks} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 - Logo only {checks_passed}/{max_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Correct sequence order - CompanyName first, Tagline second, Logo third (0.10 points)
    try:
        if len(animations) >= 3:
            anim_order = []
            for a in animations[:3]:
                sname = shape_map.get(a['spid'], 'unknown')
                anim_order.append(sname)

            expected_order_names = ['CompanyName', 'Tagline', 'Logo']
            if anim_order == expected_order_names:
                print(f"PASS: Component 5 - Animation order is correct: {anim_order} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - Animation order is {anim_order}, expected {expected_order_names}")
        else:
            print(f"FAIL: Component 5 - Not enough animations ({len(animations)}) to check order")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
