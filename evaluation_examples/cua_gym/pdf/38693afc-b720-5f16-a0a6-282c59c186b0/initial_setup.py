"""
Initial Setup: Create two multi-page research PDFs for side-by-side comparison task.
Task ID: pdf_res_031
Domain: pdf

Creates:
  /home/user/papers/original.pdf  - Original research paper (6 pages)
  /home/user/papers/revised.pdf   - Revised version with visible changes (6 pages)

The agent must combine these into a side-by-side comparison PDF.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_031'
PAPERS_DIR = f'{WORKDIR}/papers'
ORIGINAL = f'{PAPERS_DIR}/original.pdf'
REVISED = f'{PAPERS_DIR}/revised.pdf'

# Page dimensions: A4
W, H = 595, 842


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


def add_header_footer(page, title, page_num, total_pages, is_revised=False):
    """Add consistent header and footer to a page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 60), pymupdf.Point(W - 50, 60))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()

    label = "REVISED" if is_revised else "ORIGINAL"
    color = (0.7, 0.0, 0.0) if is_revised else (0.0, 0.0, 0.5)
    page.insert_text(pymupdf.Point(50, 50), f"{label} - {title}",
                     fontsize=8, fontname="heit", color=color)

    # Footer
    footer_y = H - 30
    page.insert_text(pymupdf.Point(50, footer_y),
                     f"Page {page_num} of {total_pages}",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(W - 200, footer_y),
                     "Confidential - Internal Use Only",
                     fontsize=7, fontname="heit", color=(0.5, 0.5, 0.5))


