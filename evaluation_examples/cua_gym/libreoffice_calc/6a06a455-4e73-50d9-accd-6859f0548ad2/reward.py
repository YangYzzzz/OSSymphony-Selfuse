"""
Reward Script: Verify that exactly 3 sheets (Executive Summary, Financial Results, KPIs)
are tab-selected for printing, and no other sheets are selected.
Task ID: calc_gsi_093
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Exactly 3 sheets have tabSelected="1"
  Component 2 (0.3): The selected sheets match the target set
  Component 3 (0.3): No non-target sheets are selected (compound with target match)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_093'

TARGET_SHEETS = {'Executive Summary', 'Financial Results', 'KPIs'}

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def get_sheet_tab_selection(file_path):
    """
    Parse the xlsx to determine which sheets have tabSelected="1".
    Returns a dict: {sheet_name: bool} for all sheets.
    """
    zf = zipfile.ZipFile(file_path, 'r')

    # 1. Get ordered sheet names and their rIds from workbook.xml
    wb_xml = ET.fromstring(zf.read('xl/workbook.xml'))
    sheets_els = wb_xml.findall(f'.//{{{NS}}}sheet')
    sheet_info = []
    for s in sheets_els:
        name = s.attrib['name']
        rid = s.attrib[f'{{{REL_NS}}}id']
        sheet_info.append((name, rid))

    # 2. Map rIds to file targets via workbook.xml.rels
    rels_xml = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
    rid_to_target = {}
    for rel in rels_xml.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        rid_to_target[rel.attrib['Id']] = rel.attrib['Target']

    # 3. Check tabSelected in each sheet's XML
    result = {}
    for name, rid in sheet_info:
        target = rid_to_target.get(rid, '')
        # Handle both absolute (/xl/worksheets/...) and relative (worksheets/...) paths
        if target.startswith('/'):
            sheet_path = target.lstrip('/')
        else:
            sheet_path = f'xl/{target}'
        try:
            sheet_xml = ET.fromstring(zf.read(sheet_path))
            views = sheet_xml.findall(f'.//{{{NS}}}sheetView')
            tab_selected = False
            for v in views:
                if v.attrib.get('tabSelected', '0') == '1':
                    tab_selected = True
                    break
            result[name] = tab_selected
        except Exception as e:
            print(f"  WARN: Could not parse {sheet_path}: {e}")
            result[name] = False

    zf.close()
    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        selection = get_sheet_tab_selection(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Sheet tab-selection state: {selection}")

    selected_sheets = {name for name, sel in selection.items() if sel}
    non_selected_sheets = {name for name, sel in selection.items() if not sel}

    print(f"Selected sheets: {selected_sheets}")
    print(f"Non-selected sheets: {non_selected_sheets}")

    # Component 1: Exactly 3 sheets have tabSelected (0.4 points)
    try:
        num_selected = len(selected_sheets)
        if num_selected == 3:
            print(f"PASS: Component 1 — exactly 3 sheets are tab-selected (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 3 tab-selected sheets, found {num_selected}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The selected sheets match the target set exactly (0.3 points)
    try:
        if selected_sheets == TARGET_SHEETS:
            print(f"PASS: Component 2 — selected sheets match target set exactly (0.3 pts)")
            total_score += 0.3
        else:
            missing = TARGET_SHEETS - selected_sheets
            extra = selected_sheets - TARGET_SHEETS
            if missing:
                print(f"FAIL: Component 2 — missing from selection: {missing}")
            if extra:
                print(f"FAIL: Component 2 — extra in selection: {extra}")
            # Partial credit: if at least some target sheets are selected
            matched = TARGET_SHEETS & selected_sheets
            if len(matched) > 0 and len(matched) < 3:
                partial = round(0.3 * len(matched) / 3, 2)
                print(f"PARTIAL: Component 2 — {len(matched)}/3 target sheets selected (+{partial} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No non-target sheets are selected AND all targets are selected (compound) (0.3 points)
    try:
        non_target_selected = selected_sheets - TARGET_SHEETS
        all_targets_selected = TARGET_SHEETS.issubset(selected_sheets)
        if all_targets_selected and len(non_target_selected) == 0:
            print(f"PASS: Component 3 — all targets selected, no non-targets selected (0.3 pts)")
            total_score += 0.3
        elif all_targets_selected and len(non_target_selected) > 0:
            print(f"FAIL: Component 3 — all targets selected but {len(non_target_selected)} non-target sheets also selected: {non_target_selected}")
        elif not all_targets_selected:
            print(f"FAIL: Component 3 — not all target sheets are selected")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
