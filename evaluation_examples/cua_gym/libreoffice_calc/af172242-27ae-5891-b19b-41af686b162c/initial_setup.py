"""
Initial Setup: PDF author extraction task
Task ID: osworld_multi_apps_pdf_author_extract_002
Domain: libreoffice_calc (multi-app: PDF + Calc)

Creates 5 realistic CV conference paper PDFs in ~/Documents/CV_Papers/
and opens Nautilus file manager showing that directory.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_002'
PAPERS_DIR = f'{WORKDIR}/Documents/CV_Papers'


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


def create_pdf_paper(filepath, title, conference, year, authors, affiliations, abstract):
    """Create a realistic-looking conference paper PDF using fpdf2."""
    from fpdf import FPDF

    pdf = FPDF(format='A4')
    pdf.add_page()
    # margins: left=25, top=20, right=25
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.set_top_margin(20)
    pdf.set_auto_page_break(auto=True, margin=20)

    def mc(h, txt, align="L"):
        """Helper: reset x to left margin before each multi_cell to avoid position drift."""
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, h, txt, align=align)

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_y(20)
    mc(8, title, align="C")
    pdf.ln(3)

    # Conference and year
    pdf.set_font("Helvetica", "I", 11)
    mc(6, f"{conference} {year}", align="C")
    pdf.ln(3)

    # Authors line
    author_line = ", ".join(authors)
    pdf.set_font("Helvetica", "B", 11)
    mc(6, author_line, align="C")
    pdf.ln(2)

    # Affiliations - each author with their affiliation
    pdf.set_font("Helvetica", "I", 10)
    for author, affil in zip(authors, affiliations):
        mc(5, f"{author}: {affil}", align="C")
    pdf.ln(6)

    # Abstract section
    pdf.set_font("Helvetica", "B", 11)
    mc(6, "Abstract")
    pdf.set_font("Helvetica", "", 10)
    mc(5, abstract)
    pdf.ln(6)

    # Introduction section
    pdf.set_font("Helvetica", "B", 11)
    mc(6, "1. Introduction")
    pdf.set_font("Helvetica", "", 10)
    intro_text = (
        "Computer vision has advanced significantly over recent years, driven by deep learning "
        "and large-scale datasets. In this work, we address a fundamental challenge in the field "
        "and propose a novel approach that achieves state-of-the-art results on multiple benchmarks. "
        "Our method builds on recent advances in neural network architectures and self-supervised "
        "learning, demonstrating strong generalization across diverse tasks and domains."
    )
    mc(5, intro_text)
    pdf.ln(4)

    # Method section
    pdf.set_font("Helvetica", "B", 11)
    mc(6, "2. Method")
    pdf.set_font("Helvetica", "", 10)
    method_text = (
        "Our proposed framework consists of three main components: a feature extraction backbone, "
        "an attention-based aggregation module, and a task-specific prediction head. "
        "The backbone processes input images at multiple scales, capturing both local and global "
        "features. The aggregation module uses multi-head self-attention to model relationships "
        "between spatial regions."
    )
    mc(5, method_text)
    pdf.ln(4)

    # References section
    pdf.set_font("Helvetica", "B", 11)
    mc(6, "References")
    pdf.set_font("Helvetica", "", 9)
    refs = [
        "[1] He et al.: Deep residual learning for image recognition. CVPR 2016.",
        "[2] Dosovitskiy et al.: An image is worth 16x16 words. ICLR 2021.",
        "[3] Radford et al.: Learning transferable visual models from natural language. ICML 2021.",
        "[4] Chen et al.: A simple framework for contrastive learning. ICML 2020.",
    ]
    for ref in refs:
        mc(5, ref)

    pdf.output(filepath)


def create_papers():
    """Create 5 CV conference paper PDFs with realistic author information."""
    os.makedirs(PAPERS_DIR, exist_ok=True)

    papers = [
        {
            "filename": "cvpr2023_dense_prediction.pdf",
            "title": "DenseFormer: Unified Dense Prediction via Transformer-Based Feature Aggregation",
            "conference": "CVPR",
            "year": 2023,
            "authors": ["Chen Wei", "Liu Yang", "Zhang Hao", "Wang Fang"],
            "affiliations": [
                "Peking University",
                "Tsinghua University",
                "Peking University",
                "Microsoft Research Asia",
            ],
            "abstract": (
                "Dense prediction tasks such as semantic segmentation, depth estimation, and surface "
                "normal prediction are fundamental to scene understanding. We present DenseFormer, "
                "a unified architecture that handles multiple dense prediction tasks within a single "
                "transformer-based framework. By leveraging cross-task feature sharing and a novel "
                "task-adaptive attention mechanism, DenseFormer achieves competitive results on "
                "ADE20K, NYU-Depth v2, and Cityscapes benchmarks while reducing computational "
                "overhead by 30% compared to task-specific models."
            ),
        },
        {
            "filename": "eccv2022_object_detection.pdf",
            "title": "Adaptive Anchor-Free Detection with Dynamic Query Refinement",
            "conference": "ECCV",
            "year": 2022,
            "authors": ["Emma Novak", "Thomas Fischer", "Maria Bauer", "Stefan Gruber"],
            "affiliations": [
                "ETH Zurich",
                "ETH Zurich",
                "Technical University of Munich",
                "Max Planck Institute for Intelligent Systems",
            ],
            "abstract": (
                "Modern object detection approaches rely on anchor-based or query-based paradigms, "
                "each with distinct trade-offs. We propose an adaptive anchor-free detector that "
                "dynamically refines detection queries based on multi-scale contextual features. "
                "Our method introduces a novel query refinement module that progressively improves "
                "localization accuracy. Experiments on COCO and Objects365 demonstrate "
                "state-of-the-art performance with significantly fewer parameters than competing "
                "approaches."
            ),
        },
        {
            "filename": "iccv2023_video_understanding.pdf",
            "title": "Temporal-Spatial Attention for Efficient Video Action Recognition",
            "conference": "ICCV",
            "year": 2023,
            "authors": ["Hiroshi Nakamura", "Yuki Tanaka", "Kenji Watanabe"],
            "affiliations": [
                "University of Tokyo",
                "Kyoto University",
                "University of Tokyo",
            ],
            "abstract": (
                "Video action recognition requires modeling complex temporal dynamics across many "
                "frames. Existing methods often trade computational efficiency for accuracy or fail "
                "to capture long-range temporal dependencies. We propose a Temporal-Spatial "
                "Attention (TSA) module that efficiently models both short-term motion and "
                "long-range context. Our lightweight architecture achieves 87.3% top-1 accuracy "
                "on Kinetics-400 while requiring only 60% of the FLOPs of competing methods."
            ),
        },
        {
            "filename": "cvpr2022_self_supervised.pdf",
            "title": "MOCO-v3: Robust Self-Supervised Representation Learning with Momentum Contrast",
            "conference": "CVPR",
            "year": 2022,
            "authors": ["James Mitchell", "Sarah O'Brien", "Kevin Park", "Lisa Nguyen"],
            "affiliations": [
                "Stanford University",
                "Stanford University",
                "Carnegie Mellon University",
                "University of California Berkeley",
            ],
            "abstract": (
                "Self-supervised learning has emerged as a powerful paradigm for visual "
                "representation learning without manual labels. We present an improved momentum "
                "contrast framework that addresses training instability and representation collapse "
                "in large-batch settings. Our method introduces an adaptive momentum schedule and "
                "a novel projection head architecture. Evaluated on ImageNet linear probing and "
                "downstream transfer tasks, our approach surpasses prior self-supervised methods."
            ),
        },
        {
            "filename": "eccv2022_3d_reconstruction.pdf",
            "title": "NeRF-Fusion: Real-Time Neural Radiance Field Reconstruction from RGB-D Streams",
            "conference": "ECCV",
            "year": 2022,
            "authors": ["Priya Sharma", "Rahul Gupta", "Ananya Krishnan"],
            "affiliations": [
                "Indian Institute of Technology Bombay",
                "Indian Institute of Technology Bombay",
                "Indian Institute of Science Bangalore",
            ],
            "abstract": (
                "Neural Radiance Fields (NeRF) have demonstrated remarkable quality for novel view "
                "synthesis but are typically slow to train and render, limiting real-time "
                "applications. We present NeRF-Fusion, an online reconstruction system that "
                "incrementally builds and updates a neural radiance field from streaming RGB-D "
                "data. By combining volumetric fusion with learned radiance modeling, our system "
                "achieves high-quality reconstruction with real-time performance at 25 fps."
            ),
        },
    ]

    for paper in papers:
        filepath = os.path.join(PAPERS_DIR, paper["filename"])
        create_pdf_paper(
            filepath=filepath,
            title=paper["title"],
            conference=paper["conference"],
            year=paper["year"],
            authors=paper["authors"],
            affiliations=paper["affiliations"],
            abstract=paper["abstract"],
        )
        print(f"Created: {filepath}")

    print(f"\nAll 5 PDF papers created in: {PAPERS_DIR}")
    print("\nFirst authors and affiliations (for reference):")
    for p in papers:
        print(f"  {p['authors'][0]} | {p['affiliations'][0]} | {p['filename']}")


def main():
    create_papers()

    # GUI-ready startup: open Nautilus file manager showing the Papers directory
    launch_gui(f'nautilus "{PAPERS_DIR}"', delay_sec=2.0)
    print(f'\nGUI_READY: Nautilus opened at {PAPERS_DIR}')


main()
