"""
Initial Setup: Create a 12-page letter-size PDF for 2-up printing task
Task ID: pdf_res_058
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_058'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/printable_paper.pdf'


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

    # Letter size
    W, H = 612, 792

    # Realistic academic paper content for 12 pages
    pages_content = [
        {
            "title": "Advances in Neural Architecture Search: A Comprehensive Survey",
            "body": (
                "Abstract\n\n"
                "Neural Architecture Search (NAS) has emerged as a pivotal technique in automating "
                "the design of deep neural networks. This survey provides a comprehensive overview "
                "of recent advances in NAS methodologies, covering search spaces, optimization "
                "strategies, and performance estimation techniques. We analyze over 150 papers "
                "published between 2018 and 2025, categorizing approaches into reinforcement "
                "learning-based, evolutionary, gradient-based, and one-shot methods. Our analysis "
                "reveals that weight-sharing strategies have significantly reduced computational "
                "costs while maintaining competitive accuracy. We also identify key challenges "
                "including transferability across datasets, hardware-aware optimization, and "
                "the need for standardized benchmarks."
            ),
        },
        {
            "title": "1. Introduction",
            "body": (
                "The design of neural network architectures has traditionally relied on expert "
                "knowledge and extensive manual experimentation. With the increasing complexity "
                "of modern deep learning systems, this manual process has become a significant "
                "bottleneck in the development pipeline. Neural Architecture Search (NAS) aims "
                "to automate this process by systematically exploring the space of possible "
                "architectures to find optimal designs for specific tasks.\n\n"
                "The field of NAS gained significant attention following the seminal work of "
                "Zoph and Le (2017), which demonstrated that reinforcement learning could be "
                "used to discover architectures rivaling human-designed networks on image "
                "classification benchmarks. Since then, the field has expanded rapidly, with "
                "contributions from both academia and industry."
            ),
        },
        {
            "title": "2. Search Space Design",
            "body": (
                "The search space defines the set of possible architectures that can be explored "
                "during the search process. A well-designed search space balances expressiveness "
                "with tractability, enabling the discovery of novel architectures while keeping "
                "the search computationally feasible.\n\n"
                "2.1 Cell-Based Search Spaces\n\n"
                "Cell-based search spaces decompose the architecture into repeating building "
                "blocks called cells. Each cell is a directed acyclic graph (DAG) where nodes "
                "represent feature maps and edges represent operations such as convolutions, "
                "pooling, and skip connections. The NASNet search space introduced by Zoph et al. "
                "(2018) popularized this approach, defining normal cells and reduction cells "
                "that are stacked to form the complete architecture."
            ),
        },
        {
            "title": "3. Optimization Strategies",
            "body": (
                "3.1 Reinforcement Learning Methods\n\n"
                "RL-based NAS methods treat the architecture generation as a sequential decision "
                "problem. A controller network, typically an RNN, generates architecture "
                "descriptions that are then trained and evaluated. The validation accuracy "
                "serves as the reward signal for updating the controller.\n\n"
                "3.2 Evolutionary Methods\n\n"
                "Evolutionary approaches maintain a population of architectures that undergo "
                "mutation and crossover operations. Tournament selection is commonly used to "
                "select parent architectures. AmoebaNet (Real et al., 2019) demonstrated that "
                "evolutionary methods could match or exceed RL-based approaches while being "
                "conceptually simpler and more parallelizable.\n\n"
                "3.3 Gradient-Based Methods\n\n"
                "DARTS (Liu et al., 2019) introduced a differentiable relaxation of the "
                "discrete architecture search space, enabling gradient-based optimization."
            ),
        },
        {
            "title": "4. Performance Estimation",
            "body": (
                "Evaluating candidate architectures is the most computationally expensive "
                "component of NAS. Training each candidate to convergence on the full dataset "
                "can take days on modern hardware. Various strategies have been proposed to "
                "reduce this cost:\n\n"
                "4.1 Early Stopping\n\n"
                "Training is terminated after a fixed number of epochs, and the partial "
                "learning curve is used to estimate final performance. While simple, this "
                "approach can be unreliable for architectures with different convergence rates.\n\n"
                "4.2 Weight Sharing\n\n"
                "One-shot methods train a single over-parameterized supernet that encompasses "
                "all candidate architectures. Individual architectures inherit weights from "
                "the supernet, eliminating the need for independent training. ENAS (Pham et al., "
                "2018) pioneered this approach, reducing search cost from thousands of GPU-days "
                "to a single GPU-day."
            ),
        },
        {
            "title": "5. Hardware-Aware NAS",
            "body": (
                "As deep learning models are deployed on diverse hardware platforms—from cloud "
                "TPUs to mobile phones—there is growing interest in architectures optimized "
                "for specific hardware constraints.\n\n"
                "5.1 Latency-Constrained Search\n\n"
                "MnasNet (Tan et al., 2019) incorporated real device latency measurements "
                "into the reward function, producing architectures that achieve a balance "
                "between accuracy and inference speed. The multi-objective optimization "
                "formulation uses a weighted product of accuracy and latency penalties.\n\n"
                "5.2 Energy-Efficient Architectures\n\n"
                "Recent work has extended hardware awareness to include energy consumption "
                "and memory footprint. These metrics are particularly relevant for edge "
                "devices with limited battery capacity and memory bandwidth."
            ),
        },
        {
            "title": "6. Transferability and Generalization",
            "body": (
                "A critical question in NAS research is whether architectures discovered on "
                "proxy tasks transfer effectively to target tasks. Most NAS methods search "
                "on small-scale datasets (e.g., CIFAR-10) and then transfer to larger datasets "
                "(e.g., ImageNet).\n\n"
                "6.1 Cross-Dataset Transfer\n\n"
                "Empirical studies have shown that architectures found on CIFAR-10 generally "
                "transfer well to ImageNet, maintaining their relative ranking. However, the "
                "correlation weakens for substantially different domains such as medical imaging "
                "or natural language processing.\n\n"
                "6.2 Cross-Task Transfer\n\n"
                "Architectures designed for image classification may not be optimal for object "
                "detection, semantic segmentation, or other downstream tasks. Task-specific "
                "search spaces and multi-task NAS have been proposed to address this limitation."
            ),
        },
        {
            "title": "7. Benchmarks and Reproducibility",
            "body": (
                "The NAS community has recognized the importance of standardized benchmarks "
                "for fair comparison. Several benchmark suites have been developed:\n\n"
                "NAS-Bench-101: Contains the complete training results of 423,624 unique "
                "architectures on CIFAR-10, enabling comparison without actual training.\n\n"
                "NAS-Bench-201: Provides a unified cell-based search space with results on "
                "CIFAR-10, CIFAR-100, and ImageNet-16-120.\n\n"
                "NAS-Bench-301: Uses surrogate models trained on architecture-performance pairs "
                "to approximate the full benchmark landscape.\n\n"
                "These benchmarks have facilitated reproducible research and enabled the "
                "development of new search strategies without expensive GPU computation."
            ),
        },
        {
            "title": "8. Recent Trends",
            "body": (
                "8.1 Zero-Cost Proxies\n\n"
                "Zero-cost NAS methods estimate architecture quality without any training, "
                "using metrics computed on randomly initialized networks. These proxies "
                "analyze gradient flow, linear region counts, or the neural tangent kernel "
                "to predict architecture performance.\n\n"
                "8.2 Transformer Architecture Search\n\n"
                "With the dominance of transformer models in both NLP and computer vision, "
                "NAS has been extended to search over transformer-specific design choices "
                "including attention head configurations, feed-forward dimensions, and "
                "layer normalization strategies.\n\n"
                "8.3 Multi-Modal NAS\n\n"
                "As multi-modal models become prevalent, NAS is being applied to discover "
                "optimal fusion architectures that combine visual, textual, and audio inputs."
            ),
        },
        {
            "title": "9. Limitations and Open Problems",
            "body": (
                "Despite significant progress, several challenges remain in the NAS field:\n\n"
                "Computational Cost: Even with weight sharing, NAS remains expensive compared "
                "to using established architectures. The environmental cost of large-scale "
                "searches is a growing concern.\n\n"
                "Search Space Bias: The design of the search space itself requires expert "
                "knowledge, partially defeating the purpose of automated architecture design.\n\n"
                "Reproducibility: Many NAS methods are sensitive to hyperparameter choices "
                "and random seeds, making results difficult to reproduce.\n\n"
                "Evaluation Fairness: Different training procedures, data augmentation strategies, "
                "and hyperparameter tuning protocols make fair comparisons challenging."
            ),
        },
        {
            "title": "10. Conclusion",
            "body": (
                "Neural Architecture Search has matured significantly since its inception, "
                "evolving from computationally prohibitive approaches to efficient methods "
                "applicable in practical settings. Key advances include differentiable search "
                "methods, weight-sharing supernets, hardware-aware optimization, and "
                "standardized benchmarks.\n\n"
                "Looking forward, the integration of NAS with foundation models, "
                "sustainability-focused search objectives, and automated search space design "
                "represent promising research directions. As the field continues to develop, "
                "we expect NAS to play an increasingly important role in making deep learning "
                "more accessible and efficient.\n\n"
                "The convergence of NAS with other AutoML techniques—including hyperparameter "
                "optimization, data augmentation search, and loss function design—points "
                "toward a future of fully automated machine learning pipelines."
            ),
        },
        {
            "title": "References",
            "body": (
                "[1] Zoph, B. and Le, Q. V. (2017). Neural architecture search with "
                "reinforcement learning. ICLR.\n\n"
                "[2] Zoph, B., Vasudevan, V., Shlens, J., and Le, Q. V. (2018). Learning "
                "transferable architectures for scalable image recognition. CVPR.\n\n"
                "[3] Liu, H., Simonyan, K., and Yang, Y. (2019). DARTS: Differentiable "
                "architecture search. ICLR.\n\n"
                "[4] Real, E., Aggarwal, A., Huang, Y., and Le, Q. V. (2019). Regularized "
                "evolution for image classifier architecture search. AAAI.\n\n"
                "[5] Pham, H., Guan, M., Zoph, B., Le, Q. V., and Dean, J. (2018). Efficient "
                "neural architecture search via parameter sharing. ICML.\n\n"
                "[6] Tan, M., Chen, B., Pang, R., et al. (2019). MnasNet: Platform-aware "
                "neural architecture search for mobile. CVPR.\n\n"
                "[7] Ying, C., Klein, A., Christiansen, E., et al. (2019). NAS-Bench-101: "
                "Towards reproducible neural architecture search. ICML.\n\n"
                "[8] Dong, X. and Yang, Y. (2020). NAS-Bench-201: Extending the scope of "
                "reproducible neural architecture search. ICLR.\n\n"
                "[9] Chen, W., Gong, X., and Wang, Z. (2021). Neural architecture search on "
                "ImageNet in four GPU hours. ICLR.\n\n"
                "[10] White, C., Neiswanger, W., and Savani, Y. (2021). BANANAS: Bayesian "
                "optimization with neural architectures for neural architecture search. AAAI."
            ),
        },
    ]

    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        # Title
        title_y = 72
        page.insert_text(
            pymupdf.Point(72, title_y),
            page_data["title"],
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Body text in a textbox
        body_rect = pymupdf.Rect(72, title_y + 30, W - 72, H - 72)
        page.insert_textbox(
            body_rect,
            page_data["body"],
            fontsize=10.5,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Page number at bottom center
        page_num_text = f"- {i + 1} -"
        page.insert_text(
            pymupdf.Point(W / 2 - 15, H - 40),
            page_num_text,
            fontsize=9,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(W - 72, 50))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
