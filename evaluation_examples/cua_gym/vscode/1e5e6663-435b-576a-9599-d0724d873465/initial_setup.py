"""
Initial Setup: Configure Todo Tree extension with custom tag highlights
Task ID: vscode_we_068
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
WORKSPACE_DIR = os.path.join(HOME, "workspace")


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


def install_extension(extension_id: str):
    """Install a VSCode extension."""
    subprocess.run(["code", "--install-extension", extension_id], check=True)


def create_initial():
    # Step 1: Install the Todo Tree extension
    print("Installing Gruntfuggly.todo-tree extension...")
    install_extension("Gruntfuggly.todo-tree")
    print("Extension installed.")

    # Step 2: Ensure settings.json has only the base trust settings (no todo-tree config)
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {
        "security.workspace.trust.enabled": False,
        "security.workspace.trust.startupPrompt": "never",
        "security.workspace.trust.emptyWindow": False
    }
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings written: {SETTINGS_PATH}")

    # Step 3: Create a workspace with sample files containing TODO/FIXME/HACK/BUG tags
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Sample Python file with various tags
    with open(os.path.join(WORKSPACE_DIR, "app.py"), "w") as f:
        f.write('''"""
E-commerce Order Processing Module
"""
import datetime
from decimal import Decimal


class OrderProcessor:
    """Handles order validation, pricing, and fulfillment."""

    TAX_RATE = Decimal("0.08")
    FREE_SHIPPING_THRESHOLD = Decimal("75.00")

    def __init__(self, db_connection):
        self.db = db_connection
        self.pending_orders = []

    def validate_order(self, order):
        """Validate order data before processing."""
        # TODO: Add support for international address validation
        if not order.get("customer_id"):
            raise ValueError("Missing customer ID")
        if not order.get("items"):
            raise ValueError("Order must contain at least one item")
        # FIXME: Quantity check fails for fractional units (e.g., fabric by the meter)
        for item in order["items"]:
            if item["quantity"] <= 0:
                raise ValueError(f"Invalid quantity for item {item['sku']}")
        return True

    def calculate_total(self, order):
        """Calculate order total with tax and shipping."""
        subtotal = sum(
            Decimal(str(item["price"])) * item["quantity"]
            for item in order["items"]
        )
        tax = subtotal * self.TAX_RATE
        # HACK: Hardcoded flat-rate shipping until the carrier API integration is done
        shipping = Decimal("0.00") if subtotal >= self.FREE_SHIPPING_THRESHOLD else Decimal("9.99")
        return {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": subtotal + tax + shipping,
        }

    def process_payment(self, order_id, payment_info):
        """Process payment for an order."""
        # BUG: Race condition when two payments hit the same order simultaneously
        order = self.db.get_order(order_id)
        if order["status"] != "pending":
            raise RuntimeError(f"Order {order_id} is not in pending state")
        # TODO: Implement retry logic for transient gateway failures
        result = self._charge_card(payment_info)
        if result["success"]:
            self.db.update_order_status(order_id, "paid")
        return result

    def _charge_card(self, payment_info):
        """Simulate card charge."""
        # FIXME: Card expiry validation uses wrong date format (MM/YY vs MM/YYYY)
        return {"success": True, "transaction_id": "txn_abc123"}

    def fulfill_order(self, order_id):
        """Send order to warehouse for fulfillment."""
        order = self.db.get_order(order_id)
        # HACK: Bypassing inventory check because the warehouse API returns stale data
        shipment = {
            "order_id": order_id,
            "items": order["items"],
            "shipped_at": datetime.datetime.utcnow().isoformat(),
        }
        # BUG: Tracking number is not persisted when the notification service is down
        self.db.update_order_status(order_id, "shipped")
        return shipment
''')

    # Sample JavaScript file
    with open(os.path.join(WORKSPACE_DIR, "utils.js"), "w") as f:
        f.write('''/**
 * Utility functions for data transformation and caching.
 */

const CACHE_TTL = 300; // seconds

// TODO: Replace in-memory cache with Redis for multi-instance deployments
const cache = new Map();

function memoize(fn, ttlSeconds = CACHE_TTL) {
    return function (...args) {
        const key = JSON.stringify(args);
        const cached = cache.get(key);
        if (cached && Date.now() - cached.ts < ttlSeconds * 1000) {
            return cached.value;
        }
        const result = fn.apply(this, args);
        cache.set(key, { value: result, ts: Date.now() });
        return result;
    };
}

// FIXME: Does not handle nested arrays — flattens them incorrectly
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// BUG: Timezone offset is applied twice when the server locale differs from UTC
function formatDate(isoString) {
    const d = new Date(isoString);
    const offset = d.getTimezoneOffset() * 60000;
    const local = new Date(d.getTime() - offset);
    return local.toISOString().split("T")[0];
}

module.exports = { memoize, deepClone, formatDate };
''')

    print(f"Workspace created at {WORKSPACE_DIR} with sample files.")

    # Step 4: Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
