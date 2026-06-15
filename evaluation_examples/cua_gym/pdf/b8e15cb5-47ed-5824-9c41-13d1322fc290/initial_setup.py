"""
Initial Setup: Create an A3 poster PDF for the tiling task.
Task ID: pdf_gf2_033
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf2_033'
OUTPUT = f'{DOCS_DIR}/poster.pdf'

# A3 dimensions in points
A3_WIDTH = 842
A3_HEIGHT = 1191


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=A3_WIDTH, height=A3_HEIGHT)

    # ---- Background ----
    shape = page.new_shape()
    # Light gradient-like background (solid light cream)
    shape.draw_rect(pymupdf.Rect(0, 0, A3_WIDTH, A3_HEIGHT))
    shape.finish(fill=(0.98, 0.96, 0.92), color=None)
    shape.commit()

    # ---- Title Banner (top center, spanning both top quadrants) ----
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(40, 30, A3_WIDTH - 40, 120))
    shape.finish(fill=(0.12, 0.24, 0.48), color=(0.08, 0.16, 0.32), width=2)
    shape.commit()

    page.insert_text(
        pymupdf.Point(80, 90),
        "Annual Research Symposium 2025",
        fontsize=36,
        fontname="hebo",
        color=(1, 1, 1),
    )

    page.insert_text(
        pymupdf.Point(80, 115),
        "Department of Computational Sciences — Westfield University",
        fontsize=14,
        fontname="heit",
        color=(0.85, 0.85, 0.95),
    )

    # ==== TOP-LEFT QUADRANT: Introduction & Methods ====
    # Section header
    page.insert_text(
        pymupdf.Point(50, 170),
        "1. Introduction",
        fontsize=20,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    intro_text = (
        "Recent advances in transformer-based architectures have revolutionized "
        "natural language processing, enabling models to capture long-range "
        "dependencies with unprecedented accuracy. Our research focuses on "
        "developing efficient attention mechanisms that reduce computational "
        "complexity from O(n^2) to O(n log n) while maintaining performance "
        "parity with full-attention baselines across 12 benchmark datasets."
    )
    rect_intro = pymupdf.Rect(50, 180, 400, 340)
    page.insert_textbox(rect_intro, intro_text, fontsize=11, fontname="helv",
                        color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Methods sub-section
    page.insert_text(
        pymupdf.Point(50, 360),
        "2. Methodology",
        fontsize=20,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    methods_text = (
        "We employ a multi-stage training pipeline consisting of: (i) pre-training "
        "on 800GB of curated web text, (ii) supervised fine-tuning on 15 domain-"
        "specific corpora, and (iii) reinforcement learning from human feedback "
        "(RLHF) with 50,000 preference pairs collected from expert annotators. "
        "Hyperparameters were tuned using Bayesian optimization over 200 trials."
    )
    rect_methods = pymupdf.Rect(50, 370, 400, 540)
    page.insert_textbox(rect_methods, methods_text, fontsize=11, fontname="helv",
                        color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==== TOP-RIGHT QUADRANT: Results Table & Chart-like visualization ====
    page.insert_text(
        pymupdf.Point(450, 170),
        "3. Results",
        fontsize=20,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    # Results table header
    shape = page.new_shape()
    table_x = 450
    table_y = 185
    col_widths = [130, 80, 80, 80]
    row_height = 22
    headers = ["Dataset", "Baseline", "Ours", "Gain"]

    # Header row background
    shape.draw_rect(pymupdf.Rect(table_x, table_y,
                                 table_x + sum(col_widths), table_y + row_height))
    shape.finish(fill=(0.12, 0.24, 0.48), color=(0.08, 0.16, 0.32))
    shape.commit()

    # Header text
    cx = table_x
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cx + 5, table_y + 16), h,
                         fontsize=10, fontname="hebo", color=(1, 1, 1))
        cx += col_widths[i]

    # Data rows
    data_rows = [
        ["GLUE Average",   "87.3", "91.2", "+3.9"],
        ["SQuAD v2.0",     "84.1", "88.7", "+4.6"],
        ["WMT En-De",      "29.4", "31.8", "+2.4"],
        ["SuperGLUE",      "85.6", "89.1", "+3.5"],
        ["CoNLL-2003 NER", "92.4", "94.7", "+2.3"],
        ["XNLI (avg)",     "78.9", "83.5", "+4.6"],
        ["TyDi QA",        "71.2", "76.8", "+5.6"],
        ["PIQA",           "80.1", "84.3", "+4.2"],
    ]

    for r_idx, row in enumerate(data_rows):
        ry = table_y + row_height * (r_idx + 1)
        bg_color = (0.95, 0.95, 0.98) if r_idx % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(table_x, ry,
                                     table_x + sum(col_widths), ry + row_height))
        shape.finish(fill=bg_color, color=(0.8, 0.8, 0.8))
        shape.commit()

        cx = table_x
        for c_idx, cell in enumerate(row):
            fn = "hebo" if c_idx == 3 else "helv"
            clr = (0.0, 0.5, 0.0) if c_idx == 3 else (0.15, 0.15, 0.15)
            page.insert_text(pymupdf.Point(cx + 5, ry + 16), cell,
                             fontsize=9, fontname=fn, color=clr)
            cx += col_widths[i]

    # Bar chart-like visualization
    page.insert_text(
        pymupdf.Point(450, 420),
        "Performance Comparison",
        fontsize=14,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    bar_labels = ["GLUE", "SQuAD", "WMT", "SGLUE", "NER"]
    baseline_vals = [87.3, 84.1, 29.4, 85.6, 92.4]
    ours_vals = [91.2, 88.7, 31.8, 89.1, 94.7]
    bar_x_start = 460
    bar_y_start = 530
    bar_width = 25
    bar_gap = 45
    max_val = 100.0
    chart_height = 90

    for i, label in enumerate(bar_labels):
        bx = bar_x_start + i * bar_gap
        # Baseline bar
        bh1 = (baseline_vals[i] / max_val) * chart_height
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(bx, bar_y_start - bh1, bx + bar_width // 2, bar_y_start))
        shape.finish(fill=(0.6, 0.6, 0.8), color=(0.4, 0.4, 0.6))
        shape.commit()

        # Ours bar
        bh2 = (ours_vals[i] / max_val) * chart_height
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(bx + bar_width // 2, bar_y_start - bh2,
                                     bx + bar_width, bar_y_start))
        shape.finish(fill=(0.2, 0.6, 0.3), color=(0.1, 0.4, 0.2))
        shape.commit()

        # Label
        page.insert_text(pymupdf.Point(bx, bar_y_start + 12), label,
                         fontsize=7, fontname="helv", color=(0.3, 0.3, 0.3))

    # Legend
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(680, 435, 695, 445))
    shape.finish(fill=(0.6, 0.6, 0.8), color=None)
    shape.commit()
    page.insert_text(pymupdf.Point(700, 445), "Baseline", fontsize=8,
                     fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(680, 450, 695, 460))
    shape.finish(fill=(0.2, 0.6, 0.3), color=None)
    shape.commit()
    page.insert_text(pymupdf.Point(700, 460), "Ours", fontsize=8,
                     fontname="helv", color=(0.3, 0.3, 0.3))

    # ==== BOTTOM-LEFT QUADRANT: Analysis & Discussion ====
    page.insert_text(
        pymupdf.Point(50, 630),
        "4. Analysis & Discussion",
        fontsize=20,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    analysis_text = (
        "Our sparse attention mechanism achieves consistent improvements across "
        "all benchmarks while reducing training time by 35% and inference latency "
        "by 42%. The largest gains are observed on cross-lingual tasks (XNLI, "
        "TyDi QA), suggesting that efficient attention patterns better capture "
        "universal linguistic structures.\n\n"
        "Key Findings:\n"
        "  - Attention sparsity of 85% maintains 99.1% of dense performance\n"
        "  - Memory usage reduced from 48GB to 28GB on A100 GPUs\n"
        "  - Training convergence achieved 2.3x faster than baseline\n"
        "  - Zero-shot cross-lingual transfer improved by 6.2 F1 points"
    )
    rect_analysis = pymupdf.Rect(50, 640, 400, 880)
    page.insert_textbox(rect_analysis, analysis_text, fontsize=11, fontname="helv",
                        color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_LEFT)

    # Diagram: simple flowchart
    shape = page.new_shape()
    boxes = [
        (100, 900, 220, 935, "Pre-training"),
        (100, 955, 220, 990, "Fine-tuning"),
        (100, 1010, 220, 1045, "RLHF"),
        (260, 955, 380, 990, "Evaluation"),
    ]
    for x0, y0, x1, y1, label in boxes:
        shape.draw_rect(pymupdf.Rect(x0, y0, x1, y1))
        shape.finish(fill=(0.9, 0.92, 0.98), color=(0.12, 0.24, 0.48), width=1.5)
    shape.commit()

    for x0, y0, x1, y1, label in boxes:
        page.insert_text(pymupdf.Point(x0 + 10, y0 + 22), label,
                         fontsize=10, fontname="hebo", color=(0.12, 0.24, 0.48))

    # Arrows between boxes
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(160, 935), pymupdf.Point(160, 955))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
    shape.commit()
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(160, 990), pymupdf.Point(160, 1010))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
    shape.commit()
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(220, 972), pymupdf.Point(260, 972))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
    shape.commit()

    # ==== BOTTOM-RIGHT QUADRANT: Conclusion & References ====
    page.insert_text(
        pymupdf.Point(450, 630),
        "5. Conclusion",
        fontsize=20,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    conclusion_text = (
        "We present a novel sparse attention mechanism that significantly improves "
        "efficiency without sacrificing accuracy. Our approach sets new state-of-the-"
        "art results on 8 of 12 benchmarks tested, while reducing computational "
        "requirements by over 40%. Future work will explore adaptive sparsity "
        "patterns that dynamically adjust to input complexity."
    )
    rect_conclusion = pymupdf.Rect(450, 640, 790, 780)
    page.insert_textbox(rect_conclusion, conclusion_text, fontsize=11, fontname="helv",
                        color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(
        pymupdf.Point(450, 810),
        "References",
        fontsize=16,
        fontname="hebo",
        color=(0.12, 0.24, 0.48),
    )

    references = [
        "[1] Vaswani et al. (2017). Attention Is All You Need. NeurIPS.",
        "[2] Devlin et al. (2019). BERT: Pre-training of Deep Bidirectional",
        "     Transformers. NAACL-HLT.",
        "[3] Brown et al. (2020). Language Models are Few-Shot Learners. NeurIPS.",
        "[4] Kitaev et al. (2020). Reformer: The Efficient Transformer. ICLR.",
        "[5] Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences.",
        "     NeurIPS.",
        "[6] Beltagy et al. (2020). Longformer: The Long-Document Transformer.",
        "[7] Wang et al. (2022). Efficient Sparse Attention for Language Models.",
        "     ICML.",
    ]
    ref_y = 825
    for ref in references:
        page.insert_text(pymupdf.Point(455, ref_y), ref,
                         fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        ref_y += 14

    # Contact info at bottom-right
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(450, 1050, 790, 1130))
    shape.finish(fill=(0.94, 0.94, 0.97), color=(0.7, 0.7, 0.8), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(460, 1070), "Contact Information",
                     fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.48))
    page.insert_text(pymupdf.Point(460, 1088), "Dr. Elena Rodriguez  |  erodriguez@westfield.edu",
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(460, 1102), "Computational Sciences Lab  |  Building 4, Room 312",
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(460, 1116), "https://compscience.westfield.edu/sparse-attention",
                     fontsize=9, fontname="helv", color=(0.2, 0.2, 0.7))

    # Decorative line separator down the middle
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(A3_WIDTH / 2, 135), pymupdf.Point(A3_WIDTH / 2, A3_HEIGHT - 50))
    shape.finish(color=(0.8, 0.8, 0.85), width=0.5, dashes="[4 4]")
    shape.commit()

    # Horizontal separator at midpoint
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(40, A3_HEIGHT / 2), pymupdf.Point(A3_WIDTH - 40, A3_HEIGHT / 2))
    shape.finish(color=(0.8, 0.8, 0.85), width=0.5, dashes="[4 4]")
    shape.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
