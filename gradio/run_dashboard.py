import gradio as gr
import requests
import datetime
import json
import threading
import time

DEFAULT_MASTER_URL = "http://10.140.52.51:10001"

def fetch_cluster_status(master_url):
    """Fetch status from the Master Gateway"""
    try:
        url = f"{master_url.rstrip('/')}/workers"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def generate_dashboard(master_url):
    """Generate the dashboard metrics and HTML based on master API data"""
    data, error = fetch_cluster_status(master_url)

    frontend_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # If API fails, provide a fallback mock for demonstration
    if error:
        mock_mode = True
        workers = [
            {
                "worker_id": "worker-10.140.52.49",
                "url": "http://10.140.52.49:8000",
                "total_envs": 24,
                "free_envs_ids": [0, 1, 2, 3, 5, 8, 10, 11, 22, 23],
                "health_envs_ids": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23], # 20 is unhealthy
                "healthy": True,
                "last_heartbeat": time.time() - 2.5
            },
            {
                "worker_id": "worker-10.140.52.51",
                "url": "http://10.140.52.51:8000",
                "total_envs": 5,
                "free_envs_ids": [0, 1, 2, 3, 4],
                "health_envs_ids": [0, 1, 2, 3, 4],
                "healthy": True,
                "last_heartbeat": time.time() - 1.2
            },
            {
                "worker_id": "worker-10.140.52.54",
                "url": "http://10.140.52.54:8000",
                "total_envs": 24,
                "free_envs_ids": [],
                "health_envs_ids": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23], # 9, 14 unhealthy
                "healthy": True,
                "last_heartbeat": time.time() - 5.8
            },
            {
                "worker_id": "worker-10.140.52.55",
                "url": "http://10.140.52.55:8000",
                "total_envs": 12,
                "free_envs_ids": [0, 1],
                "health_envs_ids": [0, 1],
                "healthy": False,
                "last_heartbeat": time.time() - 150.0
            },
        ]
        error_html = f"""
        <div style="padding: 12px; margin-bottom: 20px; background-color: #fee2e2; border-left: 4px solid #ef4444; border-radius: 4px; color: #991b1b; font-size: 0.9rem;">
            <strong>Warning:</strong> Cannot connect to {master_url}. Showing <b>Mock Data</b> for UI demonstration. <br/>Error details: {error}
        </div>
        """
    else:
        mock_mode = False
        workers = data.get("workers", [])
        error_html = ""

    total_workers = len(workers)
    healthy_workers = sum(1 for w in workers if w.get("healthy", False))

    total_envs_overall = 0
    total_healthy_envs_overall = 0
    total_free_envs_overall = 0
    total_working_envs_overall = 0
    total_unhealthy_envs_overall = 0

    # Process metrics
    for w in workers:
        t_envs = w.get("total_envs", 0)
        h_ids = set(w.get("health_envs_ids", []))
        f_ids = set(w.get("free_envs_ids", []))

        # Calculate counts
        healthy_count = len(h_ids)
        unhealthy_count = t_envs - healthy_count

        # Healthy & Free
        healthy_free_count = len(h_ids.intersection(f_ids))
        # Healthy & Working (not free)
        healthy_working_count = healthy_count - healthy_free_count

        total_envs_overall += t_envs
        total_healthy_envs_overall += healthy_count
        total_unhealthy_envs_overall += unhealthy_count
        total_free_envs_overall += healthy_free_count
        total_working_envs_overall += healthy_working_count

    # Overall usage metrics (based on healthy envs)
    usage_rate = (total_working_envs_overall / total_healthy_envs_overall * 100) if total_healthy_envs_overall > 0 else 0
    unhealthy_rate = (total_unhealthy_envs_overall / total_envs_overall * 100) if total_envs_overall > 0 else 0

    # Start HTML generation
    html = error_html

    # Add Legend
    html += """
    <div style='margin-bottom: 20px; padding: 16px; background: var(--background-fill-secondary, #ffffff); border: 1px solid var(--border-color-primary, #e5e7eb); border-radius: 8px; display: flex; align-items: center; flex-wrap: wrap; gap: 20px;'>
        <div style='font-weight: 600; color: var(--body-text-color, #1f2937); margin-right: 10px;'>Environment Legend:</div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 20px; height: 20px; background-color: #10b981; border-radius: 4px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.1);'></div>
            <span style='font-size: 0.9rem; color: var(--body-text-color-subdued, #4b5563);'>Healthy & Free</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 20px; height: 20px; background-color: #f59e0b; border-radius: 4px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.1);'></div>
            <span style='font-size: 0.9rem; color: var(--body-text-color-subdued, #4b5563);'>Healthy & Working</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 20px; height: 20px; background-color: #ef4444; border-radius: 4px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.2), 0 1px 2px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: center;'>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </div>
            <span style='font-size: 0.9rem; color: var(--body-text-color-subdued, #4b5563);'>Unhealthy (Broken)</span>
        </div>
    </div>
    """

    html += "<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 24px; margin-top: 10px;'>"

    for w in workers:
        worker_id = w.get("worker_id", "unknown")
        url = w.get("url", "")
        healthy = w.get("healthy", False)
        t_envs = w.get("total_envs", 0)
        h_ids = set(w.get("health_envs_ids", []))
        f_ids = set(w.get("free_envs_ids", []))

        last_hb_ts = w.get("last_heartbeat", 0)
        if last_hb_ts > 0:
            last_hb_str = datetime.datetime.fromtimestamp(last_hb_ts).strftime("%H:%M:%S")
            hb_age_sec = time.time() - last_hb_ts

            if hb_age_sec < 15:
                hb_color = "#10b981" # Green
            elif hb_age_sec < 60:
                hb_color = "#f59e0b" # Yellow
            else:
                hb_color = "#ef4444" # Red

            hb_text = f"Backend update: {last_hb_str} ({int(hb_age_sec)}s ago)"
        else:
            hb_color = "#6b7280"
            hb_text = "Backend update: Unknown"

        healthy_count = len(h_ids)
        unhealthy_count = t_envs - healthy_count
        healthy_free_count = len(h_ids.intersection(f_ids))
        healthy_working_count = healthy_count - healthy_free_count

        status_color = "#10b981" if healthy else "#ef4444"
        status_text = "Node Healthy" if healthy else "Node Offline"
        status_bg = "#d1fae5" if healthy else "#fee2e2"

        # Worker utilization (working / total healthy)
        w_usage = (healthy_working_count / healthy_count * 100) if healthy_count > 0 else 0

        card_html = f"""
        <div style='border: 1px solid var(--border-color-primary, #e5e7eb); border-radius: 12px; padding: 24px; background: var(--background-fill-secondary, #ffffff); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: transform 0.2s;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border-color-primary, #e5e7eb); padding-bottom: 16px; margin-bottom: 16px;'>
                <div>
                    <h3 style='margin: 0 0 4px 0; font-size: 1.15rem; color: var(--body-text-color, #1f2937); font-weight: 600; display: flex; align-items: center; gap: 8px;'>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #6366f1;"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
                        {worker_id}
                    </h3>
                    <span style='font-size: 0.85rem; color: var(--body-text-color-subdued, #6b7280); font-family: monospace;'>{url}</span>
                    <div style='margin-top: 4px; font-size: 0.75rem; color: {hb_color}; display: flex; align-items: center; gap: 4px;'>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        {hb_text}
                    </div>
                </div>
                <div style='display: flex; align-items: center; gap: 6px; background-color: {status_bg}; padding: 4px 10px; border-radius: 999px;'>
                    <div style='width: 8px; height: 8px; border-radius: 50%; background-color: {status_color}; box-shadow: 0 0 0 2px rgba(255,255,255,0.5);'></div>
                    <span style='font-size: 0.8rem; font-weight: 600; color: {status_color};'>{status_text}</span>
                </div>
            </div>

            <div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 20px; font-size: 0.9rem;'>
                <div style='text-align: center; background: var(--background-fill-primary, #f9fafb); padding: 8px 2px; border-radius: 8px;' title='Total Environments'>
                    <div style='color: var(--body-text-color-subdued, #6b7280); font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;'>Total</div>
                    <div style='font-weight: 700; font-size: 1.1rem; color: var(--body-text-color, #111827);'>{t_envs}</div>
                </div>
                <div style='text-align: center; background: #ecfdf5; padding: 8px 2px; border-radius: 8px;' title='Healthy & Free'>
                    <div style='color: #059669; font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;'>Free</div>
                    <div style='font-weight: 700; font-size: 1.1rem; color: #10b981;'>{healthy_free_count}</div>
                </div>
                <div style='text-align: center; background: #fffbeb; padding: 8px 2px; border-radius: 8px;' title='Healthy & Working'>
                    <div style='color: #d97706; font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;'>Work</div>
                    <div style='font-weight: 700; font-size: 1.1rem; color: #f59e0b;'>{healthy_working_count}</div>
                </div>
                <div style='text-align: center; background: #fef2f2; padding: 8px 2px; border-radius: 8px;' title='Unhealthy (Broken)'>
                    <div style='color: #dc2626; font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;'>Bad</div>
                    <div style='font-weight: 700; font-size: 1.1rem; color: #ef4444;'>{unhealthy_count}</div>
                </div>
                <div style='text-align: center; background: var(--background-fill-primary, #f9fafb); padding: 8px 2px; border-radius: 8px;' title='Usage Rate (Working/Healthy)'>
                    <div style='color: var(--body-text-color-subdued, #6b7280); font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;'>Usage</div>
                    <div style='font-weight: 700; font-size: 1.1rem; color: var(--body-text-color, #111827);'>{w_usage:.0f}%</div>
                </div>
            </div>

            <div style='margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-size: 0.8rem; font-weight: 600; color: var(--body-text-color-subdued, #6b7280);'>Environment Slots Map</span>
            </div>
            <div style='display: flex; flex-wrap: wrap; gap: 8px; background: var(--background-fill-primary, #f9fafb); padding: 12px; border-radius: 8px; border: 1px solid var(--border-color-primary, #f3f4f6);'>
        """

        # Draw individual environments based on ID
        for env_id in range(t_envs):
            is_healthy = env_id in h_ids
            is_free = env_id in f_ids

            if not is_healthy:
                # Unhealthy (Red with cross)
                card_html += f"""
                    <div style='width: 32px; height: 32px; background-color: #ef4444; border-radius: 6px;
                         box-shadow: inset 0 2px 4px rgba(255,255,255,0.2), inset 0 -2px 4px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.1);
                         position: relative; cursor: help; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: rgba(255,255,255,0.9);'
                         title='Env {env_id} - UNHEALTHY'>
                        {env_id}
                        <svg style='position: absolute; opacity: 0.5;' width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </div>"""
            elif is_free:
                # Healthy & Free (Green)
                card_html += f"""
                    <div style='width: 32px; height: 32px; background-color: #10b981; border-radius: 6px;
                         box-shadow: inset 0 2px 4px rgba(255,255,255,0.3), inset 0 -2px 4px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.1);
                         position: relative; cursor: help; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: rgba(255,255,255,0.9);'
                         title='Env {env_id} - Free'>
                        {env_id}
                        <div style='position: absolute; top: 3px; right: 3px; width: 4px; height: 4px; border-radius: 50%; background: rgba(255,255,255,0.8);'></div>
                    </div>"""
            else:
                # Healthy & Working (Yellow)
                card_html += f"""
                    <div style='width: 32px; height: 32px; background-color: #f59e0b; border-radius: 6px;
                         box-shadow: inset 0 2px 4px rgba(255,255,255,0.3), inset 0 -2px 4px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.1);
                         position: relative; cursor: help; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: rgba(255,255,255,0.9);'
                         title='Env {env_id} - Working'>
                        {env_id}
                        <div style='position: absolute; top: 3px; right: 3px; width: 4px; height: 4px; border-radius: 50%; background: rgba(255,255,255,0.5);'></div>
                    </div>"""

        card_html += """
            </div>
        </div>
        """
        html += card_html

    html += "</div>"

    last_update_text = f"🔄 Frontend UI updated: {frontend_current_time}"
    if mock_mode:
         last_update_text += " | ⚠️ Mock Mode Active"

    # Format return variables for UI
    stats = {
        "nodes": f"{healthy_workers}/{total_workers}",
        "total": total_envs_overall,
        "free": total_free_envs_overall,
        "working": total_working_envs_overall,
        "unhealthy": total_unhealthy_envs_overall,
        "usage": f"{usage_rate:.1f}%",
        "broken_rate": f"{unhealthy_rate:.1f}%"
    }

    return (
        stats["nodes"],
        stats["total"],
        stats["free"],
        stats["working"],
        stats["unhealthy"],
        stats["usage"],
        stats["broken_rate"],
        html,
        last_update_text
    )

