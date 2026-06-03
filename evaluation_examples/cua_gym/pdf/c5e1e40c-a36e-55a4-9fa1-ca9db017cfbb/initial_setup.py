"""
Initial Setup: Build a 45-page dissertation PDF with no bookmarks
Task ID: pdf_mbc_048
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
TASK_ID = 'pdf_mbc_048'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/dissertation.pdf'

# Page layout constants
PAGE_W, PAGE_H = 595, 842  # A4
MARGIN_LEFT = 72
MARGIN_RIGHT = 523
MARGIN_TOP = 72
MARGIN_BOTTOM = 770
BODY_RECT = pymupdf.Rect(MARGIN_LEFT, 120, MARGIN_RIGHT, MARGIN_BOTTOM)

# Dissertation content organized by page ranges
CHAPTER_CONTENT = {
    # Page 1: Abstract
    1: ("Abstract", [
        "This dissertation investigates the application of deep reinforcement learning techniques "
        "to autonomous navigation systems in complex urban environments. We present a novel framework "
        "that combines model-based planning with model-free policy optimization to achieve robust "
        "navigation under uncertainty.",
        "Our approach addresses three fundamental challenges: partial observability of the environment, "
        "dynamic obstacle avoidance, and long-horizon planning under computational constraints. Through "
        "extensive experimentation on both simulated and real-world platforms, we demonstrate that our "
        "hybrid architecture achieves a 34% improvement in navigation success rate compared to existing "
        "state-of-the-art methods.",
        "The key contributions of this work include: (1) a hierarchical decision-making framework that "
        "decomposes complex navigation tasks into manageable sub-goals, (2) a novel reward shaping "
        "mechanism that accelerates learning convergence by 2.7x, and (3) a comprehensive benchmark "
        "suite for evaluating autonomous navigation in urban scenarios.",
        "We validate our approach across 12 distinct urban environments with varying complexity levels, "
        "traffic densities ranging from 50 to 500 vehicles per square kilometer, and pedestrian flows "
        "between 200 and 2000 individuals per hour. Results consistently show superior performance in "
        "safety metrics, computational efficiency, and generalization to unseen environments.",
    ]),
    # Pages 2-4: Abstract continuation / blank filler
    2: ("", [
        "Keywords: deep reinforcement learning, autonomous navigation, urban environments, "
        "hierarchical planning, model-based reinforcement learning, policy optimization.",
        "",
        "Declaration: I hereby declare that this dissertation is the result of my own original work "
        "and has not been submitted for any other degree or professional qualification. All sources "
        "of information have been properly acknowledged.",
        "",
        "Acknowledgements",
        "",
        "I would like to express my deepest gratitude to my advisor, Professor Elena Vasquez, for her "
        "unwavering support and guidance throughout this research journey. Her insights into multi-agent "
        "systems and reinforcement learning theory were instrumental in shaping the direction of this work.",
        "I am also grateful to my committee members, Dr. James Thornton and Dr. Priya Ramanathan, "
        "for their constructive feedback and thoughtful suggestions during the development of this thesis.",
        "Special thanks go to the members of the Autonomous Systems Laboratory, particularly Dr. Wei "
        "Zhang and Maria Gonzalez, for the countless discussions and collaborative experiments that "
        "enriched this research significantly.",
    ]),
    3: ("", [
        "Table of Contents",
        "",
        "Abstract .................................................. 1",
        "Chapter 1: Introduction ................................... 5",
        "  1.1 Background .......................................... 5",
        "  1.2 Motivation .......................................... 8",
        "Chapter 2: Literature Review ............................. 12",
        "  2.1 Historical Context .................................. 12",
        "  2.2 Current Research .................................... 18",
        "    2.2.1 Method A ........................................ 18",
        "    2.2.2 Method B ........................................ 22",
        "Chapter 3: Methodology ................................... 26",
        "References ............................................... 40",
    ]),
    4: ("", [
        "List of Figures",
        "",
        "Figure 1.1: Overview of the autonomous navigation pipeline ........... 6",
        "Figure 1.2: Comparison of reactive and deliberative architectures .... 7",
        "Figure 2.1: Timeline of key developments in RL-based navigation ..... 13",
        "Figure 2.2: Taxonomy of current approaches .......................... 19",
        "Figure 3.1: System architecture diagram ............................. 27",
        "Figure 3.2: Training pipeline overview .............................. 29",
        "",
        "List of Tables",
        "",
        "Table 2.1: Comparison of classical planning methods ................. 14",
        "Table 2.2: Summary of deep RL approaches for navigation ............ 20",
        "Table 3.1: Hyperparameter configurations ........................... 30",
    ]),
    # Pages 5-7: Chapter 1 Introduction / 1.1 Background
    5: ("Chapter 1: Introduction", [
        "1.1 Background",
        "",
        "Autonomous navigation in urban environments represents one of the most challenging problems "
        "in modern robotics and artificial intelligence. The complexity arises from the need to process "
        "high-dimensional sensory inputs, reason about the intentions of other agents, and make "
        "real-time decisions under strict safety constraints.",
        "The past decade has witnessed remarkable advances in deep learning, particularly in areas such "
        "as computer vision, natural language processing, and game playing. These advances have "
        "naturally led to the application of deep learning techniques to autonomous navigation, with "
        "deep reinforcement learning (DRL) emerging as a particularly promising paradigm.",
        "Early work in this field focused on simple grid-world environments, where agents learned "
        "basic navigation policies through trial and error. Mnih et al. (2015) demonstrated that deep "
        "Q-networks (DQN) could learn to play Atari games at superhuman levels, sparking interest in "
        "applying similar techniques to more complex decision-making problems.",
    ]),
    6: ("", [
        "The transition from game environments to real-world navigation introduced several fundamental "
        "challenges. Unlike games with discrete action spaces and perfect state observation, real-world "
        "navigation requires continuous control, deals with partial observability, and demands robust "
        "performance under distribution shift between training and deployment conditions.",
        "Several architectural innovations have been proposed to address these challenges. Convolutional "
        "neural networks (CNNs) have been used to process visual inputs from cameras and LiDAR sensors. "
        "Recurrent neural networks (RNNs) and their variants, such as Long Short-Term Memory (LSTM) "
        "networks, have been employed to maintain memory of past observations and handle temporal "
        "dependencies in sequential decision-making.",
        "More recently, attention mechanisms and transformer architectures have been explored for their "
        "ability to selectively focus on relevant features in complex environments. These architectures "
        "have shown particular promise in multi-agent scenarios, where an autonomous vehicle must "
        "attend to multiple dynamic entities simultaneously.",
    ]),
    7: ("", [
        "The integration of planning and learning has emerged as a critical research direction. "
        "Pure model-free approaches, while capable of learning complex behaviors, often require "
        "prohibitively large amounts of interaction data and may fail to generalize to novel situations. "
        "Model-based approaches, on the other hand, can leverage learned environment models to plan "
        "ahead, but their performance is limited by the accuracy of the learned models.",
        "Hybrid approaches that combine the strengths of both paradigms have shown promising results. "
        "The Dreamer algorithm (Hafner et al., 2020) demonstrated that learning a world model and "
        "planning within it could achieve competitive performance with significantly fewer environment "
        "interactions. AlphaGo and its successors showed the power of combining learned value functions "
        "with Monte Carlo tree search for planning.",
        "This dissertation builds upon these foundational ideas, proposing a hierarchical framework "
        "that leverages model-based planning at a strategic level while employing model-free policy "
        "optimization for low-level control, creating a synergistic system that addresses the unique "
        "challenges of urban autonomous navigation.",
    ]),
    # Pages 8-11: 1.2 Motivation
    8: ("", [
        "1.2 Motivation",
        "",
        "The motivation for this research stems from several converging trends in technology and "
        "society. The global autonomous vehicle market is projected to reach $556.67 billion by 2026, "
        "with major automotive manufacturers and technology companies investing heavily in self-driving "
        "technology. However, current systems still struggle with the complexity of urban environments, "
        "particularly in scenarios involving dense traffic, unpredictable pedestrian behavior, and "
        "adverse weather conditions.",
        "According to the National Highway Traffic Safety Administration (NHTSA), approximately 94% "
        "of serious crashes are due to human error. Autonomous navigation systems have the potential "
        "to dramatically reduce this number, but only if they can reliably handle the full spectrum "
        "of driving scenarios. Current systems, while impressive in controlled conditions, often "
        "disengage in complex urban situations, requiring human intervention.",
        "The fundamental limitation of existing approaches lies in their reliance on hand-crafted "
        "rules and pre-programmed behaviors for edge cases. As the number of possible scenarios grows "
        "combinatorially with environment complexity, this approach becomes intractable. Learning-based "
        "methods offer a scalable alternative, but current deep RL algorithms face challenges in "
        "sample efficiency, safety guarantees, and transferability across domains.",
    ]),
    9: ("", [
        "From a technical perspective, three specific gaps in the current literature motivate this work:",
        "",
        "First, most existing DRL-based navigation systems treat the problem as a monolithic "
        "decision-making task. This flat approach struggles with long-horizon planning, as the "
        "credit assignment problem becomes increasingly difficult when the time between an action "
        "and its ultimate consequence spans hundreds or thousands of steps. Our hierarchical framework "
        "addresses this by decomposing the problem into multiple levels of abstraction.",
        "Second, the exploration-exploitation tradeoff in urban navigation presents unique safety "
        "challenges. Unlike game environments where exploration failures have no real consequences, "
        "unsafe exploration in autonomous driving can lead to catastrophic outcomes. Our reward "
        "shaping mechanism provides dense learning signals that guide exploration toward safe and "
        "efficient behaviors without compromising the optimality of the learned policy.",
        "Third, the lack of standardized benchmarks for urban autonomous navigation makes it "
        "difficult to compare different approaches fairly. Existing benchmarks either focus on "
        "simplified scenarios or lack the diversity needed to test generalization. Our benchmark "
        "suite addresses this gap by providing a comprehensive evaluation framework.",
    ]),
    10: ("", [
        "The practical implications of this research extend beyond autonomous vehicles. The techniques "
        "developed in this dissertation are applicable to a wide range of autonomous navigation "
        "scenarios, including:",
        "",
        "- Delivery robots navigating sidewalks and pedestrian areas in urban centers",
        "- Indoor service robots operating in hospitals, warehouses, and office buildings",
        "- Search and rescue drones navigating disaster-affected areas",
        "- Agricultural robots performing precision farming tasks",
        "- Underwater autonomous vehicles conducting ocean exploration",
        "",
        "Each of these applications shares the fundamental challenges of operating in partially "
        "observable, dynamic environments with safety constraints. The hierarchical planning framework "
        "and reward shaping mechanisms proposed in this dissertation provide a general-purpose solution "
        "that can be adapted to these diverse domains with minimal modification.",
        "Furthermore, the benchmark suite developed as part of this work can serve as a foundation "
        "for evaluating navigation systems across different application domains, promoting "
        "reproducibility and fair comparison in the research community.",
    ]),
    11: ("", [
        "Research Objectives",
        "",
        "Based on the identified gaps and motivations, this dissertation pursues the following "
        "specific research objectives:",
        "",
        "Objective 1: Design and implement a hierarchical reinforcement learning framework for "
        "autonomous urban navigation that effectively decomposes complex navigation tasks into "
        "manageable sub-goals while maintaining global optimality guarantees.",
        "",
        "Objective 2: Develop a novel reward shaping mechanism that accelerates learning convergence "
        "while preserving the optimal policy, with theoretical analysis of convergence properties "
        "and empirical validation across multiple environment configurations.",
        "",
        "Objective 3: Create a comprehensive benchmark suite for evaluating autonomous navigation "
        "systems in urban environments, encompassing diverse scenarios, standardized metrics, and "
        "baseline implementations for fair comparison.",
        "",
        "Objective 4: Validate the proposed framework through extensive experiments on both simulated "
        "and real-world platforms, demonstrating practical applicability and scalability.",
    ]),
    # Pages 12-17: Chapter 2 Literature Review / 2.1 Historical Context
    12: ("Chapter 2: Literature Review", [
        "2.1 Historical Context",
        "",
        "The history of autonomous navigation research spans several decades, evolving from simple "
        "reactive systems to sophisticated learning-based architectures. This section traces the key "
        "developments that have shaped the field and provides context for the approach presented in "
        "this dissertation.",
        "The earliest autonomous navigation systems emerged in the 1960s and 1970s, with Shakey the "
        "Robot (Nilsson, 1984) being one of the most notable examples. Shakey combined logical "
        "reasoning with primitive computer vision to navigate simple indoor environments. The system "
        "used the STRIPS planner for high-level task planning and basic obstacle avoidance for "
        "low-level control.",
        "The 1980s saw the development of the subsumption architecture by Brooks (1986), which "
        "proposed a layered control structure where simple behaviors could be combined to produce "
        "complex navigation capabilities. This reactive approach contrasted sharply with the "
        "deliberative planning paradigm exemplified by Shakey, and the tension between reactive "
        "and deliberative approaches continues to influence the field today.",
    ]),
    13: ("", [
        "The DARPA Autonomous Land Vehicle (ALV) program in the 1980s and the subsequent DARPA Grand "
        "Challenge events (2004, 2005, 2007) were pivotal in advancing autonomous navigation "
        "technology. The first Grand Challenge in 2004 saw no vehicle complete the 142-mile course "
        "through the Mojave Desert. By 2005, five vehicles finished the course, with Stanley "
        "(Thrun et al., 2006) winning the competition using a combination of machine learning "
        "and probabilistic reasoning.",
        "The 2007 DARPA Urban Challenge marked a significant shift toward urban navigation, requiring "
        "vehicles to operate in traffic alongside other vehicles. The winning entry, Boss (Urmson "
        "et al., 2008), employed a sophisticated perception pipeline, a planning system based on "
        "lattice-based search, and a behavioral layer for traffic rule compliance.",
        "Table 2.1: Key Milestones in Autonomous Navigation",
        "",
        "Year | Event | Significance",
        "1966 | Shakey the Robot | First autonomous mobile robot",
        "1986 | Subsumption Architecture | Reactive navigation paradigm",
        "2004 | DARPA Grand Challenge | Off-road autonomous navigation",
        "2007 | DARPA Urban Challenge | Urban autonomous navigation",
        "2015 | DQN (Mnih et al.) | Deep RL for decision-making",
        "2019 | Waymo One | Commercial autonomous ride-hailing",
    ]),
    14: ("", [
        "The introduction of deep learning to autonomous navigation began in earnest around 2015, "
        "catalyzed by the success of deep neural networks in computer vision tasks. Bojarski et al. "
        "(2016) demonstrated end-to-end learning for self-driving, where a convolutional neural "
        "network learned to map raw camera images directly to steering commands. This approach, "
        "while limited in its applicability, demonstrated the potential of learning-based methods.",
        "Concurrent with the development of end-to-end learning, researchers began exploring "
        "reinforcement learning for navigation. The combination of deep neural networks with "
        "RL algorithms gave rise to deep reinforcement learning, which offered a principled "
        "framework for learning navigation policies through interaction with the environment.",
        "Several key algorithms emerged during this period. Deep Q-Networks (DQN) and their "
        "extensions (Double DQN, Dueling DQN, Prioritized Experience Replay) provided stable "
        "training for discrete action spaces. Policy gradient methods (REINFORCE, A3C, PPO) "
        "enabled training with continuous action spaces, making them more suitable for vehicle "
        "control applications.",
    ]),
    15: ("", [
        "The sim-to-real transfer problem became a central focus of research as the gap between "
        "simulated training environments and real-world deployment conditions became apparent. "
        "Domain randomization (Tobin et al., 2017) and domain adaptation techniques were developed "
        "to improve the transferability of policies learned in simulation.",
        "The development of high-fidelity simulators played a crucial role in advancing DRL-based "
        "navigation. CARLA (Dosovitskiy et al., 2017) provided a realistic urban driving simulator "
        "built on Unreal Engine, offering detailed urban environments with dynamic traffic. "
        "AirSim (Shah et al., 2018) provided similar capabilities for aerial vehicles. These "
        "simulators enabled large-scale training that would be impractical in real-world settings.",
        "Multi-agent reinforcement learning (MARL) emerged as an important research direction "
        "as researchers recognized the need to model interactions between autonomous vehicles "
        "and other road users. Cooperative and competitive MARL frameworks were developed to "
        "handle scenarios such as intersection management, lane merging, and platoon formation.",
    ]),
    16: ("", [
        "The integration of graph neural networks (GNNs) with reinforcement learning represented "
        "another significant advance. GNNs provided a natural way to represent the relational "
        "structure of traffic scenarios, where vehicles, pedestrians, and infrastructure elements "
        "form a dynamic interaction graph. Works by Li et al. (2020) and Kipf et al. (2019) "
        "demonstrated the effectiveness of this approach for predicting the behavior of other "
        "road users.",
        "Safety-constrained reinforcement learning gained prominence as the field moved toward "
        "real-world deployment. Constrained MDPs (Altman, 1999) and their deep RL counterparts "
        "(CPO, TRPO-Lagrangian) provided formal frameworks for optimizing performance subject to "
        "safety constraints. However, providing hard safety guarantees remained an open challenge, "
        "particularly for complex urban environments.",
        "The emergence of foundation models and large language models (LLMs) in 2022-2023 opened "
        "new possibilities for autonomous navigation. These models demonstrated remarkable "
        "capabilities in understanding context, reasoning about novel situations, and generating "
        "human-interpretable explanations. Researchers began exploring the integration of LLMs "
        "with navigation systems for high-level reasoning and decision-making.",
    ]),
    17: ("", [
        "The current state of the art in autonomous navigation reflects the convergence of multiple "
        "research traditions. Modern systems typically employ a modular architecture consisting of:",
        "",
        "1. Perception: Processing sensor data (cameras, LiDAR, radar) to build an understanding "
        "of the environment, including object detection, tracking, and semantic segmentation.",
        "",
        "2. Prediction: Forecasting the future trajectories of other agents based on their "
        "observed behavior and contextual information.",
        "",
        "3. Planning: Generating a sequence of actions that achieve the navigation goal while "
        "satisfying safety constraints and traffic rules.",
        "",
        "4. Control: Executing the planned trajectory through low-level actuator commands.",
        "",
        "While this modular approach provides interpretability and maintainability, the interfaces "
        "between modules can lead to information loss and error propagation. End-to-end learning "
        "approaches aim to address these limitations but face challenges in safety assurance and "
        "interpretability. The framework proposed in this dissertation seeks to balance these "
        "competing concerns through hierarchical decomposition.",
    ]),
    # Pages 18-21: 2.2 Current Research / 2.2.1 Method A
    18: ("", [
        "2.2 Current Research",
        "",
        "2.2.1 Method A: Model-Free Deep Reinforcement Learning",
        "",
        "Model-free deep reinforcement learning has been the dominant paradigm for learning "
        "navigation policies. These methods directly learn a mapping from observations to actions "
        "without explicitly modeling the environment dynamics. The key advantage is their ability "
        "to handle complex, high-dimensional observations without requiring accurate environment "
        "models.",
        "Proximal Policy Optimization (PPO) has emerged as one of the most widely used algorithms "
        "for continuous control in navigation tasks. Introduced by Schulman et al. (2017), PPO "
        "provides stable training through a clipped surrogate objective that prevents large policy "
        "updates. Its simplicity and effectiveness have made it the default choice for many "
        "navigation applications.",
        "Soft Actor-Critic (SAC) represents another popular choice, particularly for tasks "
        "requiring exploration. SAC maximizes a modified objective that includes an entropy bonus, "
        "encouraging the agent to maintain a stochastic policy that explores diverse behaviors. "
        "Haarnoja et al. (2018) demonstrated that SAC could learn locomotion and manipulation "
        "policies with remarkable sample efficiency.",
    ]),
    19: ("", [
        "Table 2.2: Comparison of Model-Free DRL Approaches for Navigation",
        "",
        "Algorithm | Action Space | Sample Eff. | Stability | Key Feature",
        "DQN | Discrete | Low | Moderate | Experience Replay",
        "A3C | Both | Low | Low | Asynchronous Training",
        "PPO | Continuous | Moderate | High | Clipped Objective",
        "SAC | Continuous | High | High | Entropy Regularization",
        "TD3 | Continuous | High | High | Twin Critics",
        "",
        "Recent work has focused on improving sample efficiency through techniques such as "
        "hindsight experience replay (HER), which enables learning from failed trajectories by "
        "relabeling goals. Andrychowicz et al. (2017) showed that HER could dramatically "
        "accelerate learning in goal-conditioned navigation tasks.",
        "Curriculum learning has been applied to gradually increase the difficulty of navigation "
        "scenarios during training. Starting with simple environments and progressively introducing "
        "complexity (more traffic, complex intersections, adverse weather) has been shown to "
        "improve both learning speed and final performance.",
    ]),
    20: ("", [
        "Attention mechanisms have been integrated into model-free DRL architectures to improve "
        "the agent's ability to focus on relevant aspects of complex scenes. Multi-head attention "
        "layers allow the agent to simultaneously attend to different objects and regions, "
        "providing a richer representation of the environment than traditional CNN-based approaches.",
        "Graph attention networks (GATs) have been particularly effective for modeling interactions "
        "between traffic participants. Each vehicle, pedestrian, or cyclist is represented as a "
        "node in a graph, with edges encoding spatial and temporal relationships. The attention "
        "mechanism learns to weigh these relationships based on their relevance to the current "
        "decision.",
        "Transfer learning and meta-learning approaches have been explored to improve generalization "
        "across different urban environments. The key insight is that navigation skills learned in "
        "one city should be transferable to another, with only minor adaptations needed for local "
        "traffic patterns and road layouts. MAML (Finn et al., 2017) and its variants have shown "
        "promising results in few-shot adaptation to new environments.",
    ]),
    21: ("", [
        "Despite significant progress, model-free DRL approaches for navigation face several "
        "persistent challenges:",
        "",
        "Challenge 1: Sample efficiency remains a major concern. Training a navigation agent from "
        "scratch typically requires millions of environment interactions, which is impractical for "
        "real-world training. Even with sophisticated simulators, the computational cost of training "
        "can be prohibitive.",
        "",
        "Challenge 2: Safety during training and deployment is difficult to guarantee. Model-free "
        "methods learn through trial and error, and errors in navigation can have severe "
        "consequences. While constrained RL methods provide soft safety guarantees, hard constraints "
        "are difficult to enforce without sacrificing optimality.",
        "",
        "Challenge 3: Generalization to unseen scenarios remains limited. Agents trained in specific "
        "environments often fail when encountering novel situations, such as unusual road layouts, "
        "unexpected obstacle configurations, or adversarial behaviors from other road users.",
        "",
        "These limitations motivate the exploration of model-based and hybrid approaches, which "
        "we discuss in the following section.",
    ]),
    # Pages 22-25: 2.2.2 Method B
    22: ("", [
        "2.2.2 Method B: Model-Based and Hybrid Approaches",
        "",
        "Model-based reinforcement learning (MBRL) addresses the sample efficiency limitations of "
        "model-free methods by learning an explicit model of the environment dynamics. This model "
        "can be used for planning, generating synthetic training data, or both. The key advantage "
        "is that the agent can reason about the consequences of its actions before executing them, "
        "reducing the need for extensive real-world interaction.",
        "The World Models framework (Ha and Schmidhuber, 2018) demonstrated that an agent could "
        "learn a compact latent representation of the environment and use it for planning. The "
        "system consisted of three components: a visual encoder (V), a memory module (M), and a "
        "controller (C). The V component encoded raw observations into a compact latent space, "
        "M learned the dynamics of the latent space, and C optimized actions within the learned "
        "model.",
        "Dreamer (Hafner et al., 2020) extended this approach by learning both the world model "
        "and the policy entirely within the latent space. By imagining trajectories in the learned "
        "model and optimizing the policy using these imagined trajectories, Dreamer achieved "
        "state-of-the-art performance on continuous control benchmarks with significantly fewer "
        "environment interactions.",
    ]),
    23: ("", [
        "The application of MBRL to autonomous navigation has yielded promising results. Rhinehart "
        "et al. (2019) proposed DEEP IMITATIVE MODELS, which combined imitation learning with "
        "model-based planning for autonomous driving. The system learned a generative model of "
        "expert trajectories and used it to plan goal-directed navigation while avoiding collisions.",
        "Neural network-based trajectory prediction models have been integrated into planning "
        "frameworks to anticipate the behavior of other road users. These models typically use "
        "recurrent or transformer architectures to encode observed trajectories and decode "
        "predicted future positions. The predicted trajectories are then used by the planner to "
        "generate safe and efficient navigation strategies.",
        "Monte Carlo Tree Search (MCTS) has been combined with learned value functions and "
        "dynamics models to perform lookahead planning in complex scenarios. This approach, "
        "inspired by the success of AlphaGo, enables the agent to consider multiple possible "
        "futures and select actions that maximize long-term utility while managing risk.",
        "Ensemble methods have been employed to quantify uncertainty in learned dynamics models. "
        "By maintaining an ensemble of models and measuring disagreement between them, the agent "
        "can distinguish between well-understood regions of the state space (where the model is "
        "reliable) and novel situations (where caution is warranted).",
    ]),
    24: ("", [
        "Hybrid approaches that combine model-free and model-based components have emerged as a "
        "promising direction. The key insight is that model-based planning can provide strategic "
        "guidance while model-free policies handle low-level control, leveraging the strengths "
        "of both paradigms.",
        "Options framework (Sutton et al., 1999) and its deep learning extensions provide a "
        "natural way to implement hierarchical RL for navigation. High-level options (e.g., "
        "'follow lane', 'turn left at intersection', 'change lane') are composed of low-level "
        "primitive actions. A meta-controller selects options based on the current context, "
        "while each option has its own termination condition and policy.",
        "Feudal reinforcement learning (Vezhnevets et al., 2017) introduced a manager-worker "
        "architecture where a high-level manager sets goals for a low-level worker. The manager "
        "operates at a coarser temporal resolution, setting subgoals every N steps, while the "
        "worker optimizes actions to achieve these subgoals. This temporal abstraction enables "
        "effective planning over long horizons.",
        "HIRO (Nachum et al., 2018) and HAC (Levy et al., 2019) further developed hierarchical "
        "RL for continuous control, demonstrating that multi-level hierarchies could solve tasks "
        "requiring extended sequences of coordinated behaviors. These methods showed particular "
        "promise for navigation tasks with sparse rewards.",
    ]),
    25: ("", [
        "The integration of classical planning with learned components represents another form of "
        "hybrid approach. Systems like LeTS-Drive (Cai et al., 2020) use learned cost functions "
        "within classical trajectory optimization frameworks, combining the interpretability and "
        "constraint satisfaction guarantees of classical planning with the flexibility and "
        "adaptability of learned models.",
        "Diffusion models have recently been applied to trajectory planning for autonomous "
        "navigation. Janner et al. (2022) proposed Diffuser, which frames planning as iterative "
        "denoising of trajectory distributions. This approach naturally handles multi-modal "
        "trajectory distributions and can be conditioned on various objectives and constraints.",
        "Language-conditioned navigation has gained attention as a way to incorporate high-level "
        "reasoning into navigation systems. By conditioning the navigation policy on natural "
        "language instructions or descriptions, the system can handle novel tasks and environments "
        "specified through language rather than requiring task-specific training.",
        "The framework proposed in this dissertation draws inspiration from these hybrid approaches, "
        "combining a model-based strategic planner with model-free tactical execution. The key "
        "innovation lies in the interface between these components and the reward shaping mechanism "
        "that ensures coherent behavior across levels of the hierarchy.",
    ]),
    # Pages 26-39: Chapter 3 Methodology
    26: ("Chapter 3: Methodology", [
        "This chapter presents the technical details of our proposed framework for autonomous urban "
        "navigation. We describe the system architecture, the hierarchical reinforcement learning "
        "formulation, the reward shaping mechanism, and the training procedure.",
        "",
        "3.1 System Architecture Overview",
        "",
        "Our framework consists of three main components operating at different levels of abstraction:",
        "",
        "Strategic Planner (Level 3): A model-based planner that generates high-level route plans "
        "and waypoints based on a learned world model. This component operates at a temporal "
        "resolution of approximately 5 seconds, setting navigation subgoals for the tactical layer.",
        "",
        "Tactical Controller (Level 2): A model-free RL agent that translates high-level waypoints "
        "into specific driving behaviors (lane following, lane changing, intersection navigation). "
        "This component operates at a temporal resolution of approximately 0.5 seconds.",
        "",
        "Reactive Controller (Level 1): A safety-critical control layer that ensures collision "
        "avoidance and vehicle stability. This component operates at the highest frequency "
        "(20-50 Hz) and can override higher-level commands when safety is at risk.",
    ]),
    27: ("", [
        "3.2 Hierarchical RL Formulation",
        "",
        "We formulate the navigation problem as a hierarchical semi-Markov decision process "
        "(HSMDP). At each level i of the hierarchy, we define a tuple (S_i, A_i, T_i, R_i, gamma_i) "
        "where S_i is the state space, A_i is the action space, T_i is the transition function, "
        "R_i is the reward function, and gamma_i is the discount factor.",
        "The key insight of our formulation is that the action space at each level corresponds to "
        "the goal space of the level below. Specifically:",
        "",
        "- Level 3 actions are waypoints in the 2D road network: a_3 in R^2",
        "- Level 2 actions are velocity and heading setpoints: a_2 in R^3 (v, theta, kappa)",
        "- Level 1 actions are actuator commands: a_1 in R^2 (throttle/brake, steering)",
        "",
        "This telescoping structure ensures that high-level strategic decisions are progressively "
        "refined into concrete control actions, with each level operating at an appropriate temporal "
        "scale and abstraction level.",
    ]),
    28: ("", [
        "3.3 State Representation",
        "",
        "The state representation varies across hierarchy levels to capture the relevant information "
        "at each abstraction level:",
        "",
        "Level 3 State: Consists of the ego vehicle's position on the road network graph, the "
        "destination, traffic density estimates along possible routes, and aggregate risk scores "
        "for different road segments. This representation is compact and supports long-horizon "
        "planning.",
        "",
        "Level 2 State: Includes the ego vehicle's kinematic state (position, velocity, heading), "
        "the surrounding vehicles' states within a 100-meter radius (encoded using a graph "
        "attention network), lane markings, traffic signals, and the current high-level waypoint. "
        "This representation captures the tactical situation needed for driving behavior selection.",
        "",
        "Level 1 State: Contains the ego vehicle's detailed dynamic state (velocities, "
        "accelerations, tire slip angles), immediate obstacle positions, and the target velocity "
        "and heading from Level 2. This representation supports high-frequency reactive control.",
    ]),
    29: ("", [
        "3.4 Reward Shaping Mechanism",
        "",
        "One of the key contributions of this work is a novel reward shaping mechanism that provides "
        "dense learning signals while preserving the optimal policy. The shaped reward at each "
        "hierarchy level consists of three components:",
        "",
        "R_shaped = R_task + alpha * R_progress + beta * R_safety",
        "",
        "where R_task is the original sparse task reward (reaching the destination), R_progress "
        "measures progress toward intermediate goals, and R_safety penalizes unsafe states and "
        "actions. The coefficients alpha and beta control the relative importance of these components.",
        "",
        "Theorem 1 (Policy Invariance): Under the potential-based shaping formulation of Ng et al. "
        "(1999), our shaped reward R_shaped preserves the set of optimal policies of the original "
        "MDP. Specifically, for any potential function Phi: S -> R, the shaped reward "
        "F(s, a, s') = gamma * Phi(s') - Phi(s) does not alter the optimal policy.",
        "",
        "We define the potential function using the learned value function from the strategic "
        "planner, ensuring that the shaping reward captures meaningful progress toward the "
        "navigation goal.",
    ]),
    30: ("", [
        "3.5 Training Procedure",
        "",
        "The training procedure follows a bottom-up approach, starting from the lowest level "
        "of the hierarchy and progressively training higher levels:",
        "",
        "Phase 1 - Reactive Controller Training: The Level 1 controller is pre-trained using "
        "imitation learning on expert demonstrations, then fine-tuned with constrained RL to "
        "ensure safety compliance. Training uses 500,000 episodes in a simplified environment.",
        "",
        "Phase 2 - Tactical Controller Training: The Level 2 controller is trained using PPO "
        "with the shaped reward function. The Level 1 controller is frozen during this phase. "
        "Training uses 2,000,000 episodes in urban traffic scenarios with increasing complexity.",
        "",
        "Phase 3 - Strategic Planner Training: The Level 3 world model is trained on collected "
        "trajectory data using supervised learning. The planning policy is then optimized using "
        "Dreamer-style imagination in the learned model. Training uses 5,000,000 imagined episodes.",
        "",
        "Table 3.1: Training Hyperparameters",
        "Parameter | Level 1 | Level 2 | Level 3",
        "Learning rate | 3e-4 | 1e-4 | 5e-5",
        "Batch size | 256 | 512 | 1024",
        "Discount factor | 0.99 | 0.995 | 0.999",
        "Entropy coefficient | 0.01 | 0.005 | 0.001",
    ]),
}

# Fill remaining pages with methodology/results/references content
for p in range(31, 40):
    if p not in CHAPTER_CONTENT:
        CHAPTER_CONTENT[p] = ("", [
            f"Section 3.{p - 25} — Experimental Validation (continued)",
            "",
            f"In this section, we present results from Environment Configuration {p - 30}, which "
            "simulates a high-density urban corridor with 350 vehicles per square kilometer and "
            "1,200 pedestrians per hour. The ego vehicle must navigate a 2.5-kilometer route through "
            "three signalized intersections and two roundabouts.",
            f"The results demonstrate that our hierarchical framework achieves a navigation success "
            f"rate of {85 + (p % 7)}% in this challenging scenario, compared to {62 + (p % 5)}% for the "
            "flat PPO baseline and {71 + (p % 6)}% for the HIRO hierarchical baseline. The improvement "
            "is particularly pronounced in scenarios involving multi-lane roundabouts, where the "
            "strategic planner's lookahead capability enables more effective lane selection.",
            "Safety metrics show a collision rate of 0.3 per 100 km for our method, compared to "
            "1.8 per 100 km for flat PPO and 0.9 per 100 km for HIRO. The reactive safety layer "
            "successfully prevented 98.7% of potential collisions identified during deployment.",
            f"Computational overhead analysis reveals that the strategic planner adds approximately "
            f"{12 + p % 8}ms of latency per planning cycle, well within the 200ms budget allocated for "
            "strategic decisions. The tactical controller operates with an average inference time of "
            "3.2ms, and the reactive controller achieves sub-millisecond response times.",
        ])

# References pages 40-45
REFERENCES = [
    "Altman, E. (1999). Constrained Markov decision processes. CRC Press.",
    "Andrychowicz, M., et al. (2017). Hindsight experience replay. NeurIPS.",
    "Bojarski, M., et al. (2016). End to end learning for self-driving cars. arXiv:1604.07316.",
    "Brooks, R. A. (1986). A robust layered control system for a mobile robot. IEEE Journal of Robotics and Automation, 2(1), 14-23.",
    "Cai, P., et al. (2020). LeTS-Drive: Driving in a crowd by learning from tree search. RSS.",
    "Dosovitskiy, A., et al. (2017). CARLA: An open urban driving simulator. CoRL.",
    "Finn, C., Abbeel, P., & Levine, S. (2017). Model-agnostic meta-learning for fast adaptation of deep networks. ICML.",
    "Ha, D., & Schmidhuber, J. (2018). World models. arXiv:1803.10122.",
    "Haarnoja, T., et al. (2018). Soft actor-critic: Off-policy maximum entropy deep RL with a stochastic actor. ICML.",
    "Hafner, D., et al. (2020). Dream to control: Learning behaviors by latent imagination. ICLR.",
    "Janner, M., Du, Y., Tenenbaum, J., & Levine, S. (2022). Planning with diffusion for flexible behavior synthesis. ICML.",
    "Kipf, T., et al. (2019). Contrastive learning of structured world models. arXiv:1911.12247.",
    "Levy, A., et al. (2019). Learning multi-level hierarchies with hindsight. ICLR.",
    "Li, J., et al. (2020). EvolveGraph: Multi-agent trajectory prediction with dynamic relational reasoning. NeurIPS.",
    "Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540), 529-533.",
    "Nachum, O., et al. (2018). Data-efficient hierarchical reinforcement learning. NeurIPS.",
    "Ng, A. Y., Harada, D., & Russell, S. (1999). Policy invariance under reward transformations: Theory and application to reward shaping. ICML.",
    "Nilsson, N. J. (1984). Shakey the robot. Technical Report 323, SRI International.",
    "Rhinehart, N., McAllister, R., & Levine, S. (2019). Deep imitative models for flexible inference, planning, and control. ICLR.",
    "Schulman, J., et al. (2017). Proximal policy optimization algorithms. arXiv:1707.06347.",
    "Shah, S., et al. (2018). AirSim: High-fidelity visual and physical simulation for autonomous vehicles. FSR.",
    "Sutton, R. S., Precup, D., & Singh, S. (1999). Between MDPs and semi-MDPs: A framework for temporal abstraction in RL. Artificial Intelligence, 112(1-2), 181-211.",
    "Thrun, S., et al. (2006). Stanley: The robot that won the DARPA Grand Challenge. Journal of Field Robotics, 23(9), 661-692.",
    "Tobin, J., et al. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. IROS.",
    "Urmson, C., et al. (2008). Autonomous driving in urban environments: Boss and the Urban Challenge. Journal of Field Robotics, 25(8), 425-466.",
    "Vezhnevets, A. S., et al. (2017). Feudal networks for hierarchical reinforcement learning. ICML.",
]

def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, 46):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        if page_num in CHAPTER_CONTENT:
            title, paragraphs = CHAPTER_CONTENT[page_num]
        elif page_num >= 40:
            title = "References" if page_num == 40 else ""
            # Build references for these pages
            refs_per_page = 5
            start_idx = (page_num - 40) * refs_per_page
            end_idx = min(start_idx + refs_per_page, len(REFERENCES))
            if page_num == 40:
                paragraphs = ["References", ""]
                paragraphs += [f"[{i+1}] {REFERENCES[i]}" for i in range(start_idx, end_idx)]
            elif start_idx < len(REFERENCES):
                paragraphs = [f"[{i+1}] {REFERENCES[i]}" for i in range(start_idx, end_idx)]
            else:
                paragraphs = [""]
        else:
            title = ""
            paragraphs = [
                f"[Page {page_num} content continues from previous section]",
                "",
                "Additional analysis and discussion of the methodology and experimental results "
                "are presented in the following paragraphs, providing further evidence for the "
                "effectiveness of the proposed hierarchical navigation framework.",
            ]

        y_pos = MARGIN_TOP

        # Add chapter title if present
        if title:
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, y_pos),
                title,
                fontsize=18,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y_pos += 30

        # Add body text
        text_body = "\n\n".join(paragraphs)
        body_rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, MARGIN_BOTTOM - 30)
        page.insert_textbox(
            body_rect,
            text_body,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Add page number at bottom center
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 10, MARGIN_BOTTOM + 20),
            str(page_num),
            fontsize=10,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # NO bookmarks - the task is to add them
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 45')
    print(f'Bookmarks: NONE')


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


create_initial()

# Open in Evince for the GUI agent
launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
print('GUI_READY: launched Evince with DISPLAY=:0')
