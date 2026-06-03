"""
Reward Script: Generate individual survey response PDFs from customer feedback Excel
Task ID: osworld_multi_apps_excel_pdf_form_010
Domain: multi_apps (libreoffice_calc + PDF generation)

Scoring Rubric:
- Component 1 (0.4 pts): All 12 PDF files exist on Desktop with correct FeedbackID names
- Component 2 (0.3 pts): PDFs contain correct customer data (FeedbackID, CustomerName, Product, Date)
- Component 3 (0.3 pts): PDFs have correct rating mark and recommend mark

Expected FeedbackIDs: FB-2025-001 through FB-2025-012
Rating mark: 'X' appears immediately before the selected rating line
Recommend mark: 'X' appears immediately before the selected Y/N line
"""

import os
import subprocess

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_excel_pdf_form_010'

# Ground truth from customer_feedback.xlsx
EXPECTED_CUSTOMERS = [
    {'id': 'FB-2025-001', 'name': 'Sarah Chen', 'product': 'UltraBoost Pro Headphones', 'date': '2025-01-10', 'rating': 5, 'recommend': 'Y', 'comment': 'Absolutely love the sound quality'},
    {'id': 'FB-2025-002', 'name': 'Marcus Johnson', 'product': 'SmartHome Hub X200', 'date': '2025-01-15', 'rating': 4, 'recommend': 'Y', 'comment': 'Good product overall'},
    {'id': 'FB-2025-003', 'name': 'Elena Rodriguez', 'product': 'ErgoDesk Standing Desk Pro', 'date': '2025-01-18', 'rating': 5, 'recommend': 'Y', 'comment': 'This desk has transformed'},
    {'id': 'FB-2025-004', 'name': 'David Kim', 'product': 'FitTrack Smartwatch Series 3', 'date': '2025-01-22', 'rating': 3, 'recommend': 'N', 'comment': 'Battery life is disappointing'},
    {'id': 'FB-2025-005', 'name': 'Priya Patel', 'product': 'CloudStor Portable SSD 2TB', 'date': '2025-01-25', 'rating': 5, 'recommend': 'Y', 'comment': 'Incredibly fast transfer speeds'},
    {'id': 'FB-2025-006', 'name': "James O'Brien", 'product': 'AquaPure Water Filtration Sys', 'date': '2025-02-02', 'rating': 4, 'recommend': 'Y', 'comment': 'Installation was easy'},
    {'id': 'FB-2025-007', 'name': 'Mei-Ling Zhang', 'product': 'LuminaDesk LED Monitor 27in', 'date': '2025-02-05', 'rating': 5, 'recommend': 'Y', 'comment': 'Display colors are vibrant'},
    {'id': 'FB-2025-008', 'name': 'Robert Vasquez', 'product': 'SwiftKey Mechanical Keyboard', 'date': '2025-02-10', 'rating': 4, 'recommend': 'Y', 'comment': 'Tactile feedback is satisfying'},
    {'id': 'FB-2025-009', 'name': 'Aisha Williams', 'product': 'NutriBlend Pro Blender 1200W', 'date': '2025-02-14', 'rating': 2, 'recommend': 'N', 'comment': 'Leaks around the blade'},
    {'id': 'FB-2025-010', 'name': 'Thomas Nguyen', 'product': 'PowerCell Solar Charger 20W', 'date': '2025-02-18', 'rating': 4, 'recommend': 'Y', 'comment': 'Works great for camping'},
    {'id': 'FB-2025-011', 'name': 'Sofia Kowalski', 'product': 'BrewMaster Coffee Station Pro', 'date': '2025-02-22', 'rating': 5, 'recommend': 'Y', 'comment': 'Makes the best espresso'},
    {'id': 'FB-2025-012', 'name': 'Nathan Brooks', 'product': 'CoolMax Air Purifier HEPA 500', 'date': '2025-02-28', 'rating': 3, 'recommend': 'Y', 'comment': 'Air quality noticeably improved'},
]

RATING_LABELS = {
    1: '1 - Very Dissatisfied',
    2: '2 - Dissatisfied',
    3: '3 - Neutral',
    4: '4 - Satisfied',
    5: '5 - Very Satisfied',
}


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ['pdftotext', pdf_path, '-'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"ERROR extracting PDF text from {pdf_path}: {e}")
        return None


def check_rating_marked(lines, expected_rating):
    """
    Check that the correct rating is marked with 'X'.
    The 'X' appears on the line just before the selected rating label.
    Pattern: [..., 'X', '', 'N - RatingLabel', ...] or [..., 'X', 'N - RatingLabel', ...]
    """
    rating_label = RATING_LABELS[expected_rating]
    for i, line in enumerate(lines):
        if line.strip() == rating_label:
            # Check if 'X' appears in the 1-2 lines before this label
            for offset in [1, 2]:
                if i - offset >= 0 and lines[i - offset].strip() == 'X':
                    return True
    return False


