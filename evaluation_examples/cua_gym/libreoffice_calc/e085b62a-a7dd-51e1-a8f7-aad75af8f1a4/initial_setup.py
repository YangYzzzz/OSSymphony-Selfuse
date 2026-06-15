"""
Initial Setup: Collected Academic Papers Document
Task ID: osworld_multi_apps_book_splitting_nav_010
Domain: libreoffice_writer (ODT)

Creates:
  - /home/user/Documents/collected_papers.odt — 8 academic papers combined into one document
  - /home/user/Desktop/papers/ — empty directory
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H, P, Span
from odf import teletype

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_010'
OUTPUT = f'{WORKDIR}/Documents/collected_papers.odt'
PAPERS_DIR = f'{WORKDIR}/Desktop/papers'


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


# Paper data: (number, title, slug, abstract_text, intro_text, methods_text, results_text, conclusion_text)
PAPERS = [
    {
        "num": "01",
        "title": "Neural Networks for Image Recognition",
        "slug": "neural_networks_for_image_recognition",
        "authors": "J. Smith, A. Wang, L. Chen",
        "year": 2023,
        "abstract": (
            "This paper presents a comprehensive study of deep neural network architectures "
            "for image recognition tasks. We investigate convolutional neural networks (CNNs) "
            "with varying depths and widths, comparing their performance on standard benchmarks "
            "including ImageNet and CIFAR-100. Our experiments demonstrate that residual "
            "connections significantly improve training stability and final accuracy. We achieve "
            "a top-1 accuracy of 78.4% on ImageNet using a novel architecture that combines "
            "depthwise separable convolutions with squeeze-and-excitation blocks. The proposed "
            "model reduces parameter count by 35% compared to baseline ResNet-50 while "
            "maintaining competitive performance."
        ),
        "intro": (
            "Image recognition has been a fundamental challenge in computer vision for decades. "
            "With the advent of deep learning, convolutional neural networks have dramatically "
            "advanced the state of the art. Early pioneering work by LeCun et al. (1998) "
            "established the foundation for modern CNN architectures. The breakthrough of AlexNet "
            "in 2012 demonstrated the power of deep CNNs trained on large datasets with GPU "
            "acceleration. Since then, architectures such as VGGNet, GoogLeNet, ResNet, and "
            "DenseNet have pushed performance boundaries ever further.\n\n"
            "Despite these advances, challenges remain in balancing model complexity with "
            "computational efficiency. This paper addresses the need for lightweight yet "
            "accurate architectures suitable for deployment on resource-constrained devices."
        ),
        "methods": (
            "Our proposed architecture builds upon the ResNet framework with three key "
            "modifications. First, we replace standard 3x3 convolutions with depthwise "
            "separable convolutions to reduce parameter count. Second, we introduce "
            "squeeze-and-excitation (SE) blocks after each residual unit to enable "
            "channel-wise feature recalibration. Third, we employ a progressive training "
            "schedule with data augmentation including random cropping, horizontal flipping, "
            "and color jitter. Training was performed on 8 NVIDIA V100 GPUs using SGD with "
            "momentum 0.9 and an initial learning rate of 0.1, decayed by a factor of 10 "
            "at epochs 30, 60, and 90."
        ),
        "results": (
            "Table 1 summarizes the performance comparison across different architectures. "
            "Our model achieves 78.4% top-1 accuracy on ImageNet validation set, surpassing "
            "EfficientNet-B0 (77.1%) and MobileNetV3-Large (75.2%) while using fewer "
            "parameters. On CIFAR-100, we achieve 82.3% accuracy compared to 81.4% for "
            "baseline ResNet-56. Ablation studies confirm that both SE blocks (+1.2%) and "
            "depthwise separable convolutions (+0.8%) contribute to the final performance "
            "gain. Inference time on a single GPU is 2.3ms per image, representing a 40% "
            "speedup over the ResNet-50 baseline."
        ),
        "conclusion": (
            "We have presented a novel CNN architecture that achieves state-of-the-art "
            "performance on image recognition benchmarks while maintaining computational "
            "efficiency. The combination of depthwise separable convolutions and SE blocks "
            "proves effective for building compact yet powerful models. Future work will "
            "explore neural architecture search techniques to further optimize the design "
            "space. We also plan to extend the approach to object detection and semantic "
            "segmentation tasks, where efficiency is equally critical."
        ),
    },
    {
        "num": "02",
        "title": "Transformer Models in Natural Language Processing",
        "slug": "transformer_models_in_natural_language_processing",
        "authors": "M. Johnson, R. Patel, K. Yamamoto",
        "year": 2023,
        "abstract": (
            "The Transformer architecture has revolutionized natural language processing "
            "since its introduction in 2017. This survey examines the evolution of Transformer "
            "variants including BERT, GPT, T5, and their successors, analyzing their "
            "architectural innovations and performance characteristics. We conduct a systematic "
            "comparison across 12 NLP benchmarks covering text classification, named entity "
            "recognition, question answering, and machine translation. Our analysis reveals "
            "that pre-training objectives, model scale, and data quality are the primary "
            "determinants of downstream task performance. We also discuss emerging trends "
            "including efficient attention mechanisms and mixture-of-experts architectures."
        ),
        "intro": (
            "Natural language processing has undergone a profound transformation with the "
            "introduction of the Transformer architecture by Vaswani et al. (2017). The "
            "self-attention mechanism at its core enables parallel processing of sequences "
            "and captures long-range dependencies more effectively than recurrent neural "
            "networks. The subsequent introduction of BERT (Devlin et al., 2018) demonstrated "
            "the power of bidirectional pre-training, while GPT (Radford et al., 2018) showed "
            "the potential of unidirectional language modeling.\n\n"
            "The field has since witnessed an explosion of Transformer variants, each "
            "introducing specific innovations to address limitations in efficiency, "
            "interpretability, or task-specific performance. This survey aims to provide "
            "a comprehensive overview of these developments."
        ),
        "methods": (
            "We evaluate 15 Transformer variants on 12 standard NLP benchmarks. For each "
            "model, we use publicly available pre-trained weights and fine-tune on "
            "task-specific datasets following standard protocols. Hyperparameters are "
            "selected via grid search on validation sets. We report mean and standard "
            "deviation across 5 random seeds to account for training variance. "
            "Hardware: experiments run on a cluster of 32 A100 80GB GPUs. "
            "Statistical significance is assessed using paired t-tests with Bonferroni "
            "correction for multiple comparisons."
        ),
        "results": (
            "Table 2 presents results across all 12 benchmarks. GPT-4 achieves the highest "
            "average score of 88.7%, followed by PaLM-2 (87.3%) and Claude-2 (86.9%). "
            "Among open-source models, LLaMA-2-70B (83.1%) leads, outperforming Falcon-40B "
            "(80.4%). On reading comprehension tasks (SQuAD 2.0), DeBERTa-v3-large achieves "
            "the best F1 of 91.4. For machine translation (WMT 2022), NLLB-200 achieves "
            "the highest BLEU scores across language pairs. Efficient models (e.g., "
            "Distil-BERT) achieve 97% of BERT performance with 60% fewer parameters."
        ),
        "conclusion": (
            "This survey has provided a comprehensive analysis of Transformer architectures "
            "and their performance across diverse NLP tasks. The rapid scaling of model "
            "parameters has yielded consistent improvements, though with diminishing returns "
            "at extreme scales. Efficient attention mechanisms such as FlashAttention and "
            "linear attention approximations offer promising paths to reduce computational "
            "costs. Looking forward, we expect continued progress in multimodal Transformers "
            "that jointly process text, images, and other modalities. The development of "
            "interpretability methods remains a critical open challenge."
        ),
    },
    {
        "num": "03",
        "title": "Reinforcement Learning for Robotic Control",
        "slug": "reinforcement_learning_for_robotic_control",
        "authors": "S. Garcia, T. Nakamura, H. Williams",
        "year": 2023,
        "abstract": (
            "We present a framework for applying deep reinforcement learning to robotic "
            "manipulation tasks with sparse reward signals. Our approach combines "
            "hindsight experience replay (HER) with a novel curriculum learning strategy "
            "that progressively increases task difficulty. Experiments on a 7-DOF robotic "
            "arm performing object manipulation, assembly, and tool-use tasks demonstrate "
            "that our method achieves 89% success rate on previously unseen object "
            "configurations, outperforming baseline methods by 23 percentage points. "
            "Sim-to-real transfer experiments on a physical Franka Emika Panda robot "
            "validate the approach in real-world settings."
        ),
        "intro": (
            "Robotic manipulation represents one of the most challenging applications of "
            "reinforcement learning due to high-dimensional state and action spaces, "
            "sparse rewards, and the need for precise motor control. Traditional approaches "
            "relied on manually designed reward functions and task-specific heuristics, "
            "limiting scalability to complex real-world scenarios.\n\n"
            "Deep RL methods such as DDPG, SAC, and TD3 have shown promise in simulated "
            "environments but face significant challenges in sample efficiency and "
            "generalization. The gap between simulation and reality (sim-to-real) remains "
            "a critical bottleneck for practical deployment."
        ),
        "methods": (
            "Our framework consists of three components. First, a curriculum generator "
            "that automatically scales task difficulty based on the agent's current "
            "performance level. Second, an enhanced HER implementation that samples "
            "goal-conditioned replay transitions with adaptive strategies. Third, "
            "a domain randomization module that varies physical parameters (friction, "
            "mass, inertia) during training to improve robustness. The policy network "
            "is a 4-layer MLP with 256 units per layer, trained using SAC with "
            "automatic temperature tuning. Training runs for 5 million steps across "
            "16 parallel simulation environments."
        ),
        "results": (
            "Table 3 shows success rates across six manipulation tasks. Our method "
            "achieves an average success rate of 89% compared to 66% for baseline HER "
            "and 71% for curriculum learning without adaptive goal sampling. The "
            "progressive curriculum reduces training time by 40% to reach 80% success "
            "threshold. In sim-to-real transfer experiments, the physical robot achieves "
            "76% success rate on block stacking tasks without any real-world fine-tuning, "
            "compared to 43% for models trained without domain randomization."
        ),
        "conclusion": (
            "We have demonstrated an effective framework for training robotic manipulation "
            "policies using deep reinforcement learning with sparse rewards. The combination "
            "of adaptive curriculum learning and enhanced hindsight experience replay "
            "provides substantial improvements in both sample efficiency and final "
            "performance. The successful sim-to-real transfer validates the practical "
            "utility of the approach. Future work will investigate multi-task learning "
            "where a single policy handles diverse manipulation tasks, and contact-rich "
            "manipulation scenarios requiring tactile sensing."
        ),
    },
    {
        "num": "04",
        "title": "Graph Neural Networks for Molecular Property Prediction",
        "slug": "graph_neural_networks_for_molecular_property_prediction",
        "authors": "L. Anderson, Y. Kim, C. Martinez",
        "year": 2022,
        "abstract": (
            "Predicting molecular properties from chemical structure is fundamental to "
            "drug discovery and materials science. We propose MolGraph-Net, a graph "
            "neural network architecture that incorporates atomic features, bond types, "
            "and 3D geometric information for accurate property prediction. Evaluated "
            "on 17 molecular property benchmarks from MoleculeNet including ESOL, "
            "FreeSolv, Lipophilicity, and HIV, our model achieves state-of-the-art "
            "results on 14 of 17 tasks. The geometric encoding module provides an "
            "average improvement of 8.3% over 2D-only baselines, demonstrating the "
            "value of 3D structural information."
        ),
        "intro": (
            "The ability to predict molecular properties computationally accelerates "
            "the drug discovery pipeline by enabling virtual screening of large chemical "
            "libraries. Traditional approaches relied on handcrafted molecular fingerprints "
            "or physics-based simulations, which are either insufficiently expressive or "
            "computationally prohibitive at scale.\n\n"
            "Graph neural networks have emerged as a natural framework for molecular "
            "representation learning, treating atoms as nodes and bonds as edges. "
            "Models such as MPNN, D-MPNN, and AttentiveFP have advanced the field "
            "significantly but typically ignore 3D geometric information available "
            "from quantum chemical calculations."
        ),
        "methods": (
            "MolGraph-Net processes molecules as attributed graphs where nodes represent "
            "atoms with features including atomic number, hybridization, formal charge, "
            "and ring membership. Edge features encode bond type, conjugation, and "
            "ring membership. The geometric module processes 3D coordinates through "
            "equivariant message passing layers following the E(n)-equivariant GNN "
            "framework. Multiple rounds of message passing are performed before global "
            "pooling to obtain molecular representations. Property-specific output heads "
            "with task-appropriate activation functions handle regression and "
            "classification tasks."
        ),
        "results": (
            "Table 4 compares MolGraph-Net against 8 baseline methods across 17 "
            "benchmarks. Our model achieves RMSE of 0.553 on ESOL (best published: "
            "0.555), MAE of 0.982 on FreeSolv, and RMSE of 0.534 on Lipophilicity. "
            "For classification tasks, we achieve ROC-AUC of 0.812 on HIV and "
            "0.892 on BBBP. The geometric module provides improvements on 15 of 17 "
            "tasks, with the largest gains on conformational tasks where 3D structure "
            "most directly determines properties."
        ),
        "conclusion": (
            "MolGraph-Net demonstrates that incorporating 3D geometric information "
            "substantially improves molecular property prediction across diverse tasks. "
            "The equivariant geometric processing ensures physical consistency and "
            "enables generalization to different molecular orientations. The model "
            "provides a strong foundation for virtual screening applications in drug "
            "discovery. Future directions include incorporation of protein-ligand "
            "interactions for binding affinity prediction and extension to larger "
            "macromolecular structures."
        ),
    },
    {
        "num": "05",
        "title": "Federated Learning for Privacy-Preserving Machine Learning",
        "slug": "federated_learning_for_privacy_preserving_machine_learning",
        "authors": "R. Thompson, N. Sharma, O. Petrov",
        "year": 2022,
        "abstract": (
            "Federated learning enables training machine learning models across "
            "distributed data sources without sharing raw data, preserving privacy "
            "by design. This paper addresses the challenges of statistical "
            "heterogeneity and communication efficiency in federated settings. "
            "We propose FedAdapt, an adaptive aggregation algorithm that dynamically "
            "weights client updates based on local data distribution estimates. "
            "Experiments on benchmark datasets across healthcare and finance "
            "domains demonstrate convergence improvements of 18-34% over FedAvg "
            "with 40% reduction in communication rounds, while maintaining "
            "differential privacy guarantees with epsilon=1.0."
        ),
        "intro": (
            "The proliferation of data-generating devices and increasing privacy "
            "regulations such as GDPR and HIPAA have created strong incentives for "
            "distributed learning approaches. Federated learning, introduced by "
            "McMahan et al. (2017), trains global models through aggregation of "
            "locally computed updates, keeping sensitive data on-device.\n\n"
            "Two fundamental challenges limit practical deployment: statistical "
            "heterogeneity (non-IID data distributions across clients) and "
            "communication overhead. Standard algorithms like FedAvg suffer "
            "from slow convergence under data heterogeneity, and each round "
            "requires transmitting full model gradients."
        ),
        "methods": (
            "FedAdapt extends FedAvg with two key innovations. First, each client "
            "computes a lightweight distribution fingerprint using a random projection "
            "of local data statistics. These fingerprints are shared with the server "
            "(they contain no private information) to estimate client similarity. "
            "Second, the server computes adaptive aggregation weights using the "
            "similarity matrix, downweighting updates from outlier distributions. "
            "Communication efficiency is improved through gradient sparsification "
            "and quantization. Privacy is guaranteed via local differential privacy "
            "with Gaussian noise mechanism."
        ),
        "results": (
            "Table 5 presents convergence comparison on CIFAR-10 (100 clients), "
            "FEMNIST (3400 clients), and synthetic healthcare data (50 hospitals). "
            "FedAdapt achieves target accuracy (80%) in 234 rounds vs 389 for FedAvg "
            "on CIFAR-10 (40% reduction). Final accuracy improves by 2.1% on average. "
            "Communication cost per round is reduced by 68% through sparsification. "
            "Privacy-utility tradeoff analysis shows FedAdapt maintains advantages "
            "under differential privacy (epsilon=1.0, delta=1e-5)."
        ),
        "conclusion": (
            "FedAdapt provides a practical solution to the twin challenges of "
            "statistical heterogeneity and communication efficiency in federated "
            "learning. The adaptive weighting mechanism improves convergence "
            "without compromising privacy guarantees. The approach scales to "
            "thousands of clients and handles diverse data distributions encountered "
            "in real-world deployments. Future work will explore personalized "
            "federated learning where clients maintain local model adaptations "
            "while benefiting from global knowledge sharing."
        ),
    },
    {
        "num": "06",
        "title": "Attention Mechanisms in Computer Vision",
        "slug": "attention_mechanisms_in_computer_vision",
        "authors": "E. Brown, F. Liu, G. Okonkwo",
        "year": 2022,
        "abstract": (
            "Attention mechanisms have become ubiquitous in computer vision, from "
            "channel attention in SENet to spatial attention in CBAM and global "
            "self-attention in Vision Transformers. This paper provides a systematic "
            "taxonomy of visual attention mechanisms and empirically evaluates their "
            "computational efficiency and performance tradeoffs. We introduce AttnBench, "
            "a standardized benchmark evaluating 24 attention variants on image "
            "classification, object detection, and semantic segmentation. Our analysis "
            "reveals that window-based attention provides the best efficiency-accuracy "
            "tradeoff, while deformable attention excels on dense prediction tasks."
        ),
        "intro": (
            "The concept of attention, inspired by human visual processing, has "
            "fundamentally changed the design of visual recognition systems. "
            "Squeeze-and-excitation networks (SENet, Hu et al., 2018) introduced "
            "channel attention, enabling selective amplification of informative "
            "feature channels. CBAM (Woo et al., 2018) extended this with spatial "
            "attention. Vision Transformer (ViT, Dosovitskiy et al., 2020) replaced "
            "convolutions entirely with global self-attention.\n\n"
            "Despite extensive empirical work, a unified understanding of when "
            "different attention variants are most beneficial remains elusive. "
            "This paper aims to fill this gap through systematic benchmarking."
        ),
        "methods": (
            "AttnBench evaluates attention mechanisms by inserting them into a "
            "standardized ResNet-50 backbone. For object detection and segmentation, "
            "we use FPN with standard Faster R-CNN and DeepLab heads. Each attention "
            "variant is evaluated with 3 random seeds. We report FLOPs per image, "
            "parameter overhead, throughput (images/second), and task-specific "
            "metrics. Evaluation datasets: ImageNet (1K), COCO (detection), "
            "ADE20K (segmentation). Ablation experiments identify the contribution "
            "of different attention design choices."
        ),
        "results": (
            "Table 6 summarizes AttnBench results. Channel attention (SE) adds "
            "minimal overhead (+2.5% params) with +1.1% top-1 accuracy on ImageNet. "
            "Spatial attention (CBAM) provides +1.4% at +7% params. Window-based "
            "self-attention (Swin) achieves the best accuracy (83.5%) with "
            "competitive throughput. Deformable attention achieves +3.2 mAP "
            "improvement on COCO detection vs. standard ViT. Global self-attention "
            "scales poorly with image resolution due to quadratic complexity."
        ),
        "conclusion": (
            "Our systematic evaluation through AttnBench reveals clear performance-"
            "efficiency tradeoffs across visual attention mechanisms. Window-based "
            "attention mechanisms strike the best balance for general-purpose vision "
            "tasks, while deformable attention is preferred for dense prediction "
            "applications. Channel attention provides a cost-effective performance "
            "boost for any backbone. These findings provide practical guidance for "
            "practitioners selecting attention mechanisms for specific applications. "
            "Future work will extend the benchmark to video understanding tasks."
        ),
    },
    {
        "num": "07",
        "title": "Generative Adversarial Networks for Data Augmentation",
        "slug": "generative_adversarial_networks_for_data_augmentation",
        "authors": "A. Wilson, D. Santos, I. Johansson",
        "year": 2021,
        "abstract": (
            "Data scarcity is a persistent challenge in supervised learning, "
            "particularly in medical imaging and industrial inspection where "
            "annotated data is expensive to obtain. We investigate the use of "
            "conditional generative adversarial networks (cGANs) for augmenting "
            "training datasets in low-data regimes. Our framework, AugGAN, generates "
            "class-conditional synthetic images that capture intra-class variability "
            "while respecting class boundaries. Evaluated on skin lesion classification "
            "(ISIC 2019) and defect detection (MVTec-AD) datasets with 10-100 labeled "
            "samples, AugGAN improves classification accuracy by 7-15% over standard "
            "augmentation baselines."
        ),
        "intro": (
            "Deep learning models are notoriously data-hungry, requiring thousands "
            "of labeled examples to achieve good generalization. In many practical "
            "domains, obtaining labeled data is prohibitively expensive or time-"
            "consuming. Medical image annotation requires clinical expertise, "
            "industrial inspection datasets require controlled manufacturing defects, "
            "and satellite imagery requires expert geospatial analysis.\n\n"
            "Traditional augmentation techniques (flipping, rotation, color jitter) "
            "provide limited diversity and cannot generate novel semantic variations. "
            "GANs offer the potential to generate realistic synthetic examples, "
            "but controlling output diversity and class fidelity remains challenging."
        ),
        "methods": (
            "AugGAN uses a conditional GAN architecture with a ResNet-based "
            "generator and PatchGAN discriminator. Class conditioning is implemented "
            "via class-conditional batch normalization in the generator and projection "
            "discriminator. Training stability is improved through spectral normalization "
            "and two-timescale update rule (TTUR). We introduce a novel diversity loss "
            "that penalizes mode collapse by encouraging generated images to cover "
            "the intra-class distribution. The augmentation strategy selects synthetic "
            "samples based on uncertainty scores from the downstream classifier."
        ),
        "results": (
            "Table 7 shows classification accuracy as a function of labeled sample "
            "count. With 10 labeled samples per class, AugGAN achieves 68.3% accuracy "
            "on ISIC 2019 vs. 58.1% for standard augmentation (+10.2%). With 100 "
            "samples, the gap narrows to 78.9% vs. 74.2% (+4.7%). FID scores confirm "
            "high synthetic image quality (FID=18.3 on ISIC vs. real data). On MVTec-AD "
            "defect detection, AugGAN improves AUROC by 6.8% with 20 anomaly examples, "
            "compared to 3.1% for CutPaste baseline."
        ),
        "conclusion": (
            "AugGAN demonstrates that GAN-based augmentation provides meaningful "
            "improvements in low-data regimes where traditional augmentation is "
            "insufficient. The diversity loss is critical for preventing mode collapse "
            "and ensuring generated data covers the true intra-class distribution. "
            "As labeled data increases, the relative benefit of synthetic augmentation "
            "decreases, suggesting adaptive augmentation strategies should be used. "
            "Future work will explore diffusion-model-based augmentation and "
            "few-shot generation approaches for extreme data scarcity."
        ),
    },
    {
        "num": "08",
        "title": "Knowledge Distillation for Model Compression",
        "slug": "knowledge_distillation_for_model_compression",
        "authors": "P. Lee, Q. Hassan, V. Rodriguez",
        "year": 2021,
        "abstract": (
            "Knowledge distillation transfers learned representations from large "
            "teacher models to compact student models, enabling deployment on "
            "resource-constrained devices. We present KD-Pro, a progressive "
            "distillation framework that hierarchically transfers knowledge at "
            "multiple semantic levels including features, attention maps, and "
            "logits. Evaluated on image classification, object detection, and "
            "semantic segmentation, KD-Pro achieves student models that retain "
            "95% of teacher accuracy while reducing model size by 4x and "
            "inference latency by 3.2x. Our ablation study identifies that "
            "intermediate feature matching contributes 40% of total performance "
            "recovery."
        ),
        "intro": (
            "The trend toward ever-larger neural networks has yielded impressive "
            "performance gains but created a significant deployment gap: models "
            "with billions of parameters cannot be practically deployed on edge "
            "devices with limited compute, memory, and battery. Knowledge "
            "distillation, introduced by Hinton et al. (2015), addresses this "
            "gap by training compact student models to mimic large teacher models.\n\n"
            "Standard KD transfers only output distributions (soft targets), "
            "leaving substantial information in intermediate representations "
            "untapped. Feature-level distillation methods such as FitNets and "
            "AT have shown that matching intermediate representations improves "
            "student performance but require careful layer alignment."
        ),
        "methods": (
            "KD-Pro implements a three-stage distillation pipeline. Stage 1 "
            "trains the student to match teacher feature maps at multiple "
            "resolution levels using L2 loss with learned projections to handle "
            "dimension mismatch. Stage 2 transfers attention patterns by "
            "minimizing KL divergence between self-attention maps. Stage 3 "
            "applies standard output distillation with temperature-scaled "
            "softmax. The three stages are fine-tuned jointly in a final "
            "stage with weighted loss combination. Student architectures "
            "are derived from teacher models through structured pruning."
        ),
        "results": (
            "Table 8 summarizes compression results across 6 teacher-student "
            "pairs. For ResNet-50 to ResNet-18 distillation, KD-Pro achieves "
            "70.8% top-1 accuracy (vs. 69.4% for standard KD, +1.4%). "
            "For BERT-base to BERT-tiny, we achieve 84.3% on GLUE benchmark "
            "(vs. 82.1% baseline). Detection: RetinaNet-R101 to RetinaNet-R50 "
            "achieves 38.1 mAP (vs. 36.4 standard KD). Segmentation: "
            "DeepLab-ResNet-101 to DeepLab-ResNet-50 achieves 39.2 mIoU. "
            "Latency reduction of 3.2x validated on NVIDIA Jetson Nano."
        ),
        "conclusion": (
            "KD-Pro provides a systematic and effective framework for knowledge "
            "distillation across diverse vision and language tasks. The progressive "
            "three-stage approach ensures comprehensive knowledge transfer from "
            "teacher to student at multiple levels of abstraction. The consistent "
            "improvements over standard KD baseline demonstrate the value of "
            "intermediate feature and attention matching. Deployment experiments "
            "confirm practical benefits on edge hardware. Future work will "
            "investigate self-distillation where a model is compressed using "
            "its own earlier training snapshots as teachers."
        ),
    },
]


def create_initial():
    # Ensure Documents dir exists
    docs_dir = f'{WORKDIR}/Documents'
    os.makedirs(docs_dir, exist_ok=True)
    # Ensure Desktop/papers dir exists and is empty
    os.makedirs(PAPERS_DIR, exist_ok=True)
    # Remove any files from papers dir (idempotent)
    for fname in os.listdir(PAPERS_DIR):
        fpath = os.path.join(PAPERS_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)

    doc = OpenDocumentText()

    # ---- Define Heading styles ----
    h1_style = Style(name="Heading 1", family="paragraph")
    h1_style.addElement(
        ParagraphProperties(breakbefore="page")
    )
    h1_style.addElement(
        TextProperties(fontsize="18pt", fontweight="bold")
    )
    doc.styles.addElement(h1_style)

    h2_style = Style(name="Heading 2", family="paragraph")
    h2_style.addElement(
        TextProperties(fontsize="14pt", fontweight="bold")
    )
    doc.styles.addElement(h2_style)

    body_style = Style(name="TextBody", family="paragraph")
    body_style.addElement(
        TextProperties(fontsize="11pt")
    )
    doc.styles.addElement(body_style)

    def add_heading1(text):
        h = H(outlinelevel=1, stylename="Heading 1")
        h.addText(text)
        doc.text.addElement(h)

    def add_heading2(text):
        h = H(outlinelevel=2, stylename="Heading 2")
        h.addText(text)
        doc.text.addElement(h)

    def add_para(text):
        p = P(stylename="TextBody")
        p.addText(text)
        doc.text.addElement(p)

    # Build document: one paper per Heading 1 section
    for paper in PAPERS:
        add_heading1(paper["title"])
        add_para(f"Authors: {paper['authors']}")
        add_para(f"Year: {paper['year']}")

        add_heading2("Abstract")
        add_para(paper["abstract"])

        add_heading2("Introduction")
        add_para(paper["intro"])

        add_heading2("Methods")
        add_para(paper["methods"])

        add_heading2("Results")
        add_para(paper["results"])

        add_heading2("Conclusion")
        add_para(paper["conclusion"])

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Desktop/papers/ directory created: {PAPERS_DIR}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
