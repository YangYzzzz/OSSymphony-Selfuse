"""
Initial Setup: Create a rich Markdown tutorial document with a broken image link
Task ID: vscode_rf_037
Domain: vscode
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_037'
PROJECT_DIR = f'{WORKDIR}/projects/docs'
IMAGES_DIR = f'{PROJECT_DIR}/images'
OUTPUT = f'{PROJECT_DIR}/tutorial.md'


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


def create_placeholder_image(path, label, width=640, height=400, bg_color=(220, 230, 245)):
    """Create a simple placeholder diagram image."""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, width - 6, height - 6], outline=(70, 90, 140), width=2)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except (IOError, OSError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) / 2, (height - th) / 2), label, fill=(40, 60, 120), font=font)
    draw.ellipse([50, 50, 150, 120], outline=(100, 140, 200), width=2)
    draw.rectangle([200, 60, 350, 130], outline=(100, 140, 200), width=2)
    draw.line([150, 85, 200, 95], fill=(100, 140, 200), width=2)
    draw.ellipse([400, 50, 500, 120], outline=(100, 140, 200), width=2)
    draw.line([350, 95, 400, 85], fill=(100, 140, 200), width=2)
    img.save(path)


def create_initial():
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Create 4 placeholder images in ./images/
    create_placeholder_image(f'{IMAGES_DIR}/overview.png', 'System Overview', 640, 400, (230, 240, 220))
    create_placeholder_image(f'{IMAGES_DIR}/arch.png', 'Architecture Diagram', 640, 400, (220, 230, 245))
    create_placeholder_image(f'{IMAGES_DIR}/workflow.png', 'CI/CD Workflow', 640, 400, (245, 230, 220))
    create_placeholder_image(f'{IMAGES_DIR}/deployment.png', 'Deployment Pipeline', 640, 400, (230, 220, 245))

    # Build markdown content with broken image link on exactly line 45
    # Lines are carefully counted below (each line of the list = 1 line number)
    lines = []
    lines.append("# Building a Modern Web Application: A Comprehensive Tutorial")  # 1
    lines.append("")  # 2
    lines.append("Welcome to this in-depth guide on building and deploying a modern web application using Python, Docker, and cloud services.")  # 3
    lines.append("")  # 4
    lines.append("> **Note:** This tutorial assumes you have Python 3.10+ installed and basic familiarity with the command line.")  # 5
    lines.append("")  # 6
    lines.append("## 1. Project Overview")  # 7
    lines.append("")  # 8
    lines.append("Our application is a task management system called **TaskFlow** that helps teams track issues and manage sprints.")  # 9
    lines.append("")  # 10
    lines.append("![System Overview](./images/overview.png)")  # 11
    lines.append("")  # 12
    lines.append("The system uses a microservices architecture with the following components:")  # 13
    lines.append("")  # 14
    lines.append("- **Frontend Layer**")  # 15
    lines.append("  - React 18 with TypeScript for type safety")  # 16
    lines.append("  - Redux Toolkit for state management")  # 17
    lines.append("    - Slice-based architecture for modularity")  # 18
    lines.append("    - RTK Query for API data fetching")  # 19
    lines.append("      - Automatic cache invalidation")  # 20
    lines.append("      - Optimistic updates for better UX")  # 21
    lines.append("  - Tailwind CSS for responsive styling")  # 22
    lines.append("")  # 23
    lines.append("- **Backend Services**")  # 24
    lines.append("  - FastAPI for the REST API gateway")  # 25
    lines.append("  - Celery workers for background tasks")  # 26
    lines.append("    - Email notifications")  # 27
    lines.append("    - Report generation")  # 28
    lines.append("      - PDF export with charts")  # 29
    lines.append("      - CSV data dumps")  # 30
    lines.append("  - Redis for caching and session management")  # 31
    lines.append("")  # 32
    lines.append("- **Infrastructure**")  # 33
    lines.append("  - Docker containers for service isolation")  # 34
    lines.append("  - Kubernetes for orchestration")  # 35
    lines.append("    - Horizontal pod autoscaling")  # 36
    lines.append("    - Rolling deployments with health checks")  # 37
    lines.append("      - Readiness probes on /health endpoint")  # 38
    lines.append("      - Liveness probes every 30 seconds")  # 39
    lines.append("  - Terraform for infrastructure as code")  # 40
    lines.append("")  # 41
    lines.append("> **Architecture Decision:** We chose FastAPI over Django REST Framework because of its native async support and automatic OpenAPI documentation generation.")  # 42
    lines.append("")  # 43
    lines.append("> **Performance Note:** The async architecture handles 10,000+ concurrent connections with sub-50ms p99 latency under typical production workloads.")  # 44
    lines.append("![Architecture](./imgs/arch.png)")  # 45 -- BROKEN LINK
    lines.append("")  # 46
    lines.append("## 2. Setting Up the Development Environment")  # 47
    lines.append("")  # 48
    lines.append("### 2.1 Prerequisites")  # 49
    lines.append("")  # 50
    lines.append("Before starting, ensure you have the following tools installed:")  # 51
    lines.append("")  # 52
    lines.append("```bash")  # 53
    lines.append("# Clone the repository")  # 54
    lines.append("git clone https://github.com/taskflow/taskflow-app.git")  # 55
    lines.append("cd taskflow-app")  # 56
    lines.append("")  # 57
    lines.append("# Create and activate virtual environment")  # 58
    lines.append("python3 -m venv .venv")  # 59
    lines.append("source .venv/bin/activate")  # 60
    lines.append("")  # 61
    lines.append("# Install dependencies")  # 62
    lines.append("pip install -r requirements.txt")  # 63
    lines.append("pip install -r requirements-dev.txt")  # 64
    lines.append("")  # 65
    lines.append("# Set up pre-commit hooks")  # 66
    lines.append("pre-commit install")  # 67
    lines.append("```")  # 68
    lines.append("")  # 69
    lines.append("> **Tip:** Always use a virtual environment to isolate project dependencies. This prevents version conflicts between different Python projects.")  # 70
    lines.append("")  # 71
    lines.append("## 3. Backend Implementation")  # 72
    lines.append("")  # 73
    lines.append("### 3.1 API Design")  # 74
    lines.append("")  # 75
    lines.append("The REST API follows resource-oriented design principles:")  # 76
    lines.append("")  # 77
    lines.append("```python")  # 78
    lines.append("from fastapi import FastAPI, HTTPException, Depends")  # 79
    lines.append("from pydantic import BaseModel, Field")  # 80
    lines.append("from datetime import datetime")  # 81
    lines.append("from typing import Optional")  # 82
    lines.append("import uuid")  # 83
    lines.append("")  # 84
    lines.append('app = FastAPI(title="TaskFlow API", version="2.1.0")')  # 85
    lines.append("")  # 86
    lines.append("class TaskCreate(BaseModel):")  # 87
    lines.append('    title: str = Field(..., min_length=1, max_length=200)')  # 88
    lines.append('    description: Optional[str] = Field(None, max_length=5000)')  # 89
    lines.append('    priority: str = Field("medium", pattern="^(low|medium|high|critical)$")')  # 90
    lines.append("    assignee_id: Optional[uuid.UUID] = None")  # 91
    lines.append("    due_date: Optional[datetime] = None")  # 92
    lines.append("    tags: list[str] = Field(default_factory=list)")  # 93
    lines.append("")  # 94
    lines.append("class TaskResponse(TaskCreate):")  # 95
    lines.append("    id: uuid.UUID")  # 96
    lines.append("    status: str")  # 97
    lines.append("    created_at: datetime")  # 98
    lines.append("    updated_at: datetime")  # 99
    lines.append("")  # 100
    lines.append('@app.post("/api/v1/tasks", response_model=TaskResponse, status_code=201)')  # 101
    lines.append("async def create_task(task: TaskCreate):")  # 102
    lines.append('    """Create a new task in the current sprint."""')  # 103
    lines.append("    db_task = Task(**task.model_dump())")  # 104
    lines.append("    await db.commit()")  # 105
    lines.append("    return db_task")  # 106
    lines.append("```")  # 107
    lines.append("")  # 108
    lines.append("> **Best Practice:** Always use Pydantic models for request/response validation. This ensures data integrity at the API boundary.")  # 109
    lines.append("")  # 110
    lines.append("## 4. CI/CD Pipeline")  # 111
    lines.append("")  # 112
    lines.append("The continuous integration and deployment pipeline automates testing, building, and releasing:")  # 113
    lines.append("")  # 114
    lines.append("![CI/CD Workflow](./images/workflow.png)")  # 115
    lines.append("")  # 116
    lines.append("> **Pipeline Insight:** Each stage must pass before the next begins, ensuring code quality gates are enforced at every step of the process.")  # 117
    lines.append("")  # 118
    lines.append("## 5. Deployment Architecture")  # 119
    lines.append("")  # 120
    lines.append("The production deployment uses Kubernetes for container orchestration:")  # 121
    lines.append("")  # 122
    lines.append("![Deployment Pipeline](./images/deployment.png)")  # 123
    lines.append("")  # 124
    lines.append("> **Operational Insight:** We use a blue-green deployment strategy to achieve zero-downtime releases. The load balancer switches traffic after health checks pass.")  # 125
    lines.append("")  # 126
    lines.append("## Conclusion")  # 127
    lines.append("")  # 128
    lines.append("This tutorial covered the complete lifecycle of building TaskFlow. The key takeaways are:")  # 129
    lines.append("")  # 130
    lines.append("1. Use type-safe frameworks (FastAPI + Pydantic) for robust APIs")  # 131
    lines.append("2. Containerize early and maintain parity between dev and prod environments")  # 132
    lines.append("3. Automate everything: testing, building, deploying, and monitoring")  # 133
    lines.append("4. Design for observability from the start, not as an afterthought")  # 134

    content = "\n".join(lines) + "\n"

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')
    print(f'Images created in: {IMAGES_DIR}')

    # Verify line 45 has the broken image link
    with open(OUTPUT, 'r') as f:
        read_lines = f.readlines()
    print(f'Total lines: {len(read_lines)}')
    print(f'Line 45: {read_lines[44].strip()}')
    assert '![Architecture](./imgs/arch.png)' in read_lines[44], f"Line 45 mismatch: {read_lines[44]}"
    print('Line 45 verified: contains broken image link ./imgs/arch.png')

    # Launch VSCode with the project directory, then open the file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
