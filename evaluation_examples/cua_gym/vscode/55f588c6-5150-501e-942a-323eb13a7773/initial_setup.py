"""
Initial Setup: Configure VSCode to show vertical rulers at columns 80 and 120
Task ID: vscode_prod_024
Domain: vscode

Creates a Python project with long lines, opens VSCode with no rulers configured.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_024'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'styleguide')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project_files():
    """Create a realistic Python project with long lines."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main Python file with intentionally long lines for style guide context
    main_py = '''\
"""
StyleGuide Analytics - Data Processing Module
Processes user engagement metrics and generates reports for the marketing team.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class EngagementTracker:
    """Tracks and analyzes user engagement metrics across multiple marketing channels and campaign types."""

    DEFAULT_CHANNELS = ["email", "social_media", "organic_search", "paid_search", "referral", "direct", "display_ads"]

    def __init__(self, campaign_name: str, start_date: str, end_date: str, target_audience: str = "all_segments"):
        self.campaign_name = campaign_name
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.target_audience = target_audience
        self.metrics: Dict[str, List[float]] = {}
        self.channel_weights: Dict[str, float] = {channel: 1.0 / len(self.DEFAULT_CHANNELS) for channel in self.DEFAULT_CHANNELS}

    def calculate_weighted_engagement_score(self, channel_data: Dict[str, List[float]], normalization_factor: float = 100.0, include_outliers: bool = False) -> float:
        """Calculate the weighted engagement score across all channels, applying normalization and optional outlier filtering for more accurate quarterly reporting."""
        total_weighted_score = 0.0
        total_weight = 0.0
        for channel_name, engagement_values in channel_data.items():
            if channel_name not in self.channel_weights:
                raise ValueError(f"Unknown channel: {channel_name}. Valid channels are: {', '.join(self.DEFAULT_CHANNELS)}")
            filtered_values = engagement_values if include_outliers else [v for v in engagement_values if abs(v - sum(engagement_values) / len(engagement_values)) < 2 * (sum((x - sum(engagement_values) / len(engagement_values)) ** 2 for x in engagement_values) / len(engagement_values)) ** 0.5]
            channel_score = sum(filtered_values) / len(filtered_values) if filtered_values else 0.0
            total_weighted_score += channel_score * self.channel_weights[channel_name]
            total_weight += self.channel_weights[channel_name]
        return (total_weighted_score / total_weight * normalization_factor) if total_weight > 0 else 0.0

    def generate_period_comparison(self, current_period_data: Dict[str, float], previous_period_data: Dict[str, float], threshold_pct: float = 5.0) -> Dict[str, Tuple[float, float, str]]:
        """Compare engagement metrics between two periods and flag significant changes that exceed the specified percentage threshold for executive dashboard reporting."""
        comparison_results: Dict[str, Tuple[float, float, str]] = {}
        for metric_name in current_period_data:
            current_value = current_period_data.get(metric_name, 0.0)
            previous_value = previous_period_data.get(metric_name, 0.0)
            if previous_value != 0:
                percent_change = ((current_value - previous_value) / previous_value) * 100.0
                status = "significant_increase" if percent_change > threshold_pct else ("significant_decrease" if percent_change < -threshold_pct else "stable")
            else:
                percent_change = 100.0 if current_value > 0 else 0.0
                status = "new_metric" if current_value > 0 else "no_data"
            comparison_results[metric_name] = (current_value, percent_change, status)
        return comparison_results

    def export_report_summary(self, output_path: str, format_type: str = "json", include_metadata: bool = True, compression_enabled: bool = False) -> str:
        """Export the engagement report summary to the specified format with optional metadata headers and compression for archival storage in the data warehouse."""
        report_data = {
            "campaign": self.campaign_name,
            "period": f"{self.start_date.strftime(\'%Y-%m-%d\')} to {self.end_date.strftime(\'%Y-%m-%d\')}",
            "audience": self.target_audience,
            "generated_at": datetime.now().isoformat(),
            "metrics_summary": {k: {"mean": sum(v) / len(v), "count": len(v), "min": min(v), "max": max(v)} for k, v in self.metrics.items() if v},
        }
        if include_metadata:
            report_data["metadata"] = {"version": "2.1.0", "generator": "StyleGuide Analytics Engine", "channel_config": self.channel_weights}
        full_output_path = os.path.join(output_path, f"{self.campaign_name}_engagement_report_{self.end_date.strftime(\'%Y%m%d\')}.{format_type}")
        with open(full_output_path, "w") as report_file:
            json.dump(report_data, report_file, indent=2, default=str)
        return full_output_path


def process_daily_metrics(raw_data_path: str, date_range: Tuple[str, str], channels: Optional[List[str]] = None, aggregation_method: str = "mean") -> Dict[str, Dict[str, float]]:
    """Process daily engagement metrics from raw CSV data files, filtering by date range and channels, then aggregating using the specified statistical method for the weekly summary dashboard."""
    channels = channels or EngagementTracker.DEFAULT_CHANNELS
    aggregated_results: Dict[str, Dict[str, float]] = {channel: {"impressions": 0.0, "clicks": 0.0, "conversions": 0.0, "revenue": 0.0} for channel in channels}
    return aggregated_results


if __name__ == "__main__":
    tracker = EngagementTracker(campaign_name="Q1_2025_Product_Launch", start_date="2025-01-01", end_date="2025-03-31", target_audience="enterprise_customers")
    print(f"Initialized tracker for campaign: {tracker.campaign_name} targeting {tracker.target_audience}")
    daily_results = process_daily_metrics("/data/raw/engagement", ("2025-01-01", "2025-03-31"), channels=["email", "social_media", "paid_search"], aggregation_method="median")
    print(f"Processed {len(daily_results)} channels")
'''

    with open(os.path.join(PROJECT_DIR, 'analytics.py'), 'w') as f:
        f.write(main_py)

    # A config file for the project
    config_content = {
        "project_name": "StyleGuide Analytics",
        "version": "2.1.0",
        "data_sources": [
            {"name": "engagement_db", "host": "analytics-db.internal", "port": 5432},
            {"name": "events_stream", "host": "kafka.internal", "port": 9092}
        ],
        "reporting": {
            "output_dir": "/data/reports",
            "formats": ["json", "csv", "pdf"],
            "schedule": "weekly"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'config.json'), 'w') as f:
        json.dump(config_content, f, indent=2)

    print(f'Project files created in {PROJECT_DIR}')


def setup_vscode_settings():
    """Ensure VSCode settings exist but with NO rulers configured."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Ensure no rulers are set - remove if they exist
    settings.pop('editor.rulers', None)
    # Remove any existing ruler color customizations
    if 'workbench.colorCustomizations' in settings:
        color_customs = settings['workbench.colorCustomizations']
        color_customs.pop('editorRuler.foreground', None)

    # Set some baseline settings that make sense
    settings.setdefault('editor.fontSize', 14)
    settings.setdefault('editor.tabSize', 4)
    settings.setdefault('editor.minimap.enabled', True)
    settings.setdefault('workbench.colorTheme', 'Default Dark Modern')

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured (no rulers) at {SETTINGS_PATH}')


def main():
    create_project_files()
    setup_vscode_settings()

    # Launch VSCode with the project folder and open the Python file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{os.path.join(PROJECT_DIR, "analytics.py")}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