def create_original():
    """Create a realistic 6-page original research paper."""
    doc = pymupdf.open()
    title = "Adaptive Resource Allocation in Distributed Edge Computing Networks"
    total_pages = 6

    # --- Page 1: Title page ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 1, total_pages)

    p.insert_text(pymupdf.Point(72, 150), title,
                  fontsize=18, fontname="hebo", color=(0.0, 0.0, 0.3))

    authors = [
        "Elena Marchetti, Department of Computer Science, ETH Zurich",
        "Kenji Watanabe, Systems Research Lab, NTT Corporation",
        "Priya Raghavan, School of Engineering, IIT Bombay",
    ]
    y = 200
    for author in authors:
        p.insert_text(pymupdf.Point(72, y), author,
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 18

    # Abstract
    p.insert_text(pymupdf.Point(72, 290), "Abstract", fontsize=13, fontname="hebo")
    abstract = (
        "This paper presents a novel framework for adaptive resource allocation in distributed "
        "edge computing networks. Our approach leverages reinforcement learning to dynamically "
        "balance computational workloads across heterogeneous edge nodes, achieving a 23% improvement "
        "in average response latency compared to existing static allocation methods. We evaluate "
        "our framework on a testbed of 48 edge nodes deployed across three metropolitan areas, "
        "demonstrating significant gains in throughput and energy efficiency. The proposed algorithm "
        "converges within 150 training episodes and maintains stable performance under varying "
        "network conditions, including node failures and traffic spikes."
    )
    p.insert_textbox(pymupdf.Rect(72, 310, W - 72, 520), abstract,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 540), "Keywords: ", fontsize=10, fontname="hebo")
    p.insert_text(pymupdf.Point(135, 540),
                  "edge computing, resource allocation, reinforcement learning, distributed systems",
                  fontsize=10, fontname="heit")

    # --- Page 2: Introduction ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 2, total_pages)

    p.insert_text(pymupdf.Point(72, 90), "1. Introduction", fontsize=14, fontname="hebo")
    intro_text = (
        "The rapid proliferation of Internet of Things (IoT) devices and latency-sensitive applications "
        "has driven significant interest in edge computing architectures. Unlike centralized cloud "
        "computing, edge computing distributes processing closer to data sources, reducing network "
        "latency and bandwidth consumption. However, managing resources across geographically "
        "distributed edge nodes presents substantial challenges.\n\n"
        "Current resource allocation strategies predominantly rely on static provisioning or simple "
        "threshold-based heuristics. These approaches fail to capture the dynamic nature of edge "
        "workloads, which exhibit temporal patterns influenced by user behavior, application demands, "
        "and environmental factors. For instance, traffic patterns in a smart city deployment show "
        "predictable diurnal variations but also exhibit sudden bursts during events.\n\n"
        "In this paper, we address these limitations by proposing EdgeRL, a reinforcement learning "
        "framework that continuously adapts resource allocation decisions based on observed system "
        "state. Our contributions include: (1) a novel state representation that captures both local "
        "node utilization and global network topology, (2) a multi-agent coordination protocol that "
        "reduces communication overhead by 67%, and (3) a comprehensive evaluation on a real-world "
        "testbed spanning 48 edge nodes across Singapore, Tokyo, and Mumbai."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 520), intro_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 540), "1.1 Problem Statement", fontsize=12, fontname="hebo")
    problem_text = (
        "Consider a network G = (V, E) where V represents edge nodes and E represents communication "
        "links. Each node v_i has a capacity vector c_i = (cpu_i, mem_i, bw_i) representing available "
        "CPU cycles, memory, and network bandwidth. Task requests arrive according to a non-stationary "
        "Poisson process with rate lambda(t). The objective is to minimize the weighted sum of response "
        "latency and energy consumption while satisfying quality-of-service constraints."
    )
    p.insert_textbox(pymupdf.Rect(72, 560, W - 72, 720), problem_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Related Work ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 3, total_pages)

    p.insert_text(pymupdf.Point(72, 90), "2. Related Work", fontsize=14, fontname="hebo")
    related_text = (
        "Resource allocation in distributed computing has been extensively studied. We categorize "
        "existing approaches into three groups: optimization-based methods, heuristic algorithms, "
        "and learning-based approaches.\n\n"
        "Optimization-based methods: Zhang et al. [1] formulated edge resource allocation as a "
        "mixed-integer linear program (MILP) and solved it using branch-and-bound. While optimal "
        "for small instances, this approach does not scale beyond 12 nodes. Liu and Chen [2] proposed "
        "a convex relaxation that reduces complexity to O(n^2 log n) but sacrifices solution quality "
        "by up to 15%.\n\n"
        "Heuristic algorithms: The First-Fit Decreasing (FFD) algorithm and its variants have been "
        "widely applied to task scheduling in edge environments [3]. Park et al. [4] introduced a "
        "genetic algorithm that outperforms FFD by 8% on average but requires 500ms per scheduling "
        "decision, limiting real-time applicability.\n\n"
        "Learning-based approaches: Recent work has applied deep reinforcement learning to resource "
        "management. Mao et al. [5] used a policy gradient method for job scheduling in cloud clusters, "
        "achieving 15-25% improvement over heuristics. However, their approach assumes homogeneous "
        "resources and centralized decision-making, which is not practical for edge deployments."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 520), related_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Table of comparison
    p.insert_text(pymupdf.Point(72, 540), "Table 1: Comparison of Resource Allocation Methods",
                  fontsize=9, fontname="hebo")

    # Draw table
    table_data = [
        ["Method", "Scalability", "Latency (ms)", "Energy (W)", "Adaptability"],
        ["MILP [1]", "Low (<=12)", "45.2", "312", "None"],
        ["Convex [2]", "Medium", "52.8", "298", "None"],
        ["FFD [3]", "High", "68.4", "345", "None"],
        ["GA [4]", "Medium", "58.1", "321", "Low"],
        ["DRL [5]", "Medium", "42.7", "287", "Medium"],
    ]
    col_widths = [90, 80, 80, 70, 80]
    x_start = 72
    y_start = 560
    row_h = 18

    shape = p.new_shape()
    for ri, row in enumerate(table_data):
        x = x_start
        for ci, cell in enumerate(row):
            cw = col_widths[ci]
            rect = pymupdf.Rect(x, y_start + ri * row_h, x + cw, y_start + (ri + 1) * row_h)
            shape.draw_rect(rect)
            if ri == 0:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.85, 0.85, 0.95), width=0.5)
            else:
                shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
            fs = 8 if ri == 0 else 7.5
            fn = "hebo" if ri == 0 else "helv"
            p.insert_text(pymupdf.Point(x + 3, y_start + ri * row_h + 13), cell,
                          fontsize=fs, fontname=fn)
            x += cw
    shape.commit()

    # --- Page 4: Methodology ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 4, total_pages)

    p.insert_text(pymupdf.Point(72, 90), "3. Methodology", fontsize=14, fontname="hebo")
    p.insert_text(pymupdf.Point(72, 115), "3.1 System Architecture", fontsize=12, fontname="hebo")
    method_text = (
        "EdgeRL employs a hierarchical architecture with three layers: (1) a local agent on each "
        "edge node that monitors resource utilization and incoming task queues, (2) a cluster "
        "coordinator that aggregates state information from nodes within the same geographical region, "
        "and (3) a global controller that maintains a policy network shared across all clusters.\n\n"
        "The local agent observes a state vector s_i(t) = [u_cpu, u_mem, u_bw, q_len, q_wait] where "
        "u represents utilization ratios and q represents queue statistics. The cluster coordinator "
        "computes a regional embedding using an attention mechanism over local states, producing a "
        "fixed-dimensional representation regardless of the number of nodes.\n\n"
        "The policy network pi(a|s; theta) maps the concatenated state [s_local, s_regional, s_global] "
        "to a probability distribution over allocation actions. Actions include: (a) process locally, "
        "(b) offload to a specific neighbor, (c) queue for batch processing, and (d) reject with "
        "graceful degradation."
    )
    p.insert_textbox(pymupdf.Rect(72, 135, W - 72, 430), method_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 450), "3.2 Training Procedure", fontsize=12, fontname="hebo")
    training_text = (
        "We train the policy using Proximal Policy Optimization (PPO) with a clipping parameter "
        "epsilon = 0.2. The reward function R(s, a) combines three components: "
        "R = -alpha * latency - beta * energy + gamma * throughput, where alpha = 0.4, beta = 0.3, "
        "gamma = 0.3. Training proceeds in episodes of 1000 timesteps with a discount factor "
        "gamma = 0.99. We use a learning rate of 3e-4 with cosine annealing over 500 episodes.\n\n"
        "To handle the non-stationarity of edge workloads, we employ experience replay with "
        "prioritized sampling. The replay buffer stores the most recent 100,000 transitions, "
        "and we sample mini-batches of 256 for each update step."
    )
    p.insert_textbox(pymupdf.Rect(72, 470, W - 72, 700), training_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 5: Results ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 5, total_pages)

    p.insert_text(pymupdf.Point(72, 90), "4. Experimental Results", fontsize=14, fontname="hebo")
    results_text = (
        "We evaluate EdgeRL on our testbed of 48 Raspberry Pi 4B nodes (8GB RAM) connected via "
        "a mesh network with average link latency of 12ms. The testbed spans three sites: "
        "Singapore (16 nodes), Tokyo (16 nodes), and Mumbai (16 nodes). We generate workloads "
        "using traces from a production CDN covering 72 hours of traffic.\n\n"
        "Table 2 presents the main performance comparison. EdgeRL achieves the lowest average "
        "response latency (34.6ms) while maintaining competitive energy efficiency. The improvement "
        "over the best baseline (DRL [5]) is statistically significant (p < 0.01, paired t-test)."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 300), results_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 320), "Table 2: Performance Comparison on 48-Node Testbed",
                  fontsize=9, fontname="hebo")

    results_table = [
        ["Method", "Avg Latency", "P99 Latency", "Throughput", "Energy"],
        ["Static", "78.3 ms", "245.1 ms", "1,240 req/s", "412 W"],
        ["FFD", "62.1 ms", "198.7 ms", "1,580 req/s", "389 W"],
        ["GA", "51.4 ms", "167.2 ms", "1,720 req/s", "367 W"],
        ["DRL [5]", "42.7 ms", "134.5 ms", "1,890 req/s", "341 W"],
        ["EdgeRL", "34.6 ms", "98.3 ms", "2,150 req/s", "318 W"],
    ]
    col_w2 = [80, 80, 80, 80, 70]
    y2 = 340
    shape = p.new_shape()
    for ri, row in enumerate(results_table):
        x = 72
        for ci, cell in enumerate(row):
            cw = col_w2[ci]
            rect = pymupdf.Rect(x, y2 + ri * 18, x + cw, y2 + (ri + 1) * 18)
            shape.draw_rect(rect)
            if ri == 0:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.85, 0.95, 0.85), width=0.5)
            elif ri == len(results_table) - 1:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.95, 0.95, 0.85), width=0.5)
            else:
                shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
            fs = 8 if ri == 0 else 7.5
            fn = "hebo" if (ri == 0 or ri == len(results_table) - 1) else "helv"
            p.insert_text(pymupdf.Point(x + 3, y2 + ri * 18 + 13), cell,
                          fontsize=fs, fontname=fn)
            x += cw
    shape.commit()

    # --- Page 6: Conclusion ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 6, total_pages)

    p.insert_text(pymupdf.Point(72, 90), "5. Conclusion", fontsize=14, fontname="hebo")
    conclusion_text = (
        "We presented EdgeRL, a reinforcement learning framework for adaptive resource allocation "
        "in distributed edge computing networks. Our approach achieves a 23% reduction in average "
        "response latency compared to the best existing method while consuming 6.7% less energy. "
        "The framework scales to networks of 48+ nodes and maintains stable performance under "
        "dynamic workload conditions.\n\n"
        "Key findings include: (1) the hierarchical state representation effectively captures "
        "cross-region dependencies, (2) the multi-agent coordination protocol reduces communication "
        "overhead without sacrificing allocation quality, and (3) the system converges within "
        "150 training episodes, making it practical for real-world deployment.\n\n"
        "Future work will explore federated learning extensions to preserve data privacy across "
        "edge clusters, and investigate transfer learning to accelerate adaptation when new nodes "
        "join the network."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 400), conclusion_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 420), "References", fontsize=14, fontname="hebo")
    refs = [
        "[1] Zhang, W. et al. Optimal edge resource allocation via MILP. IEEE TCC, 2022.",
        "[2] Liu, H. and Chen, X. Convex relaxation for edge scheduling. ACM SIGCOMM, 2021.",
        "[3] Kumar, R. et al. First-fit heuristics for edge task placement. INFOCOM, 2020.",
        "[4] Park, S. et al. Genetic algorithm for distributed edge computing. IEEE TPDS, 2023.",
        "[5] Mao, H. et al. Resource management with deep RL. HotNets, 2016.",
        "[6] Sutton, R. and Barto, A. Reinforcement Learning: An Introduction. MIT Press, 2018.",
        "[7] Schulman, J. et al. Proximal Policy Optimization. arXiv:1707.06347, 2017.",
        "[8] Li, E. et al. Edge intelligence: Frameworks and challenges. IEEE Access, 2019.",
    ]
    y_ref = 445
    for ref in refs:
        p.insert_text(pymupdf.Point(72, y_ref), ref, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))
        y_ref += 16

    doc.save(ORIGINAL)
    doc.close()
    print(f"Created: {ORIGINAL}")


