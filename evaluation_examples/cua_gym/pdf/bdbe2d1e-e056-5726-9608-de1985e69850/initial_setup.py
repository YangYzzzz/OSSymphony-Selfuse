"""
Initial Setup: Create a 6-page scanned PDF of a 1987 paper with no embedded text layer.
Task ID: pdf_res_013
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_013'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT_PDF = f'{PAPERS_DIR}/scanned_old_paper.pdf'


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


def create_scanned_page_image(page_num, title_text, body_text, width=2480, height=3508):
    """Create a raster image that looks like a scanned typewritten page.
    Resolution: ~300 DPI for A4 (2480x3508 pixels).
    Returns PIL Image object.
    """
    from PIL import Image, ImageDraw, ImageFont
    import random

    # Create slightly off-white background (simulating aged paper scan)
    bg_color = (245, 240, 230)
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Add slight noise/grain to simulate scan artifacts
    random.seed(42 + page_num)
    for _ in range(3000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        gray = random.randint(200, 240)
        draw.point((x, y), fill=(gray, gray, gray))

    # Use a monospace font to simulate typewriter text
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 48)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
    except Exception:
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 48)
            font_body = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 32)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 26)
        except Exception:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_small = ImageFont.load_default()

    text_color = (30, 30, 35)  # dark gray, not pure black (like typewriter ink)

    # Draw title text
    y_pos = 200
    for line in title_text.split('\n'):
        draw.text((200, y_pos), line.strip(), fill=text_color, font=font_title)
        y_pos += 65

    y_pos += 40

    # Draw body text
    for line in body_text.split('\n'):
        stripped = line.strip()
        if not stripped:
            y_pos += 30
            continue
        # Word-wrap long lines
        words = stripped.split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font_body)
            if bbox[2] > width - 400:
                draw.text((200, y_pos), current_line, fill=text_color, font=font_body)
                y_pos += 48
                current_line = word
            else:
                current_line = test_line
        if current_line:
            draw.text((200, y_pos), current_line, fill=text_color, font=font_body)
            y_pos += 48

    # Add page number at bottom
    page_str = f"- {page_num} -"
    bbox = draw.textbbox((0, 0), page_str, font=font_small)
    pw = bbox[2] - bbox[0]
    draw.text(((width - pw) // 2, height - 150), page_str, fill=text_color, font=font_small)

    return img


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    # Content for a fake 1987 paper on "Distributed Computing Architectures"
    pages_content = [
        # Page 1: Title and Abstract
        (
            "DISTRIBUTED COMPUTING ARCHITECTURES\nFOR LARGE-SCALE DATA PROCESSING",
            """R. M. Henderson and J. K. Whitfield
Department of Computer Science
Stanford University, Stanford, CA 94305

Published in: Proceedings of the IEEE International
Conference on Distributed Computing Systems, 1987

Abstract

The rapid growth of computational demands in scientific
research and commercial applications has necessitated the
development of distributed computing architectures capable
of handling large-scale data processing tasks. In this paper,
we present a novel framework for distributing computational
workloads across heterogeneous processor networks. Our
approach utilizes a hierarchical task decomposition strategy
combined with dynamic load balancing to achieve near-linear
speedup for a class of parallelizable problems. Experimental
results on a 64-node network demonstrate throughput
improvements of 47x compared to single-processor execution,
with communication overhead limited to approximately 8.3
percent of total execution time. We further discuss the
implications of our findings for the design of future
distributed systems and outline several promising directions
for subsequent research.

Keywords: distributed computing, parallel processing,
load balancing, task decomposition, heterogeneous networks"""
        ),

        # Page 2: Introduction
        (
            "1. INTRODUCTION",
            """The increasing complexity of computational problems
in fields such as meteorological modeling, molecular
dynamics simulation, and large-scale database management
has created an urgent need for computing systems that
can deliver substantially higher throughput than
conventional single-processor architectures (Smith, 1984;
Tanaka and Mori, 1985).

While shared-memory multiprocessor systems offer one
path toward increased performance, their scalability
is fundamentally limited by memory bus contention and
the practical difficulties of maintaining cache coherence
across large numbers of processors (Dubois et al., 1986).

Distributed computing architectures, in which autonomous
processors communicate via message passing over a network,
offer a more scalable alternative. However, achieving
efficient utilization of distributed resources requires
careful attention to several challenging problems:

