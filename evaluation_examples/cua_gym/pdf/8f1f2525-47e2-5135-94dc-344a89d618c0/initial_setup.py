"""
Initial Setup: Create a 10-page academic paper PDF with landscape-oriented figures on pages 5 and 6.
Task ID: pdf_res_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_030'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/landscape_figures.pdf'


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

    # --- Academic paper content across 10 pages ---

    # Page 1: Title page
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(150, 200), "Advances in Neural Architecture Search",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(160, 260), "for Efficient Image Classification",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 340), "Elena Vasquez, Rajesh Patel, Mei-Lin Wong",
                     fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(140, 380), "Department of Computer Science, Stanford University",
                     fontsize=11, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(200, 420), "Published: March 15, 2025",
                     fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))

    abstract_text = (
        "Abstract: Neural Architecture Search (NAS) has emerged as a powerful paradigm for automating "
        "the design of deep neural networks. In this paper, we present EfficientNAS, a novel framework "
        "that reduces the computational cost of architecture search by 73% while maintaining state-of-the-art "
        "accuracy on ImageNet, CIFAR-100, and Oxford Flowers-102. Our method combines progressive search "
        "space pruning with a lightweight performance predictor trained on architectural features. "
        "Experiments across 14 benchmark datasets demonstrate consistent improvements in both search "
        "efficiency and final model quality compared to DARTS, ENAS, and ProxylessNAS baselines."
    )
    page.insert_textbox(pymupdf.Rect(72, 480, 523, 700), abstract_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 2: Introduction
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "1. Introduction", fontsize=16, fontname="hebo", color=(0, 0, 0))
    intro_text = (
        "The design of neural network architectures has traditionally relied on human expertise and extensive "
        "trial-and-error experimentation. While hand-crafted architectures such as ResNet, VGG, and "
        "Inception have achieved remarkable success, the process of designing them requires significant "
        "domain knowledge and computational resources.\n\n"
        "Neural Architecture Search (NAS) addresses this limitation by automating the architecture design "
        "process. Early NAS methods, including those based on reinforcement learning and evolutionary "
        "algorithms, demonstrated the potential of automated design but required thousands of GPU hours. "
        "More recent approaches like DARTS introduced differentiable search, reducing search costs "
        "significantly.\n\n"
        "Despite these advances, current NAS methods still face several challenges: (1) the search space "
        "remains prohibitively large for complex tasks, (2) the correlation between proxy tasks and final "
        "performance is often weak, and (3) transferability across different datasets and hardware "
        "constraints remains limited.\n\n"
        "In this paper, we propose EfficientNAS, which addresses all three challenges through a novel "
        "combination of progressive search space pruning, a learned performance predictor, and "
        "hardware-aware optimization. Our key contributions are:\n\n"
        "  - A hierarchical search space reduction algorithm that prunes 85% of candidates in the first "
        "phase while retaining all top-performing architectures.\n"
        "  - A graph neural network-based performance predictor that achieves 0.94 rank correlation "
        "with true performance after training on only 200 architectures.\n"
        "  - A multi-objective optimization formulation that jointly optimizes accuracy, latency, and "
        "memory footprint for target deployment platforms."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 790), intro_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 3: Related Work
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "2. Related Work", fontsize=16, fontname="hebo", color=(0, 0, 0))
    related_text = (
        "2.1 Reinforcement Learning-Based NAS\n\n"
        "Zoph and Le (2017) pioneered the use of reinforcement learning for architecture search, "
        "using a recurrent neural network controller to generate architecture descriptions. While "
        "achieving competitive results on CIFAR-10 and Penn Treebank, the method required 800 GPUs "
        "running for 28 days. Baker et al. (2017) proposed MetaQNN, using Q-learning to sequentially "
        "select CNN layers, reducing the search cost but still requiring substantial computation.\n\n"
        "2.2 Evolutionary Methods\n\n"
        "Real et al. (2019) demonstrated that evolutionary algorithms can match or exceed RL-based "
        "approaches for NAS. AmoebaNet achieved state-of-the-art results on ImageNet using regularized "
        "evolution with tournament selection. Liu et al. (2018) proposed a hierarchical evolution "
        "strategy that builds architectures from simple motifs to complex structures.\n\n"
        "2.3 Differentiable Architecture Search\n\n"
        "DARTS (Liu et al., 2019) reformulated the discrete search problem as a continuous optimization "
        "by relaxing the categorical choice of operations using softmax. This enabled gradient-based "
        "optimization, reducing search time to a single GPU day. However, DARTS suffers from instability "
        "issues, often converging to skip-connection-dominated architectures.\n\n"
        "2.4 One-Shot and Weight-Sharing Methods\n\n"
        "One-shot methods train a single supernet that shares weights across all candidate architectures. "
        "ENAS (Pham et al., 2018) and FairNAS (Chu et al., 2021) use this paradigm to dramatically "
        "reduce search costs. ProxylessNAS (Cai et al., 2019) extended this to directly search on "
        "target tasks and hardware platforms."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 790), related_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 4: Methodology
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "3. Methodology", fontsize=16, fontname="hebo", color=(0, 0, 0))
    method_text = (
        "3.1 Search Space Definition\n\n"
        "We define a cell-based search space consisting of two types of cells: normal cells and "
        "reduction cells. Each cell is a directed acyclic graph (DAG) with N=7 nodes. The candidate "
        "operation set includes: 3x3 separable convolution, 5x5 separable convolution, 3x3 dilated "
        "convolution, 3x3 max pooling, 3x3 average pooling, identity (skip connection), and zero "
        "(no connection).\n\n"
        "The total search space contains approximately 1.8 x 10^18 possible architectures, making "
        "exhaustive evaluation infeasible.\n\n"
        "3.2 Progressive Search Space Pruning\n\n"
        "Our progressive pruning algorithm operates in three phases:\n\n"
        "Phase 1 (Coarse Filter): We train a lightweight proxy model on each operation independently "
        "and rank operations by their standalone performance. Operations consistently performing below "
        "the 20th percentile are removed from the search space.\n\n"
        "Phase 2 (Pairwise Analysis): We evaluate all remaining pairwise operation combinations at each "
        "edge. Combinations with negative synergy scores are pruned, reducing the space by an "
        "additional 60%.\n\n"
        "Phase 3 (Fine-Grained Search): The remaining search space (approximately 2.7 x 10^10 "
        "architectures) is explored using our learned performance predictor combined with evolutionary "
        "search.\n\n"
        "3.3 Performance Predictor\n\n"
        "We train a Graph Neural Network (GNN) to predict architecture performance from graph "
        "structure. The predictor takes as input the adjacency matrix and operation encodings of "
        "a candidate architecture and outputs predicted accuracy, latency, and parameter count."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 790), method_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 5: Landscape figure (search space visualization) - portrait page with landscape content
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "Figure 1: Search Space Visualization",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    # Draw a landscape-oriented figure (wide chart) sideways on a portrait page
    shape = page.new_shape()

    # Figure border
    shape.draw_rect(pymupdf.Rect(80, 100, 515, 750))
    shape.finish(color=(0.5, 0.5, 0.5), width=1)

    # Draw bars (performance comparison chart - rotated 90 degrees to simulate landscape)
    bar_data = [
        ("ResNet-50", 0.76, (0.2, 0.4, 0.8)),
        ("VGG-19", 0.72, (0.3, 0.5, 0.8)),
        ("Inception-v3", 0.78, (0.2, 0.6, 0.7)),
        ("DARTS", 0.81, (0.8, 0.4, 0.2)),
        ("ENAS", 0.79, (0.8, 0.5, 0.3)),
        ("ProxylessNAS", 0.80, (0.7, 0.3, 0.3)),
        ("AmoebaNet", 0.82, (0.6, 0.2, 0.6)),
        ("EfficientNAS", 0.85, (0.1, 0.7, 0.2)),
    ]
    bar_width = 50
    start_y = 140
    for i, (name, val, color) in enumerate(bar_data):
        y = start_y + i * 70
        bar_len = val * 400
        shape.draw_rect(pymupdf.Rect(120, y, 120 + bar_len, y + bar_width))
        shape.finish(color=color, fill=color, width=0.5)
        page.insert_text(pymupdf.Point(125, y + 35), f"{name} ({val:.2f})",
                         fontsize=9, fontname="helv", color=(1, 1, 1))

    # Axis labels
    page.insert_text(pymupdf.Point(200, 780), "Top-1 Accuracy on ImageNet",
                     fontsize=10, fontname="tibo", color=(0, 0, 0))

    shape.commit()

    # Page 6: Another landscape figure (latency vs accuracy scatter)
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "Figure 2: Accuracy vs. Inference Latency",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()

    # Figure border
    shape.draw_rect(pymupdf.Rect(80, 100, 515, 750))
    shape.finish(color=(0.5, 0.5, 0.5), width=1)

    # Draw scatter plot points (accuracy vs latency)
    scatter_data = [
        (150, 380, "ResNet-50", (0.2, 0.4, 0.8)),
        (200, 420, "VGG-19", (0.3, 0.5, 0.8)),
        (120, 350, "Inception-v3", (0.2, 0.6, 0.7)),
        (100, 310, "DARTS", (0.8, 0.4, 0.2)),
        (130, 330, "ENAS", (0.8, 0.5, 0.3)),
        (110, 320, "ProxylessNAS", (0.7, 0.3, 0.3)),
        (95, 300, "AmoebaNet", (0.6, 0.2, 0.6)),
        (80, 250, "EfficientNAS", (0.1, 0.7, 0.2)),
    ]
    for x_off, y_pos, name, color in scatter_data:
        cx = 120 + x_off * 2
        cy = y_pos
        shape.draw_circle(pymupdf.Point(cx, cy), 12)
        shape.finish(color=color, fill=color, width=1)
        page.insert_text(pymupdf.Point(cx + 15, cy + 4), name,
                         fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))

    # Axis labels
    page.insert_text(pymupdf.Point(220, 780), "Inference Latency (ms) vs Accuracy",
                     fontsize=10, fontname="tibo", color=(0, 0, 0))

    # Draw axes
    shape.draw_line(pymupdf.Point(120, 720), pymupdf.Point(500, 720))
    shape.finish(color=(0, 0, 0), width=1)
    shape.draw_line(pymupdf.Point(120, 150), pymupdf.Point(120, 720))
    shape.finish(color=(0, 0, 0), width=1)

    shape.commit()

    # Page 7: Experimental Setup
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "4. Experimental Setup", fontsize=16, fontname="hebo", color=(0, 0, 0))
    exp_text = (
        "4.1 Datasets\n\n"
        "We evaluate EfficientNAS on the following benchmarks:\n\n"
        "  - ImageNet (ILSVRC 2012): 1.28M training images, 50K validation images, 1000 classes.\n"
        "  - CIFAR-100: 50K training images, 10K test images, 100 classes.\n"
        "  - Oxford Flowers-102: 8,189 images across 102 flower categories.\n"
        "  - Stanford Cars: 16,185 images across 196 car classes.\n"
        "  - FGVC Aircraft: 10,000 images across 100 aircraft variants.\n\n"
        "4.2 Search Configuration\n\n"
        "Architecture search is conducted on CIFAR-100 using 8 NVIDIA A100 GPUs with a batch size "
        "of 256. The search takes approximately 4.2 GPU hours for the progressive pruning phase and "
        "1.8 GPU hours for the fine-grained evolutionary search. The performance predictor is trained "
        "on 200 fully-evaluated architectures sampled uniformly from the reduced search space.\n\n"
        "4.3 Training Protocol\n\n"
        "Discovered architectures are retrained from scratch using the following hyperparameters:\n"
        "  - Optimizer: SGD with momentum 0.9 and weight decay 3e-4\n"
        "  - Learning rate: cosine annealing from 0.025 to 0.001 over 600 epochs\n"
        "  - Data augmentation: Cutout, AutoAugment, Random Erasing\n"
        "  - Regularization: ScheduledDropPath with max rate 0.3\n\n"
        "4.4 Baselines\n\n"
        "We compare against: DARTS (Liu et al., 2019), ENAS (Pham et al., 2018), ProxylessNAS "
        "(Cai et al., 2019), AmoebaNet (Real et al., 2019), FairNAS (Chu et al., 2021), "
        "and SNAS (Xie et al., 2019)."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 790), exp_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 8: Results Table
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "5. Results", fontsize=16, fontname="hebo", color=(0, 0, 0))

    results_text = (
        "Table 1 summarizes the performance of EfficientNAS compared to baseline methods across "
        "all benchmark datasets. Our method consistently achieves superior or competitive accuracy "
        "while requiring significantly fewer search GPU hours.\n\n"
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 140), results_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Draw results table
    shape = page.new_shape()
    table_top = 160
    row_h = 28
    cols = [72, 180, 270, 360, 450, 523]
    headers = ["Method", "ImageNet", "CIFAR-100", "Search Cost", "Params"]
    data_rows = [
        ["DARTS", "73.3%", "82.5%", "4.0 days", "3.3M"],
        ["ENAS", "71.9%", "80.6%", "0.5 days", "4.6M"],
        ["ProxylessNAS", "74.6%", "83.1%", "8.3 hrs", "5.1M"],
        ["AmoebaNet", "74.0%", "83.9%", "7.0 days", "3.2M"],
        ["FairNAS", "73.8%", "82.9%", "12.0 hrs", "4.6M"],
        ["SNAS", "72.7%", "81.3%", "1.5 days", "2.8M"],
        ["EfficientNAS", "75.8%", "84.7%", "6.0 hrs", "3.8M"],
    ]

    # Header row
    shape.draw_rect(pymupdf.Rect(cols[0], table_top, cols[-1], table_top + row_h))
    shape.finish(color=(0, 0, 0), fill=(0.15, 0.25, 0.45), width=0.5)
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i] + 5, table_top + 19), h,
                         fontsize=9, fontname="hebo", color=(1, 1, 1))

    # Data rows
    for r, row_data in enumerate(data_rows):
        y = table_top + (r + 1) * row_h
        fill = (0.95, 0.95, 0.95) if r % 2 == 0 else (1, 1, 1)
        shape.draw_rect(pymupdf.Rect(cols[0], y, cols[-1], y + row_h))
        shape.finish(color=(0.7, 0.7, 0.7), fill=fill, width=0.5)
        fontname = "hebo" if row_data[0] == "EfficientNAS" else "helv"
        for i, val in enumerate(row_data):
            page.insert_text(pymupdf.Point(cols[i] + 5, y + 19), val,
                             fontsize=9, fontname=fontname, color=(0, 0, 0))

    shape.commit()

    discussion_text = (
        "\nAs shown in Table 1, EfficientNAS achieves 75.8% top-1 accuracy on ImageNet, "
        "outperforming all baselines. On CIFAR-100, our method reaches 84.7%, surpassing the "
        "previous best (AmoebaNet, 83.9%) while requiring only 6.0 GPU hours for search compared "
        "to AmoebaNet's 7.0 GPU days. The discovered architecture uses 3.8M parameters, striking "
        "an effective balance between model capacity and efficiency."
    )
    page.insert_textbox(pymupdf.Rect(72, table_top + 8 * row_h + 20, 523, 790), discussion_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 9: Ablation Studies
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "6. Ablation Studies", fontsize=16, fontname="hebo", color=(0, 0, 0))
    ablation_text = (
        "6.1 Impact of Progressive Pruning\n\n"
        "To isolate the contribution of each pruning phase, we evaluate search performance with "
        "different subsets of our pruning pipeline. Removing Phase 1 (coarse filter) increases search "
        "time by 4.2x while improving accuracy by only 0.1%. Removing Phase 2 (pairwise analysis) "
        "increases search time by 2.1x with no measurable accuracy improvement. This confirms that "
        "our progressive strategy effectively eliminates low-quality regions of the search space.\n\n"
        "6.2 Performance Predictor Analysis\n\n"
        "We study how the number of training architectures affects predictor quality. With only 50 "
        "training samples, the predictor achieves 0.82 Kendall tau correlation. At 100 samples, "
        "correlation reaches 0.89, and at 200 samples, it saturates at 0.94. Beyond 200 samples, "
        "marginal improvements are negligible, suggesting our training budget is near-optimal.\n\n"
        "6.3 Hardware-Aware Optimization\n\n"
        "When targeting mobile deployment (Pixel 6 Pro), EfficientNAS discovers architectures with "
        "3.2ms inference latency at 74.1% ImageNet accuracy. For edge TPU deployment, the framework "
        "finds architectures achieving 73.8% accuracy with 1.1ms latency. These results demonstrate "
        "the effectiveness of our multi-objective optimization across diverse hardware targets.\n\n"
        "6.4 Transferability\n\n"
        "Architectures discovered on CIFAR-100 transfer well to other datasets: Oxford Flowers-102 "
        "(96.3% accuracy), Stanford Cars (94.7%), and FGVC Aircraft (92.1%). Fine-tuning the "
        "architecture on each target dataset provides an additional 0.3-0.8% improvement over "
        "direct transfer."
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 790), ablation_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 10: Conclusion and References
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "7. Conclusion", fontsize=16, fontname="hebo", color=(0, 0, 0))
    conclusion_text = (
        "We have presented EfficientNAS, a neural architecture search framework that combines "
        "progressive search space pruning with a learned performance predictor. Our approach reduces "
        "search cost by 73% compared to DARTS while achieving state-of-the-art accuracy across "
        "14 benchmark datasets. The multi-objective optimization capability enables deployment-aware "
        "architecture design for diverse hardware platforms.\n\n"
        "Future work includes extending EfficientNAS to additional modalities (NLP, speech, video), "
        "incorporating neural architecture distillation for further efficiency gains, and developing "
        "online adaptation mechanisms for continual architecture improvement.\n\n"
    )
    page.insert_textbox(pymupdf.Rect(72, 80, 523, 300), conclusion_text,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 330), "References", fontsize=14, fontname="hebo", color=(0, 0, 0))
    refs = [
        "[1] Zoph, B., Le, Q.V. (2017). Neural Architecture Search with Reinforcement Learning. ICLR.",
        "[2] Liu, H., Simonyan, K., Yang, Y. (2019). DARTS: Differentiable Architecture Search. ICLR.",
        "[3] Pham, H., et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. ICML.",
        "[4] Real, E., et al. (2019). Regularized Evolution for Image Classifier Architecture Search. AAAI.",
        "[5] Cai, H., Zhu, L., Han, S. (2019). ProxylessNAS: Direct NAS without Proxy. ICLR.",
        "[6] Baker, B., et al. (2017). Designing Neural Network Architectures using RL. ICLR.",
        "[7] Chu, X., et al. (2021). FairNAS: Rethinking Evaluation Fairness of Weight Sharing NAS. ICCV.",
        "[8] Xie, S., et al. (2019). SNAS: Stochastic Neural Architecture Search. ICLR.",
        "[9] Liu, H., et al. (2018). Hierarchical Representations for Efficient Architecture Search. ICLR.",
    ]
    ref_text = "\n\n".join(refs)
    page.insert_textbox(pymupdf.Rect(72, 350, 523, 790), ref_text,
                        fontsize=9, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_LEFT)

    # Set TOC
    toc = [
        [1, "Title", 1],
        [1, "1. Introduction", 2],
        [1, "2. Related Work", 3],
        [1, "3. Methodology", 4],
        [1, "Figure 1: Search Space Visualization", 5],
        [1, "Figure 2: Accuracy vs. Inference Latency", 6],
        [1, "4. Experimental Setup", 7],
        [1, "5. Results", 8],
        [1, "6. Ablation Studies", 9],
        [1, "7. Conclusion", 10],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Advances in Neural Architecture Search for Efficient Image Classification",
        "author": "Elena Vasquez, Rajesh Patel, Mei-Lin Wong",
        "subject": "Neural Architecture Search",
        "keywords": "NAS, deep learning, architecture search, image classification",
        "creator": "LaTeX",
        "producer": "pdfTeX",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
