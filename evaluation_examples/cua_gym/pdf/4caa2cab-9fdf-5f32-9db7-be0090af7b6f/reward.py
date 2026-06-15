"""
Reward Script: PDF Version Control System
Task ID: pdf_gf3_045
Domain: pdf
Scoring:
  Component 1 (0.15): pdf_vcs.py exists and has reconstruct() function
  Component 2 (0.15): history.json is valid JSON with base_text and diffs
  Component 3 (0.20): Text extraction from PDFs works and diffs use difflib
  Component 4 (0.25): reconstruct() regenerates version text matching actual PDF text
  Component 5 (0.10): Edge cases: version 1 returns base, invalid version raises ValueError
  Component 6 (0.15): history.json is smaller than total PDF file sizes (compact representation)
"""

import os
import json
import sys

WORKDIR = '/home/user'
VERSIONS_DIR = os.path.join(WORKDIR, 'versions')
SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'pdf_vcs.py')
HISTORY_PATH = os.path.join(VERSIONS_DIR, 'history.json')


def verify_task():
    """
    Verify PDF version control system task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: pdf_vcs.py exists and has reconstruct() function (0.15 pts)
    # =========================================================================
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print(f"FAIL: Component 1 — pdf_vcs.py not found at {SCRIPT_PATH}")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()
            # Check that reconstruct function is defined
            if 'def reconstruct(' in script_content:
                print(f"PASS: Component 1 — pdf_vcs.py exists with reconstruct() function (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — pdf_vcs.py exists but no reconstruct() function defined")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: history.json is valid JSON with base_text and diffs (0.15 pts)
    # =========================================================================
    history_data = None
    try:
        if not os.path.isfile(HISTORY_PATH):
            print(f"FAIL: Component 2 — history.json not found at {HISTORY_PATH}")
        else:
            with open(HISTORY_PATH, 'r') as f:
                history_data = json.load(f)

            has_base = isinstance(history_data.get('base_text'), str) and len(history_data['base_text']) > 0
            has_diffs = isinstance(history_data.get('diffs'), dict)
            # Must have diffs for versions 2-5
            has_all_diffs = has_diffs and all(
                str(v) in history_data['diffs'] for v in range(2, 6)
            )

            if has_base and has_all_diffs:
                print(f"PASS: Component 2 — history.json valid with base_text ({len(history_data['base_text'])} chars) and diffs for v2-v5 (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_base:
                    missing.append("base_text")
                if not has_all_diffs:
                    missing.append("diffs for all v2-v5")
                print(f"FAIL: Component 2 — history.json missing: {', '.join(missing)}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — history.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: Script uses difflib for diffs (0.20 pts)
    # =========================================================================
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print(f"FAIL: Component 3 — pdf_vcs.py not found")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()

            uses_difflib = 'difflib' in script_content
            uses_pymupdf = 'pymupdf' in script_content or 'fitz' in script_content

            if uses_difflib and uses_pymupdf:
                print(f"PASS: Component 3 — Script uses difflib and PyMuPDF/fitz (0.20 pts)")
                total_score += 0.20
            elif uses_difflib:
                # Partial: has difflib but not PyMuPDF references in script
                # (PyMuPDF might only be used at generation time, not in the script itself)
                print(f"PARTIAL: Component 3 — Script uses difflib but no PyMuPDF reference (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Script missing difflib (uses_difflib={uses_difflib}, uses_pymupdf={uses_pymupdf})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: reconstruct() regenerates version text matching PDF (0.25 pts)
    # =========================================================================
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print(f"FAIL: Component 4 — pdf_vcs.py not found")
        else:
            # Import the module dynamically
            import importlib.util
            spec = importlib.util.spec_from_file_location("pdf_vcs", SCRIPT_PATH)
            pdf_vcs = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pdf_vcs)

            import pymupdf

            versions_matched = 0
            versions_total = 5

            for v in range(1, 6):
                pdf_path = os.path.join(VERSIONS_DIR, f'v{v}.pdf')
                if not os.path.isfile(pdf_path):
                    print(f"  v{v}: PDF not found at {pdf_path}")
                    continue

                doc = pymupdf.open(pdf_path)
                actual_text = ""
                for page in doc:
                    actual_text += page.get_text("text")
                doc.close()

                reconstructed = pdf_vcs.reconstruct(v)

                # Normalize whitespace for comparison
                actual_norm = ' '.join(actual_text.split())
                recon_norm = ' '.join(reconstructed.split())

                if actual_norm == recon_norm:
                    versions_matched += 1
                    print(f"  v{v}: MATCH ({len(reconstructed)} chars)")
                else:
                    print(f"  v{v}: MISMATCH (actual={len(actual_norm)} chars, reconstructed={len(recon_norm)} chars)")

            # Score proportionally: 0.05 per version matched
            comp4_score = (versions_matched / versions_total) * 0.25
            if versions_matched == versions_total:
                print(f"PASS: Component 4 — All {versions_total} versions reconstruct correctly (0.25 pts)")
            else:
                print(f"PARTIAL: Component 4 — {versions_matched}/{versions_total} versions match ({comp4_score:.2f} pts)")
            total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: Edge cases handled correctly (0.10 pts)
    # =========================================================================
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print(f"FAIL: Component 5 — pdf_vcs.py not found")
        else:
            import importlib.util
            spec = importlib.util.spec_from_file_location("pdf_vcs_edge", SCRIPT_PATH)
            pdf_vcs = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pdf_vcs)

            edge_score = 0.0

            # Version 1 should return base text (same as base_text in history.json)
            if history_data is not None:
                v1_text = pdf_vcs.reconstruct(1)
                if v1_text == history_data.get('base_text', ''):
                    print(f"  Edge: version 1 returns base_text correctly")
                    edge_score += 0.05
                else:
                    print(f"  Edge: version 1 does not match base_text")

            # Invalid version should raise ValueError
            raised_error = False
            try:
                pdf_vcs.reconstruct(0)
            except ValueError:
                raised_error = True
            except Exception:
                pass  # Other exceptions don't count

            raised_error_2 = False
            try:
                pdf_vcs.reconstruct(6)
            except ValueError:
                raised_error_2 = True
            except Exception:
                pass

            if raised_error and raised_error_2:
                print(f"  Edge: invalid versions (0, 6) correctly raise ValueError")
                edge_score += 0.05
            else:
                print(f"  Edge: invalid version handling incomplete (v0={raised_error}, v6={raised_error_2})")

            if edge_score >= 0.10:
                print(f"PASS: Component 5 — Edge cases handled correctly (0.10 pts)")
            elif edge_score > 0:
                print(f"PARTIAL: Component 5 — Some edge cases pass ({edge_score:.2f} pts)")
            else:
                print(f"FAIL: Component 5 — Edge cases not handled")
            total_score += edge_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================================
    # Component 6: history.json is compact (smaller than total PDF sizes) (0.15 pts)
    # =========================================================================
    try:
        if not os.path.isfile(HISTORY_PATH):
            print(f"FAIL: Component 6 — history.json not found")
        else:
            history_size = os.path.getsize(HISTORY_PATH)

            # Calculate total PDF file sizes
            total_pdf_size = 0
            for v in range(1, 6):
                pdf_path = os.path.join(VERSIONS_DIR, f'v{v}.pdf')
                if os.path.isfile(pdf_path):
                    total_pdf_size += os.path.getsize(pdf_path)

            if total_pdf_size > 0 and history_size < total_pdf_size:
                print(f"PASS: Component 6 — history.json ({history_size} bytes) is smaller than total PDFs ({total_pdf_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — history.json ({history_size} bytes) is NOT smaller than total PDFs ({total_pdf_size} bytes)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
