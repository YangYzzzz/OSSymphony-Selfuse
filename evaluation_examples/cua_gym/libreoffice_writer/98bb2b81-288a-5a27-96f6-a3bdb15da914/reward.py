"""
Reward Script: Macro-enabled template button in Writer document
Task ID: writer_biz_074
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): ODT file with Basic macro library exists
  Component 2 (0.3): Macro inserts date, time, AND author from document properties
  Component 3 (0.2): A form button/control exists in the document
  Component 4 (0.2): Button is wired to the macro via event listener
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_074'


def find_odt_file():
    """Find the ODT file (macro-enabled format) in the workdir."""
    # Look for the task ODT file first, then any ODT
    candidates = [
        os.path.join(WORKDIR, f'{TASK_ID}.odt'),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # Search for any .odt file
    for f in os.listdir(WORKDIR):
        if f.endswith('.odt') and not f.startswith('.'):
            return os.path.join(WORKDIR, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    odt_path = find_odt_file()
    if not odt_path:
        print(f"CRITICAL: No .odt file found in {WORKDIR}. Macros require ODT format.")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(odt_path, 'r')
        names = zf.namelist()
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file {odt_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ODT file has a Basic macro library (0.3 points)
    # The file must contain Basic/Standard/ with at least one module
    try:
        basic_modules = [n for n in names if n.startswith('Basic/') and n.endswith('.xml')
                         and '/Module' in n]
        script_lb = [n for n in names if 'script-lb.xml' in n]
        script_lc = [n for n in names if 'script-lc.xml' in n]

        if basic_modules and script_lb and script_lc:
            print(f"PASS: Component 1 — Basic macro library found: {basic_modules} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No Basic macro library. "
                  f"Modules: {basic_modules}, script-lb: {script_lb}, script-lc: {script_lc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Macro contains date, time, AND author insertion logic (0.3 points)
    # Read the macro module XML and check the StarBasic code
    try:
        macro_content = ""
        for mod in basic_modules:
            macro_content += zf.read(mod).decode('utf-8', errors='replace')

        macro_lower = macro_content.lower()

        has_date = bool(re.search(r'(now|date|format\s*\(\s*now)', macro_lower))
        has_time = bool(re.search(r'(now|time|hh.*mm|format\s*\(\s*now)', macro_lower))
        has_author = bool(re.search(r'(author|getdocumentproperties|documentproperties)', macro_lower))
        has_insert = bool(re.search(r'(insertstring|inserttext|text\.insert|otext)', macro_lower))

        sub_score = 0.0
        if has_date and has_time:
            sub_score += 0.15
        if has_author:
            sub_score += 0.10
        if has_insert:
            sub_score += 0.05

        if sub_score >= 0.3:
            print(f"PASS: Component 2 — Macro has date({has_date}), time({has_time}), "
                  f"author({has_author}), insert({has_insert}) (0.3 pts)")
            total_score += 0.3
        elif sub_score > 0:
            print(f"PARTIAL: Component 2 — Macro has date({has_date}), time({has_time}), "
                  f"author({has_author}), insert({has_insert}) ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 — Macro missing required functionality. "
                  f"date={has_date}, time={has_time}, author={has_author}, insert={has_insert}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A form button/control exists in the document (0.2 points)
    try:
        content_xml = zf.read('content.xml').decode('utf-8', errors='replace')

        has_form_button = bool(re.search(r'form:button', content_xml))
        has_draw_control = bool(re.search(r'draw:control', content_xml))

        if has_form_button and has_draw_control:
            print(f"PASS: Component 3 — Form button and draw control found (0.2 pts)")
            total_score += 0.2
        elif has_form_button or has_draw_control:
            print(f"PARTIAL: Component 3 — form:button={has_form_button}, "
                  f"draw:control={has_draw_control} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — No form button or draw control in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Button is wired to the macro (0.2 points)
    # Check for event-listener linking to a Basic macro in the document
    try:
        has_event_listener = bool(re.search(r'script:event-listener', content_xml))
        has_macro_link = bool(re.search(
            r'vnd\.sun\.star\.script:.*\?language=Basic.*location=document',
            content_xml
        ))
        # Also accept xlink:href pointing to a macro
        has_xlink_macro = bool(re.search(
            r'xlink:href="vnd\.sun\.star\.script:',
            content_xml
        ))

        if has_event_listener and (has_macro_link or has_xlink_macro):
            print(f"PASS: Component 4 — Button wired to macro via event listener (0.2 pts)")
            total_score += 0.2
        elif has_event_listener:
            print(f"PARTIAL: Component 4 — Event listener found but macro link unclear (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — No event listener wiring button to macro")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
