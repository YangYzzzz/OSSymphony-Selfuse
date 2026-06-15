"""
Initial Setup: Create a 12-page manuscript PDF without line numbers.
Task ID: pdf_res_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_032'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/submission_draft.pdf'

# Manuscript content - realistic academic paper
TITLE = "Adaptive Neural Architecture Search for Resource-Constrained Edge Deployment"
AUTHORS = "Elena Vasquez, Rajiv Patel, Mei-Ling Zhou, and Thomas Bergmann"
AFFILIATION = "Department of Computer Science, Westfield Institute of Technology"

ABSTRACT = (
    "We present a novel approach to neural architecture search (NAS) that explicitly "
    "optimizes for deployment on resource-constrained edge devices. Our method, termed "
    "EdgeNAS, introduces a multi-objective search strategy that simultaneously considers "
    "model accuracy, inference latency, memory footprint, and energy consumption. Unlike "
    "previous NAS approaches that primarily focus on accuracy, EdgeNAS incorporates "
    "hardware-aware constraints directly into the search process through a differentiable "
    "surrogate model of the target hardware platform. We evaluate EdgeNAS across three "
    "benchmark datasets (ImageNet-1K, COCO-2017, and SpeechCommands-v2) and four edge "
    "hardware platforms (Raspberry Pi 4, NVIDIA Jetson Nano, Google Coral, and ARM Cortex-M7). "
    "Our results demonstrate that EdgeNAS achieves a 2.3x improvement in inference speed "
    "with less than 1.2% accuracy degradation compared to state-of-the-art manually designed "
    "architectures. Furthermore, we introduce a transfer learning mechanism that reduces "
    "the search cost by 67% when adapting to new hardware platforms. The discovered "
    "architectures exhibit consistent performance across diverse deployment scenarios, "
    "suggesting that hardware-aware NAS can bridge the gap between research-grade models "
    "and practical edge deployment requirements."
)

SECTIONS = {
    "1 Introduction": [
        (
            "The proliferation of edge computing devices has created an urgent need for "
            "efficient deep learning models that can operate within strict computational "
            "budgets. While modern neural networks achieve remarkable accuracy on benchmark "
            "tasks, deploying these models on resource-constrained hardware remains a "
            "significant challenge. Edge devices such as microcontrollers, mobile phones, "
            "and IoT sensors impose hard constraints on model size, inference latency, "
            "and power consumption that standard architectures routinely violate."
        ),
        (
            "Neural Architecture Search (NAS) has emerged as a promising paradigm for "
            "automating the design of neural network architectures. Early NAS methods "
            "demonstrated superhuman architecture design capabilities, achieving competitive "
            "or superior accuracy compared to hand-crafted models across vision and language "
            "tasks. However, these pioneering approaches focused predominantly on maximizing "
            "accuracy, often producing architectures that are impractical for deployment "
            "outside of well-resourced data centers."
        ),
        (
            "Recent work has begun to address this limitation through hardware-aware NAS, "
            "where the search process incorporates estimates of inference cost alongside "
            "accuracy. Notable examples include MnasNet, FBNet, and Once-for-All networks, "
            "each of which integrates latency or FLOP constraints into the search objective. "
            "Despite these advances, existing hardware-aware methods suffer from several "
            "shortcomings: (1) they typically optimize for a single hardware metric, ignoring "
            "the multi-dimensional nature of edge deployment constraints; (2) they rely on "
            "coarse-grained hardware models that poorly approximate real device behavior; "
            "and (3) they require expensive re-search when targeting new hardware platforms."
        ),
        (
            "In this paper, we propose EdgeNAS, a comprehensive framework for neural "
            "architecture search that addresses these limitations through three key "
            "contributions. First, we formulate NAS as a multi-objective optimization "
            "problem that jointly considers accuracy, latency, memory, and energy. Second, "
            "we develop a differentiable hardware surrogate model that accurately predicts "
            "deployment costs for diverse edge platforms. Third, we introduce a platform "
            "transfer mechanism that enables efficient adaptation of search results across "
            "different hardware targets with minimal computational overhead."
        ),
    ],
    "2 Related Work": [
        (
            "Neural architecture search has undergone rapid evolution since its introduction "
            "by Zoph and Le (2017). The field can be broadly categorized along three axes: "
            "the search space, the search strategy, and the performance estimation method. "
            "Early approaches used reinforcement learning to train a controller that generates "
            "architecture descriptions, while later methods adopted evolutionary algorithms, "
            "Bayesian optimization, and gradient-based techniques. We review the most relevant "
            "threads of prior work below."
        ),
        (
            "2.1 Differentiable Architecture Search. DARTS (Liu et al., 2019) reformulated "
            "the discrete architecture search problem as a continuous optimization through "
            "architecture parameter relaxation. This approach enabled gradient-based search "
            "and reduced computational cost by orders of magnitude compared to RL-based "
            "methods. Subsequent works including P-DARTS, Fair DARTS, and DARTS+ addressed "
            "stability issues and performance collapse observed in the original formulation. "
            "Our method builds upon the differentiable search paradigm but extends it to "
            "incorporate hardware-specific constraints."
        ),
        (
            "2.2 Hardware-Aware NAS. MnasNet (Tan et al., 2019) introduced latency-aware "
            "search by incorporating measured inference time into the reward function. "
            "FBNet (Wu et al., 2019) used a lookup table of layer-wise latencies to enable "
            "differentiable latency optimization. ProxylessNAS (Cai et al., 2019) further "
            "improved efficiency by directly searching on the target task. EfficientNet "
            "(Tan and Le, 2019) combined NAS with compound scaling to achieve strong accuracy "
            "at various model sizes. However, these methods primarily target a single "
            "hardware metric and require extensive re-search for new platforms."
        ),
        (
            "2.3 Multi-Objective NAS. LEMONADE (Elsken et al., 2019) and NSGANet (Lu et al., "
            "2019) applied multi-objective evolutionary algorithms to simultaneously optimize "
            "accuracy and computational cost. MONAS explored Pareto-optimal architectures "
            "across accuracy-latency trade-offs. Our approach differs in that we optimize "
            "across four hardware metrics simultaneously and use a differentiable formulation "
            "rather than evolutionary search, enabling more efficient exploration of the "
            "multi-dimensional Pareto frontier."
        ),
    ],
    "3 Method": [
        (
            "3.1 Problem Formulation. We formulate neural architecture search as a "
            "multi-objective optimization problem over a directed acyclic graph (DAG) "
            "search space. Let alpha denote the continuous architecture parameters that "
            "determine the operations at each edge of the DAG. The search objective is to "
            "find alpha* that maximizes accuracy A(alpha) while satisfying constraints on "
            "latency L(alpha) <= L_max, memory M(alpha) <= M_max, and energy E(alpha) <= E_max "
            "for the target hardware platform."
        ),
        (
            "Rather than imposing hard constraints, we adopt a scalarized multi-objective "
            "formulation with learnable trade-off weights. The combined loss function is "
            "given by L_total = L_task + lambda_1 * L_latency + lambda_2 * L_memory + "
            "lambda_3 * L_energy, where each penalty term is derived from the hardware "
            "surrogate model predictions. The trade-off weights lambda_i are adapted during "
            "search using a constraint satisfaction mechanism that increases penalties when "
            "constraints are violated and relaxes them when margins exist."
        ),
        (
            "3.2 Hardware Surrogate Model. A critical component of our approach is the "
            "hardware surrogate model H(alpha, p) that predicts deployment metrics for "
            "architecture alpha on platform p. We parameterize H as a graph neural network "
            "that takes the computational graph of the candidate architecture as input and "
            "outputs predicted latency, memory footprint, and energy consumption. The "
            "surrogate is trained on a dataset of (architecture, measurement) pairs collected "
            "from profiling randomly sampled architectures on the target platform."
        ),
        (
            "To handle the diversity of edge platforms, we introduce a platform embedding "
            "vector that captures hardware-specific characteristics including processor type, "
            "clock frequency, memory bandwidth, and instruction set features. This embedding "
            "is concatenated with the graph-level representation before the prediction heads, "
            "enabling a single surrogate model to serve multiple platforms. During search, "
            "the surrogate provides differentiable gradients that flow through the hardware "
            "prediction to the architecture parameters, enabling end-to-end optimization."
        ),
        (
            "3.3 Search Algorithm. EdgeNAS employs a two-stage search procedure. In the "
            "first stage, we perform a supernet training phase where all candidate operations "
            "share weights within a one-shot model. The supernet is trained for 50 epochs "
            "on the training set while simultaneously optimizing the architecture parameters "
            "on the validation set using the combined loss. In the second stage, we derive "
            "the final architecture by discretizing the continuous architecture parameters, "
            "selecting the operation with the highest weight at each edge."
        ),
    ],
    "4 Experiments": [
        (
            "4.1 Experimental Setup. We evaluate EdgeNAS on three benchmark tasks: image "
            "classification (ImageNet-1K), object detection (COCO-2017), and keyword spotting "
            "(SpeechCommands-v2). For each task, we search architectures targeting four edge "
            "platforms: Raspberry Pi 4 (ARM Cortex-A72, 4GB RAM), NVIDIA Jetson Nano (Maxwell "
            "GPU, 4GB shared memory), Google Coral Dev Board (Edge TPU), and an ARM Cortex-M7 "
            "microcontroller (STM32H743, 1MB SRAM). The search is conducted on a workstation "
            "with 8 NVIDIA A100 GPUs and takes approximately 12 GPU-hours per task-platform pair."
        ),
        (
            "4.2 ImageNet Classification Results. Table 1 presents the ImageNet top-1 accuracy "
            "and deployment metrics for architectures discovered by EdgeNAS compared to baseline "
            "methods. On Raspberry Pi 4, EdgeNAS achieves 76.8% top-1 accuracy at 23ms inference "
            "latency, compared to MobileNetV3-Large at 75.2%/31ms and EfficientNet-B0 at 77.1%/42ms. "
            "This represents a 2.3x speedup over EfficientNet-B0 with only 0.3% accuracy loss. "
            "On Jetson Nano, the discovered architecture reaches 78.3% accuracy at 8.7ms latency, "
            "outperforming all baselines in both metrics."
        ),
        (
            "4.3 Object Detection Results. For COCO object detection, we apply the discovered "
            "backbone architectures within an SSD-Lite detection framework. EdgeNAS backbones "
            "consistently improve the accuracy-efficiency trade-off compared to standard "
            "MobileNet backbones. On Raspberry Pi 4, our model achieves 22.4 mAP at 87ms per "
            "frame, compared to 21.8 mAP/112ms for SSD-MobileNetV2. The improvements are "
            "more pronounced on GPU-based platforms, where EdgeNAS achieves 28.7 mAP at 15ms "
            "on Jetson Nano, a 1.8x speedup over the MobileNetV2 baseline at comparable accuracy."
        ),
        (
            "4.4 Keyword Spotting Results. On the SpeechCommands-v2 dataset, EdgeNAS discovers "
            "architectures that achieve 97.1% accuracy on Cortex-M7 with only 156KB model size "
            "and 2.3ms inference time. This compares favorably to the DS-CNN-L baseline (96.4% "
            "accuracy, 234KB, 3.8ms) and the attention-based KWT-1 model (97.5%, 607KB, 8.1ms). "
            "The discovered architecture uses a novel combination of depthwise separable "
            "convolutions and lightweight temporal attention that is well-suited to the limited "
            "memory and compute budget of microcontroller targets."
        ),
    ],
    "5 Analysis": [
        (
            "5.1 Ablation Study. We conduct ablation experiments to quantify the contribution "
            "of each component in EdgeNAS. Removing the multi-objective formulation and "
            "optimizing only for latency-accuracy reduces the Pareto front quality by 15% as "
            "measured by hypervolume. Replacing the GNN-based surrogate with a simple lookup "
            "table degrades latency prediction accuracy from 94.2% to 81.7% correlation. "
            "Disabling platform transfer and searching from scratch for each platform increases "
            "total search cost by 3.1x without improving final architecture quality."
        ),
        (
            "5.2 Platform Transfer Analysis. A key advantage of EdgeNAS is the ability to "
            "transfer search results across hardware platforms. We measure transfer efficiency "
            "by comparing the search cost and final architecture quality when (a) searching "
            "from scratch on a new platform versus (b) transferring from a previously searched "
            "platform. Transfer reduces search cost by 67% on average while achieving architectures "
            "within 0.4% accuracy of from-scratch search. Transfer is most effective between "
            "platforms with similar computational characteristics (e.g., Cortex-A72 to Cortex-M7) "
            "and least effective for GPU-to-MCU transfer, which still saves 42% search cost."
        ),
        (
            "5.3 Surrogate Model Accuracy. We evaluate the hardware surrogate model on held-out "
            "architecture-measurement pairs for each platform. The GNN-based surrogate achieves "
            "R-squared values of 0.94 for latency, 0.97 for memory, and 0.89 for energy prediction "
            "across all platforms. Per-platform results show higher prediction accuracy for "
            "CPU-based platforms (R-squared > 0.96 for latency) compared to GPU and TPU platforms "
            "(R-squared ~ 0.91), likely due to the more predictable execution model of sequential "
            "processors. Energy prediction is consistently the most challenging metric due to "
            "dynamic voltage and frequency scaling effects."
        ),
        (
            "5.4 Discovered Architecture Patterns. Analysis of the architectures discovered by "
            "EdgeNAS reveals several interesting patterns. For CPU targets, the search consistently "
            "prefers wider architectures with fewer layers, exploiting the parallelism available "
            "in SIMD instruction sets. For GPU targets, deeper architectures with smaller channel "
            "counts are favored, leveraging the massive parallelism of GPU streaming processors. "
            "Microcontroller architectures minimize memory-intensive operations and favor "
            "operations that can be executed in-place. These patterns align with hardware design "
            "principles and suggest that the search effectively learns platform-specific "
            "optimization strategies."
        ),
    ],
    "6 Discussion": [
        (
            "Our results demonstrate that multi-objective, hardware-aware neural architecture "
            "search can significantly improve the deployment efficiency of deep learning models "
            "on edge devices. The EdgeNAS framework addresses several practical challenges that "
            "have limited the adoption of NAS in production settings: the need to optimize for "
            "multiple hardware metrics simultaneously, the high cost of re-searching for new "
            "platforms, and the gap between proxy metrics and actual deployment performance."
        ),
        (
            "Several limitations of our current approach warrant discussion. First, the hardware "
            "surrogate model requires an initial profiling phase on each new platform, which "
            "involves running approximately 500 randomly sampled architectures to collect "
            "training data. While this one-time cost is modest compared to the full NAS search, "
            "it may be prohibitive for very specialized or limited-access hardware. Second, "
            "our search space is currently limited to convolutional architectures; extending "
            "to transformer-based models and hybrid architectures is an important direction "
            "for future work."
        ),
        (
            "The platform transfer mechanism opens interesting possibilities for a search-once, "
            "deploy-everywhere paradigm. By maintaining a library of platform embeddings and "
            "pre-searched architectures, new deployment targets could be addressed with minimal "
            "additional computation. This vision aligns with the growing need for on-device "
            "AI across an increasingly diverse landscape of edge hardware, from high-performance "
            "mobile SoCs to ultra-low-power sensor processors."
        ),
    ],
    "7 Conclusion": [
        (
            "We have presented EdgeNAS, a multi-objective neural architecture search framework "
            "designed for resource-constrained edge deployment. By jointly optimizing accuracy, "
            "latency, memory, and energy through a differentiable hardware surrogate model, "
            "EdgeNAS discovers architectures that achieve superior deployment efficiency compared "
            "to both manually designed and single-objective NAS baselines. The platform transfer "
            "mechanism reduces adaptation cost to new hardware by 67%, enabling practical "
            "deployment across diverse edge platforms."
        ),
        (
            "Our experiments across three tasks and four hardware platforms demonstrate consistent "
            "improvements in the accuracy-efficiency trade-off, with the most significant gains "
            "observed on the most resource-constrained platforms. The discovered architectures "
            "exhibit platform-specific design patterns that align with known hardware optimization "
            "principles, validating the effectiveness of the hardware-aware search process. "
            "Future work will extend EdgeNAS to transformer architectures, explore dynamic "
            "architecture adaptation at deployment time, and develop online learning methods "
            "for the hardware surrogate model."
        ),
    ],
    "References": [
        (
            "[1] Cai, H., Zhu, L., and Han, S. (2019). ProxylessNAS: Direct neural architecture "
            "search on target task and hardware. In International Conference on Learning "
            "Representations (ICLR)."
        ),
        (
            "[2] Elsken, T., Metzen, J. H., and Hutter, F. (2019). Efficient multi-objective "
            "neural architecture search via Lamarckian evolution. In International Conference on "
            "Learning Representations (ICLR)."
        ),
        (
            "[3] Liu, H., Simonyan, K., and Yang, Y. (2019). DARTS: Differentiable architecture "
            "search. In International Conference on Learning Representations (ICLR)."
        ),
        (
            "[4] Lu, Z., Whalen, I., Boddeti, V., et al. (2019). NSGA-Net: Neural architecture "
            "search using multi-objective genetic algorithm. In Proceedings of the Genetic and "
            "Evolutionary Computation Conference (GECCO)."
        ),
        (
            "[5] Tan, M., Chen, B., Pang, R., et al. (2019). MnasNet: Platform-aware neural "
            "architecture search for mobile. In IEEE Conference on Computer Vision and Pattern "
            "Recognition (CVPR)."
        ),
        (
            "[6] Tan, M. and Le, Q. V. (2019). EfficientNet: Rethinking model scaling for "
            "convolutional neural networks. In International Conference on Machine Learning (ICML)."
        ),
        (
            "[7] Wu, B., Dai, X., Zhang, P., et al. (2019). FBNet: Hardware-aware efficient "
            "convnet design via differentiable neural architecture search. In IEEE Conference on "
            "Computer Vision and Pattern Recognition (CVPR)."
        ),
        (
            "[8] Zoph, B. and Le, Q. V. (2017). Neural architecture search with reinforcement "
            "learning. In International Conference on Learning Representations (ICLR)."
        ),
        (
            "[9] Howard, A., Sandler, M., Chen, B., et al. (2019). Searching for MobileNetV3. "
            "In Proceedings of the IEEE International Conference on Computer Vision (ICCV)."
        ),
        (
            "[10] Zhang, X., Zhou, X., Lin, M., and Sun, J. (2018). ShuffleNet: An extremely "
            "efficient convolutional neural network for mobile devices. In IEEE Conference on "
            "Computer Vision and Pattern Recognition (CVPR)."
        ),
    ],
}


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


def create_manuscript():
    """Create a 12-page academic manuscript PDF."""
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    WIDTH, HEIGHT = 612, 792

    # Margins
    LEFT_MARGIN = 72      # 1 inch
    RIGHT_MARGIN = 540    # 7.5 inches from left
    TOP_MARGIN = 72       # 1 inch from top
    BOTTOM_MARGIN = 720   # 10 inches from top

    BODY_FONTSIZE = 11
    LINE_SPACING = 16     # points between lines (~40 lines per page)

    # We'll build the document by inserting text into textboxes page by page
    # First, create title page content
    page = doc.new_page(width=WIDTH, height=HEIGHT)

    # Title
    title_rect = pymupdf.Rect(LEFT_MARGIN, 120, RIGHT_MARGIN, 200)
    page.insert_textbox(
        title_rect, TITLE,
        fontsize=18, fontname="hebo", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER
    )

    # Authors
    author_rect = pymupdf.Rect(LEFT_MARGIN, 210, RIGHT_MARGIN, 240)
    page.insert_textbox(
        author_rect, AUTHORS,
        fontsize=12, fontname="tiit", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER
    )

    # Affiliation
    affil_rect = pymupdf.Rect(LEFT_MARGIN, 245, RIGHT_MARGIN, 270)
    page.insert_textbox(
        affil_rect, AFFILIATION,
        fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_CENTER
    )

    # Abstract header
    page.insert_text(
        pymupdf.Point(LEFT_MARGIN, 310), "Abstract",
        fontsize=13, fontname="hebo", color=(0, 0, 0)
    )

    # Abstract body
    abstract_rect = pymupdf.Rect(LEFT_MARGIN + 20, 320, RIGHT_MARGIN - 20, 580)
    page.insert_textbox(
        abstract_rect, ABSTRACT,
        fontsize=10, fontname="tiit", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY
    )

    # Start body text on title page below abstract
    y_pos = 610

    # Collect all body text paragraphs with section headers
    all_content = []
    for section_title, paragraphs in SECTIONS.items():
        all_content.append(("heading", section_title))
        for para in paragraphs:
            all_content.append(("body", para))

    content_idx = 0
    current_page = page

    while content_idx < len(all_content):
        content_type, text = all_content[content_idx]

        if content_type == "heading":
            # Check if enough space for heading + at least some text
            if y_pos > BOTTOM_MARGIN - 60:
                # New page
                current_page = doc.new_page(width=WIDTH, height=HEIGHT)
                y_pos = TOP_MARGIN

            # Section heading
            current_page.insert_text(
                pymupdf.Point(LEFT_MARGIN, y_pos),
                text,
                fontsize=13, fontname="hebo", color=(0, 0, 0)
            )
            y_pos += 22
            content_idx += 1

        elif content_type == "body":
            # Calculate available space
            available_height = BOTTOM_MARGIN - y_pos
            if available_height < 30:
                current_page = doc.new_page(width=WIDTH, height=HEIGHT)
                y_pos = TOP_MARGIN
                available_height = BOTTOM_MARGIN - y_pos

            text_rect = pymupdf.Rect(LEFT_MARGIN, y_pos, RIGHT_MARGIN, y_pos + available_height)
            excess = current_page.insert_textbox(
                text_rect, text,
                fontsize=BODY_FONTSIZE, fontname="tiro", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY
            )

            if excess < 0:
                # Text didn't fit - figure out how much was placed
                # Move to next page with remaining text
                # excess is negative = characters that didn't fit
                chars_placed = len(text) + int(excess)
                if chars_placed <= 0:
                    # Nothing fit, go to new page
                    current_page = doc.new_page(width=WIDTH, height=HEIGHT)
                    y_pos = TOP_MARGIN
                    continue
                else:
                    # Find a good break point
                    remaining = text[chars_placed:]
                    current_page = doc.new_page(width=WIDTH, height=HEIGHT)
                    y_pos = TOP_MARGIN

                    # Insert remaining text
                    text_rect2 = pymupdf.Rect(LEFT_MARGIN, y_pos, RIGHT_MARGIN, BOTTOM_MARGIN)
                    excess2 = current_page.insert_textbox(
                        text_rect2, remaining,
                        fontsize=BODY_FONTSIZE, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY
                    )
                    # Estimate lines used
                    remaining_lines = len(remaining) / 80  # rough chars per line
                    y_pos += int(remaining_lines * LINE_SPACING) + 16
                    content_idx += 1
            else:
                # All text fit - estimate how much space was used
                # Use a rough estimate based on character count
                lines_used = max(1, len(text) / 75)  # ~75 chars per line at this font size
                y_pos += int(lines_used * LINE_SPACING) + 16
                content_idx += 1

    # Ensure we have exactly 12 pages by padding if needed
    while doc.page_count < 12:
        p = doc.new_page(width=WIDTH, height=HEIGHT)
        # Add continuation text to fill pages
        filler_paragraphs = [
            (
                "A.1 Supplementary Results. Table A1 provides detailed per-class accuracy "
                "breakdowns for the ImageNet classification experiments. The architectures "
                "discovered by EdgeNAS show particularly strong performance on classes with "
                "high intra-class variability, suggesting that the search process effectively "
                "identifies feature extraction patterns that capture fine-grained discriminative "
                "information. We observe that the accuracy improvements are not uniform across "
                "all classes but are concentrated in categories that benefit most from the "
                "specific architectural innovations selected by the search."
            ),
            (
                "A.2 Hardware Profiling Methodology. The hardware measurements reported in "
                "this paper were collected using a standardized profiling protocol designed "
                "to minimize measurement noise and ensure reproducibility. For each platform, "
                "we execute 100 warm-up inference runs followed by 1000 timed runs, reporting "
                "the median latency. Memory measurements are captured using platform-specific "
                "tools: valgrind for Linux-based platforms and custom heap tracking for "
                "microcontroller targets. Energy consumption is measured using external power "
                "monitors (Monsoon Solutions HVPM for mobile devices, INA219 current sensors "
                "for microcontrollers)."
            ),
            (
                "A.3 Search Space Details. The EdgeNAS search space consists of a stack of "
                "cells, each containing a DAG with N=7 nodes. At each edge, the search selects "
                "from a set of 8 candidate operations: 3x3 and 5x5 depthwise separable "
                "convolutions, 3x3 and 5x5 dilated separable convolutions, 3x3 max pooling, "
                "3x3 average pooling, skip connection, and zero (no connection). The network "
                "architecture consists of a stem followed by 20 stacked cells organized into "
                "3 stages with channel doubling at stage boundaries. Reduction cells with "
                "stride-2 operations are placed at the transition between stages."
            ),
            (
                "A.4 Training Hyperparameters. During the supernet training phase, we use "
                "SGD with momentum 0.9 and weight decay 1e-4 for the network weights, and "
                "Adam with learning rate 3e-4 for the architecture parameters. The initial "
                "learning rate for network weights is 0.1 with cosine annealing. For "
                "ImageNet, we train for 250 epochs with batch size 1024 distributed across "
                "8 GPUs. For COCO, we use the same backbone training schedule with an "
                "additional 90 epochs of detection head fine-tuning. For SpeechCommands, "
                "we train for 100 epochs with batch size 256."
            ),
            (
                "A.5 Additional Platform Results. We present extended results for two "
                "additional deployment scenarios not covered in the main text. First, we "
                "evaluate EdgeNAS architectures on the Samsung Exynos 2100 mobile SoC, "
                "targeting both CPU and NPU execution modes. The discovered architectures "
                "achieve 77.4% ImageNet accuracy at 11ms on the NPU and 76.1% at 28ms on "
                "the CPU cores. Second, we test deployment on the Intel Neural Compute Stick 2, "
                "where EdgeNAS reaches 77.8% accuracy at 19ms, compared to 76.3%/26ms for "
                "MobileNetV3-Large compiled with OpenVINO."
            ),
            (
                "A.6 Visualization of Discovered Architectures. Figures A1 through A4 show "
                "the cell structures discovered by EdgeNAS for each target platform. Several "
                "distinctive patterns emerge: CPU-optimized cells exhibit wider fan-out with "
                "parallel branches that can exploit SIMD vectorization, while GPU-optimized "
                "cells tend to be deeper with sequential processing that maximizes compute "
                "utilization. MCU-targeted cells aggressively minimize memory by avoiding "
                "operations that require large intermediate feature maps, preferring in-place "
                "operations and narrow bottleneck structures."
            ),
            (
                "A.7 Comparison with Post-Training Optimization. An important baseline is "
                "whether post-training optimization techniques (quantization, pruning, "
                "knowledge distillation) applied to standard architectures can match the "
                "performance of NAS-discovered architectures. We compare EdgeNAS to "
                "MobileNetV3 + INT8 quantization + 30% structured pruning. While post-training "
                "optimization significantly improves deployment efficiency, EdgeNAS still "
                "achieves 0.8-1.5% higher accuracy at the same latency target across all "
                "platforms. This suggests that architecture-level optimization provides "
                "complementary benefits to weight-level optimization."
            ),
            (
                "A.8 Robustness Analysis. We evaluate the robustness of EdgeNAS-discovered "
                "architectures to input perturbations and distribution shift. On ImageNet-C "
                "(corrupted ImageNet), our architectures show comparable robustness to "
                "EfficientNet-B0 (mean corruption error 52.3% vs 51.8%) while being 2.1x "
                "faster. On ImageNet-R (renditions), EdgeNAS achieves 38.4% accuracy compared "
                "to 36.9% for MobileNetV3-Large, suggesting that the NAS-discovered features "
                "may generalize better across visual domains. We also test adversarial "
                "robustness using PGD-20 attacks and find no significant difference compared "
                "to manually designed architectures of similar capacity."
            ),
        ]
        y = TOP_MARGIN
        if doc.page_count == 12 - (12 - doc.page_count):
            p.insert_text(
                pymupdf.Point(LEFT_MARGIN, y),
                "Appendix A: Supplementary Material",
                fontsize=13, fontname="hebo", color=(0, 0, 0)
            )
            y += 25

        for para in filler_paragraphs:
            if y > BOTTOM_MARGIN - 30:
                break
            rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, BOTTOM_MARGIN)
            excess = p.insert_textbox(
                rect, para,
                fontsize=BODY_FONTSIZE, fontname="tiro", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY
            )
            lines_approx = max(1, len(para) / 75)
            y += int(lines_approx * LINE_SPACING) + 16

    # If we have more than 12 pages, trim
    while doc.page_count > 12:
        doc.delete_page(doc.page_count - 1)

    # Add page numbers at bottom center of each page
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(
            pymupdf.Point(WIDTH / 2 - 10, HEIGHT - 36),
            str(i + 1),
            fontsize=10, fontname="tiro", color=(0, 0, 0)
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {pymupdf.open(OUTPUT).page_count}')


def main():
    create_manuscript()
    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


main()
