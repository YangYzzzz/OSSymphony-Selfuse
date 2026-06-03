"""
Reward Script: Demote 'Database Setup' and 'API Configuration' from level 1 to level 2 under 'Backend Development'
Task ID: writer_lec_014
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): 'Database Setup' paragraph has ilvl=1
  Component 2 (0.4): 'API Configuration' paragraph has ilvl=1
  Component 3 (0.2): Both demoted items appear immediately after 'Backend Development' and before 'Testing'
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_014'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_ilvl(para):
    """Extract the outline/numbering level (ilvl) from a paragraph's XML. Returns int or None."""
    ilvl_els = para._element.findall(f'.//{{{WNS}}}ilvl')
    if ilvl_els:
        val = ilvl_els[0].get(f'{{{WNS}}}val')
        if val is not None:
            return int(val)
    return None


def get_numId(para):
    """Extract the numbering ID from a paragraph's XML. Returns str or None."""
    numId_els = para._element.findall(f'.//{{{WNS}}}numId')
    if numId_els:
        return numId_els[0].get(f'{{{WNS}}}val')
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a list of numbered paragraphs (those participating in the outline list)
    numbered_paras = []
    for para in doc.paragraphs:
        numId = get_numId(para)
        if numId is not None and numId != '0':
            ilvl = get_ilvl(para)
            numbered_paras.append({
                'text': para.text.strip(),
                'ilvl': ilvl,
                'numId': numId,
            })

    print(f"INFO: Found {len(numbered_paras)} numbered paragraphs:")
    for np in numbered_paras:
        print(f"  - text={repr(np['text'])}, ilvl={np['ilvl']}, numId={np['numId']}")

    # Component 1: 'Database Setup' is at ilvl=1 (0.4 points)
    try:
        db_setup = [p for p in numbered_paras if p['text'] == 'Database Setup']
        if db_setup:
            if db_setup[0]['ilvl'] == 1:
                print(f"PASS: Component 1 -- 'Database Setup' is at ilvl=1 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 -- 'Database Setup' ilvl={db_setup[0]['ilvl']}, expected 1")
        else:
            print(f"FAIL: Component 1 -- 'Database Setup' paragraph not found in numbered list")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'API Configuration' is at ilvl=1 (0.4 points)
    try:
        api_config = [p for p in numbered_paras if p['text'] == 'API Configuration']
        if api_config:
            if api_config[0]['ilvl'] == 1:
                print(f"PASS: Component 2 -- 'API Configuration' is at ilvl=1 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- 'API Configuration' ilvl={api_config[0]['ilvl']}, expected 1")
        else:
            print(f"FAIL: Component 2 -- 'API Configuration' paragraph not found in numbered list")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct ordering — Backend Development (ilvl=0) immediately followed by
    # Database Setup (ilvl=1) then API Configuration (ilvl=1), then Testing (ilvl=0) (0.2 points)
    try:
        texts = [p['text'] for p in numbered_paras]
        ilvls = [p['ilvl'] for p in numbered_paras]

        # Find indices
        bd_idx = texts.index('Backend Development') if 'Backend Development' in texts else None
        ds_idx = texts.index('Database Setup') if 'Database Setup' in texts else None
        ac_idx = texts.index('API Configuration') if 'API Configuration' in texts else None
        t_idx = texts.index('Testing') if 'Testing' in texts else None

        if bd_idx is not None and ds_idx is not None and ac_idx is not None and t_idx is not None:
            # Database Setup and API Configuration should be right after Backend Development
            # and before Testing
            order_ok = (ds_idx == bd_idx + 1 and ac_idx == bd_idx + 2 and t_idx == bd_idx + 3)
            # Backend Development should still be at ilvl=0
            bd_level_ok = (ilvls[bd_idx] == 0)
            # Testing should still be at ilvl=0
            t_level_ok = (ilvls[t_idx] == 0)
            # The sub-items must be at ilvl=1 (this ensures the check fails on initial_env)
            ds_level_ok = (ilvls[ds_idx] == 1)
            ac_level_ok = (ilvls[ac_idx] == 1)

            if order_ok and bd_level_ok and t_level_ok and ds_level_ok and ac_level_ok:
                print(f"PASS: Component 3 -- Correct ordering: BD(0)->DS(1)->AC(1)->Testing(0) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- Ordering issues: order_ok={order_ok}, bd_level={ilvls[bd_idx]}, ds_level={ilvls[ds_idx]}, ac_level={ilvls[ac_idx]}, t_level={ilvls[t_idx]}")
        else:
            print(f"FAIL: Component 3 -- Missing required paragraphs. Indices: BD={bd_idx}, DS={ds_idx}, AC={ac_idx}, T={t_idx}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
