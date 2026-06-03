"""
Reward Script: Layered PDF with Optional Content Groups (OCG)
Task ID: pdf_aw_046
Domain: pdf
Scoring:
  Component 1 (0.15): PDF file exists at /home/user/design/floor_plan.pdf
                       AND has exactly 1 page (precondition gate combined with change check)
  Component 2 (0.25): Exactly 3 OCGs exist with correct names: Walls, Electrical, Plumbing
  Component 3 (0.20): OCG visibility defaults correct: Walls=on, Electrical=on, Plumbing=off
  Component 4 (0.20): Walls layer contains black rectangles (color 0,0,0 with rect items)
  Component 5 (0.10): Electrical layer contains yellow lines (color 1,1,0 with line items)
  Component 6 (0.10): Plumbing layer contains blue lines (color 0,0,1 with line items)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_046'
FILE_PATH = os.path.join(WORKDIR, 'design', 'floor_plan.pdf')


def parse_content_streams(doc, page):
    """Parse raw content streams to extract per-OCG drawing info.

    In PDF content streams, the pattern within an OC block is:
      /OC /MCx BDC  -- begin OC block
      <path ops>    -- re (rect), m (moveto), l (lineto)
      <color> RG S  -- set color and stroke (or B for fill+stroke)
      EMC           -- end OC block

    So we collect shape types per block, then assign color when we see RG.

    Returns dict: mc_name -> list of dicts with 'stroke' and 'type'
    """
    import re as _re
    contents = page.get_contents()
    layers = {}  # mc_name -> [{'stroke': (r,g,b), 'type': 'rect'|'line'}, ...]

    for c_xref in contents:
        data = doc.xref_stream(c_xref)
        if not data:
            continue
        text = data.decode('latin-1', errors='replace')

        current_oc = None
        block_shapes = []  # shape types in current OC block
        block_color = None

        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Detect OCG marker: /OC /MCx BDC
            if line.startswith('/OC /') and 'BDC' in line:
                parts = line.split()
                if len(parts) >= 2:
                    current_oc = parts[1].lstrip('/')
                block_shapes = []
                block_color = None
                continue

            # End marker: flush block
            if line == 'EMC':
                if current_oc and block_shapes:
                    if current_oc not in layers:
                        layers[current_oc] = []
                    for stype in block_shapes:
                        layers[current_oc].append({
                            'stroke': block_color,
                            'type': stype,
                        })
                current_oc = None
                block_shapes = []
                block_color = None
                continue

            if current_oc is None:
                continue

            # Parse stroke color: "R G B RG" anywhere in line
            rg_match = _re.search(r'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+RG', line)
            if rg_match:
                try:
                    r = float(rg_match.group(1))
                    g = float(rg_match.group(2))
                    b = float(rg_match.group(3))
                    block_color = (r, g, b)
                except ValueError:
                    pass

            # Detect rectangle path: "x y w h re"
            if _re.search(r'[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+re', line):
                block_shapes.append('rect')

            # Detect lineto path: "x y l"
            if _re.search(r'[\d.]+\s+[\d.]+\s+l\b', line):
                block_shapes.append('line')

    return layers


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print("CRITICAL: File not found: %s" % file_path)
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print("CRITICAL: Cannot open PDF %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF exists with exactly 1 page (0.15 points)
    # The file existence alone is not scored — combined with page count check
    try:
        page_count = doc.page_count
        if page_count == 1:
            print("PASS: Component 1 — PDF has 1 page (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 — expected 1 page, found %d" % page_count)
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: Exactly 3 OCGs with correct names (0.25 points)
    try:
        ocgs = doc.get_ocgs()
        ocg_names = set()
        for xref, info in ocgs.items():
            ocg_names.add(info.get('name', ''))

        required_names = {'Walls', 'Electrical', 'Plumbing'}
        if len(ocgs) == 3 and ocg_names == required_names:
            print("PASS: Component 2 — 3 OCGs found: %s (0.25 pts)" % sorted(ocg_names))
            total_score += 0.25
        else:
            print("FAIL: Component 2 — expected OCGs %s, found %d OCGs: %s" % (
                sorted(required_names), len(ocgs), sorted(ocg_names)))
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: OCG visibility defaults (0.20 points)
    # Walls=on, Electrical=on, Plumbing=off
    try:
        ocgs = doc.get_ocgs()
        expected_vis = {'Walls': True, 'Electrical': True, 'Plumbing': False}

        name_to_on = {}
        for xref, info in ocgs.items():
            name_to_on[info.get('name', '')] = info.get('on', None)

        mismatch_count = 0
        for name, expected_on in expected_vis.items():
            actual_on = name_to_on.get(name)
            if actual_on != expected_on:
                mismatch_count += 1
                print("FAIL: Component 3 — OCG '%s' visibility: expected %s, got %s" % (
                    name, expected_on, actual_on))

        if mismatch_count == 0 and len(name_to_on) >= 3:
            print("PASS: Component 3 — OCG visibility correct: Walls=on, Electrical=on, Plumbing=off (0.20 pts)")
            total_score += 0.20
        elif mismatch_count > 0:
            pass  # already printed FAIL above
        else:
            print("FAIL: Component 3 — insufficient OCGs to check visibility")
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # Components 4-6: Verify content per layer via raw content stream parsing
    # We need to map MC names to OCG names
    try:
        page = doc[0]
        page_xref = page.xref

        # Build MC -> OCG name mapping from page resources
        mc_to_name = {}
        props_str = doc.xref_get_key(page_xref, 'Resources/Properties')
        if props_str[0] == 'dict':
            # Parse the properties dict to get MC -> xref mapping
            ocgs = doc.get_ocgs()
            xref_to_name = {xref: info.get('name', '') for xref, info in ocgs.items()}

            # Try each MCn
            for i in range(10):
                mc_name = 'MC%d' % i
                try:
                    val = doc.xref_get_key(page_xref, 'Resources/Properties/%s' % mc_name)
                    if val[0] == 'xref':
                        # val[1] is like '5 0 R'
                        ref_xref = int(val[1].split()[0])
                        if ref_xref in xref_to_name:
                            mc_to_name[mc_name] = xref_to_name[ref_xref]
                except:
                    pass

        print("INFO: MC-to-OCG mapping: %s" % mc_to_name)

        # Parse content streams
        layer_data = parse_content_streams(doc, page)
        print("INFO: Layer data keys: %s" % list(layer_data.keys()))

        # Map MC names to OCG names in layer_data
        named_layers = {}
        for mc_name, items in layer_data.items():
            ocg_name = mc_to_name.get(mc_name, mc_name)
            named_layers[ocg_name] = items

        for name, items in named_layers.items():
            types = [it['type'] for it in items]
            colors = [it['stroke'] for it in items if it['stroke'] is not None]
            print("INFO: Layer '%s': %d items, types=%s, colors=%s" % (
                name, len(items), set(types), set(colors)))

    except Exception as e:
        print("ERROR: Could not parse content streams: %s" % e)
        named_layers = {}

    # Component 4: Walls layer has black rectangles (0.20 points)
    try:
        walls_items = named_layers.get('Walls', [])
        has_rects = any(it['type'] == 'rect' for it in walls_items)
        has_black = any(
            it['stroke'] is not None and
            abs(it['stroke'][0]) < 0.1 and abs(it['stroke'][1]) < 0.1 and abs(it['stroke'][2]) < 0.1
            for it in walls_items
        )

        if has_rects and has_black:
            rect_count = sum(1 for it in walls_items if it['type'] == 'rect')
            print("PASS: Component 4 — Walls layer has %d black rectangles (0.20 pts)" % rect_count)
            total_score += 0.20
        else:
            print("FAIL: Component 4 — Walls layer: has_rects=%s, has_black=%s (items=%d)" % (
                has_rects, has_black, len(walls_items)))
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    # Component 5: Electrical layer has yellow lines (0.10 points)
    try:
        elec_items = named_layers.get('Electrical', [])
        has_lines = any(it['type'] == 'line' for it in elec_items)
        has_yellow = any(
            it['stroke'] is not None and
            abs(it['stroke'][0] - 1.0) < 0.1 and abs(it['stroke'][1] - 1.0) < 0.1 and abs(it['stroke'][2]) < 0.1
            for it in elec_items
        )

        if has_lines and has_yellow:
            line_count = sum(1 for it in elec_items if it['type'] == 'line')
            print("PASS: Component 5 — Electrical layer has %d yellow lines (0.10 pts)" % line_count)
            total_score += 0.10
        else:
            print("FAIL: Component 5 — Electrical layer: has_lines=%s, has_yellow=%s (items=%d)" % (
                has_lines, has_yellow, len(elec_items)))
    except Exception as e:
        print("ERROR: Component 5 — %s" % e)

    # Component 6: Plumbing layer has blue lines (0.10 points)
    try:
        plumb_items = named_layers.get('Plumbing', [])
        has_lines = any(it['type'] == 'line' for it in plumb_items)
        has_blue = any(
            it['stroke'] is not None and
            abs(it['stroke'][0]) < 0.1 and abs(it['stroke'][1]) < 0.1 and abs(it['stroke'][2] - 1.0) < 0.1
            for it in plumb_items
        )

        if has_lines and has_blue:
            line_count = sum(1 for it in plumb_items if it['type'] == 'line')
            print("PASS: Component 6 — Plumbing layer has %d blue lines (0.10 pts)" % line_count)
            total_score += 0.10
        else:
            print("FAIL: Component 6 — Plumbing layer: has_lines=%s, has_blue=%s (items=%d)" % (
                has_lines, has_blue, len(plumb_items)))
    except Exception as e:
        print("ERROR: Component 6 — %s" % e)

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print()
    print("Score: %s/1.0" % final_score)
    print("REWARD: %s" % final_score)
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print("File not found: %s" % FILE_PATH)
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
