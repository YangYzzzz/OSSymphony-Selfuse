"""
Reward Script: Batch PDF Processor Verification
Task ID: pdf_gf3_020
Domain: pdf
Scoring:
  Component 1: batch_process.py script exists (0.10)
  Component 2: All 12 PDFs moved from incoming/ to processed/ (0.20)
  Component 3: Disclaimer page appended to each PDF (0.25)
  Component 4: PROCESSED watermark on all pages of each PDF (0.25)
  Component 5: Metadata updated on each processed PDF (0.20)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_020'

# Expected filenames (the 12 original PDFs)
EXPECTED_FILES = [
    'acme_supply_invoice_Q1.pdf',
    'atlas_freight_waybill.pdf',
    'bluewave_energy_audit.pdf',
    'cascade_maintenance_schedule.pdf',
    'greenfield_materials_cert.pdf',
    'horizon_logistics_contract.pdf',
    'nexgen_tech_proposal.pdf',
    'oakridge_compliance_review.pdf',
    'pinnacle_consulting_report.pdf',
    'riverstone_training_materials.pdf',
    'sterling_pharma_msds.pdf',
    'vertex_security_assessment.pdf',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: batch_process.py exists in /home/user/scripts/ (0.10 points)
    try:
        script_path = os.path.join(WORKDIR, 'scripts', 'batch_process.py')
        if os.path.isfile(script_path):
            # Verify it's not an empty file
            size = os.path.getsize(script_path)
            if size > 100:
                print(f"PASS: Component 1 — batch_process.py exists ({size} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — batch_process.py too small ({size} bytes), likely placeholder")
        else:
            print(f"FAIL: Component 1 — batch_process.py not found at {script_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 12 PDFs moved to processed/, incoming/ is empty (0.20 points)
    try:
        incoming_dir = os.path.join(WORKDIR, 'incoming')
        processed_dir = os.path.join(WORKDIR, 'processed')

        incoming_files = os.listdir(incoming_dir) if os.path.isdir(incoming_dir) else []
        processed_files = os.listdir(processed_dir) if os.path.isdir(processed_dir) else []

        # Check that all 12 expected files are in processed/
        processed_set = set(processed_files)
        expected_set = set(EXPECTED_FILES)
        matched = expected_set.intersection(processed_set)
        match_ratio = len(matched) / len(expected_set)

        # incoming should be empty
        incoming_empty = len(incoming_files) == 0

        if match_ratio == 1.0 and incoming_empty:
            print(f"PASS: Component 2 — All 12 PDFs in processed/, incoming/ empty (0.20 pts)")
            total_score += 0.20
        elif match_ratio > 0:
            partial = 0.20 * match_ratio * (0.5 if not incoming_empty else 1.0)
            print(f"PARTIAL: Component 2 — {len(matched)}/12 PDFs in processed/, incoming empty={incoming_empty} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No expected PDFs found in processed/. Found: {processed_files[:3]}...")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Disclaimer page appended as last page of each processed PDF (0.25 points)
    try:
        disclaimer_count = 0
        checked_count = 0

        for fname in EXPECTED_FILES:
            fpath = os.path.join(processed_dir, fname)
            if not os.path.isfile(fpath):
                continue
            checked_count += 1
            try:
                doc = pymupdf.open(fpath)
                last_page = doc[-1]
                last_text = last_page.get_text()
                doc.close()
                # The disclaimer page should contain "STANDARD DISCLAIMER" or similar
                if 'DISCLAIMER' in last_text.upper():
                    disclaimer_count += 1
            except Exception as inner_e:
                print(f"  WARN: Could not check disclaimer in {fname}: {inner_e}")

        if checked_count > 0 and disclaimer_count == checked_count:
            print(f"PASS: Component 3 — Disclaimer appended to all {disclaimer_count}/{checked_count} PDFs (0.25 pts)")
            total_score += 0.25
        elif disclaimer_count > 0:
            partial = 0.25 * (disclaimer_count / len(EXPECTED_FILES))
            print(f"PARTIAL: Component 3 — Disclaimer found in {disclaimer_count}/{checked_count} PDFs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No disclaimer pages found in processed PDFs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PROCESSED watermark on all pages of each processed PDF (0.25 points)
    try:
        files_with_watermark = 0
        checked_count = 0

        for fname in EXPECTED_FILES:
            fpath = os.path.join(processed_dir, fname)
            if not os.path.isfile(fpath):
                continue
            checked_count += 1
            try:
                doc = pymupdf.open(fpath)
                num_pages = len(doc)
                pages_with_mark = sum(
                    1 for i in range(num_pages)
                    if len(doc[i].search_for('PROCESSED')) > 0
                )
                doc.close()
                if pages_with_mark == num_pages:
                    files_with_watermark += 1
            except Exception as inner_e:
                print(f"  WARN: Could not check watermark in {fname}: {inner_e}")

        if checked_count > 0 and files_with_watermark == checked_count:
            print(f"PASS: Component 4 — PROCESSED watermark on all pages of all {files_with_watermark} PDFs (0.25 pts)")
            total_score += 0.25
        elif files_with_watermark > 0:
            partial = 0.25 * (files_with_watermark / len(EXPECTED_FILES))
            print(f"PARTIAL: Component 4 — Watermark on all pages in {files_with_watermark}/{checked_count} PDFs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No PROCESSED watermark found on processed PDFs")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Metadata updated with processing info (0.20 points)
    try:
        meta_updated_count = 0
        checked_count = 0

        for fname in EXPECTED_FILES:
            fpath = os.path.join(processed_dir, fname)
            if not os.path.isfile(fpath):
                continue
            checked_count += 1
            try:
                doc = pymupdf.open(fpath)
                meta = doc.metadata
                doc.close()
                # Check that metadata has been updated: keywords or creator or producer
                # should indicate processing
                keywords = (meta.get('keywords', '') or '').lower()
                creator = (meta.get('creator', '') or '').lower()
                producer = (meta.get('producer', '') or '').lower()
                mod_date = meta.get('modDate', '') or ''

                has_processing_indicator = (
                    'process' in keywords or
                    'process' in creator or
                    'process' in producer or
                    'batch' in keywords or
                    'batch' in creator or
                    'batch' in producer
                )
                has_mod_date = len(mod_date) > 0

                if has_processing_indicator and has_mod_date:
                    meta_updated_count += 1
            except Exception as inner_e:
                print(f"  WARN: Could not check metadata in {fname}: {inner_e}")

        if checked_count > 0 and meta_updated_count == checked_count:
            print(f"PASS: Component 5 — Metadata updated on all {meta_updated_count} PDFs (0.20 pts)")
            total_score += 0.20
        elif meta_updated_count > 0:
            partial = 0.20 * (meta_updated_count / len(EXPECTED_FILES))
            print(f"PARTIAL: Component 5 — Metadata updated on {meta_updated_count}/{checked_count} PDFs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No metadata updates found in processed PDFs")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
