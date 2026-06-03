"""
Initial Setup: Extract selected code block into a new function called 'filterAndSortProducts'
Task ID: vscode_rrt_042
Domain: vscode

Creates ~/projects/shop/catalog.py with get_catalog containing inline
filtering/sorting logic (lines 3-6). VSCode opens with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_042'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'shop')
OUTPUT = os.path.join(PROJECT_DIR, 'catalog.py')


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


CATALOG_CODE = r'''def get_catalog(products, category, min_price):
    # Filter and sort logic
    filtered = [p for p in products if p["category"] == category]
    filtered = [p for p in filtered if p["price"] >= min_price]
    filtered.sort(key=lambda p: p["price"])
    filtered = filtered[:50]  # limit results

    # Format output
    result = []
    for p in filtered:
        price_str = "${:.2f}".format(p["price"])
        result.append({"name": p["name"], "price": price_str})
    return result


def update_inventory(products, updates):
    """Apply inventory updates to product list."""
    lookup = {p["sku"]: p for p in products}
    for upd in updates:
        sku = upd["sku"]
        if sku in lookup:
            lookup[sku]["stock"] = upd["new_stock"]
            lookup[sku]["last_updated"] = upd["timestamp"]
    return list(lookup.values())


def search_products(products, query):
    """Search products by name or description."""
    query_lower = query.lower()
    matches = []
    for p in products:
        if query_lower in p["name"].lower() or query_lower in p.get("description", "").lower():
            matches.append(p)
    return matches
'''


def create_initial():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    with open(OUTPUT, 'w') as f:
        f.write(CATALOG_CODE)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the file open
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
