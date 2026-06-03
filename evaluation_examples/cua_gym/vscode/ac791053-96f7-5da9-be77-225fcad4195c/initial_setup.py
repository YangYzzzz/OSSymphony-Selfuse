"""
Initial Setup: Extract Variable refactoring in calculator.py
Task ID: vscode_py_041
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_041'
OUTPUT = f'{WORKDIR}/calculator.py'


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
    # Create a realistic calculator.py where line 18 has the complex expression
    content = '''\
"""
Pricing Calculator Module

Computes final prices for retail orders based on customer loyalty,
membership level, and promotional campaigns.
"""

import math


class PricingCalculator:
    """Handles price calculations for the retail ordering system."""

    TAX_RATE = 0.08
    BASE_SHIPPING = 5.99

    def calculate_discounted_total(self, price, loyalty_years, membership_level):
        total = price * (1 - (loyalty_years * 0.02 + membership_level * 0.05))
        return round(total, 2)

    def calculate_tax(self, subtotal):
        """Calculate tax on the given subtotal."""
        return round(subtotal * self.TAX_RATE, 2)

    def calculate_shipping(self, weight_kg, is_express=False):
        """Determine shipping cost based on weight and delivery type."""
        rate_per_kg = 1.50 if not is_express else 3.25
        shipping = self.BASE_SHIPPING + weight_kg * rate_per_kg
        return round(shipping, 2)

    def generate_invoice_total(self, price, loyalty_years, membership_level,
                               weight_kg, is_express=False):
        """Compute the full invoice total including discounts, tax, and shipping."""
        discounted = self.calculate_discounted_total(price, loyalty_years, membership_level)
        tax = self.calculate_tax(discounted)
        shipping = self.calculate_shipping(weight_kg, is_express)
        return round(discounted + tax + shipping, 2)


if __name__ == "__main__":
    calc = PricingCalculator()

    # Sample order: $250 item, 3 years loyalty, level 2 membership
    result = calc.calculate_discounted_total(250.00, 3, 2)
    print(f"Discounted total: ${result}")

    invoice = calc.generate_invoice_total(250.00, 3, 2, 2.5, is_express=True)
    print(f"Invoice total: ${invoice}")
'''

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Verify line 18 is correct
    lines = content.split('\n')
    print(f'Line 18: {lines[17]!r}')
    assert '(loyalty_years * 0.02 + membership_level * 0.05)' in lines[17], \
        f"Line 18 mismatch! Got: {lines[17]!r}"

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
