"""
Initial Setup: Open Chrome with a PDF of the GCN paper (Kipf & Welling 2017)
Task ID: osworld_multi_apps_bookmark_authors_007
Domain: chrome (multi-app: Chrome + PDF)

Initial state:
- PDF of 'Semi-Supervised Classification with Graph Convolutional Networks' is created
- Chrome Bookmarks bar has NO 'Graph Learning Authors' folder
- Chrome opens the PDF (via file:// URL or PDF viewer)
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_007'
PDF_PATH = f'{WORKDIR}/{TASK_ID}.pdf'

CHROME_USER_DATA = os.path.expanduser('~/.config/google-chrome')
CHROME_DEFAULT = os.path.join(CHROME_USER_DATA, 'Default')
BOOKMARKS_FILE = os.path.join(CHROME_DEFAULT, 'Bookmarks')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def kill_chrome():
    """Kill any running Chrome instance before modifying config files."""
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)


def create_pdf():
    """Create a realistic PDF of the GCN paper."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_xy(15, 20)
    pdf.multi_cell(180, 10,
        'Semi-Supervised Classification with Graph Convolutional Networks',
        align='C')

    # Authors
    pdf.set_font('Helvetica', '', 12)
    pdf.ln(4)
    pdf.cell(0, 8, 'Thomas N. Kipf, Max Welling', align='C', new_x='LMARGIN', new_y='NEXT')

    # Institution
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 6, 'University of Amsterdam', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 6, '{t.n.kipf, m.welling}@uva.nl', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(6)

    # Abstract header
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Abstract', new_x='LMARGIN', new_y='NEXT')

    # Abstract body
    pdf.set_font('Helvetica', '', 10)
    abstract = (
        'We present a scalable approach for semi-supervised classification of nodes in a graph, '
        'where labels are only available for a small subset of nodes. We propose a simple and '
        'well-behaved layer-wise propagation rule for neural network models which operate directly '
        'on graphs and show how it can be motivated from a first-order approximation of spectral '
        'graph convolutions. Our model scales linearly in the number of graph edges and learns '
        'hidden layer representations that encode both local graph structure and features of nodes. '
        'In a number of experiments on citation networks and a knowledge graph dataset we demonstrate '
        'that our approach outperforms related methods by a significant margin.'
    )
    pdf.multi_cell(0, 6, abstract)

    pdf.ln(4)

    # Introduction
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '1  Introduction', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    intro = (
        'We consider the problem of classifying nodes (such as documents) in a graph (such as a '
        'citation network), where labels are only available for a small subset of nodes. This problem '
        'can be framed as graph-based semi-supervised learning, where label information is smoothed '
        'over the graph via some form of explicit graph-based regularization (Zhu et al., 2003; '
        'Zhou et al., 2004; Belkin et al., 2006; Weston et al., 2012), e.g. by using a graph '
        'Laplacian regularization term in the loss function:\n\n'
        '    L = L_0 + lambda * L_reg, with L_reg = sum_{i,j} A_{ij} ||f(X_i) - f(X_j)||^2 = f(X)^T Delta f(X)\n\n'
        'Here, L_0 denotes the supervised loss w.r.t. the labeled part of the graph, f(.) can be a '
        'neural network-like differentiable function, lambda is a weighing factor and X is a matrix '
        'of node feature vectors X_i. Delta = D - A denotes the unnormalized graph Laplacian of an '
        'undirected graph G = (V, E) with N nodes v_i in V, edges (v_i, v_j) in E, an adjacency '
        'matrix A (binary or weighted) and a degree matrix D_{ii} = sum_j A_{ij}.'
    )
    pdf.multi_cell(0, 6, intro)

    pdf.ln(4)

    # Method
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2  Fast Approximate Convolutions on Graphs', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    method = (
        'We consider a multi-layer Graph Convolutional Network (GCN) with the following layer-wise '
        'propagation rule:\n\n'
        '    H^(l+1) = sigma( D_tilde^{-1/2} A_tilde D_tilde^{-1/2} H^(l) W^(l) )\n\n'
        'Here, A_tilde = A + I_N is the adjacency matrix of the undirected graph G with added '
        'self-connections. I_N is the identity matrix, D_tilde_{ii} = sum_j A_tilde_{ij} and '
        'W^(l) is a layer-specific trainable weight matrix. sigma(.) denotes an activation function, '
        'such as the ReLU(.) = max(0, .). H^(l) in R^{N x D} is the matrix of activations in the '
        'l-th layer; H^(0) = X.'
    )
    pdf.multi_cell(0, 6, method)

    pdf.ln(4)

    # Experiments
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '3  Experiments', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    exp = (
        'We evaluate our proposed model on a number of benchmark tasks: semi-supervised document '
        'classification in citation networks and semi-supervised entity classification in a bipartite '
        'graph extracted from a knowledge graph. We follow the experimental setup of Yang et al. (2016), '
        'and use the same dataset splits. In addition, we demonstrate that our approach can be used for '
        'link prediction in citation networks.\n\n'
        'Dataset Statistics:\n'
        '  - Citeseer: 3327 nodes, 4732 edges, 6 classes, 3703 features\n'
        '  - Cora: 2708 nodes, 5429 edges, 7 classes, 1433 features\n'
        '  - Pubmed: 19717 nodes, 44338 edges, 3 classes, 500 features\n\n'
        'Our GCN model achieves state-of-the-art results on all three citation network datasets, '
        'outperforming all competing methods by a significant margin.'
    )
    pdf.multi_cell(0, 6, exp)

    pdf.ln(4)

    # Conclusion
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '4  Conclusion', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    conc = (
        'We have introduced a simple and well-behaved method for semi-supervised classification on '
        'graph-structured data that outperforms recent related methods on a number of benchmark datasets. '
        'Our method is based on an efficient variant of convolutional neural networks which operate '
        'directly on graphs. We motivate the choice of our propagation rule via a first-order '
        'approximation of localized spectral filters on graphs.'
    )
    pdf.multi_cell(0, 6, conc)

    pdf.ln(4)

    # References
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'References', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 9)
    refs = [
        'Belkin, M., Matveeva, I., and Niyogi, P. Regularization and semi-supervised learning on large graphs. In COLT, 2004.',
        'Defferrard, M., Bresson, X., and Vandergheynst, P. Convolutional neural networks on graphs with fast localized spectral filtering. In NIPS, 2016.',
        'Hammond, D. K., Vandergheynst, P., and Gribonval, R. Wavelets on graphs via spectral graph theory. Applied and Computational Harmonic Analysis, 2011.',
        'Kipf, T. N. and Welling, M. Variational graph auto-encoders. NIPS Workshop on Bayesian Deep Learning, 2016.',
        'Yang, Z., Cohen, W. W., and Salakhutdinov, R. Revisiting semi-supervised learning with graph embeddings. In ICML, 2016.',
        'Zhou, D., Bousquet, O., Lal, T. N., Weston, J., and Scholkopf, B. Learning with local and global consistency. In NIPS, 2004.',
    ]
    for ref in refs:
        pdf.multi_cell(0, 5, ref)
        pdf.ln(1)

    pdf.output(PDF_PATH)
    print(f'PDF created: {PDF_PATH}')


