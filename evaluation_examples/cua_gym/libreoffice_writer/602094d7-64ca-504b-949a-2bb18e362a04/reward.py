"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m trying to give “Table 1” a cleaner look in LibreOffice Writer. What’s the quickest way to apply zebra-striping so that every alternate row (i.e., rows 2, 4, 6, …) is filled with 10 % gray (#E5E5E5) while the other rows stay white?
Generated: 2025-09-10 15:35:19
Status: success
Model: azure-o3
Total Steps: 3
"""

def verify_task(file_path):
    """
    Reward script to verify zebra-striping on **Table 1** in the submitted
    LibreOffice/Word document.

    Requirements to earn full credit (score = 1.0):
      1. Document contains at least one table (Table 1).
      2. Every **even-numbered** row (2, 4, 6, …) in Table 1 is filled with
         10 % gray – hex colour #E5E5E5.
      3. Every **odd-numbered** row (1, 3, 5, …) has *no* shading (white).

    Progressive scoring (total 1.0):
      • 0.2 – table detected.
      • 0.3 – ≥ 70 % of even rows are correctly gray *and* ≥ 70 % of odd rows are
               correctly white.
      • Up to 0.5 – proportional to overall correctness (min ratio of the two
               categories). If both categories are 100 % correct the full 0.5
               is granted, yielding a perfect 1.0.
    """
    import os
    from docx import Document

    print(f"Starting verification for: {file_path}")
    max_score = 1.0
    score = 0.0

    # ---------- prerequisite: file must exist & open ----------
    if not os.path.exists(file_path):
        print("✗ File not found – aborting")
        return 0.0  # no score if file missing
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error opening document: {e}")
        return 0.0

    # ---------- requirement 1: table presence ----------
    tables = doc.tables
    if not tables:
        print("✗ No tables detected in document")
        return 0.0
    print(f"✓ Found {len(tables)} table(s)")
    score += 0.2  # Award only because task explicitly requires a table

    table = tables[0]  # Table 1 assumed to be the first table
    total_rows = len(table.rows)
    total_cols = len(table.columns)
    print(f"Analyzing Table 1 – size: {total_rows} rows × {total_cols} columns")
    if total_rows == 0 or total_cols == 0:
        print("✗ Table contains no data – cannot verify striping")
        return score  # keep the 0.2 if table is empty

    # ---------- helper: extract cell shading colour ----------
    def get_fill(cell):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = tc_pr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}shd')
        if shd is not None:
            fill_val = shd.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill')
            if fill_val is not None:
                return fill_val.upper()
        return None  # no shading (interpreted as white)

    GREY_10 = {"E5E5E5"}
    WHITE_ALLOWED = {None, "", "FFFFFF", "AUTO"}

    even_total = odd_total = 0
    even_ok = odd_ok = 0
    incorrect_rows = []  # collect rows that violate spec

    for r_idx, row in enumerate(table.rows):
        human_idx = r_idx + 1  # user-friendly numbering starts at 1
        fills = [get_fill(c) for c in row.cells]

        if human_idx % 2 == 0:  # even rows → expect grey
            even_total += 1
            if all(fill in GREY_10 for fill in fills):
                even_ok += 1
            else:
                incorrect_rows.append((human_idx, fills))
        else:  # odd rows → expect white / no shading
            odd_total += 1
            if all(fill in WHITE_ALLOWED for fill in fills):
                odd_ok += 1
            else:
                incorrect_rows.append((human_idx, fills))

    # ---------- scoring based on correctness ----------
    print(f"Even rows correct: {even_ok}/{even_total}")
    print(f"Odd  rows correct: {odd_ok}/{odd_total}")

    if even_total and odd_total:
        even_ratio = even_ok / even_total
        odd_ratio  = odd_ok  / odd_total

        # +0.3 if both categories ≥ 70 % correct
        if even_ratio >= 0.7 and odd_ratio >= 0.7:
            score += 0.3

        # Additional up-to-0.5 proportional to weakest ratio
        score += 0.5 * min(even_ratio, odd_ratio)

    score = min(score, max_score)  # safety cap

    # ---------- reporting ----------
    if incorrect_rows:
        print("Rows with unexpected shading:")
        for idx, fills in incorrect_rows:
            print(f"  Row {idx}: {fills}")

    print(f"Final score: {score}")
    return score


if __name__ == "__main__":
    DOC_PATH = "/home/user/im_trying_to_give_table_1_a_cleaner_look_in_libreoffice_writer_whats_the_quickest_way_to_apply_zebra.docx"
    reward = verify_task(DOC_PATH)
    print(f"REWARD: {reward}")
