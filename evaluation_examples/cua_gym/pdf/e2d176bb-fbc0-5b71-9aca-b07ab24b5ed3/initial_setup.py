"""
Initial Setup: Create a 7-page academic paper PDF with a figure on page 3.
Task ID: pdf_res_083
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/highlight_region.pdf'


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

    # --- Page dimensions (Letter size) ---
    W, H = 612, 792

    # --- Common styling ---
    title_font = "hebo"
    body_font = "helv"
    heading_font = "hebo"

    # ===== PAGE 1: Title page =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "Adaptive Neural Architecture Search for",
                     fontsize=18, fontname=title_font, color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 145), "Resource-Constrained Edge Deployment",
                     fontsize=18, fontname=title_font, color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 190), "Elena Vasquez, Rajesh Patel, Yuki Tanaka, and Samuel Okonkwo",
                     fontsize=11, fontname="heit", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 215), "Department of Computer Science, Westfield Institute of Technology",
                     fontsize=10, fontname=body_font, color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 230), "Correspondence: evasquez@westfield.edu",
                     fontsize=10, fontname=body_font, color=(0.3, 0.3, 0.3))

    # Abstract
    page.insert_text(pymupdf.Point(72, 280), "Abstract", fontsize=13, fontname=heading_font, color=(0, 0, 0))
    abstract = (
        "We present AdaptNAS, a novel framework for neural architecture search that explicitly "
        "optimizes for deployment on resource-constrained edge devices. Unlike prior NAS methods "
        "that primarily target accuracy, our approach jointly optimizes latency, memory footprint, "
        "and energy consumption alongside task performance. Through a hierarchical search strategy "
        "combined with hardware-aware predictors, AdaptNAS discovers architectures that achieve "
        "94.2% of state-of-the-art accuracy while reducing inference latency by 3.7x and memory "
        "usage by 2.1x on ARM Cortex-M7 microcontrollers. We validate our approach across image "
        "classification, keyword spotting, and anomaly detection benchmarks."
    )
    page.insert_textbox(pymupdf.Rect(72, 300, 540, 450), abstract,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Keywords
    page.insert_text(pymupdf.Point(72, 470), "Keywords: ", fontsize=10, fontname=heading_font, color=(0, 0, 0))
    page.insert_text(pymupdf.Point(130, 470),
                     "neural architecture search, edge computing, model compression, hardware-aware optimization",
                     fontsize=10, fontname="heit", color=(0.2, 0.2, 0.2))

    # ===== PAGE 2: Introduction =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "1  Introduction", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    intro_text = (
        "The proliferation of Internet of Things (IoT) devices has created an urgent demand for "
        "efficient deep learning models that can operate within severe computational constraints. "
        "Modern edge devices, such as ARM Cortex-M series microcontrollers, typically feature less "
        "than 1 MB of SRAM and limited flash storage, making it infeasible to deploy conventional "
        "deep neural networks directly.\n\n"
        "Neural Architecture Search (NAS) has emerged as a promising paradigm for automatically "
        "designing efficient network architectures. However, most existing NAS frameworks optimize "
        "primarily for accuracy on powerful GPU hardware, producing architectures that remain too "
        "large for truly constrained edge devices. Recent hardware-aware NAS methods incorporate "
        "latency constraints but often rely on simplified latency models that do not capture the "
        "complex memory hierarchy and instruction pipeline behavior of real microcontrollers.\n\n"
        "In this paper, we propose AdaptNAS, a multi-objective architecture search framework that "
        "addresses these limitations through three key contributions:\n\n"
        "  (1) A hierarchical search space that decomposes architecture decisions into macro-level "
        "topology and micro-level operator choices, reducing the search complexity by 47%.\n\n"
        "  (2) Hardware-aware surrogate predictors trained on over 15,000 architecture-measurement "
        "pairs collected from physical edge devices, achieving a Kendall tau correlation of 0.93.\n\n"
        "  (3) A Pareto-guided evolutionary strategy that efficiently navigates the multi-objective "
        "landscape to produce a diverse set of architectures spanning different accuracy-efficiency "
        "trade-off points."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 750), intro_text,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ===== PAGE 3: Methodology (with figure in region 50,200 - 550,400) =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "2  Methodology", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    method_text_top = (
        "Our framework operates in three phases: search space definition, surrogate-assisted search, "
        "and fine-tuning. We describe each phase in detail below."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 140), method_text_top,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Draw a figure placeholder in the region (50, 200, 550, 400)
    # This represents the important figure that needs the blue overlay
    shape = page.new_shape()

    # Figure border
    fig_rect = pymupdf.Rect(50, 200, 550, 400)
    shape.draw_rect(fig_rect)
    shape.finish(color=(0.6, 0.6, 0.6), width=1)

    # Inner content: architecture diagram with boxes and arrows
    # Search space box
    shape.draw_rect(pymupdf.Rect(70, 220, 180, 270))
    shape.finish(color=(0.3, 0.3, 0.3), fill=(0.92, 0.95, 0.98), width=1)

    # Surrogate predictor box
    shape.draw_rect(pymupdf.Rect(220, 220, 370, 270))
    shape.finish(color=(0.3, 0.3, 0.3), fill=(0.95, 0.92, 0.92), width=1)

    # Evolutionary optimizer box
    shape.draw_rect(pymupdf.Rect(410, 220, 535, 270))
    shape.finish(color=(0.3, 0.3, 0.3), fill=(0.92, 0.98, 0.92), width=1)

    # Arrows between boxes
    shape.draw_line(pymupdf.Point(180, 245), pymupdf.Point(220, 245))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.draw_line(pymupdf.Point(370, 245), pymupdf.Point(410, 245))
    shape.finish(color=(0, 0, 0), width=1.5)

    # Hardware measurement feedback loop
    shape.draw_rect(pymupdf.Rect(200, 310, 390, 360))
    shape.finish(color=(0.3, 0.3, 0.3), fill=(0.98, 0.98, 0.90), width=1)

    # Vertical arrows
    shape.draw_line(pymupdf.Point(295, 270), pymupdf.Point(295, 310))
    shape.finish(color=(0, 0, 0), width=1, dashes="[3 3]")
    shape.draw_line(pymupdf.Point(470, 270), pymupdf.Point(470, 335))
    shape.finish(color=(0, 0, 0), width=1, dashes="[3 3]")
    shape.draw_line(pymupdf.Point(390, 335), pymupdf.Point(470, 335))
    shape.finish(color=(0, 0, 0), width=1, dashes="[3 3]")

    shape.commit()

    # Labels inside boxes
    page.insert_text(pymupdf.Point(80, 250), "Search Space", fontsize=9, fontname=body_font, color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(237, 242), "Surrogate", fontsize=9, fontname=body_font, color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(237, 258), "Predictor", fontsize=9, fontname=body_font, color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(420, 250), "Evolutionary", fontsize=9, fontname=body_font, color=(0.1, 0.1, 0.1))
    page.insert_text(pymupdf.Point(222, 340), "HW Measurement", fontsize=9, fontname=body_font, color=(0.1, 0.1, 0.1))

    # Figure caption
    page.insert_text(pymupdf.Point(120, 390), "Figure 1: AdaptNAS Framework Overview",
                     fontsize=9, fontname="heit", color=(0.2, 0.2, 0.2))

    # Text below figure
    method_text_bottom = (
        "2.1  Search Space Design\n\n"
        "We define a hierarchical search space S = (T, O) where T represents the macro-level "
        "topology decisions and O encodes the micro-level operator choices. The topology T specifies "
        "the number of stages, downsampling locations, and skip connections. Within each stage, operator "
        "choices O include depthwise separable convolutions with kernel sizes {3, 5, 7}, inverted residual "
        "blocks with expansion ratios {2, 4, 6}, and squeeze-and-excitation modules.\n\n"
        "2.2  Surrogate-Assisted Search\n\n"
        "Direct evaluation of candidate architectures on physical hardware is prohibitively expensive. "
        "We train a gradient-boosted decision tree ensemble as a surrogate predictor for each hardware "
        "metric. The training set comprises 15,247 architecture-measurement pairs collected from three "
        "target platforms: ARM Cortex-M7 (STM32H7), RISC-V (ESP32-C3), and a low-power FPGA (Lattice iCE40)."
    )
    page.insert_textbox(pymupdf.Rect(72, 420, 540, 750), method_text_bottom,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ===== PAGE 4: Experiments =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "3  Experiments", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    exp_text = (
        "We evaluate AdaptNAS on three benchmark tasks spanning different application domains:\n\n"
        "Image Classification: We use CIFAR-10 and a subset of ImageNet (ImageNet-100) as benchmarks. "
        "Models are evaluated on classification accuracy, inference latency, and peak memory usage.\n\n"
        "Keyword Spotting: Using the Google Speech Commands v2 dataset, we target 12-class keyword "
        "recognition suitable for always-on voice interfaces.\n\n"
        "Anomaly Detection: We employ the MIMII dataset for industrial acoustic anomaly detection, "
        "measuring the area under ROC curve (AUC) alongside deployment metrics.\n\n"
        "3.1  Implementation Details\n\n"
        "The evolutionary search runs for 500 generations with a population size of 100. We use "
        "NSGA-II for multi-objective optimization with three objectives: task performance, latency, "
        "and memory footprint. The surrogate predictors are retrained every 50 generations using "
        "the accumulated architecture pool. Search takes approximately 8 GPU-hours on a single "
        "NVIDIA A100.\n\n"
        "3.2  Baseline Comparisons\n\n"
        "We compare against the following baselines:\n\n"
        "  - MnasNet: Mobile NAS with latency-aware search\n"
        "  - MCUNet: Two-stage NAS for microcontrollers\n"
        "  - MicroNets: Differentiable NAS with memory constraints\n"
        "  - EfficientNet-Lite: Scaled-down EfficientNet variants\n"
        "  - Manual Expert Design: Hand-crafted architectures by domain experts\n\n"
        "All baselines are retrained under identical conditions using the same training schedule "
        "and data augmentation policies to ensure fair comparison."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 750), exp_text,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ===== PAGE 5: Results =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4  Results", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    results_text = (
        "Table 1 presents the main results on CIFAR-10 and ImageNet-100 benchmarks. AdaptNAS "
        "consistently discovers architectures that achieve competitive accuracy while significantly "
        "reducing inference latency and memory consumption.\n\n"
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 140), results_text,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Draw a results table
    page.insert_text(pymupdf.Point(160, 165), "Table 1: CIFAR-10 Classification Results",
                     fontsize=9, fontname="heit", color=(0.2, 0.2, 0.2))

    # Table headers and data
    table_y = 180
    headers = ["Method", "Acc (%)", "Latency (ms)", "Memory (KB)", "Params (K)"]
    col_x = [80, 200, 290, 390, 490]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], table_y), h, fontsize=9, fontname=heading_font, color=(0, 0, 0))

    # Draw header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, table_y + 5), pymupdf.Point(540, table_y + 5))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    rows = [
        ["MnasNet", "91.3", "45.2", "384", "312"],
        ["MCUNet", "92.8", "38.7", "320", "287"],
        ["MicroNets", "91.7", "41.3", "298", "256"],
        ["EfficientNet-Lite", "93.1", "52.6", "412", "348"],
        ["Manual Expert", "90.5", "35.1", "256", "198"],
        ["AdaptNAS (Ours)", "94.2", "12.2", "152", "143"],
    ]
    for j, row in enumerate(rows):
        y = table_y + 18 + j * 16
        for i, val in enumerate(row):
            fn = heading_font if j == len(rows) - 1 else body_font
            page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=9, fontname=fn, color=(0, 0, 0))

    # More results text
    more_results = (
        "\nOur best architecture achieves 94.2% accuracy on CIFAR-10 with only 12.2ms inference "
        "latency on ARM Cortex-M7, representing a 3.7x speedup over the previous best MCUNet "
        "while improving accuracy by 1.4 percentage points. The memory footprint of 152 KB fits "
        "comfortably within the 512 KB SRAM budget of the STM32H7.\n\n"
        "4.1  Keyword Spotting Results\n\n"
        "On the Speech Commands benchmark, AdaptNAS achieves 96.8% accuracy with 8.3ms latency, "
        "meeting the strict real-time requirements for always-on keyword detection. The discovered "
        "architecture uses a novel combination of temporal convolutions and lightweight attention "
        "that captures both local and global temporal patterns.\n\n"
        "4.2  Anomaly Detection Results\n\n"
        "For industrial anomaly detection on MIMII, our method achieves an AUC of 0.923 while "
        "operating at 5.1ms per inference window. This enables continuous monitoring at sampling "
        "rates up to 196 Hz, sufficient for most industrial applications."
    )
    page.insert_textbox(pymupdf.Rect(72, 310, 540, 750), more_results,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ===== PAGE 6: Analysis and Discussion =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "5  Analysis and Discussion",
                     fontsize=14, fontname=heading_font, color=(0, 0, 0))
    analysis_text = (
        "5.1  Ablation Study\n\n"
        "We conduct ablation experiments to quantify the contribution of each component:\n\n"
        "Hierarchical Search Space: Removing the hierarchy and using a flat search space increases "
        "search cost by 2.3x while producing architectures with 1.8% lower accuracy on average.\n\n"
        "Surrogate Predictors: Replacing surrogate predictions with actual hardware measurements "
        "improves final architecture quality by only 0.3% but increases search time from 8 to 340 "
        "GPU-hours, a 42x slowdown.\n\n"
        "Pareto-Guided Selection: Using single-objective optimization (accuracy only, with hard "
        "latency constraints) produces architectures concentrated in a narrow region of the trade-off "
        "space, limiting deployment flexibility.\n\n"
        "5.2  Discovered Architecture Patterns\n\n"
        "Analysis of top-performing architectures reveals several consistent patterns:\n\n"
        "  (1) Early stages prefer larger kernel sizes (5x5, 7x7) for efficient spatial feature "
        "extraction, while later stages use smaller kernels (3x3) to reduce computation.\n\n"
        "  (2) Skip connections are predominantly placed at 1/3 and 2/3 depth, forming an "
        "approximate U-Net-like topology.\n\n"
        "  (3) Squeeze-and-excitation modules are selectively inserted only in middle stages, "
        "balancing representational power with computational overhead.\n\n"
        "5.3  Limitations\n\n"
        "Our approach has several limitations. First, the surrogate predictors require an initial "
        "data collection phase of approximately 200 GPU-hours per target platform. Second, the "
        "search space, while flexible, does not include recent innovations such as dynamic networks "
        "or mixture-of-experts layers. Third, our evaluation focuses on single-task deployment and "
        "does not address multi-task or continual learning scenarios."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 750), analysis_text,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ===== PAGE 7: Conclusion and References =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "6  Conclusion", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    conclusion_text = (
        "We presented AdaptNAS, a multi-objective neural architecture search framework designed "
        "for resource-constrained edge deployment. Through hierarchical search space design, "
        "hardware-aware surrogate predictors, and Pareto-guided optimization, our approach discovers "
        "architectures that achieve 94.2% of SOTA accuracy while reducing latency by 3.7x and "
        "memory by 2.1x. Our framework generalizes across image classification, keyword spotting, "
        "and anomaly detection tasks, demonstrating broad applicability to edge AI applications.\n\n"
        "Future work will extend AdaptNAS to support dynamic architectures that adapt at runtime, "
        "enabling more efficient resource utilization under varying computational budgets."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 540, 250), conclusion_text,
                        fontsize=10, fontname=body_font, color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # References
    page.insert_text(pymupdf.Point(72, 280), "References", fontsize=14, fontname=heading_font, color=(0, 0, 0))
    refs = [
        "[1] Tan, M. et al. MnasNet: Platform-Aware Neural Architecture Search for Mobile. CVPR, 2019.",
        "[2] Lin, J. et al. MCUNet: Tiny Deep Learning on IoT Devices. NeurIPS, 2020.",
        "[3] Banbury, C. et al. MicroNets: Neural Network Architectures for Deploying TinyML. MLSys, 2021.",
        "[4] Tan, M. and Le, Q.V. EfficientNet: Rethinking Model Scaling for CNNs. ICML, 2019.",
        "[5] Cai, H. et al. Once-for-All: Train One Network and Specialize it for Efficient Deployment. ICLR, 2020.",
        "[6] Wu, B. et al. FBNet: Hardware-Aware Efficient ConvNet Design via Differentiable NAS. CVPR, 2019.",
        "[7] Howard, A. et al. Searching for MobileNetV3. ICCV, 2019.",
        "[8] Deb, K. et al. A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II. IEEE TEC, 2002.",
        "[9] Purohit, H. et al. MIMII Dataset: Sound Dataset for Malfunctioning Industrial Machines. DCASE, 2019.",
        "[10] Warden, P. Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition. arXiv, 2018.",
        "[11] Liberis, E. et al. mu-NAS: Constrained Neural Architecture Search for Microcontrollers. EMDL, 2021.",
        "[12] Fedorov, I. et al. SpArSe: Sparse Architecture Search for CNNs on Resource-Constrained MCUs. NeurIPS, 2019.",
    ]
    y = 300
    for ref in refs:
        page.insert_textbox(pymupdf.Rect(72, y, 540, y + 30), ref,
                            fontsize=8.5, fontname=body_font, color=(0, 0, 0))
        y += 28

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open PDF in Evince at page 3
    launch_gui(f'evince --page-index=3 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