# Define Gradio UI
with gr.Blocks(title="OSWorld RL Cluster", theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="blue")) as demo:
    gr.Markdown(
        """
        # 🌐 OSWorld Distributed RL Cluster Dashboard
        Real-time visualization of Master-Worker nodes and Desktop Environment allocations.
        """
    )

    with gr.Row(variant="panel"):
        with gr.Column(scale=4):
            master_url_input = gr.Textbox(
                label="Master Gateway URL",
                value=DEFAULT_MASTER_URL,
                placeholder="http://ip:port",
                info="URL of the OSWorld Master Gateway API"
            )
        with gr.Column(scale=1):
            refresh_btn = gr.Button("🔄 Manual Refresh", variant="primary")
            last_update_label = gr.Markdown("Waiting for data...")

    gr.Markdown("### 📊 Global Cluster Statistics")
    with gr.Row():
        nodes_box = gr.Textbox(label="Healthy Nodes (Online/Total)", interactive=False)
        total_envs_box = gr.Number(label="Total Envs", interactive=False)
        free_envs_box = gr.Number(label="Free Envs (Healthy)", interactive=False)
        working_envs_box = gr.Number(label="Working Envs (Healthy)", interactive=False)

    with gr.Row():
        unhealthy_envs_box = gr.Number(label="Unhealthy Envs (Broken)", interactive=False)
        usage_rate_box = gr.Textbox(label="Cluster Workload (Working/Healthy)", interactive=False)
        broken_rate_box = gr.Textbox(label="Cluster Broken Rate", interactive=False)

    gr.Markdown("### 🖥️ Cluster Nodes Topology")
    cluster_html = gr.HTML(label="Cluster Visualization")

    # Auto-refresh every 30 seconds
    timer = gr.Timer(30)

    # Define the update function connections
    outputs = [
        nodes_box, total_envs_box, free_envs_box, working_envs_box,
        unhealthy_envs_box, usage_rate_box, broken_rate_box,
        cluster_html, last_update_label
    ]

    # Run on startup
    demo.load(
        fn=generate_dashboard,
        inputs=[master_url_input],
        outputs=outputs
    )

    # Run on timer tick (every 30s)
    timer.tick(
        fn=generate_dashboard,
        inputs=[master_url_input],
        outputs=outputs
    )

    # Run on manual button click
    refresh_btn.click(
        fn=generate_dashboard,
        inputs=[master_url_input],
        outputs=outputs
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
