"""
Initial Setup: Batch process PDF metadata - create 8 submission PDFs with varied metadata
Task ID: pdf_mbc_035
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_035'
SUBMISSIONS_DIR = f'{WORKDIR}/Documents/submissions'

# Paper metadata - each with unique Author and Title
PAPERS = [
    {
        "filename": "paper1.pdf",
        "author": "Dr. Elena Vasquez",
        "title": "Neural Architecture Search for Edge Computing Applications",
        "abstract": (
            "This paper presents a novel approach to neural architecture search (NAS) "
            "specifically tailored for edge computing environments. We propose EdgeNAS, "
            "a hardware-aware search algorithm that jointly optimizes model accuracy and "
            "inference latency on resource-constrained devices. Our experiments on the "
            "ImageNet dataset demonstrate that EdgeNAS achieves a 2.3x speedup over "
            "existing methods while maintaining comparable top-1 accuracy of 76.8%. "
            "We evaluate our approach across multiple edge platforms including NVIDIA "
            "Jetson Nano, Raspberry Pi 4, and Google Coral Dev Board."
        ),
    },
    {
        "filename": "paper2.pdf",
        "author": "Prof. James Whitfield",
        "title": "Quantum Error Correction in Topological Superconductors",
        "abstract": (
            "We investigate the feasibility of topological quantum error correction "
            "using Majorana zero modes in hybrid semiconductor-superconductor nanowires. "
            "Our theoretical framework predicts a logical error rate below 10^-6 per "
            "gate cycle when operating at temperatures below 50 mK. We present detailed "
            "numerical simulations of a 17-qubit surface code implemented on a hexagonal "
            "lattice of topological qubits, demonstrating fault-tolerant operation under "
            "realistic noise models including quasiparticle poisoning and charge noise."
        ),
    },
    {
        "filename": "paper3.pdf",
        "author": "Dr. Mei-Ling Chen and Dr. Rajesh Patel",
        "title": "Sustainable Urban Microgrids: A Multi-Objective Optimization Framework",
        "abstract": (
            "Urban microgrids present unique challenges in balancing economic efficiency, "
            "environmental sustainability, and grid reliability. This paper introduces "
            "SUMO-Grid, a multi-objective optimization framework that integrates renewable "
            "energy forecasting, demand response modeling, and battery degradation dynamics. "
            "We validate our approach using real-world data from three metropolitan areas: "
            "Singapore, Barcelona, and Portland. Results show a 34% reduction in carbon "
            "emissions and 22% cost savings compared to conventional grid management "
            "strategies, while maintaining 99.97% supply reliability."
        ),
    },
    {
        "filename": "paper4.pdf",
        "author": "Dr. Amara Okonkwo",
        "title": "Explainable Deep Learning for Medical Image Diagnosis",
        "abstract": (
            "The deployment of deep learning models in clinical settings demands "
            "interpretability and transparency. We present MedXAI, an explainability "
            "framework that generates clinically meaningful visual and textual explanations "
            "for convolutional neural network predictions in radiology. Our approach "
            "combines gradient-weighted class activation mapping with a natural language "
            "generation module trained on 50,000 radiologist reports. In a study with "
            "42 board-certified radiologists, MedXAI explanations increased diagnostic "
            "confidence by 28% and reduced false positive rates by 15% for pulmonary "
            "nodule detection in chest CT scans."
        ),
    },
    {
        "filename": "paper5.pdf",
        "author": "Prof. Henrik Larsson",
        "title": "Bayesian Causal Discovery in High-Dimensional Genomic Data",
        "abstract": (
            "Identifying causal gene regulatory networks from observational transcriptomic "
            "data remains a fundamental challenge in computational biology. We propose "
            "BayesGenNet, a scalable Bayesian framework for causal structure learning that "
            "handles datasets with over 20,000 genes and complex confounding structures. "
            "Our method employs a variational inference scheme with a novel prior that "
            "encodes known pathway information from KEGG and Reactome databases. Applied "
            "to single-cell RNA sequencing data from human pancreatic islets, BayesGenNet "
            "recovers 73% of known regulatory interactions and predicts 12 novel "
            "interactions subsequently validated through CRISPR perturbation experiments."
        ),
    },
    {
        "filename": "paper6.pdf",
        "author": "Dr. Sofia Romanova",
        "title": "Adversarial Robustness in Federated Learning Systems",
        "abstract": (
            "Federated learning enables collaborative model training without sharing raw "
            "data, but remains vulnerable to adversarial attacks from malicious participants. "
            "This work presents FedShield, a Byzantine-robust aggregation protocol that "
            "combines spectral analysis of gradient updates with adaptive clipping mechanisms. "
            "We provide formal convergence guarantees under the assumption that fewer than "
            "30% of participants are adversarial. Experiments on CIFAR-100 and medical "
            "imaging benchmarks demonstrate that FedShield maintains model accuracy within "
            "1.2% of the non-adversarial baseline even when 25% of clients submit "
            "poisoned updates, outperforming Krum and coordinate-wise median by 8-14%."
        ),
    },
    {
        "filename": "paper7.pdf",
        "author": "Dr. Takeshi Yamamoto and Prof. Lisa Park",
        "title": "Real-Time Seismic Event Detection Using Graph Neural Networks",
        "abstract": (
            "Traditional seismic event detection methods rely on template matching and "
            "STA/LTA ratios, which struggle with low signal-to-noise scenarios common in "
            "volcanic and induced seismicity monitoring. We introduce SeisGNN, a graph "
            "neural network architecture that models seismic station networks as dynamic "
            "graphs, enabling spatiotemporal pattern recognition across distributed sensor "
            "arrays. Trained on 2.3 million labeled events from the Southern California "
            "Earthquake Data Center, SeisGNN achieves a detection rate of 96.4% for events "
            "above magnitude 0.5, with a false positive rate of 0.3 events per station per "
            "day. Processing latency is under 200 ms per event on a single GPU."
        ),
    },
    {
        "filename": "paper8.pdf",
        "author": "Prof. Catherine Dubois",
        "title": "Formal Verification of Distributed Consensus Protocols",
        "abstract": (
            "Distributed consensus protocols form the backbone of modern blockchain systems "
            "and distributed databases, yet subtle bugs can lead to catastrophic failures. "
            "We present ConsensusProof, an automated verification framework based on "
            "refinement types and temporal logic that can prove safety and liveness "
            "properties of consensus algorithms. We successfully verify correctness of "
            "Raft, PBFT, and HotStuff protocols, discovering two previously unknown edge "
            "cases in popular open-source implementations. Our framework handles message "
            "reordering, network partitions, and Byzantine faults, and scales to protocols "
            "with up to 100 participants through compositional reasoning techniques."
        ),
    },
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


def create_paper_pdf(filepath, author, title, abstract):
    """Create a realistic academic paper PDF with metadata."""
    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title (centered, large)
    title_rect = pymupdf.Rect(72, 120, 540, 220)
    page.insert_textbox(
        title_rect,
        title,
        fontsize=18,
        fontname="tibo",  # Times-Bold
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Author line
    author_rect = pymupdf.Rect(72, 240, 540, 270)
    page.insert_textbox(
        author_rect,
        author,
        fontsize=12,
        fontname="tiit",  # Times-Italic
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Date line
    date_rect = pymupdf.Rect(72, 280, 540, 300)
    page.insert_textbox(
        date_rect,
        "Submitted: March 2026",
        fontsize=10,
        fontname="tiro",
        color=(0.4, 0.4, 0.4),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Abstract heading
    page.insert_text(
        pymupdf.Point(72, 360),
        "Abstract",
        fontsize=14,
        fontname="tibo",
        color=(0, 0, 0),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 368), pymupdf.Point(540, 368))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    # Abstract text
    abstract_rect = pymupdf.Rect(72, 380, 540, 650)
    page.insert_textbox(
        abstract_rect,
        abstract,
        fontsize=10,
        fontname="tiro",  # Times-Roman
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Keywords
    page.insert_text(
        pymupdf.Point(72, 680),
        "Keywords: ",
        fontsize=9,
        fontname="tibo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(130, 680),
        "machine learning, optimization, computational methods",
        fontsize=9,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )

    # Page 2: Introduction section placeholder
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "1. Introduction",
        fontsize=14,
        fontname="tibo",
        color=(0, 0, 0),
    )
    intro_rect = pymupdf.Rect(72, 92, 540, 400)
    page2.insert_textbox(
        intro_rect,
        (
            "The rapid advancement of computational methods has created new opportunities "
            "for addressing complex problems in science and engineering. In this paper, we "
            "build upon recent developments in the field to propose a novel methodology "
            "that significantly improves upon the state of the art. Our approach is motivated "
            "by the observation that existing techniques often fail to account for the "
            "intricate dependencies present in real-world data. We address this limitation "
            "through a principled framework that combines theoretical rigor with practical "
            "efficiency. The remainder of this paper is organized as follows: Section 2 "
            "reviews related work, Section 3 describes our methodology, Section 4 presents "
            "experimental results, and Section 5 concludes with directions for future research."
        ),
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page2.insert_text(
        pymupdf.Point(72, 420),
        "2. Related Work",
        fontsize=14,
        fontname="tibo",
        color=(0, 0, 0),
    )
    related_rect = pymupdf.Rect(72, 440, 540, 700)
    page2.insert_textbox(
        related_rect,
        (
            "Several prior studies have explored various aspects of this problem domain. "
            "Smith et al. (2023) proposed an initial framework that demonstrated promising "
            "results on synthetic benchmarks but did not scale effectively to larger datasets. "
            "Johnson and Williams (2024) extended this work by incorporating attention-based "
            "mechanisms, achieving improved performance on standardized evaluation metrics. "
            "More recently, Zhang et al. (2025) introduced a hybrid approach combining "
            "classical optimization with learned representations, setting new benchmarks "
            "on several widely-used datasets. Our work differs from these approaches in "
            "its principled treatment of uncertainty quantification and its ability to "
            "handle heterogeneous data sources within a unified framework."
        ),
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set metadata
    doc.set_metadata({
        "title": title,
        "author": author,
        "subject": "Academic Submission",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    doc.save(filepath)
    doc.close()


def create_initial():
    # Create submissions directory
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

    # Ensure submissions_anon does NOT exist
    anon_dir = f'{WORKDIR}/Documents/submissions_anon'
    if os.path.exists(anon_dir):
        import shutil
        shutil.rmtree(anon_dir)

    # Create each paper PDF
    for paper in PAPERS:
        filepath = os.path.join(SUBMISSIONS_DIR, paper["filename"])
        create_paper_pdf(filepath, paper["author"], paper["title"], paper["abstract"])
        print(f'Created: {filepath}')

    print(f'\nAll 8 submission PDFs created in {SUBMISSIONS_DIR}')

    # Open file manager to show the submissions directory
    launch_gui(f'nautilus "{SUBMISSIONS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
