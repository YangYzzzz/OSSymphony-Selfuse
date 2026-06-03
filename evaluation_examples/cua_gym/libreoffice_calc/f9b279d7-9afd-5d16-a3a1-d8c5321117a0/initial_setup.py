"""
Initial Setup: Create a 12-page two-column academic research paper PDF
Task ID: pdf_gf1_016
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
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_016'
OUTPUT = f'{DOCUMENTS}/research_paper.pdf'


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


# --- Academic paper content ---

TITLE = "Deep Reinforcement Learning for Adaptive Traffic Signal Control: A Multi-Agent Approach"
AUTHORS = "Elena Vasquez, Rajesh Patel, Yuki Tanaka, and Marcus O'Brien"
AFFILIATION = "Department of Computer Science, Stanford University, Stanford, CA 94305"
JOURNAL = "IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 3, March 2025"

ABSTRACT = (
    "Traffic congestion remains one of the most pressing challenges in urban mobility, "
    "costing billions of dollars annually in lost productivity and increased emissions. "
    "Traditional traffic signal control systems rely on fixed-time plans or simple actuated "
    "controllers that cannot adapt to dynamic traffic patterns. In this paper, we propose "
    "a multi-agent deep reinforcement learning (MADRL) framework for adaptive traffic signal "
    "control that coordinates multiple intersections simultaneously. Our approach employs "
    "a decentralized execution with centralized training paradigm, where each intersection "
    "agent learns a local policy while sharing information through a graph attention network. "
    "We introduce a novel reward shaping mechanism that balances throughput maximization with "
    "fairness constraints across competing traffic streams. Extensive experiments on both "
    "synthetic grid networks and a calibrated model of downtown San Francisco demonstrate "
    "that our method reduces average vehicle delay by 23.7% compared to the best-performing "
    "baseline and achieves a 15.2% reduction in total CO2 emissions. Furthermore, we show "
    "that our framework generalizes to unseen traffic demand patterns and scales effectively "
    "to networks with over 100 intersections. The results suggest that multi-agent reinforcement "
    "learning offers a viable path toward intelligent, adaptive urban traffic management systems."
)

INTRODUCTION = [
    "Urban traffic congestion is a pervasive problem affecting cities worldwide. According to "
    "the Texas Transportation Institute, American commuters spent an average of 54 extra hours "
    "in traffic in 2023, resulting in $87.1 billion in combined time and fuel costs [1]. Beyond "
    "economic losses, traffic congestion contributes significantly to greenhouse gas emissions, "
    "with transportation accounting for approximately 29% of total U.S. carbon emissions [2]. "
    "Effective traffic signal control is among the most cost-efficient interventions for "
    "mitigating urban congestion, as it leverages existing infrastructure without requiring "
    "major capital investments.",

    "Traditional approaches to traffic signal control can be broadly categorized into three groups: "
    "fixed-time control, actuated control, and adaptive control systems. Fixed-time controllers "
    "operate on pre-computed signal timing plans optimized for historical demand patterns using "
    "tools such as TRANSYT-7F [3] or Synchro [4]. While computationally simple, these systems "
    "cannot respond to real-time fluctuations in traffic demand. Actuated controllers use loop "
    "detectors or video sensors to extend green phases based on vehicle presence, offering limited "
    "responsiveness to local conditions [5]. Centralized adaptive systems like SCOOT [6] and "
    "SCATS [7] adjust signal timings in real time using sensor data, but their performance "
    "degrades in highly variable demand scenarios and they require significant calibration effort.",

    "Recent advances in deep reinforcement learning (DRL) have opened new possibilities for "
    "traffic signal control. Unlike model-based optimization approaches, DRL agents learn "
    "control policies directly from interaction with the traffic environment, potentially "
    "capturing complex nonlinear dynamics that are difficult to model analytically. Several "
    "studies have demonstrated promising results using single-agent DRL for isolated intersection "
    "control [8, 9, 10]. However, extending these approaches to network-level control remains "
    "challenging due to the exponential growth of the joint state-action space and the need "
    "for coordination among neighboring intersections.",

    "In this paper, we address these challenges by proposing a Multi-Agent Deep Reinforcement "
    "Learning (MADRL) framework that combines decentralized execution with centralized training. "
    "Each intersection is controlled by an independent agent that observes local traffic conditions "
    "and selects signal phases accordingly. During training, agents share observations through "
    "a graph attention network (GAT) [11] that captures spatial dependencies in the road network. "
    "We introduce a novel reward function that combines throughput maximization with explicit "
    "fairness constraints, ensuring that no individual traffic stream is disproportionately "
    "penalized. Our contributions are as follows: (1) a scalable MADRL architecture for "
    "network-level traffic signal control, (2) a fairness-aware reward shaping mechanism, "
    "(3) comprehensive evaluation on both synthetic and real-world network topologies, and "
    "(4) analysis of generalization to unseen demand scenarios.",
]

METHODS = [
    "We formulate the traffic signal control problem as a decentralized partially observable "
    "Markov decision process (Dec-POMDP). Each intersection i in the network is controlled by "
    "an agent that observes a local state s_i consisting of queue lengths, current phase, "
    "elapsed time, and upstream traffic flow estimates. The action space for each agent "
    "corresponds to selecting one of K predefined signal phases, where K varies by intersection "
    "geometry (typically K = 4 for a standard four-way intersection). The transition dynamics "
    "are governed by the microscopic traffic simulator SUMO (Simulation of Urban Mobility) [12].",

    "Our architecture employs a Proximal Policy Optimization (PPO) [13] backbone for each "
    "agent, augmented with a graph attention mechanism for inter-agent communication. The "
    "observation encoder consists of a three-layer MLP with hidden dimensions [128, 64, 32] "
    "and ReLU activations. The graph attention module operates on the road network topology "
    "G = (V, E), where V represents intersections and E represents road segments connecting "
    "them. Each agent aggregates information from its k-hop neighborhood using multi-head "
    "attention with 4 heads and a 32-dimensional embedding per head.",

    "The reward function for agent i at time step t is defined as: r_i(t) = -alpha * D_i(t) "
    "- beta * max(W_j(t)) + gamma * T_i(t), where D_i(t) is the average delay at intersection "
    "i, W_j(t) is the maximum waiting time across all approaches j, T_i(t) is the throughput "
    "(vehicles cleared per cycle), and alpha, beta, gamma are weighting coefficients. The "
    "second term introduces an explicit fairness constraint by penalizing the maximum waiting "
    "time across approaches rather than the average, discouraging policies that starve minor "
    "streets in favor of arterial throughput.",

    "Training proceeds in episodes of 3600 simulation seconds (one hour). We use a centralized "
    "critic that receives the joint observation of all agents within a 3-hop radius, while the "
    "actors (policy networks) operate only on local observations augmented with GAT-aggregated "
    "features. The learning rate is set to 3e-4 with linear decay over 500 episodes. We employ "
    "a clip ratio of 0.2 for PPO, a discount factor of 0.99, and update the policy every 2048 "
    "time steps. Gradient norms are clipped at 0.5 to ensure training stability.",

    "For the traffic simulation environment, we use SUMO version 1.18.0 with a simulation step "
    "size of 1 second. Vehicle arrivals follow a Poisson process with time-varying rates derived "
    "from real-world traffic count data. We model three vehicle types: passenger cars (85%), "
    "buses (5%), and trucks (10%), each with distinct acceleration, deceleration, and gap "
    "acceptance parameters. Yellow and all-red clearance intervals follow MUTCD guidelines [14] "
    "with 3-second yellow and 2-second all-red phases.",
]

RESULTS = [
    "We evaluate our MADRL framework on three network configurations of increasing complexity. "
    "The first is a synthetic 4x4 grid network with uniform intersection geometry, serving as "
    "a controlled benchmark. The second is a 6x6 grid with heterogeneous intersection types "
    "(including T-intersections and five-way junctions). The third is a calibrated model of a "
    "25-intersection corridor in downtown San Francisco, reconstructed from OpenStreetMap data "
    "and calibrated against loop detector counts from the Performance Measurement System (PeMS).",

    "Table 1 summarizes the performance metrics across all three networks. On the 4x4 grid, "
    "our method achieves an average vehicle delay of 18.3 seconds, compared to 24.0 seconds "
    "for the fixed-time baseline (a 23.7% reduction) and 21.5 seconds for the best single-agent "
    "DRL baseline (a 14.9% reduction). The improvement is more pronounced during peak hours, "
    "where our method reduces delay by 31.2% compared to fixed-time control. Notably, the "
    "fairness metric (maximum approach delay ratio) improves from 3.41 under fixed-time to "
    "1.87 under our method, indicating more equitable treatment of competing traffic streams.",

    "On the San Francisco network, our method reduces average delay from 42.7 seconds (fixed-time) "
    "to 32.5 seconds (23.9% reduction) and total network CO2 emissions from 847 kg/hr to "
    "718 kg/hr (15.2% reduction). The emission reduction is attributed to smoother traffic "
    "progression and reduced stop-and-go cycles. Figure 3 shows the spatial distribution of "
    "delay improvements across the network, revealing that the largest gains occur at "
    "intersections with high demand asymmetry.",

    "To assess generalization, we train agents on demand patterns from weekday AM peak "
    "(7:00-9:00) and evaluate on PM peak (16:00-18:00), weekend, and special event scenarios. "
    "Table 2 shows that while performance degrades slightly on unseen patterns, our method "
    "consistently outperforms baselines. The transfer gap is smallest for PM peak (4.2% "
    "performance degradation relative to trained-on scenarios) and largest for special events "
    "(11.8% degradation), suggesting that the learned policies capture generalizable traffic "
    "management principles rather than overfitting to specific demand distributions.",

    "Scalability analysis on grid networks ranging from 2x2 to 12x12 intersections reveals "
    "that our method maintains stable performance up to approximately 100 intersections, beyond "
    "which the communication overhead of the GAT module begins to impact training convergence. "
    "We address this through a hierarchical decomposition approach where the network is "
    "partitioned into clusters of 16-25 intersections, each managed by an independent MADRL "
    "instance with inter-cluster coordination through boundary agents. This extension enables "
    "scaling to networks with over 400 intersections with less than 3% performance degradation "
    "compared to the monolithic approach.",
]

DISCUSSION = [
    "Our results demonstrate that multi-agent deep reinforcement learning offers significant "
    "advantages over both traditional and single-agent approaches for network-level traffic "
    "signal control. The key insight is that explicit modeling of inter-agent dependencies "
    "through graph attention networks enables coordinated behavior to emerge naturally during "
    "training, without the need for hand-crafted coordination rules or centralized optimization.",

    "The fairness-aware reward function proves to be a critical design choice. Without the "
    "fairness term, agents tend to converge on policies that maximize arterial throughput at "
    "the expense of side-street traffic, leading to excessively long waits for vehicles on "
    "minor approaches. This behavior, while optimal in terms of average delay, is unacceptable "
    "from a practical standpoint and would likely face public opposition if deployed. The "
    "inclusion of the max-wait penalty reduces the Gini coefficient of approach delays from "
    "0.42 to 0.18, indicating substantially more equitable service distribution.",

    "Several limitations of our work merit discussion. First, our simulation experiments assume "
    "perfect state observation through loop detectors. In practice, sensor data is noisy and "
    "may contain missing values. Preliminary experiments with 10% observation noise show only "
    "a 3.5% performance degradation, suggesting reasonable robustness, but more comprehensive "
    "robustness analysis is needed. Second, we do not model pedestrian and cyclist interactions, "
    "which are important considerations for urban deployments. Third, the computational "
    "requirements for training (approximately 48 hours on 4 NVIDIA A100 GPUs for the San "
    "Francisco network) may limit accessibility for smaller municipalities.",

    "Future work will focus on three directions. First, we plan to incorporate connected vehicle "
    "data as an additional observation source, which could improve state estimation and enable "
    "anticipatory control. Second, we will extend the framework to handle non-recurring "
    "congestion events such as incidents and work zones through online adaptation mechanisms. "
    "Third, we aim to develop a transfer learning pipeline that enables rapid deployment to "
    "new cities with minimal retraining, leveraging the structural similarities in road networks "
    "across different urban environments.",
]

REFERENCES = [
    "[1] D. Schrank, B. Eisele, and T. Lomax, \"2023 Urban Mobility Report,\" Texas A&M Transportation Institute, 2023.",
    "[2] U.S. Environmental Protection Agency, \"Inventory of U.S. Greenhouse Gas Emissions and Sinks: 1990-2022,\" EPA 430-R-24-004, 2024.",
    "[3] D. Robertson, \"TRANSYT: A traffic network study tool,\" Road Research Laboratory Report LR 253, 1969.",
    "[4] Trafficware, \"Synchro Studio 12 User Guide,\" Trafficware LLC, 2023.",
    "[5] P. Koonce et al., \"Traffic Signal Timing Manual,\" FHWA-HOP-08-024, Federal Highway Administration, 2008.",
    "[6] P. Hunt et al., \"The SCOOT on-line traffic signal optimisation technique,\" Traffic Engineering and Control, vol. 23, no. 4, pp. 190-192, 1982.",
    "[7] P. Lowrie, \"SCATS: Sydney Co-ordinated Adaptive Traffic System,\" Roads and Traffic Authority, NSW, Australia, 1990.",
    "[8] H. Wei et al., \"IntelliLight: A reinforcement learning approach for intelligent traffic light control,\" in Proc. KDD, 2018, pp. 2496-2505.",
    "[9] L. Li et al., \"Traffic signal timing via deep reinforcement learning,\" IEEE/CAA Journal of Automatica Sinica, vol. 3, no. 3, pp. 247-254, 2016.",
    "[10] T. Chu et al., \"Multi-agent deep reinforcement learning for large-scale traffic signal control,\" IEEE Trans. ITS, vol. 21, no. 3, pp. 1086-1095, 2020.",
    "[11] P. Velickovic et al., \"Graph attention networks,\" in Proc. ICLR, 2018.",
    "[12] P. Lopez et al., \"Microscopic traffic simulation using SUMO,\" in Proc. ITSC, 2018, pp. 2575-2582.",
    "[13] J. Schulman et al., \"Proximal policy optimization algorithms,\" arXiv:1707.06347, 2017.",
    "[14] Federal Highway Administration, \"Manual on Uniform Traffic Control Devices (MUTCD),\" 11th Edition, 2023.",
    "[15] V. Mnih et al., \"Human-level control through deep reinforcement learning,\" Nature, vol. 518, pp. 529-533, 2015.",
    "[16] T. Rashid et al., \"QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning,\" in Proc. ICML, 2018.",
    "[17] R. Lowe et al., \"Multi-agent actor-critic for mixed cooperative-competitive environments,\" in Proc. NeurIPS, 2017.",
    "[18] S. Hochreiter and J. Schmidhuber, \"Long short-term memory,\" Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.",
]

# Page headers/footers (these should NOT appear in the extracted text)
HEADER_LEFT = "IEEE Trans. Intelligent Transportation Systems"
HEADER_RIGHT = "Vasquez et al.: MADRL for Adaptive Traffic Signal Control"
FOOTER_TEMPLATE = "Page {}"


def add_header_footer(page, page_num, total_pages):
    """Add header and footer to a page."""
    w = page.rect.width
    h = page.rect.height
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 35), pymupdf.Point(w - 50, 35))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()
    # Header text
    if page_num % 2 == 0:
        page.insert_text(pymupdf.Point(50, 28), HEADER_LEFT, fontsize=7, fontname="tiit", color=(0.4, 0.4, 0.4))
    else:
        page.insert_text(pymupdf.Point(w - 300, 28), HEADER_RIGHT, fontsize=7, fontname="tiit", color=(0.4, 0.4, 0.4))
    # Footer
    footer_text = FOOTER_TEMPLATE.format(page_num + 1)
    page.insert_text(pymupdf.Point(w / 2 - 10, h - 30), footer_text, fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


def insert_two_column_text(page, paragraphs, start_y, fontsize=9, fontname="tiro", col_gap=20):
    """Insert text in two-column layout. Returns the y position after last text."""
    w = page.rect.width
    margin = 50
    col_width = (w - 2 * margin - col_gap) / 2
    col1_rect = pymupdf.Rect(margin, start_y, margin + col_width, page.rect.height - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, start_y, w - margin, page.rect.height - 50)

    full_text = "\n\n".join(paragraphs)

    # Try to fit in column 1
    excess = page.insert_textbox(
        col1_rect, full_text, fontsize=fontsize, fontname=fontname,
        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY
    )

    if excess:
        # Overflow to column 2
        # We need to figure out what didn't fit
        # Use a rough estimate: split text proportionally
        chars_total = len(full_text)
        chars_fit = chars_total - len(str(excess)) if isinstance(excess, str) else int(chars_total * 0.5)
        overflow_text = full_text[chars_fit:]
        page.insert_textbox(
            col2_rect, overflow_text, fontsize=fontsize, fontname=fontname,
            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY
        )

    return page.rect.height - 50


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # ====== PAGE 1: Title page ======
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 0, 12)

    # Title
    title_rect = pymupdf.Rect(50, 60, W - 50, 130)
    page.insert_textbox(title_rect, TITLE, fontsize=16, fontname="hebo", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)

    # Authors
    page.insert_textbox(pymupdf.Rect(50, 140, W - 50, 165), AUTHORS, fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)

    # Affiliation
    page.insert_textbox(pymupdf.Rect(50, 168, W - 50, 190), AFFILIATION, fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3), align=pymupdf.TEXT_ALIGN_CENTER)

    # Journal info
    page.insert_textbox(pymupdf.Rect(50, 193, W - 50, 210), JOURNAL, fontsize=8, fontname="tiit", color=(0.4, 0.4, 0.4), align=pymupdf.TEXT_ALIGN_CENTER)

    # Abstract heading
    page.insert_text(pymupdf.Point(50, 240), "Abstract", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Abstract body (single column, indented)
    abstract_rect = pymupdf.Rect(60, 250, W - 60, 430)
    page.insert_textbox(abstract_rect, ABSTRACT, fontsize=9, fontname="tiit", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Keywords
    page.insert_text(pymupdf.Point(60, 440), "Keywords: ", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(120, 440), "traffic signal control, multi-agent reinforcement learning, graph attention networks, fairness, urban mobility", fontsize=9, fontname="tiit", color=(0, 0, 0))

    # Divider
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 460), pymupdf.Point(W - 50, 460))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    # Introduction heading
    page.insert_text(pymupdf.Point(50, 480), "1. Introduction", fontsize=12, fontname="hebo", color=(0, 0, 0))

    # Two-column introduction text (first part on page 1)
    margin = 50
    col_gap = 20
    col_width = (W - 2 * margin - col_gap) / 2

    col1_rect = pymupdf.Rect(margin, 495, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 495, W - margin, H - 50)

    page.insert_textbox(col1_rect, INTRODUCTION[0], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_textbox(col2_rect, INTRODUCTION[1], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ====== PAGES 2-3: Rest of Introduction ======
    page2 = doc.new_page(width=W, height=H)
    add_header_footer(page2, 1, 12)

    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 50, W - margin, H - 50)
    page2.insert_textbox(col1_rect, INTRODUCTION[2], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page2.insert_textbox(col2_rect, INTRODUCTION[3], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ====== PAGES 3-5: Methods ======
    page3 = doc.new_page(width=W, height=H)
    add_header_footer(page3, 2, 12)
    page3.insert_text(pymupdf.Point(50, 65), "2. Methods", fontsize=12, fontname="hebo", color=(0, 0, 0))

    col1_rect = pymupdf.Rect(margin, 80, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 80, W - margin, H - 50)
    page3.insert_textbox(col1_rect, METHODS[0], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page3.insert_textbox(col2_rect, METHODS[1], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page4 = doc.new_page(width=W, height=H)
    add_header_footer(page4, 3, 12)
    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 50, W - margin, H - 50)
    page4.insert_textbox(col1_rect, METHODS[2], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page4.insert_textbox(col2_rect, METHODS[3], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page5 = doc.new_page(width=W, height=H)
    add_header_footer(page5, 4, 12)
    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    page5.insert_textbox(col1_rect, METHODS[4], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ====== PAGES 6-8: Results ======
    page6 = doc.new_page(width=W, height=H)
    add_header_footer(page6, 5, 12)
    page6.insert_text(pymupdf.Point(50, 65), "3. Results", fontsize=12, fontname="hebo", color=(0, 0, 0))

    col1_rect = pymupdf.Rect(margin, 80, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 80, W - margin, H - 50)
    page6.insert_textbox(col1_rect, RESULTS[0], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page6.insert_textbox(col2_rect, RESULTS[1], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page7 = doc.new_page(width=W, height=H)
    add_header_footer(page7, 6, 12)
    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 50, W - margin, H - 50)
    page7.insert_textbox(col1_rect, RESULTS[2], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page7.insert_textbox(col2_rect, RESULTS[3], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page8 = doc.new_page(width=W, height=H)
    add_header_footer(page8, 7, 12)
    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    page8.insert_textbox(col1_rect, RESULTS[4], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ====== PAGES 9-10: Discussion ======
    page9 = doc.new_page(width=W, height=H)
    add_header_footer(page9, 8, 12)
    page9.insert_text(pymupdf.Point(50, 65), "4. Discussion", fontsize=12, fontname="hebo", color=(0, 0, 0))

    col1_rect = pymupdf.Rect(margin, 80, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 80, W - margin, H - 50)
    page9.insert_textbox(col1_rect, DISCUSSION[0], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page9.insert_textbox(col2_rect, DISCUSSION[1], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page10 = doc.new_page(width=W, height=H)
    add_header_footer(page10, 9, 12)
    col1_rect = pymupdf.Rect(margin, 50, margin + col_width, H - 50)
    col2_rect = pymupdf.Rect(margin + col_width + col_gap, 50, W - margin, H - 50)
    page10.insert_textbox(col1_rect, DISCUSSION[2], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page10.insert_textbox(col2_rect, DISCUSSION[3], fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ====== PAGES 11-12: References ======
    page11 = doc.new_page(width=W, height=H)
    add_header_footer(page11, 10, 12)
    page11.insert_text(pymupdf.Point(50, 65), "References", fontsize=12, fontname="hebo", color=(0, 0, 0))

    ref_text = "\n\n".join(REFERENCES[:9])
    ref_rect = pymupdf.Rect(50, 85, W - 50, H - 50)
    page11.insert_textbox(ref_rect, ref_text, fontsize=8, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    page12 = doc.new_page(width=W, height=H)
    add_header_footer(page12, 11, 12)

    ref_text2 = "\n\n".join(REFERENCES[9:])
    ref_rect2 = pymupdf.Rect(50, 50, W - 50, H - 50)
    page12.insert_textbox(ref_rect2, ref_text2, fontsize=8, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Set metadata
    doc.set_metadata({
        "title": TITLE,
        "author": AUTHORS,
        "subject": "Traffic Signal Control, Deep Reinforcement Learning",
        "keywords": "MADRL, traffic, reinforcement learning, graph attention",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Add table of contents / bookmarks
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 1],
        [1, "2. Methods", 3],
        [1, "3. Results", 6],
        [1, "4. Discussion", 9],
        [1, "References", 11],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Ensure the txt file does NOT exist
    txt_path = f'{DOCUMENTS}/research_paper_text.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)

    # GUI-ready startup: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
