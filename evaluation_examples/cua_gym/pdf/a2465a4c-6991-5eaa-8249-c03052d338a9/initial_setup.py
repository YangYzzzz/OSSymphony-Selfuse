"""
Initial Setup: Create Markdown slide deck and prepare environment
Task ID: pdf_gf3_033
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_033'

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
    # Create directories
    os.makedirs(f'{WORKDIR}/content', exist_ok=True)
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)
    os.makedirs(f'{WORKDIR}/output', exist_ok=True)

    # Install reportlab
    subprocess.run(['pip3', 'install', 'reportlab'], capture_output=True)

    # Create slides.md with 15 slide sections
    slides_md = """# Welcome to DevConf 2026
## Opening Keynote - Building the Future of Developer Tools

- Join us for three days of cutting-edge tech talks
- Network with industry leaders and open-source maintainers
- Hands-on workshops and live coding sessions

---

# The State of Cloud Native
## Infrastructure Trends in 2026

- Kubernetes adoption has reached 89% among Fortune 500
- Serverless architectures powering mission-critical workloads
- Edge computing reducing latency by 60% for global applications
- Multi-cloud strategies becoming the default approach

---

# Rust in Production
## Lessons from Migrating 2M Lines of C++

- Memory safety eliminated 73% of critical CVEs
- Performance parity achieved within 6 months
- Developer onboarding time reduced from 8 weeks to 3
- Compilation times improved with incremental builds

---

# AI-Powered Code Review
## How Machine Learning is Transforming Development Workflows

- Automated detection of security vulnerabilities
- Style consistency enforcement across large teams
- Intelligent refactoring suggestions based on codebase patterns
- Reduced review turnaround from 48 hours to 2 hours

---

# Observability Beyond Metrics
## Distributed Tracing and Continuous Profiling

- OpenTelemetry as the universal instrumentation standard
- Correlating traces with business outcomes
- Continuous profiling revealing hidden performance bottlenecks
- Cost optimization through intelligent sampling strategies

---

# The WebAssembly Revolution
## Running Any Language Anywhere

- Browser-based IDEs with near-native performance
- Server-side Wasm replacing traditional containers
- Plugin ecosystems built on portable binaries
- Cross-platform desktop applications with WASI

---

# Sustainable Software Engineering
## Reducing the Carbon Footprint of Digital Infrastructure

- Green coding practices saving 40% energy consumption
- Carbon-aware scheduling shifting workloads to renewable grids
- Measuring and reporting software carbon intensity
- Building energy-efficient algorithms and data structures

---

# Zero Trust Architecture
## Security in a Perimeter-Less World

- Identity-based access replacing network-based controls
- Continuous verification for every request and transaction
- Micro-segmentation limiting blast radius of breaches
- Service mesh providing mutual TLS and authorization policies

---

# Developer Experience Matters
## Building Internal Platforms That Engineers Actually Love

- Self-service infrastructure provisioning in under 5 minutes
- Golden paths reducing cognitive load for common workflows
- Documentation as code with automated freshness checks
- Feedback loops measuring developer satisfaction quarterly

---

# GraphQL at Scale
## Federated APIs Serving 10 Billion Requests Daily

- Schema federation enabling autonomous team development
- Persisted queries reducing payload size by 85%
- Real-time subscriptions powering live collaboration features
- Rate limiting and cost analysis per query complexity

---

# The Future of Databases
## NewSQL, Vector Search, and Beyond

- Distributed SQL databases achieving single-digit millisecond latency
- Vector databases enabling semantic search at massive scale
- Time-series optimization for IoT and financial data streams
- Automatic sharding and rebalancing without downtime

---

# Open Source Sustainability
## Funding Models That Actually Work

- Corporate sponsorship programs with clear ROI metrics
- Open core strategies balancing community and revenue
- Government grants supporting critical infrastructure projects
- Maintainer cooperatives sharing resources and reducing burnout

---

# Containerization Best Practices
## From Development to Production in 2026

- Distroless images reducing attack surface by 90%
- Build reproducibility ensuring consistent deployments
- Supply chain security with SBOM and signature verification
- Graceful shutdown patterns for zero-downtime releases

---

# Workshop: Building Your First ML Pipeline
## Hands-On Session with Real-World Data

- Data ingestion from multiple sources using Apache Kafka
- Feature engineering with automated transformation pipelines
- Model training with experiment tracking and versioning
- Deployment to production with canary rollout strategy

---

# Closing Remarks and Thank You
## See You at DevConf 2027

- Thank you to all 3,500 attendees and 120 speakers
- Conference recordings available within 48 hours
- Community Discord server for ongoing discussions
- Early bird tickets for DevConf 2027 opening next month
"""

    slides_path = f'{WORKDIR}/content/slides.md'
    with open(slides_path, 'w') as f:
        f.write(slides_md.strip() + '\n')

    print(f'Created: {slides_path}')
    print(f'Created directories: content/, scripts/, output/')

    # Verify
    with open(slides_path, 'r') as f:
        content = f.read()
    section_count = content.count('---') + 1
    print(f'Slide sections in markdown: {section_count}')

    # Open the markdown file in a text editor for GUI state
    launch_gui(f'xdg-open "{slides_path}"', delay_sec=2.0)
    print('GUI_READY: launched text editor with DISPLAY=:0')

create_initial()