def setup_bookmarks():
    """Set up Chrome bookmarks without any 'Graph Learning Authors' folder."""
    os.makedirs(CHROME_DEFAULT, exist_ok=True)

    ts = str(int(time.time() * 1_000_000))

    bookmarks = {
        'checksum': '',
        'roots': {
            'bookmark_bar': {
                'children': [
                    {
                        'date_added': ts,
                        'date_last_used': '0',
                        'guid': 'da1b8d77-9d8e-4a2e-bcb4-0a07a5b0c001',
                        'id': '6',
                        'name': 'Google',
                        'type': 'url',
                        'url': 'https://www.google.com/'
                    },
                    {
                        'date_added': ts,
                        'date_last_used': '0',
                        'guid': 'da1b8d77-9d8e-4a2e-bcb4-0a07a5b0c002',
                        'id': '7',
                        'name': 'arXiv',
                        'type': 'url',
                        'url': 'https://arxiv.org/'
                    },
                ],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'da1b8d77-9d8e-4a2e-bcb4-0a07a5b0c000',
                'id': '1',
                'name': 'Bookmarks bar',
                'type': 'folder'
            },
            'other': {
                'children': [],
                'date_added': ts,
                'date_modified': '0',
                'guid': 'da1b8d77-9d8e-4a2e-bcb4-0a07a5b0d000',
                'id': '2',
                'name': 'Other bookmarks',
                'type': 'folder'
            },
            'synced': {
                'children': [],
                'date_added': ts,
                'date_modified': '0',
                'guid': 'da1b8d77-9d8e-4a2e-bcb4-0a07a5b0e000',
                'id': '3',
                'name': 'Mobile bookmarks',
                'type': 'folder'
            }
        },
        'version': 1
    }

    with open(BOOKMARKS_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=2)
    print(f'Bookmarks set up (no Graph Learning Authors folder): {BOOKMARKS_FILE}')


def create_initial():
    # Step 1: Create the PDF
    create_pdf()

    # Step 2: Kill Chrome before modifying config files
    kill_chrome()

    # Step 3: Set up bookmarks (initial state — no graph learning folder)
    setup_bookmarks()

    # Step 4: Launch Chrome with the PDF open
    # Using file:// URL to open the PDF in Chrome
    launch_gui(f'google-chrome --remote-debugging-port=1337 "file://{PDF_PATH}"', delay_sec=3.0)
    print('GUI_READY: launched Chrome with PDF open (DISPLAY=:0)')
    print(f'Initial setup complete.')
    print(f'  PDF: {PDF_PATH}')
    print(f'  Chrome open with: file://{PDF_PATH}')
    print(f'  Bookmarks bar: Google, arXiv (no Graph Learning Authors folder)')


create_initial()
