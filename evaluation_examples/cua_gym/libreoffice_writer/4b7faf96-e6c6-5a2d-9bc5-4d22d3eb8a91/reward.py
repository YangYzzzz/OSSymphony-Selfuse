"""
Reward Script: Export poster_print_ready.pdf with CMYK simulation, 300 DPI, and 3mm bleed
Task ID: osworld_multi_apps_writer_gimp_073
Domain: libreoffice_writer + gimp (multi-app)
Scoring:
  Component 1: PDF output file exists at correct path on Desktop (0.3 pts)
  Component 2: Page dimensions include 3mm bleed (MediaBox ~612.28 x 858.90 pts, within 1pt tolerance) (0.4 pts)
  Component 3: Image embedded at ~300 DPI (pixel dimensions correspond to ~300 DPI at page size) (0.3 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_writer_gimp_073'

# Target path: PDF on Desktop
PDF_PATH = '/home/user/Desktop/poster_print_ready.pdf'

# Golden PDF MediaBox: 0 0 612.28 858.90 (A4 = 595.28x841.89 pts, 3mm bleed = 8.504 pts each side)
# Expected: 595.28 + 2*8.504 = 612.29, 841.89 + 2*8.504 = 858.90
EXPECTED_W_MIN = 611.0
EXPECTED_W_MAX = 614.0
EXPECTED_H_MIN = 857.5
EXPECTED_H_MAX = 860.5

# 300 DPI verification via embedded image pixel dimensions
# At 300 DPI, image should be approximately:
#   width_px = (page_width_pts / 72) * 300 = ~2550 px
#   height_px = (page_height_pts / 72) * 300 = ~3578 px
# Tolerance: allow 200-3500 px range check and verify DPI between 280 and 320
DPI_MIN = 280.0
DPI_MAX = 320.0


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF output file exists at /home/user/Desktop/poster_print_ready.pdf (0.3 pts)
    # This FAILS on initial_env (no PDF present) and PASSES on golden_env
    try:
        if os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0:
            # Confirm it's a valid PDF by checking header
            with open(pdf_path, 'rb') as f:
                header = f.read(8)
            if header.startswith(b'%PDF'):
                print(f"PASS: Component 1 — PDF file exists at {pdf_path} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — File exists but is not a valid PDF (header: {header[:8]})")
        else:
            print(f"FAIL: Component 1 — PDF not found at {pdf_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page dimensions include 3mm bleed (0.4 pts)
    # A4 page = 595.28 x 841.89 pts; 3mm bleed per side = 8.504 pts
    # Expected MediaBox: ~612.28 x 858.90 pts
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        if not os.path.isfile(pdf_path):
            print(f"FAIL: Component 2 — PDF not found, cannot check dimensions")
        else:
            with open(pdf_path, 'rb') as f:
                content = f.read()

            mediabox_matches = re.findall(rb'/MediaBox \[([^\]]+)\]', content)
            if not mediabox_matches:
                print(f"FAIL: Component 2 — No MediaBox found in PDF")
            else:
                # Parse first MediaBox
                mb_str = mediabox_matches[0].decode('latin-1').strip()
                parts = mb_str.split()
                if len(parts) < 4:
                    print(f"FAIL: Component 2 — MediaBox format unexpected: {mb_str}")
                else:
                    # MediaBox format: [x0 y0 x1 y1]
                    x0, y0, x1, y1 = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
                    page_w = x1 - x0
                    page_h = y1 - y0
                    print(f"INFO: MediaBox = {x0} {y0} {x1} {y1}  →  page {page_w:.2f} x {page_h:.2f} pts")

                    w_ok = EXPECTED_W_MIN <= page_w <= EXPECTED_W_MAX
                    h_ok = EXPECTED_H_MIN <= page_h <= EXPECTED_H_MAX

                    if w_ok and h_ok:
                        print(f"PASS: Component 2 — 3mm bleed confirmed: page {page_w:.2f} x {page_h:.2f} pts "
                              f"(expected ~612.28 x 858.90) (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 — Page dimensions {page_w:.2f} x {page_h:.2f} pts "
                              f"not in expected range [{EXPECTED_W_MIN}-{EXPECTED_W_MAX}] x "
                              f"[{EXPECTED_H_MIN}-{EXPECTED_H_MAX}]")
                        if not w_ok:
                            print(f"       Width {page_w:.2f} out of range [{EXPECTED_W_MIN}, {EXPECTED_W_MAX}]")
                        if not h_ok:
                            print(f"       Height {page_h:.2f} out of range [{EXPECTED_H_MIN}, {EXPECTED_H_MAX}]")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image embedded at ~300 DPI (0.3 pts)
    # PDF embeds image at 2550 x 3578 px within 612.28 x 858.90 pt page → ~300 DPI
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        if not os.path.isfile(pdf_path):
            print(f"FAIL: Component 3 — PDF not found, cannot check DPI")
        else:
            with open(pdf_path, 'rb') as f:
                content = f.read()

            # Extract image Width and Height from PDF stream dictionaries
            widths = [int(w) for w in re.findall(rb'/Width (\d+)', content)]
            heights = [int(h) for h in re.findall(rb'/Height (\d+)', content)]

            if not widths or not heights:
                print(f"FAIL: Component 3 — No image dimensions found in PDF")
            else:
                print(f"INFO: Image widths in PDF: {widths}")
                print(f"INFO: Image heights in PDF: {heights}")

                # Use largest image (the main poster image)
                max_width = max(widths)
                max_height = max(heights)

                # Calculate effective DPI using MediaBox dimensions
                mediabox_matches = re.findall(rb'/MediaBox \[([^\]]+)\]', content)
                if mediabox_matches:
                    mb_str = mediabox_matches[0].decode('latin-1').strip()
                    parts = mb_str.split()
                    x0, y0, x1, y1 = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
                    page_w_pts = x1 - x0
                    page_h_pts = y1 - y0

                    # DPI = pixels / (pts / 72)
                    page_w_inches = page_w_pts / 72.0
                    page_h_inches = page_h_pts / 72.0
                    dpi_x = max_width / page_w_inches
                    dpi_y = max_height / page_h_inches
                    print(f"INFO: Effective DPI: {dpi_x:.1f} x {dpi_y:.1f}")

                    if DPI_MIN <= dpi_x <= DPI_MAX and DPI_MIN <= dpi_y <= DPI_MAX:
                        print(f"PASS: Component 3 — ~300 DPI confirmed: {dpi_x:.1f} x {dpi_y:.1f} DPI "
                              f"(image {max_width}x{max_height} px) (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 3 — DPI {dpi_x:.1f} x {dpi_y:.1f} not in expected range "
                              f"[{DPI_MIN}, {DPI_MAX}]. Image: {max_width}x{max_height} px")
                else:
                    print(f"FAIL: Component 3 — Cannot compute DPI without MediaBox")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification — always call verify_task; function handles missing file per-component
verify_task(PDF_PATH)
