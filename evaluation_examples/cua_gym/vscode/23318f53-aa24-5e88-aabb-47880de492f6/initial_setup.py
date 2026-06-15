"""
Initial Setup: Install and configure Markdown All in One extension with TOC
Task ID: vscode_stu_074
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_074'
OUTPUT = f'{WORKDIR}/README.md'


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
    # Create a realistic research paper README.md with multiple headings
    content = """# Scalable Approaches to Federated Learning in Heterogeneous Networks

## Abstract

This paper presents a comprehensive study of federated learning techniques
applied to heterogeneous network environments. We propose FedHetero, a novel
aggregation strategy that accounts for varying computational capabilities and
data distributions across participating nodes. Our experiments demonstrate
a 23% improvement in convergence speed compared to standard FedAvg while
maintaining differential privacy guarantees.

## Introduction

Federated learning has emerged as a promising paradigm for training machine
learning models across distributed data sources without centralizing sensitive
information. However, real-world deployments face significant challenges when
participating devices exhibit heterogeneous computational resources, network
bandwidth, and local data distributions.

In this work, we address three key limitations of existing approaches:
1. Non-IID data partitioning across clients
2. Stragglers caused by resource-constrained devices
3. Communication overhead in bandwidth-limited settings

## Related Work

McMahan et al. (2017) introduced the FedAvg algorithm, establishing the
foundation for communication-efficient federated optimization. Subsequent
work by Li et al. (2020) proposed FedProx to handle systems heterogeneity
through a proximal term in the local objective. Karimireddy et al. (2020)
analyzed the impact of gradient dissimilarity and introduced SCAFFOLD to
correct for client drift.

Recent advances in personalized federated learning, including Per-FedAvg
(Fallah et al., 2020) and pFedMe (Dinh et al., 2020), have shown that
meta-learning frameworks can adapt global models to individual client
distributions effectively.

## Methodology

### Problem Formulation

We consider a federated setting with $N$ clients, each holding a local
dataset $D_k$ drawn from a potentially distinct distribution $P_k$. The
global objective is to minimize:

$$\\min_w \\sum_{k=1}^{N} \\frac{|D_k|}{|D|} F_k(w)$$

where $F_k(w)$ denotes the local empirical risk on client $k$.

### FedHetero Algorithm

Our proposed algorithm introduces an adaptive weighting scheme that
dynamically adjusts client contributions based on:
- Local gradient norm as a proxy for data heterogeneity
- Estimated computational capacity from historical round times
- Communication reliability scores derived from packet loss rates

### Privacy Guarantees

We incorporate a calibrated Gaussian noise mechanism into each client's
local update, achieving $(\\epsilon, \\delta)$-differential privacy with
$\\epsilon = 1.2$ and $\\delta = 10^{-5}$ for a participation rate of 5%
per round over 500 communication rounds.

## Experimental Setup

All experiments are conducted on a cluster of 100 simulated clients using
the LEAF benchmark suite. We evaluate on three datasets:

| Dataset    | Clients | Samples/Client | Classes | Task              |
|------------|---------|-----------------|---------|-------------------|
| FEMNIST    | 100     | 50-350          | 62      | Image Recognition |
| Shakespeare| 100     | 200-1200        | 80      | Next Character    |
| CelebA     | 100     | 30-100          | 2       | Attribute Pred.   |

Hardware configuration: Each simulated client runs on a Raspberry Pi 4B
(4GB RAM) connected via 802.11ac WiFi with varying signal strengths to
introduce realistic network heterogeneity.

## Results

### Convergence Analysis

FedHetero achieves 85.3% test accuracy on FEMNIST after 200 rounds,
compared to 79.1% for FedAvg and 82.4% for FedProx under identical
conditions. The convergence improvement is most pronounced in the first
100 rounds, where our adaptive weighting reduces the negative impact
of slow or unreliable clients.

### Communication Efficiency

By selectively compressing updates from bandwidth-limited clients and
allowing partial model updates, FedHetero reduces total bytes transferred
by 41% compared to the baseline while maintaining comparable accuracy.

### Ablation Study

We conducted ablation experiments to isolate the contribution of each
component of our adaptive weighting scheme:

| Component Removed     | FEMNIST Acc. | Shakespeare Acc. | CelebA Acc. |
|-----------------------|-------------|------------------|-------------|
| Full FedHetero        | 85.3%       | 54.7%            | 91.2%       |
| w/o Gradient Norm     | 82.1%       | 52.3%            | 89.8%       |
| w/o Capacity Estimate | 83.7%       | 53.1%            | 90.4%       |
| w/o Reliability Score | 84.0%       | 53.9%            | 90.7%       |

## Discussion

Our results indicate that accounting for gradient heterogeneity provides
the largest individual improvement, suggesting that data distribution
mismatch remains the dominant challenge in federated settings. The
computational capacity estimator contributes meaningful gains primarily
in scenarios with high device variance, while the reliability score
shows diminishing returns when network conditions are relatively stable.

A limitation of our approach is the additional metadata exchange required
for the adaptive weighting computation, which adds approximately 2KB per
client per round. In extremely privacy-sensitive settings, even this
metadata could reveal information about local data characteristics.

## Conclusion

We presented FedHetero, an adaptive federated learning algorithm that
addresses systems and data heterogeneity through dynamic client weighting.
Our experiments on standard benchmarks demonstrate consistent improvements
in convergence speed and communication efficiency. Future work will explore
integration with secure aggregation protocols and extension to cross-silo
federated settings with institutional participants.

## References

1. McMahan, B. et al. (2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. AISTATS.
2. Li, T. et al. (2020). Federated Optimization in Heterogeneous Networks. MLSys.
3. Karimireddy, S. P. et al. (2020). SCAFFOLD: Stochastic Controlled Averaging for Federated Learning. ICML.
4. Fallah, A. et al. (2020). Personalized Federated Learning with Moreau Envelopes. NeurIPS.
5. Dinh, C. T. et al. (2020). Personalized Federated Learning with Moreau Envelopes. NeurIPS.
"""

    with open(OUTPUT, 'w') as f:
        f.write(content.lstrip('\n'))

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the README.md file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
