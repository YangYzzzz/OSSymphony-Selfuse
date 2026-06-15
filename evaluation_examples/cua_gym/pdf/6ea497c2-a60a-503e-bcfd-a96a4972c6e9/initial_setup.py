"""
Initial Setup: Create untagged thesis abstract PDF
Task ID: pdf_res_077
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_077'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/thesis_abstract.pdf'

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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # === Page 1 ===
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title (H1 candidate) - centered, large, bold
    title = "Adaptive Neural Architecture Search for Resource-Constrained Edge Deployment"
    title_y = 72
    page1.insert_text(
        pymupdf.Point(306, title_y),
        title,
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    # Title is long, wrap manually
    rect_title = pymupdf.Rect(72, 50, 540, 110)
    page1.insert_textbox(
        rect_title,
        title,
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Author line
    page1.insert_textbox(
        pymupdf.Rect(72, 115, 540, 140),
        "Elena Vasquez, Department of Computer Science, Stanford University",
        fontsize=10,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # Section 1 heading (H2 candidate)
    section1_y = 170
    page1.insert_text(
        pymupdf.Point(72, section1_y),
        "1. Introduction and Motivation",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Body paragraph 1
    intro_text = (
        "The proliferation of Internet of Things (IoT) devices and mobile platforms has created "
        "an urgent demand for neural network architectures that can operate effectively within "
        "stringent computational budgets. Traditional neural architecture search (NAS) methods, "
        "while achieving impressive accuracy on benchmark datasets, frequently produce models "
        "that exceed the memory and latency constraints imposed by edge hardware. This "
        "dissertation presents a novel framework for adaptive neural architecture search that "
        "explicitly incorporates hardware-aware constraints during the search process, enabling "
        "the discovery of architectures optimized for deployment on resource-constrained devices."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 185, 540, 340),
        intro_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    intro_text2 = (
        "Our approach builds upon the differentiable architecture search paradigm introduced by "
        "Liu et al. (2019) but extends it with a multi-objective optimization strategy that "
        "balances classification accuracy against inference latency, peak memory consumption, "
        "and energy expenditure. By formulating the search as a constrained optimization problem "
        "with Pareto-optimal trade-offs, we enable practitioners to select architectures that "
        "best match their specific deployment requirements without rerunning the search procedure."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 345, 540, 490),
        intro_text2,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 2 heading (H2 candidate)
    page1.insert_text(
        pymupdf.Point(72, 515),
        "2. Methodology",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Body paragraph for methodology
    method_text = (
        "The proposed framework operates in three phases. In the first phase, a supernet "
        "encompassing a diverse set of candidate operations is trained using gradient-based "
        "optimization on a proxy dataset. Each edge in the supernet's directed acyclic graph "
        "is associated with a continuous architecture parameter that controls operation selection. "
        "The second phase introduces hardware-aware penalty terms derived from latency lookup "
        "tables calibrated on the target device. These penalty terms are incorporated into the "
        "loss function as Lagrangian multipliers, steering the search toward architectures that "
        "satisfy the specified constraints."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 530, 540, 700),
        method_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page1.insert_text(
        pymupdf.Point(296, 770),
        "1",
        fontsize=10,
        fontname="tiro",
        color=(0.5, 0.5, 0.5),
    )

    # === Page 2 ===
    page2 = doc.new_page(width=612, height=792)

    method_text2 = (
        "In the third phase, the discovered architecture undergoes knowledge distillation from "
        "a larger teacher network to further improve its accuracy without increasing computational "
        "cost. We employ a progressive shrinking strategy that gradually reduces the supernet "
        "capacity, allowing finer-grained exploration of the architecture space near the "
        "constraint boundaries. The entire pipeline is automated and requires minimal human "
        "intervention beyond specifying the target hardware profile and acceptable accuracy-latency "
        "trade-off range."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 50, 540, 195),
        method_text2,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 3 heading (H2 candidate)
    page2.insert_text(
        pymupdf.Point(72, 225),
        "3. Results and Contributions",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    results_text = (
        "Extensive experiments on ImageNet, CIFAR-100, and a custom industrial defect detection "
        "dataset demonstrate that architectures discovered by our framework achieve accuracy within "
        "0.3% of state-of-the-art NAS methods while requiring 40-60% fewer FLOPs and 35-50% less "
        "peak memory. On an NVIDIA Jetson Nano, the discovered models achieve real-time inference "
        "at 30 frames per second for 224x224 input resolution, compared to 12 FPS for "
        "EfficientNet-B0 and 8 FPS for MobileNetV3-Large. The search process itself completes "
        "in under 4 GPU-hours on a single NVIDIA A100, representing a 3x speedup over comparable "
        "hardware-aware NAS approaches."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 240, 540, 420),
        results_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    results_text2 = (
        "The principal contributions of this dissertation are threefold. First, we introduce a "
        "differentiable hardware-aware search space that directly encodes device constraints as "
        "differentiable penalty terms. Second, we propose a progressive shrinking strategy that "
        "improves search efficiency by an order of magnitude compared to uniform sampling "
        "approaches. Third, we provide an open-source toolkit, EdgeNASBench, containing "
        "pre-calibrated latency tables for twelve popular edge devices, enabling reproducible "
        "and comparable hardware-aware NAS research. These contributions collectively advance "
        "the practical applicability of neural architecture search for real-world edge deployment "
        "scenarios where computational resources are fundamentally limited."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 425, 540, 620),
        results_text2,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page2.insert_text(
        pymupdf.Point(296, 770),
        "2",
        fontsize=10,
        fontname="tiro",
        color=(0.5, 0.5, 0.5),
    )

    # Save WITHOUT any structure tags
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify no structure tags exist
    doc_check = pymupdf.open(OUTPUT)
    catalog = doc_check.pdf_catalog()
    xref_str = doc_check.xref_object(catalog)
    has_struct = "StructTreeRoot" in xref_str
    doc_check.close()
    print(f'StructTreeRoot present: {has_struct} (should be False)')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
