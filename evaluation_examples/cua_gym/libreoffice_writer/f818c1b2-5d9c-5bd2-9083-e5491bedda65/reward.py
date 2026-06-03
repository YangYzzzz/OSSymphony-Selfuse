"""
Reward Script: Lease Agreement in LibreOffice Writer
Task ID: writer_wf_042
Domain: libreoffice_writer
Scoring:
  Component 1: Title present, centered, bold (0.15)
  Component 2: Party details with Landlord/Tenant sections (0.15)
  Component 3: 12 numbered articles present with correct topics (0.40)
  Component 4: Articles have body text (2-3 sentences each) (0.15)
  Component 5: Execution section with signatures, dates, witnesses (0.15)
"""

import os
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_042'

EXPECTED_ARTICLES = [
    "premises",
    "term",
    "rent",
    "security deposit",
    "utilities",
    "maintenance",
    "rules",
    "insurance",
    "termination",
    "default",
    "notices",
    "entire agreement",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    all_paras = doc.paragraphs
    all_texts = [p.text.strip() for p in all_paras]

    # Precondition gate: document must have at least 10 paragraphs with content
    content_paras = [t for t in all_texts if t]
    if len(content_paras) < 10:
        print(f"FAIL: Document too short — only {len(content_paras)} non-empty paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title "RESIDENTIAL LEASE AGREEMENT" centered and bold (0.15 points)
    try:
        title_found = False
        title_centered = False
        title_bold = False
        for p in all_paras:
            if "residential lease agreement" in p.text.strip().lower():
                title_found = True
                if p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                    title_centered = True
                # Check if at least one run is bold and contains the title text
                for r in p.runs:
                    if r.bold and "residential lease agreement" in r.text.strip().lower():
                        title_bold = True
                        break
                break

        if title_found and title_centered and title_bold:
            print(f"PASS: Component 1 — Title is present, centered, and bold (0.15 pts)")
            total_score += 0.15
        elif title_found and (title_centered or title_bold):
            print(f"PARTIAL: Component 1 — Title found but missing {'center' if not title_centered else 'bold'} (0.07 pts)")
            total_score += 0.07
        elif title_found:
            print(f"PARTIAL: Component 1 — Title found but not centered or bold (0.03 pts)")
            total_score += 0.03
        else:
            print(f"FAIL: Component 1 — Title 'RESIDENTIAL LEASE AGREEMENT' not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Party details section with Landlord and Tenant (0.15 points)
    try:
        full_text_lower = "\n".join(all_texts).lower()
        has_landlord = False
        has_tenant = False
        has_address_blanks = False

        for p in all_paras:
            t = p.text.strip().lower()
            if t.startswith("landlord:") or t.startswith("landlord :"):
                has_landlord = True
            if t.startswith("tenant:") or t.startswith("tenant :"):
                has_tenant = True
            if "address:" in t and ("___" in t or "____" in t):
                has_address_blanks = True

        party_score = 0.0
        if has_landlord:
            party_score += 0.05
        if has_tenant:
            party_score += 0.05
        if has_address_blanks:
            party_score += 0.05

        if party_score > 0:
            print(f"PASS: Component 2 — Party details: landlord={has_landlord}, tenant={has_tenant}, address_blanks={has_address_blanks} ({party_score} pts)")
            total_score += party_score
        else:
            print(f"FAIL: Component 2 — No party details (Landlord/Tenant) found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 12 numbered articles with correct topics (0.40 points)
    try:
        found_articles = []
        article_indices = []  # track paragraph indices of article headers

        for idx, p in enumerate(all_paras):
            t = p.text.strip().lower()
            # Match patterns like "article 1: premises" or "article 1. premises"
            match = re.match(r'article\s+(\d+)\s*[:.\-]\s*(.*)', t)
            if match:
                num = int(match.group(1))
                topic = match.group(2).strip()
                found_articles.append((num, topic))
                article_indices.append(idx)

        # Check how many of the 12 expected articles are present
        matched_articles = 0
        for i, expected_topic in enumerate(EXPECTED_ARTICLES):
            article_num = i + 1
            for num, topic in found_articles:
                if num == article_num and expected_topic in topic:
                    matched_articles += 1
                    break

        # Score: proportional to how many of the 12 articles are found (0.40 points total)
        article_ratio = matched_articles / 12.0
        article_score = round(article_ratio * 0.40, 4)
        if article_score > 0:
            print(f"PASS: Component 3 — {matched_articles}/12 articles found with correct topics ({article_score} pts)")
            total_score += article_score
        else:
            print(f"FAIL: Component 3 — No matching articles found. Found headers: {found_articles}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Articles have body text (2-3 sentences each) (0.15 points)
    try:
        articles_with_body = 0
        if article_indices:
            for k, art_idx in enumerate(article_indices):
                # Look at paragraphs after this article header until the next header or end
                next_idx = article_indices[k + 1] if k + 1 < len(article_indices) else len(all_paras)
                body_text = ""
                for bi in range(art_idx + 1, next_idx):
                    bt = all_paras[bi].text.strip()
                    # Stop if we hit another article or a major section header
                    if bt and not re.match(r'article\s+\d+', bt.lower()):
                        body_text += bt + " "

                # Count sentences (rough: split on period followed by space or end)
                sentences = [s.strip() for s in re.split(r'[.!?]+', body_text) if len(s.strip()) > 10]
                if len(sentences) >= 2:
                    articles_with_body += 1

            body_ratio = articles_with_body / max(len(article_indices), 1)
            body_score = round(body_ratio * 0.15, 4)
            if body_score > 0:
                print(f"PASS: Component 4 — {articles_with_body}/{len(article_indices)} articles have adequate body text ({body_score} pts)")
                total_score += body_score
            else:
                print(f"FAIL: Component 4 — No articles have adequate body text (2+ sentences)")
        else:
            print(f"FAIL: Component 4 — No article headers found, cannot check body text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Execution section with signatures, dates, witnesses (0.15 points)
    try:
        has_execution = False
        has_signature_lines = False
        has_date_lines = False
        has_witnesses = False

        for p in all_paras:
            t = p.text.strip().lower()
            if "execution" in t or "in witness whereof" in t:
                has_execution = True
            if "signature:" in t or "signature :" in t:
                has_signature_lines = True
            if t.startswith("date:") or t.startswith("date :"):
                has_date_lines = True
            if "witness" in t:
                has_witnesses = True

        exec_score = 0.0
        if has_execution:
            exec_score += 0.04
        if has_signature_lines:
            exec_score += 0.04
        if has_date_lines:
            exec_score += 0.04
        if has_witnesses:
            exec_score += 0.03

        if exec_score > 0:
            print(f"PASS: Component 5 — Execution section: execution_header={has_execution}, signatures={has_signature_lines}, dates={has_date_lines}, witnesses={has_witnesses} ({exec_score} pts)")
            total_score += exec_score
        else:
            print(f"FAIL: Component 5 — No execution section elements found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
