"""
Initial Setup: Create a 20-page CS textbook chapter PDF with no bookmarks.
Task ID: pdf_gf2_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import shutil

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_010'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/textbook_ch3.pdf'
CANONICAL = f'{WORKDIR}/{TASK_ID}.pdf'


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    W, H = 595, 842  # A4
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 523
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 770
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # --- Content for each page ---
    # Chapter structure:
    # Pages 1-7: Arrays and Lists
    # Pages 8-11: Trees and Graphs (intro + Binary Trees)
    # Pages 12-14: Graph Algorithms
    # Pages 15-20: Hash Tables

    chapter_content = [
        # Page 1: Chapter title + Arrays intro
        {
            "title": "Chapter 3: Data Structures",
            "subtitle": "3.1 Arrays and Lists",
            "body": (
                "Data structures are fundamental building blocks of computer science. They provide "
                "organized ways to store, access, and manipulate data efficiently. The choice of data "
                "structure can dramatically affect the performance of an algorithm, sometimes making the "
                "difference between a solution that runs in milliseconds and one that takes hours.\n\n"
                "An array is a contiguous block of memory that stores elements of the same type. "
                "Arrays provide O(1) random access to elements by index, making them ideal for "
                "situations where frequent lookups are required. In languages like C and Java, arrays "
                "have a fixed size determined at allocation time. Modern languages such as Python and "
                "JavaScript provide dynamic arrays that automatically resize when capacity is exceeded.\n\n"
                "The time complexity of common array operations is as follows: accessing an element "
                "by index takes O(1) time, searching for an element takes O(n) in the worst case for "
                "unsorted arrays, insertion at the end takes amortized O(1) for dynamic arrays, and "
                "insertion at an arbitrary position takes O(n) due to shifting elements."
            ),
        },
        # Page 2: Arrays continued
        {
            "subtitle": "3.1.1 Static Arrays",
            "body": (
                "Static arrays allocate a fixed amount of memory at compile time or initialization. "
                "Consider a scenario where Professor Elena Rodriguez is teaching her Algorithm Design "
                "course at Stanford. She presents the following example to illustrate memory allocation:\n\n"
                "When we declare int scores[100] in C, the system allocates exactly 400 bytes of "
                "contiguous memory (assuming 4-byte integers). This memory block is placed on the stack "
                "if declared inside a function, or in the data segment if declared globally.\n\n"
                "The advantages of static arrays include predictable memory usage, cache-friendly access "
                "patterns due to spatial locality, and zero overhead for memory management. However, "
                "their fixed size means wasted memory if the array is not fully utilized, or buffer "
                "overflow vulnerabilities if more elements are inserted than the array can hold.\n\n"
                "Example: Consider a student grade tracking system. Dr. Rodriguez stores midterm "
                "scores for her class of 85 students: float midterm_scores[85] = {92.5, 87.3, 95.1, "
                "78.9, 91.0, 83.7, 88.4, 76.2, 94.8, 85.6, ...}. Each score can be accessed in "
                "constant time, making statistical calculations straightforward."
            ),
        },
        # Page 3: Dynamic arrays
        {
            "subtitle": "3.1.2 Dynamic Arrays",
            "body": (
                "Dynamic arrays solve the fixed-size limitation by automatically growing when more "
                "space is needed. The most common implementation strategy is to double the array's "
                "capacity whenever it becomes full, a technique known as geometric expansion.\n\n"
                "Consider the ArrayList implementation in Java or the vector class in C++. When an "
                "ArrayList is created with an initial capacity of 10 and the 11th element is added, "
                "the system allocates a new array of size 20, copies all existing elements, and frees "
                "the old memory. This doubling strategy ensures that the amortized cost of insertion "
                "remains O(1), even though individual insertions may occasionally take O(n) time.\n\n"
                "Dr. Marcus Chen at MIT demonstrated this concept using a real-world analogy: imagine "
                "a restaurant that starts with 10 tables. When all tables are occupied and a new "
                "reservation arrives, the restaurant moves to a space with 20 tables. Each subsequent "
                "move doubles the capacity, so moves become increasingly rare relative to the number "
                "of customers served.\n\n"
                "The load factor, defined as n/capacity where n is the current number of elements, "
                "determines when resizing occurs. Most implementations resize when the load factor "
                "exceeds 0.75, balancing memory efficiency with resize frequency."
            ),
        },
        # Page 4: Linked Lists
        {
            "subtitle": "3.1.3 Linked Lists",
            "body": (
                "A linked list is a sequence of nodes where each node contains data and a reference "
                "(pointer) to the next node. Unlike arrays, linked lists do not require contiguous "
                "memory, allowing flexible memory allocation and efficient insertion and deletion.\n\n"
                "Singly linked lists contain nodes with a single 'next' pointer. Insertion at the head "
                "takes O(1) time, while insertion at an arbitrary position requires O(n) traversal. "
                "The trade-off is that random access is no longer O(1); accessing the k-th element "
                "requires traversing k nodes from the head.\n\n"
                "Research by Dr. Amara Okafor at Carnegie Mellon showed that linked lists outperform "
                "arrays in scenarios with frequent insertions and deletions at arbitrary positions, "
                "particularly when the dataset size is unpredictable. In her 2023 benchmarks using "
                "real-world workloads from database query processing, linked lists reduced insertion "
                "latency by 47% compared to dynamic arrays when the insertion point was uniformly "
                "distributed across the data structure.\n\n"
                "However, the pointer overhead in linked lists (8 bytes per node on 64-bit systems) "
                "and poor cache performance due to non-contiguous memory layout make them less "
                "suitable for workloads dominated by sequential access patterns."
            ),
        },
        # Page 5: Doubly linked lists
        {
            "subtitle": "3.1.4 Doubly Linked Lists",
            "body": (
                "Doubly linked lists extend the singly linked list by adding a 'prev' pointer to "
                "each node, enabling bidirectional traversal. This additional pointer increases memory "
                "overhead but provides significant operational benefits.\n\n"
                "Key operations and their complexities:\n"
                "  - Insert at head: O(1)\n"
                "  - Insert at tail: O(1) with tail pointer\n"
                "  - Delete a known node: O(1)\n"
                "  - Search: O(n)\n"
                "  - Reverse traversal: O(n)\n\n"
                "The Java LinkedList class implements a doubly linked list and serves as the backing "
                "data structure for both the List and Deque interfaces. Consider a music playlist "
                "application developed by Sophia Tanaka at Spotify's engineering team. The playlist "
                "uses a doubly linked list to allow users to navigate forward and backward through "
                "songs, with O(1) insertion when adding songs to the beginning or end of the queue.\n\n"
                "Circular doubly linked lists connect the tail's next pointer to the head and the "
                "head's prev pointer to the tail, forming a ring structure. This variant is useful "
                "for implementing round-robin schedulers and buffer pools in operating systems."
            ),
        },
        # Page 6: Skip lists
        {
            "subtitle": "3.1.5 Skip Lists",
            "body": (
                "Skip lists are a probabilistic data structure that layers multiple sorted linked "
                "lists to achieve O(log n) average-case search, insertion, and deletion times. "
                "Invented by William Pugh in 1989, skip lists provide an elegant alternative to "
                "balanced binary search trees.\n\n"
                "The structure consists of a base-level sorted linked list containing all elements. "
                "Above it, higher levels contain subsets of elements, where each element at level i "
                "appears at level i+1 with probability p (typically 0.5). This creates an express "
                "lane effect: searches start at the highest level and drop down when the next "
                "element would overshoot the target.\n\n"
                "Professor James Whitfield at the University of Washington uses skip lists in his "
                "distributed systems course to teach students about concurrent data structures. "
                "Skip lists are particularly amenable to lock-free concurrent implementations "
                "because insertions at different positions can proceed independently without "
                "the complex rotations required by balanced trees.\n\n"
                "Real-world applications include Redis sorted sets, LevelDB and RocksDB memtables, "
                "and Apache Lucene's posting list indexing. In Redis, the sorted set implementation "
                "uses a skip list with a maximum of 32 levels and p = 0.25, optimizing for memory "
                "efficiency while maintaining logarithmic performance guarantees."
            ),
        },
        # Page 7: Array vs List comparison
        {
            "subtitle": "3.1.6 Comparative Analysis",
            "body": (
                "Choosing between arrays and linked lists requires careful analysis of the specific "
                "use case. The table below summarizes key trade-offs:\n\n"
                "Operation        | Array    | Linked List\n"
                "Access by index  | O(1)     | O(n)\n"
                "Search           | O(n)     | O(n)\n"
                "Insert at start  | O(n)     | O(1)\n"
                "Insert at end    | O(1)*    | O(1)**\n"
                "Insert at middle | O(n)     | O(1)***\n"
                "Memory overhead  | Low      | High\n"
                "Cache performance| Excellent| Poor\n\n"
                "* Amortized for dynamic arrays\n"
                "** With tail pointer\n"
                "*** After locating the position\n\n"
                "A 2024 benchmark study by the Systems Research Group at ETH Zurich compared array "
                "and linked list performance on modern hardware with 256 KB L2 cache and 12 MB L3 "
                "cache. For datasets fitting in L2 cache (up to approximately 32,000 32-bit integers), "
                "arrays outperformed linked lists by a factor of 8-12x for sequential access due to "
                "hardware prefetching. However, for insertion-heavy workloads with random positions, "
                "linked lists matched or exceeded array performance when the dataset exceeded L3 cache "
                "capacity, as the cost of element shifting in arrays dominated cache miss penalties."
            ),
        },
        # Page 8: Trees and Graphs intro
        {
            "title": None,
            "subtitle": "3.2 Trees and Graphs",
            "body": (
                "Trees are hierarchical data structures consisting of nodes connected by edges. "
                "Each tree has exactly one root node, and every non-root node has exactly one parent. "
                "Trees are fundamental to computer science, appearing in file systems, databases, "
                "compiler design, and network routing.\n\n"
                "A tree with n nodes has exactly n-1 edges. The depth of a node is the number of "
                "edges from the root to that node. The height of a tree is the maximum depth among "
                "all nodes. A binary tree is a special case where each node has at most two children, "
                "conventionally called the left child and right child.\n\n"
                "Graphs generalize trees by allowing cycles and multiple paths between nodes. "
                "Formally, a graph G = (V, E) consists of a set of vertices V and a set of edges E, "
                "where each edge connects two vertices. Graphs can be directed (edges have direction) "
                "or undirected (edges are bidirectional), weighted (edges have associated costs) or "
                "unweighted.\n\n"
                "Dr. Priya Krishnamurthy's research group at IIT Bombay has catalogued over 200 "
                "distinct graph algorithms used in production systems, spanning domains from social "
                "network analysis to bioinformatics. Their survey, published in ACM Computing Surveys "
                "(2024), identified tree-based structures as the most commonly used subset, appearing "
                "in 73% of the systems studied."
            ),
        },
        # Page 9: Binary Trees (under Trees and Graphs, 3rd level)
        {
            "subtitle": "3.2.1 Binary Trees",
            "body": (
                "Binary trees restrict each node to at most two children. This constraint enables "
                "efficient algorithms for searching, sorting, and indexing. The three primary "
                "traversal orders for binary trees are:\n\n"
                "In-order traversal visits the left subtree, then the current node, then the right "
                "subtree. For a binary search tree (BST), in-order traversal produces elements in "
                "sorted ascending order. This property makes BSTs ideal for implementing ordered "
                "sets and maps.\n\n"
                "Pre-order traversal visits the current node before its children, useful for "
                "creating a copy of the tree or generating prefix expressions from expression trees. "
                "Post-order traversal visits children before the parent, commonly used for tree "
                "deletion and evaluating postfix expressions.\n\n"
                "Binary Search Trees (BSTs) maintain the invariant that for every node, all values "
                "in the left subtree are less than the node's value, and all values in the right "
                "subtree are greater. This invariant enables O(log n) search in a balanced tree. "
                "However, a BST can degenerate to O(n) if elements are inserted in sorted order, "
                "producing a structure equivalent to a linked list.\n\n"
                "Self-balancing BSTs such as AVL trees and Red-Black trees prevent this degeneration "
                "by performing rotations after insertions and deletions to maintain logarithmic height."
            ),
        },
        # Page 10: AVL and Red-Black Trees
        {
            "subtitle": "3.2.1.1 AVL Trees",
            "body": (
                "AVL trees, named after inventors Adelson-Velsky and Landis (1962), maintain strict "
                "balance by ensuring that for every node, the heights of its left and right subtrees "
                "differ by at most one. This balance factor constraint guarantees O(log n) height, "
                "and consequently O(log n) time for search, insertion, and deletion.\n\n"
                "When an insertion or deletion violates the balance condition, AVL trees restore "
                "balance through rotations. There are four cases:\n\n"
                "  Left-Left (LL): Single right rotation\n"
                "  Right-Right (RR): Single left rotation\n"
                "  Left-Right (LR): Left rotation on left child, then right rotation\n"
                "  Right-Left (RL): Right rotation on right child, then left rotation\n\n"
                "Professor Yuki Tanaka at the University of Tokyo published an extensive comparison "
                "of AVL and Red-Black trees in the Journal of Algorithms (2023). Her experiments "
                "on datasets ranging from 10,000 to 100 million elements showed that AVL trees "
                "perform fewer comparisons per search (approximately 1.44 log2(n) vs. 2 log2(n) "
                "for Red-Black trees) but require more rotations per insertion (up to 2 rotations "
                "vs. at most 2 for Red-Black trees, though Red-Black trees may need up to 3 "
                "recolorings).\n\n"
                "In practice, AVL trees are preferred for read-heavy workloads where search "
                "performance is critical, such as in-memory databases and real-time systems."
            ),
        },
        # Page 11: B-Trees
        {
            "subtitle": "3.2.1.2 B-Trees and B+ Trees",
            "body": (
                "B-trees are self-balancing tree structures designed for systems that read and write "
                "large blocks of data, such as databases and file systems. Unlike binary trees, "
                "B-trees can have many children per node, reducing tree height and minimizing "
                "disk I/O operations.\n\n"
                "A B-tree of order m has the following properties:\n"
                "  - Each node has at most m children\n"
                "  - Each non-root internal node has at least ceil(m/2) children\n"
                "  - The root has at least 2 children (if not a leaf)\n"
                "  - All leaves appear at the same level\n"
                "  - A node with k children contains k-1 keys\n\n"
                "B+ trees, a variant used extensively in database indexing, store all data in leaf "
                "nodes and maintain a linked list connecting consecutive leaves. This design "
                "optimizes range queries, as sequential data can be retrieved by traversing the "
                "leaf chain without revisiting internal nodes.\n\n"
                "MySQL's InnoDB storage engine uses B+ trees for both primary and secondary indexes. "
                "Senior Database Engineer Wei Zhang at Oracle Corporation notes that a B+ tree with "
                "order 200 and three levels of internal nodes can index approximately 8 million "
                "records with only three disk seeks per lookup, compared to approximately 23 seeks "
                "for a binary tree indexing the same number of records."
            ),
        },
        # Page 12: Graph Algorithms (3rd level under Trees and Graphs)
        {
            "subtitle": "3.2.2 Graph Algorithms",
            "body": (
                "Graph algorithms are essential tools for solving problems involving relationships "
                "and connections. The two fundamental graph traversal algorithms are Breadth-First "
                "Search (BFS) and Depth-First Search (DFS).\n\n"
                "BFS explores vertices level by level, using a queue to track the frontier of "
                "unexplored vertices. Starting from a source vertex s, BFS visits all vertices at "
                "distance 1, then all vertices at distance 2, and so on. BFS naturally computes "
                "shortest paths in unweighted graphs and runs in O(V + E) time.\n\n"
                "DFS explores as far as possible along each branch before backtracking, using a "
                "stack (explicit or implicit via recursion). DFS is the foundation for many advanced "
                "algorithms including topological sorting, strongly connected component detection "
                "(Tarjan's algorithm), and cycle detection.\n\n"
                "Dr. Rachel Goldberg at the Weizmann Institute of Science developed an optimized "
                "parallel BFS implementation for large-scale graph processing. Her algorithm, "
                "published at SIGMOD 2024, achieved 3.7x speedup on a 64-core machine for social "
                "network graphs with over 1 billion edges, by partitioning the frontier across "
                "processor cores and using lock-free concurrent queues to minimize synchronization "
                "overhead."
            ),
        },
        # Page 13: Shortest path algorithms
        {
            "subtitle": "3.2.2.1 Shortest Path Algorithms",
            "body": (
                "Finding the shortest path between vertices is one of the most studied problems in "
                "graph theory. Several classical algorithms address different variants of this problem.\n\n"
                "Dijkstra's Algorithm (1959) computes single-source shortest paths in graphs with "
                "non-negative edge weights. Using a min-heap priority queue, Dijkstra's algorithm "
                "runs in O((V + E) log V) time. The algorithm greedily selects the unvisited vertex "
                "with the smallest tentative distance, relaxes all its outgoing edges, and repeats.\n\n"
                "The Bellman-Ford algorithm handles graphs with negative edge weights (but not "
                "negative cycles) in O(VE) time. It relaxes all edges V-1 times, guaranteeing "
                "convergence for any graph without negative cycles. An additional pass can detect "
                "negative cycles: if any edge can still be relaxed, a negative cycle exists.\n\n"
                "The Floyd-Warshall algorithm computes all-pairs shortest paths in O(V^3) time using "
                "dynamic programming. Despite its cubic complexity, Floyd-Warshall is efficient for "
                "dense graphs and is widely used in network routing protocols.\n\n"
                "In 2023, researchers at Google Brain published the A* Neural Heuristic, a learned "
                "heuristic function for the A* algorithm that reduced pathfinding time by 62% on "
                "road networks compared to traditional Euclidean distance heuristics, while "
                "maintaining optimality guarantees."
            ),
        },
        # Page 14: Minimum spanning trees
        {
            "subtitle": "3.2.2.2 Minimum Spanning Trees",
            "body": (
                "A minimum spanning tree (MST) of a connected, weighted, undirected graph is a "
                "subset of edges that connects all vertices with the minimum total edge weight "
                "and without forming cycles.\n\n"
                "Kruskal's Algorithm sorts all edges by weight and greedily adds the lightest edge "
                "that doesn't form a cycle. Using a Union-Find data structure for cycle detection, "
                "Kruskal's algorithm runs in O(E log E) time. This approach is particularly efficient "
                "for sparse graphs where E is close to V.\n\n"
                "Prim's Algorithm grows the MST from a starting vertex by repeatedly adding the "
                "lightest edge connecting a tree vertex to a non-tree vertex. With a Fibonacci heap, "
                "Prim's algorithm achieves O(E + V log V) time, making it faster than Kruskal's for "
                "dense graphs.\n\n"
                "Applications of MSTs include:\n"
                "  - Network design: Connecting cities with minimum-cost cable\n"
                "  - Cluster analysis: MST-based clustering removes longest edges\n"
                "  - Approximation algorithms: MST provides 2-approximation for TSP\n"
                "  - Image segmentation: Felzenszwalb's algorithm uses MST-based merging\n\n"
                "Dr. Carlos Mendez at UNAM demonstrated that for telecommunications network planning "
                "in Mexico City, MST-based optimization reduced infrastructure costs by 23% while "
                "maintaining connectivity requirements for 4.2 million endpoints."
            ),
        },
        # Page 15: Hash Tables intro
        {
            "subtitle": "3.3 Hash Tables",
            "body": (
                "Hash tables provide average-case O(1) time complexity for insertion, deletion, and "
                "lookup operations, making them one of the most practical data structures in computer "
                "science. A hash table uses a hash function to map keys to indices in an underlying "
                "array, called the hash table or bucket array.\n\n"
                "The quality of a hash function directly impacts performance. An ideal hash function "
                "distributes keys uniformly across the table, minimizing collisions (multiple keys "
                "mapping to the same index). Common hash functions for integers include the division "
                "method h(k) = k mod m and the multiplication method h(k) = floor(m * (k * A mod 1)) "
                "where A is an irrational constant (Knuth suggests A = (sqrt(5) - 1) / 2).\n\n"
                "For string keys, polynomial rolling hash functions are standard: h(s) = sum(s[i] * p^i) "
                "mod m, where p is a prime (commonly 31 or 37) and m is the table size. Java's "
                "String.hashCode() uses this approach with p = 31.\n\n"
                "The load factor alpha = n/m (number of elements divided by table size) is a critical "
                "parameter. Most implementations resize when alpha exceeds a threshold: Java's "
                "HashMap resizes at alpha = 0.75, Python's dict at alpha = 2/3, and Go's map at "
                "alpha = 6.5 (using a different collision strategy)."
            ),
        },
        # Page 16: Collision resolution
        {
            "subtitle": "3.3.1 Collision Resolution Strategies",
            "body": (
                "When two keys hash to the same index, a collision resolution strategy determines "
                "how to handle the conflict. The two primary approaches are chaining and open "
                "addressing.\n\n"
                "Separate Chaining stores all elements that hash to the same index in a linked list "
                "(or other secondary data structure) at that bucket. Insertion is always O(1) since "
                "we simply prepend to the chain. Search and deletion take O(1 + alpha) expected time, "
                "where alpha is the load factor. Chaining handles high load factors gracefully, "
                "with performance degrading linearly.\n\n"
                "Open Addressing stores all elements directly in the table array. When a collision "
                "occurs, the algorithm probes for the next empty slot. Three common probing strategies "
                "are:\n\n"
                "  Linear probing: h(k, i) = (h(k) + i) mod m\n"
                "  Quadratic probing: h(k, i) = (h(k) + c1*i + c2*i^2) mod m\n"
                "  Double hashing: h(k, i) = (h1(k) + i * h2(k)) mod m\n\n"
                "Linear probing suffers from primary clustering, where consecutive occupied slots "
                "form long runs that slow subsequent operations. Quadratic probing reduces clustering "
                "but may not probe all table positions. Double hashing provides the most uniform "
                "distribution but requires computing two hash functions.\n\n"
                "Senior Software Engineer Kenji Yamamoto at Google described in a 2024 tech talk how "
                "Google's Swiss Table implementation uses open addressing with SIMD-optimized probing, "
                "achieving 2-3x faster lookups compared to traditional chaining-based hash maps."
            ),
        },
        # Page 17: Cuckoo hashing
        {
            "subtitle": "3.3.2 Cuckoo Hashing",
            "body": (
                "Cuckoo hashing, introduced by Pagh and Rodler (2001), guarantees O(1) worst-case "
                "lookup time by using two or more hash functions and allowing elements to be displaced "
                "during insertion.\n\n"
                "The algorithm uses two hash tables T1 and T2 with independent hash functions h1 and "
                "h2. To insert key k: place k at T1[h1(k)]. If that slot is occupied by key k', "
                "displace k' to its alternative location T2[h2(k')]. If that slot is also occupied, "
                "the displaced key is moved to its alternative location, creating a chain of "
                "displacements. If the chain exceeds a threshold length (typically O(log n)), the "
                "tables are rebuilt with new hash functions.\n\n"
                "The expected amortized insertion time is O(1) when the total load factor (across "
                "both tables) is below approximately 50%. With three hash functions and three tables, "
                "the load factor threshold increases to about 91%.\n\n"
                "Researcher Dr. Anna Bergstrom at Uppsala University extended cuckoo hashing to "
                "support concurrent operations in her 2024 VLDB paper. Her lock-free cuckoo hash "
                "table achieves 850 million operations per second on a 128-core server, making it "
                "suitable for high-performance key-value stores.\n\n"
                "MemSQL (now SingleStore) uses cuckoo hashing in its in-memory storage engine for "
                "point queries, achieving sub-microsecond latency for individual key lookups."
            ),
        },
        # Page 18: Perfect hashing
        {
            "subtitle": "3.3.3 Perfect Hashing",
            "body": (
                "Perfect hashing constructs a hash function with zero collisions for a known set of "
                "keys. This is achievable when the key set is static (known in advance and does not "
                "change). Perfect hash functions guarantee O(1) worst-case lookup with no collision "
                "resolution overhead.\n\n"
                "Minimal perfect hashing (MPH) maps n keys to exactly n consecutive integers "
                "[0, n-1] with no gaps and no collisions. The Czech, Havas, and Majewski (CHM) "
                "algorithm and the Botelho, Pagh, and Ziviani (BPZ) algorithm are widely used "
                "methods for constructing MPH functions.\n\n"
                "The construction process involves:\n"
                "  1. Building a random hypergraph from the key set\n"
                "  2. Checking if the hypergraph is acyclic\n"
                "  3. If acyclic, assigning values to graph vertices to create the hash function\n"
                "  4. If cyclic, retry with different random seeds\n\n"
                "The CMPH library (http://cmph.sourceforge.net) implements several MPH algorithms "
                "and is used in production systems at Facebook for static dictionary lookups. "
                "Dr. Fabiano Botelho's CHD algorithm, implemented in CMPH, constructs MPH functions "
                "for 1 billion keys in under 3 minutes, using approximately 2.07 bits per key of "
                "space overhead.\n\n"
                "Applications include compiler keyword recognition, network packet classification, "
                "and static configuration lookups in embedded systems."
            ),
        },
        # Page 19: Bloom filters
        {
            "subtitle": "3.3.4 Probabilistic Hash Structures",
            "body": (
                "Bloom filters are space-efficient probabilistic data structures that test whether "
                "an element is a member of a set. They allow false positives but never false negatives, "
                "making them ideal for filtering operations where occasional false alarms are acceptable.\n\n"
                "A Bloom filter uses a bit array of m bits and k independent hash functions. To insert "
                "an element, compute all k hash values and set the corresponding bits to 1. To query, "
                "check if all k positions are set. If any bit is 0, the element is definitely not in "
                "the set. If all bits are 1, the element is probably in the set (with a calculable "
                "false positive rate).\n\n"
                "The optimal number of hash functions is k = (m/n) * ln(2), where n is the expected "
                "number of elements. With these parameters, the false positive rate is approximately "
                "(1 - e^(-kn/m))^k, which equals (0.6185)^(m/n) at the optimal k.\n\n"
                "Counting Bloom filters extend the basic structure by replacing each bit with a "
                "counter, supporting deletion operations. Cuckoo filters, proposed by Fan et al. "
                "(2014), offer better space efficiency and support deletion while maintaining similar "
                "false positive rates.\n\n"
                "Major applications include: web caching (Squid proxy), database query optimization "
                "(PostgreSQL, Cassandra), network security (detecting malicious URLs), and blockchain "
                "(Bitcoin SPV nodes use Bloom filters to request relevant transactions)."
            ),
        },
        # Page 20: Summary
        {
            "subtitle": "3.4 Chapter Summary",
            "body": (
                "This chapter explored the fundamental data structures that form the backbone of "
                "efficient algorithm design. We began with linear structures: arrays offering O(1) "
                "random access, linked lists providing O(1) insertion, and skip lists bridging "
                "the gap with probabilistic O(log n) operations.\n\n"
                "Tree structures introduced hierarchical organization, with binary search trees "
                "enabling efficient ordered operations and B-trees optimizing disk-based storage. "
                "We examined self-balancing variants including AVL trees and Red-Black trees that "
                "guarantee logarithmic worst-case performance.\n\n"
                "Graph algorithms extended our toolkit to handle arbitrary relationships. BFS and "
                "DFS serve as building blocks for more sophisticated algorithms including shortest "
                "path computation (Dijkstra, Bellman-Ford, Floyd-Warshall) and minimum spanning "
                "tree construction (Kruskal, Prim).\n\n"
                "Hash tables demonstrated the power of randomization, achieving expected O(1) "
                "operations through carefully designed hash functions and collision resolution "
                "strategies. Advanced variants like cuckoo hashing and perfect hashing push "
                "performance boundaries for specialized use cases.\n\n"
                "Key takeaways:\n"
                "  1. No single data structure is optimal for all operations\n"
                "  2. Understanding the workload pattern guides structure selection\n"
                "  3. Cache behavior increasingly dominates theoretical complexity\n"
                "  4. Probabilistic structures offer powerful space-time trade-offs\n"
                "  5. Modern hardware (SIMD, multi-core) enables new implementations"
            ),
        },
    ]

    for i, page_content in enumerate(chapter_content):
        page = doc.new_page(width=W, height=H)
        y = MARGIN_TOP

        # Chapter title (only on page 1)
        if page_content.get("title"):
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, y + 20),
                page_content["title"],
                fontsize=22,
                fontname="hebo",
                color=(0, 0, 0.5),
            )
            y += 50

        # Section subtitle
        if page_content.get("subtitle"):
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, y + 16),
                page_content["subtitle"],
                fontsize=16,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y += 35

        # Body text in a text box
        if page_content.get("body"):
            rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM - 30)
            page.insert_textbox(
                rect,
                page_content["body"],
                fontsize=10.5,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(W / 2 - 5, MARGIN_BOTTOM + 15),
            str(i + 1),
            fontsize=10,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Ensure NO bookmarks/TOC
    doc.set_toc([])

    # Set metadata
    doc.set_metadata({
        "title": "Data Structures and Algorithms - Chapter 3",
        "author": "Dr. Robert Sedgewick, Dr. Kevin Wayne",
        "subject": "Computer Science Textbook",
        "keywords": "data structures, algorithms, arrays, trees, graphs, hash tables",
        "creator": "CUA-Gym Setup",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Copy to canonical path for reward script
    shutil.copy(OUTPUT, CANONICAL)
    print(f'Canonical copy created: {CANONICAL}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
