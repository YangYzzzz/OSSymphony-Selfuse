"""
Initial Setup: Create multi-language PDF invoice generator environment
Task ID: pdf_gf3_043
Domain: pdf
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_043'

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
    # Create directory structure
    os.makedirs(f'{WORKDIR}/data', exist_ok=True)
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)
    os.makedirs(f'{WORKDIR}/output/invoices', exist_ok=True)

    # Create invoice data JSON
    invoice_data = {
        "invoice_number": "INV-2025-0847",
        "invoice_date": "2025-03-15",
        "due_date": "2025-04-14",
        "locale": "multi",
        "company": {
            "name": "NovaTech Solutions GmbH",
            "address": "Friedrichstrasse 123",
            "city": "Berlin",
            "postal_code": "10117",
            "country": "Germany",
            "vat_id": "DE298745123",
            "email": "billing@novatech-solutions.de",
            "phone": "+49 30 5557890"
        },
        "customer": {
            "name": "Meridian Logistics Corp.",
            "contact_person": "Elena Vasquez",
            "address": "425 Commerce Boulevard, Suite 300",
            "city": "Miami",
            "state": "FL",
            "postal_code": "33101",
            "country": "United States",
            "email": "elena.vasquez@meridianlogistics.com"
        },
        "line_items": [
            {
                "description": "Enterprise Cloud Migration - Phase 1",
                "quantity": 1,
                "unit_price": 12500.00,
                "tax_rate": 0.19
            },
            {
                "description": "Custom API Integration Development",
                "quantity": 3,
                "unit_price": 3750.00,
                "tax_rate": 0.19
            },
            {
                "description": "Database Optimization & Performance Tuning",
                "quantity": 2,
                "unit_price": 2800.00,
                "tax_rate": 0.19
            },
            {
                "description": "24/7 Technical Support Package (Monthly)",
                "quantity": 6,
                "unit_price": 1200.00,
                "tax_rate": 0.19
            },
            {
                "description": "Security Audit & Compliance Review",
                "quantity": 1,
                "unit_price": 4500.00,
                "tax_rate": 0.19
            }
        ],
        "currency": "USD",
        "payment_terms": "Net 30",
        "bank_details": {
            "bank_name": "Deutsche Bank",
            "iban": "DE89 3704 0044 0532 0130 00",
            "bic": "COBADEFFXXX"
        },
        "notes": "Thank you for your business. Please reference the invoice number in your payment."
    }

    json_path = f'{WORKDIR}/data/invoice_data.json'
    with open(json_path, 'w') as f:
        json.dump(invoice_data, f, indent=2)
    print(f'Invoice data created: {json_path}')

    # Ensure reportlab and babel are installed
    subprocess.run(['pip3', 'install', 'reportlab', 'babel'],
                   capture_output=True, timeout=60)
    print('Dependencies installed: reportlab, babel')

    # Open the data file in a text editor and the file manager
    launch_gui(f'xdg-open "{WORKDIR}/data"', delay_sec=1.5)
    launch_gui(f'gedit "{json_path}"', delay_sec=2.0)
    print('GUI_READY: launched file manager and text editor with DISPLAY=:0')

create_initial()
