"""
Initial Setup: Create a Python file with missing type imports for Pylance code actions task.
Task ID: vscode_py_089
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_089'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
OUTPUT = f'{PROJECT_DIR}/api_types.py'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write api_types.py WITHOUT any typing imports.
    # Uses Optional, List, Dict, Union, Tuple in annotations - all unresolved.
    content = '''\
"""
API Type definitions for the analytics service.
Provides request/response models and shared type aliases.
"""

import dataclasses
from datetime import datetime


@dataclasses.dataclass
class PaginationParams:
    """Parameters for paginated API responses."""
    page: int
    page_size: int
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"


@dataclasses.dataclass
class UserProfile:
    """Represents a user profile in the system."""
    user_id: str
    username: str
    email: str
    full_name: Optional[str] = None
    roles: List[str] = dataclasses.field(default_factory=list)
    metadata: Dict[str, str] = dataclasses.field(default_factory=dict)
    created_at: Optional[datetime] = None


@dataclasses.dataclass
class ApiResponse:
    """Generic API response wrapper."""
    status_code: int
    data: Union[Dict[str, object], List[object]]
    errors: Optional[List[str]] = None
    pagination: Optional[PaginationParams] = None


@dataclasses.dataclass
class QueryFilter:
    """Defines a filter condition for database queries."""
    field: str
    operator: str
    value: Union[str, int, float, bool]


@dataclasses.dataclass
class BatchRequest:
    """Holds a batch of API operations to execute together."""
    request_id: str
    operations: List[Tuple[str, Dict[str, object]]]
    filters: Optional[List[QueryFilter]] = None
    timeout_seconds: Optional[int] = 30


@dataclasses.dataclass
class AnalyticsEvent:
    """Represents a single analytics tracking event."""
    event_name: str
    timestamp: datetime
    properties: Dict[str, Union[str, int, float, bool]]
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    tags: List[str] = dataclasses.field(default_factory=list)


def build_query(
    table: str,
    columns: List[str],
    filters: Optional[List[QueryFilter]] = None,
    order_by: Optional[Tuple[str, str]] = None,
    limit: Optional[int] = None,
) -> Dict[str, object]:
    """Build a structured query dictionary from parameters."""
    query: Dict[str, object] = {
        "table": table,
        "columns": columns,
    }
    if filters:
        query["filters"] = [
            {"field": f.field, "operator": f.operator, "value": f.value}
            for f in filters
        ]
    if order_by:
        query["order_by"] = {"column": order_by[0], "direction": order_by[1]}
    if limit is not None:
        query["limit"] = limit
    return query


def merge_responses(
    responses: List[ApiResponse],
) -> Tuple[List[object], List[str]]:
    """Merge multiple API responses into combined data and error lists."""
    all_data: List[object] = []
    all_errors: List[str] = []
    for resp in responses:
        if isinstance(resp.data, list):
            all_data.extend(resp.data)
        else:
            all_data.append(resp.data)
        if resp.errors:
            all_errors.extend(resp.errors)
    return all_data, all_errors
'''

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the project folder and the specific file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
