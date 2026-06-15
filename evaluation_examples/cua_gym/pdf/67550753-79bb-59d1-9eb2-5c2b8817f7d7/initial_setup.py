"""
Initial Setup: Create a 75-page thesis PDF for tab/bookmark marking task
Task ID: pdf_res_094
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_094'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/tabbed_thesis.pdf'

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
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Thesis structure: chapters, sections, with realistic academic content
    thesis_structure = [
        # (page_range_start, page_range_end, chapter_title, sections)
        (1, 1, "Title Page", []),
        (2, 3, "Abstract and Acknowledgments", []),
        (4, 5, "Table of Contents", []),
        (6, 14, "Chapter 1: Introduction", [
            "1.1 Background and Motivation",
            "1.2 Problem Statement",
            "1.3 Research Objectives",
            "1.4 Thesis Organization",
        ]),
        (15, 28, "Chapter 2: Literature Review", [
            "2.1 Historical Overview of Machine Learning",
            "2.2 Deep Neural Network Architectures",
            "2.3 Transfer Learning Approaches",
            "2.4 Reinforcement Learning Foundations",
            "2.5 Related Work in Autonomous Systems",
        ]),
        (29, 42, "Chapter 3: Methodology", [
            "3.1 Research Design",
            "3.2 Data Collection Framework",
            "3.3 Model Architecture",
            "3.4 Training Procedure",
            "3.5 Evaluation Metrics",
        ]),
        (43, 55, "Chapter 4: Experimental Setup", [
            "4.1 Hardware and Software Configuration",
            "4.2 Dataset Description",
            "4.3 Baseline Models",
            "4.4 Hyperparameter Selection",
        ]),
        (56, 67, "Chapter 5: Results and Discussion", [
            "5.1 Quantitative Results",
            "5.2 Qualitative Analysis",
            "5.3 Ablation Studies",
            "5.4 Comparison with State-of-the-Art",
            "5.5 Limitations and Threats to Validity",
        ]),
        (68, 72, "Chapter 6: Conclusion and Future Work", [
            "6.1 Summary of Contributions",
            "6.2 Implications for Practice",
            "6.3 Directions for Future Research",
        ]),
        (73, 75, "References", []),
    ]

    # Body text paragraphs for filling pages
    body_paragraphs = [
        "The rapid advancement of artificial intelligence has fundamentally transformed how we approach complex computational problems. Recent developments in deep learning architectures have enabled breakthroughs across diverse domains including natural language processing, computer vision, and robotics.",
        "Our experimental framework builds upon the theoretical foundations established by prior work in reinforcement learning. The integration of attention mechanisms with policy gradient methods provides a robust approach to handling high-dimensional state spaces.",
        "Statistical analysis of the collected data reveals significant improvements over baseline methods. The proposed architecture achieves a mean accuracy of 94.7% on the benchmark dataset, representing a 3.2% improvement over the previous state-of-the-art.",
        "The implications of these findings extend beyond the immediate scope of this research. As autonomous systems become more prevalent in industrial applications, the need for reliable and interpretable decision-making frameworks becomes increasingly critical.",
        "Cross-validation experiments were conducted using a stratified five-fold approach to ensure robust evaluation. Each fold maintained the original class distribution, and results were averaged across all iterations to minimize variance.",
        "The convergence behavior of the optimization algorithm was monitored throughout training. Early stopping criteria were applied based on validation loss plateaus, with a patience window of 15 epochs to prevent premature termination.",
        "Feature importance analysis using SHAP values revealed that temporal dependencies in the input sequences contributed most significantly to the model's predictive performance. This finding aligns with the theoretical motivation for incorporating recurrent connections.",
        "Qualitative evaluation through expert interviews confirmed the practical applicability of the proposed system. Domain specialists from three partner institutions provided feedback on the system's outputs, rating them as highly relevant and actionable.",
    ]

    page_idx = 0
    for start, end, chapter, sections in thesis_structure:
        for pg in range(start, end + 1):
            page = doc.new_page(width=595, height=842)  # A4
            page_idx += 1

            if pg == 1:
                # Title page
                page.insert_text(
                    pymupdf.Point(297, 200),
                    "Adaptive Reinforcement Learning",
                    fontsize=22, fontname="hebo", color=(0, 0, 0),
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 230, 523, 270),
                    "for Autonomous Decision-Making in Complex Environments",
                    fontsize=18, fontname="hebo", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 350, 523, 380),
                    "A Thesis Submitted in Partial Fulfillment of the Requirements",
                    fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 380, 523, 410),
                    "for the Degree of Doctor of Philosophy",
                    fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 460, 523, 490),
                    "Elena Vasquez-Rodriguez",
                    fontsize=16, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 510, 523, 540),
                    "Department of Computer Science",
                    fontsize=12, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 540, 523, 570),
                    "Stanford University",
                    fontsize=12, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
                page.insert_textbox(
                    pymupdf.Rect(72, 600, 523, 630),
                    "March 2025",
                    fontsize=12, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
            elif chapter == "Table of Contents" and pg == start:
                # TOC page
                page.insert_text(
                    pymupdf.Point(72, 72),
                    "Table of Contents",
                    fontsize=18, fontname="hebo", color=(0, 0, 0),
                )
                y = 110
                for s, e, ch, secs in thesis_structure:
                    if ch in ("Title Page", "Abstract and Acknowledgments", "Table of Contents"):
                        continue
                    page.insert_text(
                        pymupdf.Point(72, y),
                        f"{ch} {'.' * (50 - len(ch))} {s}",
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                    )
                    y += 18
                    for sec in secs:
                        if y > 780:
                            break
                        page.insert_text(
                            pymupdf.Point(100, y),
                            sec,
                            fontsize=9, fontname="tiro", color=(0.2, 0.2, 0.2),
                        )
                        y += 15
            elif pg == start and chapter not in ("Title Page", "Abstract and Acknowledgments", "Table of Contents"):
                # Chapter start page
                page.insert_text(
                    pymupdf.Point(72, 100),
                    chapter,
                    fontsize=18, fontname="hebo", color=(0, 0, 0),
                )
                # Draw a line under the chapter title
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, 110), pymupdf.Point(523, 110))
                shape.finish(color=(0, 0, 0), width=1)
                shape.commit()

                y = 140
                # Add first section heading if available
                if sections:
                    page.insert_text(
                        pymupdf.Point(72, y),
                        sections[0],
                        fontsize=13, fontname="hebo", color=(0, 0, 0),
                    )
                    y += 30

                # Fill with body text
                para_idx = (pg * 3) % len(body_paragraphs)
                for i in range(3):
                    if y > 750:
                        break
                    para = body_paragraphs[(para_idx + i) % len(body_paragraphs)]
                    excess = page.insert_textbox(
                        pymupdf.Rect(72, y, 523, y + 120),
                        para,
                        fontsize=11, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    y += 130
            else:
                # Regular content pages
                y = 60
                # Determine which section we're in
                relative_page = pg - start
                if sections and relative_page < len(sections):
                    sec_title = sections[relative_page]
                    page.insert_text(
                        pymupdf.Point(72, y),
                        sec_title,
                        fontsize=13, fontname="hebo", color=(0, 0, 0),
                    )
                    y += 30

                # Fill with body text paragraphs
                para_idx = (pg * 7 + 13) % len(body_paragraphs)
                for i in range(5):
                    if y > 750:
                        break
                    para = body_paragraphs[(para_idx + i) % len(body_paragraphs)]
                    excess = page.insert_textbox(
                        pymupdf.Rect(72, y, 523, y + 110),
                        para,
                        fontsize=11, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    y += 120

            # Page number at bottom center (except title page)
            if pg > 1:
                page.insert_textbox(
                    pymupdf.Rect(250, 800, 345, 825),
                    str(pg),
                    fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )

    # Set metadata
    doc.set_metadata({
        "title": "Adaptive Reinforcement Learning for Autonomous Decision-Making in Complex Environments",
        "author": "Elena Vasquez-Rodriguez",
        "subject": "PhD Thesis - Computer Science",
        "keywords": "reinforcement learning, deep learning, autonomous systems, decision-making",
    })

    # Set TOC bookmarks
    toc = [
        [1, "Title Page", 1],
        [1, "Abstract and Acknowledgments", 2],
        [1, "Table of Contents", 4],
        [1, "Chapter 1: Introduction", 6],
        [1, "Chapter 2: Literature Review", 15],
        [1, "Chapter 3: Methodology", 29],
        [1, "Chapter 4: Experimental Setup", 43],
        [1, "Chapter 5: Results and Discussion", 56],
        [1, "Chapter 6: Conclusion and Future Work", 68],
        [1, "References", 73],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 75')

    # Open PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
