"""
Initial Setup: Create a 30-page academic paper PDF with bookmarks, equations,
code blocks, tables, figures, and citations for document intelligence extraction.
Task ID: pdf_gf3_050
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_050'
DOCS_DIR = f'{WORKDIR}/docs'
OUTPUT = f'{DOCS_DIR}/technical_paper.pdf'


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
    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)

    doc = pymupdf.open()

    # ---- Document structure ----
    # A 30-page academic paper: "Adaptive Neural Architecture Search for Edge Computing"
    # Sections:
    #   1. Abstract (page 1)
    #   2. Introduction (pages 2-4)
    #   3. Related Work (pages 5-7)
    #   4. Methodology (pages 8-14)
    #     4.1 Problem Formulation (8-9)
    #     4.2 Search Space Design (10-11)
    #     4.3 Optimization Algorithm (12-14)
    #   5. Experiments (pages 15-22)
    #     5.1 Experimental Setup (15-16)
    #     5.2 Results and Analysis (17-20)
    #     5.3 Ablation Study (21-22)
    #   6. Discussion (pages 23-25)
    #   7. Conclusion (pages 26-27)
    #   8. References (pages 28-30)

    W, H = 612, 792  # Letter size
    MARGIN = 72
    TEXT_W = W - 2 * MARGIN

    def new_page():
        return doc.new_page(width=W, height=H)

    def add_header(page, text, y, fontsize=20, fontname="hebo"):
        page.insert_text(pymupdf.Point(MARGIN, y), text,
                         fontsize=fontsize, fontname=fontname, color=(0, 0, 0))
        return y + fontsize + 8

    def add_body(page, text, y, fontsize=11, fontname="tiro", line_spacing=16):
        rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - MARGIN)
        excess = page.insert_textbox(rect, text, fontsize=fontsize,
                                     fontname=fontname, color=(0, 0, 0),
                                     align=pymupdf.TEXT_ALIGN_JUSTIFY)
        return excess

    def add_equation(page, eq_text, y, eq_num):
        """Add equation in italic with equation number."""
        page.insert_text(pymupdf.Point(MARGIN + 40, y), eq_text,
                         fontsize=12, fontname="tiit", color=(0, 0, 0.3))
        page.insert_text(pymupdf.Point(W - MARGIN - 40, y), f"({eq_num})",
                         fontsize=11, fontname="tiro", color=(0, 0, 0))
        return y + 24

    def add_code_block(page, code_lines, y):
        """Add code block in monospace font with light gray background."""
        block_h = len(code_lines) * 14 + 16
        rect = pymupdf.Rect(MARGIN + 20, y - 4, W - MARGIN - 20, y + block_h)
        shape = page.new_shape()
        shape.draw_rect(rect)
        shape.finish(color=(0.7, 0.7, 0.7), fill=(0.95, 0.95, 0.95), width=0.5)
        shape.commit()
        cy = y + 10
        for line in code_lines:
            page.insert_text(pymupdf.Point(MARGIN + 30, cy), line,
                             fontsize=9, fontname="cour", color=(0.1, 0.1, 0.1))
            cy += 14
        return y + block_h + 12

    def add_table(page, headers, rows, y, col_widths=None):
        """Draw a simple table with borders."""
        n_cols = len(headers)
        if col_widths is None:
            col_w = TEXT_W / n_cols
            col_widths = [col_w] * n_cols
        row_h = 20
        shape = page.new_shape()
        # Header row
        x = MARGIN
        for i, hdr in enumerate(headers):
            r = pymupdf.Rect(x, y, x + col_widths[i], y + row_h)
            shape.draw_rect(r)
            shape.finish(color=(0, 0, 0), fill=(0.2, 0.3, 0.5), width=0.5)
            x += col_widths[i]
        shape.commit()
        x = MARGIN
        for i, hdr in enumerate(headers):
            page.insert_text(pymupdf.Point(x + 4, y + 14), hdr,
                             fontsize=9, fontname="hebo", color=(1, 1, 1))
            x += col_widths[i]
        y += row_h
        # Data rows
        for row_idx, row in enumerate(rows):
            shape2 = page.new_shape()
            x = MARGIN
            fill = (0.95, 0.95, 0.97) if row_idx % 2 == 0 else (1, 1, 1)
            for i, cell in enumerate(row):
                r = pymupdf.Rect(x, y, x + col_widths[i], y + row_h)
                shape2.draw_rect(r)
                shape2.finish(color=(0.5, 0.5, 0.5), fill=fill, width=0.3)
                x += col_widths[i]
            shape2.commit()
            x = MARGIN
            for i, cell in enumerate(row):
                page.insert_text(pymupdf.Point(x + 4, y + 14), str(cell),
                                 fontsize=9, fontname="tiro", color=(0, 0, 0))
                x += col_widths[i]
            y += row_h
        return y + 12

    def add_figure_placeholder(page, caption, fig_num, y):
        """Draw a placeholder figure (colored rectangle with shapes) and caption."""
        fig_h = 100
        fig_rect = pymupdf.Rect(MARGIN + 60, y, W - MARGIN - 60, y + fig_h)
        shape = page.new_shape()
        shape.draw_rect(fig_rect)
        shape.finish(color=(0.3, 0.3, 0.3), fill=(0.9, 0.92, 0.95), width=1)
        # Add some internal shapes to look like a diagram
        shape.draw_line(pymupdf.Point(MARGIN + 100, y + 30),
                        pymupdf.Point(W - MARGIN - 100, y + 30))
        shape.finish(color=(0.4, 0.4, 0.8), width=1)
        shape.draw_circle(pymupdf.Point(W / 2, y + 60), 20)
        shape.finish(color=(0.2, 0.5, 0.2), fill=(0.7, 0.9, 0.7), width=1)
        shape.commit()
        page.insert_text(pymupdf.Point(MARGIN + 60, y + fig_h + 14),
                         f"Figure {fig_num}: {caption}",
                         fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
        return y + fig_h + 30

    def add_citation_text(page, text, y):
        """Add text that contains [N] style citations."""
        page.insert_text(pymupdf.Point(MARGIN, y), text,
                         fontsize=11, fontname="tiro", color=(0, 0, 0))
        return y + 16

    # ======================= PAGE 1: Title & Abstract =======================
    p = new_page()
    y = 120
    p.insert_text(pymupdf.Point(MARGIN, y),
                  "Adaptive Neural Architecture Search",
                  fontsize=22, fontname="hebo", color=(0, 0, 0))
    y += 30
    p.insert_text(pymupdf.Point(MARGIN, y),
                  "for Edge Computing: A Comprehensive Study",
                  fontsize=22, fontname="hebo", color=(0, 0, 0))
    y += 40
    p.insert_text(pymupdf.Point(MARGIN, y),
                  "Elena Vasquez, Hiroshi Tanaka, Priya Sharma, David Mueller",
                  fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))
    y += 20
    p.insert_text(pymupdf.Point(MARGIN, y),
                  "Institute for Advanced Computing, Stanford University",
                  fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))
    y += 16
    p.insert_text(pymupdf.Point(MARGIN, y),
                  "Department of Electrical Engineering, Tokyo Institute of Technology",
                  fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))
    y += 40
    y = add_header(p, "Abstract", y, fontsize=14)
    abstract = (
        "Neural Architecture Search (NAS) has emerged as a powerful paradigm for automating "
        "the design of deep neural networks. However, deploying NAS-discovered architectures "
        "on edge devices remains challenging due to stringent latency and memory constraints. "
        "In this paper, we propose AdaptiveNAS, a novel framework that jointly optimizes "
        "architecture topology and quantization strategy for heterogeneous edge platforms. "
        "Our approach introduces a differentiable search space that encompasses both macro "
        "and micro architecture decisions, coupled with a hardware-aware objective function "
        "that accounts for device-specific latency profiles. Through extensive experiments "
        "on CIFAR-10, ImageNet, and our custom EdgeBench dataset, we demonstrate that "
        "AdaptiveNAS achieves 94.7% top-1 accuracy on CIFAR-10 while maintaining inference "
        "latency under 5ms on ARM Cortex-A72 processors [1]. Our framework reduces search "
        "cost by 3.2x compared to state-of-the-art methods [2] while discovering architectures "
        "that are 1.8x more efficient than manually designed networks [3]. We further show that "
        "the discovered architectures generalize well across different edge platforms including "
        "NVIDIA Jetson Nano, Raspberry Pi 4, and Google Coral [4]."
    )
    add_body(p, abstract, y)

    # ======================= PAGES 2-4: Introduction =======================
    p = new_page()
    y = 72
    y = add_header(p, "1. Introduction", y, fontsize=18)
    intro_text = (
        "The proliferation of edge computing devices has created an unprecedented demand for "
        "efficient deep learning models that can operate within strict computational budgets. "
        "While neural architecture search has shown remarkable success in discovering high-performance "
        "architectures [5], [6], the computational cost of traditional NAS methods makes them "
        "impractical for edge deployment scenarios. Recent advances in one-shot NAS methods [7] "
        "have significantly reduced search costs, but these approaches often fail to account for "
        "the heterogeneous nature of edge computing platforms. "
        "The fundamental challenge lies in the multi-objective nature of edge deployment: we must "
        "simultaneously optimize for accuracy, latency, memory footprint, and energy consumption [8]. "
        "Traditional NAS formulations treat these as secondary constraints rather than first-class "
        "objectives, leading to suboptimal trade-offs. Furthermore, the diversity of edge platforms "
        "means that an architecture optimal for one device may perform poorly on another [9]. "
        "In this work, we address these challenges through a unified framework called AdaptiveNAS "
        "that introduces three key contributions. First, we propose a hierarchical search space "
        "that naturally encodes both topology and quantization decisions. Second, we develop a "
        "differentiable hardware-aware objective that can be efficiently optimized using gradient "
        "descent [10]. Third, we introduce a transfer mechanism that enables rapid adaptation "
        "of discovered architectures to new target platforms [11]."
    )
    add_body(p, intro_text, y)

    p = new_page()
    y = 72
    intro_text2 = (
        "Our experimental evaluation demonstrates the effectiveness of AdaptiveNAS across multiple "
        "benchmarks and hardware platforms. On CIFAR-10, our method achieves 94.7% accuracy with "
        "only 2.3M parameters and 4.8ms inference latency on ARM Cortex-A72 [12]. On ImageNet, "
        "we achieve 76.8% top-1 accuracy with 3.1M parameters, outperforming EfficientNet-B0 [13] "
        "by 0.5% while being 1.4x faster on Jetson Nano. "
        "The remainder of this paper is organized as follows. Section 2 reviews related work on "
        "neural architecture search and efficient model design. Section 3 presents our methodology "
        "including the search space, optimization algorithm, and hardware-aware objective. Section 4 "
        "describes our experimental setup and presents comprehensive results. Section 5 discusses "
        "limitations and future directions, and Section 6 concludes the paper."
    )
    add_body(p, intro_text2, y)
    y = 360
    # Equation in introduction
    y = add_equation(p, "L(w, \u03b1) = \u2211\u1d62 CE(f(x\u1d62; w, \u03b1), y\u1d62) + \u03bb\u00b7R(\u03b1)", y, 1)
    body_after_eq = (
        "where w represents the network weights, \u03b1 denotes the architecture parameters, "
        "CE is the cross-entropy loss, and R(\u03b1) is a regularization term that penalizes "
        "architectures exceeding the target latency budget. The coefficient \u03bb controls "
        "the trade-off between accuracy and efficiency [14]."
    )
    add_body(p, body_after_eq, y)

    p = new_page()
    y = 72
    intro_text3 = (
        "The key insight of our approach is that architecture decisions and quantization strategies "
        "are fundamentally coupled. A network layer that benefits from higher bit-width may have "
        "a different optimal topology than one operating at lower precision [15]. By jointly "
        "searching over both dimensions, AdaptiveNAS discovers architectures that are Pareto-optimal "
        "in the accuracy-efficiency space. Our theoretical analysis shows that the joint search "
        "space, while larger, has favorable optimization properties that enable efficient exploration "
        "through gradient-based methods [16], [17]. We validate this through extensive ablation "
        "studies demonstrating that joint optimization outperforms sequential approaches by "
        "1.2-2.8% accuracy at equivalent latency budgets."
    )
    add_body(p, intro_text3, y)

    # ======================= PAGES 5-7: Related Work =======================
    p = new_page()
    y = 72
    y = add_header(p, "2. Related Work", y, fontsize=18)
    y = add_header(p, "2.1 Neural Architecture Search", y, fontsize=14, fontname="hebo")
    rw_text = (
        "Neural Architecture Search has evolved rapidly since the seminal work of Zoph and Le [18] "
        "who used reinforcement learning to discover competitive architectures. Subsequent approaches "
        "have explored evolutionary algorithms [19], Bayesian optimization [20], and gradient-based "
        "methods [21]. DARTS [22] introduced differentiable architecture search by relaxing the "
        "discrete search space to continuous, enabling gradient-based optimization. ProxylessNAS [23] "
        "extended this idea to directly search on the target task and hardware. "
        "One-shot methods [24] amortize the search cost by training a single supernet that shares "
        "weights across all candidate architectures. OFA (Once-for-All) [25] trained a single "
        "network that supports diverse sub-networks for different deployment scenarios. However, "
        "these methods typically assume a fixed quantization strategy, limiting their ability to "
        "exploit mixed-precision opportunities."
    )
    add_body(p, rw_text, y)

    p = new_page()
    y = 72
    y = add_header(p, "2.2 Efficient Model Design", y, fontsize=14, fontname="hebo")
    rw_text2 = (
        "Manual design of efficient architectures has produced several influential model families. "
        "MobileNets [26] introduced depthwise separable convolutions, reducing computational cost "
        "while maintaining accuracy. ShuffleNet [27] further improved efficiency through channel "
        "shuffling operations. EfficientNet [13] proposed compound scaling to balance depth, width, "
        "and resolution. More recently, transformer-based architectures [28] have shown promising "
        "results for edge deployment when combined with appropriate compression techniques [29]. "
        "Knowledge distillation [30] and pruning [31] offer complementary approaches to model "
        "compression that can be applied post-search to further reduce model complexity."
    )
    add_body(p, rw_text2, y)
    y = 380
    y = add_header(p, "2.3 Hardware-Aware Optimization", y, fontsize=14, fontname="hebo")
    hw_text = (
        "Hardware-aware NAS methods incorporate device-specific constraints into the search process. "
        "MnasNet [32] used latency measured on actual devices as an optimization objective. "
        "FBNet [33] and ChamNet [34] employed latency lookup tables for efficient hardware-aware "
        "search. NetAdapt [35] proposed an iterative approach to adapt architectures to meet "
        "resource budgets. Our work differs by jointly optimizing architecture and quantization "
        "while supporting rapid transfer across heterogeneous platforms."
    )
    add_body(p, hw_text, y)

    p = new_page()
    y = 72
    rw_text3 = (
        "Mixed-precision quantization has emerged as a powerful technique for edge deployment [36]. "
        "HAQ [37] used reinforcement learning to determine per-layer bit-widths. HAWQ [38] "
        "leveraged Hessian information to guide bit-width allocation. DQ [39] proposed "
        "differentiable quantization for end-to-end training. However, these methods operate on "
        "fixed architectures, missing the opportunity to co-optimize topology and precision. "
        "Recent work by Wu et al. [40] explored joint architecture-quantization search but was "
        "limited to a restricted search space and single-device optimization. Our AdaptiveNAS "
        "framework addresses these limitations through a more expressive search space and "
        "multi-platform transfer learning."
    )
    add_body(p, rw_text3, y)

    # Table: comparison of related methods
    y = 380
    y = add_figure_placeholder(p, "Taxonomy of Neural Architecture Search methods", 1, y)

    # ======================= PAGES 8-14: Methodology =======================
    p = new_page()
    y = 72
    y = add_header(p, "3. Methodology", y, fontsize=18)
    y = add_header(p, "3.1 Problem Formulation", y, fontsize=14, fontname="hebo")
    method_text = (
        "We formulate the architecture search problem as a constrained multi-objective optimization. "
        "Given a target edge device d with latency budget T and memory budget M, we seek to find "
        "the optimal architecture \u03b1* and quantization policy q* that maximize task accuracy "
        "while satisfying hardware constraints. The formal optimization problem is defined as follows:"
    )
    add_body(p, method_text, y)
    y = 280
    y = add_equation(p, "max   Acc(w*(\u03b1, q), \u03b1, q)", y, 2)
    y = add_equation(p, "s.t.  Lat(\u03b1, q, d) \u2264 T,  Mem(\u03b1, q) \u2264 M", y, 3)
    y = add_equation(p, "w*(\u03b1, q) = arg min\u2097 L(w, \u03b1, q)", y, 4)
    y += 10
    form_text2 = (
        "where Acc denotes the validation accuracy, Lat represents the device-specific inference "
        "latency, and Mem is the peak memory consumption. The inner optimization finds the optimal "
        "weights w* for a given architecture \u03b1 and quantization policy q. To make this "
        "bilevel optimization tractable, we adopt a continuous relaxation approach inspired by "
        "DARTS [22] but extended to jointly handle architecture and quantization decisions."
    )
    add_body(p, form_text2, y)

    p = new_page()
    y = 72
    form_text3 = (
        "The continuous relaxation transforms the discrete architecture decisions into a probability "
        "distribution over candidate operations. For each edge (i, j) in the computation graph, "
        "the output is computed as a weighted sum:"
    )
    add_body(p, form_text3, y)
    y = 180
    y = add_equation(p, "h\u2c7c = \u2211\u2096 softmax(\u03b1\u1d62\u2c7c)\u2096 \u00b7 o\u2096(h\u1d62, q\u2096)", y, 5)
    y += 10
    form_text4 = (
        "where o\u2096 represents the k-th candidate operation (convolution, pooling, etc.) applied "
        "with quantization level q\u2096. The architecture parameters \u03b1 and quantization "
        "parameters q are jointly optimized through gradient descent on the validation loss."
    )
    add_body(p, form_text4, y)
    y = 360
    y = add_equation(p, "\u2207\u03b1 L\u1d65\u2090\u2097(\u03b1, q) \u2248 \u2207\u03b1 L\u1d65\u2090\u2097(\u03b1, q) - \u03be\u00b7\u2207\u00b2\u03b1,w L\u209c\u1d63\u2090\u1d62\u2099 \u00b7 \u2207w L\u209c\u1d63\u2090\u1d62\u2099", y, 6)
    y += 10
    approx_text = (
        "This first-order approximation avoids the expensive second-order computation while "
        "maintaining search quality. The hyperparameter \u03be controls the strength of the "
        "approximation correction term."
    )
    add_body(p, approx_text, y)

    # Pages 10-11: Search Space Design
    p = new_page()
    y = 72
    y = add_header(p, "3.2 Search Space Design", y, fontsize=14, fontname="hebo")
    ss_text = (
        "Our search space is organized hierarchically into cells and blocks. Each cell consists of "
        "N nodes with directed edges representing information flow. The candidate operations include:"
    )
    add_body(p, ss_text, y)

    # Table of operations
    y = 220
    ops_headers = ["Operation", "Parameters", "FLOPs", "Latency (ms)"]
    ops_data = [
        ["3x3 Conv", "9K\u00b7C\u00b2", "18M", "0.42"],
        ["5x5 Conv", "25K\u00b7C\u00b2", "50M", "0.98"],
        ["3x3 DWConv", "9K\u00b7C", "0.2M", "0.08"],
        ["5x5 DWConv", "25K\u00b7C", "0.5M", "0.15"],
        ["3x3 MaxPool", "0", "0.1M", "0.05"],
        ["Skip Connect", "0", "0", "0.01"],
        ["Zero (None)", "0", "0", "0"],
        ["SE Block", "2C\u00b2/r", "0.4M", "0.12"],
    ]
    y = add_table(p, ops_headers, ops_data, y, [160, 120, 100, 88])

    y += 20
    ss_text2 = (
        "Table 1: Candidate operations in the search space with typical parameter counts, "
        "FLOPs, and measured latency on ARM Cortex-A72. C denotes channel width, r is the "
        "SE reduction ratio. The search space yields approximately 10\u00b9 unique architectures."
    )
    add_body(p, ss_text2, y, fontsize=9, fontname="tiit")

    p = new_page()
    y = 72
    ss_text3 = (
        "The quantization search space allows per-layer bit-width selection from the set "
        "{2, 4, 8, 16, 32} bits for both weights and activations. The total joint search space "
        "size is approximately 10\u00b9 \u00d7 5\u00b2\u1d38 where L is the number of layers. "
        "Despite this enormous space, our differentiable formulation enables efficient exploration."
    )
    add_body(p, ss_text3, y)
    y = 240
    y = add_equation(p, "q\u2096 = \u2211\u2c7c b\u2c7c \u00b7 softmax(\u03b2\u2096)\u2c7c,  b \u2208 {2, 4, 8, 16, 32}", y, 7)
    y += 20
    y = add_figure_placeholder(p, "Hierarchical search space with cell and block structure", 2, y)
    y += 10
    ss_text4 = (
        "The hierarchical structure allows the search algorithm to first identify promising "
        "macro-level topologies before refining micro-level operation choices. This coarse-to-fine "
        "strategy significantly improves search efficiency [41], [42]."
    )
    add_body(p, ss_text4, y)

    # Pages 12-14: Optimization Algorithm
    p = new_page()
    y = 72
    y = add_header(p, "3.3 Optimization Algorithm", y, fontsize=14, fontname="hebo")
    opt_text = (
        "Our optimization procedure alternates between updating network weights and architecture "
        "parameters. The complete algorithm is presented below:"
    )
    add_body(p, opt_text, y)
    y = 200

    # Code block: algorithm pseudocode
    code1 = [
        "def adaptive_nas_search(supernet, train_loader, val_loader,",
        "                        target_device, T_max, M_max):",
        "    alpha = initialize_arch_params(supernet)",
        "    beta = initialize_quant_params(supernet)",
        "    w = supernet.parameters()",
        "",
        "    for epoch in range(num_epochs):",
        "        # Phase 1: Update weights",
        "        for x_train, y_train in train_loader:",
        "            loss = cross_entropy(supernet(x_train, alpha, beta), y_train)",
        "            loss.backward()",
        "            optimizer_w.step()",
        "",
        "        # Phase 2: Update architecture params",
        "        for x_val, y_val in val_loader:",
        "            lat = estimate_latency(alpha, beta, target_device)",
        "            mem = estimate_memory(alpha, beta)",
        "            loss = CE(supernet(x_val, alpha, beta), y_val)",
        "            loss += lambda_lat * max(0, lat - T_max)",
        "            loss += lambda_mem * max(0, mem - M_max)",
        "            loss.backward()",
        "            optimizer_arch.step()",
        "",
        "    return derive_final_architecture(alpha, beta)",
    ]
    y = add_code_block(p, code1, y)

    p = new_page()
    y = 72
    opt_text2 = (
        "The latency estimation function uses a differentiable lookup table approach. For each "
        "operation-quantization pair, we pre-measure the actual latency on the target device and "
        "construct a continuous approximation:"
    )
    add_body(p, opt_text2, y)
    y = 200
    y = add_equation(p, "Lat(\u03b1, q) = \u2211\u2097 \u2211\u2096 \u2211\u2c7c p\u2097\u2096 \u00b7 r\u2097\u2c7c \u00b7 lat(o\u2096, b\u2c7c, d)", y, 8)
    y += 10
    opt_text3 = (
        "where p\u2097\u2096 is the probability of selecting operation k at layer l (from softmax "
        "over \u03b1), r\u2097\u2c7c is the probability of selecting bit-width j at layer l (from "
        "softmax over \u03b2), and lat(o\u2096, b\u2c7c, d) is the measured latency of operation "
        "o\u2096 at bit-width b\u2c7c on device d."
    )
    add_body(p, opt_text3, y)
    y = 400
    y = add_equation(p, "\u2202Lat/\u2202\u03b1\u2097\u2096 = r\u2097 \u00b7 (lat(o\u2096, q\u2097, d) - \u2211\u2096' p\u2097\u2096' \u00b7 lat(o\u2096', q\u2097, d))", y, 9)

    p = new_page()
    y = 72
    # Transfer learning mechanism
    transfer_text = (
        "To enable efficient transfer to new devices, we propose a platform adaptation module "
        "that fine-tunes only the architecture parameters while keeping weights frozen. Given "
        "an architecture \u03b1* discovered for source device d\u209b, we adapt it to target "
        "device d\u209c by solving a lightweight optimization:"
    )
    add_body(p, transfer_text, y)
    y = 230
    y = add_equation(p, "\u03b1\u209c = \u03b1* - \u03b7 \u00b7 \u2207\u03b1 [Lat(\u03b1, q, d\u209c) + \u03bc\u00b7||\u03b1 - \u03b1*||]", y, 10)
    y += 20
    transfer_text2 = (
        "The regularization term ||\u03b1 - \u03b1*|| encourages the adapted architecture to remain "
        "close to the source, preserving learned representations. This transfer typically converges "
        "within 50 iterations, taking less than 5 minutes on a single GPU, compared to 8 hours "
        "for full search from scratch."
    )
    add_body(p, transfer_text2, y)

    # Code block: transfer adaptation
    y = 440
    code2 = [
        "def transfer_to_device(alpha_source, device_target,",
        "                       latency_table, num_steps=50):",
        "    alpha = alpha_source.clone().requires_grad_(True)",
        "    optimizer = torch.optim.Adam([alpha], lr=0.01)",
        "",
        "    for step in range(num_steps):",
        "        lat = estimate_latency(alpha, q, device_target)",
        "        reg = torch.norm(alpha - alpha_source)",
        "        loss = lat + mu * reg",
        "        loss.backward()",
        "        optimizer.step()",
        "",
        "    return alpha.detach()",
    ]
    y = add_code_block(p, code2, y)

    # ======================= PAGES 15-22: Experiments =======================
    p = new_page()
    y = 72
    y = add_header(p, "4. Experiments", y, fontsize=18)
    y = add_header(p, "4.1 Experimental Setup", y, fontsize=14, fontname="hebo")
    exp_text = (
        "We evaluate AdaptiveNAS on three benchmark datasets: CIFAR-10 (60K images, 10 classes), "
        "ImageNet (1.28M images, 1000 classes), and EdgeBench (our custom dataset with 100K images "
        "across 50 fine-grained categories). The search phase uses 50% of training data for weight "
        "updates and 50% for architecture updates. We search for 100 epochs with batch size 64 "
        "on 4 NVIDIA V100 GPUs. The discovered architectures are then retrained from scratch for "
        "600 epochs using standard training recipes [13]."
    )
    add_body(p, exp_text, y)
    y = 360
    # Hardware platforms table
    hw_headers = ["Platform", "CPU/GPU", "RAM", "TDP"]
    hw_data = [
        ["Raspberry Pi 4", "BCM2711 4xA72", "4 GB", "7.5W"],
        ["Jetson Nano", "128-core Maxwell", "4 GB", "10W"],
        ["Google Coral", "Edge TPU", "1 GB", "2W"],
        ["Intel NCS2", "Myriad X VPU", "512 MB", "1.5W"],
        ["STM32H7", "Cortex-M7 480MHz", "1 MB", "0.5W"],
    ]
    y = add_table(p, hw_headers, hw_data, y, [130, 160, 80, 98])
    y += 5
    add_body(p, "Table 2: Edge hardware platforms used in evaluation.", y, fontsize=9, fontname="tiit")

    p = new_page()
    y = 72
    exp_text2 = (
        "We compare AdaptiveNAS against several baseline methods spanning different categories: "
        "manually designed architectures (MobileNetV2 [43], ShuffleNetV2 [44], EfficientNet-B0 [13]), "
        "NAS-discovered architectures (DARTS [22], ProxylessNAS [23], OFA [25]), and joint "
        "architecture-quantization methods (APQ [45], DQ-NAS [46]). All methods are evaluated "
        "under identical training conditions for fair comparison."
    )
    add_body(p, exp_text2, y)

    y = 300
    y = add_figure_placeholder(p, "Search cost comparison across NAS methods (GPU-hours)", 3, y)

    # Pages 17-20: Results
    p = new_page()
    y = 72
    y = add_header(p, "4.2 Results and Analysis", y, fontsize=14, fontname="hebo")
    res_text = (
        "Table 3 presents the main results on CIFAR-10. AdaptiveNAS achieves the highest accuracy "
        "among methods with comparable latency budgets. Notably, our method discovers architectures "
        "that are both more accurate and more efficient than manually designed baselines [43], [44]."
    )
    add_body(p, res_text, y)

    # Main results table
    y = 240
    res_headers = ["Method", "Params(M)", "Top-1(%)", "Lat(ms)", "Search(h)"]
    res_data = [
        ["MobileNetV2", "3.4", "92.1", "8.2", "-"],
        ["ShuffleNetV2", "2.3", "91.5", "6.7", "-"],
        ["EfficientNet-B0", "5.3", "93.2", "11.4", "-"],
        ["DARTS", "3.3", "93.5", "7.8", "24"],
        ["ProxylessNAS", "4.1", "93.8", "6.1", "8.3"],
        ["OFA", "2.6", "93.1", "5.5", "48"],
        ["APQ", "2.8", "93.4", "5.2", "12"],
        ["DQ-NAS", "3.0", "93.6", "5.8", "16"],
        ["AdaptiveNAS", "2.3", "94.7", "4.8", "7.5"],
    ]
    y = add_table(p, res_headers, res_data, y, [120, 85, 85, 85, 93])
    y += 5
    add_body(p, "Table 3: Results on CIFAR-10 with ARM Cortex-A72 target. Best results in each column are highlighted.", y, fontsize=9, fontname="tiit")

    p = new_page()
    y = 72
    res_text2 = (
        "On ImageNet, our method maintains competitive accuracy while significantly reducing "
        "both parameter count and inference latency. The results demonstrate the scalability "
        "of our approach to large-scale datasets and complex architectures."
    )
    add_body(p, res_text2, y)

    # ImageNet results
    y = 200
    img_headers = ["Method", "Params(M)", "Top-1(%)", "Top-5(%)", "Lat(ms)"]
    img_data = [
        ["MobileNetV2-1.0", "3.4", "72.0", "91.0", "12.3"],
        ["EfficientNet-B0", "5.3", "76.3", "93.2", "16.8"],
        ["ProxylessNAS", "4.1", "74.6", "92.2", "10.5"],
        ["OFA-595M", "2.6", "75.6", "92.7", "9.8"],
        ["AdaptiveNAS-S", "2.1", "74.8", "92.4", "7.2"],
        ["AdaptiveNAS-M", "3.1", "76.8", "93.5", "9.1"],
        ["AdaptiveNAS-L", "4.5", "78.2", "94.1", "12.6"],
    ]
    y = add_table(p, img_headers, img_data, y, [120, 85, 80, 80, 103])
    y += 5
    add_body(p, "Table 4: ImageNet classification results. AdaptiveNAS variants span different accuracy-efficiency trade-offs.", y, fontsize=9, fontname="tiit")

    y += 30
    res_text3 = (
        "The accuracy-latency Pareto frontier in Figure 4 shows that AdaptiveNAS consistently "
        "dominates existing methods across the entire efficiency spectrum. The joint optimization "
        "of architecture and quantization is particularly beneficial at the low-latency end of "
        "the spectrum, where aggressive quantization is essential [47]."
    )
    add_body(p, res_text3, y)

    p = new_page()
    y = 72
    y = add_figure_placeholder(p, "Accuracy-Latency Pareto frontier on ImageNet", 4, y)
    y += 20
    res_text4 = (
        "Cross-platform evaluation results are presented in Table 5. AdaptiveNAS architectures "
        "transferred to new devices maintain over 95% of their original accuracy while meeting "
        "platform-specific latency constraints. The transfer adaptation typically requires less "
        "than 50 optimization steps."
    )
    add_body(p, res_text4, y)

    y = 360
    xp_headers = ["Source \u2192 Target", "Acc Drop(%)", "Transfer Time", "Lat Met"]
    xp_data = [
        ["RPi4 \u2192 Jetson", "-0.3", "4.2 min", "Yes"],
        ["RPi4 \u2192 Coral", "-0.8", "3.1 min", "Yes"],
        ["RPi4 \u2192 NCS2", "-0.5", "5.7 min", "Yes"],
        ["Jetson \u2192 RPi4", "-0.4", "3.8 min", "Yes"],
        ["Jetson \u2192 Coral", "-0.7", "2.9 min", "Yes"],
    ]
    y = add_table(p, xp_headers, xp_data, y, [140, 100, 120, 108])
    y += 5
    add_body(p, "Table 5: Cross-platform transfer results. Accuracy drop is relative to platform-specific search.", y, fontsize=9, fontname="tiit")

    p = new_page()
    y = 72
    res_text5 = (
        "The discovered architectures exhibit interesting patterns. For latency-constrained "
        "scenarios, the search consistently selects depthwise separable convolutions with 4-bit "
        "quantization in early layers and standard convolutions with 8-bit quantization in later "
        "layers. This aligns with theoretical predictions about information flow in neural "
        "networks [48], [49]. The SE blocks are predominantly placed in the final third of the "
        "network where channel attention is most beneficial."
    )
    add_body(p, res_text5, y)

    # Code block: architecture derived
    y = 320
    code3 = [
        "# Discovered AdaptiveNAS-M architecture",
        "architecture = {",
        "    'stem': {'op': 'conv3x3', 'channels': 32, 'bits': 8},",
        "    'stage1': [",
        "        {'op': 'dwconv3x3', 'exp': 1, 'channels': 16, 'bits': 4},",
        "        {'op': 'dwconv3x3', 'exp': 6, 'channels': 24, 'bits': 4},",
        "    ],",
        "    'stage2': [",
        "        {'op': 'dwconv5x5', 'exp': 6, 'channels': 40, 'bits': 8},",
        "        {'op': 'dwconv3x3', 'exp': 6, 'channels': 40, 'bits': 8, 'se': True},",
        "    ],",
        "    'stage3': [",
        "        {'op': 'conv3x3', 'exp': 6, 'channels': 80, 'bits': 8},",
        "        {'op': 'dwconv5x5', 'exp': 6, 'channels': 112, 'bits': 8, 'se': True},",
        "    ],",
        "    'head': {'op': 'conv1x1', 'channels': 1280, 'bits': 8},",
        "}",
    ]
    y = add_code_block(p, code3, y)

    # Pages 21-22: Ablation Study
    p = new_page()
    y = 72
    y = add_header(p, "4.3 Ablation Study", y, fontsize=14, fontname="hebo")
    abl_text = (
        "We conduct ablation studies to understand the contribution of each component in our "
        "framework. Table 6 shows the impact of removing individual components from the full "
        "AdaptiveNAS pipeline."
    )
    add_body(p, abl_text, y)

    y = 230
    abl_headers = ["Configuration", "Top-1(%)", "Lat(ms)", "Search(h)"]
    abl_data = [
        ["Full AdaptiveNAS", "94.7", "4.8", "7.5"],
        ["w/o joint quant search", "93.9", "5.4", "5.2"],
        ["w/o hardware-aware obj", "94.2", "7.1", "6.8"],
        ["w/o hierarchical space", "93.5", "5.1", "9.3"],
        ["w/o transfer module", "94.7", "4.8", "32.0"],
        ["Fixed 8-bit quant", "94.1", "5.9", "6.1"],
        ["Random search baseline", "91.8", "6.3", "7.5"],
    ]
    y = add_table(p, abl_headers, abl_data, y, [200, 80, 80, 108])
    y += 5
    add_body(p, "Table 6: Ablation study on CIFAR-10. Each row removes one component from the full method.", y, fontsize=9, fontname="tiit")

    y += 30
    abl_text2 = (
        "The results confirm that joint quantization search contributes 0.8% accuracy improvement "
        "and 0.6ms latency reduction. The hardware-aware objective prevents latency violations "
        "without significantly impacting search cost. The hierarchical search space improves both "
        "accuracy and search efficiency by enabling coarse-to-fine exploration."
    )
    add_body(p, abl_text2, y)

    p = new_page()
    y = 72
    y = add_figure_placeholder(p, "Ablation: contribution of each component to accuracy-latency trade-off", 5, y)
    y += 20
    abl_text3 = (
        "We also analyze the sensitivity to key hyperparameters. The latency penalty coefficient "
        "\u03bb has the most significant impact: values below 0.1 lead to latency violations, "
        "while values above 1.0 overly constrain the search space. The optimal range is "
        "\u03bb \u2208 [0.3, 0.5] across all evaluated scenarios."
    )
    add_body(p, abl_text3, y)
    y = 380
    y = add_equation(p, "\u0394Acc/\u0394\u03bb = -2.3\u00b7\u03bb + 0.95,  R\u00b2 = 0.94", y, 11)
    y += 10
    sens_text = (
        "The memory penalty coefficient \u03bc shows similar behavior with an optimal range of "
        "[0.2, 0.4]. The SE reduction ratio r = 4 consistently outperforms other choices across "
        "all architectures and datasets, consistent with findings in [50]."
    )
    add_body(p, sens_text, y)

    # ======================= PAGES 23-25: Discussion =======================
    p = new_page()
    y = 72
    y = add_header(p, "5. Discussion", y, fontsize=18)
    disc_text = (
        "Our results demonstrate that joint architecture-quantization search is a powerful "
        "paradigm for edge deployment. However, several limitations and future directions merit "
        "discussion. First, our current search space focuses on convolutional architectures and "
        "does not include transformer-based operations [28], [51]. Extending the search space "
        "to include attention mechanisms would enable discovery of hybrid architectures that "
        "may offer superior accuracy-efficiency trade-offs."
    )
    add_body(p, disc_text, y)
    y = 310
    disc_text2 = (
        "Second, our latency estimation relies on pre-measured lookup tables, which must be "
        "reconstructed for each new device. Developing universal latency predictors [52] that "
        "generalize across hardware platforms would significantly reduce the overhead of "
        "supporting new devices. Third, the current framework does not consider dynamic "
        "inference scenarios where different inputs may benefit from different compute budgets. "
        "Integrating early-exit mechanisms [53] or dynamic channel allocation [54] could further "
        "improve real-world efficiency."
    )
    add_body(p, disc_text2, y)

    p = new_page()
    y = 72
    disc_text3 = (
        "The energy consumption of the search process itself is a growing concern [55]. While "
        "our method reduces search cost by 3.2x compared to baseline NAS methods, the overall "
        "carbon footprint of architecture search remains significant. Future work should explore "
        "zero-shot NAS proxies [56] that can predict architecture quality without any training, "
        "potentially reducing search energy by orders of magnitude."
    )
    add_body(p, disc_text3, y)
    y = 280
    y = add_equation(p, "E\u209b\u2091\u2090\u1d63\u1d64\u2095 = P\u1d9e\u1d56\u1d58 \u00d7 T\u209b\u2091\u2090\u1d63\u1d64\u2095 \u00d7 PUE \u00d7 C\u1d62", y, 12)
    y += 10
    energy_text = (
        "where P denotes GPU power consumption, T is search duration, PUE is the data center "
        "power usage effectiveness, and C\u1d62 is the regional carbon intensity. For our method "
        "on 4 V100 GPUs, E \u2248 7.5h \u00d7 1.2kW \u00d7 1.1 \u00d7 0.475 kg/kWh \u2248 4.7 kg CO\u2082."
    )
    add_body(p, energy_text, y)

    y = 480
    disc_text4 = (
        "Despite these limitations, AdaptiveNAS represents a practical and effective approach "
        "for automated edge model design. The combination of joint search, hardware awareness, "
        "and cross-platform transfer addresses the key pain points in deploying neural networks "
        "on heterogeneous edge devices [57], [58]."
    )
    add_body(p, disc_text4, y)

    p = new_page()
    y = 72
    disc_text5 = (
        "An interesting finding from our experiments is the emergence of architecture patterns "
        "that correlate with device characteristics. ARM-targeted architectures favor depthwise "
        "convolutions while GPU-targeted ones prefer standard convolutions. This suggests that "
        "the traditional one-size-fits-all approach to model design is fundamentally limited, "
        "and device-aware architecture search will become increasingly important as the edge "
        "computing ecosystem continues to diversify."
    )
    add_body(p, disc_text5, y)
    y = 300
    y = add_figure_placeholder(p, "Architecture pattern analysis across different target platforms", 6, y)

    # ======================= PAGES 26-27: Conclusion =======================
    p = new_page()
    y = 72
    y = add_header(p, "6. Conclusion", y, fontsize=18)
    concl_text = (
        "We presented AdaptiveNAS, a unified framework for joint architecture and quantization "
        "search targeting heterogeneous edge devices. Our approach introduces a differentiable "
        "hierarchical search space, a hardware-aware multi-objective function, and a transfer "
        "mechanism for rapid adaptation to new platforms. Extensive experiments on CIFAR-10, "
        "ImageNet, and EdgeBench demonstrate that AdaptiveNAS achieves state-of-the-art "
        "accuracy-efficiency trade-offs across multiple hardware platforms."
    )
    add_body(p, concl_text, y)
    y = 330
    concl_text2 = (
        "Key findings include: (1) Joint architecture-quantization search yields 0.8-1.2% "
        "accuracy improvement over sequential approaches at equivalent latency. (2) Hardware-aware "
        "optimization prevents latency violations while maintaining search quality. (3) Cross-platform "
        "transfer reduces search cost by 4-6x for new devices. (4) The discovered architectures "
        "exhibit device-specific patterns that validate the need for hardware-aware design [59]."
    )
    add_body(p, concl_text2, y)
    y = 530
    concl_text3 = (
        "Future work will explore extending the search space to include transformer operations, "
        "developing universal latency predictors, and integrating dynamic inference capabilities. "
        "We will also investigate the application of AdaptiveNAS to other domains including "
        "object detection [60], semantic segmentation [61], and speech recognition [62] on "
        "edge devices."
    )
    add_body(p, concl_text3, y)

    p = new_page()
    y = 72
    y = add_header(p, "Acknowledgments", y, fontsize=14)
    ack_text = (
        "This work was supported by the National Science Foundation under Grant No. CNS-2145678 "
        "and the DARPA TRADES program under Agreement No. HR00112090091. We thank the anonymous "
        "reviewers for their constructive feedback. Computational resources were provided by "
        "the Stanford Research Computing Center and Google Cloud Research Credits program."
    )
    add_body(p, ack_text, y)

    # ======================= PAGES 28-30: References =======================
    # Page 28
    p = new_page()
    y = 72
    y = add_header(p, "References", y, fontsize=18)
    all_refs = [
        "[1] E. Vasquez et al., \"Latency-aware architecture search for mobile inference,\" Proc. CVPR, 2024.",
        "[2] H. Tanaka and P. Sharma, \"Efficient NAS with progressive shrinking,\" Proc. NeurIPS, 2023.",
        "[3] D. Mueller et al., \"Benchmarking edge neural networks,\" IEEE Trans. Mobile Comput., 2024.",
        "[4] A. Howard et al., \"Searching for MobileNetV3,\" Proc. ICCV, 2019.",
        "[5] B. Zoph and Q. Le, \"Neural architecture search with RL,\" Proc. ICLR, 2017.",
        "[6] T. Elsken et al., \"Neural architecture search: A survey,\" JMLR, vol. 20, 2019.",
        "[7] D. Stamoulis et al., \"Single-path NAS,\" Proc. ECCV, 2020.",
        "[8] N. Benmeziane et al., \"Hardware-aware NAS survey,\" arXiv:2101.09336, 2021.",
        "[9] Y. He and S. Lin, \"AMC: AutoML for model compression,\" Proc. ECCV, 2018.",
        "[10] H. Liu et al., \"DARTS: Differentiable architecture search,\" Proc. ICLR, 2019.",
        "[11] C. Ying et al., \"NAS-Bench-101,\" Proc. ICML, 2019.",
        "[12] X. Dong and Y. Yang, \"NAS-Bench-201,\" Proc. ICLR, 2020.",
        "[13] M. Tan and Q. Le, \"EfficientNet,\" Proc. ICML, 2019.",
        "[14] R. Shin et al., \"Differentiable NAS with compact representation,\" Proc. NeurIPS, 2018.",
        "[15] K. Wang et al., \"HAQ: Hardware-aware automated quantization,\" Proc. CVPR, 2019.",
        "[16] G. Li et al., \"Random search and reproducibility for NAS,\" Proc. UAI, 2020.",
        "[17] A. Brock et al., \"SMASH: One-shot model architecture search,\" Proc. ICLR, 2018.",
        "[18] B. Zoph et al., \"Learning transferable architectures,\" Proc. CVPR, 2018.",
        "[19] E. Real et al., \"Regularized evolution for image classifiers,\" Proc. AAAI, 2019.",
        "[20] C. White et al., \"BANANAS: Bayesian optimization with NAS,\" Proc. NeurIPS, 2021.",
        "[21] H. Liu et al., \"Hierarchical representations for efficient NAS,\" Proc. ICLR, 2018.",
        "[22] H. Liu et al., \"DARTS: Differentiable architecture search,\" Proc. ICLR, 2019.",
        "[23] H. Cai et al., \"ProxylessNAS,\" Proc. ICLR, 2019.",
        "[24] G. Bender et al., \"Understanding and simplifying one-shot NAS,\" Proc. ICML, 2018.",
        "[25] H. Cai et al., \"Once-for-All: Train one network for all,\" Proc. ICLR, 2020.",
        "[26] A. Howard et al., \"MobileNets,\" arXiv:1704.04861, 2017.",
        "[27] N. Ma et al., \"ShuffleNet V2,\" Proc. ECCV, 2018.",
        "[28] A. Dosovitskiy et al., \"An image is worth 16x16 words,\" Proc. ICLR, 2021.",
        "[29] S. Mehta and M. Rastegari, \"MobileViT,\" Proc. ICLR, 2022.",
        "[30] G. Hinton et al., \"Distilling the knowledge in a neural network,\" arXiv:1503.02531, 2015.",
        "[31] T. He et al., \"Filter pruning via geometric median,\" Proc. CVPR, 2019.",
        "[32] M. Tan et al., \"MnasNet,\" Proc. CVPR, 2019.",
        "[33] B. Wu et al., \"FBNet,\" Proc. CVPR, 2019.",
        "[34] X. Dai et al., \"ChamNet,\" Proc. CVPR, 2019.",
        "[35] T. Yang et al., \"NetAdapt,\" Proc. ECCV, 2018.",
        "[36] M. Nagel et al., \"A white paper on neural network quantization,\" arXiv:2106.08295, 2021.",
        "[37] K. Wang et al., \"HAQ,\" Proc. CVPR, 2019.",
        "[38] Z. Dong et al., \"HAWQ,\" Proc. ICCV, 2019.",
        "[39] R. Gong et al., \"Differentiable soft quantization,\" Proc. ICML, 2019.",
        "[40] B. Wu et al., \"Mixed precision quantization of ConvNets via DRL,\" Proc. ICLR, 2019.",
    ]
    for ref in all_refs[:20]:
        p.insert_text(pymupdf.Point(MARGIN, y), ref,
                      fontsize=8.5, fontname="tiro", color=(0, 0, 0))
        y += 14

    # Page 29
    p = new_page()
    y = 72
    for ref in all_refs[20:40]:
        p.insert_text(pymupdf.Point(MARGIN, y), ref,
                      fontsize=8.5, fontname="tiro", color=(0, 0, 0))
        y += 14

    remaining_refs = [
        "[41] Y. Xu et al., \"PC-DARTS: Partial channel connections for memory-efficient NAS,\" Proc. ICLR, 2020.",
        "[42] X. Chen et al., \"Progressive DARTS,\" Proc. ICCV, 2019.",
        "[43] M. Sandler et al., \"MobileNetV2,\" Proc. CVPR, 2018.",
        "[44] N. Ma et al., \"ShuffleNet V2,\" Proc. ECCV, 2018.",
        "[45] T. Wang et al., \"APQ: Joint search for network architecture, pruning, and quantization,\" Proc. CVPR, 2020.",
        "[46] Z. Shen et al., \"DQ-NAS: Discovering quant-friendly architectures,\" arXiv:2105.02094, 2021.",
        "[47] S. Han et al., \"Deep compression,\" Proc. ICLR, 2016.",
        "[48] S. Shwartz-Ziv and N. Tishby, \"Opening the black box of DNNs via information,\" arXiv:1703.00810, 2017.",
        "[49] R. Novak et al., \"Sensitivity and generalization in neural networks,\" Proc. ICLR, 2018.",
        "[50] J. Hu et al., \"Squeeze-and-Excitation networks,\" Proc. CVPR, 2018.",
        "[51] H. Touvron et al., \"Training data-efficient image transformers,\" Proc. ICML, 2021.",
        "[52] C. Dudziak et al., \"BRP-NAS: Prediction-based NAS using GCNs,\" Proc. NeurIPS, 2020.",
        "[53] S. Teerapittayanon et al., \"BranchyNet: Fast inference via early exiting,\" Proc. ICPR, 2016.",
        "[54] J. Yu et al., \"Slimmable neural networks,\" Proc. ICLR, 2019.",
        "[55] E. Strubell et al., \"Energy and policy considerations for deep learning in NLP,\" Proc. ACL, 2019.",
        "[56] M. Lin et al., \"Zen-NAS: A zero-shot NAS for high-performance image classifiers,\" Proc. ICCV, 2021.",
        "[57] C. Li et al., \"Edge intelligence: Architectures, challenges, and applications,\" arXiv:2003.12172, 2020.",
        "[58] Z. Zhou et al., \"Edge intelligence: Paving the last mile of AI with edge computing,\" Proc. IEEE, 2019.",
        "[59] X. Jiang et al., \"Device-channel-spatial attention for mobile image classification,\" Proc. ECCV, 2020.",
        "[60] G. Ghiasi et al., \"NAS-FPN,\" Proc. CVPR, 2019.",
        "[61] C. Liu et al., \"Auto-DeepLab,\" Proc. CVPR, 2019.",
        "[62] S. Kim et al., \"Evolved Speech-Transformer,\" Proc. INTERSPEECH, 2020.",
    ]

    # Page 30
    p = new_page()
    y = 72
    for ref in remaining_refs:
        p.insert_text(pymupdf.Point(MARGIN, y), ref,
                      fontsize=8.5, fontname="tiro", color=(0, 0, 0))
        y += 14

    # ======================= Set TOC (Bookmarks) =======================
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 2],
        [1, "2. Related Work", 5],
        [2, "2.1 Neural Architecture Search", 5],
        [2, "2.2 Efficient Model Design", 6],
        [2, "2.3 Hardware-Aware Optimization", 6],
        [1, "3. Methodology", 8],
        [2, "3.1 Problem Formulation", 8],
        [2, "3.2 Search Space Design", 10],
        [2, "3.3 Optimization Algorithm", 12],
        [1, "4. Experiments", 15],
        [2, "4.1 Experimental Setup", 15],
        [2, "4.2 Results and Analysis", 17],
        [2, "4.3 Ablation Study", 21],
        [1, "5. Discussion", 23],
        [1, "6. Conclusion", 26],
        [1, "Acknowledgments", 27],
        [1, "References", 28],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Adaptive Neural Architecture Search for Edge Computing: A Comprehensive Study",
        "author": "Elena Vasquez, Hiroshi Tanaka, Priya Sharma, David Mueller",
        "subject": "Neural Architecture Search, Edge Computing, Deep Learning",
        "keywords": "NAS, edge computing, quantization, architecture search, deep learning",
        "creator": "Academic Paper Generator",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {doc.page_count if False else "30 pages (approx)"}')

    # Verify page count
    verify_doc = pymupdf.open(OUTPUT)
    pc = verify_doc.page_count
    verify_doc.close()
    print(f'Actual page count: {pc}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
