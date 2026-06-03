"""
Reward Script: Split collected_papers.odt into individual paper files with bookmarks and index
Task ID: osworld_multi_apps_book_splitting_nav_010
Domain: libreoffice_writer (ODT files)
Scoring:
  Component 1 (0.30): 8 paper .odt files exist in Desktop/papers/ with correct naming pattern
  Component 2 (0.40): Each paper file has abstract and conclusion bookmarks
  Component 3 (0.30): index.odt exists with correct table structure (6 cols, 9 rows)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_010'
PAPERS_DIR = '/home/user/Desktop/papers'

# Expected paper file names based on golden state
EXPECTED_PAPER_FILES = [
    'paper_01_neural_networks_for_image_recognition.odt',
    'paper_02_transformer_models_in_natural_language_processing.odt',
    'paper_03_reinforcement_learning_for_robotic_control.odt',
    'paper_04_graph_neural_networks_for_molecular_property_prediction.odt',
    'paper_05_federated_learning_for_privacy_preserving_machine_learning.odt',
    'paper_06_attention_mechanisms_in_computer_vision.odt',
    'paper_07_generative_adversarial_networks_for_data_augmentation.odt',
    'paper_08_knowledge_distillation_for_model_compression.odt',
]

# Expected bookmark names per paper
EXPECTED_BOOKMARKS = [
    ('abstract_paper_01', 'conclusion_paper_01'),
    ('abstract_paper_02', 'conclusion_paper_02'),
    ('abstract_paper_03', 'conclusion_paper_03'),
    ('abstract_paper_04', 'conclusion_paper_04'),
    ('abstract_paper_05', 'conclusion_paper_05'),
    ('abstract_paper_06', 'conclusion_paper_06'),
    ('abstract_paper_07', 'conclusion_paper_07'),
    ('abstract_paper_08', 'conclusion_paper_08'),
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Desktop/papers/ directory must exist
    if not os.path.isdir(PAPERS_DIR):
        print(f"CRITICAL: Papers directory not found: {PAPERS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # List all files in papers dir
    try:
        papers_files = set(os.listdir(PAPERS_DIR))
    except Exception as e:
        print(f"CRITICAL: Cannot list papers directory: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: 8 paper .odt files exist with correct naming (0.30 points)
    # Each file found earns 0.30/8 = 0.0375 points
    # -------------------------------------------------------------------------
    print("\n--- Component 1: Paper files present with correct names (0.30 pts) ---")
    component1_score = 0.0
    points_per_file = 0.30 / 8
    found_files = []
    missing_files = []

    for fname in EXPECTED_PAPER_FILES:
        if fname in papers_files:
            print(f"PASS: Found {fname}")
            component1_score += points_per_file
            found_files.append(fname)
        else:
            print(f"FAIL: Missing {fname}")
            missing_files.append(fname)

    component1_score = round(component1_score, 4)
    print(f"Component 1 score: {component1_score:.4f}/0.30")
    total_score += component1_score

    # -------------------------------------------------------------------------
    # Component 2: Each paper file has abstract and conclusion bookmarks (0.40 pts)
    # Each paper with both bookmarks earns 0.40/8 = 0.05 points
    # -------------------------------------------------------------------------
    print("\n--- Component 2: Abstract and conclusion bookmarks in each paper (0.40 pts) ---")
    component2_score = 0.0
    points_per_paper = 0.40 / 8

    try:
        from odf.opendocument import load
        from odf import text as odf_text

        for i, fname in enumerate(EXPECTED_PAPER_FILES):
            if fname not in found_files:
                print(f"SKIP: {fname} not present, cannot check bookmarks")
                continue

            fpath = os.path.join(PAPERS_DIR, fname)
            expected_abstract, expected_conclusion = EXPECTED_BOOKMARKS[i]

            try:
                doc = load(fpath)
                body = doc.text

                # Collect bookmark names (BookmarkStart elements)
                bookmark_names = set()
                for elem in body.getElementsByType(odf_text.BookmarkStart):
                    name = elem.getAttribute('name')
                    if name:
                        bookmark_names.add(name)
                for elem in body.getElementsByType(odf_text.Bookmark):
                    name = elem.getAttribute('name')
                    if name:
                        bookmark_names.add(name)

                has_abstract = expected_abstract in bookmark_names
                has_conclusion = expected_conclusion in bookmark_names

                if has_abstract and has_conclusion:
                    print(f"PASS: {fname} — bookmarks {expected_abstract} and {expected_conclusion} found")
                    component2_score += points_per_paper
                elif has_abstract:
                    print(f"PARTIAL: {fname} — abstract bookmark found but missing {expected_conclusion}")
                    component2_score += points_per_paper * 0.5
                elif has_conclusion:
                    print(f"PARTIAL: {fname} — conclusion bookmark found but missing {expected_abstract}")
                    component2_score += points_per_paper * 0.5
                else:
                    print(f"FAIL: {fname} — missing both bookmarks (found: {bookmark_names})")

            except Exception as e:
                print(f"ERROR: Cannot load {fname}: {e}")

    except ImportError as e:
        print(f"ERROR: odf library not available: {e}")

    component2_score = round(component2_score, 4)
    print(f"Component 2 score: {component2_score:.4f}/0.40")
    total_score += component2_score

    # -------------------------------------------------------------------------
    # Component 3: index.odt exists with correct table structure (0.30 pts)
    # Sub-checks:
    #   3a (0.10): index.odt file exists and has a table
    #   3b (0.10): Table has 6 columns (Paper #, Title, File Name, Abstract Bookmark, Conclusion Bookmark, Page Count)
    #   3c (0.10): Table has 9 rows (1 header + 8 paper rows)
    # -------------------------------------------------------------------------
    print("\n--- Component 3: index.odt with correct table structure (0.30 pts) ---")
    component3_score = 0.0
    index_path = os.path.join(PAPERS_DIR, 'index.odt')

    if 'index.odt' not in papers_files:
        print(f"FAIL: index.odt not found in {PAPERS_DIR}")
    else:
        try:
            from odf.opendocument import load
            from odf.table import Table, TableRow, TableCell
            from odf import teletype

            doc = load(index_path)
            body = doc.text
            tables = body.getElementsByType(Table)

            if len(tables) == 0:
                print("FAIL: index.odt has no table")
            else:
                # Sub-check 3a: Table exists (0.10 pts)
                print(f"PASS: index.odt contains {len(tables)} table(s)")
                component3_score += 0.10

                table = tables[0]
                rows = table.getElementsByType(TableRow)
                num_rows = len(rows)

                # Sub-check 3b: Table has 6 columns (0.10 pts)
                # Check header row for 6 cells
                if num_rows > 0:
                    header_row = rows[0]
                    header_cells = header_row.getElementsByType(TableCell)
                    num_cols = len(header_cells)

                    # Check that expected column headers are present
                    expected_headers = ['paper', 'title', 'file', 'abstract', 'conclusion', 'page']
                    header_texts = []
                    for cell in header_cells:
                        cell_text = teletype.extractText(cell).strip().lower()
                        header_texts.append(cell_text)

                    headers_ok = num_cols == 6
                    # Also check for key words in header text
                    all_text_joined = ' '.join(header_texts)
                    headers_content_ok = (
                        'abstract' in all_text_joined and
                        'conclusion' in all_text_joined and
                        ('page' in all_text_joined or 'count' in all_text_joined)
                    )

                    if headers_ok and headers_content_ok:
                        print(f"PASS: Table has 6 columns with correct headers: {header_texts}")
                        component3_score += 0.10
                    elif headers_ok:
                        print(f"PASS: Table has 6 columns (headers: {header_texts})")
                        component3_score += 0.10
                    else:
                        print(f"FAIL: Table has {num_cols} columns (expected 6), headers: {header_texts}")
                else:
                    print("FAIL: Table has no rows")

                # Sub-check 3c: Table has 9 rows (1 header + 8 papers) (0.10 pts)
                if num_rows == 9:
                    print(f"PASS: Table has {num_rows} rows (1 header + 8 papers)")
                    component3_score += 0.10
                else:
                    print(f"FAIL: Table has {num_rows} rows (expected 9: 1 header + 8 papers)")

        except ImportError as e:
            print(f"ERROR: odf library not available: {e}")
        except Exception as e:
            print(f"ERROR: Cannot load/parse index.odt: {e}")

    component3_score = round(component3_score, 4)
    print(f"Component 3 score: {component3_score:.4f}/0.30")
    total_score += component3_score

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
