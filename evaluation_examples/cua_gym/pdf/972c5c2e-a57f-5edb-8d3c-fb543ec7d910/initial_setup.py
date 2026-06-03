"""
Initial Setup: Create a 4-page A3-sized PDF poster document.
Task ID: pdf_fm_070
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/a3_poster.pdf'

# A3 dimensions in points (297mm x 420mm)
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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title / Cover ---
    page = doc.new_page(width=A3_WIDTH, height=A3_HEIGHT)
    # Title
    page.insert_text(
        pymupdf.Point(120, 200),
        "Annual Research Symposium 2025",
        fontsize=42,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    # Subtitle
    page.insert_text(
        pymupdf.Point(120, 280),
        "Exploring Frontiers in Computational Biology",
        fontsize=24,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )
    # Authors
    page.insert_text(
        pymupdf.Point(120, 360),
        "Dr. Elena Vasquez, Prof. Kenji Tanaka, Dr. Amara Osei",
        fontsize=18,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    # Institution
    page.insert_text(
        pymupdf.Point(120, 410),
        "Institute for Advanced Computational Sciences",
        fontsize=16,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(120, 440),
        "University of Cambridge",
        fontsize=16,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(120, 470), pymupdf.Point(720, 470))
    shape.finish(color=(0.1, 0.15, 0.4), width=3)
    shape.commit()
    # Abstract box
    rect = pymupdf.Rect(120, 520, 720, 800)
    page.insert_textbox(
        rect,
        "Abstract: This poster presents our latest findings on protein folding prediction "
        "using deep reinforcement learning architectures. We demonstrate a 34% improvement "
        "in prediction accuracy over existing methods when applied to membrane-bound protein "
        "complexes. Our approach combines graph neural networks with attention mechanisms "
        "to capture long-range amino acid interactions that traditional convolutional methods "
        "miss. We validated our results on the CASP15 benchmark dataset, achieving state-of-the-art "
        "performance on 78% of target structures. These results have significant implications "
        "for drug discovery pipelines and personalized medicine applications.",
        fontsize=16,
        fontname="helv",
        color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Conference info at bottom
    page.insert_text(
        pymupdf.Point(120, 1050),
        "International Conference on Computational Biology | March 15-18, 2025 | Geneva, Switzerland",
        fontsize=14,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    # --- Page 2: Methods ---
    page = doc.new_page(width=A3_WIDTH, height=A3_HEIGHT)
    page.insert_text(
        pymupdf.Point(80, 100),
        "Methods & Experimental Design",
        fontsize=36,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(80, 120), pymupdf.Point(760, 120))
    shape.finish(color=(0.8, 0.2, 0.2), width=2)
    shape.commit()

    methods_text = (
        "1. Data Collection & Preprocessing\n\n"
        "We collected 12,847 protein structures from the Protein Data Bank (PDB), "
        "filtering for resolution better than 2.5 Angstroms. Each structure was "
        "preprocessed using our custom pipeline:\n\n"
        "  - Backbone atom extraction (N, CA, C, O)\n"
        "  - Side-chain torsion angle computation\n"
        "  - Contact map generation at 8A threshold\n"
        "  - Multiple sequence alignment via HHblits\n\n"
        "2. Model Architecture\n\n"
        "Our model employs a dual-branch architecture:\n\n"
        "  Branch A: Graph Neural Network (6 layers, 256 hidden units)\n"
        "  Branch B: Transformer Encoder (8 heads, 512 dim)\n\n"
        "Both branches process the same input features but capture different "
        "structural relationships. The outputs are fused through a learned "
        "attention gate before the final distance prediction head.\n\n"
        "3. Training Protocol\n\n"
        "  - Optimizer: AdamW (lr=3e-4, weight_decay=0.01)\n"
        "  - Batch size: 32 proteins\n"
        "  - Training epochs: 150\n"
        "  - Loss function: Smooth L1 + Cross-entropy (alpha=0.7)\n"
        "  - Hardware: 8x NVIDIA A100 GPUs\n"
        "  - Training time: ~72 hours\n\n"
        "4. Evaluation Metrics\n\n"
        "  - GDT-TS (Global Distance Test - Total Score)\n"
        "  - TM-score (Template Modeling score)\n"
        "  - lDDT (local Distance Difference Test)\n"
        "  - RMSD (Root Mean Square Deviation)\n"
    )
    rect = pymupdf.Rect(80, 160, 760, 1100)
    page.insert_textbox(rect, methods_text, fontsize=14, fontname="helv",
                        color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    # --- Page 3: Results ---
    page = doc.new_page(width=A3_WIDTH, height=A3_HEIGHT)
    page.insert_text(
        pymupdf.Point(80, 100),
        "Results & Analysis",
        fontsize=36,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(80, 120), pymupdf.Point(760, 120))
    shape.finish(color=(0.8, 0.2, 0.2), width=2)
    shape.commit()

    results_text = (
        "Performance Comparison on CASP15 Benchmark\n\n"
        "Our method (DeepFold-RL) achieves the following scores:\n\n"
        "  Model              GDT-TS    TM-score   lDDT     RMSD\n"
        "  ---------------------------------------------------------\n"
        "  AlphaFold2          0.847     0.891     0.823    1.42\n"
        "  RoseTTAFold         0.812     0.856     0.798    1.67\n"
        "  ESMFold             0.831     0.874     0.811    1.53\n"
        "  DeepFold-RL (Ours)  0.892     0.923     0.867    1.08\n\n"
        "Key Findings:\n\n"
        "1. Our model shows the largest improvement on membrane proteins "
        "(+12.3% GDT-TS vs AlphaFold2), where traditional methods struggle "
        "due to the hydrophobic core interactions.\n\n"
        "2. The attention gate mechanism contributes 8.7% of the total "
        "improvement, as demonstrated by ablation studies.\n\n"
        "3. Graph neural network branch alone outperforms the transformer "
        "branch by 3.2% on single-domain proteins but underperforms by "
        "1.8% on multi-domain complexes.\n\n"
        "4. Inference time is 2.3 seconds per protein on a single GPU, "
        "making it suitable for high-throughput screening applications.\n\n"
        "5. Cross-validation (5-fold) shows consistent performance with "
        "standard deviation < 0.015 across all metrics.\n"
    )
    rect = pymupdf.Rect(80, 160, 760, 1100)
    page.insert_textbox(rect, results_text, fontsize=14, fontname="helv",
                        color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    # --- Page 4: Conclusions ---
    page = doc.new_page(width=A3_WIDTH, height=A3_HEIGHT)
    page.insert_text(
        pymupdf.Point(80, 100),
        "Conclusions & Future Work",
        fontsize=36,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(80, 120), pymupdf.Point(760, 120))
    shape.finish(color=(0.8, 0.2, 0.2), width=2)
    shape.commit()

    conclusions_text = (
        "Conclusions\n\n"
        "We have presented DeepFold-RL, a novel hybrid architecture that "
        "combines graph neural networks with transformer encoders for protein "
        "structure prediction. Our method achieves state-of-the-art results "
        "on the CASP15 benchmark, with particularly strong performance on "
        "membrane-bound protein complexes.\n\n"
        "The key innovation is the learned attention gate that dynamically "
        "balances local (GNN) and global (Transformer) structural features "
        "based on the input protein characteristics.\n\n"
        "Future Directions\n\n"
        "  1. Extension to protein-ligand binding prediction\n"
        "  2. Integration with molecular dynamics simulations\n"
        "  3. Application to de novo protein design\n"
        "  4. Scaling to protein complexes with >5000 residues\n"
        "  5. Development of uncertainty quantification methods\n\n"
        "References\n\n"
        "  [1] Jumper et al. Nature 596, 583-589 (2021)\n"
        "  [2] Baek et al. Science 373, 871-876 (2021)\n"
        "  [3] Lin et al. Science 379, 1123-1130 (2023)\n"
        "  [4] Abramson et al. Nature 630, 493-500 (2024)\n\n"
        "Acknowledgments\n\n"
        "This work was supported by the European Research Council (ERC) under "
        "grant agreement No. 834756, and the Cambridge Trust. Computing resources "
        "were provided by the Cambridge Service for Data Driven Discovery (CSD3).\n\n"
        "Contact: e.vasquez@cam.ac.uk | k.tanaka@cam.ac.uk | a.osei@cam.ac.uk\n"
    )
    rect = pymupdf.Rect(80, 160, 760, 1100)
    page.insert_textbox(rect, conclusions_text, fontsize=14, fontname="helv",
                        color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    doc = pymupdf.open(OUTPUT)
    print(f'Page count: {doc.page_count}')
    for i in range(doc.page_count):
        p = doc[i]
        print(f'Page {i}: {p.rect.width:.1f} x {p.rect.height:.1f} pts')
    doc.close()

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
