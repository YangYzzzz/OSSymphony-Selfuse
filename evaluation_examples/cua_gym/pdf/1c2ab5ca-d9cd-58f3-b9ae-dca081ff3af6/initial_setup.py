"""
Initial Setup: Create an 11-page academic paper PDF for annotation task
Task ID: pdf_res_086
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_086'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/feedback_copy.pdf'


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

    # --- Page dimensions ---
    W, H = 595, 842  # A4

    # --- Academic Paper Content ---

    # Page 1: Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(120, 120), "Advances in Distributed Machine Learning",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, 160), "Frameworks for Large-Scale Data Processing",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 220), "Dr. Elena Vasquez, Dr. Raj Patel, Dr. Kenji Tanaka",
                     fontsize=11, fontname="tiit", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(160, 250), "Department of Computer Science, Stanford University",
                     fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(230, 280), "Published: February 2026",
                     fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    rect = pymupdf.Rect(72, 340, 523, 600)
    page.insert_textbox(rect,
        "Abstract\n\n"
        "This paper presents a comprehensive analysis of distributed machine learning frameworks "
        "designed for processing datasets exceeding 10 terabytes. We evaluate five leading frameworks "
        "across multiple dimensions including throughput, fault tolerance, communication overhead, and "
        "scalability. Our experiments, conducted on clusters ranging from 16 to 512 nodes, demonstrate "
        "that hybrid parameter-server and all-reduce architectures achieve 2.3x throughput improvements "
        "over traditional approaches. We further propose a novel adaptive gradient compression scheme "
        "that reduces inter-node communication by 47% while maintaining model convergence quality "
        "within 0.3% of uncompressed baselines. The findings have significant implications for "
        "practitioners deploying ML workloads in production environments.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_text(pymupdf.Point(72, 630), "Keywords: distributed computing, machine learning, gradient compression, scalability",
                     fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3))

    # Page 2: Introduction
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Introduction", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "The exponential growth of data-driven applications has created an urgent need for scalable "
        "machine learning infrastructure. Modern training datasets for natural language processing, "
        "computer vision, and recommendation systems routinely exceed terabyte-scale volumes, "
        "making single-machine training impractical.\n\n"
        "Distributed machine learning addresses this challenge by partitioning computation across "
        "multiple networked machines. However, the efficiency of distributed training depends critically "
        "on several factors: the communication topology between workers, the synchronization strategy "
        "employed during gradient aggregation, and the degree of data parallelism achievable given "
        "hardware constraints.\n\n"
        "Recent advances in network hardware, particularly the deployment of 400Gbps InfiniBand "
        "interconnects and NVLink bridges, have shifted the performance bottleneck from raw bandwidth "
        "to software-level coordination overhead. Framework design choices that were optimal for "
        "10Gbps Ethernet environments may no longer represent the best tradeoffs in modern clusters.\n\n"
        "In this paper, we systematically evaluate the performance characteristics of five widely-used "
        "distributed ML frameworks: Horovod, PyTorch Distributed (DDP), TensorFlow Distribution Strategy, "
        "Ray Train, and DeepSpeed. We conduct experiments across three hardware configurations "
        "representative of production deployments at major technology companies.\n\n"
        "Our contributions are threefold:\n"
        "  1. A comprehensive benchmark suite covering throughput, latency, and fault recovery metrics\n"
        "  2. An analysis of framework behavior under heterogeneous hardware conditions\n"
        "  3. A novel adaptive compression algorithm that dynamically adjusts gradient precision\n\n"
        "The remainder of this paper is organized as follows. Section 2 reviews related work in "
        "distributed ML systems. Section 3 describes our experimental methodology. Section 4 presents "
        "results and analysis. Section 5 discusses implications and limitations. Section 6 introduces our "
        "adaptive compression scheme. Section 7 concludes with future directions.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 3: Related Work
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Related Work", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "2.1 Parameter Server Architecture\n\n"
        "The parameter server paradigm, introduced by Li et al. (2014), centralizes model parameters on "
        "dedicated server nodes while worker nodes compute gradients on data partitions. This architecture "
        "enables asynchronous updates but introduces potential consistency challenges. Dean et al. (2012) "
        "demonstrated the viability of asynchronous SGD for training large neural networks at Google, "
        "achieving near-linear scaling on up to 16,000 CPU cores.\n\n"
        "2.2 All-Reduce Communication Patterns\n\n"
        "Ring all-reduce, popularized by Baidu Research and subsequently adopted by Horovod (Sergeev & "
        "Del Balso, 2018), distributes gradient aggregation across all workers without requiring dedicated "
        "parameter servers. The ring topology ensures that each node sends and receives a fixed volume "
        "of data regardless of cluster size, providing O(N) aggregate bandwidth utilization. Patarasuk and "
        "Yuan (2009) provide a thorough analysis of bandwidth-optimal all-reduce algorithms.\n\n"
        "2.3 Gradient Compression\n\n"
        "Stich et al. (2018) established theoretical convergence guarantees for distributed SGD with "
        "compressed gradients, showing that top-k sparsification preserves convergence with O(1/sqrt(NK)) "
        "rate. Bernstein et al. (2018) introduced signSGD, which transmits only the sign of each gradient "
        "component, achieving 32x compression. Alistarh et al. (2017) proposed QSGD, a quantization "
        "scheme with tunable precision-communication tradeoffs.\n\n"
        "2.4 Hybrid Approaches\n\n"
        "Recent systems like BytePS (Jiang et al., 2020) combine parameter server and all-reduce patterns, "
        "using idle CPU and bandwidth resources on parameter servers for gradient summation while "
        "leveraging GPU-to-GPU communication for the all-reduce phase. This hybrid approach achieves "
        "up to 84% higher throughput compared to pure all-reduce on networks with heterogeneous bandwidth.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 4: Methodology
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. Experimental Methodology", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "3.1 Hardware Configurations\n\n"
        "We conducted experiments on three cluster configurations:\n\n"
        "Configuration A (Small): 16 nodes, each with 4x NVIDIA A100 (40GB), Intel Xeon 8380 (64 cores), "
        "512GB RAM, 100Gbps InfiniBand HDR.\n\n"
        "Configuration B (Medium): 64 nodes, each with 8x NVIDIA A100 (80GB), AMD EPYC 7763 (128 cores), "
        "1TB RAM, 200Gbps InfiniBand HDR.\n\n"
        "Configuration C (Large): 512 nodes, each with 8x NVIDIA H100 (80GB), Intel Xeon 8480+ (112 cores), "
        "2TB RAM, 400Gbps InfiniBand NDR.\n\n"
        "3.2 Benchmark Models\n\n"
        "We selected four representative models spanning different computational profiles:\n\n"
        "  - ResNet-152: 60M parameters, compute-bound CNN for image classification\n"
        "  - BERT-Large: 340M parameters, transformer model for NLP tasks\n"
        "  - GPT-2 XL: 1.5B parameters, autoregressive language model\n"
        "  - DLRM: 540M parameters with sparse embedding tables, recommendation model\n\n"
        "3.3 Metrics\n\n"
        "We measure the following metrics across all framework-configuration pairs:\n\n"
        "  - Throughput: samples processed per second (images/s or tokens/s)\n"
        "  - Scaling efficiency: ratio of N-node throughput to N times single-node throughput\n"
        "  - Communication overhead: percentage of training time spent in gradient synchronization\n"
        "  - Fault recovery time: time to resume training after a single node failure\n"
        "  - Memory overhead: additional GPU memory consumed by the framework beyond model and data",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 5: Results (part 1)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. Results and Analysis", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 500)
    page.insert_textbox(rect,
        "4.1 Throughput Comparison\n\n"
        "Table 1 summarizes the throughput results for ResNet-152 training across all configurations. "
        "DeepSpeed achieved the highest throughput on Configuration C with 47,820 images/second, "
        "followed by PyTorch DDP at 43,150 images/second. Horovod demonstrated competitive "
        "performance on smaller clusters but showed diminishing returns beyond 128 nodes.\n\n"
        "For BERT-Large, the results showed a different pattern. PyTorch DDP maintained the most "
        "consistent scaling efficiency, achieving 89.2% efficiency at 512 nodes compared to DeepSpeed's "
        "91.7%. However, DeepSpeed's ZeRO-3 optimization provided substantially lower memory overhead, "
        "enabling larger batch sizes that partially offset the efficiency difference.\n\n"
        "The GPT-2 XL experiments revealed framework-specific bottlenecks in pipeline parallelism "
        "implementations. DeepSpeed's pipeline engine achieved 78% GPU utilization with 32 pipeline "
        "stages, while Ray Train's implementation reached only 61% due to higher bubble overhead.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Draw a simple table
    shape = page.new_shape()
    table_top = 520
    row_h = 22
    cols = [72, 172, 272, 372, 523]
    headers = ["Framework", "Config A", "Config B", "Config C"]
    data_rows = [
        ["Horovod", "3,240", "11,850", "38,620"],
        ["PyTorch DDP", "3,410", "12,730", "43,150"],
        ["TF Strategy", "3,180", "11,290", "36,480"],
        ["Ray Train", "3,050", "10,940", "35,210"],
        ["DeepSpeed", "3,520", "13,100", "47,820"],
    ]
    for i in range(7):
        y = table_top + i * row_h
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(523, y))
    for x in cols:
        shape.draw_line(pymupdf.Point(x, table_top), pymupdf.Point(x, table_top + 6 * row_h))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    for j, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[j] + 5, table_top + 15), h, fontsize=9, fontname="hebo")
    for i, row in enumerate(data_rows):
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(cols[j] + 5, table_top + (i + 1) * row_h + 15), val, fontsize=9, fontname="tiro")
    page.insert_text(pymupdf.Point(72, table_top + 7 * row_h + 5),
                     "Table 1: ResNet-152 throughput (images/sec) across cluster configurations",
                     fontsize=8, fontname="tiit", color=(0.3, 0.3, 0.3))

    # Page 6: Results (part 2)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4.2 Communication Overhead Analysis", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "Communication overhead varied significantly across frameworks and cluster sizes. At 16 nodes, "
        "all frameworks maintained communication overhead below 15% of total training time. However, "
        "at 512 nodes, substantial differences emerged.\n\n"
        "Horovod's ring all-reduce implementation showed 34% communication overhead for BERT-Large "
        "on Configuration C, compared to 28% for PyTorch DDP's NCCL-based backend. DeepSpeed's "
        "ZeRO-2 optimizer partitioning reduced communication volume by scattering optimizer states, "
        "achieving only 22% overhead at the same scale.\n\n"
        "TensorFlow Distribution Strategy exhibited the highest overhead at 39% for 512-node "
        "BERT-Large training. Profiling revealed that TensorFlow's graph-level optimization passes "
        "introduced additional synchronization barriers not present in eager-mode frameworks.\n\n"
        "4.3 Fault Recovery\n\n"
        "Fault tolerance testing revealed significant architectural differences between frameworks. "
        "We injected node failures during training and measured the time to resume from the last "
        "checkpoint.\n\n"
        "Ray Train demonstrated the fastest recovery at 12.4 seconds average, leveraging its built-in "
        "actor supervision and automatic checkpoint management. DeepSpeed required 45.8 seconds on "
        "average due to its distributed checkpoint loading mechanism. Horovod and PyTorch DDP both "
        "required manual restart coordination, with recovery times of 78 and 65 seconds respectively.\n\n"
        "4.4 Memory Efficiency\n\n"
        "DeepSpeed ZeRO-3 achieved 4.2x memory reduction compared to standard data parallelism, "
        "enabling GPT-2 XL training on 4x A100-40GB nodes that would otherwise require 80GB variants. "
        "PyTorch FSDP (Fully Sharded Data Parallel) achieved 3.8x reduction with comparable throughput. "
        "Other frameworks did not offer equivalent memory optimization capabilities.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 7 (0-indexed 6): Discussion - the section that needs revision
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. Discussion", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "5.1 Implications for Production Deployments\n\n"
        "Our results suggest that no single framework dominates across all metrics and scales. "
        "Practitioners should consider their specific deployment constraints when selecting a distributed "
        "ML framework.\n\n"
        "For latency-sensitive training jobs on clusters of 64 nodes or fewer, PyTorch DDP offers the "
        "best combination of throughput and ease of use. Its tight integration with the PyTorch ecosystem "
        "and minimal code changes required for distributed training make it the pragmatic default choice.\n\n"
        "For large-scale training (256+ nodes) with memory-constrained hardware, DeepSpeed provides "
        "compelling advantages through its ZeRO optimizer family and pipeline parallelism engine. The "
        "additional configuration complexity is justified by the 2.3x throughput improvement and 4.2x "
        "memory reduction observed in our experiments.\n\n"
        "5.2 Limitations of Current Approaches\n\n"
        "Several limitations warrant discussion. First, all evaluated frameworks assume relatively "
        "homogeneous cluster configurations. In practice, many organizations operate heterogeneous "
        "GPU fleets mixing different generations (V100, A100, H100) and memory capacities. None of "
        "the tested frameworks gracefully handle such heterogeneity without manual configuration.\n\n"
        "Second, our experiments focused on synchronous training paradigms. Asynchronous approaches "
        "such as Hogwild! and its variants may offer superior throughput at the cost of convergence "
        "guarantees. A systematic comparison of synchronous versus asynchronous methods across these "
        "frameworks remains an important direction for future work.\n\n"
        "Third, the cost analysis presented here considers only computation time and does not account "
        "for cloud pricing dynamics, spot instance availability, or cross-region communication costs that "
        "significantly impact real-world deployment budgets.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 8: Adaptive Compression (part 1)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6. Adaptive Gradient Compression", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "6.1 Motivation\n\n"
        "Our benchmark results highlight communication overhead as the primary scaling bottleneck "
        "beyond 128 nodes. Existing compression methods apply a fixed compression ratio throughout "
        "training, which is suboptimal because gradient statistics change significantly across training "
        "phases.\n\n"
        "During early training, gradients exhibit high variance and large magnitudes, making aggressive "
        "compression risky. In later phases, gradients become smaller and more concentrated, allowing "
        "higher compression without convergence impact.\n\n"
        "6.2 Algorithm Design\n\n"
        "We propose Adaptive Gradient Compression (AGC), a scheme that dynamically adjusts the "
        "compression ratio based on a running estimate of gradient signal-to-noise ratio (SNR).\n\n"
        "At each training iteration t, we compute:\n"
        "  SNR(t) = ||mean(g_t)||_2 / ||std(g_t)||_2\n\n"
        "where g_t is the gradient vector at iteration t. We maintain an exponential moving average:\n"
        "  SNR_ema(t) = alpha * SNR(t) + (1 - alpha) * SNR_ema(t-1)\n\n"
        "The compression ratio k(t) is then determined by:\n"
        "  k(t) = k_min + (k_max - k_min) * sigmoid(beta * (SNR_ema(t) - SNR_threshold))\n\n"
        "where k_min and k_max define the compression ratio bounds, beta controls the transition "
        "sharpness, and SNR_threshold is a hyperparameter calibrated during a warmup phase.\n\n"
        "6.3 Implementation Details\n\n"
        "AGC is implemented as a communication hook compatible with PyTorch DDP and DeepSpeed. "
        "The SNR computation adds negligible overhead (< 0.1% of iteration time) as it operates on "
        "gradient statistics already maintained by the optimizer. The top-k sparsification used for "
        "compression employs a partial sort algorithm with O(d) expected time complexity, where d "
        "is the gradient dimension.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 9: Adaptive Compression (part 2)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6.4 Experimental Evaluation of AGC", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "We evaluated AGC on BERT-Large and GPT-2 XL training using Configuration B (64 nodes). "
        "Results are compared against three baselines: uncompressed training, fixed top-1% sparsification, "
        "and signSGD.\n\n"
        "For BERT-Large, AGC achieved 47% communication reduction while maintaining within 0.18% of "
        "uncompressed final accuracy (F1 score: 91.23 vs 91.41). Fixed top-1% sparsification achieved "
        "similar communication reduction but degraded accuracy by 0.74% (F1: 90.67). SignSGD reduced "
        "communication by 96% but suffered 1.82% accuracy degradation.\n\n"
        "For GPT-2 XL, AGC maintained within 0.31% perplexity deviation from the uncompressed baseline "
        "(perplexity: 18.74 vs 18.43) while reducing communication volume by 43%. The lower compression "
        "ratio compared to BERT-Large reflects GPT-2 XL's higher gradient variance, causing AGC to "
        "automatically select more conservative compression.\n\n"
        "Convergence speed analysis showed that AGC reached 90% of final accuracy 1.4x faster than "
        "uncompressed training on 64 nodes, due to the net throughput improvement from reduced "
        "communication. Fixed compression methods occasionally exhibited training instability manifesting "
        "as loss spikes, which AGC's adaptive mechanism successfully avoided.\n\n"
        "The warmup phase for SNR threshold calibration required 500 iterations (approximately 2 minutes "
        "of training time), after which the compression ratio stabilized. We observed that the optimal "
        "SNR_threshold varied by model architecture but was consistent across different dataset sizes "
        "and cluster configurations, suggesting good transferability of calibrated hyperparameters.\n\n"
        "Additional ablation studies confirmed that the exponential moving average smoothing (alpha=0.99) "
        "was critical for stable compression ratio adaptation. Without smoothing, the compression ratio "
        "oscillated rapidly, introducing variance in per-iteration training time that degraded overall "
        "throughput by 8-12%.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 10: Conclusion
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. Conclusion", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "This paper presented a comprehensive evaluation of five distributed machine learning frameworks "
        "across three cluster configurations ranging from 16 to 512 nodes. Our benchmarks covered "
        "throughput, communication overhead, fault tolerance, and memory efficiency for four representative "
        "model architectures.\n\n"
        "Key findings include:\n\n"
        "  1. DeepSpeed achieves the highest throughput for large-scale training (512 nodes), with "
        "47,820 images/second for ResNet-152, a 24% improvement over the next best framework.\n\n"
        "  2. PyTorch DDP provides the most consistent scaling efficiency across cluster sizes, making "
        "it the recommended default for moderate-scale deployments.\n\n"
        "  3. Communication overhead becomes the dominant bottleneck beyond 128 nodes, accounting for "
        "22-39% of training time depending on the framework.\n\n"
        "  4. Fault recovery capabilities vary dramatically, with Ray Train recovering in 12.4 seconds "
        "compared to 78 seconds for Horovod.\n\n"
        "We further proposed Adaptive Gradient Compression (AGC), which dynamically adjusts compression "
        "ratios based on gradient signal-to-noise ratio. AGC reduces communication by 47% while "
        "maintaining model quality within 0.3% of uncompressed baselines, validated on BERT-Large and "
        "GPT-2 XL training.\n\n"
        "Future work will extend this evaluation to emerging model architectures including mixture-of-experts "
        "models, investigate the interaction between gradient compression and learning rate scheduling, "
        "and develop AGC variants optimized for heterogeneous GPU clusters.",
        fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 11: References
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "References", fontsize=14, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, 523, 780)
    page.insert_textbox(rect,
        "[1] Alistarh, D., Grubic, D., Li, J., Tomioka, R., & Vojnovic, M. (2017). QSGD: "
        "Communication-efficient SGD via gradient quantization and encoding. NeurIPS 2017.\n\n"
        "[2] Bernstein, J., Wang, Y., Azizzadenesheli, K., & Anandkumar, A. (2018). signSGD: "
        "Compressed optimisation for non-convex problems. ICML 2018.\n\n"
        "[3] Dean, J., et al. (2012). Large scale distributed deep networks. NeurIPS 2012.\n\n"
        "[4] Jiang, Y., et al. (2020). A unified architecture for accelerating distributed DNN training "
        "in heterogeneous GPU/CPU clusters. OSDI 2020.\n\n"
        "[5] Li, M., et al. (2014). Scaling distributed machine learning with the parameter server. "
        "OSDI 2014.\n\n"
        "[6] Patarasuk, P., & Yuan, X. (2009). Bandwidth optimal all-reduce algorithms for clusters "
        "of workstations. Journal of Parallel and Distributed Computing.\n\n"
        "[7] Sergeev, A., & Del Balso, M. (2018). Horovod: fast and easy distributed deep learning "
        "in TensorFlow. arXiv preprint arXiv:1802.05799.\n\n"
        "[8] Stich, S. U., Cordonnier, J. B., & Jaggi, M. (2018). Sparsified SGD with memory. "
        "NeurIPS 2018.\n\n"
        "[9] Rajbhandari, S., Rasley, J., Rber, O., & He, Y. (2020). ZeRO: Memory optimizations "
        "toward training trillion parameter models. SC 2020.\n\n"
        "[10] Rasley, J., Rajbhandari, S., Ruwase, O., & He, Y. (2020). DeepSpeed: System optimizations "
        "enable training deep learning models with over 100 billion parameters. KDD 2020.\n\n"
        "[11] Zhao, Y., et al. (2023). PyTorch FSDP: Experiences on scaling fully sharded data parallel. "
        "VLDB 2023.\n\n"
        "[12] Moritz, P., et al. (2018). Ray: A distributed framework for emerging AI applications. "
        "OSDI 2018.",
        fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 11')

    # Open in Evince on page 7 for the agent
    launch_gui(f'evince --page-index=6 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
