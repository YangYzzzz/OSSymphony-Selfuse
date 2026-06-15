"""
Initial Setup: Create a 12-page deep RL paper PDF with 30 IEEE references on pages 10-12.
Task ID: pdf_res_027
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
TASK_ID = 'pdf_res_027'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/deep_rl_paper.pdf'

W, H = 612, 792
ML, MR, MT, MB = 72, 540, 72, 720


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(shlex.split(command), stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, env=env)
    time.sleep(delay_sec)


def add_page_number(page, num):
    page.insert_text(pymupdf.Point(W / 2 - 5, H - 36), str(num),
                     fontsize=9, fontname="tiro", color=(0, 0, 0))


def add_body_text(page, text, y, fontsize=9, fontname="tiro"):
    """Add text in a full-width textbox, returns new y."""
    rect = pymupdf.Rect(ML, y, MR, MB)
    page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    return MB


REFERENCES = [
    '[1] V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wierstra, and M. Riedmiller, "Playing Atari with deep reinforcement learning," in Proc. NeurIPS Workshop Deep Learn., 2013, pp. 1-9.',
    '[2] D. Silver, G. Lever, N. Heess, T. Degris, D. Wierstra, and M. Riedmiller, "Deterministic policy gradient algorithms," in Proc. Int. Conf. Mach. Learn. (ICML), 2014, pp. 387-395.',
    '[3] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra, "Continuous control with deep reinforcement learning," in Proc. Int. Conf. Learn. Represent. (ICLR), 2016, pp. 1-14.',
    '[4] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, "CARLA: An open urban driving simulator," in Proc. Conf. Robot Learn. (CoRL), 2017, pp. 1-16.',
    '[5] D. Chen, B. Zhou, V. Koltun, and P. Krahenbuhl, "Learning by cheating," in Proc. Conf. Robot Learn. (CoRL), 2020, pp. 66-75.',
    '[6] M. Toromanoff, E. Wirbel, and F. Moutarde, "End-to-end model-free reinforcement learning for urban driving using implicit affordances," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2020, pp. 7153-7162.',
    '[7] A. Prakash, K. Chitta, and A. Geiger, "Multi-modal fusion transformer for end-to-end autonomous driving," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2021, pp. 7077-7087.',
    '[8] R. S. Sutton, D. Precup, and S. Singh, "Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning," Artif. Intell., vol. 112, no. 1-2, pp. 181-211, 1999.',
    '[9] P.-L. Bacon, J. Harb, and D. Precup, "The option-critic architecture," in Proc. AAAI Conf. Artif. Intell., 2017, pp. 1726-1734.',
    '[10] A. S. Vezhnevets, S. Osindero, T. Schaul, N. Heess, M. Jaderberg, D. Silver, and K. Kavukcuoglu, "FeUdal networks for hierarchical reinforcement learning," in Proc. Int. Conf. Mach. Learn. (ICML), 2017, pp. 3540-3549.',
    '[11] C. Paxton, V. Raman, G. D. Hager, and M. Kobilarov, "Combining neural network verification and trajectory optimization for safe robot planning," in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), 2017, pp. 3235-3242.',
    '[12] Z. Qiao, K. Muelling, J. Dolan, P. Palanisamy, and P. Mudalige, "Automatically generated curriculum based reinforcement learning for autonomous vehicles in urban environment," in Proc. IEEE Intell. Veh. Symp. (IV), 2018, pp. 1233-1238.',
    '[13] J. Lee, B. Eysenbach, E. Parisotto, E. Xing, S. Levine, and R. Salakhutdinov, "Efficient exploration via state marginal matching," in Proc. Int. Conf. Learn. Represent. (ICLR), 2020, pp. 1-18.',
    '[14] C. R. Qi, H. Su, K. Mo, and L. J. Guibas, "PointNet: Deep learning on point sets for 3D classification and segmentation," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2017, pp. 652-660.',
    '[15] C. R. Qi, L. Yi, H. Su, and L. J. Guibas, "PointNet++: Deep hierarchical feature learning on point sets in a metric space," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), 2017, pp. 5099-5108.',
    '[16] Y. Zhou and O. Tuzel, "VoxelNet: End-to-end learning for point cloud based 3D object detection," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 4490-4499.',
    '[17] A. H. Lang, S. Vora, H. Caesar, L. Zhou, J. Yang, and O. Beijbom, "PointPillars: Fast encoders for object detection from point clouds," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2019, pp. 12697-12705.',
    '[18] S. Sindagi, Y. Zhou, and O. Tuzel, "MVX-Net: Multimodal VoxelNet for 3D object detection," in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), 2019, pp. 7276-7282.',
    '[19] A. Prakash, K. Chitta, and A. Geiger, "TransFuser: Imitation with transformer-based sensor fusion for autonomous driving," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2021, pp. 2257-2266.',
    '[20] Z. Liu, H. Tang, A. Amini, X. Yang, H. Mao, D. Rus, and S. Han, "BEVFusion: Multi-task multi-sensor fusion with unified bird\'s-eye view representation," in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), 2023, pp. 2774-2781.',
    '[21] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, and S. Levine, "Soft actor-critic algorithms and applications," arXiv preprint arXiv:1812.05905, 2018.',
    '[22] R. Liang, S. Graves, D. Ku, and J. Gonzalez, "Hierarchical reinforcement learning for autonomous driving with option-critic framework," in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), 2020, pp. 9580-9587.',
    '[23] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, "Proximal policy optimization algorithms," arXiv preprint arXiv:1707.06347, 2017.',
    '[24] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor," in Proc. Int. Conf. Mach. Learn. (ICML), 2018, pp. 1861-1870.',
    '[25] A. Kendall, J. Hawke, D. Janz, P. Mazur, D. Reda, J.-M. Allen, V.-D. Lam, A. Mayol-Cuevas, and N. Belvederesi, "Learning to drive in a day," in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), 2019, pp. 8248-8254.',
    '[26] P. Wang, C.-Y. Chan, and A. de La Fortelle, "A reinforcement learning based approach for automated lane change maneuvers," in Proc. IEEE Intell. Veh. Symp. (IV), 2018, pp. 1379-1384.',
    '[27] M. Bansal, A. Krizhevsky, and A. Ogale, "ChauffeurNet: Learning to drive by imitating the best and synthesizing the worst," in Proc. Robot.: Sci. Syst. (RSS), 2019, pp. 1-10.',
    '[28] W. Zeng, W. Luo, S. Suo, A. Sadat, B. Yang, S. Casas, and R. Urtasun, "End-to-end interpretable neural motion planner," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2019, pp. 8660-8669.',
    '[29] H. Shao, L. Wang, R. Chen, H. Li, and Y. Liu, "Safety-enhanced autonomous driving using interpretable sensor fusion transformer," in Proc. Conf. Robot Learn. (CoRL), 2023, pp. 726-737.',
    '[30] J. Chen, S. E. Li, and M. Tomizuka, "Interpretable end-to-end urban autonomous driving with latent deep reinforcement learning," IEEE Trans. Intell. Transp. Syst., vol. 23, no. 6, pp. 5068-5078, 2022.',
]


def create_paper():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    doc = pymupdf.open()

    # ===== PAGE 1: Title + Abstract + Intro start =====
    p = doc.new_page(width=W, height=H)
    p.insert_textbox(pymupdf.Rect(72, 72, 540, 140),
                     "Deep Reinforcement Learning for Autonomous Navigation\nin Complex Urban Environments",
                     fontsize=17, fontname="hebo", color=(0, 0, 0), align=1)
    p.insert_textbox(pymupdf.Rect(72, 145, 540, 165),
                     "Wei Zhang, Sarah Mitchell, Rajesh Patel, Maria Garcia, Takeshi Yamamoto",
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=1)
    p.insert_textbox(pymupdf.Rect(72, 170, 540, 210),
                     "Department of Computer Science, Stanford University\nDeepMind Research, London, UK\nRobotics Institute, Carnegie Mellon University",
                     fontsize=8, fontname="tiit", color=(0.3, 0.3, 0.3), align=1)
    p.insert_text(pymupdf.Point(272, 235), "Abstract", fontsize=10, fontname="hebo", color=(0, 0, 0))
    abstract = ("We present a novel deep reinforcement learning framework for autonomous navigation "
                "in dense urban traffic scenarios. Our approach combines a hierarchical policy architecture "
                "with a multi-modal perception module that processes LiDAR point clouds, camera images, "
                "and high-definition maps. We introduce a curriculum-based training strategy that "
                "progressively increases scenario complexity. Extensive experiments on the CARLA simulator "
                "demonstrate that our method achieves a 94.3% success rate in previously unseen intersections, "
                "outperforming existing approaches by 12.7 percentage points. We further validate sim-to-real "
                "transfer through deployment on a full-scale autonomous vehicle platform.")
    p.insert_textbox(pymupdf.Rect(90, 245, 522, 380), abstract, fontsize=9, fontname="tiro",
                     color=(0, 0, 0), align=3)
    p.insert_text(pymupdf.Point(ML, 400), "1. INTRODUCTION", fontsize=10, fontname="hebo", color=(0, 0, 0))
    intro = ("Autonomous driving remains one of the most challenging applications of artificial intelligence, "
             "requiring real-time decision-making under uncertainty in safety-critical environments. While "
             "classical approaches based on modular perception-planning-control pipelines have achieved "
             "considerable success in structured highway scenarios, navigating complex urban intersections "
             "with diverse traffic participants continues to pose fundamental challenges. Deep reinforcement "
             "learning has emerged as a compelling paradigm for learning end-to-end driving policies directly "
             "from sensor observations. In this paper, we address these challenges through three key "
             "contributions: a hierarchical policy architecture, a multi-modal perception encoder, and a "
             "curriculum learning strategy that systematically increases training complexity.")
    p.insert_textbox(pymupdf.Rect(ML, 415, MR, MB), intro, fontsize=9, fontname="tiro",
                     color=(0, 0, 0), align=3)
    add_page_number(p, 1)

    # ===== PAGES 2-9: Body sections =====
    body_pages = [
        ("2. RELATED WORK",
         "The application of deep reinforcement learning to autonomous driving has seen significant "
         "progress in recent years. Mnih et al. [1] demonstrated the potential of deep Q-networks for "
         "learning control policies from raw pixel inputs. Silver et al. [2] extended this with "
         "deterministic policy gradients for continuous control. Lillicrap et al. [3] proposed DDPG, "
         "combining actor-critic methods with experience replay. Dosovitskiy et al. [4] introduced "
         "conditional imitation learning as an alternative to pure RL. Chen et al. [5] proposed learning "
         "by cheating with privileged teacher distillation. Toromanoff et al. [6] achieved state-of-the-art "
         "by combining implicit affordances with RL. Prakash et al. [7] introduced multi-modal fusion for "
         "robust urban driving. Hierarchical RL provides a principled framework for temporal abstraction. "
         "Sutton et al. [8] formalized temporally extended actions. Bacon et al. [9] proposed the "
         "option-critic architecture. Vezhnevets et al. [10] introduced FeUdal Networks. For multi-modal "
         "perception, PointNet [14] and PointNet++ [15] established foundational architectures for LiDAR. "
         "VoxelNet [16] and PointPillars [17] improved efficiency. MVX-Net [18], TransFuser [19], and "
         "BEVFusion [20] explored camera-LiDAR fusion strategies."),
        ("3. METHOD",
         "3.1 Problem Formulation\n\n"
         "We formulate urban navigation as a partially observable Markov decision process (POMDP) defined "
         "by the tuple (S, A, T, R, O, Z, gamma). The state encompasses the ego vehicle pose, velocity, "
         "and acceleration, along with poses and velocities of all traffic participants within a 100-meter "
         "radius. The action consists of continuous steering angle in [-0.5, 0.5] radians and acceleration "
         "in [-3.0, 3.0] m/s^2. The observation includes a 64-beam LiDAR point cloud, a front-facing "
         "RGB camera image (1920x1080), and a local HD map crop.\n\n"
         "3.2 Hierarchical Policy Architecture\n\n"
         "Our policy decomposes into three levels: a strategic planner that selects intermediate waypoints "
         "using a graph attention network, a tactical planner using dueling DQN that selects from driving "
         "behaviors (follow_lane, change_left, change_right, turn_left, turn_right, stop, yield, "
         "emergency_stop), and a motion controller using soft actor-critic that generates continuous "
         "steering and acceleration commands."),
        ("3. METHOD (continued)",
         "3.3 Multi-Modal Perception Encoder\n\n"
         "Our perception encoder processes three input modalities: LiDAR point clouds via a modified "
         "PointPillars architecture producing a 128-dimensional BEV feature map, camera images via "
         "EfficientNet-B3 with FPN producing a 256-dimensional representation, and HD map data via a "
         "lightweight ConvNet producing a 64-dimensional feature map. All features are projected into "
         "BEV space and fused through 6 layers of cross-attention with 8 heads.\n\n"
         "3.4 Curriculum Learning Strategy\n\n"
         "Training begins with empty roads, increasing by 5 vehicles every 100K steps up to 50 traffic "
         "participants. Scenarios progress from straight roads through curved roads, T-intersections, "
         "4-way intersections, roundabouts, and multi-lane highway merges. Weather conditions start "
         "clear and progressively add rain, fog, and night. Advancement requires >85% success rate "
         "over a 500-episode window."),
        ("4. EXPERIMENTAL SETUP",
         "4.1 Training Environment\n\n"
         "Experiments use CARLA 0.9.14 with training on 8 NVIDIA A100 GPUs processing approximately "
         "200K environment steps per hour. Six training towns (Town01-Town06) cover diverse urban layouts. "
         "Evaluation uses two held-out towns (Town07, Town10HD). Episodes last up to 1000 steps at 10 Hz.\n\n"
         "4.2 Baseline Methods\n\n"
         "We compare against: DQN-Drive [1], DDPG-Nav [3], Conditional Imitation Learning [4], Learning "
         "by Cheating [5], SAC-Urban [21], and HRLAD [22]. All baselines use the same perception backbone "
         "and reward function. An expert Oracle planner serves as upper bound.\n\n"
         "4.3 Evaluation Metrics\n\n"
         "Success Rate (SR): percentage reaching goal without collision or violation. Route Completion (RC): "
         "average fraction completed. Infraction Score (IS): penalty-weighted violations. Comfort Score (CS): "
         "RMS jerk magnitude. Driving Score (DS): RC times IS per CARLA Leaderboard protocol."),
        ("5. RESULTS AND ANALYSIS",
         "5.1 Main Results\n\n"
         "Our approach (HiDRL-Nav) achieves the highest success rate of 94.3% on Town07 and 91.8% on "
         "Town10HD, outperforming the strongest baseline (HRLAD) by 12.7 and 10.4 percentage points "
         "respectively. In complex intersection scenarios, our method achieves 89.2% success rate compared "
         "to 68.5% for SAC-Urban. Curriculum learning reduces training time by 40%.\n\n"
         "5.2 Ablation Studies\n\n"
         "Removing hierarchy: SR drops from 94.3% to 79.6%. Single-modal results: LiDAR-only 86.1%, "
         "camera-only 77.4%, map-only 62.3%. Without curriculum: SR drops to 82.1% with 2.5x more steps. "
         "Replacing cross-attention with concatenation: SR drops by 5.2%.\n\n"
         "5.3 Sim-to-Real Transfer\n\n"
         "Deployed on a Lincoln MKZ platform with Velodyne VLP-32C LiDAR, Mobileye camera, and Novatel "
         "GNSS/IMU. The transferred policy achieves 80.1% SR on a 15 km urban route with 23 intersections. "
         "Domain randomization improves this to 85.2%."),
        ("5. RESULTS AND ANALYSIS (continued)",
         "Table 1: Performance comparison on held-out evaluation towns.\n\n"
         "Method          | Town07 SR | Town10HD SR | DS    | CS\n"
         "DQN-Drive [1]   | 52.1%     | 48.7%       | 0.421 | 3.82\n"
         "DDPG-Nav [3]    | 61.3%     | 57.9%       | 0.523 | 2.94\n"
         "CIL [4]         | 67.8%     | 63.2%       | 0.584 | 2.41\n"
         "LBC [5]         | 73.4%     | 70.1%       | 0.645 | 2.15\n"
         "SAC-Urban [21]  | 75.2%     | 72.8%       | 0.672 | 1.98\n"
         "HRLAD [22]      | 81.6%     | 81.4%       | 0.738 | 1.76\n"
         "HiDRL-Nav (ours)| 94.3%     | 91.8%       | 0.891 | 1.23\n"
         "Oracle (expert) | 98.7%     | 97.4%       | 0.962 | 0.87\n\n"
         "Table 2: Ablation study results on Town07.\n\n"
         "Configuration           | SR    | RC    | DS\n"
         "Full model              | 94.3% | 97.1% | 0.891\n"
         "w/o hierarchy           | 79.6% | 89.4% | 0.698\n"
         "w/o curriculum          | 82.1% | 90.8% | 0.731\n"
         "w/o cross-attention     | 89.1% | 94.3% | 0.825\n"
         "LiDAR only              | 86.1% | 92.7% | 0.784\n"
         "Camera only             | 77.4% | 88.6% | 0.673"),
        ("6. DISCUSSION",
         "6.1 Limitations and Future Work\n\n"
         "Our framework assumes access to high-definition maps which may not always be available. Future "
         "work should investigate map-free navigation. The method does not explicitly model other agents' "
         "intentions; integrating trajectory prediction could improve interactive scenarios. The sim-to-real "
         "gap, while promising at 15%, suggests combining with online fine-tuning using real data.\n\n"
         "6.2 Safety Considerations\n\n"
         "Deploying RL policies in safety-critical driving requires careful safeguards: a rule-based safety "
         "monitor for collision override, conservative speed limits in uncertain areas, and a fallback "
         "behavior for low-confidence situations. We advocate for extensive closed-course testing and "
         "graduated deployment strategies."),
        ("7. CONCLUSION",
         "We presented HiDRL-Nav, a hierarchical deep reinforcement learning framework for autonomous "
         "navigation in complex urban environments. Our three-level policy hierarchy coupled with "
         "multi-modal perception and curriculum learning achieves state-of-the-art performance on the "
         "CARLA benchmark with a 94.3% success rate. Real-world deployment demonstrates viable sim-to-real "
         "transfer with controlled degradation.\n\n"
         "ACKNOWLEDGMENT\n\n"
         "This work was supported by NSF Award IIS-2324567, the DARPA Assured Autonomy program "
         "(FA8750-18-C-0089), and a Google Research Scholar Award. We thank the anonymous reviewers "
         "for their constructive feedback and the CMU autonomous vehicle team for assisting with "
         "real-world experiments."),
    ]

    for i, (title, text) in enumerate(body_pages):
        p = doc.new_page(width=W, height=H)
        p.insert_text(pymupdf.Point(ML, MT), title, fontsize=10, fontname="hebo", color=(0, 0, 0))
        p.insert_textbox(pymupdf.Rect(ML, MT + 16, MR, MB), text, fontsize=9, fontname="tiro",
                         color=(0, 0, 0), align=3)
        add_page_number(p, i + 2)

    # ===== PAGES 10-12: REFERENCES =====
    refs_per_page = [12, 10, 8]
    ref_idx = 0
    for pg_offset, count in enumerate(refs_per_page):
        p = doc.new_page(width=W, height=H)
        y = MT
        if pg_offset == 0:
            p.insert_text(pymupdf.Point(ML, y), "REFERENCES", fontsize=10, fontname="hebo", color=(0, 0, 0))
            y += 18
        for _ in range(count):
            if ref_idx >= len(REFERENCES):
                break
            ref_rect = pymupdf.Rect(ML, y, MR, y + 48)
            p.insert_textbox(ref_rect, REFERENCES[ref_idx], fontsize=8, fontname="tiro",
                             color=(0, 0, 0), align=0)
            y += 42
            ref_idx += 1
        add_page_number(p, 10 + pg_offset)

    # Trim or pad to exactly 12 pages
    while doc.page_count > 12:
        doc.delete_page(doc.page_count - 1)
    while doc.page_count < 12:
        p = doc.new_page(width=W, height=H)
        add_page_number(p, doc.page_count)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')


def main():
    create_paper()
    # Ensure references.bib does NOT exist
    bib_path = f'{PAPERS_DIR}/references.bib'
    if os.path.exists(bib_path):
        os.remove(bib_path)
    # Open PDF in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


main()
