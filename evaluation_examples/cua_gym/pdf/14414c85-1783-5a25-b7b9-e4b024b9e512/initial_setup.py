"""
Initial Setup: Create a 50-page thesis PDF with page numbering errors
Task ID: pdf_res_093
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_093'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/final_submission.pdf'

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


# ---- Thesis content data ----

CHAPTER_TITLES = {
    1: "Introduction",
    2: "Literature Review",
    3: "Methodology",
    4: "Data Collection and Analysis",
    5: "Results",
    6: "Discussion",
    7: "Conclusions and Future Work",
}

# Map page number (1-indexed) to content
# Pages: 1=title, 2=abstract, 3=ToC, 4-10=Ch1, 11-18=Ch2, 19-26=Ch3,
# 27-33=Ch4, 34-40=Ch5, 41-45=Ch6, 46-48=Ch7, 49-50=References

PAGE_CONTENT = {}
PAGE_CONTENT[1] = ("title", "Adaptive Machine Learning Approaches\nfor Urban Traffic Flow Optimization\n\n\nA Thesis Submitted in Partial Fulfillment\nof the Requirements for the Degree of\nDoctor of Philosophy\n\n\nDepartment of Computer Science\nStanford University\n\n\nElena Vasquez\nJune 2025")
PAGE_CONTENT[2] = ("abstract", "Abstract\n\nUrban traffic congestion remains one of the most pressing challenges facing modern cities worldwide. This thesis presents a novel adaptive machine learning framework for real-time traffic flow optimization that integrates reinforcement learning with graph neural networks. Our approach models urban road networks as dynamic graphs where intersections serve as nodes and road segments as edges, with traffic flow represented as time-varying edge weights.\n\nWe introduce TrafficAdapt, a multi-agent reinforcement learning system that coordinates traffic signal timing across interconnected intersections. Unlike prior approaches that optimize individual intersections independently, our method captures spatial-temporal dependencies through a message-passing mechanism that enables neighboring agents to share learned representations.\n\nExperimental evaluation on three real-world urban networks (San Francisco, Singapore, and Munich) demonstrates that TrafficAdapt reduces average vehicle delay by 23.7% compared to state-of-the-art adaptive signal control methods, while maintaining robust performance under varying demand patterns and incident conditions.")
PAGE_CONTENT[3] = ("toc", "Table of Contents\n\n1. Introduction ............................................. 4\n   1.1 Background and Motivation ........................... 5\n   1.2 Problem Statement ................................... 6\n   1.3 Research Objectives ................................. 7\n   1.4 Thesis Organization ................................. 8\n\n2. Literature Review ....................................... 11\n   2.1 Traditional Traffic Signal Control .................. 12\n   2.2 Machine Learning in Traffic Management .............. 14\n   2.3 Multi-Agent Reinforcement Learning .................. 16\n\n3. Methodology ............................................. 19\n   3.1 System Architecture ................................. 20\n   3.2 Graph Neural Network Model .......................... 22\n   3.3 Reward Function Design .............................. 24\n\n4. Data Collection and Analysis ............................ 27\n5. Results ................................................. 34\n6. Discussion .............................................. 41\n7. Conclusions and Future Work ............................. 46\nReferences ................................................. 49")

# Chapter 1: Introduction (pages 4-10)
ch1_texts = [
    "1. Introduction\n\nUrban traffic congestion is estimated to cost the United States economy over $87 billion annually in lost productivity, wasted fuel, and increased emissions. As urban populations continue to grow, with projections indicating that 68% of the world's population will reside in urban areas by 2050, the need for intelligent traffic management systems becomes increasingly critical.\n\nTraditional traffic signal control systems, such as SCOOT and SCATS, rely on predefined signal timing plans that are periodically updated based on historical traffic patterns. While these systems have demonstrated improvements over fixed-time controllers, they struggle to adapt to real-time fluctuations in traffic demand, particularly during non-recurring congestion events such as accidents, special events, or severe weather conditions.",
    "1.1 Background and Motivation\n\nThe rapid advancement of sensor technologies, including inductive loop detectors, video cameras, and connected vehicle data, has created unprecedented opportunities for real-time traffic state estimation. Modern intersections can be equipped with multiple sensing modalities that provide detailed information about vehicle counts, speeds, queue lengths, and turning movements.\n\nSimultaneously, breakthroughs in deep reinforcement learning have demonstrated the potential for autonomous decision-making in complex, dynamic environments. The success of deep RL in game playing, robotics, and resource allocation suggests that similar approaches could revolutionize traffic signal control by learning optimal policies directly from observed traffic states.",
    "1.2 Problem Statement\n\nDespite significant progress in both traffic sensing and machine learning, several fundamental challenges remain in developing practical adaptive traffic signal control systems:\n\n1. Scalability: Urban networks contain hundreds or thousands of signalized intersections that must be coordinated efficiently.\n\n2. Non-stationarity: Traffic patterns exhibit complex temporal dynamics including daily cycles, weekly variations, and seasonal trends.\n\n3. Partial Observability: Individual intersection controllers typically have access to local sensor data only, requiring mechanisms for information sharing.\n\n4. Safety Constraints: Signal control policies must satisfy hard constraints on minimum green times, clearance intervals, and pedestrian phases.",
    "1.3 Research Objectives\n\nThis thesis addresses the following research objectives:\n\nObjective 1: Develop a graph neural network architecture that effectively captures the spatial-temporal dependencies in urban traffic networks, enabling information propagation between neighboring intersections.\n\nObjective 2: Design a multi-agent reinforcement learning framework where individual intersection agents can learn coordinated signal timing policies through shared representations and cooperative reward structures.\n\nObjective 3: Incorporate safety constraints and operational requirements into the learning process through constrained optimization techniques that guarantee feasible signal timing plans.\n\nObjective 4: Evaluate the proposed system on real-world traffic networks of varying scales and complexity to demonstrate practical applicability.",
    "1.4 Thesis Organization\n\nThe remainder of this thesis is organized as follows:\n\nChapter 2 provides a comprehensive review of related work in traffic signal control, including traditional methods, machine learning approaches, and multi-agent systems.\n\nChapter 3 presents the methodology, including the system architecture, graph neural network model, and reinforcement learning framework.\n\nChapter 4 describes the data collection process and preliminary analysis of the three study networks.\n\nChapter 5 presents the experimental results, including comparisons with baseline methods and ablation studies.\n\nChapter 6 discusses the findings, limitations, and practical implications.\n\nChapter 7 concludes the thesis and outlines directions for future research.",
    "1.4.1 Notation and Conventions\n\nThroughout this thesis, we adopt the following notation conventions. Bold uppercase letters (e.g., X, W) denote matrices, bold lowercase letters (e.g., x, h) denote vectors, and regular lowercase letters (e.g., n, t) denote scalars. Sets are denoted by calligraphic letters (e.g., V, E). The traffic network is represented as a directed graph G = (V, E), where V is the set of intersections and E is the set of road segments connecting them.\n\nTime is discretized into intervals of duration delta_t, typically set to 5 seconds in our experiments. The traffic state at intersection i and time step t is denoted s_i^t, and the signal control action is denoted a_i^t. The joint state of all intersections is S^t = {s_1^t, s_2^t, ..., s_N^t}.",
    "1.5 Summary of Contributions\n\nThe primary contributions of this thesis are:\n\n1. TrafficAdapt Framework: A novel multi-agent reinforcement learning system that leverages graph neural networks for coordinated traffic signal control across urban networks.\n\n2. Spatial-Temporal Message Passing: A communication protocol that enables efficient information sharing between neighboring intersection agents while maintaining computational scalability.\n\n3. Constrained Policy Optimization: A method for incorporating safety constraints directly into the policy gradient optimization, ensuring that learned policies satisfy operational requirements.\n\n4. Comprehensive Evaluation: Extensive experiments on three real-world networks demonstrating significant improvements over existing adaptive control methods.\n\n5. Open-Source Implementation: A publicly available codebase and simulation environment to facilitate reproducibility and future research.",
]

# Chapter 2: Literature Review (pages 11-18)
ch2_texts = [
    "2. Literature Review\n\nThis chapter provides a comprehensive overview of the existing literature on traffic signal control, organized into three main categories: traditional control methods, machine learning approaches, and multi-agent reinforcement learning systems. We identify the key limitations of existing approaches that motivate the development of TrafficAdapt.",
    "2.1 Traditional Traffic Signal Control\n\nFixed-time signal control plans are the most widely deployed approach, where signal timing parameters are optimized offline using historical traffic data. Webster's formula, proposed in 1958, provides a simple method for calculating optimal cycle length and green splits based on traffic volumes and saturation flows. The TRANSYT optimization tool extends this approach by considering network-level coordination through offset optimization.\n\nActuated control systems represent an intermediate level of adaptivity, using loop detectors to extend green phases for approaching vehicles within predefined limits. Semi-actuated control provides preferential treatment to major approaches while maintaining fixed timing for minor movements.",
    "2.2 Adaptive Traffic Signal Control\n\nSCOOT (Split Cycle Offset Optimization Technique), developed by TRL in the United Kingdom, is one of the most widely deployed adaptive systems globally. SCOOT uses upstream detectors to estimate cyclic flow profiles and makes small, incremental adjustments to splits, offsets, and cycle times. The system operates on a centralized architecture where a single computer optimizes signal parameters for an entire network.\n\nSCATS (Sydney Coordinated Adaptive Traffic System) takes a distributed approach, where local controllers at each intersection make timing adjustments based on degree of saturation measurements. Regional coordination is achieved through a hierarchical structure where area computers synchronize timing plans across groups of intersections.",
    "2.3 Machine Learning in Traffic Management\n\nThe application of machine learning to traffic management has a rich history dating back to the early 1990s. Porche and Lafortune (1999) demonstrated the potential of neural networks for traffic signal control, training a multilayer perceptron to approximate optimal timing plans. However, these early approaches were limited by the available computational resources and training data.\n\nThe emergence of deep learning has renewed interest in data-driven traffic control. Li et al. (2016) proposed IntelliLight, one of the first deep reinforcement learning systems for traffic signal control, using a deep Q-network to learn phase selection policies from raw intersection observations.",
    "2.4 Deep Reinforcement Learning for Traffic Signals\n\nRecent years have witnessed an explosion of research applying deep RL to traffic signal control. Wei et al. (2018) introduced PressLight, which uses the concept of intersection pressure (the difference between upstream and downstream vehicle counts) as a reward signal. Zheng et al. (2019) proposed FRAP, which uses phase competition information to design efficient network architectures.\n\nCoLight (Wei et al., 2019) represents one of the first attempts to incorporate graph attention networks for multi-intersection coordination. The model uses attention mechanisms to weigh the influence of neighboring intersections when making local signal timing decisions.",
    "2.5 Multi-Agent Reinforcement Learning\n\nMulti-agent reinforcement learning (MARL) provides a natural framework for distributed traffic signal control, where each intersection is modeled as an independent agent that must coordinate with others to optimize network-level performance. The key challenge in MARL is the non-stationarity introduced by simultaneous learning: each agent's environment changes as other agents update their policies.\n\nIndependent Q-learning (IQL), where each agent learns its own Q-function independently, serves as a simple baseline but ignores inter-agent dependencies. QMIX (Rashid et al., 2018) addresses this by decomposing the joint action-value function into individual utilities while enforcing monotonicity constraints.",
    "2.6 Graph Neural Networks in Transportation\n\nGraph neural networks (GNNs) have emerged as a powerful tool for modeling spatial relationships in transportation networks. Unlike grid-based approaches that treat spatial data as images, GNNs can directly operate on the irregular topology of road networks.\n\nSpatio-temporal graph convolutional networks (ST-GCN) have been widely adopted for traffic prediction tasks. Li et al. (2018) proposed DCRNN, which combines diffusion convolutions with gated recurrent units to capture spatial and temporal dependencies simultaneously.",
    "2.7 Summary and Research Gaps\n\nDespite the significant progress reviewed above, several critical research gaps remain:\n\n1. Most existing RL-based approaches treat each intersection as having a fixed neighborhood structure, ignoring the dynamic nature of traffic influence propagation.\n\n2. Safety constraints are typically handled through post-hoc clipping or penalty terms rather than being formally incorporated into the optimization process.\n\n3. Scalability to large networks (>100 intersections) remains challenging due to the exponential growth of the joint state-action space.\n\n4. Transfer learning between different networks and adaptation to changing demand patterns has received limited attention.\n\nThese gaps motivate the development of TrafficAdapt, which addresses each of these limitations through its graph-based architecture, constrained optimization framework, and scalable message-passing mechanism.",
]

# Chapters 3-7 and references in shorter form for the remaining pages
ch3_texts = [
    "3. Methodology\n\nThis chapter presents the technical details of the TrafficAdapt framework. We begin with an overview of the system architecture, followed by detailed descriptions of the graph neural network model, the reinforcement learning formulation, and the constrained optimization approach.",
    "3.1 System Architecture\n\nTrafficAdapt consists of three main components: (1) a traffic state encoder that processes raw sensor data into compact intersection representations, (2) a graph neural network that propagates information between neighboring intersections through learned message functions, and (3) a policy network that maps the enriched intersection representations to signal timing actions.\n\nThe architecture follows a decentralized execution with centralized training paradigm, where agents share parameters and training data but execute independently during deployment.",
    "3.2 Traffic State Representation\n\nAt each time step t, the local state of intersection i is represented as a vector s_i^t that encodes the current traffic conditions observed by local sensors. The state vector includes: (1) queue lengths for each incoming lane, (2) average speeds on approaching links, (3) current signal phase and elapsed time, (4) time-of-day and day-of-week features, and (5) historical demand statistics.\n\nThe state encoder f_enc is implemented as a two-layer MLP with ReLU activations: h_i^0 = f_enc(s_i^t) = ReLU(W_2 * ReLU(W_1 * s_i^t + b_1) + b_2).",
    "3.3 Graph Neural Network Model\n\nThe graph neural network performs K rounds of message passing to propagate information across the network. At each round k, intersection i aggregates messages from its neighbors N(i) and updates its representation:\n\nm_i^k = AGG({MSG(h_i^{k-1}, h_j^{k-1}, e_{ij}) : j in N(i)})\nh_i^k = UPD(h_i^{k-1}, m_i^k)\n\nwhere MSG is the message function, AGG is the aggregation function, and UPD is the update function.",
    "3.4 Reinforcement Learning Formulation\n\nWe formulate the traffic signal control problem as a decentralized partially observable Markov decision process (Dec-POMDP). Each intersection agent i selects actions from a discrete action space A_i consisting of feasible signal phase combinations.\n\nThe reward function is designed to minimize a weighted combination of vehicle delay, queue spillback, and throughput: r_i^t = -alpha * delay_i^t - beta * spillback_i^t + gamma * throughput_i^t.",
    "3.5 Constrained Policy Optimization\n\nTo ensure safety during both training and deployment, we incorporate signal timing constraints into the policy optimization process using a Lagrangian relaxation approach. The constrained optimization problem is:\n\nmax_theta J(theta) subject to: g_min <= g_k(theta) <= g_max for all phases k\n\nwhere g_k(theta) represents the expected green time for phase k under policy theta.",
    "3.6 Training Procedure\n\nTraining proceeds in three phases: (1) pre-training on historical data using imitation learning from an expert SCOOT-like controller, (2) fine-tuning with reinforcement learning using PPO with the constrained objective, and (3) multi-scenario adaptation where the policy is exposed to diverse demand patterns and incident scenarios.\n\nWe use a replay buffer of 100,000 transitions and update the policy every 256 time steps using mini-batches of size 64.",
    "3.7 Implementation Details\n\nThe GNN uses K=3 message-passing rounds with hidden dimension d=128. The policy network consists of a two-layer MLP with 256 and 128 hidden units. We use the Adam optimizer with an initial learning rate of 3e-4 and a cosine annealing schedule over 500,000 training steps.\n\nAll experiments are conducted using the SUMO (Simulation of Urban Mobility) traffic simulator with a 5-second control interval. The simulation is coupled with our PyTorch-based agent through a custom API that handles state extraction and action application.",
]

ch4_texts = [
    "4. Data Collection and Analysis\n\nThis chapter describes the three real-world urban traffic networks used for evaluation, the data collection process, and preliminary analyses that informed our experimental design.",
    "4.1 San Francisco Network\n\nThe San Francisco study area covers a 4.2 km^2 region in the SoMa district, encompassing 42 signalized intersections. Traffic data was collected from the San Francisco Municipal Transportation Agency (SFMTA) over a 12-month period from January to December 2023.\n\nThe dataset includes: (1) 15-minute aggregated loop detector counts for 168 detection stations, (2) signal timing plans and phase configurations for all 42 intersections, (3) Waze incident reports for the study period, and (4) transit vehicle GPS traces from the Muni system.",
    "4.2 Singapore Network\n\nThe Singapore study area covers the Jurong East commercial district with 67 signalized intersections. Data was provided by the Land Transport Authority (LTA) of Singapore through a research collaboration agreement.\n\nThe Singapore network presents unique challenges including high pedestrian volumes, bus priority signals, and the presence of grade-separated intersections. Peak-hour demand reaches approximately 4,200 vehicles per hour entering the network.",
    "4.3 Munich Network\n\nThe Munich study area covers the Mittlerer Ring, a major arterial ring road encircling the city center, with 38 signalized intersections. Data was obtained from the Bayerisches Staatsministerium fuer Wohnen, Bau und Verkehr.\n\nThe Munich network features tram priority signals, complex phase designs with up to 8 phases per intersection, and significant seasonal demand variation due to Oktoberfest and other major events.",
    "4.4 Data Preprocessing\n\nRaw detector data was cleaned using a three-stage pipeline: (1) outlier detection using the modified Z-score method with a threshold of 3.5, (2) imputation of missing values using a matrix factorization approach that preserves spatial-temporal patterns, and (3) normalization to hourly equivalent flow rates.\n\nSignal timing data was standardized to a common format compatible with the SUMO simulator. Phase mappings were manually verified against field observations for a random sample of 20% of intersections.",
    "4.5 Demand Pattern Analysis\n\nClustering analysis using dynamic time warping (DTW) distance revealed four distinct demand pattern types across the three networks: (1) typical weekday with morning and evening peaks, (2) weekend/holiday with a single midday peak, (3) event-influenced with elevated sustained demand, and (4) incident-disrupted with sudden demand shifts.\n\nTable 4.1 shows the distribution of pattern types across networks and seasons.",
    "4.6 Network Topology Analysis\n\nWe analyzed the topological properties of each network to understand their structural differences. The San Francisco network has an average node degree of 3.4 with a grid-like structure. The Singapore network is more irregular with an average degree of 3.1 and several critical bottleneck intersections. The Munich ring has a predominantly linear topology with an average degree of 2.6.\n\nThese structural differences have important implications for message-passing efficiency and the optimal number of GNN layers.",
]

ch5_texts = [
    "5. Results\n\nThis chapter presents the experimental results comparing TrafficAdapt against baseline methods across the three study networks. We evaluate performance using multiple metrics and conduct ablation studies to understand the contribution of each system component.",
    "5.1 Baseline Methods\n\nWe compare TrafficAdapt against five baseline methods: (1) Fixed-time control optimized using Webster's formula, (2) SCOOT adaptive control, (3) Independent DQN (each intersection trained independently), (4) MA2C (multi-agent actor-critic with mean-field approximation), and (5) CoLight (graph attention network-based coordination).",
    "5.2 Performance on San Francisco Network\n\nTable 5.1 summarizes the results for the San Francisco network across four demand scenarios. TrafficAdapt achieves the lowest average delay in all scenarios, with improvements of 23.7% over Fixed-time, 15.2% over SCOOT, 11.8% over Independent DQN, 8.3% over MA2C, and 5.1% over CoLight.\n\nNotably, TrafficAdapt demonstrates the most significant advantages during incident scenarios, where its ability to propagate disruption information through the GNN enables proactive rerouting of green time to alternative paths.",
    "5.3 Performance on Singapore Network\n\nThe Singapore network results show consistent improvements, with TrafficAdapt reducing average delay by 21.4% compared to SCOOT. The larger network size (67 vs 42 intersections) amplifies the benefits of coordinated control, as myopic approaches struggle with spillback propagation across the denser network.\n\nPedestrian delay, measured at 15 high-pedestrian-volume intersections, improved by 12.3% compared to SCOOT, confirming that the constrained optimization framework successfully balances vehicle and pedestrian objectives.",
    "5.4 Performance on Munich Network\n\nThe Munich ring network presents a different challenge due to its linear topology. TrafficAdapt achieves a 19.8% reduction in average delay compared to SCOOT. The tram priority constraints are successfully maintained, with tram delay increasing by only 1.2% compared to the dedicated tram-priority controller.\n\nThe arterial progression quality, measured using the bandwidth metric, improves by 18.5% compared to SCOOT, indicating effective offset coordination along the ring.",
    "5.5 Ablation Studies\n\nTo understand the contribution of each component, we conduct ablation experiments on the San Francisco network:\n\n1. Without GNN (local features only): Average delay increases by 14.2%, confirming the importance of spatial information propagation.\n2. Without constrained optimization: Minimum green time violations increase by 340%, and pedestrian delay increases by 28.7%.\n3. With K=1 GNN layers (vs K=3): Average delay increases by 6.8%, suggesting that multi-hop information is valuable.\n4. Without pre-training: Training requires 3.2x more samples to converge to similar performance.",
    "5.6 Scalability Analysis\n\nWe evaluate scalability by progressively increasing the network size from 10 to 200 intersections using synthetic grid networks. Training time scales approximately linearly with network size due to the localized nature of message passing. Inference time remains below 50ms per control interval for networks up to 200 intersections on a single GPU.",
]

ch6_texts = [
    "6. Discussion\n\nThis chapter discusses the implications of our experimental results, addresses limitations of the current approach, and contextualizes our findings within the broader landscape of intelligent transportation systems.",
    "6.1 Practical Implications\n\nThe consistent performance improvements demonstrated across three diverse real-world networks suggest that TrafficAdapt is ready for pilot deployment. The decentralized execution architecture enables incremental deployment, where TrafficAdapt controllers can be installed at individual intersections while maintaining compatibility with existing fixed-time or actuated controllers at neighboring locations.\n\nThe estimated annual cost savings for the San Francisco network are approximately $2.3 million in reduced vehicle operating costs and $890,000 in reduced emissions.",
    "6.2 Limitations\n\nSeveral limitations should be noted. First, our evaluation relies on simulation rather than real-world deployment, and the sim-to-real gap may affect performance. Second, the GNN architecture assumes a static network topology and does not handle dynamic changes such as lane closures or construction zones. Third, the current framework does not incorporate vehicle-to-infrastructure communication, which could provide richer state information.\n\nAdditionally, the training process requires access to a calibrated traffic simulation model, which involves significant engineering effort for each new deployment site.",
    "6.3 Comparison with Concurrent Work\n\nDuring the preparation of this thesis, several related works have been published that partially address similar challenges. GeneraLight (Zhang et al., 2024) proposes a transfer learning framework, while AttendLight (Oroojlooy et al., 2024) uses attention mechanisms for phase selection. We note that these approaches are complementary to our contribution and could potentially be integrated into the TrafficAdapt framework.",
    "6.4 Ethical Considerations\n\nThe deployment of AI-based traffic control raises important ethical considerations. Algorithmic fairness requires that signal timing policies do not systematically disadvantage certain communities or transportation modes. Our constrained optimization framework provides a mechanism for encoding equity objectives, but further research is needed to develop appropriate fairness metrics for traffic signal control.\n\nPrivacy concerns related to traffic data collection and the potential for surveillance misuse must also be carefully addressed through appropriate data governance frameworks.",
]

ch7_texts = [
    "7. Conclusions and Future Work\n\nThis thesis presented TrafficAdapt, a multi-agent reinforcement learning framework for adaptive traffic signal control that leverages graph neural networks for inter-intersection coordination. Through extensive evaluation on three real-world urban networks, we demonstrated significant improvements over existing methods in terms of average delay, throughput, and safety constraint satisfaction.",
    "7.1 Key Findings\n\nThe key findings of this thesis are:\n\n1. Graph neural networks effectively capture spatial-temporal dependencies in traffic networks, enabling information propagation that improves coordination quality.\n\n2. Constrained policy optimization can successfully enforce safety requirements while maintaining near-optimal performance.\n\n3. Pre-training with imitation learning significantly accelerates convergence and improves final performance.\n\n4. The decentralized execution architecture enables scalable deployment without sacrificing coordination quality.",
    "7.2 Future Directions\n\nSeveral promising directions for future research include:\n\n1. Integration of connected vehicle data for enhanced state estimation.\n2. Extension to mixed autonomy scenarios where both human-driven and autonomous vehicles share the road.\n3. Development of online adaptation mechanisms that continuously update policies based on real-world feedback.\n4. Multi-modal optimization that jointly considers vehicle, pedestrian, cyclist, and transit objectives.\n5. Federated learning approaches that enable policy sharing between cities while preserving data privacy.",
]

ref_texts = [
    "References\n\n[1] Abdulhai, B., Pringle, R., and Karakoulas, G. J. (2003). Reinforcement learning for true adaptive traffic signal control. Journal of Transportation Engineering, 129(3):278-285.\n\n[2] Arel, I., Liu, C., Urbanik, T., and Kohls, A. G. (2010). Reinforcement learning-based multi-agent system for network traffic signal control. IET Intelligent Transport Systems, 4(2):128-135.\n\n[3] Chu, T., Wang, J., Codeca, L., and Li, Z. (2019). Multi-agent deep reinforcement learning for large-scale traffic signal control. IEEE Transactions on Intelligent Transportation Systems, 21(3):1086-1095.\n\n[4] El-Tantawy, S., Abdulhai, B., and Abdelgawad, H. (2013). Multiagent reinforcement learning for integrated network of adaptive traffic signal controllers. IEEE Transactions on Intelligent Transportation Systems, 14(3):1140-1150.\n\n[5] Gao, J., Shen, Y., Liu, J., Ito, M., and Shiratori, N. (2017). Adaptive traffic signal control: Deep reinforcement learning algorithm with experience replay and target network. ArXiv preprint.",
    "[6] Hunt, P. B., Robertson, D. I., Bretherton, R. D., and Royle, M. C. (1982). The SCOOT on-line traffic signal optimisation technique. Traffic Engineering and Control, 23(4):190-192.\n\n[7] Kipf, T. N. and Welling, M. (2017). Semi-supervised classification with graph convolutional networks. In International Conference on Learning Representations.\n\n[8] Li, Y., Yu, R., Shahabi, C., and Liu, Y. (2018). Diffusion convolutional recurrent neural network: Data-driven traffic forecasting. In International Conference on Learning Representations.\n\n[9] Liang, X., Du, X., Wang, G., and Han, Z. (2019). A deep reinforcement learning network for traffic light cycle control. IEEE Transactions on Vehicular Technology, 68(2):1243-1253.\n\n[10] Lowrie, P. R. (1990). SCATS, Sydney co-ordinated adaptive traffic system: A traffic responsive method of controlling urban traffic. Roads and Traffic Authority NSW.\n\n[11] Nishi, T., Otaki, K., Hayakawa, K., and Yoshimura, T. (2018). Traffic signal control based on reinforcement learning with graph convolutional neural nets. In ITSC.\n\n[12] Oroojlooy, A., Nazari, M., Hajinezhad, D., and Silva, J. (2024). AttendLight: Universal attention-based reinforcement learning model for traffic signal control. In NeurIPS.\n\n[13] Rashid, T., Samvelyan, M., De Witt, C. S., Farquhar, G., Foerster, J., and Whitaker, S. (2018). QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning. In ICML.\n\n[14] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is all you need. In NeurIPS.\n\n[15] Webster, F. V. (1958). Traffic signal settings. Road Research Technical Paper No. 39. HMSO, London.\n\n[16] Wei, H., Chen, C., Zheng, G., et al. (2019). CoLight: Learning network-level cooperation for traffic signal control. In CIKM.\n\n[17] Wei, H., Zheng, G., Yao, H., and Li, Z. (2018). IntelliLight: A reinforcement learning approach for intelligent traffic light control. In KDD.\n\n[18] Zhang, L., Wu, Q., and Shen, J. (2024). GeneraLight: Generalizable traffic signal control via meta reinforcement learning. In AAAI.",
]

# Combine chapter texts
all_chapters = {
    (4, 10): ch1_texts,   # pages 4-10
    (11, 18): ch2_texts,  # pages 11-18
    (19, 26): ch3_texts,  # pages 19-26 (8 pages)
    (27, 33): ch4_texts,  # pages 27-33 (7 pages)
    (34, 40): ch5_texts,  # pages 34-40 (7 pages)
    (41, 45): ch6_texts,  # pages 41-45 (5 pages)
    (46, 48): ch7_texts,  # pages 46-48 (3 pages)
    (49, 50): ref_texts,  # pages 49-50 (2 pages)
}


# Define which pages have numbering errors
# Errors: page 7 shows "9" (wrong number), page 23 has no number (missing),
# page 31 shows "30" (duplicate of previous), page 38 shows "40" (wrong),
# page 45 has no number (missing), page 50 shows "49" (wrong, duplicate)
PAGE_NUMBER_ERRORS = {
    7: "9",       # wrong number
    23: None,     # missing
    31: "30",     # duplicate/wrong
    38: "40",     # wrong
    45: None,     # missing
    50: "49",     # wrong/duplicate
}


def get_displayed_page_number(page_idx):
    """Return the displayed page number string for a 1-indexed page.
    Title page (1) has no number. Others have their number unless overridden."""
    page_num = page_idx  # 1-indexed
    if page_num == 1:
        return None  # title page has no number
    if page_num in PAGE_NUMBER_ERRORS:
        return PAGE_NUMBER_ERRORS[page_num]
    return str(page_num)


def get_page_text(page_num):
    """Get body text for a given 1-indexed page number."""
    if page_num in PAGE_CONTENT:
        return PAGE_CONTENT[page_num][1]

    for (start, end), texts in all_chapters.items():
        if start <= page_num <= end:
            idx = page_num - start
            if idx < len(texts):
                return texts[idx]
            # If we run out of chapter text, generate filler continuation
            return f"[Continuation of analysis, page {page_num}]\n\nThe experimental results presented in this section further corroborate the findings discussed in the preceding pages. Statistical significance tests (paired t-test, p < 0.05) confirm that the observed improvements are not attributable to random variation in simulation outcomes."

    return f"[Content for page {page_num}]"


def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, 51):
        page = doc.new_page(width=595, height=842)  # A4

        body_text = get_page_text(page_num)

        if page_num == 1:
            # Title page - centered, larger font, no page number
            lines = body_text.split('\n')
            y = 180
            for line in lines:
                line = line.strip()
                if not line:
                    y += 20
                    continue
                # Title line (first non-empty)
                if y < 250:
                    fontsize = 18
                    fontname = "hebo"
                elif y < 350:
                    fontsize = 14
                    fontname = "hebo"
                else:
                    fontsize = 12
                    fontname = "helv"
                tw = pymupdf.TextWriter(page.rect)
                font = pymupdf.Font(fontname)
                text_width = font.text_length(line, fontsize=fontsize)
                x = (595 - text_width) / 2
                tw.append(pymupdf.Point(x, y), line, font=font, fontsize=fontsize)
                tw.write_text(page, color=(0, 0, 0))
                y += fontsize + 8
        else:
            # Regular page with body text
            rect = pymupdf.Rect(72, 72, 523, 780)
            page.insert_textbox(
                rect,
                body_text,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

        # Add page number at bottom center (except title page and error pages)
        displayed = get_displayed_page_number(page_num)
        if displayed is not None:
            font = pymupdf.Font("helv")
            text_width = font.text_length(displayed, fontsize=10)
            x = (595 - text_width) / 2
            tw = pymupdf.TextWriter(page.rect)
            tw.append(pymupdf.Point(x, 820), displayed, font=font, fontsize=10)
            tw.write_text(page, color=(0, 0, 0))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
