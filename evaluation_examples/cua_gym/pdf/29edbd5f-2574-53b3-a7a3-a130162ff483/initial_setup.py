"""
Initial Setup: Create a 60-page thesis PDF with bookmarks but default view settings
Task ID: pdf_res_044
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_044'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/thesis_presentation.pdf'

def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

BODY_TEXTS = [
    "Deep learning has revolutionized numerous fields in artificial intelligence, enabling breakthroughs in computer vision, natural language processing, and reinforcement learning. The rapid advancement of neural network architectures has led to models that can process increasingly complex patterns in data.",
    "Transfer learning has emerged as a critical technique for leveraging pre-trained representations across domains. By initializing models with weights learned from large-scale datasets, researchers can achieve strong performance even with limited task-specific data, reducing both computational cost and data requirements.",
    "Our experimental framework employs a rigorous cross-validation strategy to ensure robust evaluation of the proposed methods. We utilize stratified k-fold validation with k=5, maintaining class distribution across all folds while preventing data leakage between training and evaluation sets.",
    "The neural architecture search space encompasses a diverse set of operation primitives including standard convolutions, depthwise separable convolutions, dilated convolutions, and attention mechanisms. Each candidate architecture is evaluated using a proxy task to reduce computational overhead.",
    "Statistical analysis reveals significant improvements over baseline methods across all evaluation metrics. The paired t-test yields p-values below 0.01 for accuracy, F1-score, and area under the ROC curve, confirming that the observed improvements are not attributable to random variation.",
    "Visualization of learned feature representations using t-SNE dimensionality reduction shows clear cluster separation in the embedding space. The proposed model learns more discriminative features compared to baseline approaches, with inter-class distance increasing by an average of 23.7%.",
    "The computational efficiency of the proposed approach is noteworthy, requiring only 40% of the floating-point operations compared to the best-performing baseline while maintaining comparable accuracy. This reduction in computational cost makes the model suitable for deployment on resource-constrained edge devices.",
    "Future work will explore the integration of self-supervised pre-training objectives with the proposed architecture search framework. Additionally, extending the approach to multi-modal learning scenarios presents an exciting avenue for advancing the state of the art in cross-domain transfer.",
]

# TOC structure: (level, title, start_page_1indexed)
# We'll lay out 60 pages with a known structure
TOC_ENTRIES = [
    (1, "Abstract", 1),
    (1, "Acknowledgements", 2),
    (1, "Table of Contents", 3),
    (1, "List of Figures", 4),
    (1, "List of Tables", 5),
    (1, "Chapter 1: Introduction", 6),
    (2, "1.1 Background and Motivation", 7),
    (2, "1.2 Problem Statement", 8),
    (2, "1.3 Research Objectives", 9),
    (2, "1.4 Thesis Organization", 10),
    (1, "Chapter 2: Literature Review", 11),
    (2, "2.1 Theoretical Framework", 12),
    (2, "2.2 Prior Work on Neural Architecture Search", 14),
    (2, "2.3 Transfer Learning Approaches", 17),
    (2, "2.4 Research Gaps", 18),
    (1, "Chapter 3: Methodology", 19),
    (2, "3.1 Research Design", 20),
    (2, "3.2 Data Collection", 22),
    (2, "3.3 Proposed Architecture", 24),
    (2, "3.4 Training Procedure", 27),
    (2, "3.5 Evaluation Metrics", 28),
    (1, "Chapter 4: Experimental Setup", 29),
    (2, "4.1 Dataset Description", 30),
    (2, "4.2 Baseline Models", 32),
    (2, "4.3 Hyperparameter Configuration", 34),
    (2, "4.4 Computational Resources", 36),
    (1, "Chapter 5: Results and Analysis", 37),
    (2, "5.1 Main Results", 38),
    (2, "5.2 Ablation Studies", 41),
    (2, "5.3 Comparison with State-of-the-Art", 44),
    (2, "5.4 Qualitative Analysis", 46),
    (2, "5.5 Statistical Significance Tests", 48),
    (1, "Chapter 6: Discussion", 49),
    (2, "6.1 Interpretation of Results", 50),
    (2, "6.2 Limitations", 52),
    (2, "6.3 Implications for Practice", 54),
    (1, "Chapter 7: Conclusion and Future Work", 55),
    (2, "7.1 Summary of Contributions", 56),
    (2, "7.2 Future Research Directions", 57),
    (1, "References", 58),
    (1, "Appendix A: Supplementary Figures", 60),
]


def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)
    doc = pymupdf.open()

    # Build a lookup: page_num -> list of titles to display
    page_titles = {}
    for level, title, page_num in TOC_ENTRIES:
        if page_num not in page_titles:
            page_titles[page_num] = []
        page_titles[page_num].append((level, title))

    # Create exactly 60 pages
    for pg in range(1, 61):
        page = doc.new_page(width=612, height=792)
        y = 72

        if pg in page_titles:
            for level, title in page_titles[pg]:
                fontsize = 22 if level == 1 else 16
                page.insert_text(
                    pymupdf.Point(72, y), title,
                    fontsize=fontsize, fontname="hebo",
                    color=(0.1, 0.1, 0.3) if level == 1 else (0.15, 0.15, 0.4),
                )
                y += fontsize + 10
            # Draw separator line under chapter titles
            if any(lv == 1 for lv, _ in page_titles[pg]):
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
                shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
                shape.commit()
                y += 15

        # Fill rest of page with body text
        para_idx = 0
        while y < 700:
            text = BODY_TEXTS[(pg + para_idx) % len(BODY_TEXTS)]
            rect = pymupdf.Rect(72, y, 540, y + 100)
            page.insert_textbox(
                rect, text,
                fontsize=11, fontname="tiro", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            y += 110
            para_idx += 1

        # Page number
        page.insert_text(
            pymupdf.Point(290, 770), str(pg),
            fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4),
        )

    # Set TOC (bookmarks)
    toc = [[level, title, page_num] for level, title, page_num in TOC_ENTRIES]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Efficient Neural Architecture Search with Adaptive Transfer Learning",
        "author": "Alexandra M. Rodriguez",
        "subject": "PhD Thesis - Department of Computer Science",
        "keywords": "neural architecture search, transfer learning, deep learning, NAS",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # NO viewer preferences set - task requires agent to set them
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 60')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
