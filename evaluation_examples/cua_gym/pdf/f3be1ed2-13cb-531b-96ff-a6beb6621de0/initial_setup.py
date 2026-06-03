"""
Initial Setup: Create a 40-page bundled proceedings PDF
Task ID: pdf_res_066
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_066'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/proceedings_bundle.pdf'

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


# Paper metadata for 5 realistic academic papers
PAPERS = [
    {
        "title": "Efficient Transformer Architectures for Low-Resource Neural Machine Translation",
        "authors": "Sarah Chen, Marcus Johnson, Priya Patel",
        "affiliation": "Department of Computer Science, Stanford University",
        "abstract": (
            "Neural machine translation (NMT) systems have achieved remarkable performance on high-resource "
            "language pairs, yet remain challenging for low-resource settings. In this paper, we propose a novel "
            "transformer architecture that incorporates cross-lingual transfer learning and parameter-efficient "
            "fine-tuning strategies. Our approach reduces the number of trainable parameters by 60% while "
            "maintaining competitive BLEU scores across 12 low-resource language pairs. We conduct extensive "
            "experiments on the FLORES-200 benchmark and demonstrate that our method outperforms existing "
            "approaches by an average of 3.2 BLEU points. Furthermore, we introduce a new data augmentation "
            "technique that leverages monolingual corpora to improve translation quality in extremely "
            "low-resource scenarios with fewer than 10,000 parallel sentences."
        ),
        "sections": [
            ("1. Introduction", [
                "Machine translation has seen tremendous progress with the advent of neural approaches, "
                "particularly the Transformer architecture introduced by Vaswani et al. (2017). However, the "
                "performance of these models heavily depends on the availability of large-scale parallel corpora, "
                "which are scarce for the majority of the world's languages.",
                "Recent studies have explored various strategies to address the low-resource challenge, including "
                "multilingual pre-training, back-translation, and transfer learning from related high-resource "
                "language pairs. Despite these advances, there remains a significant performance gap between "
                "high-resource and low-resource translation systems.",
                "In this work, we propose EfficientMT, a parameter-efficient transformer architecture specifically "
                "designed for low-resource neural machine translation. Our key contributions are threefold: (1) a "
                "novel adapter module that enables efficient cross-lingual transfer, (2) a curriculum learning "
                "strategy that progressively increases translation difficulty, and (3) a data augmentation method "
                "that generates synthetic parallel data from monolingual sources."
            ]),
            ("2. Related Work", [
                "Transfer learning for NMT has been extensively studied in recent years. Zoph et al. (2016) "
                "demonstrated that initializing a low-resource model with parameters from a high-resource parent "
                "model significantly improves translation quality. Neubig and Hu (2018) extended this approach by "
                "exploring rapid adaptation techniques for extremely low-resource languages.",
                "Parameter-efficient fine-tuning methods, such as adapters (Houlsby et al., 2019) and LoRA "
                "(Hu et al., 2022), have shown promise in reducing computational costs while maintaining model "
                "quality. Bapna and Firat (2019) applied adapter layers to multilingual NMT, achieving competitive "
                "results with significantly fewer trainable parameters.",
                "Data augmentation strategies for NMT include back-translation (Sennrich et al., 2016), "
                "tagged back-translation (Caswell et al., 2019), and self-training approaches. Our method builds "
                "upon these foundations while introducing novel techniques for leveraging monolingual data."
            ]),
            ("3. Methodology", [
                "Our EfficientMT framework consists of three main components: the base transformer encoder-decoder, "
                "cross-lingual adapter modules, and a curriculum-based training procedure. The base architecture "
                "follows the standard Transformer with 6 encoder and 6 decoder layers, 8 attention heads, and a "
                "model dimension of 512.",
                "The cross-lingual adapter modules are inserted between the self-attention and feed-forward "
                "sub-layers of both the encoder and decoder. Each adapter consists of a down-projection layer "
                "(d_model to d_adapter), a non-linear activation function (GeLU), and an up-projection layer "
                "(d_adapter to d_model), with a residual connection. We set d_adapter = 64, resulting in only "
                "2.1M additional parameters per adapter.",
                "During training, we first pre-train the base model on a high-resource language pair (English-German "
                "with 4.5M sentence pairs from WMT'19). We then freeze the base model parameters and train only "
                "the adapter modules on the target low-resource pair. This two-stage approach enables efficient "
                "knowledge transfer while preserving the general translation capabilities of the pre-trained model."
            ]),
            ("4. Experiments", [
                "We evaluate our approach on 12 low-resource language pairs from the FLORES-200 benchmark, "
                "covering diverse language families including Turkic, Bantu, Austronesian, and Dravidian languages. "
                "For each pair, we use the standard train/dev/test splits provided by the benchmark.",
                "Baseline systems include: (1) a vanilla Transformer trained from scratch, (2) mBART-50 fine-tuned "
                "on the target pair, (3) NLLB-200 (distilled 600M), and (4) the adapter-based approach of Bapna "
                "and Firat (2019). All models are trained with the same hyperparameters: learning rate 5e-4, "
                "batch size 4096 tokens, and 100K training steps.",
                "Table 1 presents the BLEU scores on the FLORES-200 devtest set. Our EfficientMT achieves the "
                "highest average BLEU score of 24.7 across all 12 language pairs, outperforming the strongest "
                "baseline (NLLB-200) by 3.2 points. Notably, the improvement is most pronounced for extremely "
                "low-resource pairs (< 50K parallel sentences), where we observe gains of up to 5.8 BLEU points."
            ]),
            ("5. Analysis and Discussion", [
                "To understand the contribution of each component, we conduct an ablation study removing one "
                "component at a time from our full system. Removing the cross-lingual adapters reduces the average "
                "BLEU score by 2.1 points, confirming their importance for knowledge transfer. Disabling the "
                "curriculum learning strategy leads to a 1.4-point decrease, while removing data augmentation "
                "results in a 1.8-point drop.",
                "We also analyze the effect of adapter size on translation quality. With d_adapter values of "
                "32, 64, 128, and 256, we find that d_adapter = 64 provides the best trade-off between parameter "
                "efficiency and translation quality. Larger adapters show diminishing returns while significantly "
                "increasing the number of trainable parameters."
            ]),
            ("6. Conclusion", [
                "We presented EfficientMT, a parameter-efficient transformer architecture for low-resource neural "
                "machine translation. Through cross-lingual adapters, curriculum learning, and novel data "
                "augmentation techniques, our approach achieves state-of-the-art results on the FLORES-200 "
                "benchmark while using 60% fewer trainable parameters than comparable systems. Future work will "
                "explore extending our approach to zero-shot translation and document-level NMT."
            ]),
        ],
        "pages": 8,
    },
    {
        "title": "Deep Reinforcement Learning for Autonomous Warehouse Navigation with Dynamic Obstacles",
        "authors": "James Liu, Anna Kowalski, Roberto Fernandez",
        "affiliation": "Robotics Institute, Carnegie Mellon University",
        "abstract": (
            "Autonomous navigation in dynamic warehouse environments presents unique challenges due to the "
            "presence of moving obstacles such as human workers, forklifts, and other robotic agents. We present "
            "a deep reinforcement learning framework that combines model-based planning with model-free control "
            "to achieve safe and efficient navigation in cluttered warehouse settings. Our approach utilizes a "
            "hierarchical policy architecture where a high-level planner selects waypoints and a low-level "
            "controller generates smooth trajectories. Experiments in both simulation and real-world warehouse "
            "environments demonstrate that our method reduces collision rates by 78% compared to traditional "
            "path planning algorithms while maintaining comparable navigation speed."
        ),
        "sections": [
            ("1. Introduction", [
                "The rapid growth of e-commerce has driven unprecedented demand for warehouse automation. Mobile "
                "robots are increasingly deployed for tasks such as inventory management, order picking, and "
                "package sorting. However, navigating safely in environments shared with human workers and other "
                "moving entities remains a fundamental challenge.",
                "Traditional path planning methods, such as A* and RRT, assume static or slowly changing "
                "environments and often fail to react quickly to dynamic obstacles. Reactive approaches based on "
                "potential fields or velocity obstacles can handle dynamic scenarios but may produce suboptimal "
                "paths or get trapped in local minima.",
                "In this paper, we propose HierNav, a hierarchical deep reinforcement learning framework for "
                "autonomous warehouse navigation. Our system operates at two levels: a strategic planner that "
                "reasons about global navigation objectives and a tactical controller that handles local obstacle "
                "avoidance and trajectory generation."
            ]),
            ("2. Problem Formulation", [
                "We formulate the warehouse navigation problem as a Partially Observable Markov Decision Process "
                "(POMDP). The robot observes its local surroundings through LiDAR sensors (360-degree, 10m range) "
                "and an RGB-D camera (120-degree field of view). The observation space includes a local occupancy "
                "grid (20x20 cells, 0.25m resolution), detected obstacle velocities, and the robot's own state "
                "(position, velocity, heading).",
                "The action space is continuous, consisting of linear velocity v in [0, 1.5] m/s and angular "
                "velocity omega in [-1.0, 1.0] rad/s. The reward function includes terms for goal proximity "
                "(r_goal = -0.1 * d_goal), collision penalty (r_collision = -100), progress reward "
                "(r_progress = 10 * delta_d), and smoothness penalty (r_smooth = -0.05 * |delta_omega|)."
            ]),
            ("3. HierNav Architecture", [
                "The high-level planner operates at 2 Hz and selects intermediate waypoints from a discretized "
                "set of candidates generated by sampling points on a visibility graph. It uses a Graph Neural "
                "Network (GNN) to encode the spatial relationships between waypoint candidates and obstacles, "
                "followed by an attention mechanism to select the most promising waypoint.",
                "The low-level controller operates at 10 Hz and generates continuous velocity commands to navigate "
                "toward the selected waypoint while avoiding obstacles. It is implemented as a Soft Actor-Critic "
                "(SAC) agent with a CNN encoder for processing the local occupancy grid and an MLP for combining "
                "sensor features with the waypoint target.",
                "Both levels are trained jointly using a two-phase curriculum: Phase 1 trains the low-level "
                "controller in simple environments with static obstacles, while Phase 2 introduces dynamic "
                "obstacles and trains the full hierarchical system end-to-end."
            ]),
            ("4. Simulation Experiments", [
                "We evaluate HierNav in three simulated warehouse environments of increasing complexity: "
                "SmallWarehouse (500 sq.m, 5 dynamic obstacles), MediumWarehouse (2000 sq.m, 15 dynamic obstacles), "
                "and LargeWarehouse (5000 sq.m, 30 dynamic obstacles). Dynamic obstacles include simulated "
                "forklifts (v_max = 2.0 m/s), human workers (v_max = 1.5 m/s), and other robots (v_max = 1.0 m/s).",
                "Table 2 shows the comparison results. HierNav achieves the lowest collision rate (0.8%) in "
                "the LargeWarehouse scenario, compared to 3.6% for DWA, 2.1% for ORCA, and 1.5% for the "
                "end-to-end RL baseline. Navigation efficiency, measured as the ratio of actual path length to "
                "optimal path length, is 1.12 for HierNav versus 1.08 for A* (which has a 5.2% collision rate).",
                "We also evaluate robustness to sensor noise by adding Gaussian noise (sigma = 0.1m) to LiDAR "
                "readings and reducing camera resolution by 50%. HierNav maintains a collision rate below 1.5% "
                "under these degraded conditions, while baseline methods see collision rates increase by 2-3x."
            ]),
            ("5. Real-World Deployment", [
                "We deploy HierNav on a fleet of 3 TurtleBot3 Waffle Pi robots in a 200 sq.m mock warehouse "
                "environment. The warehouse contains 4 aisles with shelving units, a central sorting area, and "
                "designated loading zones. Two human operators walk through the environment performing typical "
                "warehouse tasks.",
                "Over 50 navigation trials (total distance: 2.3 km), HierNav achieves zero collisions with "
                "an average navigation speed of 0.8 m/s. The sim-to-real transfer is facilitated by domain "
                "randomization during training and online adaptation of the low-level controller using a small "
                "buffer of real-world experiences."
            ]),
            ("6. Conclusion", [
                "We presented HierNav, a hierarchical deep reinforcement learning framework for autonomous "
                "warehouse navigation. By decomposing the navigation task into strategic planning and tactical "
                "control, our approach achieves safe and efficient navigation in complex dynamic environments. "
                "Future work includes multi-agent coordination and integration with warehouse management systems "
                "for task-level optimization."
            ]),
        ],
        "pages": 7,
    },
    {
        "title": "Federated Learning with Differential Privacy for Electronic Health Records: A Multi-Institutional Study",
        "authors": "Elena Vasquez, David Kim, Fatima Al-Rashidi, Thomas Mueller",
        "affiliation": "School of Medicine and Department of Biomedical Informatics, Columbia University",
        "abstract": (
            "Electronic health records (EHRs) contain invaluable information for clinical research and "
            "predictive modeling, but privacy regulations such as HIPAA severely limit data sharing across "
            "institutions. We present PrivHealth, a federated learning framework with formal differential "
            "privacy guarantees for training predictive models on distributed EHR data. Our approach combines "
            "secure aggregation with noise-calibrated gradient updates to achieve (epsilon, delta)-differential "
            "privacy while maintaining clinically useful model accuracy. In a multi-institutional study across "
            "5 hospital systems covering 2.3 million patient records, PrivHealth achieves AUROC of 0.89 for "
            "30-day readmission prediction, within 2% of centralized training, while providing provable privacy "
            "guarantees with epsilon = 3.0."
        ),
        "sections": [
            ("1. Introduction", [
                "The digitization of healthcare records has created unprecedented opportunities for data-driven "
                "clinical research. Machine learning models trained on large-scale EHR data have shown promise in "
                "predicting patient outcomes, identifying disease subtypes, and optimizing treatment protocols. "
                "However, EHR data is distributed across thousands of healthcare institutions, and stringent "
                "privacy regulations prevent direct data sharing.",
                "Federated learning (FL) offers a paradigm for collaborative model training without data "
                "centralization. In FL, participating institutions train local models on their own data and share "
                "only model updates (gradients or parameters) with a central server. While FL reduces direct data "
                "exposure, recent work has shown that model updates can leak sensitive patient information through "
                "membership inference and model inversion attacks.",
                "To address these vulnerabilities, we propose PrivHealth, which augments federated learning with "
                "differential privacy (DP) mechanisms. Our contributions include: (1) a noise calibration strategy "
                "that adapts DP noise to the sensitivity of clinical features, (2) a secure aggregation protocol "
                "that prevents the server from observing individual institution updates, and (3) a comprehensive "
                "multi-institutional evaluation demonstrating clinical utility under privacy constraints."
            ]),
            ("2. Background and Related Work", [
                "Differential privacy, formalized by Dwork et al. (2006), provides a mathematical framework for "
                "quantifying privacy loss. A randomized mechanism M satisfies (epsilon, delta)-differential privacy "
                "if for any two adjacent datasets D and D' that differ in a single record, and for any set of "
                "outputs S, we have P[M(D) in S] <= exp(epsilon) * P[M(D') in S] + delta.",
                "McMahan et al. (2018) introduced Federated Averaging (FedAvg), the most widely used FL algorithm, "
                "which aggregates locally trained model updates through weighted averaging. Subsequent work by "
                "Geyer et al. (2017) and McMahan et al. (2018) combined FL with DP by adding Gaussian noise to "
                "clipped gradients.",
                "In the healthcare domain, Sheller et al. (2020) demonstrated FL for brain tumor segmentation "
                "across institutions, while Brisimi et al. (2018) applied FL to EHR-based prediction tasks. "
                "However, most existing healthcare FL systems lack formal privacy guarantees."
            ]),
            ("3. The PrivHealth Framework", [
                "PrivHealth operates in rounds. In each round t, the server broadcasts the current global model "
                "w_t to all participating institutions. Each institution k trains the model locally for E epochs "
                "on its dataset D_k, producing an update delta_k = w_k - w_t. The update is then clipped to "
                "bound its L2 norm: delta_k_clipped = delta_k * min(1, C / ||delta_k||), where C is the "
                "clipping threshold.",
                "Calibrated Gaussian noise is added to the clipped update: delta_k_noisy = delta_k_clipped + "
                "N(0, sigma^2 * C^2 * I), where sigma is determined by the desired privacy budget (epsilon, delta) "
                "and the number of rounds T. The noisy updates are aggregated using secure aggregation, so the "
                "server only observes the sum of noisy updates.",
                "Our key innovation is feature-aware noise calibration. Clinical features vary greatly in "
                "sensitivity: demographic data (age, gender) is less sensitive than diagnostic codes (HIV status, "
                "mental health), which in turn is less sensitive than genomic markers. We partition model parameters "
                "by their associated feature groups and apply different noise levels accordingly."
            ]),
            ("4. Multi-Institutional Evaluation", [
                "We evaluate PrivHealth across 5 hospital systems: two academic medical centers (AMC-1: 800K "
                "patients, AMC-2: 520K patients), two community hospitals (CH-1: 350K patients, CH-2: 280K "
                "patients), and one rural health network (RHN: 150K patients). The total cohort comprises 2.1M "
                "unique patients with 15.3M encounter records spanning 2015-2023.",
                "We focus on three clinically important prediction tasks: (1) 30-day hospital readmission, "
                "(2) in-hospital mortality within 48 hours of ICU admission, and (3) onset of sepsis within 6 "
                "hours. For each task, we use a gradient-boosted tree model with 127 input features derived from "
                "demographics, vital signs, lab results, medications, and diagnosis codes.",
                "Table 3 presents the results. For 30-day readmission, PrivHealth achieves AUROC 0.89 (95% CI: "
                "0.88-0.90) with epsilon = 3.0, compared to 0.91 for centralized training and 0.84 for local-only "
                "training. For ICU mortality, AUROC is 0.93 vs 0.95 (centralized) and 0.87 (local). For sepsis "
                "onset, AUROC is 0.86 vs 0.88 (centralized) and 0.79 (local)."
            ]),
            ("5. Privacy Analysis", [
                "We formally analyze the privacy guarantees of PrivHealth under the Renyi Differential Privacy "
                "(RDP) framework, which provides tighter composition bounds than basic (epsilon, delta)-DP. Using "
                "the moments accountant, we track the cumulative privacy loss across T = 200 communication rounds "
                "with subsampling rate q = 0.01 (100 patients per institution per round).",
                "With our feature-aware noise calibration, the overall privacy budget is epsilon = 3.0 at "
                "delta = 1/N (where N is the total number of patients). This is a substantial improvement over "
                "uniform noise calibration, which requires epsilon = 5.2 to achieve the same model accuracy. "
                "The improvement is attributed to allocating less noise to low-sensitivity features and more "
                "noise to high-sensitivity features."
            ]),
            ("6. Conclusion", [
                "PrivHealth demonstrates that federated learning with differential privacy can achieve clinically "
                "useful prediction accuracy on EHR data while providing formal privacy guarantees. Our feature-aware "
                "noise calibration strategy reduces the accuracy-privacy trade-off by 40% compared to uniform "
                "approaches. We are working with institutional review boards to plan a prospective deployment study "
                "across the participating hospital systems."
            ]),
        ],
        "pages": 7,
    },
    {
        "title": "Scalable Graph Neural Networks for Molecular Property Prediction in Drug Discovery",
        "authors": "Kenji Tanaka, Lisa Berger, Arun Sharma, Michelle Wong",
        "affiliation": "Department of Chemistry and Chemical Biology, Harvard University",
        "abstract": (
            "Accurate prediction of molecular properties is a cornerstone of computational drug discovery, enabling "
            "virtual screening of vast chemical libraries. We introduce MolGraph-XL, a scalable graph neural network "
            "architecture that achieves state-of-the-art performance on molecular property prediction benchmarks "
            "while scaling efficiently to molecules with over 1000 atoms. Our approach employs a multi-scale "
            "message-passing scheme that captures both local chemical interactions and global molecular topology. "
            "On the MoleculeNet benchmark suite, MolGraph-XL achieves average improvements of 4.5% in AUROC for "
            "classification tasks and 12% reduction in RMSE for regression tasks compared to previous best methods. "
            "We demonstrate practical utility by screening 2.1 million compounds against three oncology targets, "
            "identifying 47 novel hit compounds validated through in vitro assays."
        ),
        "sections": [
            ("1. Introduction", [
                "The drug discovery process is notoriously expensive and time-consuming, with an average cost of "
                "$2.6 billion and a timeline of 10-15 years from initial discovery to market approval. Computational "
                "methods that accurately predict molecular properties can significantly accelerate the early stages "
                "of this process by enabling rapid virtual screening and lead optimization.",
                "Graph neural networks (GNNs) have emerged as the dominant paradigm for molecular representation "
                "learning, naturally encoding the graph structure of molecules where atoms are nodes and bonds are "
                "edges. However, existing GNN architectures face limitations in scalability (struggling with large "
                "molecules) and expressiveness (failing to capture long-range interactions).",
                "We present MolGraph-XL, a multi-scale GNN architecture designed to address both challenges. Our "
                "approach introduces: (1) a coarsening-based multi-scale message passing scheme, (2) virtual nodes "
                "that enable global information flow, and (3) an efficient attention mechanism with linear "
                "complexity in the number of atoms."
            ]),
            ("2. Related Work", [
                "Early applications of GNNs to molecular property prediction include the neural fingerprint "
                "(Duvenaud et al., 2015) and Message Passing Neural Network (Gilmer et al., 2017). SchNet "
                "(Schutt et al., 2017) and DimeNet (Gasteiger et al., 2020) incorporate 3D geometric information "
                "to improve predictions for conformational properties.",
                "Recent advances include GIN (Xu et al., 2019), which achieves maximal expressiveness among "
                "message-passing GNNs, and GPS (Rampasek et al., 2022), which combines local message passing "
                "with global attention. Pre-training strategies such as those in Hu et al. (2020) and GraphMVP "
                "(Liu et al., 2022) leverage self-supervised learning on large unlabeled molecular datasets.",
                "Scalability remains an open challenge. Most GNN architectures have quadratic memory complexity "
                "in the number of atoms when using global attention, limiting their applicability to small molecules "
                "(< 100 atoms). Our MolGraph-XL addresses this through efficient multi-scale processing."
            ]),
            ("3. MolGraph-XL Architecture", [
                "The MolGraph-XL architecture consists of three components: a local message-passing module, a "
                "multi-scale coarsening module, and a global readout module. The input molecular graph is "
                "augmented with bond features (type, stereochemistry, conjugation) and atom features (element, "
                "hybridization, formal charge, aromaticity).",
                "The local message-passing module performs K rounds of neighborhood aggregation using a modified "
                "GIN layer with edge features. At each layer, atom representations are updated as: "
                "h_v^(k) = MLP((1 + epsilon) * h_v^(k-1) + sum_{u in N(v)} ReLU(h_u^(k-1) + e_{uv})).",
                "The multi-scale coarsening module creates a hierarchy of increasingly coarse molecular graphs "
                "using the Graclus algorithm. At each coarsening level, pairs of atoms are merged based on their "
                "chemical similarity, creating super-nodes that represent functional groups and larger structural "
                "motifs. Message passing at coarser levels captures long-range interactions efficiently.",
                "The global readout module combines representations from all scales using an attention-weighted "
                "sum: z = sum_s alpha_s * mean(h_v^s), where alpha_s are learned scale attention weights and "
                "h_v^s are atom representations at scale s."
            ]),
            ("4. Experiments", [
                "We evaluate MolGraph-XL on the MoleculeNet benchmark suite (Wu et al., 2018), covering 8 "
                "classification datasets (HIV, BACE, BBBP, Tox21, ToxCast, SIDER, ClinTox, MUV) and 4 regression "
                "datasets (ESOL, FreeSolv, Lipophilicity, QM7). We use scaffold splitting for all datasets and "
                "report results averaged over 3 random seeds.",
                "Table 4 shows the classification results. MolGraph-XL achieves the highest AUROC on 6 of 8 "
                "datasets. On HIV (the largest classification dataset with 41K molecules), we achieve AUROC 0.823 "
                "compared to 0.796 for GPS and 0.781 for GIN. On Tox21 (8K molecules, 12 tasks), we achieve "
                "average AUROC 0.857 compared to 0.844 for the previous best.",
                "For regression tasks, MolGraph-XL reduces RMSE by 8-15% compared to baselines. On QM7 (quantum "
                "mechanics properties), we achieve MAE 57.3 kcal/mol compared to 69.8 for SchNet and 61.2 for "
                "DimeNet, despite not using 3D conformer information."
            ]),
            ("5. Virtual Screening Case Study", [
                "To demonstrate practical utility, we apply MolGraph-XL to virtual screening against three "
                "oncology targets: KRAS G12C (non-small cell lung cancer), CDK4/6 (breast cancer), and PD-L1 "
                "(immunotherapy). We screen the Enamine REAL library subset of 2.1 million commercially available "
                "compounds.",
                "For each target, we train a binary classifier on known active/inactive compounds from ChEMBL "
                "(5K-15K labeled examples per target). The top 500 predicted hits for each target are filtered "
                "for drug-likeness (Lipinski's Rule of Five) and synthetic feasibility, yielding 150-200 "
                "candidates per target.",
                "We experimentally validate a subset of 120 compounds (40 per target) using in vitro binding "
                "assays. Results show a hit rate of 39% (47/120), significantly exceeding the typical high-throughput "
                "screening hit rate of 0.1-1%. Among the confirmed hits, 12 compounds show IC50 values below 1 "
                "micromolar, representing promising lead candidates for further optimization."
            ]),
            ("6. Scalability Analysis", [
                "We analyze the computational efficiency of MolGraph-XL on molecules of varying sizes. Processing "
                "time scales linearly with the number of atoms (O(n)) for our multi-scale approach, compared to "
                "O(n^2) for global attention methods. On molecules with 1000 atoms, MolGraph-XL is 15x faster "
                "than GPS and uses 8x less GPU memory.",
                "Training on the full MoleculeNet suite takes 4.2 hours on a single NVIDIA A100 GPU, compared to "
                "6.8 hours for GPS and 2.1 hours for GIN. The additional cost over GIN is justified by the "
                "consistent accuracy improvements across all benchmarks."
            ]),
            ("7. Conclusion", [
                "MolGraph-XL provides a scalable and expressive GNN architecture for molecular property prediction "
                "that sets new state-of-the-art results across multiple benchmarks. The multi-scale message-passing "
                "scheme efficiently captures both local and global molecular features while maintaining linear "
                "computational complexity. Our virtual screening case study demonstrates direct practical impact in "
                "drug discovery."
            ]),
        ],
        "pages": 8,
    },
    {
        "title": "Causal Inference in Large Language Models: Understanding and Mitigating Spurious Correlations",
        "authors": "Olivia Hernandez, Wei Zhang, Nadia Okafor, Henrik Johansson, Rachel Goldstein",
        "affiliation": "Department of Statistics and Machine Learning, MIT",
        "abstract": (
            "Large language models (LLMs) exhibit remarkable capabilities in natural language understanding and "
            "generation, yet they frequently rely on spurious correlations rather than genuine causal relationships "
            "when making predictions. This paper presents CausalLM, a framework for identifying and mitigating "
            "spurious correlations in LLMs through causal inference techniques. We introduce a structural causal "
            "model (SCM) that formalizes the relationship between input features, confounders, and model predictions, "
            "enabling systematic intervention experiments. Applied to GPT-4, LLaMA-3, and Mistral-7B across four "
            "NLU benchmarks, CausalLM identifies that 23-41% of correct predictions rely on spurious features. "
            "Our mitigation strategy, which combines counterfactual data augmentation with causal regularization, "
            "reduces reliance on spurious correlations by 62% while improving out-of-distribution generalization "
            "by an average of 8.3 percentage points."
        ),
        "sections": [
            ("1. Introduction", [
                "Large language models have achieved impressive performance on a wide range of natural language "
                "understanding tasks, from sentiment analysis to natural language inference. However, mounting "
                "evidence suggests that these models often exploit dataset artifacts and spurious correlations "
                "rather than learning robust linguistic representations.",
                "For example, in natural language inference (NLI), models learn to associate specific words like "
                "'not', 'nobody', and 'never' with the 'contradiction' label, regardless of the actual semantic "
                "relationship between premise and hypothesis. Similarly, in question answering, models may rely on "
                "lexical overlap between the question and context rather than genuine comprehension.",
                "These spurious correlations pose serious risks in high-stakes applications such as medical "
                "diagnosis, legal reasoning, and financial analysis, where model predictions must be based on "
                "causally relevant features. We propose CausalLM, a principled framework for understanding and "
                "mitigating spurious correlations in LLMs using tools from causal inference."
            ]),
            ("2. Structural Causal Model for LLMs", [
                "We formalize the prediction process of an LLM as a structural causal model (SCM) with the "
                "following variables: X (input text), Y (true label), Y_hat (model prediction), Z (causal features "
                "that genuinely determine Y), and S (spurious features that correlate with Y in training data but "
                "do not cause it).",
                "The key causal relationships are: Z -> Y (causal features determine the true label), "
                "Z -> X (causal features are expressed in the input), S -> X (spurious features are present in the "
                "input), S <- U -> Y (spurious features are confounded with the label by latent variable U, "
                "representing dataset construction bias), and X -> Y_hat (the model predicts based on observed input).",
                "Under this SCM, a model that correctly identifies the causal mechanism should satisfy the "
                "interventional criterion: P(Y_hat | do(Z=z)) should change when we intervene on Z, while "
                "P(Y_hat | do(S=s)) should remain constant when we intervene on S (holding Z fixed)."
            ]),
            ("3. Identifying Spurious Correlations", [
                "We propose three complementary methods for identifying spurious features that LLMs rely on:",
                "Counterfactual probing: For each input, we generate counterfactual variants that modify spurious "
                "features while preserving causal features, and vice versa. We use GPT-4 as a counterfactual "
                "generator, guided by task-specific templates that specify which features to intervene on. A model "
                "that changes its prediction when only spurious features change is relying on spurious correlations.",
                "Attention-based causal analysis: We analyze attention patterns to identify which input tokens "
                "receive disproportionate attention relative to their causal relevance. We compute the causal "
                "attention ratio (CAR) as the fraction of total attention mass on causally relevant tokens.",
                "Gradient-based intervention: We compute the gradient of the model's output with respect to input "
                "embeddings and measure the sensitivity to spurious vs. causal features. Features with high "
                "gradient magnitude but no causal relevance are flagged as spurious dependencies."
            ]),
            ("4. Mitigation Strategies", [
                "We propose two complementary mitigation strategies:",
                "Counterfactual data augmentation (CDA): Using the counterfactual generation pipeline from "
                "Section 3, we create augmented training examples where spurious features are randomized while "
                "causal features and labels are preserved. This breaks the spurious correlation S -> Y_hat by "
                "ensuring that S is independent of Y in the augmented training data.",
                "Causal regularization (CR): We add a regularization term to the training loss that penalizes "
                "sensitivity to spurious features: L_CR = lambda * E[|f(x) - f(x')|^2], where x and x' are "
                "counterfactual pairs differing only in spurious features, and lambda controls the regularization "
                "strength. This encourages the model to be invariant to changes in spurious features."
            ]),
            ("5. Experimental Evaluation", [
                "We evaluate CausalLM on four NLU benchmarks: SNLI (natural language inference), FEVER (fact "
                "verification), QQP (paraphrase detection), and BoolQ (yes/no question answering). For each "
                "benchmark, we use the standard train/dev/test splits and also evaluate on challenge sets "
                "designed to test for spurious correlation reliance.",
                "Table 5 presents the results. On in-distribution test sets, CausalLM maintains competitive "
                "accuracy (within 1% of baseline). On challenge sets, our mitigated models show dramatic "
                "improvements: +12.7% on SNLI-hard, +9.1% on FEVER-Symmetric, +6.8% on QQP-adversarial, and "
                "+4.5% on BoolQ-contrast. The average OOD improvement is 8.3 percentage points.",
                "Analysis reveals that 23% of GPT-4's correct predictions on SNLI rely on spurious features, "
                "compared to 35% for LLaMA-3 70B and 41% for Mistral-7B. After mitigation, these rates drop to "
                "8%, 14%, and 17% respectively."
            ]),
            ("6. Case Studies", [
                "We present detailed case studies illustrating the types of spurious correlations identified and "
                "mitigated by CausalLM. In NLI, we find that models heavily rely on lexical overlap (67% of "
                "spurious predictions), negation words (21%), and sentence length differences (12%). After CDA "
                "and CR, the model correctly handles contradictions that do not contain negation words and "
                "entailments with high lexical overlap.",
                "In fact verification (FEVER), models exploit claim-evidence lexical similarity and named entity "
                "presence. CausalLM successfully trains models to focus on semantic consistency rather than surface "
                "overlap, improving accuracy on adversarially constructed claims by 15.2%."
            ]),
            ("7. Limitations and Future Work", [
                "Our framework assumes that causal and spurious features can be clearly separated, which may not "
                "always hold in practice. The counterfactual generation process relies on GPT-4, introducing "
                "potential biases. Future work will explore automated causal discovery methods that do not require "
                "manual specification of the causal graph.",
                "We also plan to extend CausalLM to generation tasks (summarization, translation) where the "
                "notion of spurious correlation is less well-defined, and to multimodal models where visual and "
                "textual features may interact in complex causal structures."
            ]),
            ("8. Conclusion", [
                "CausalLM provides a principled framework for understanding and mitigating spurious correlations "
                "in large language models. By formalizing the prediction process as a structural causal model and "
                "applying intervention-based analysis, we identify significant spurious dependencies across multiple "
                "LLMs and benchmarks. Our counterfactual augmentation and causal regularization strategies "
                "effectively reduce these dependencies while improving out-of-distribution robustness."
            ]),
        ],
        "pages": 10,
    },
]


def create_proceedings():
    """Create a 40-page proceedings bundle PDF with 5 academic papers."""
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    page_number = 0
    for paper_idx, paper in enumerate(PAPERS):
        target_pages = paper["pages"]
        pages_created = 0

        # --- Title Page (first page of each paper) ---
        page = doc.new_page(width=595, height=842)
        page_number += 1
        pages_created += 1
        y = 120

        # Conference header
        page.insert_text(
            pymupdf.Point(297.5, 50),
            "Proceedings of the 2025 International Conference on",
            fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3),
        )
        page.insert_text(
            pymupdf.Point(297.5, 64),
            "Artificial Intelligence and Machine Learning (ICAIML 2025)",
            fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3),
        )

        # Draw separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 78), pymupdf.Point(523, 78))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()

        # Title
        title_rect = pymupdf.Rect(72, y, 523, y + 80)
        page.insert_textbox(
            title_rect, paper["title"],
            fontsize=16, fontname="tibo", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        y += 85

        # Authors
        page.insert_textbox(
            pymupdf.Rect(72, y, 523, y + 25),
            paper["authors"],
            fontsize=11, fontname="tiit", color=(0.2, 0.2, 0.2),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        y += 28

        # Affiliation
        page.insert_textbox(
            pymupdf.Rect(72, y, 523, y + 25),
            paper["affiliation"],
            fontsize=9, fontname="tiro", color=(0.4, 0.4, 0.4),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        y += 45

        # Abstract
        page.insert_text(pymupdf.Point(72, y), "Abstract", fontsize=11, fontname="tibo", color=(0, 0, 0))
        y += 18
        abstract_rect = pymupdf.Rect(90, y, 505, y + 160)
        page.insert_textbox(
            abstract_rect, paper["abstract"],
            fontsize=9, fontname="tiit", color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        y += 170

        # Start body sections on title page if space
        section_idx = 0
        para_idx = 0

        while y < 770 and section_idx < len(paper["sections"]):
            sec_title, paragraphs = paper["sections"][section_idx]
            if para_idx == 0:
                # Section heading
                page.insert_text(
                    pymupdf.Point(72, y),
                    sec_title, fontsize=11, fontname="tibo", color=(0, 0, 0),
                )
                y += 18

            while para_idx < len(paragraphs) and y < 740:
                para = paragraphs[para_idx]
                para_rect = pymupdf.Rect(72, y, 523, y + 200)
                excess = page.insert_textbox(
                    para_rect, para,
                    fontsize=9.5, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                # Estimate lines used (rough)
                lines_used = len(para) / 75  # ~75 chars per line at 9.5pt in this rect
                height_used = lines_used * 12 + 8
                y += max(height_used, 30)
                para_idx += 1
                if y >= 740:
                    break

            if para_idx >= len(paragraphs):
                section_idx += 1
                para_idx = 0
            else:
                break

        # Page footer
        page.insert_text(
            pymupdf.Point(280, 820),
            str(page_number), fontsize=8, fontname="tiro", color=(0.5, 0.5, 0.5),
        )

        # --- Remaining pages for this paper ---
        while pages_created < target_pages:
            page = doc.new_page(width=595, height=842)
            page_number += 1
            pages_created += 1
            y = 60

            # Conference header (smaller, on continuation pages)
            page.insert_text(
                pymupdf.Point(72, 35),
                "ICAIML 2025 Proceedings",
                fontsize=7, fontname="tiit", color=(0.5, 0.5, 0.5),
            )
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 42), pymupdf.Point(523, 42))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.3)
            shape.commit()

            # Continue sections
            while y < 770 and section_idx < len(paper["sections"]):
                sec_title, paragraphs = paper["sections"][section_idx]
                if para_idx == 0:
                    page.insert_text(
                        pymupdf.Point(72, y),
                        sec_title, fontsize=11, fontname="tibo", color=(0, 0, 0),
                    )
                    y += 18

                while para_idx < len(paragraphs) and y < 740:
                    para = paragraphs[para_idx]
                    para_rect = pymupdf.Rect(72, y, 523, y + 200)
                    page.insert_textbox(
                        para_rect, para,
                        fontsize=9.5, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    lines_used = len(para) / 75
                    height_used = lines_used * 12 + 8
                    y += max(height_used, 30)
                    para_idx += 1
                    if y >= 740:
                        break

                if para_idx >= len(paragraphs):
                    section_idx += 1
                    para_idx = 0
                else:
                    break

            # If we run out of sections but need more pages, add filler (references)
            if section_idx >= len(paper["sections"]) and pages_created < target_pages and y < 700:
                page.insert_text(
                    pymupdf.Point(72, y),
                    "References", fontsize=11, fontname="tibo", color=(0, 0, 0),
                )
                y += 18
                refs = [
                    "[1] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is all you need. NeurIPS.",
                    "[2] Devlin, J., Chang, M., Lee, K., Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers. NAACL.",
                    "[3] Brown, T., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. NeurIPS.",
                    "[4] He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep residual learning for image recognition. CVPR.",
                    "[5] Goodfellow, I., Pouget-Abadie, J., Mirza, M., et al. (2014). Generative adversarial nets. NeurIPS.",
                    "[6] Kingma, D., Ba, J. (2015). Adam: A method for stochastic optimization. ICLR.",
                    "[7] Hochreiter, S., Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8).",
                    "[8] Krizhevsky, A., Sutskever, I., Hinton, G. (2012). ImageNet classification with deep CNNs. NeurIPS.",
                    "[9] Silver, D., Huang, A., Maddison, C., et al. (2016). Mastering the game of Go with DNNs. Nature.",
                    "[10] Sutton, R. and Barto, A. (2018). Reinforcement Learning: An Introduction. MIT Press.",
                    "[11] LeCun, Y., Bengio, Y., Hinton, G. (2015). Deep learning. Nature, 521(7553).",
                    "[12] Radford, A., Wu, J., Child, R., et al. (2019). Language models are unsupervised multitask learners.",
                    "[13] Liu, Y., Ott, M., Goyal, N., et al. (2019). RoBERTa: A robustly optimized BERT approach.",
                    "[14] Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al. (2021). An image is worth 16x16 words. ICLR.",
                    "[15] Chen, T., Kornblith, S., Norouzi, M., Hinton, G. (2020). SimCLR: Simple contrastive learning. ICML.",
                    "[16] Raffel, C., Shazeer, N., Roberts, A., et al. (2020). Exploring the limits of transfer learning. JMLR.",
                    "[17] Touvron, H., Lavril, T., Izacard, G., et al. (2023). LLaMA: Open and efficient foundation models.",
                    "[18] Achiam, J., Adler, S., Agarwal, S., et al. (2023). GPT-4 technical report. arXiv preprint.",
                ]
                for ref in refs:
                    if y >= 750:
                        break
                    ref_rect = pymupdf.Rect(72, y, 523, y + 30)
                    page.insert_textbox(
                        ref_rect, ref,
                        fontsize=8, fontname="tiro", color=(0.2, 0.2, 0.2),
                        align=pymupdf.TEXT_ALIGN_LEFT,
                    )
                    y += 14

            # Page footer
            page.insert_text(
                pymupdf.Point(280, 820),
                str(page_number), fontsize=8, fontname="tiro", color=(0.5, 0.5, 0.5),
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_number}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_proceedings()
