"""
Initial Setup: Create a scrambled thesis PDF with pages in wrong order
Task ID: pdf_res_054
Domain: pdf

Creates a 10-page thesis PDF where odd-numbered pages come first [1,3,5,7,9]
followed by even-numbered pages [2,4,6,8,10].
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_054'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/scrambled_thesis.pdf'

# Page content for a realistic thesis (10 pages, sequential content)
PAGE_CONTENT = {
    1: {
        "title": "Chapter 1: Introduction",
        "body": (
            "The rapid advancement of artificial intelligence has fundamentally transformed "
            "how organizations approach data analysis and decision-making. This thesis examines "
            "the intersection of machine learning techniques and urban transportation systems, "
            "with a particular focus on predictive modeling for traffic flow optimization.\n\n"
            "Urban congestion costs the United States economy approximately $87 billion annually "
            "in lost productivity and wasted fuel. Traditional traffic management systems rely on "
            "fixed-timing signal controllers that cannot adapt to real-time conditions. Our research "
            "proposes a novel adaptive framework that leverages deep reinforcement learning to "
            "dynamically adjust signal timing based on current traffic patterns.\n\n"
            "The remainder of this thesis is organized as follows: Chapter 2 reviews related work, "
            "Chapter 3 describes our methodology, Chapters 4-5 present our experimental framework, "
            "and Chapters 6-10 discuss results, analysis, and conclusions."
        ),
    },
    2: {
        "title": "Chapter 2: Literature Review",
        "body": (
            "Traffic signal optimization has been studied extensively since the pioneering work "
            "of Webster (1958), who established the first mathematical framework for computing "
            "optimal signal timing. Subsequent research by Robertson (1969) introduced the TRANSYT "
            "model, which enabled area-wide signal coordination.\n\n"
            "The application of reinforcement learning to traffic control began with Thorpe (1997), "
            "who demonstrated that Q-learning agents could outperform fixed-time controllers at "
            "isolated intersections. More recently, Wei et al. (2018) showed that deep Q-networks "
            "could handle multi-intersection coordination, achieving a 23% reduction in average "
            "vehicle delay compared to actuated control methods.\n\n"
            "However, existing approaches face significant limitations in scalability. As the "
            "number of intersections grows, the state-action space expands exponentially, making "
            "centralized control computationally intractable for real-world deployment scenarios."
        ),
    },
    3: {
        "title": "Chapter 3: Methodology",
        "body": (
            "Our approach employs a multi-agent deep reinforcement learning architecture where "
            "each intersection is controlled by an independent agent that communicates with "
            "neighboring agents through a graph neural network. This decentralized design allows "
            "the system to scale linearly with the number of intersections.\n\n"
            "We formulate the traffic signal control problem as a Markov Decision Process (MDP). "
            "The state space includes vehicle counts, queue lengths, and current signal phase for "
            "each approach lane. The action space consists of signal phase selections with variable "
            "green time durations ranging from 10 to 60 seconds.\n\n"
            "The reward function combines three objectives: minimizing total vehicle delay, "
            "maximizing throughput, and reducing the variance of wait times across approaches "
            "to ensure fairness. We use a weighted sum with coefficients alpha=0.5, beta=0.3, "
            "and gamma=0.2 determined through sensitivity analysis."
        ),
    },
    4: {
        "title": "Chapter 4: Experimental Setup",
        "body": (
            "We conducted experiments using the SUMO (Simulation of Urban Mobility) traffic "
            "simulator, version 1.14.1. Our test network models a 4x4 grid of signalized "
            "intersections calibrated to match traffic patterns observed in downtown Portland, "
            "Oregon during October 2023.\n\n"
            "Training data was collected from 2,400 simulation hours spanning peak and off-peak "
            "conditions. Each agent was trained for 500 episodes using the Proximal Policy "
            "Optimization (PPO) algorithm with a learning rate of 3e-4, batch size of 256, "
            "and discount factor gamma of 0.99.\n\n"
            "Hardware specifications: Training was performed on a cluster of 8 NVIDIA A100 "
            "GPUs with 80GB memory each. Total training time was approximately 72 hours. "
            "Evaluation runs used a dedicated server with 64 CPU cores for parallel simulation "
            "execution across multiple traffic scenarios."
        ),
    },
    5: {
        "title": "Chapter 5: Baseline Comparisons",
        "body": (
            "We compared our multi-agent approach against four baseline methods:\n\n"
            "1. Fixed-Time Control (FTC): Pre-timed signals using Webster's formula with "
            "cycle lengths optimized for average daily traffic volumes.\n\n"
            "2. Actuated Control (AC): Vehicle-actuated signals using loop detector data "
            "with minimum green of 10s and maximum green of 45s per phase.\n\n"
            "3. SCOOT Adaptive Control: The Split Cycle Offset Optimization Technique, "
            "a widely deployed adaptive signal system used in over 250 cities worldwide.\n\n"
            "4. Single-Agent DRL: A centralized deep reinforcement learning controller "
            "managing all 16 intersections simultaneously.\n\n"
            "Each baseline was evaluated over 100 simulation runs with randomized demand "
            "profiles to ensure statistical significance. Performance metrics include average "
            "delay, total throughput, and queue length distributions."
        ),
    },
    6: {
        "title": "Chapter 6: Results - Traffic Flow Analysis",
        "body": (
            "Our multi-agent system achieved significant improvements across all metrics. "
            "Average vehicle delay was reduced by 31.2% compared to fixed-time control, "
            "22.7% compared to actuated control, 15.4% compared to SCOOT, and 8.3% compared "
            "to the single-agent DRL baseline.\n\n"
            "During peak hours (7:00-9:00 AM and 4:30-6:30 PM), the improvements were even "
            "more pronounced. Peak-hour delay reduction reached 38.6% versus FTC and 27.1% "
            "versus SCOOT. Total network throughput increased by 12.8%, measured as vehicles "
            "completing their trips within the simulation period.\n\n"
            "Queue length analysis revealed that our approach reduced maximum queue lengths "
            "by 44% at critical intersections, virtually eliminating spillback conditions that "
            "frequently occurred under fixed-time and actuated control strategies."
        ),
    },
    7: {
        "title": "Chapter 7: Results - Communication Analysis",
        "body": (
            "The graph neural network communication mechanism proved essential for coordination. "
            "When communication was disabled (ablation study), performance degraded by 18.5% "
            "in average delay and 9.2% in throughput, approaching single-agent DRL performance.\n\n"
            "Analysis of learned communication patterns revealed emergent coordination behaviors. "
            "Agents at arterial intersections developed strong upstream-downstream information "
            "sharing, effectively creating green waves along major corridors without explicit "
            "programming of this behavior.\n\n"
            "Communication overhead remained manageable: each agent exchanged a 32-dimensional "
            "vector with its neighbors at each decision step, requiring approximately 2.1 KB/s "
            "of bandwidth per intersection. Inference latency averaged 12ms per agent, well "
            "within the real-time control requirement of sub-second response times."
        ),
    },
    8: {
        "title": "Chapter 8: Robustness and Generalization",
        "body": (
            "To evaluate robustness, we tested the trained agents under conditions not seen "
            "during training, including incident scenarios, demand fluctuations of +/- 30%, "
            "and sensor failures at randomly selected intersections.\n\n"
            "Under incident conditions (lane closures at 3 randomly selected links), our "
            "system maintained 89% of its normal performance, while fixed-time control "
            "degraded to 62% and actuated control to 71%. The agents demonstrated an ability "
            "to reroute traffic through adjacent corridors within 2-3 signal cycles.\n\n"
            "Transfer learning experiments showed that agents trained on the Portland network "
            "could be fine-tuned for a different city (Austin, TX) using only 50 episodes, "
            "achieving 92% of fully-trained performance. This suggests that the learned policies "
            "capture generalizable traffic control principles rather than network-specific patterns."
        ),
    },
    9: {
        "title": "Chapter 9: Discussion",
        "body": (
            "Our results demonstrate that decentralized multi-agent reinforcement learning "
            "provides a viable and scalable approach to urban traffic signal optimization. "
            "The key innovation lies in the graph neural network communication layer, which "
            "enables implicit coordination without centralized control.\n\n"
            "Several practical considerations merit discussion. First, deployment would require "
            "reliable vehicle detection infrastructure at each intersection. While loop detectors "
            "are standard, camera-based detection systems using computer vision could provide "
            "richer state information. Second, the transition from fixed-time to adaptive AI "
            "control raises questions about fail-safe mechanisms and regulatory compliance.\n\n"
            "Limitations of this study include the reliance on simulation rather than real-world "
            "deployment, the assumption of perfect communication between agents, and the "
            "simplified demand models that may not capture all real-world traffic phenomena."
        ),
    },
    10: {
        "title": "Chapter 10: Conclusions and Future Work",
        "body": (
            "This thesis presented a multi-agent deep reinforcement learning framework for "
            "adaptive traffic signal control that achieves state-of-the-art performance while "
            "maintaining computational scalability. Key contributions include: (1) a novel "
            "graph neural network architecture for inter-agent communication, (2) a multi-objective "
            "reward function balancing efficiency and fairness, and (3) demonstrated transferability "
            "across different urban networks.\n\n"
            "Future work will focus on three directions. First, we plan to conduct a real-world "
            "pilot study in collaboration with the Portland Bureau of Transportation, deploying "
            "our system at 8 intersections along a major arterial corridor. Second, we will "
            "extend the framework to incorporate pedestrian and cyclist detection for multi-modal "
            "signal optimization. Third, we intend to explore federated learning approaches that "
            "could enable privacy-preserving training across multiple cities.\n\n"
            "The source code and trained models are available at github.com/traffic-marl/adaptive-signals "
            "under the MIT license to support reproducibility and further research."
        ),
    },
}


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
    # Create thesis directory
    os.makedirs(THESIS_DIR, exist_ok=True)

    # First, create all pages in correct order
    doc = pymupdf.open()

    for page_num in range(1, 11):
        page = doc.new_page(width=595, height=842)  # A4
        content = PAGE_CONTENT[page_num]

        # Page header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(523, 60))
        shape.finish(color=(0.3, 0.3, 0.3), width=1)
        shape.commit()

        # Title
        page.insert_text(
            pymupdf.Point(72, 90),
            content["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Body text in a bounded rectangle
        rect = pymupdf.Rect(72, 120, 523, 770)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=11,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(280, 810),
            f"- {page_num} -",
            fontsize=10,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

        # Footer line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 790), pymupdf.Point(523, 790))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

    # Now scramble: reorder to [1,3,5,7,9,2,4,6,8,10]
    # Page indices (0-based): [0,2,4,6,8,1,3,5,7,9]
    scrambled_order = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    doc.select(scrambled_order)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
