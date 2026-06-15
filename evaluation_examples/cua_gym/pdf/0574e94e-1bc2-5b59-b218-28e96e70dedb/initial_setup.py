"""
Initial Setup: Create a 10-page published paper PDF
Task ID: pdf_res_057
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_057'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/published_paper.pdf'


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

    # Page dimensions (Letter size)
    W, H = 612, 792
    LEFT_MARGIN = 72
    RIGHT_MARGIN = 540
    TEXT_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=W, height=H)
    y = 120
    # Title
    page.insert_text(pymupdf.Point(W / 2 - 180, y),
                     "Deep Reinforcement Learning for",
                     fontsize=18, fontname="tibo", color=(0, 0, 0))
    y += 26
    page.insert_text(pymupdf.Point(W / 2 - 200, y),
                     "Autonomous Navigation in Dynamic",
                     fontsize=18, fontname="tibo", color=(0, 0, 0))
    y += 26
    page.insert_text(pymupdf.Point(W / 2 - 80, y),
                     "Environments",
                     fontsize=18, fontname="tibo", color=(0, 0, 0))

    y += 50
    # Authors
    authors = [
        ("Wei Zhang", "Tsinghua University, Beijing, China"),
        ("Sarah Mitchell", "MIT, Cambridge, MA, USA"),
        ("Hiroshi Tanaka", "University of Tokyo, Tokyo, Japan"),
        ("Elena Vasquez", "ETH Zurich, Zurich, Switzerland"),
    ]
    for name, affil in authors:
        page.insert_text(pymupdf.Point(W / 2 - 80, y), name,
                         fontsize=11, fontname="tibo", color=(0, 0, 0))
        y += 14
        page.insert_text(pymupdf.Point(W / 2 - 120, y), affil,
                         fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3))
        y += 20

    # Abstract
    y += 30
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "Abstract",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 18
    abstract = (
        "We present a novel deep reinforcement learning framework for autonomous "
        "navigation in highly dynamic environments. Our approach combines a "
        "hierarchical policy architecture with a learned world model to achieve "
        "robust path planning under uncertainty. The proposed method, Dynamic-Nav, "
        "integrates visual perception with temporal reasoning through a dual-stream "
        "attention mechanism. Experiments on both simulated and real-world datasets "
        "demonstrate that Dynamic-Nav outperforms existing baselines by 23.7% in "
        "success rate and 31.2% in path efficiency. We further show that our "
        "framework generalizes to previously unseen obstacle configurations with "
        "minimal performance degradation. These results establish a new state of "
        "the art for navigation in environments with moving obstacles, pedestrians, "
        "and dynamic terrain conditions."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 140)
    page.insert_textbox(rect, abstract, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 155
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y),
                     "Keywords: reinforcement learning, autonomous navigation, path planning, deep learning",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))

    # ---- Page 2: Introduction ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "1. Introduction",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    intro_text = (
        "Autonomous navigation remains one of the grand challenges in robotics and "
        "artificial intelligence. While significant progress has been achieved in static "
        "environments through classical planning algorithms and learned policies, dynamic "
        "settings with moving obstacles, unpredictable agents, and changing terrain "
        "conditions continue to pose substantial difficulties.\n\n"
        "Traditional approaches to dynamic navigation rely on reactive controllers that "
        "combine local obstacle avoidance with global path planning. Methods such as the "
        "Dynamic Window Approach (DWA) and Velocity Obstacles (VO) have shown effectiveness "
        "in structured environments but struggle with complex, multi-agent scenarios where "
        "long-horizon reasoning is required.\n\n"
        "Recent advances in deep reinforcement learning (DRL) have opened new avenues for "
        "addressing these challenges. By learning end-to-end policies from raw sensory "
        "inputs, DRL agents can potentially handle the full complexity of dynamic environments "
        "without handcrafted features or explicit motion models. However, existing DRL-based "
        "navigation systems face several critical limitations: (1) sample inefficiency during "
        "training, (2) poor generalization to novel configurations, and (3) difficulty in "
        "balancing exploration with safe behavior.\n\n"
        "In this paper, we introduce Dynamic-Nav, a hierarchical reinforcement learning "
        "framework that addresses these limitations through three key innovations. First, we "
        "propose a dual-stream attention mechanism that separately processes static and dynamic "
        "elements of the environment. Second, we incorporate a learned world model that enables "
        "efficient imagination-based planning. Third, we introduce a curriculum learning strategy "
        "that progressively increases environment complexity during training.\n\n"
        "Our contributions are as follows:\n"
        "- A novel hierarchical policy architecture for dynamic navigation\n"
        "- A dual-stream attention mechanism for environment perception\n"
        "- A learned world model for sample-efficient training\n"
        "- Comprehensive evaluation on simulated and real-world benchmarks"
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, intro_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 3: Related Work ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "2. Related Work",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    related_text = (
        "2.1 Classical Navigation Approaches\n\n"
        "The field of robot navigation has a rich history spanning several decades. Early "
        "approaches focused on complete algorithms such as A* and Dijkstra's algorithm "
        "operating on grid-based representations. Potential field methods introduced continuous "
        "representations that naturally combine attractive goals with repulsive obstacles. "
        "The Rapidly-exploring Random Tree (RRT) family of algorithms enabled efficient "
        "sampling-based planning in high-dimensional spaces.\n\n"
        "For dynamic environments, the Dynamic Window Approach (Fox et al., 1997) remains "
        "widely used. It evaluates candidate velocity commands within the robot's dynamic "
        "constraints and selects actions that balance progress toward the goal with obstacle "
        "clearance. Velocity Obstacles (Fiorini and Shiller, 1998) extended this concept by "
        "explicitly reasoning about the future positions of moving obstacles.\n\n"
        "2.2 Deep Reinforcement Learning for Navigation\n\n"
        "The application of deep RL to navigation began with the work of Zhu et al. (2017), "
        "who trained visual navigation policies using target-driven deep RL. Subsequent work "
        "by Mirowski et al. (2018) demonstrated that auxiliary tasks such as depth prediction "
        "and loop closure detection improve navigation performance. Chen et al. (2019) "
        "introduced socially-aware navigation through inverse reinforcement learning from "
        "human demonstrations.\n\n"
        "More recently, transformer-based architectures have shown promise for sequential "
        "decision-making in navigation tasks. Decision Transformer (Chen et al., 2021) and "
        "Gato (Reed et al., 2022) demonstrated that offline RL with sequence modeling can "
        "achieve competitive performance across diverse tasks.\n\n"
        "2.3 World Models for Planning\n\n"
        "World models enable agents to learn predictive models of environment dynamics and "
        "use them for planning. Ha and Schmidhuber (2018) proposed learning compact "
        "representations of environment dynamics using variational autoencoders. Hafner et al. "
        "(2019, 2020, 2023) developed the Dreamer family of algorithms that learn world "
        "models and train policies entirely within the learned model."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, related_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 4: Methodology (Part 1) ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "3. Methodology",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    method1_text = (
        "3.1 Problem Formulation\n\n"
        "We formulate dynamic navigation as a Partially Observable Markov Decision Process "
        "(POMDP) defined by the tuple (S, A, T, R, O, Z, gamma), where S is the state space, "
        "A is the action space, T is the transition function, R is the reward function, O is "
        "the observation space, Z is the observation function, and gamma is the discount factor.\n\n"
        "The agent receives egocentric observations o_t consisting of RGB images, depth maps, "
        "and proprioceptive data. Actions a_t specify desired linear and angular velocities "
        "within kinematic constraints. The reward function combines goal-reaching bonus (+10), "
        "collision penalty (-5), time penalty (-0.01 per step), and progress reward.\n\n"
        "3.2 Hierarchical Policy Architecture\n\n"
        "Our framework decomposes the navigation task into two levels of abstraction:\n\n"
        "High-level policy (pi_H): Operates at 2 Hz, selects subgoals in a learned "
        "latent space. The high-level policy receives the current belief state b_t and "
        "outputs a subgoal g_t in the latent representation space.\n\n"
        "Low-level policy (pi_L): Operates at 10 Hz, generates primitive actions to reach "
        "subgoals while avoiding immediate obstacles. Given the current observation o_t and "
        "subgoal g_t, it produces velocity commands.\n\n"
        "3.3 Dual-Stream Attention Mechanism\n\n"
        "A key challenge in dynamic navigation is distinguishing between static obstacles "
        "(walls, furniture) and dynamic entities (pedestrians, vehicles). We address this "
        "through a dual-stream attention mechanism that processes these elements separately "
        "before fusion.\n\n"
        "Static stream: Processes the current frame through a ResNet-18 encoder to extract "
        "spatial features, followed by a self-attention layer that captures structural "
        "relationships among static elements.\n\n"
        "Dynamic stream: Takes a sequence of the last K=8 frames and applies a spatio-temporal "
        "attention module to identify and track moving entities. The temporal component uses "
        "a causal transformer to model motion patterns."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, method1_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 5: Methodology (Part 2) ----
    page = doc.new_page(width=W, height=H)
    y = 72
    method2_text = (
        "3.4 Learned World Model\n\n"
        "To improve sample efficiency, we incorporate a learned world model that predicts "
        "future states given current observations and actions. The world model consists of "
        "three components:\n\n"
        "Encoder (E): Maps observations o_t to latent states z_t using a convolutional "
        "encoder followed by a recurrent state-space model.\n\n"
        "Dynamics predictor (D): Predicts the next latent state z_{t+1} given z_t and "
        "action a_t. We use a deterministic path combined with a stochastic component to "
        "capture environment uncertainty.\n\n"
        "Decoder (G): Reconstructs observations from latent states for training the "
        "representation. Separate heads predict RGB images, depth maps, and reward signals.\n\n"
        "The world model is trained jointly with the policy using the following objective:\n\n"
        "L_wm = L_recon + beta * L_kl + alpha * L_reward\n\n"
        "where L_recon is the reconstruction loss, L_kl is the KL divergence regularizing "
        "the latent distribution, and L_reward is the reward prediction loss.\n\n"
        "3.5 Curriculum Learning Strategy\n\n"
        "Training navigation agents in complex dynamic environments from scratch is "
        "prohibitively difficult. We employ a curriculum that progressively increases "
        "environment difficulty along three axes:\n\n"
        "Stage 1 (Episodes 0-50K): Static obstacles only. The agent learns basic navigation "
        "and obstacle avoidance in fixed environments.\n\n"
        "Stage 2 (Episodes 50K-150K): Introduction of slow-moving obstacles with "
        "predictable linear trajectories. The agent develops temporal reasoning abilities.\n\n"
        "Stage 3 (Episodes 150K-300K): Full dynamic environments with fast-moving obstacles, "
        "pedestrians following social force models, and random perturbations.\n\n"
        "Stage 4 (Episodes 300K-500K): Adversarial scenarios where obstacle behavior adapts "
        "to the agent's policy, promoting robust generalization."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, method2_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 6: Experimental Setup ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "4. Experimental Setup",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    exp_text = (
        "4.1 Simulation Environments\n\n"
        "We evaluate Dynamic-Nav on three simulation benchmarks of increasing complexity:\n\n"
        "NavBench-Static: A suite of 500 navigation scenarios in indoor environments with "
        "fixed obstacles. Rooms range from simple corridors to complex multi-room layouts.\n\n"
        "NavBench-Dynamic: Extension of NavBench-Static with 3-15 moving obstacles per "
        "scenario. Obstacles follow predefined trajectories with speed variations.\n\n"
        "CrowdNav-3D: A 3D pedestrian navigation benchmark with realistic crowd dynamics. "
        "Includes 200 scenarios in urban settings with 10-50 pedestrians per scene.\n\n"
        "4.2 Real-World Experiments\n\n"
        "We deploy Dynamic-Nav on a TurtleBot3 platform equipped with an Intel RealSense "
        "D435i depth camera and an NVIDIA Jetson Xavier NX for onboard inference. Real-world "
        "experiments are conducted in a 15m x 20m indoor space with movable obstacles and "
        "volunteer pedestrians following scripted and unscripted patterns.\n\n"
        "4.3 Baselines\n\n"
        "We compare against the following methods:\n"
        "- DWA: Dynamic Window Approach with LiDAR-based perception\n"
        "- ORCA: Optimal Reciprocal Collision Avoidance\n"
        "- DRL-Nav: Standard PPO policy with CNN encoder (Chen et al., 2019)\n"
        "- SAC-Nav: Soft Actor-Critic with attention (Li et al., 2021)\n"
        "- Dreamer-Nav: Dreamer V3 adapted for navigation (Hafner et al., 2023)\n\n"
        "4.4 Evaluation Metrics\n\n"
        "- Success Rate (SR): Percentage of episodes reaching the goal\n"
        "- Path Efficiency (PE): Ratio of optimal path length to actual path length\n"
        "- Collision Rate (CR): Percentage of episodes with at least one collision\n"
        "- Average Time to Goal (ATG): Mean time to reach the goal in successful episodes\n"
        "- Social Compliance (SC): Adherence to social navigation norms (CrowdNav only)"
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, exp_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 7: Results (Part 1) ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "5. Results",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    results1_text = (
        "5.1 Simulation Results\n\n"
        "Table 1 presents the main results on our three simulation benchmarks. Dynamic-Nav "
        "achieves the highest success rate across all environments, with particularly "
        "significant improvements in the dynamic settings.\n\n"
        "Table 1: Main simulation results (mean over 5 seeds)\n\n"
        "Method          | NavBench-S  | NavBench-D  | CrowdNav-3D\n"
        "                | SR    PE    | SR    PE    | SR    PE    SC\n"
        "DWA             | 89.2  0.81  | 62.4  0.58  | 45.1  0.42  0.61\n"
        "ORCA            | 91.5  0.85  | 71.3  0.64  | 53.8  0.51  0.72\n"
        "DRL-Nav         | 93.1  0.87  | 74.6  0.68  | 58.2  0.55  0.65\n"
        "SAC-Nav         | 94.8  0.89  | 78.2  0.72  | 63.5  0.60  0.71\n"
        "Dreamer-Nav     | 95.2  0.90  | 81.7  0.76  | 68.9  0.65  0.74\n"
        "Dynamic-Nav     | 97.1  0.94  | 92.3  0.89  | 85.4  0.82  0.88\n\n"
        "On NavBench-Dynamic, Dynamic-Nav improves the success rate by 10.6 percentage points "
        "over the best baseline (Dreamer-Nav). The improvement is even more pronounced on "
        "CrowdNav-3D, where our method achieves an 85.4% success rate compared to 68.9% for "
        "Dreamer-Nav, representing a 23.9% relative improvement.\n\n"
        "5.2 Ablation Study\n\n"
        "We conduct ablations on NavBench-Dynamic to evaluate the contribution of each "
        "component:\n\n"
        "Configuration                    | SR    | PE    | CR\n"
        "Full Dynamic-Nav                 | 92.3  | 0.89  | 3.2%\n"
        "w/o Dual-Stream Attention        | 85.1  | 0.78  | 8.7%\n"
        "w/o World Model                  | 83.4  | 0.75  | 9.1%\n"
        "w/o Curriculum Learning          | 78.9  | 0.71  | 12.3%\n"
        "w/o Hierarchical Policy          | 81.2  | 0.73  | 10.8%\n"
        "Single-level + No World Model    | 72.5  | 0.62  | 15.6%\n\n"
        "All components contribute significantly to performance. The curriculum learning "
        "strategy has the largest individual impact, suggesting that progressive training "
        "is essential for learning robust policies in complex dynamic settings."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, results1_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 8: Results (Part 2) ----
    page = doc.new_page(width=W, height=H)
    y = 72
    results2_text = (
        "5.3 Real-World Experiments\n\n"
        "We evaluate Dynamic-Nav in three real-world scenarios with increasing difficulty:\n\n"
        "Scenario A (Static): Office environment with fixed furniture. 50 trials.\n"
        "Results: SR=96.0%, PE=0.91, CR=2.0%, ATG=12.3s\n\n"
        "Scenario B (Dynamic-Slow): Same environment with 3 slow-moving obstacles on "
        "predefined paths. 50 trials.\n"
        "Results: SR=90.0%, PE=0.84, CR=6.0%, ATG=15.7s\n\n"
        "Scenario C (Pedestrians): Open space with 5-8 volunteer pedestrians walking "
        "naturally. 100 trials.\n"
        "Results: SR=82.0%, PE=0.76, CR=8.0%, ATG=18.2s\n\n"
        "The sim-to-real transfer gap is moderate, with approximately 3-10% reduction in "
        "success rate compared to corresponding simulation scenarios. The dual-stream "
        "attention mechanism proves particularly beneficial in real-world settings by "
        "effectively separating static and dynamic elements despite sensor noise.\n\n"
        "5.4 Generalization Analysis\n\n"
        "To assess generalization, we evaluate on held-out environment configurations not "
        "seen during training. We vary three factors: room layout, number of dynamic "
        "obstacles, and obstacle speed.\n\n"
        "Novel layouts: SR drops by only 2.1% (from 92.3% to 90.2%), indicating strong "
        "spatial generalization.\n\n"
        "Increased obstacle count (2x training maximum): SR decreases by 7.8% (to 84.5%), "
        "showing graceful degradation under increased density.\n\n"
        "Increased obstacle speed (1.5x training maximum): SR decreases by 5.3% (to 87.0%), "
        "demonstrating that the temporal reasoning module provides some robustness to faster "
        "dynamics.\n\n"
        "5.5 Computational Efficiency\n\n"
        "Dynamic-Nav runs at 15.2 Hz on an NVIDIA Jetson Xavier NX, well above the 10 Hz "
        "control frequency required by the low-level policy. The high-level policy at 2 Hz "
        "requires only 12ms per inference. Total training time is 72 GPU-hours on a single "
        "NVIDIA A100, compared to 120 GPU-hours for Dreamer-Nav."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, results2_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 9: Discussion ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "6. Discussion",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    disc_text = (
        "Our results demonstrate that combining hierarchical policies, dual-stream attention, "
        "and learned world models yields substantial improvements for dynamic navigation. "
        "Several key insights emerge from our analysis.\n\n"
        "The importance of curriculum learning. The ablation study reveals that curriculum "
        "learning contributes the most significant individual improvement. Without progressive "
        "training, agents converge to conservative policies that avoid dynamic regions entirely, "
        "leading to longer paths and lower success rates in scenarios requiring passage through "
        "dense areas.\n\n"
        "Dual-stream attention enables selective processing. Qualitative analysis of attention "
        "maps shows that the static stream focuses on structural features (doorways, corridors, "
        "walls) while the dynamic stream tracks individual moving entities. This separation "
        "allows the policy to maintain a stable spatial representation while adapting to "
        "dynamic changes.\n\n"
        "World model quality correlates with planning horizon. We observe that the world model "
        "prediction accuracy degrades beyond approximately 2 seconds into the future. This "
        "aligns with the chosen high-level policy frequency of 2 Hz, which replans before "
        "prediction quality significantly deteriorates.\n\n"
        "Limitations. Despite strong performance, Dynamic-Nav has several limitations. First, "
        "the method assumes access to depth sensing, which may not be available on all "
        "platforms. Second, the hierarchical decomposition introduces additional hyperparameters "
        "(subgoal space dimensionality, planning frequency) that require tuning. Third, our "
        "evaluation does not address multi-agent coordination where multiple robots must "
        "navigate simultaneously.\n\n"
        "Future directions. We identify three promising directions for future work: (1) "
        "extending the framework to multi-robot coordination using decentralized policies, "
        "(2) incorporating language instructions for task-conditioned navigation, and (3) "
        "developing continual learning capabilities that adapt the world model to new "
        "environments online without catastrophic forgetting."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, H - 72)
    page.insert_textbox(rect, disc_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 10: Conclusion and References ----
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "7. Conclusion",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 22
    concl_text = (
        "We presented Dynamic-Nav, a hierarchical deep reinforcement learning framework for "
        "autonomous navigation in dynamic environments. Through the combination of dual-stream "
        "attention, learned world models, and curriculum training, our approach achieves "
        "state-of-the-art results on multiple benchmarks with a 23.7% improvement in success "
        "rate over the strongest baseline on the challenging CrowdNav-3D benchmark.\n\n"
        "Our real-world experiments on a TurtleBot3 platform validate the practical "
        "applicability of the approach, with moderate sim-to-real transfer gaps. The framework's "
        "modular design allows individual components to be upgraded independently as better "
        "architectures become available."
    )
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 120)
    page.insert_textbox(rect, concl_text, fontsize=10, fontname="tiro",
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 140
    page.insert_text(pymupdf.Point(LEFT_MARGIN, y), "References",
                     fontsize=14, fontname="tibo", color=(0, 0, 0))
    y += 20
    refs = [
        "[1] Chen, C., et al. (2019). Crowd-robot interaction: Crowd-aware robot navigation with attention-based DRL. ICRA.",
        "[2] Chen, L., et al. (2021). Decision Transformer: Reinforcement learning via sequence modeling. NeurIPS.",
        "[3] Fiorini, P., Shiller, Z. (1998). Motion planning in dynamic environments using velocity obstacles. IJRR, 17(7).",
        "[4] Fox, D., Burgard, W., Thrun, S. (1997). The dynamic window approach to collision avoidance. IEEE RA, 4(1).",
        "[5] Ha, D., Schmidhuber, J. (2018). World models. arXiv:1803.10122.",
        "[6] Hafner, D., et al. (2023). Mastering diverse domains through world models. arXiv:2301.04104.",
        "[7] Li, S., et al. (2021). Attention-based navigation with SAC in dynamic environments. CoRL.",
        "[8] Mirowski, P., et al. (2018). Learning to navigate in complex environments. ICLR.",
        "[9] Reed, S., et al. (2022). A generalist agent. arXiv:2205.06175.",
        "[10] Zhu, Y., et al. (2017). Target-driven visual navigation using deep RL. ICRA.",
    ]
    for ref in refs:
        rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 28)
        page.insert_textbox(rect, ref, fontsize=8, fontname="tiro")
        y += 28

    # Add page numbers to all pages (footer area, centered)
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(pymupdf.Point(W / 2 - 5, H - 40),
                      str(i + 1), fontsize=9, fontname="tiro", color=(0.4, 0.4, 0.4))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
