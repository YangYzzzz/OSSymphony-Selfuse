"""
Initial Setup: Create a 14-page reinforcement learning PDF paper
Task ID: pdf_res_005
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/reinforcement_learning.pdf'

# Page dimensions (Letter)
W, H = 612, 792
MARGIN_LEFT = 72
MARGIN_RIGHT = 540
MARGIN_TOP = 72
MARGIN_BOTTOM = 720
TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def add_page_number(page, page_num, total):
    """Add page number at bottom center."""
    page.insert_text(
        pymupdf.Point(306, 760),
        f"{page_num}",
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
    )

def add_heading(page, y, text, fontsize=16, fontname="hebo"):
    """Add a section heading and return new y position."""
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), text,
                     fontsize=fontsize, fontname=fontname, color=(0, 0, 0))
    return y + fontsize + 10

def add_paragraph(page, y, text, fontsize=11, fontname="tiro"):
    """Add a paragraph in a textbox and return new y position."""
    rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM)
    excess = page.insert_textbox(
        rect, text, fontsize=fontsize, fontname=fontname,
        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Estimate height used (rough: chars per line ~ TEXT_WIDTH / (fontsize * 0.5))
    chars_per_line = int(TEXT_WIDTH / (fontsize * 0.45))
    lines_needed = max(1, len(text) // chars_per_line + 1)
    height_used = lines_needed * (fontsize + 3)
    return y + height_used + 8

ABSTRACT_TEXT = (
    "Reinforcement learning (RL) has emerged as a powerful paradigm for training autonomous agents "
    "to make sequential decisions in complex environments. This paper presents a comprehensive survey "
    "of modern reinforcement learning methods, covering foundational concepts such as Markov Decision "
    "Processes, value-based methods including Q-learning and Deep Q-Networks, and policy gradient "
    "approaches such as REINFORCE, Proximal Policy Optimization, and Actor-Critic architectures. "
    "We examine recent advances in model-based reinforcement learning, multi-agent systems, and the "
    "application of transformer architectures to RL problems. Our analysis reveals that while significant "
    "progress has been made in game-playing, robotic manipulation, and resource optimization, challenges "
    "remain in sample efficiency, reward specification, and safe exploration. We propose a unified "
    "taxonomy of RL algorithms and discuss promising research directions including offline RL, "
    "curriculum learning, and foundation models for decision-making. Experimental results across "
    "benchmark environments demonstrate that hybrid approaches combining model-based planning with "
    "model-free optimization achieve superior performance in terms of both sample efficiency and "
    "asymptotic reward."
)

def create_paper():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    doc = pymupdf.open()

    # ============ PAGE 1: Title, Authors, Abstract ============
    page = doc.new_page(width=W, height=H)
    y = 100
    page.insert_text(pymupdf.Point(306, y), "A Comprehensive Survey of Modern",
                     fontsize=20, fontname="hebo", color=(0, 0, 0),)
    y += 28
    page.insert_text(pymupdf.Point(306, y), "Reinforcement Learning Methods",
                     fontsize=20, fontname="hebo", color=(0, 0, 0),)

    # Center the title lines
    # Re-do with textbox for centering
    page = doc[0]  # get the page back
    # Clear and redo - actually let's just use coordinates carefully

    # Authors
    y = 170
    authors = "Wei Zhang, Sarah Chen, Raj Patel, Yuki Tanaka, and Michael O'Brien"
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), authors,
                     fontsize=11, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 18
    affiliation = "Department of Computer Science, Stanford University"
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), affiliation,
                     fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))
    y += 18
    email = "{wzhang, schen, rpatel, ytanaka, mobrien}@cs.stanford.edu"
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), email,
                     fontsize=9, fontname="cour", color=(0.3, 0.3, 0.3))

    y += 35

    # Abstract heading
    y = add_heading(page, y, "Abstract", fontsize=14, fontname="hebo")
    y = add_paragraph(page, y, ABSTRACT_TEXT, fontsize=10, fontname="tiit")

    y += 10
    # Keywords
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "Keywords: ", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_LEFT + 60, y),
                     "reinforcement learning, deep RL, policy gradient, Q-learning, multi-agent systems",
                     fontsize=10, fontname="tiro", color=(0, 0, 0))

    y += 30
    y = add_heading(page, y, "1. Introduction", fontsize=14)
    intro_text = (
        "The field of artificial intelligence has witnessed remarkable progress in recent years, "
        "driven largely by advances in deep learning and computational infrastructure. Among the "
        "various paradigms of machine learning, reinforcement learning (RL) stands out for its "
        "ability to learn optimal behavior through trial-and-error interaction with an environment. "
        "Unlike supervised learning, which requires labeled datasets, RL agents discover effective "
        "strategies by maximizing cumulative reward signals, making it particularly well-suited for "
        "sequential decision-making tasks."
    )
    y = add_paragraph(page, y, intro_text)

    intro_text2 = (
        "From mastering complex board games like Go and Chess to controlling robotic arms in "
        "manufacturing facilities, RL has demonstrated impressive capabilities across diverse domains. "
        "The integration of deep neural networks with RL algorithms, commonly referred to as deep "
        "reinforcement learning (deep RL), has dramatically expanded the scope of problems that can "
        "be addressed, enabling agents to operate directly from high-dimensional sensory inputs such "
        "as images and natural language."
    )
    y = add_paragraph(page, y, intro_text2)
    add_page_number(page, 1, 14)

    # ============ PAGE 2: Introduction continued + Background ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    intro_text3 = (
        "Despite these successes, significant challenges remain. Sample efficiency continues to be "
        "a primary concern, as many RL algorithms require millions of environment interactions to "
        "learn effective policies. The specification of reward functions that accurately capture desired "
        "behavior is another open problem, often requiring careful engineering and domain expertise. "
        "Furthermore, ensuring safe exploration during training is critical for real-world deployment, "
        "where catastrophic failures can have serious consequences."
    )
    y = add_paragraph(page, y, intro_text3)

    intro_text4 = (
        "This survey aims to provide a comprehensive overview of modern reinforcement learning methods. "
        "We organize our discussion around the fundamental algorithmic families, highlight key "
        "innovations that have shaped the field, and identify promising directions for future research. "
        "Our contributions include: (1) a unified taxonomy of RL algorithms covering both model-free "
        "and model-based approaches, (2) a detailed analysis of recent advances in multi-agent RL and "
        "transformer-based architectures, and (3) an empirical comparison across standard benchmark "
        "environments."
    )
    y = add_paragraph(page, y, intro_text4)

    y += 10
    y = add_heading(page, y, "2. Background and Preliminaries", fontsize=14)

    y = add_heading(page, y, "2.1 Markov Decision Processes", fontsize=12, fontname="hebo")
    mdp_text = (
        "The mathematical framework underlying most reinforcement learning algorithms is the Markov "
        "Decision Process (MDP). An MDP is defined as a tuple (S, A, P, R, gamma), where S is the state "
        "space, A is the action space, P: S x A x S -> [0,1] is the transition probability function, "
        "R: S x A -> R is the reward function, and gamma in [0,1) is the discount factor. The Markov "
        "property states that the future state depends only on the current state and action, independent "
        "of the history of previous states and actions."
    )
    y = add_paragraph(page, y, mdp_text)

    mdp_text2 = (
        "The goal of an RL agent is to find an optimal policy pi*: S -> A (or pi*: S x A -> [0,1] for "
        "stochastic policies) that maximizes the expected cumulative discounted reward, also known as "
        "the return: G_t = sum_{k=0}^{infinity} gamma^k * R_{t+k+1}. The state-value function V^pi(s) "
        "represents the expected return starting from state s and following policy pi, while the "
        "action-value function Q^pi(s,a) represents the expected return after taking action a in state s "
        "and subsequently following policy pi."
    )
    y = add_paragraph(page, y, mdp_text2)
    add_page_number(page, 2, 14)

    # ============ PAGE 3: Background continued ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "2.2 Bellman Equations", fontsize=12, fontname="hebo")
    bellman_text = (
        "The Bellman equations provide the recursive relationship that connects value functions across "
        "successive time steps. The Bellman expectation equation for the state-value function is: "
        "V^pi(s) = sum_a pi(a|s) * sum_{s'} P(s'|s,a) * [R(s,a) + gamma * V^pi(s')]. Similarly, for the "
        "action-value function: Q^pi(s,a) = sum_{s'} P(s'|s,a) * [R(s,a) + gamma * sum_{a'} pi(a'|s') * "
        "Q^pi(s',a')]. The Bellman optimality equations characterize the optimal value functions and form "
        "the basis for dynamic programming methods."
    )
    y = add_paragraph(page, y, bellman_text)

    y = add_heading(page, y, "2.3 Temporal Difference Learning", fontsize=12, fontname="hebo")
    td_text = (
        "Temporal difference (TD) learning combines ideas from Monte Carlo methods and dynamic programming. "
        "The simplest form, TD(0), updates the value estimate using the observed reward and the estimated "
        "value of the next state: V(s_t) <- V(s_t) + alpha * [R_{t+1} + gamma * V(s_{t+1}) - V(s_t)], "
        "where alpha is the learning rate. The term delta_t = R_{t+1} + gamma * V(s_{t+1}) - V(s_t) is "
        "known as the TD error. TD methods can learn directly from raw experience without a model of the "
        "environment's dynamics, and they update estimates based on other learned estimates without waiting "
        "for a final outcome (bootstrapping)."
    )
    y = add_paragraph(page, y, td_text)

    td_text2 = (
        "Eligibility traces provide a mechanism to bridge the gap between TD(0) and Monte Carlo methods. "
        "The TD(lambda) algorithm uses a trace parameter lambda in [0,1] to control the balance: when "
        "lambda=0, the algorithm reduces to TD(0), and when lambda=1, it becomes equivalent to Monte Carlo. "
        "In practice, intermediate values of lambda often perform best, combining the low variance of "
        "TD methods with the lower bias of Monte Carlo estimation. The n-step return formulation provides "
        "an alternative perspective, where the return is computed using n actual rewards before bootstrapping."
    )
    y = add_paragraph(page, y, td_text2)
    add_page_number(page, 3, 14)

    # ============ PAGE 4: Value-Based Methods ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "3. Value-Based Methods", fontsize=14)

    y = add_heading(page, y, "3.1 Q-Learning", fontsize=12, fontname="hebo")
    ql_text = (
        "Q-learning, introduced by Watkins in 1989, is an off-policy TD control algorithm that directly "
        "learns the optimal action-value function Q*. The update rule is: Q(s_t, a_t) <- Q(s_t, a_t) + "
        "alpha * [R_{t+1} + gamma * max_a Q(s_{t+1}, a) - Q(s_t, a_t)]. The key insight of Q-learning "
        "is that the target uses the maximum over actions in the next state, which corresponds to the "
        "greedy policy with respect to the current Q-values, regardless of the actual behavior policy "
        "used for exploration."
    )
    y = add_paragraph(page, y, ql_text)

    ql_text2 = (
        "The epsilon-greedy exploration strategy is commonly used with Q-learning: with probability "
        "epsilon, the agent selects a random action, and with probability 1-epsilon, it selects the "
        "action with the highest Q-value. The convergence of Q-learning to the optimal Q-function is "
        "guaranteed under certain conditions, including visiting all state-action pairs infinitely often "
        "and appropriate decay of the learning rate."
    )
    y = add_paragraph(page, y, ql_text2)

    y = add_heading(page, y, "3.2 Deep Q-Networks (DQN)", fontsize=12, fontname="hebo")
    dqn_text = (
        "The Deep Q-Network (DQN) algorithm, proposed by Mnih et al. in 2015, represents a breakthrough "
        "in combining deep learning with reinforcement learning. DQN uses a deep neural network to "
        "approximate the Q-function, taking raw pixel observations as input and outputting Q-values for "
        "each possible action. Two key innovations enable stable training: experience replay, which stores "
        "transitions in a buffer and samples mini-batches uniformly for training, breaking temporal "
        "correlations; and a target network, a slowly-updated copy of the Q-network used to compute "
        "stable TD targets."
    )
    y = add_paragraph(page, y, dqn_text)

    dqn_text2 = (
        "DQN achieved human-level performance on 29 of 49 Atari 2600 games, demonstrating that a single "
        "architecture could learn diverse skills directly from pixels. This landmark result spawned numerous "
        "improvements: Double DQN addresses overestimation bias by decoupling action selection from evaluation; "
        "Prioritized Experience Replay weights transitions by their TD error magnitude; Dueling DQN separates "
        "the value and advantage streams in the network architecture; and Rainbow combines six such extensions "
        "into a unified agent that significantly outperforms each individual component."
    )
    y = add_paragraph(page, y, dqn_text2)
    add_page_number(page, 4, 14)

    # ============ PAGE 5: Policy Gradient Methods ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "4. Policy Gradient Methods", fontsize=14)

    y = add_heading(page, y, "4.1 REINFORCE Algorithm", fontsize=12, fontname="hebo")
    reinforce_text = (
        "Policy gradient methods directly parameterize the policy pi_theta(a|s) and optimize the parameters "
        "theta by gradient ascent on the expected return. The policy gradient theorem establishes that "
        "the gradient of the objective J(theta) = E[G_0] can be expressed as: nabla_theta J(theta) = "
        "E[sum_t nabla_theta log pi_theta(a_t|s_t) * G_t]. The REINFORCE algorithm, proposed by Williams "
        "in 1992, estimates this gradient using Monte Carlo rollouts, updating parameters after complete "
        "episodes."
    )
    y = add_paragraph(page, y, reinforce_text)

    reinforce_text2 = (
        "A common variance reduction technique is to subtract a baseline from the return: "
        "nabla_theta J(theta) = E[sum_t nabla_theta log pi_theta(a_t|s_t) * (G_t - b(s_t))], where "
        "b(s_t) is typically a learned value function. This modification does not introduce bias but can "
        "significantly reduce the variance of gradient estimates, leading to faster and more stable learning. "
        "Despite its simplicity, REINFORCE suffers from high variance and is generally less sample-efficient "
        "than value-based methods."
    )
    y = add_paragraph(page, y, reinforce_text2)

    y = add_heading(page, y, "4.2 Actor-Critic Methods", fontsize=12, fontname="hebo")
    ac_text = (
        "Actor-Critic methods combine the advantages of policy gradient and value-based approaches by "
        "maintaining two separate function approximators: an actor that represents the policy and a critic "
        "that estimates the value function. The critic provides a lower-variance signal for policy updates "
        "compared to Monte Carlo returns. The Advantage Actor-Critic (A2C) algorithm uses the advantage "
        "function A(s,a) = Q(s,a) - V(s) to reduce variance while maintaining an unbiased gradient estimate."
    )
    y = add_paragraph(page, y, ac_text)

    ac_text2 = (
        "Asynchronous Advantage Actor-Critic (A3C) extends A2C by running multiple agents in parallel "
        "across different environment instances, each computing gradients independently and asynchronously "
        "updating shared parameters. This parallelization provides natural exploration through policy "
        "diversity and significantly reduces training time. Generalized Advantage Estimation (GAE) offers "
        "a principled way to trade off bias and variance in advantage estimation through an exponentially-"
        "weighted sum of n-step advantage estimates."
    )
    y = add_paragraph(page, y, ac_text2)
    add_page_number(page, 5, 14)

    # ============ PAGE 6: PPO and TRPO ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "4.3 Trust Region Methods", fontsize=12, fontname="hebo")
    trpo_text = (
        "Trust Region Policy Optimization (TRPO) addresses the instability of standard policy gradient "
        "methods by constraining policy updates to a trust region. TRPO maximizes a surrogate objective "
        "subject to a KL-divergence constraint: maximize E[pi_theta(a|s)/pi_theta_old(a|s) * A(s,a)] "
        "subject to E[KL(pi_theta_old || pi_theta)] <= delta. This constraint ensures that the new "
        "policy does not deviate too far from the old policy, preventing catastrophically large updates."
    )
    y = add_paragraph(page, y, trpo_text)

    y = add_heading(page, y, "4.4 Proximal Policy Optimization (PPO)", fontsize=12, fontname="hebo")
    ppo_text = (
        "Proximal Policy Optimization (PPO), proposed by Schulman et al. in 2017, simplifies the trust "
        "region approach by using a clipped surrogate objective. The PPO-Clip objective is: "
        "L(theta) = E[min(r_t(theta) * A_t, clip(r_t(theta), 1-epsilon, 1+epsilon) * A_t)], where "
        "r_t(theta) = pi_theta(a_t|s_t) / pi_theta_old(a_t|s_t) is the probability ratio. The clipping "
        "mechanism prevents excessive policy changes without the computational overhead of constrained "
        "optimization."
    )
    y = add_paragraph(page, y, ppo_text)

    ppo_text2 = (
        "PPO has become one of the most widely used RL algorithms due to its simplicity, generality, and "
        "robust performance. It serves as the default algorithm in many RL frameworks and has been "
        "successfully applied to diverse problems including game playing, robotic locomotion, natural "
        "language generation (via RLHF), and autonomous driving. The algorithm typically uses multiple "
        "epochs of mini-batch SGD on the surrogate objective, further improving sample efficiency."
    )
    y = add_paragraph(page, y, ppo_text2)

    y += 10
    y = add_heading(page, y, "5. Model-Based Reinforcement Learning", fontsize=14)
    mb_text = (
        "Model-based RL algorithms learn a model of the environment dynamics and use it for planning "
        "or generating synthetic experience. The key advantage is improved sample efficiency, as the "
        "learned model can be queried without actual environment interaction. World models, such as those "
        "proposed by Ha and Schmidhuber, learn compact latent representations of the environment and "
        "train policies within the learned model. Dreamer extends this approach by learning actions and "
        "values purely within a learned latent space."
    )
    y = add_paragraph(page, y, mb_text)
    add_page_number(page, 6, 14)

    # ============ PAGE 7: Model-Based RL continued ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "5.1 Dyna Architecture", fontsize=12, fontname="hebo")
    dyna_text = (
        "The Dyna architecture, proposed by Sutton in 1991, provides a general framework for integrating "
        "model-based and model-free learning. In Dyna, the agent simultaneously learns a policy from real "
        "experience and uses a learned model to generate simulated experience for additional policy updates. "
        "This approach can dramatically improve sample efficiency: for every real transition, the agent can "
        "perform multiple model-based planning steps, effectively amplifying the value of each real "
        "interaction."
    )
    y = add_paragraph(page, y, dyna_text)

    y = add_heading(page, y, "5.2 Monte Carlo Tree Search", fontsize=12, fontname="hebo")
    mcts_text = (
        "Monte Carlo Tree Search (MCTS) is a planning algorithm that builds a search tree by repeatedly "
        "simulating trajectories from the current state. Each simulation consists of four phases: selection "
        "(traversing the tree using UCB1 or similar criteria), expansion (adding a new node), rollout "
        "(simulating to terminal state using a default policy), and backpropagation (updating statistics "
        "along the path). AlphaGo and AlphaZero combine MCTS with deep neural networks that provide "
        "both policy priors and value estimates, replacing random rollouts with learned evaluations."
    )
    y = add_paragraph(page, y, mcts_text)

    y = add_heading(page, y, "5.3 MuZero and Model Predictive Control", fontsize=12, fontname="hebo")
    muzero_text = (
        "MuZero, developed by DeepMind, extends AlphaZero by learning a model that predicts rewards, "
        "values, and policies without requiring knowledge of the game rules or environment dynamics. "
        "The model operates in a learned latent space, predicting the consequences of actions without "
        "reconstructing full observations. This approach achieves superhuman performance in Atari, Go, "
        "chess, and shogi while maintaining the benefits of planning. Model Predictive Control (MPC) "
        "approaches use the learned model to optimize short-horizon action sequences at each time step."
    )
    y = add_paragraph(page, y, muzero_text)

    mb_challenges = (
        "A fundamental challenge in model-based RL is model error: inaccuracies in the learned model "
        "can compound over multi-step predictions, leading to poor policy performance. Approaches to "
        "mitigate this include ensemble methods for uncertainty estimation, short planning horizons, "
        "model-based policy optimization that explicitly accounts for model uncertainty, and hybrid "
        "approaches that combine model-based planning with model-free fine-tuning."
    )
    y = add_paragraph(page, y, mb_challenges)
    add_page_number(page, 7, 14)

    # ============ PAGE 8: Multi-Agent RL ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "6. Multi-Agent Reinforcement Learning", fontsize=14)
    marl_text = (
        "Multi-agent reinforcement learning (MARL) extends the single-agent RL framework to settings "
        "with multiple interacting agents. The presence of other learning agents makes the environment "
        "non-stationary from each agent's perspective, violating the stationarity assumptions underlying "
        "most single-agent algorithms. MARL problems can be categorized as fully cooperative, fully "
        "competitive, or mixed (general-sum games)."
    )
    y = add_paragraph(page, y, marl_text)

    y = add_heading(page, y, "6.1 Cooperative Methods", fontsize=12, fontname="hebo")
    coop_text = (
        "In cooperative settings, agents share a common reward and must coordinate to maximize team "
        "performance. Centralized Training with Decentralized Execution (CTDE) is the dominant paradigm, "
        "where agents have access to global information during training but act based on local observations "
        "during execution. QMIX decomposes the joint Q-function into individual agent Q-functions subject "
        "to a monotonicity constraint, enabling tractable joint action selection. MAPPO applies PPO in "
        "the multi-agent setting with shared parameters and has shown surprisingly strong performance."
    )
    y = add_paragraph(page, y, coop_text)

    y = add_heading(page, y, "6.2 Competitive and Mixed Settings", fontsize=12, fontname="hebo")
    comp_text = (
        "Competitive MARL is often formulated as finding Nash equilibria in multi-player games. "
        "Self-play, where agents train against copies of themselves, has been remarkably successful in "
        "games like Go, StarCraft, and Dota 2. Fictitious play maintains a belief model of opponents "
        "based on their historical action frequencies. Population-based training evolves a diverse "
        "population of agents, promoting robustness through exposure to varied strategies. League "
        "training, as used in AlphaStar, maintains a league of diverse agents at different skill levels."
    )
    y = add_paragraph(page, y, comp_text)

    comm_text = (
        "Communication between agents is a key research area in cooperative MARL. Learned communication "
        "protocols allow agents to share information through discrete or continuous message channels. "
        "CommNet uses a continuous communication channel with mean-pooled messages, while TarMAC introduces "
        "attention-based targeted communication. RIAL and DIAL explore reinforced and differentiable "
        "inter-agent learning respectively, enabling agents to develop emergent communication strategies "
        "through end-to-end training."
    )
    y = add_paragraph(page, y, comm_text)
    add_page_number(page, 8, 14)

    # ============ PAGE 9: Transformer-based RL ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "7. Transformer Architectures for RL", fontsize=14)
    trans_text = (
        "The remarkable success of transformer architectures in natural language processing has inspired "
        "their application to reinforcement learning. Decision Transformer, proposed by Chen et al. in "
        "2021, reformulates RL as a sequence modeling problem: given a desired return, the model autoregressively "
        "generates actions conditioned on the trajectory history and a return-to-go token. This approach "
        "bypasses traditional RL optimization entirely, instead leveraging the pattern-matching capabilities "
        "of transformers trained via supervised learning on offline datasets."
    )
    y = add_paragraph(page, y, trans_text)

    gato_text = (
        "Gato, developed by DeepMind, demonstrates that a single transformer can serve as a generalist "
        "agent across hundreds of tasks spanning different modalities and embodiments. By tokenizing "
        "observations, actions, and rewards into a unified sequence format, Gato learns to play Atari "
        "games, caption images, chat, and control robotic arms using the same network weights. This "
        "multi-task approach suggests that scaling transformer architectures with diverse experience "
        "data could lead to increasingly capable generalist agents."
    )
    y = add_paragraph(page, y, gato_text)

    y = add_heading(page, y, "7.1 Offline RL with Transformers", fontsize=12, fontname="hebo")
    offline_text = (
        "Offline RL, also known as batch RL, learns policies exclusively from a fixed dataset of "
        "previously collected experience without further environment interaction. This setting is "
        "particularly relevant for real-world applications where online data collection is expensive "
        "or risky. Conservative Q-Learning (CQL) addresses the distribution shift problem by adding "
        "a regularizer that penalizes Q-values for out-of-distribution actions. Trajectory Transformer "
        "applies beam search over discretized trajectories, treating RL as a planning problem in "
        "sequence space."
    )
    y = add_paragraph(page, y, offline_text)

    offline_text2 = (
        "Recent work has explored the connection between large language models and decision-making. "
        "Models pretrained on internet-scale text data exhibit zero-shot reasoning capabilities that "
        "can be leveraged for planning and problem-solving. Chain-of-thought prompting enables LLMs "
        "to break complex tasks into manageable steps, while tools like SayCan ground language models "
        "in robotic affordances to generate feasible action plans."
    )
    y = add_paragraph(page, y, offline_text2)
    add_page_number(page, 9, 14)

    # ============ PAGE 10: Applications ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "8. Applications", fontsize=14)

    y = add_heading(page, y, "8.1 Game Playing", fontsize=12, fontname="hebo")
    games_text = (
        "Reinforcement learning has achieved superhuman performance in numerous game domains. AlphaGo "
        "and its successors demonstrated mastery of Go, chess, and shogi through self-play. OpenAI Five "
        "defeated world champions in Dota 2, a complex real-time strategy game with imperfect information "
        "and long time horizons. Agent57 was the first to achieve super-human performance on all 57 Atari "
        "games in the Arcade Learning Environment. These achievements showcase RL's ability to discover "
        "novel strategies in complex environments."
    )
    y = add_paragraph(page, y, games_text)

    y = add_heading(page, y, "8.2 Robotics", fontsize=12, fontname="hebo")
    robotics_text = (
        "RL has enabled significant advances in robotic manipulation and locomotion. Sim-to-real transfer "
        "trains policies in simulation and deploys them on physical robots, with domain randomization "
        "improving robustness to the reality gap. Dexterous hand manipulation has progressed from simple "
        "grasping to complex tasks like Rubik's cube solving. Legged locomotion policies trained with "
        "RL enable quadrupedal and bipedal robots to traverse challenging terrain, recover from "
        "perturbations, and adapt to novel environments."
    )
    y = add_paragraph(page, y, robotics_text)

    y = add_heading(page, y, "8.3 Natural Language Processing", fontsize=12, fontname="hebo")
    nlp_text = (
        "Reinforcement Learning from Human Feedback (RLHF) has emerged as a crucial technique for "
        "aligning large language models with human preferences. The process involves training a reward "
        "model from human comparisons of model outputs, then fine-tuning the language model using PPO "
        "to maximize the learned reward while staying close to the original model. This approach was "
        "instrumental in developing ChatGPT and has become standard practice for instruction-following "
        "and safety alignment in modern LLMs."
    )
    y = add_paragraph(page, y, nlp_text)

    y = add_heading(page, y, "8.4 Resource Optimization", fontsize=12, fontname="hebo")
    resource_text = (
        "RL has been successfully applied to resource optimization in data centers, network routing, "
        "chip placement, and compiler optimization. DeepMind's work on data center cooling reduced "
        "energy consumption by 40%. RL-based chip placement generates layouts competitive with human "
        "experts in significantly less time. In network optimization, RL agents learn to route traffic "
        "dynamically based on current network conditions, reducing latency and improving throughput."
    )
    y = add_paragraph(page, y, resource_text)
    add_page_number(page, 10, 14)

    # ============ PAGE 11: Challenges ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "9. Open Challenges", fontsize=14)

    y = add_heading(page, y, "9.1 Sample Efficiency", fontsize=12, fontname="hebo")
    sample_text = (
        "Despite significant improvements, sample efficiency remains a critical bottleneck for "
        "real-world RL applications. State-of-the-art algorithms often require millions or billions "
        "of environment steps to learn effective policies. Data augmentation, representation learning, "
        "and meta-learning offer promising avenues for reducing data requirements. Hindsight Experience "
        "Replay (HER) improves efficiency in sparse reward settings by retroactively relabeling failed "
        "trajectories with achieved goals."
    )
    y = add_paragraph(page, y, sample_text)

    y = add_heading(page, y, "9.2 Reward Specification", fontsize=12, fontname="hebo")
    reward_text = (
        "Designing reward functions that faithfully capture desired behavior is a persistent challenge. "
        "Reward hacking occurs when agents find unintended ways to maximize reward without achieving the "
        "intended objective. Inverse RL infers reward functions from expert demonstrations, while reward "
        "modeling learns rewards from human preferences. Constitutional AI approaches use self-critique "
        "and revision to reduce reliance on human feedback while maintaining alignment."
    )
    y = add_paragraph(page, y, reward_text)

    y = add_heading(page, y, "9.3 Safe Exploration", fontsize=12, fontname="hebo")
    safe_text = (
        "In safety-critical domains such as autonomous driving, healthcare, and industrial control, "
        "ensuring safe exploration during training is paramount. Constrained MDPs formalize safety "
        "requirements as constraints on expected costs. Safe RL methods include Lagrangian approaches "
        "that convert constraints into penalty terms, shielding mechanisms that override unsafe actions, "
        "and formal verification techniques that provide probabilistic safety guarantees. The tension "
        "between exploration and safety remains an active area of research."
    )
    y = add_paragraph(page, y, safe_text)

    y = add_heading(page, y, "9.4 Generalization and Transfer", fontsize=12, fontname="hebo")
    gen_text = (
        "RL agents often struggle to generalize beyond their training environments. Procedural content "
        "generation creates diverse training environments to promote robustness. Curriculum learning "
        "structures the training process by gradually increasing task difficulty. Contextual policies "
        "condition behavior on task descriptions, enabling zero-shot transfer to new tasks. Foundation "
        "models for decision-making aim to leverage broad pretraining to enable rapid adaptation to "
        "new environments with minimal fine-tuning."
    )
    y = add_paragraph(page, y, gen_text)
    add_page_number(page, 11, 14)

    # ============ PAGE 12: Experimental Results ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "10. Experimental Comparison", fontsize=14)
    exp_intro = (
        "To provide a concrete comparison of the discussed algorithms, we evaluate representative "
        "methods across four standard benchmark environments: CartPole-v1, LunarLander-v2, "
        "HalfCheetah-v3, and a custom multi-agent cooperative task. Each algorithm was trained for "
        "1 million environment steps with three random seeds, and we report mean reward with "
        "standard deviation."
    )
    y = add_paragraph(page, y, exp_intro)

    y += 5
    # Table header
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Table 1: Performance comparison across benchmark environments",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 20

    # Draw a simple table
    table_data = [
        ["Algorithm", "CartPole", "LunarLander", "HalfCheetah", "CoopTask"],
        ["DQN", "500.0 +/- 0.0", "198.3 +/- 12.1", "N/A", "N/A"],
        ["PPO", "500.0 +/- 0.0", "243.7 +/- 8.4", "4832.1 +/- 341", "87.3 +/- 4.2"],
        ["SAC", "500.0 +/- 0.0", "251.2 +/- 6.9", "5290.4 +/- 278", "91.6 +/- 3.8"],
        ["TRPO", "498.2 +/- 3.1", "231.4 +/- 11.2", "4521.3 +/- 412", "82.1 +/- 5.7"],
        ["A3C", "497.8 +/- 4.5", "218.6 +/- 14.3", "4102.8 +/- 389", "79.4 +/- 6.1"],
        ["Dreamer", "500.0 +/- 0.0", "247.8 +/- 7.2", "5487.2 +/- 302", "89.8 +/- 3.5"],
        ["DT", "489.3 +/- 8.7", "215.4 +/- 16.8", "4987.3 +/- 356", "84.2 +/- 5.1"],
    ]

    col_widths = [80, 95, 95, 95, 80]
    row_height = 18
    x_start = MARGIN_LEFT
    for row_idx, row in enumerate(table_data):
        x = x_start
        for col_idx, cell in enumerate(row):
            fn = "hebo" if row_idx == 0 else "tiro"
            fs = 9 if row_idx == 0 else 8
            page.insert_text(pymupdf.Point(x + 3, y + 12), cell,
                             fontsize=fs, fontname=fn, color=(0, 0, 0))
            x += col_widths[col_idx]
        # Draw horizontal line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(x_start, y), pymupdf.Point(x_start + sum(col_widths), y))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()
        y += row_height
    # Bottom line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(x_start, y), pymupdf.Point(x_start + sum(col_widths), y))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()

    y += 20
    analysis = (
        "The results demonstrate several key findings. First, model-based methods (Dreamer) achieve "
        "competitive or superior performance while requiring significantly fewer environment interactions. "
        "Second, PPO and SAC consistently perform well across all environments, confirming their status "
        "as reliable general-purpose algorithms. Third, the Decision Transformer achieves strong results "
        "on some tasks using offline data alone, though it underperforms online methods in environments "
        "requiring extensive exploration."
    )
    y = add_paragraph(page, y, analysis)

    analysis2 = (
        "In the cooperative multi-agent task, SAC-based methods with centralized critics achieve the "
        "highest scores, followed closely by Dreamer with a shared world model. The performance gap "
        "between cooperative and independent learning highlights the importance of explicit coordination "
        "mechanisms in multi-agent settings."
    )
    y = add_paragraph(page, y, analysis2)
    add_page_number(page, 12, 14)

    # ============ PAGE 13: Future Directions ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "11. Future Directions", fontsize=14)

    y = add_heading(page, y, "11.1 Foundation Models for Decision-Making", fontsize=12, fontname="hebo")
    fm_text = (
        "The convergence of large language models and RL is creating new paradigms for decision-making. "
        "Foundation models pretrained on diverse internet data possess broad world knowledge that can be "
        "leveraged for planning, reasoning, and tool use. We envision a future where RL fine-tuning of "
        "foundation models enables rapid adaptation to new tasks with minimal environment interaction, "
        "similar to how few-shot learning works in NLP."
    )
    y = add_paragraph(page, y, fm_text)

    y = add_heading(page, y, "11.2 Hierarchical and Goal-Conditioned RL", fontsize=12, fontname="hebo")
    hier_text = (
        "Hierarchical RL addresses the challenge of long-horizon tasks by decomposing them into "
        "subgoals. Option frameworks define temporally extended actions with initiation sets, policies, "
        "and termination conditions. Goal-conditioned policies learn to reach arbitrary goal states, "
        "enabling compositional generalization. The HAM (Hierarchy of Abstract Machines) and MAXQ "
        "frameworks provide formal foundations for hierarchical task decomposition."
    )
    y = add_paragraph(page, y, hier_text)

    y = add_heading(page, y, "11.3 RL for Scientific Discovery", fontsize=12, fontname="hebo")
    sci_text = (
        "Reinforcement learning is increasingly being applied to accelerate scientific discovery. "
        "In drug design, RL agents learn to generate molecular structures with desired properties. "
        "In materials science, RL optimizes the composition and processing of novel materials. "
        "AlphaFold's success in protein structure prediction, while primarily supervised, has inspired "
        "RL-based approaches to protein design and enzyme engineering. Climate modeling and energy "
        "system optimization represent additional high-impact application areas."
    )
    y = add_paragraph(page, y, sci_text)

    y = add_heading(page, y, "11.4 Ethical Considerations", fontsize=12, fontname="hebo")
    ethics_text = (
        "As RL agents become more capable and widely deployed, ethical considerations become increasingly "
        "important. Issues include the potential for RL systems to discover and exploit loopholes in "
        "reward specifications, the challenge of ensuring fairness when RL agents make decisions affecting "
        "individuals, and the concentration of RL capabilities in large organizations with significant "
        "computational resources. Establishing standards for responsible RL development and deployment "
        "is an important ongoing effort."
    )
    y = add_paragraph(page, y, ethics_text)
    add_page_number(page, 13, 14)

    # ============ PAGE 14: Conclusion and References ============
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP
    y = add_heading(page, y, "12. Conclusion", fontsize=14)
    conclusion = (
        "This survey has presented a comprehensive overview of modern reinforcement learning methods, "
        "spanning value-based, policy gradient, model-based, multi-agent, and transformer-based approaches. "
        "The field has made remarkable progress, from mastering complex games to enabling real-world "
        "applications in robotics, NLP, and resource optimization. However, significant challenges remain "
        "in sample efficiency, reward specification, safe exploration, and generalization. We believe that "
        "the convergence of RL with foundation models, combined with advances in hierarchical learning "
        "and improved theoretical understanding, will drive the next wave of breakthroughs in autonomous "
        "decision-making."
    )
    y = add_paragraph(page, y, conclusion)

    y += 15
    y = add_heading(page, y, "References", fontsize=14)
    refs = [
        "[1] Sutton, R.S. and Barto, A.G. (2018). Reinforcement Learning: An Introduction. MIT Press.",
        "[2] Mnih, V. et al. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540).",
        "[3] Silver, D. et al. (2017). Mastering the game of Go without human knowledge. Nature, 550(7676).",
        "[4] Schulman, J. et al. (2017). Proximal Policy Optimization Algorithms. arXiv:1707.06347.",
        "[5] Haarnoja, T. et al. (2018). Soft Actor-Critic. ICML 2018.",
        "[6] Chen, L. et al. (2021). Decision Transformer. NeurIPS 2021.",
        "[7] Schrittwieser, J. et al. (2020). Mastering Atari, Go, Chess and Shogi by Planning. Nature, 588.",
        "[8] Ouyang, L. et al. (2022). Training language models to follow instructions with RLHF. NeurIPS.",
        "[9] Ha, D. and Schmidhuber, J. (2018). World Models. arXiv:1803.10122.",
        "[10] Vinyals, O. et al. (2019). Grandmaster level in StarCraft II using multi-agent RL. Nature, 575.",
        "[11] Reed, S. et al. (2022). A Generalist Agent. arXiv:2205.06175.",
        "[12] Yu, C. et al. (2022). The Surprising Effectiveness of PPO in Cooperative MARL. NeurIPS.",
        "[13] Hafner, D. et al. (2023). Mastering Diverse Domains through World Models. arXiv:2301.04104.",
        "[14] Rashid, T. et al. (2018). QMIX: Monotonic Value Function Factorisation for MARL. ICML.",
    ]
    for ref in refs:
        rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 30)
        page.insert_textbox(rect, ref, fontsize=8, fontname="tiro", color=(0, 0, 0))
        y += 22

    add_page_number(page, 14, 14)

    # ============ SET TOC ============
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 1],
        [1, "2. Background and Preliminaries", 2],
        [2, "2.1 Markov Decision Processes", 2],
        [2, "2.2 Bellman Equations", 3],
        [2, "2.3 Temporal Difference Learning", 3],
        [1, "3. Value-Based Methods", 4],
        [2, "3.1 Q-Learning", 4],
        [2, "3.2 Deep Q-Networks (DQN)", 4],
        [1, "4. Policy Gradient Methods", 5],
        [2, "4.1 REINFORCE Algorithm", 5],
        [2, "4.2 Actor-Critic Methods", 5],
        [2, "4.3 Trust Region Methods", 6],
        [2, "4.4 Proximal Policy Optimization (PPO)", 6],
        [1, "5. Model-Based Reinforcement Learning", 6],
        [2, "5.1 Dyna Architecture", 7],
        [2, "5.2 Monte Carlo Tree Search", 7],
        [2, "5.3 MuZero and Model Predictive Control", 7],
        [1, "6. Multi-Agent Reinforcement Learning", 8],
        [2, "6.1 Cooperative Methods", 8],
        [2, "6.2 Competitive and Mixed Settings", 8],
        [1, "7. Transformer Architectures for RL", 9],
        [2, "7.1 Offline RL with Transformers", 9],
        [1, "8. Applications", 10],
        [2, "8.1 Game Playing", 10],
        [2, "8.2 Robotics", 10],
        [2, "8.3 Natural Language Processing", 10],
        [2, "8.4 Resource Optimization", 10],
        [1, "9. Open Challenges", 11],
        [2, "9.1 Sample Efficiency", 11],
        [2, "9.2 Reward Specification", 11],
        [2, "9.3 Safe Exploration", 11],
        [2, "9.4 Generalization and Transfer", 11],
        [1, "10. Experimental Comparison", 12],
        [1, "11. Future Directions", 13],
        [2, "11.1 Foundation Models for Decision-Making", 13],
        [2, "11.2 Hierarchical and Goal-Conditioned RL", 13],
        [2, "11.3 RL for Scientific Discovery", 13],
        [2, "11.4 Ethical Considerations", 13],
        [1, "12. Conclusion", 14],
        [1, "References", 14],
    ]
    doc.set_toc(toc)

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 14')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_paper()
