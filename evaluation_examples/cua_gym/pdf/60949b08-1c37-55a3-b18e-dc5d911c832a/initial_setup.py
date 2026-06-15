"""
Initial Setup: Create a 12-page academic paper PDF for review annotation task
Task ID: pdf_res_073
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_073'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/draft_feedback.pdf'


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

    # Page dimensions - Letter size
    W, H = 612, 792
    LEFT_MARGIN = 72
    RIGHT_MARGIN = W - 72
    TEXT_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    # Academic paper content for 12 pages
    sections = [
        {
            "title": "Adaptive Neural Architecture Search for Edge Computing:\nA Resource-Constrained Optimization Framework",
            "is_title_page": True,
            "authors": "Elena Vasquez, Rajesh Patel, Mei-Lin Chang, Thomas Okonkwo",
            "affiliation": "Department of Computer Science, Stanford University\nInstitute for Computational Intelligence, ETH Zurich",
            "abstract": (
                "Abstract -- Neural architecture search (NAS) has shown remarkable success in automating "
                "the design of deep neural networks. However, deploying NAS-derived architectures on "
                "edge devices with limited computational resources remains a significant challenge. "
                "In this paper, we propose EdgeNAS, a resource-constrained optimization framework that "
                "jointly optimizes model accuracy, latency, and energy consumption for edge deployment. "
                "Our approach introduces a novel differentiable search space that explicitly encodes "
                "hardware constraints as soft penalties in the optimization objective. Through extensive "
                "experiments on ImageNet, CIFAR-100, and a custom industrial inspection dataset, we "
                "demonstrate that EdgeNAS achieves 94.2% of the accuracy of unconstrained NAS models "
                "while reducing inference latency by 3.7x and energy consumption by 2.9x on ARM "
                "Cortex-A72 processors. Furthermore, we introduce a transfer learning protocol that "
                "reduces search cost from 48 GPU-hours to just 6.3 GPU-hours by leveraging "
                "pre-computed architecture embeddings. Our results suggest that hardware-aware NAS "
                "can effectively bridge the gap between state-of-the-art accuracy and practical "
                "deployment constraints."
            ),
        },
        {
            "heading": "1. Introduction",
            "body": (
                "The proliferation of edge computing devices has created an unprecedented demand for "
                "efficient deep learning models that can operate within strict resource budgets. While "
                "neural architecture search has automated much of the model design process, the "
                "resulting architectures often exceed the computational capacity of target hardware "
                "platforms such as mobile phones, IoT sensors, and embedded controllers.\n\n"
                "Traditional NAS approaches optimize primarily for accuracy on a validation set, "
                "treating hardware constraints as post-hoc considerations. This disconnect leads to "
                "architectures that achieve impressive benchmark scores but fail to meet real-world "
                "deployment requirements. For instance, Liu et al. (2023) demonstrated that 67% of "
                "NAS-derived models exceed the memory budget of typical edge devices by a factor of "
                "2x or more.\n\n"
                "Several recent works have attempted to incorporate hardware awareness into the search "
                "process. ProxylessNAS (Cai et al., 2019) introduced latency prediction as a "
                "regularization term, while FBNet (Wu et al., 2019) proposed differentiable neural "
                "architecture search with latency-aware loss. However, these approaches typically "
                "target a single hardware metric and do not account for the complex interplay between "
                "latency, energy consumption, and memory footprint.\n\n"
                "In this paper, we present EdgeNAS, a comprehensive framework that addresses these "
                "limitations through three key contributions:\n\n"
                "1) A multi-objective differentiable search space that jointly encodes accuracy, "
                "latency, energy, and memory constraints as learnable penalty terms.\n\n"
                "2) A hardware-aware predictor network trained on measurements from actual edge "
                "devices, providing accurate cost estimates during the search process.\n\n"
                "3) A transfer learning protocol that amortizes search costs across device families "
                "by learning shared architecture representations."
            ),
        },
        {
            "heading": "2. Related Work",
            "body": (
                "2.1 Neural Architecture Search\n\n"
                "Early NAS methods employed reinforcement learning (Zoph and Le, 2017) or evolutionary "
                "algorithms (Real et al., 2019) to explore discrete architecture spaces. These methods "
                "required thousands of GPU-hours, making them impractical for most research groups. "
                "The introduction of weight sharing (Pham et al., 2018) and differentiable relaxation "
                "(Liu et al., 2019) reduced search costs by orders of magnitude.\n\n"
                "DARTS (Liu et al., 2019) formulated NAS as a bilevel optimization problem, enabling "
                "gradient-based search over a continuous relaxation of the architecture space. "
                "Subsequent works have addressed DARTS's tendency toward performance collapse through "
                "regularization (Chen and Hsieh, 2020), progressive pruning (Xu et al., 2020), and "
                "robust training protocols (Zela et al., 2020).\n\n"
                "2.2 Hardware-Aware NAS\n\n"
                "The integration of hardware metrics into NAS has followed two main approaches: "
                "constraint-based and objective-based. Constraint-based methods enforce hard limits "
                "on latency or model size, pruning architectures that exceed thresholds (Tan et al., "
                "2019). Objective-based methods incorporate hardware costs as additional optimization "
                "terms, allowing smooth trade-offs between accuracy and efficiency.\n\n"
                "MnasNet (Tan et al., 2019) pioneered the use of real device measurements during "
                "search, achieving a strong accuracy-latency trade-off on mobile platforms. "
                "Once-for-All networks (Cai et al., 2020) trained a single supernet that could be "
                "specialized for different hardware targets without re-searching. Most recently, "
                "HW-NAS-Bench (Li et al., 2021) provided standardized benchmarks for evaluating "
                "hardware-aware NAS methods across diverse devices."
            ),
        },
        {
            "heading": "3. Methodology",
            "body": (
                "3.1 Problem Formulation\n\n"
                "We formulate edge-aware NAS as a constrained multi-objective optimization problem. "
                "Let A denote the architecture space, and let f(a) represent the validation accuracy "
                "of architecture a in A. We define hardware cost functions L(a), E(a), and M(a) "
                "representing latency, energy consumption, and peak memory usage, respectively.\n\n"
                "The optimization objective is:\n\n"
                "    max f(a) - lambda_L * max(0, L(a) - L_target)\n"
                "              - lambda_E * max(0, E(a) - E_target)\n"
                "              - lambda_M * max(0, M(a) - M_target)\n\n"
                "where lambda_L, lambda_E, lambda_M are penalty coefficients and L_target, E_target, "
                "M_target are user-specified hardware budgets.\n\n"
                "3.2 Differentiable Search Space\n\n"
                "Following the DARTS formulation, we represent the architecture as a directed acyclic "
                "graph (DAG) where each edge is associated with a mixture of candidate operations. "
                "Our search space extends the standard DARTS cell with edge-computing-friendly "
                "operations including depthwise separable convolutions, inverted residual blocks, "
                "and squeeze-and-excitation modules.\n\n"
                "The operation set O for each edge comprises:\n"
                "- 3x3 depthwise separable convolution\n"
                "- 5x5 depthwise separable convolution\n"
                "- 3x3 inverted residual block (expansion ratio 3)\n"
                "- 5x5 inverted residual block (expansion ratio 6)\n"
                "- Squeeze-and-excitation block (reduction ratio 4)\n"
                "- Skip connection\n"
                "- Zero (no connection)\n\n"
                "3.3 Hardware Cost Prediction\n\n"
                "To enable differentiable optimization with hardware metrics, we train a neural "
                "predictor that estimates L(a), E(a), and M(a) from the architecture parameters. "
                "We collected 15,000 architecture-measurement pairs across three target platforms "
                "(ARM Cortex-A72, Qualcomm Snapdragon 845, and Intel Movidius VPU) using automated "
                "benchmarking scripts that measure wall-clock latency, power consumption via external "
                "meters, and peak memory allocation."
            ),
        },
        {
            "heading": "3. Methodology (continued)",
            "body": (
                "3.4 Multi-Objective Optimization\n\n"
                "We employ a Pareto-aware training strategy that maintains a diverse set of "
                "architectures along the accuracy-efficiency frontier. At each training step, "
                "we sample architectures from the current Pareto front and update both the "
                "architecture parameters and the shared weights.\n\n"
                "Algorithm 1: EdgeNAS Training Procedure\n"
                "-------------------------------------------\n"
                "Input: Search space A, hardware budgets {L_t, E_t, M_t}\n"
                "Output: Optimal architecture a*\n\n"
                "1: Initialize architecture parameters alpha\n"
                "2: Initialize shared weights w\n"
                "3: Train hardware predictor P on measurement dataset\n"
                "4: for epoch = 1 to T do\n"
                "5:     Update w by gradient descent on training loss\n"
                "6:     Compute hardware costs via predictor P\n"
                "7:     Update alpha by gradient descent on penalized objective\n"
                "8:     Update Pareto front\n"
                "9: end for\n"
                "10: Select a* from Pareto front based on user preferences\n\n"
                "3.5 Transfer Learning Protocol\n\n"
                "To reduce search costs when targeting new hardware platforms, we introduce an "
                "architecture embedding space learned from previous searches. Given a pre-computed "
                "set of Pareto-optimal architectures for K source platforms, we train an encoder "
                "network g that maps architecture parameters to a 128-dimensional embedding vector.\n\n"
                "For a new target platform, we fine-tune only the hardware predictor while keeping "
                "the architecture embeddings fixed. This reduces the search cost from the full "
                "48 GPU-hours to approximately 6.3 GPU-hours, as the search can start from a "
                "warm initialization informed by the source platforms.\n\n"
                "The transfer efficiency depends on the similarity between source and target "
                "hardware. We quantify this using a hardware distance metric based on the "
                "correlation of operation latencies across platforms. Empirically, we observe "
                "high transfer efficiency (>85% relative accuracy) between ARM-family processors "
                "and moderate efficiency (>72%) when transferring from GPU to CPU architectures."
            ),
        },
        {
            "heading": "4. Experimental Setup",
            "body": (
                "4.1 Datasets\n\n"
                "We evaluate EdgeNAS on three benchmark datasets:\n\n"
                "ImageNet (ILSVRC 2012): 1.28M training images and 50K validation images across "
                "1,000 classes. We use the standard training/validation split and report top-1 and "
                "top-5 accuracy on the validation set.\n\n"
                "CIFAR-100: 50,000 training images and 10,000 test images across 100 classes with "
                "32x32 resolution. We apply standard data augmentation (random crop, horizontal flip) "
                "and report test accuracy averaged over 3 independent runs.\n\n"
                "IndustrialQC: A proprietary dataset of 23,847 images from an electronics "
                "manufacturing quality control pipeline. Images are 640x480 grayscale captures of "
                "PCB solder joints, labeled as acceptable (78.3%), defective (15.2%), or borderline "
                "(6.5%). We report balanced accuracy and F1-score.\n\n"
                "4.2 Hardware Platforms\n\n"
                "Target deployment platforms include:\n"
                "- Raspberry Pi 4 (ARM Cortex-A72, 4GB RAM)\n"
                "- Qualcomm Snapdragon 845 (Kryo 385, 6GB RAM)\n"
                "- Intel Movidius Neural Compute Stick 2 (VPU)\n"
                "- NVIDIA Jetson Nano (128-core Maxwell GPU, 4GB RAM)\n\n"
                "For each platform, we measure:\n"
                "- Inference latency (median over 1,000 runs, batch size 1)\n"
                "- Energy per inference (external power meter, averaged over 500 runs)\n"
                "- Peak memory allocation during inference\n"
                "- Throughput at maximum batch size fitting in memory\n\n"
                "4.3 Baselines\n\n"
                "We compare against: MobileNetV3 (Howard et al., 2019), EfficientNet-B0 (Tan and "
                "Le, 2019), ProxylessNAS (Cai et al., 2019), FBNetV2 (Wan et al., 2020), "
                "Once-for-All (Cai et al., 2020), and AttentiveNAS (Wang et al., 2021)."
            ),
        },
        {
            "heading": "5. Results",
            "body": (
                "5.1 ImageNet Results\n\n"
                "Table 1 summarizes the ImageNet performance of EdgeNAS variants compared to "
                "baselines on the Raspberry Pi 4 platform.\n\n"
                "Model                Top-1(%)  Latency(ms)  Energy(mJ)  Params(M)\n"
                "---------------------------------------------------------------------\n"
                "MobileNetV3-Small    67.4      28.3         142         2.5\n"
                "MobileNetV3-Large    75.2      63.7         318         5.4\n"
                "EfficientNet-B0      77.1      89.2         445         5.3\n"
                "ProxylessNAS         74.6      52.1         261         4.1\n"
                "FBNetV2-L            77.2      78.4         392         6.8\n"
                "Once-for-All         76.9      45.8         229         4.7\n"
                "AttentiveNAS-A0      77.3      81.6         408         5.6\n"
                "EdgeNAS-S            74.8      17.1         85          2.1\n"
                "EdgeNAS-M            76.5      31.4         157         3.8\n"
                "EdgeNAS-L            77.8      48.9         245         5.2\n\n"
                "EdgeNAS-L achieves the highest top-1 accuracy (77.8%) among all methods while "
                "maintaining competitive latency. EdgeNAS-S provides the fastest inference at "
                "17.1ms with only a 2.6% accuracy drop compared to the best baseline.\n\n"
                "5.2 CIFAR-100 Results\n\n"
                "On CIFAR-100, EdgeNAS demonstrates consistent improvements in the "
                "accuracy-efficiency trade-off. EdgeNAS-M achieves 82.3% test accuracy with a "
                "search cost of only 4.2 GPU-hours, compared to 81.7% for Once-for-All at "
                "12.8 GPU-hours.\n\n"
                "5.3 Industrial Quality Control\n\n"
                "The IndustrialQC evaluation highlights EdgeNAS's practical value. EdgeNAS-M "
                "achieves a balanced accuracy of 96.1% and F1-score of 0.943, outperforming "
                "the manually-designed baseline CNN (93.8% balanced accuracy) while running "
                "2.4x faster on the Jetson Nano deployment target."
            ),
        },
        {
            "heading": "5. Results (continued)",
            "body": (
                "5.4 Multi-Platform Transfer Results\n\n"
                "Table 2 shows the effectiveness of our transfer learning protocol when adapting "
                "EdgeNAS architectures across hardware platforms.\n\n"
                "Source -> Target          Search Cost  Relative Acc.  Latency Match\n"
                "--------------------------------------------------------------------\n"
                "RPi4 -> Snapdragon 845    5.8 hrs      97.2%          94.8%\n"
                "RPi4 -> Movidius VPU      7.1 hrs      91.4%          88.3%\n"
                "RPi4 -> Jetson Nano       6.3 hrs      95.8%          92.1%\n"
                "Snapdragon -> RPi4        5.2 hrs      96.8%          95.2%\n"
                "Full search (no transfer) 48.0 hrs     100.0%         100.0%\n\n"
                "Transfer between ARM-family processors (RPi4 and Snapdragon) achieves the highest "
                "efficiency, with relative accuracy above 96% at roughly 1/8th the search cost. "
                "Even the most challenging transfer pair (RPi4 to Movidius VPU) retains 91.4% "
                "relative accuracy.\n\n"
                "5.5 Ablation Studies\n\n"
                "We conduct ablation experiments to isolate the contributions of each EdgeNAS "
                "component. Removing the energy penalty term reduces energy efficiency by 34% "
                "with only marginal accuracy improvement (+0.3%). Replacing the neural hardware "
                "predictor with lookup tables degrades latency estimation accuracy from 94.2% to "
                "81.7% correlation, resulting in suboptimal architectures. The Pareto-aware training "
                "strategy improves the diversity of the architecture population by 2.1x compared to "
                "single-objective scalarization, as measured by the hypervolume indicator.\n\n"
                "5.6 Latency Distribution Analysis\n\n"
                "Figure 3 shows the distribution of per-layer latency contributions for EdgeNAS-M "
                "on the Raspberry Pi 4. Depthwise separable convolutions account for 42% of total "
                "inference time, followed by pointwise convolutions (28%) and squeeze-and-excitation "
                "blocks (15%). The remaining 15% is attributed to batch normalization, activation "
                "functions, and memory operations."
            ),
        },
        {
            "heading": "6. Discussion",
            "body": (
                "Our results demonstrate that hardware-aware NAS can effectively navigate the "
                "complex trade-offs between model accuracy and deployment efficiency. Several "
                "observations merit further discussion.\n\n"
                "Accuracy vs. Efficiency Frontier: EdgeNAS consistently pushes the Pareto frontier "
                "compared to existing methods. The key insight is that jointly optimizing multiple "
                "hardware metrics (latency, energy, memory) produces more balanced architectures "
                "than optimizing each metric independently. When we train separate models for latency "
                "and energy optimization, the resulting architectures often sacrifice one metric for "
                "marginal gains in another.\n\n"
                "Search Space Design: The inclusion of squeeze-and-excitation modules in the search "
                "space proved particularly beneficial for quality control tasks, where channel "
                "attention helps distinguish subtle defect patterns. However, these modules introduce "
                "overhead that may not be justified for classification tasks with more discriminative "
                "features.\n\n"
                "Hardware Predictor Accuracy: Our neural predictor achieves 94.2% correlation with "
                "actual measurements on ARM platforms, but this degrades to 87.6% on the Movidius "
                "VPU due to its unique data flow architecture. Future work should explore "
                "hardware-specific predictor architectures that better capture device idiosyncrasies.\n\n"
                "Practical Deployment Considerations: While EdgeNAS optimizes for steady-state "
                "inference metrics, real-world deployment also involves model loading time, "
                "compilation overhead, and thermal throttling. We observed that Jetson Nano models "
                "experience up to 18% latency degradation after sustained operation due to thermal "
                "management. Incorporating such dynamic effects into the search objective remains "
                "an open challenge.\n\n"
                "Reproducibility: All experiments were conducted using PyTorch 2.1 on NVIDIA A100 "
                "GPUs for the search phase. Edge measurements used vendor-provided inference "
                "runtimes (TFLite for ARM, OpenVINO for Movidius, TensorRT for Jetson)."
            ),
        },
        {
            "heading": "7. Limitations and Future Work",
            "body": (
                "Despite the promising results, several limitations should be acknowledged.\n\n"
                "First, our hardware measurement dataset, while covering 15,000 architectures, "
                "may not capture the full diversity of operations encountered in unconstrained "
                "search spaces. Extending the measurement campaign to include transformer-based "
                "operations (self-attention, layer normalization) would broaden the applicability "
                "of EdgeNAS to vision transformer architectures.\n\n"
                "Second, the current framework assumes a single deployment target. In practice, "
                "many applications require models that perform well across a heterogeneous fleet "
                "of devices. Multi-target NAS that produces a single architecture optimized for "
                "a distribution of hardware platforms represents an important direction.\n\n"
                "Third, our transfer learning protocol requires measurements from at least one "
                "source platform. For truly novel hardware (e.g., neuromorphic chips), the initial "
                "measurement cost cannot be amortized. Simulation-based approaches that predict "
                "hardware behavior from architectural specifications could address this limitation.\n\n"
                "Fourth, we have focused on classification and detection tasks. Extending EdgeNAS "
                "to other architectures such as generative models, graph neural networks, and "
                "recurrent architectures would demonstrate broader utility.\n\n"
                "Future work will also investigate:\n"
                "- Quantization-aware search that jointly optimizes bit-width allocation\n"
                "- Dynamic architectures that adapt computational effort based on input complexity\n"
                "- Federated NAS for privacy-preserving architecture search across distributed data\n"
                "- Integration with neural network compilers for end-to-end optimization"
            ),
        },
        {
            "heading": "8. Conclusion",
            "body": (
                "We have presented EdgeNAS, a resource-constrained neural architecture search "
                "framework that jointly optimizes model accuracy, inference latency, and energy "
                "consumption for edge computing platforms. Our approach introduces a differentiable "
                "multi-objective search space with learned hardware cost predictors, enabling "
                "efficient exploration of the accuracy-efficiency Pareto frontier.\n\n"
                "Experimental results on ImageNet, CIFAR-100, and an industrial quality control "
                "dataset demonstrate that EdgeNAS achieves 94.2% of unconstrained NAS accuracy "
                "while reducing latency by 3.7x and energy by 2.9x on ARM Cortex-A72 processors. "
                "Our transfer learning protocol further reduces search costs from 48 GPU-hours to "
                "6.3 GPU-hours, making hardware-aware NAS practical for deployment teams.\n\n"
                "These results suggest that the gap between NAS-derived model quality and practical "
                "deployment constraints can be substantially narrowed through principled co-design "
                "of the search space, objective function, and hardware modeling. We release our "
                "code, pre-trained models, and hardware measurement dataset to facilitate "
                "reproducibility and further research in this direction.\n\n"
                "Acknowledgments\n\n"
                "This work was supported in part by NSF grants IIS-2143895 and CNS-2104532, and by "
                "the Stanford Human-Centered AI Institute. We thank the anonymous reviewers for "
                "their constructive feedback and suggestions."
            ),
        },
        {
            "heading": "References",
            "body": (
                "Cai, H., Zhu, L., and Han, S. (2019). ProxylessNAS: Direct neural architecture "
                "search on target task and hardware. In ICLR.\n\n"
                "Cai, H., Gan, C., Wang, T., Zhang, Z., and Han, S. (2020). Once-for-All: Train "
                "one network and specialize it for efficient deployment. In ICLR.\n\n"
                "Chen, X., and Hsieh, C.-J. (2020). Stabilizing differentiable architecture search "
                "via perturbation-based regularization. In ICML.\n\n"
                "Howard, A., et al. (2019). Searching for MobileNetV3. In ICCV.\n\n"
                "Li, C., et al. (2021). HW-NAS-Bench: Hardware-aware neural architecture search "
                "benchmark. In ICLR.\n\n"
                "Liu, C., et al. (2023). Bridging the gap: Hardware constraints in neural "
                "architecture search. In NeurIPS.\n\n"
                "Liu, H., Simonyan, K., and Yang, Y. (2019). DARTS: Differentiable architecture "
                "search. In ICLR.\n\n"
                "Pham, H., Guan, M., Zoph, B., Le, Q., and Dean, J. (2018). Efficient neural "
                "architecture search via parameter sharing. In ICML.\n\n"
                "Real, E., Aggarwal, A., Huang, Y., and Le, Q. V. (2019). Regularized evolution "
                "for image classifier architecture search. In AAAI.\n\n"
                "Tan, M., et al. (2019). MnasNet: Platform-aware neural architecture search for "
                "mobile. In CVPR.\n\n"
                "Tan, M., and Le, Q. (2019). EfficientNet: Rethinking model scaling for "
                "convolutional neural networks. In ICML.\n\n"
                "Wan, A., et al. (2020). FBNetV2: Differentiable neural architecture search for "
                "spatial and channel dimensions. In CVPR.\n\n"
                "Wang, D., et al. (2021). AttentiveNAS: Improving neural architecture search via "
                "attentive sampling. In CVPR.\n\n"
                "Wu, B., et al. (2019). FBNet: Hardware-aware efficient convnet design via "
                "differentiable neural architecture search. In CVPR.\n\n"
                "Xu, Y., et al. (2020). PC-DARTS: Partial channel connections for memory-efficient "
                "architecture search. In ICLR.\n\n"
                "Zela, A., et al. (2020). Understanding and robustifying differentiable architecture "
                "search. In ICLR.\n\n"
                "Zoph, B., and Le, Q. V. (2017). Neural architecture search with reinforcement "
                "learning. In ICLR."
            ),
        },
    ]

    for idx, section in enumerate(sections):
        page = doc.new_page(width=W, height=H)

        if section.get("is_title_page"):
            # Title page layout
            y = 200
            page.insert_textbox(
                pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 80),
                section["title"],
                fontsize=18,
                fontname="hebo",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            y += 100
            page.insert_textbox(
                pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 40),
                section["authors"],
                fontsize=12,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            y += 50
            page.insert_textbox(
                pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 40),
                section["affiliation"],
                fontsize=10,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            y += 70
            page.insert_textbox(
                pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72),
                section["abstract"],
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
        else:
            y = 72
            # Section heading
            if "heading" in section:
                page.insert_textbox(
                    pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 30),
                    section["heading"],
                    fontsize=14,
                    fontname="hebo",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )
                y += 36

            # Body text
            page.insert_textbox(
                pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72),
                section["body"],
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(W / 2 - 5, H - 40),
            str(idx + 1),
            fontsize=10,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {len(sections)}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
