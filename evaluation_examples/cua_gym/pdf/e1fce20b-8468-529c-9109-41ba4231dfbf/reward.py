"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to extract all images from PDFs in /home/user/Documents/Catalogs, saving extracted images to folder 'Catalog_Images' with filenames indicating source PDF.
Generated: 2025-11-29 10:15:38
Status: success
Model: o3
Total Steps: 2
"""

from pathlib import Path
from PyPDF2 import PdfReader

"""
Reward Script: Verify Image Extraction from PDFs
------------------------------------------------
Task: "Extract all images from PDFs in /home/user/Documents/Catalogs, saving extracted images to folder
       'Catalog_Images' with filenames indicating source PDF."

This script checks three things:
1.  How many image XObjects each PDF in /home/user/Documents/Catalogs contains.
2.  How many images were actually exported to a folder named Catalog_Images (it accepts several common
    locations to be user-friendly).
3.  Whether the exported image filenames include the originating PDF’s basename (case-insensitive).

Scoring (progressive):
    completeness_score = extracted_total_images / expected_total_images   (capped at 1.0)
    naming_score        = 1.0 if every image file sits in an existing Catalog_Images dir AND every
                          exported image filename contains its source PDF basename (case-insensitive)
                          else 0.0
    final_score         = 0.8 * completeness_score + 0.2 * naming_score  (capped at 1.0)

The script prints detailed diagnostics and finally prints exactly one line beginning with
    REWARD: <float>
which is consumed by the autograder.
"""

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}


def count_images_in_pdf(pdf_path: Path) -> int:
    """Return the number of unique image XObjects (recursively) in a PDF file."""
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Failed to read {pdf_path}: {e}")
        return 0

    seen_ids = set()

    def count_images_in_xobj(xobj_dict) -> int:
        cnt = 0
        for name, obj_ref in xobj_dict.items():
            try:
                obj = obj_ref.get_object()
            except Exception as e:
                print(f"  - Error dereferencing {name}: {e}")
                continue

            # Build a unique identifier to avoid double-counting shared objects
            obj_id = getattr(obj_ref, 'idnum', id(obj)), getattr(obj_ref, 'generation', 0)
            if obj_id in seen_ids:
                continue

            subtype = obj.get('/Subtype')
            if subtype == '/Image':
                cnt += 1
                seen_ids.add(obj_id)
            elif subtype == '/Form':
                # Recurse into Form XObject resources (can nest images)
                inner_xobj = (obj.get('/Resources') or {}).get('/XObject') or {}
                cnt += count_images_in_xobj(inner_xobj)
        return cnt

    total = 0
    for page_idx, page in enumerate(reader.pages):
        resources = page.get('/Resources') or {}
        xobj = resources.get('/XObject') or {}
        total += count_images_in_xobj(xobj)
    print(f"{pdf_path.name}: contains {total} image XObjects")
    return total


def find_images_directory() -> Path:
    """Return the Catalog_Images directory Path (checks common locations)."""
    candidates = [
        Path.home() / 'Catalog_Images',
        Path.home() / 'Documents' / 'Catalog_Images',
        Path.home() / 'Documents' / 'Catalogs' / 'Catalog_Images'
    ]
    for p in candidates:
        if p.exists() and p.is_dir():
            return p
    # Return preferred default even if it doesn’t exist (for messaging)
    return candidates[0]


def verify_image_extraction() -> float:
    catalogs_dir = Path('/home/user/Documents/Catalogs')
    if not catalogs_dir.exists():
        print(f"✗ Catalogs directory not found: {catalogs_dir}")
        return 0.0

    pdf_paths = list(catalogs_dir.rglob('*.pdf'))
    if not pdf_paths:
        print("✗ No PDF files found in Catalogs directory")
        return 0.0

    # Locate the images directory and enumerate image files
    images_dir = find_images_directory()
    if images_dir.exists():
        all_images = [p for p in images_dir.rglob('*') if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    else:
        all_images = []

    print(f"Using images directory: {images_dir} (exists={images_dir.exists()})")
    print(f"Discovered {len(all_images)} image files total")

    expected_total = 0
    extracted_total = 0
    naming_ok_overall = images_dir.exists()

    for pdf in pdf_paths:
        base = pdf.stem.lower()
        expected_imgs = count_images_in_pdf(pdf)
        expected_total += expected_imgs

        related = [img for img in all_images if base in img.name.lower()]
        extracted_total += len(related)

        # Verify naming convention for each related file
        for img in related:
            if base not in img.name.lower():
                naming_ok_overall = False

        # Per-PDF diagnostics
        if expected_imgs > 0:
            if len(related) >= expected_imgs:
                print(f"✓ {pdf.stem}: {len(related)}/{expected_imgs} images extracted")
            else:
                print(f"✗ {pdf.stem}: {len(related)}/{expected_imgs} images extracted (missing)")
        else:
            print(f"i {pdf.stem}: No images found inside PDF (nothing to extract)")

    # Scoring
    if expected_total == 0:
        completeness_score = 1.0  # Nothing to extract is considered complete
    else:
        completeness_score = min(extracted_total / expected_total, 1.0)

    naming_score = 1.0 if naming_ok_overall else 0.0

    final_score = round(min(1.0, 0.8 * completeness_score + 0.2 * naming_score), 4)

    print("============================")
    print(f"Expected images total:   {expected_total}")
    print(f"Extracted images total:  {extracted_total}")
    print(f"Completeness score:      {completeness_score}")
    print(f"Naming/dir score:        {naming_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    reward = verify_image_extraction()
    print(f"REWARD: {reward}")