(a) Task decomposition: dividing a computational problem
into subtasks that can be executed concurrently with
minimal inter-task dependencies.

(b) Load balancing: assigning subtasks to processors
in a manner that minimizes idle time and ensures
equitable distribution of computational burden.

(c) Communication optimization: minimizing the volume
and frequency of inter-processor communication, which
constitutes the primary source of overhead in distributed
systems.

(d) Fault tolerance: ensuring that the system can
continue to operate correctly in the presence of
individual processor or network failures.

In this paper, we address problems (a) through (c) within
the context of a hierarchical task decomposition framework.
Our approach builds upon the foundational work of Foster
(1982) and extends it to accommodate heterogeneous
processor configurations."""
        ),

        # Page 3: System Architecture
        (
            "2. SYSTEM ARCHITECTURE",
            """2.1 Hardware Configuration

Our experimental testbed consists of 64 processing nodes
interconnected via a hypercube topology network. Each node
contains a Motorola 68020 processor operating at 16 MHz,
equipped with 4 megabytes of local memory and a dedicated
network interface controller. The inter-node communication
links operate at a sustained bandwidth of 10 megabits per
second, with measured latency of 0.8 milliseconds for
short messages (64 bytes or fewer).

Table 1. Hardware specifications of the test network

  Component          Specification
  ------------------------------------------
  Processor          Motorola 68020, 16 MHz
  Local Memory       4 MB DRAM
  Network Topology   6-dimensional hypercube
  Link Bandwidth     10 Mbps sustained
  Message Latency    0.8 ms (64-byte msg)
  Total Nodes        64

2.2 Software Architecture

The software architecture comprises three principal layers:

(i) The Communication Layer provides reliable message
delivery with automatic retransmission and flow control.
It implements both synchronous and asynchronous message
passing primitives, as well as collective operations
including broadcast, scatter, and gather.

(ii) The Resource Management Layer maintains a global
view of processor availability and workload distribution.
It implements the dynamic load balancing algorithm
described in Section 3.2.

(iii) The Application Layer provides the programming
interface through which users specify task graphs and
data dependencies. Applications are expressed as directed
acyclic graphs (DAGs) of computational tasks."""
        ),

        # Page 4: Algorithm
        (
            "3. ALGORITHMS",
            """3.1 Hierarchical Task Decomposition

Given a computational problem P, we construct a task
tree T(P) through recursive decomposition. At each level
of the tree, a task is divided into subtasks based on
data partitioning, functional decomposition, or a
combination of both strategies.

Definition 1. A task tree T = (V, E) is a rooted tree
where each vertex v in V represents a computational
subtask and each edge (u, v) in E indicates that v is
a child subtask of u.

The decomposition proceeds according to the following
algorithm:

Algorithm 1: DECOMPOSE(task, depth)
  Input: task T, maximum depth d
  Output: task tree rooted at T
  1. if depth >= d or |T| < threshold then
  2.     return leaf(T)
  3. end if
  4. (T1, T2, ..., Tk) <- PARTITION(T)
  5. for each Ti do
  6.     child_i <- DECOMPOSE(Ti, depth + 1)
  7. end for
  8. return node(T, child_1, ..., child_k)

The PARTITION function employs domain-specific knowledge
to identify natural decomposition boundaries. For matrix
computations, this typically involves block partitioning;
for graph problems, we use recursive bisection based on
the Kernighan-Lin heuristic (Kernighan and Lin, 1970).

3.2 Dynamic Load Balancing

Our load balancing strategy employs a distributed work-
stealing approach. Each processor maintains a local deque
of pending tasks. When a processor's deque becomes empty,
it requests work from a randomly selected peer processor.

The overhead of work-stealing is bounded by O(P * D * log N),
where P is the number of processors, D is the maximum task
depth, and N is the total number of tasks (Blumofe and
Leiserson, 1999 -- note: this bound was later formalized).

Empirically, we observe that the communication overhead
attributable to load balancing constitutes less than 2.1
percent of total execution time for problems with more
than 10,000 leaf tasks distributed across 64 processors."""
        ),

        # Page 5: Results
        (
            "4. EXPERIMENTAL RESULTS",
            """We evaluate our framework on three benchmark applications:
(A) dense matrix multiplication, (B) discrete event
simulation, and (C) database join operations.

