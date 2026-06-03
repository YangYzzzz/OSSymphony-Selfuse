"""
Initial Setup: Create an 8-page accepted academic paper PDF
Task ID: pdf_res_053
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_053'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/camera_ready.pdf'


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

    # --- Page 1: Title page ---
    page = doc.new_page(width=612, height=792)
    # Title
    page.insert_text(
        pymupdf.Point(72, 120),
        "Efficient Neural Architecture Search via",
        fontsize=20, fontname="tibo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 148),
        "Progressive Differentiable Optimization",
        fontsize=20, fontname="tibo", color=(0, 0, 0),
    )
    # Authors
    page.insert_text(
        pymupdf.Point(72, 195),
        "Wei Zhang, Sarah Chen, Raj Patel, Maria Lopez",
        fontsize=12, fontname="tiro", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 215),
        "Department of Computer Science, Stanford University",
        fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 232),
        "{wzhang, schen, rpatel, mlopez}@cs.stanford.edu",
        fontsize=10, fontname="cour", color=(0.2, 0.2, 0.6),
    )
    # Abstract
    page.insert_text(
        pymupdf.Point(72, 280),
        "Abstract",
        fontsize=14, fontname="tibo", color=(0, 0, 0),
    )
    abstract_rect = pymupdf.Rect(72, 300, 540, 480)
    page.insert_textbox(
        abstract_rect,
        "Neural Architecture Search (NAS) has emerged as a powerful paradigm for automating "
        "the design of deep neural networks. However, existing methods often suffer from "
        "prohibitive computational costs or limited search space expressiveness. In this paper, "
        "we propose Progressive Differentiable Optimization (PDO), a novel NAS framework that "
        "progressively expands the search space while maintaining computational efficiency through "
        "differentiable relaxation. Our method achieves state-of-the-art results on CIFAR-10 "
        "(97.8% accuracy), CIFAR-100 (85.3% accuracy), and ImageNet (79.2% top-1 accuracy) "
        "while reducing the search cost by 3.7x compared to DARTS. We further demonstrate the "
        "transferability of discovered architectures across diverse tasks including object "
        "detection and semantic segmentation.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Keywords
    page.insert_text(
        pymupdf.Point(72, 500),
        "Keywords: Neural Architecture Search, AutoML, Differentiable Optimization",
        fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3),
    )

    # --- Page 2: Introduction ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "1  Introduction", fontsize=16, fontname="tibo", color=(0, 0, 0))
    intro_rect = pymupdf.Rect(72, 100, 540, 750)
    page2.insert_textbox(
        intro_rect,
        "Deep neural networks have achieved remarkable success across a wide range of machine "
        "learning tasks, from image classification and natural language processing to robotics "
        "and scientific computing. However, designing effective network architectures remains a "
        "labor-intensive process that requires significant domain expertise and extensive "
        "experimentation.\n\n"
        "Neural Architecture Search (NAS) aims to automate this design process by searching "
        "for optimal architectures within a predefined search space. Early NAS methods based "
        "on reinforcement learning and evolutionary algorithms demonstrated impressive results "
        "but required thousands of GPU hours. Recent differentiable approaches such as DARTS "
        "have significantly reduced search costs by relaxing the discrete architecture choices "
        "into a continuous optimization problem.\n\n"
        "Despite these advances, several challenges remain. First, the one-shot search paradigm "
        "used by most differentiable NAS methods can lead to performance collapse when the "
        "search space is too large. Second, the architectures discovered on proxy tasks often "
        "fail to transfer to larger-scale problems. Third, existing methods typically optimize "
        "for a single objective (e.g., accuracy) without considering computational constraints.\n\n"
        "In this work, we propose Progressive Differentiable Optimization (PDO), which addresses "
        "these limitations through three key innovations: (1) a progressive search space expansion "
        "strategy that gradually increases complexity, (2) a multi-fidelity evaluation scheme that "
        "provides reliable performance estimates at reduced cost, and (3) a multi-objective "
        "optimization framework that jointly considers accuracy and efficiency.\n\n"
        "Our contributions can be summarized as follows:\n"
        "  - We introduce a progressive search strategy that stabilizes differentiable NAS by "
        "gradually expanding the operation set during search.\n"
        "  - We propose an efficient multi-fidelity evaluation protocol that reduces search cost "
        "by 3.7x compared to standard DARTS.\n"
        "  - We demonstrate state-of-the-art performance on multiple benchmarks while maintaining "
        "competitive computational efficiency.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Related Work ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "2  Related Work", fontsize=16, fontname="tibo", color=(0, 0, 0))
    rw_rect = pymupdf.Rect(72, 100, 540, 750)
    page3.insert_textbox(
        rw_rect,
        "2.1  Reinforcement Learning-based NAS\n\n"
        "Zoph and Le (2017) pioneered the use of reinforcement learning for architecture search, "
        "training a recurrent neural network controller to generate architecture descriptions. "
        "While this approach achieved state-of-the-art results on CIFAR-10, it required 800 GPUs "
        "for 28 days. NASNet improved efficiency by searching on a smaller proxy dataset and "
        "transferring the discovered cell structure. ENAS further reduced costs through parameter "
        "sharing among child models.\n\n"
        "2.2  Evolutionary Methods\n\n"
        "Evolutionary algorithms offer a natural framework for architecture search. Real et al. "
        "(2019) demonstrated that evolved architectures can match or exceed hand-designed ones. "
        "AmoebaNet achieved competitive results on ImageNet using regularized evolution. However, "
        "evolutionary methods still require substantial computational resources due to the need "
        "for training each candidate architecture.\n\n"
        "2.3  Differentiable Architecture Search\n\n"
        "DARTS (Liu et al., 2019) introduced a continuous relaxation of the discrete architecture "
        "search space, enabling gradient-based optimization. This reduced search cost from "
        "thousands of GPU hours to a single GPU day. Subsequent works have addressed various "
        "limitations of DARTS: P-DARTS proposed progressive search space shrinking, FairDARTS "
        "addressed the unfair advantage of skip connections, and GDAS improved search stability "
        "through Gumbel-Softmax sampling.\n\n"
        "2.4  One-Shot Methods\n\n"
        "One-shot NAS methods train a supernet that encompasses all candidate architectures, then "
        "derive the final architecture through pruning or sampling. Single-Path NAS trains only a "
        "single path at each step, while OFA (Once-for-All) supports multiple sub-networks at "
        "deployment time. These methods offer favorable trade-offs between search cost and "
        "architecture quality.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 4: Method (Part 1) ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 72), "3  Method", fontsize=16, fontname="tibo", color=(0, 0, 0))
    m1_rect = pymupdf.Rect(72, 100, 540, 750)
    page4.insert_textbox(
        m1_rect,
        "3.1  Search Space Definition\n\n"
        "We define our search space as a directed acyclic graph (DAG) where each node represents "
        "a latent feature representation and each edge represents a candidate operation. The "
        "operation set O includes: 3x3 separable convolution, 5x5 separable convolution, 3x3 "
        "dilated convolution, 3x3 max pooling, 3x3 average pooling, skip connection, and zero "
        "(no connection).\n\n"
        "Unlike standard DARTS which uses a fixed operation set throughout search, PDO starts "
        "with a minimal set O_0 = {skip, zero, 3x3 sep conv} and progressively adds operations "
        "at predefined intervals. This progressive expansion prevents the supernet from "
        "collapsing to degenerate solutions early in training.\n\n"
        "3.2  Progressive Differentiable Optimization\n\n"
        "Let alpha denote the architecture parameters that control the mixing weights of "
        "operations on each edge. The mixed output of edge (i,j) is computed as:\n\n"
        "    f_{i,j}(x) = sum_{o in O_t} [exp(alpha_o) / sum_{o'} exp(alpha_{o'})] * o(x)\n\n"
        "where O_t is the active operation set at stage t. The architecture parameters alpha "
        "and network weights w are optimized alternately using gradient descent:\n\n"
        "    w* = w - eta_w * grad_w L_train(w, alpha)\n"
        "    alpha* = alpha - eta_a * grad_alpha L_val(w*, alpha)\n\n"
        "At each progressive stage t, we expand O_t by adding the next group of operations. "
        "The architecture parameters for new operations are initialized to match the minimum "
        "existing value, ensuring they start with low probability and must prove their worth.\n\n"
        "3.3  Multi-Fidelity Evaluation\n\n"
        "To reduce evaluation cost, we employ a multi-fidelity scheme that uses shorter training "
        "runs to estimate architecture performance. Specifically, we train each candidate for "
        "only T_proxy = 50 epochs instead of the full T_full = 600 epochs. We use a learned "
        "performance predictor phi to map proxy performance to expected full performance:\n\n"
        "    perf_estimated = phi(perf_proxy, arch_features)",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 5: Method (Part 2) ---
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(pymupdf.Point(72, 72), "3.4  Multi-Objective Optimization", fontsize=14, fontname="tibo", color=(0, 0, 0))
    m2_rect = pymupdf.Rect(72, 100, 540, 750)
    page5.insert_textbox(
        m2_rect,
        "Real-world deployment often requires balancing accuracy with computational cost. We "
        "extend our framework to handle multiple objectives by incorporating latency and FLOPs "
        "into the optimization. The multi-objective loss is:\n\n"
        "    L_total = L_task + lambda_1 * L_latency + lambda_2 * L_flops\n\n"
        "where L_latency is estimated using a lookup table of per-operation latencies measured "
        "on the target hardware platform, and L_flops is computed analytically from the "
        "architecture parameters.\n\n"
        "We use a scalarization approach with adaptive weights that are adjusted during search "
        "to explore different regions of the Pareto front. This allows practitioners to select "
        "architectures that best match their deployment constraints.\n\n"
        "3.5  Architecture Derivation\n\n"
        "After search completes, we derive the discrete architecture by selecting the top-k "
        "operations per edge based on the learned architecture parameters alpha. Specifically, "
        "for each edge (i,j), we retain the two operations with the highest softmax probabilities "
        "(excluding zero). The resulting cell is then stacked to form the final network.\n\n"
        "For the progressive stages, we found that starting with k=1 and increasing to k=2 in "
        "the final stage yields the best results. This gradual increase in cell complexity "
        "mirrors the progressive expansion of the search space.\n\n"
        "4  Experiments\n\n"
        "4.1  Datasets and Setup\n\n"
        "We evaluate PDO on three standard benchmarks: CIFAR-10 (50K training, 10K test images, "
        "10 classes), CIFAR-100 (50K training, 10K test images, 100 classes), and ImageNet "
        "(1.28M training, 50K validation images, 1000 classes). For CIFAR experiments, we search "
        "on a network with 8 cells and 16 initial channels, then evaluate with 20 cells and 36 "
        "initial channels. For ImageNet, we transfer the cell discovered on CIFAR-10.\n\n"
        "Search is conducted on a single NVIDIA V100 GPU. We use SGD with momentum 0.9 for "
        "network weights and Adam with learning rate 3e-4 for architecture parameters. The "
        "progressive expansion occurs at epochs 10, 25, and 40 of the 50-epoch search phase.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 6: Results ---
    page6 = doc.new_page(width=612, height=792)
    page6.insert_text(pymupdf.Point(72, 72), "4.2  Main Results", fontsize=14, fontname="tibo", color=(0, 0, 0))
    r_rect = pymupdf.Rect(72, 100, 540, 400)
    page6.insert_textbox(
        r_rect,
        "Table 1 presents the comparison of PDO with existing NAS methods on CIFAR-10 and "
        "CIFAR-100. Our method achieves 97.8% test accuracy on CIFAR-10 with only 3.4M "
        "parameters and 0.3 GPU days of search cost. On CIFAR-100, PDO reaches 85.3% accuracy, "
        "surpassing all compared methods.\n\n"
        "Table 1: Comparison with state-of-the-art NAS methods\n\n"
        "Method          | CIFAR-10 | CIFAR-100 | Params | Search Cost\n"
        "NASNet-A        |  97.35%  |  83.18%   |  3.3M  |  1800 days\n"
        "AmoebaNet-A     |  96.66%  |  81.07%   |  3.2M  |  3150 days\n"
        "DARTS (2nd)     |  97.24%  |  82.46%   |  3.3M  |  1.0 days\n"
        "P-DARTS         |  97.50%  |  83.72%   |  3.4M  |  0.3 days\n"
        "FairDARTS       |  97.46%  |  84.17%   |  3.3M  |  0.4 days\n"
        "GDAS            |  97.07%  |  81.62%   |  3.4M  |  0.2 days\n"
        "PDO (Ours)      |  97.80%  |  85.30%   |  3.4M  |  0.3 days\n\n"
        "On ImageNet, PDO achieves 79.2% top-1 accuracy and 94.5% top-5 accuracy with 5.7M "
        "parameters, outperforming DARTS (73.3%) and P-DARTS (75.6%) by significant margins. "
        "The search cost on ImageNet is reduced to 0.8 GPU days when using the cell transferred "
        "from CIFAR-10.\n\n"
        "4.3  Ablation Study\n\n"
        "We conduct ablation studies to evaluate the contribution of each component. Removing "
        "the progressive expansion reduces CIFAR-10 accuracy from 97.80% to 97.31%, confirming "
        "that gradual search space growth is critical. Without multi-fidelity evaluation, search "
        "cost increases 4.2x with negligible accuracy improvement. The multi-objective variant "
        "discovers architectures that are 1.8x faster at inference with only 0.3% accuracy loss.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 7: Analysis and Discussion ---
    page7 = doc.new_page(width=612, height=792)
    page7.insert_text(pymupdf.Point(72, 72), "5  Analysis and Discussion", fontsize=16, fontname="tibo", color=(0, 0, 0))
    a_rect = pymupdf.Rect(72, 100, 540, 750)
    page7.insert_textbox(
        a_rect,
        "5.1  Visualization of Discovered Architectures\n\n"
        "Figure 2 visualizes the normal and reduction cells discovered by PDO. The normal cell "
        "exhibits a preference for separable convolutions with skip connections, creating an "
        "efficient feature extraction pattern. The reduction cell uses a combination of max "
        "pooling and dilated convolutions to effectively downsample spatial dimensions while "
        "preserving important features.\n\n"
        "5.2  Progressive Expansion Analysis\n\n"
        "Figure 3 tracks the architecture parameters throughout the search process. During the "
        "first stage (epochs 0-10), the network learns to effectively use skip connections and "
        "3x3 separable convolutions. When 5x5 convolutions are introduced at epoch 10, there "
        "is a brief adjustment period of approximately 3 epochs before the parameters stabilize. "
        "This validates our hypothesis that progressive expansion allows the network to "
        "incrementally adapt to increased complexity.\n\n"
        "5.3  Search Space Sensitivity\n\n"
        "We investigate how the order of operation introduction affects final performance. We "
        "find that starting with simpler operations (convolutions, skip) and adding complex ones "
        "(dilated convolutions, attention) later consistently outperforms the reverse order. "
        "Random ordering performs between these extremes, suggesting that curriculum-based "
        "expansion provides a useful inductive bias.\n\n"
        "5.4  Transferability\n\n"
        "To evaluate the transferability of discovered architectures, we apply PDO cells to "
        "object detection (MS-COCO) and semantic segmentation (Cityscapes). When used as the "
        "backbone in Faster R-CNN, PDO cells improve mAP by 1.2 points over the ResNet-50 "
        "baseline. On Cityscapes, replacing the backbone with PDO cells yields a 1.8% "
        "improvement in mean IoU, demonstrating strong transfer learning capability.\n\n"
        "5.5  Limitations\n\n"
        "Despite these promising results, PDO has several limitations. First, the progressive "
        "expansion schedule is currently hand-designed and may not be optimal for all search "
        "spaces. Second, the multi-fidelity predictor requires a warmup phase with full-length "
        "training runs. Third, our method has not been evaluated on non-vision domains such as "
        "NLP or speech, where the optimal search spaces may differ significantly.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 8: Conclusion and References ---
    page8 = doc.new_page(width=612, height=792)
    page8.insert_text(pymupdf.Point(72, 72), "6  Conclusion", fontsize=16, fontname="tibo", color=(0, 0, 0))
    c_rect = pymupdf.Rect(72, 100, 540, 280)
    page8.insert_textbox(
        c_rect,
        "We have presented Progressive Differentiable Optimization (PDO), a neural architecture "
        "search framework that achieves state-of-the-art performance through progressive search "
        "space expansion, multi-fidelity evaluation, and multi-objective optimization. PDO "
        "achieves 97.8% on CIFAR-10, 85.3% on CIFAR-100, and 79.2% on ImageNet while requiring "
        "only 0.3 GPU days of search. Future work will explore learned expansion schedules and "
        "extend PDO to non-vision domains.\n\n"
        "Acknowledgments: This work was supported by NSF Grant IIS-2024513 and a Google "
        "Faculty Research Award. We thank the anonymous reviewers for their constructive "
        "feedback.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page8.insert_text(pymupdf.Point(72, 310), "References", fontsize=14, fontname="tibo", color=(0, 0, 0))
    ref_rect = pymupdf.Rect(72, 335, 540, 750)
    page8.insert_textbox(
        ref_rect,
        "[1] Zoph, B. and Le, Q. V. Neural Architecture Search with Reinforcement Learning. "
        "ICLR 2017.\n\n"
        "[2] Liu, H., Simonyan, K., and Yang, Y. DARTS: Differentiable Architecture Search. "
        "ICLR 2019.\n\n"
        "[3] Real, E., Aggarwal, A., Huang, Y., and Le, Q. V. Regularized Evolution for Image "
        "Classifier Architecture Search. AAAI 2019.\n\n"
        "[4] Chen, X., Xie, L., Wu, J., and Tian, Q. Progressive Differentiable Architecture "
        "Search: Bridging the Depth Gap between Search and Evaluation. ICCV 2019.\n\n"
        "[5] Chu, X., Zhou, T., Zhang, B., and Li, J. Fair DARTS: Eliminating Unfair Advantages "
        "in Differentiable Architecture Search. ECCV 2020.\n\n"
        "[6] Dong, X. and Yang, Y. Searching for A Robust Neural Architecture in Four GPU Hours. "
        "CVPR 2019.\n\n"
        "[7] Cai, H., Gan, C., Wang, T., Zhang, Z., and Han, S. Once-for-All: Train One Network "
        "and Specialize it for Efficient Deployment. ICLR 2020.\n\n"
        "[8] Pham, H., Guan, M., Zoph, B., Le, Q., and Dean, J. Efficient Neural Architecture "
        "Search via Parameter Sharing. ICML 2018.",
        fontsize=9, fontname="tiro", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Efficient Neural Architecture Search via Progressive Differentiable Optimization",
        "author": "Wei Zhang, Sarah Chen, Raj Patel, Maria Lopez",
        "subject": "Neural Architecture Search",
        "keywords": "NAS, AutoML, deep learning, differentiable optimization",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Add table of contents / bookmarks
    toc = [
        [1, "Abstract", 1],
        [1, "1  Introduction", 2],
        [1, "2  Related Work", 3],
        [1, "3  Method", 4],
        [2, "3.4  Multi-Objective Optimization", 5],
        [1, "4  Experiments", 6],
        [1, "5  Analysis and Discussion", 7],
        [1, "6  Conclusion", 8],
        [1, "References", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
