"""
Initial Setup: Reorder bookmarks in conference proceedings PDF
Task ID: pdf_mbc_041
Domain: pdf

Creates a multi-page proceedings PDF with bookmarks in the WRONG order:
  Session B (page 15), Closing Remarks (page 50), Session A (page 8),
  Keynote Address (page 1), Session C (page 30)
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/proceedings.pdf'

# Bookmark structure - WRONG ORDER (this is what the agent must fix)
WRONG_ORDER_TOC = [
    [1, "Session B", 15],
    [1, "Closing Remarks", 50],
    [1, "Session A", 8],
    [1, "Keynote Address", 1],
    [1, "Session C", 30],
]

# Section content for realistic pages
SECTIONS = {
    1: ("Keynote Address", "Advancing the Frontiers of Distributed Computing",
        "Dr. Elena Vasquez, MIT Computer Science and Artificial Intelligence Laboratory"),
    8: ("Session A: Machine Learning", "Scalable Approaches to Neural Architecture Search",
        "Papers presented in this session focus on efficient methods for automated ML model design."),
    15: ("Session B: Systems and Networking", "Low-Latency Consensus Protocols for Edge Computing",
         "This session explores novel systems-level optimizations for distributed environments."),
    30: ("Session C: Security and Privacy", "Differential Privacy in Federated Learning Pipelines",
         "Contributions in this session address critical challenges in preserving user privacy."),
    50: ("Closing Remarks", "Summary and Future Directions",
         "Prof. Marcus Chen, Conference General Chair, Stanford University"),
}

# Filler talk titles for other pages
FILLER_TALKS = [
    "Optimizing Memory Allocation in Serverless Functions",
    "Graph Neural Networks for Protein Folding Prediction",
    "Robust Adversarial Training with Data Augmentation",
    "Efficient Query Processing over Streaming Data",
    "Privacy-Preserving Record Linkage at Scale",
    "Compiler Optimizations for Heterogeneous Architectures",
    "Multi-Agent Reinforcement Learning in Dynamic Environments",
    "Causal Inference for Treatment Effect Estimation",
    "Blockchain-Based Supply Chain Verification",
    "Attention Mechanisms for Long Document Summarization",
    "Secure Multi-Party Computation with Honest Majority",
    "Adaptive Load Balancing in Microservice Architectures",
    "Zero-Shot Cross-Lingual Transfer Learning",
    "Quantum Error Correction with Surface Codes",
    "Real-Time Object Detection on Resource-Constrained Devices",
    "Automated Theorem Proving with Transformer Models",
    "Decentralized Identity Management Systems",
    "Continual Learning without Catastrophic Forgetting",
    "Energy-Efficient Training of Large Language Models",
    "Fairness-Aware Recommendation Systems",
]


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()
    total_pages = 55  # enough to cover all sections including page 50

    # Create all pages
    for i in range(total_pages):
        page_num = i + 1  # 1-indexed
        page = doc.new_page(width=595, height=842)  # A4

        if page_num in SECTIONS:
            # Section title page
            title, subtitle, description = SECTIONS[page_num]

            # Draw a header bar
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(0, 0, 595, 80))
            shape.finish(fill=(0.1, 0.2, 0.4))  # dark blue
            shape.commit()

            # Conference name in header
            page.insert_text(
                pymupdf.Point(72, 50),
                "ICDCS 2025 - International Conference on Distributed Computing Systems",
                fontsize=10, fontname="helv", color=(1, 1, 1),
            )

            # Section title
            page.insert_text(
                pymupdf.Point(72, 140),
                title,
                fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.4),
            )

            # Horizontal rule
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(72, 155), pymupdf.Point(523, 155))
            shape2.finish(color=(0.1, 0.2, 0.4), width=2)
            shape2.commit()

            # Subtitle
            page.insert_text(
                pymupdf.Point(72, 190),
                subtitle,
                fontsize=14, fontname="tiit", color=(0.3, 0.3, 0.3),
            )

            # Description
            rect = pymupdf.Rect(72, 230, 523, 400)
            page.insert_textbox(
                rect, description,
                fontsize=12, fontname="helv", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

            # Page number footer
            page.insert_text(
                pymupdf.Point(280, 810),
                str(page_num),
                fontsize=10, fontname="helv", color=(0.5, 0.5, 0.5),
            )

        else:
            # Regular content page with filler talk
            talk_idx = (page_num - 2) % len(FILLER_TALKS)

            # Header line
            page.insert_text(
                pymupdf.Point(72, 40),
                "ICDCS 2025 Proceedings",
                fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5),
            )
            shape3 = page.new_shape()
            shape3.draw_line(pymupdf.Point(72, 48), pymupdf.Point(523, 48))
            shape3.finish(color=(0.8, 0.8, 0.8), width=0.5)
            shape3.commit()

            # Talk title
            page.insert_text(
                pymupdf.Point(72, 90),
                FILLER_TALKS[talk_idx],
                fontsize=14, fontname="hebo", color=(0, 0, 0),
            )

            # Fake authors
            authors = [
                "A. Williams, B. Nakamura, C. Okafor",
                "D. Petrov, E. Garcia, F. Liu",
                "G. Andersen, H. Patel, I. Schmidt",
                "J. Kim, K. Bjornsson, L. Santos",
            ]
            page.insert_text(
                pymupdf.Point(72, 115),
                authors[talk_idx % len(authors)],
                fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3),
            )

            # Abstract content
            abstract = (
                "Abstract -- We present a novel approach to the problem described above. "
                "Our method achieves state-of-the-art results on multiple benchmark datasets, "
                "demonstrating significant improvements over existing baselines. "
                "Through extensive experiments we show that our technique scales efficiently "
                "to large real-world problem instances while maintaining theoretical guarantees. "
                "We provide a formal analysis of the computational complexity and discuss "
                "practical implications for deployment in production environments. "
                "Our contributions include (1) a new algorithmic framework, (2) rigorous "
                "theoretical analysis, and (3) comprehensive empirical evaluation across "
                "diverse settings including both synthetic and real-world datasets."
            )
            rect = pymupdf.Rect(72, 145, 523, 780)
            page.insert_textbox(
                rect, abstract,
                fontsize=11, fontname="helv", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

            # Page number
            page.insert_text(
                pymupdf.Point(280, 810),
                str(page_num),
                fontsize=10, fontname="helv", color=(0.5, 0.5, 0.5),
            )

    # Set bookmarks in WRONG order
    doc.set_toc(WRONG_ORDER_TOC)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