def create_revised():
    """Create a revised version of the paper with visible differences."""
    doc = pymupdf.open()
    title = "Adaptive Resource Allocation in Distributed Edge Computing Networks"
    total_pages = 6

    # --- Page 1: Title page (changed author list, updated abstract) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 1, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 150), title,
                  fontsize=18, fontname="hebo", color=(0.0, 0.0, 0.3))

    # Added a 4th author in revision
    authors = [
        "Elena Marchetti, Department of Computer Science, ETH Zurich",
        "Kenji Watanabe, Systems Research Lab, NTT Corporation",
        "Priya Raghavan, School of Engineering, IIT Bombay",
        "David Okonkwo, Faculty of Technology, University of Lagos",
    ]
    y = 200
    for author in authors:
        p.insert_text(pymupdf.Point(72, y), author,
                      fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 18

    p.insert_text(pymupdf.Point(72, 300), "Abstract", fontsize=13, fontname="hebo")
    abstract = (
        "This paper presents an enhanced framework for adaptive resource allocation in distributed "
        "edge computing networks. Our approach leverages multi-agent reinforcement learning to "
        "dynamically balance computational workloads across heterogeneous edge nodes, achieving a "
        "31% improvement in average response latency compared to existing static allocation methods "
        "(revised from 23% in the original submission). We evaluate our framework on an expanded "
        "testbed of 64 edge nodes deployed across four metropolitan areas, demonstrating significant "
        "gains in throughput, energy efficiency, and fault tolerance. The proposed algorithm converges "
        "within 120 training episodes and maintains stable performance under varying network conditions."
    )
    p.insert_textbox(pymupdf.Rect(72, 320, W - 72, 540), abstract,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 560), "Keywords: ", fontsize=10, fontname="hebo")
    p.insert_text(pymupdf.Point(135, 560),
                  "edge computing, resource allocation, multi-agent reinforcement learning, distributed systems, fault tolerance",
                  fontsize=10, fontname="heit")

    # --- Page 2: Introduction (minor updates) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 2, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 90), "1. Introduction", fontsize=14, fontname="hebo")
    intro_text = (
        "The rapid proliferation of Internet of Things (IoT) devices and latency-sensitive applications "
        "has driven significant interest in edge computing architectures. Unlike centralized cloud "
        "computing, edge computing distributes processing closer to data sources, reducing network "
        "latency and bandwidth consumption. However, managing resources across geographically "
        "distributed edge nodes presents substantial challenges.\n\n"
        "Current resource allocation strategies predominantly rely on static provisioning or simple "
        "threshold-based heuristics. These approaches fail to capture the dynamic nature of edge "
        "workloads, which exhibit temporal patterns influenced by user behavior, application demands, "
        "and environmental factors. Recent studies [9, 10] further highlight the need for adaptive "
        "approaches in 5G-enabled edge environments.\n\n"
        "In this paper, we address these limitations by proposing EdgeRL-v2, a multi-agent reinforcement "
        "learning framework that continuously adapts resource allocation decisions. Compared to our "
        "earlier submission, this revision includes: (1) an expanded testbed with 64 nodes across four "
        "cities, (2) a new fault tolerance mechanism based on consensus protocols, (3) improved "
        "convergence speed through curriculum learning, and (4) additional comparisons with three "
        "recent baselines published in 2024."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 520), intro_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 540), "1.1 Problem Statement", fontsize=12, fontname="hebo")
    problem_text = (
        "Consider a network G = (V, E) where V represents edge nodes and E represents communication "
        "links. Each node v_i has a capacity vector c_i = (cpu_i, mem_i, bw_i, gpu_i) representing "
        "available CPU cycles, memory, network bandwidth, and GPU resources. Task requests arrive "
        "according to a non-stationary Poisson process with rate lambda(t). We additionally model "
        "node failures with probability p_fail drawn from operational logs."
    )
    p.insert_textbox(pymupdf.Rect(72, 560, W - 72, 720), problem_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Related Work (updated) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 3, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 90), "2. Related Work", fontsize=14, fontname="hebo")
    related_text = (
        "Resource allocation in distributed computing has been extensively studied. We categorize "
        "existing approaches into four groups: optimization-based methods, heuristic algorithms, "
        "learning-based approaches, and hybrid methods.\n\n"
        "Optimization-based methods: Zhang et al. [1] formulated edge resource allocation as a "
        "mixed-integer linear program (MILP). Liu and Chen [2] proposed a convex relaxation. "
        "More recently, Fernandez et al. [9] used Benders decomposition achieving near-optimal "
        "solutions for up to 30 nodes.\n\n"
        "Heuristic algorithms: The First-Fit Decreasing (FFD) algorithm and variants have been "
        "widely applied [3]. Park et al. [4] introduced a genetic algorithm. Kim and Lee [10] "
        "proposed an ant colony optimization variant specifically designed for edge environments.\n\n"
        "Learning-based approaches: Mao et al. [5] used policy gradient for cloud job scheduling. "
        "Wang et al. [11] extended this to edge with a graph neural network state encoder.\n\n"
        "Hybrid methods: Recent work combines optimization with learning. Chen et al. [12] used "
        "RL to select among optimization solvers, achieving 94% of optimal with 10x speedup."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 500), related_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 520), "Table 1: Comparison of Resource Allocation Methods (Updated)",
                  fontsize=9, fontname="hebo")

    table_data = [
        ["Method", "Scalability", "Latency (ms)", "Energy (W)", "Adaptability"],
        ["MILP [1]", "Low (<=12)", "45.2", "312", "None"],
        ["Convex [2]", "Medium", "52.8", "298", "None"],
        ["FFD [3]", "High", "68.4", "345", "None"],
        ["GA [4]", "Medium", "58.1", "321", "Low"],
        ["DRL [5]", "Medium", "42.7", "287", "Medium"],
        ["Benders [9]", "Med-High", "40.1", "295", "Low"],
        ["ACO [10]", "High", "55.3", "332", "Low"],
        ["GNN-RL [11]", "High", "38.9", "275", "High"],
    ]
    col_widths = [90, 80, 80, 70, 80]
    x_start = 72
    y_start = 540
    row_h = 16

    shape = p.new_shape()
    for ri, row in enumerate(table_data):
        x = x_start
        for ci, cell in enumerate(row):
            cw = col_widths[ci]
            rect = pymupdf.Rect(x, y_start + ri * row_h, x + cw, y_start + (ri + 1) * row_h)
            shape.draw_rect(rect)
            if ri == 0:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.85, 0.85, 0.95), width=0.5)
            else:
                shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
            fs = 7.5 if ri == 0 else 7
            fn = "hebo" if ri == 0 else "helv"
            p.insert_text(pymupdf.Point(x + 3, y_start + ri * row_h + 12), cell,
                          fontsize=fs, fontname=fn)
            x += cw
    shape.commit()

    # --- Page 4: Methodology (updated) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 4, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 90), "3. Methodology", fontsize=14, fontname="hebo")
    p.insert_text(pymupdf.Point(72, 115), "3.1 System Architecture", fontsize=12, fontname="hebo")
    method_text = (
        "EdgeRL-v2 employs an enhanced hierarchical architecture with four layers: (1) a local agent "
        "on each edge node, (2) a cluster coordinator for regional aggregation, (3) a global controller "
        "with a shared policy network, and (4) a new fault recovery module that monitors node health "
        "and triggers task migration when failures are detected.\n\n"
        "The local agent observes an extended state vector s_i(t) = [u_cpu, u_mem, u_bw, u_gpu, "
        "q_len, q_wait, health_score] where health_score is derived from heartbeat intervals and "
        "error rates. The cluster coordinator uses a graph attention network (GAT) to compute "
        "topology-aware regional embeddings.\n\n"
        "The policy network pi(a|s; theta) maps the concatenated state to allocation actions. "
        "We add a new action (e) migrate-and-replicate for fault tolerance scenarios, bringing "
        "the total action space to five discrete choices per task."
    )
    p.insert_textbox(pymupdf.Rect(72, 135, W - 72, 420), method_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 440), "3.2 Training Procedure", fontsize=12, fontname="hebo")
    training_text = (
        "We train using Proximal Policy Optimization (PPO) with clipping epsilon = 0.2 and a "
        "curriculum learning schedule. Training begins with simple 16-node topologies and "
        "progressively increases to the full 64-node network. The reward function is updated to "
        "R = -alpha * latency - beta * energy + gamma * throughput + delta * availability, "
        "where alpha = 0.35, beta = 0.25, gamma = 0.25, delta = 0.15. The availability term "
        "penalizes task failures due to node crashes.\n\n"
        "Curriculum learning reduces convergence time from 150 to 120 episodes. We use a learning "
        "rate of 3e-4 with cosine annealing over 400 episodes, and gradient clipping at 0.5."
    )
    p.insert_textbox(pymupdf.Rect(72, 460, W - 72, 700), training_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 5: Results (improved) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 5, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 90), "4. Experimental Results", fontsize=14, fontname="hebo")
    results_text = (
        "We evaluate EdgeRL-v2 on an expanded testbed of 64 Raspberry Pi 4B nodes (8GB RAM) "
        "spanning four sites: Singapore (16 nodes), Tokyo (16 nodes), Mumbai (16 nodes), and "
        "Lagos (16 nodes). We use 120 hours of production CDN traces. Additionally, we inject "
        "synthetic node failures at rates of 1%, 5%, and 10% to evaluate fault tolerance.\n\n"
        "Table 2 presents the updated performance comparison with additional baselines."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 260), results_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 280), "Table 2: Performance Comparison on 64-Node Testbed",
                  fontsize=9, fontname="hebo")

    results_table = [
        ["Method", "Avg Latency", "P99 Latency", "Throughput", "Energy"],
        ["Static", "82.1 ms", "261.3 ms", "1,180 req/s", "438 W"],
        ["FFD", "65.8 ms", "208.4 ms", "1,520 req/s", "405 W"],
        ["GA", "54.2 ms", "175.6 ms", "1,680 req/s", "381 W"],
        ["DRL [5]", "44.9 ms", "141.2 ms", "1,840 req/s", "355 W"],
        ["GNN-RL [11]", "39.7 ms", "118.5 ms", "2,020 req/s", "332 W"],
        ["EdgeRL-v2", "28.4 ms", "82.1 ms", "2,380 req/s", "298 W"],
    ]
    col_w2 = [80, 80, 80, 80, 70]
    y2 = 300
    shape = p.new_shape()
    for ri, row in enumerate(results_table):
        x = 72
        for ci, cell in enumerate(row):
            cw = col_w2[ci]
            rect = pymupdf.Rect(x, y2 + ri * 18, x + cw, y2 + (ri + 1) * 18)
            shape.draw_rect(rect)
            if ri == 0:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.85, 0.95, 0.85), width=0.5)
            elif ri == len(results_table) - 1:
                shape.finish(color=(0.3, 0.3, 0.3), fill=(0.95, 0.95, 0.85), width=0.5)
            else:
                shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
            fs = 8 if ri == 0 else 7.5
            fn = "hebo" if (ri == 0 or ri == len(results_table) - 1) else "helv"
            p.insert_text(pymupdf.Point(x + 3, y2 + ri * 18 + 13), cell,
                          fontsize=fs, fontname=fn)
            x += cw
    shape.commit()

    # Fault tolerance results
    p.insert_text(pymupdf.Point(72, 470), "4.1 Fault Tolerance Evaluation", fontsize=12, fontname="hebo")
    fault_text = (
        "Under 5% node failure rate, EdgeRL-v2 maintains 96.2% task completion rate compared to "
        "87.4% for DRL [5] and 91.8% for GNN-RL [11]. The fault recovery module detects failures "
        "within 200ms and migrates affected tasks with minimal latency overhead (< 5ms additional)."
    )
    p.insert_textbox(pymupdf.Rect(72, 490, W - 72, 600), fault_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 6: Conclusion (updated) ---
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, title, 6, total_pages, is_revised=True)

    p.insert_text(pymupdf.Point(72, 90), "5. Conclusion", fontsize=14, fontname="hebo")
    conclusion_text = (
        "We presented EdgeRL-v2, an enhanced multi-agent reinforcement learning framework for "
        "adaptive resource allocation in distributed edge computing networks. Compared to our "
        "initial submission, this revision demonstrates a 31% reduction in average response latency "
        "(improved from 23%) on a larger 64-node testbed spanning four metropolitan areas.\n\n"
        "Key improvements in this revision: (1) expanded evaluation with 64 nodes across four cities, "
        "(2) new fault tolerance mechanism achieving 96.2% task completion under 5% failure rate, "
        "(3) curriculum learning reducing convergence time by 20%, and (4) comprehensive comparison "
        "with four additional recent baselines.\n\n"
        "Future work will explore federated learning extensions, transfer learning for network "
        "expansion, and integration with emerging 6G infrastructure."
    )
    p.insert_textbox(pymupdf.Rect(72, 115, W - 72, 380), conclusion_text,
                     fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p.insert_text(pymupdf.Point(72, 400), "References", fontsize=14, fontname="hebo")
    refs = [
        "[1] Zhang, W. et al. Optimal edge resource allocation via MILP. IEEE TCC, 2022.",
        "[2] Liu, H. and Chen, X. Convex relaxation for edge scheduling. ACM SIGCOMM, 2021.",
        "[3] Kumar, R. et al. First-fit heuristics for edge task placement. INFOCOM, 2020.",
        "[4] Park, S. et al. Genetic algorithm for distributed edge computing. IEEE TPDS, 2023.",
        "[5] Mao, H. et al. Resource management with deep RL. HotNets, 2016.",
        "[6] Sutton, R. and Barto, A. Reinforcement Learning: An Introduction. MIT Press, 2018.",
        "[7] Schulman, J. et al. Proximal Policy Optimization. arXiv:1707.06347, 2017.",
        "[8] Li, E. et al. Edge intelligence: Frameworks and challenges. IEEE Access, 2019.",
        "[9] Fernandez, M. et al. Benders decomposition for edge placement. IEEE TNSM, 2024.",
        "[10] Kim, J. and Lee, S. Ant colony optimization for edge computing. Future Gen. CS, 2024.",
        "[11] Wang, Y. et al. GNN-based RL for distributed edge scheduling. NeurIPS, 2023.",
        "[12] Chen, Z. et al. Hybrid optimization-RL for edge systems. AAAI, 2024.",
    ]
    y_ref = 425
    for ref in refs:
        p.insert_text(pymupdf.Point(72, y_ref), ref, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))
        y_ref += 14

    doc.save(REVISED)
    doc.close()
    print(f"Created: {REVISED}")


def main():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    create_original()
    create_revised()

    # Open original.pdf in Evince for the agent
    launch_gui(f'evince "{ORIGINAL}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


main()