def check_recommend_marked(lines, expected_recommend):
    """
    Check that the correct recommend option is marked with 'X'.
    'X' appears just before the selected Y/N option label.
    """
    if expected_recommend == 'Y':
        target_label = 'Y - Yes, I would recommend'
    else:
        target_label = 'N - No, I would not recommend'

    for i, line in enumerate(lines):
        if target_label in line:
            # Check if 'X' appears in the 1-2 lines before this label
            for offset in [1, 2]:
                if i - offset >= 0 and lines[i - offset].strip() == 'X':
                    return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 12 PDF files exist with correct FeedbackID names (0.4 points)
    try:
        existing_pdfs = []
        missing_pdfs = []

        for customer in EXPECTED_CUSTOMERS:
            pdf_name = f"{customer['id']}.pdf"
            pdf_path = os.path.join(DESKTOP, pdf_name)
            if os.path.isfile(pdf_path):
                existing_pdfs.append(pdf_name)
            else:
                missing_pdfs.append(pdf_name)

        if len(missing_pdfs) == 0:
            print(f"PASS: Component 1 — All 12 PDFs exist on Desktop (0.4 pts)")
            total_score += 0.4
        elif len(existing_pdfs) >= 6:
            partial = round(0.4 * len(existing_pdfs) / 12, 2)
            print(f"PARTIAL: Component 1 — {len(existing_pdfs)}/12 PDFs exist ({partial} pts). Missing: {missing_pdfs[:3]}...")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {len(existing_pdfs)}/12 PDFs exist. Missing: {missing_pdfs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDFs contain correct customer data (FeedbackID, Name, Date) (0.3 points)
    try:
        data_correct_count = 0
        data_total_checked = 0

        # Check all available PDFs for customer data
        for customer in EXPECTED_CUSTOMERS:
            pdf_path = os.path.join(DESKTOP, f"{customer['id']}.pdf")
            if not os.path.isfile(pdf_path):
                continue

            text = extract_pdf_text(pdf_path)
            if text is None:
                continue

            data_total_checked += 1
            # Check that the FeedbackID, CustomerName, and PurchaseDate appear in the PDF text
            has_id = customer['id'] in text
            has_name = customer['name'] in text
            has_date = customer['date'] in text

            if has_id and has_name and has_date:
                data_correct_count += 1
            else:
                missing = []
                if not has_id:
                    missing.append(f"FeedbackID={customer['id']}")
                if not has_name:
                    missing.append(f"Name={customer['name']}")
                if not has_date:
                    missing.append(f"Date={customer['date']}")
                print(f"FAIL: Component 2 — {customer['id']}.pdf missing: {missing}")

        if data_total_checked == 0:
            print(f"FAIL: Component 2 — No PDFs available to check")
        elif data_correct_count == data_total_checked:
            print(f"PASS: Component 2 — All {data_total_checked} PDFs have correct customer data (0.3 pts)")
            total_score += 0.3
        elif data_correct_count >= data_total_checked * 0.5:
            partial = round(0.3 * data_correct_count / max(data_total_checked, 12), 2)
            print(f"PARTIAL: Component 2 — {data_correct_count}/{data_total_checked} PDFs have correct data ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {data_correct_count}/{data_total_checked} PDFs have correct customer data")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDFs have correct rating and recommend marks (0.3 points)
    try:
        marks_correct_count = 0
        marks_total_checked = 0

        for customer in EXPECTED_CUSTOMERS:
            pdf_path = os.path.join(DESKTOP, f"{customer['id']}.pdf")
            if not os.path.isfile(pdf_path):
                continue

            text = extract_pdf_text(pdf_path)
            if text is None:
                continue

            marks_total_checked += 1
            lines = text.split('\n')

            rating_ok = check_rating_marked(lines, customer['rating'])
            recommend_ok = check_recommend_marked(lines, customer['recommend'])

            if rating_ok and recommend_ok:
                marks_correct_count += 1
            else:
                issues = []
                if not rating_ok:
                    issues.append(f"rating mark missing (expected {customer['rating']})")
                if not recommend_ok:
                    issues.append(f"recommend mark missing (expected {customer['recommend']})")
                print(f"FAIL: Component 3 — {customer['id']}.pdf: {', '.join(issues)}")

        if marks_total_checked == 0:
            print(f"FAIL: Component 3 — No PDFs available to check")
        elif marks_correct_count == marks_total_checked:
            print(f"PASS: Component 3 — All {marks_total_checked} PDFs have correct rating and recommend marks (0.3 pts)")
            total_score += 0.3
        elif marks_correct_count >= marks_total_checked * 0.5:
            partial = round(0.3 * marks_correct_count / max(marks_total_checked, 12), 2)
            print(f"PARTIAL: Component 3 — {marks_correct_count}/{marks_total_checked} PDFs have correct marks ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {marks_correct_count}/{marks_total_checked} PDFs have correct marks")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