Table 2. Speedup results (relative to single processor)

  Processors    Matrix    Simulation    DB Join
  ---------------------------------------------------
       4          3.8        3.6          3.4
       8          7.4        6.9          6.5
      16         14.6       13.2         12.4
      32         28.1       24.8         23.1
      64         52.3       41.7         38.9

Table 3. Communication overhead as percentage of runtime

  Processors    Matrix    Simulation    DB Join
  ---------------------------------------------------
       4          1.2%       2.4%        3.1%
       8          1.8%       3.1%        4.2%
      16          2.7%       4.3%        5.8%
      32          4.1%       6.2%        7.9%
      64          6.4%       8.3%       11.2%

The matrix multiplication benchmark exhibits near-linear
speedup due to its regular communication pattern and high
computation-to-communication ratio. The discrete event
simulation shows somewhat lower efficiency owing to its
irregular task structure and the resulting load imbalance.
The database join operation is most sensitive to
communication overhead, as it requires substantial data
redistribution during the hash partitioning phase.

Figure 1 presents the speedup curves graphically. The
dashed line indicates ideal linear speedup for reference.
Our framework achieves efficiency (speedup/processors)
above 0.73 for all benchmarks at 64 processors, with
matrix multiplication reaching 0.82 efficiency."""
        ),

        # Page 6: Conclusion and References
        (
            "5. CONCLUSION AND FUTURE WORK",
            """We have presented a distributed computing framework
based on hierarchical task decomposition and dynamic
load balancing that achieves substantial speedup across
a range of application domains. Our experimental results
on a 64-node hypercube network demonstrate that the
approach is practical and efficient, with communication
overhead remaining manageable even at the largest
processor counts tested.

Several directions for future research merit attention.
First, the extension of our framework to support fault
tolerance through checkpoint-restart mechanisms would
significantly enhance its applicability to long-running
computations. Second, the integration of heterogeneous
processor types (e.g., vector processors for numerically
intensive subtasks) could further improve overall system
throughput. Third, the development of compiler-based
tools for automatic task decomposition would reduce the
programming burden on application developers.

REFERENCES

Blumofe, R. D. and Leiserson, C. E. (1993). Space-
  efficient scheduling of multithreaded computations.
  SIAM J. Comput., 27(1): 202-229.

Dubois, M., Scheurich, C., and Briggs, F. A. (1986).
  Memory access buffering in multiprocessors. Proc.
  13th Annual Intl. Symp. Computer Architecture.

Foster, I. T. (1982). Task decomposition strategies for
  concurrent computation. Technical Report CS-82-14,
  Caltech.

Kernighan, B. W. and Lin, S. (1970). An efficient
  heuristic procedure for partitioning graphs. Bell
  System Technical Journal, 49(2): 291-307.

Smith, B. J. (1984). Architecture and applications of
  the HEP multiprocessor computer system. SPIE Real-
  Time Signal Processing IV, 298: 241-248.

Tanaka, H. and Mori, S. (1985). Parallel algorithms
  for computational fluid dynamics on distributed
  memory machines. J. Comp. Physics, 61(3): 452-471."""
        ),
    ]

    # Build the PDF: each page is a raster image (no text layer)
    import pymupdf

    doc = pymupdf.open()

    for i, (title, body) in enumerate(pages_content, 1):
        img = create_scanned_page_image(i, title, body)

        # Save image to temporary bytes
        import io
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        # Create a page and insert the image as a full-page raster
        page = doc.new_page(width=595, height=842)  # A4 in points
        page.insert_image(page.rect, stream=img_bytes)

    doc.save(OUTPUT_PDF)
    doc.close()

    # Verify no text layer exists
    verify_doc = pymupdf.open(OUTPUT_PDF)
    for i in range(verify_doc.page_count):
        text = verify_doc[i].get_text("text").strip()
        if text:
            print(f"WARNING: Page {i+1} has embedded text: {text[:50]}...")
    verify_doc.close()

    print(f'Initial file created: {OUTPUT_PDF}')
    print(f'Pages: 6 (raster images, no text layer)')

    # Ensure ocr_output.txt does NOT exist (task is to create it)
    ocr_output = f'{PAPERS_DIR}/ocr_output.txt'
    if os.path.exists(ocr_output):
        os.remove(ocr_output)
        print(f'Removed pre-existing {ocr_output}')

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
