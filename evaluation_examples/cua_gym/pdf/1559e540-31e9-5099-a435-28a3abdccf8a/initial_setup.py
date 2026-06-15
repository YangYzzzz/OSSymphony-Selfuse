"""
Initial Setup: Create a 20-page recipe book PDF with 15 embedded food photos
Task ID: pdf_cross_088
Domain: pdf

Creates: ~/Documents/recipe_book.pdf
  - 20 pages of recipe content
  - 15 food photography images embedded across the pages
  - Images are of various sizes (the agent must extract and resize them)
Opens the file in Evince for the GUI agent to work with.
"""

import os
import shlex
import subprocess
import time
import random
import struct
import zlib

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from PIL import Image, ImageDraw, ImageFont
import io

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_088'
OUTPUT = f'{WORKDIR}/recipe_book.pdf'


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


def make_food_image(width, height, food_name, bg_color, accent_color):
    """Create a synthetic food photograph image."""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a stylized food item
    cx, cy = width // 2, height // 2

    # Plate / bowl shape
    plate_r = min(width, height) // 3
    draw.ellipse(
        [cx - plate_r, cy - plate_r // 2, cx + plate_r, cy + plate_r // 2],
        fill=accent_color,
        outline=(200, 200, 200),
        width=3
    )

    # Food contents (abstract blobs)
    random.seed(hash(food_name) % 10000)
    for _ in range(8):
        bx = cx + random.randint(-plate_r // 2, plate_r // 2)
        by = cy + random.randint(-plate_r // 4, plate_r // 4)
        br = random.randint(8, 25)
        rc = (
            min(255, accent_color[0] + random.randint(-40, 40)),
            min(255, accent_color[1] + random.randint(-40, 40)),
            min(255, accent_color[2] + random.randint(-40, 40)),
        )
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=rc)

    # Label at bottom
    draw.rectangle([0, height - 40, width, height], fill=(30, 30, 30))
    draw.text((10, height - 30), food_name, fill=(255, 255, 255))

    return img


# 15 different food items with varying image sizes
FOOD_ITEMS = [
    ("Spaghetti Carbonara", (320, 240), (245, 235, 220), (180, 140, 90)),
    ("Beef Tacos", (400, 300), (255, 245, 230), (200, 100, 50)),
    ("Caesar Salad", (350, 280), (240, 250, 240), (80, 160, 60)),
    ("Margherita Pizza", (450, 350), (255, 240, 220), (220, 60, 40)),
    ("Grilled Salmon", (380, 260), (240, 240, 255), (220, 140, 60)),
    ("Chocolate Cake", (300, 300), (50, 30, 20), (90, 50, 30)),
    ("Chicken Tikka", (420, 310), (255, 240, 200), (210, 100, 20)),
    ("Greek Salad", (360, 270), (240, 255, 250), (50, 150, 200)),
    ("BBQ Ribs", (440, 320), (60, 40, 30), (160, 60, 20)),
    ("Shrimp Pasta", (390, 280), (255, 245, 235), (200, 120, 80)),
    ("Beef Burger", (410, 330), (245, 230, 210), (170, 90, 30)),
    ("Tiramisu", (340, 260), (240, 230, 200), (110, 70, 30)),
    ("Lobster Bisque", (360, 290), (255, 235, 200), (200, 80, 30)),
    ("Mushroom Risotto", (380, 300), (240, 235, 220), (130, 100, 60)),
    ("Lemon Tart", (320, 260), (255, 250, 220), (230, 200, 50)),
]


# Recipe text content for pages without images
RECIPE_NAMES = [name for name, _, _, _ in FOOD_ITEMS]

RECIPE_DESCRIPTIONS = {
    "Spaghetti Carbonara": "A classic Roman pasta dish made with eggs, Pecorino Romano, guanciale, and black pepper. The silky sauce clings to al dente pasta for a rich, satisfying meal.",
    "Beef Tacos": "Seasoned ground beef in crispy corn tortillas, topped with fresh salsa, shredded cheese, sour cream, and crisp lettuce. A weeknight family favorite.",
    "Caesar Salad": "Crisp romaine lettuce, house-made croutons, and shaved Parmesan tossed in a classic anchovy-garlic dressing. Finish with fresh lemon juice and cracked pepper.",
    "Margherita Pizza": "San Marzano tomato sauce, fresh mozzarella di bufala, and basil leaves on a hand-stretched Neapolitan crust, baked at high heat until perfectly charred.",
    "Grilled Salmon": "Atlantic salmon fillet marinated in lemon, dill, and olive oil, grilled over medium-high heat. Serve with roasted asparagus and hollandaise.",
    "Chocolate Cake": "A deeply moist three-layer chocolate cake with a rich ganache frosting. Uses Dutch-process cocoa and espresso powder to enhance the chocolate flavor.",
    "Chicken Tikka": "Tender chicken marinated in yogurt and aromatic spices, chargrilled to perfection. Served with a velvety tomato-cream sauce and fragrant basmati rice.",
    "Greek Salad": "Ripe tomatoes, cucumbers, Kalamata olives, red onion, and creamy feta cheese drizzled with extra virgin olive oil and dried oregano.",
    "BBQ Ribs": "Slow-smoked pork spare ribs coated in a sweet and smoky dry rub, then finished with a tangy Kansas City-style barbecue glaze.",
    "Shrimp Pasta": "Juicy tiger prawns sautéed in garlic butter with cherry tomatoes, white wine, and fresh herbs, tossed with linguine and finished with lemon zest.",
    "Beef Burger": "A half-pound smash burger made with 80/20 chuck, American cheese, caramelized onions, pickles, and special sauce on a brioche bun.",
    "Tiramisu": "Savoiardi biscuits soaked in espresso and Marsala, layered with a mascarpone-cream filling and finished with a dusting of fine cocoa powder.",
    "Lobster Bisque": "A velvety cream soup made from whole lobster shells, cognac, and aromatic vegetables, strained smooth and garnished with a swirl of cream and chive oil.",
    "Mushroom Risotto": "Arborio rice cooked slowly with a blend of wild mushrooms, dry white wine, and warm chicken stock, finished with cold butter and aged Parmigiano.",
    "Lemon Tart": "A buttery pâte sablée shell filled with a smooth, bright lemon curd made from fresh-squeezed juice and zest, topped with Italian meringue.",
}


def create_recipe_book():
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 595, 842  # A4

    # Page 1: Title page (no food image)
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    # Title background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H))
    shape.finish(fill=(0.95, 0.90, 0.82))
    shape.draw_rect(pymupdf.Rect(40, 40, PAGE_W - 40, PAGE_H - 40))
    shape.finish(color=(0.6, 0.3, 0.1), width=3)
    shape.commit()

    page.insert_text(pymupdf.Point(PAGE_W / 2 - 130, 250), "The Home Chef's",
                     fontsize=32, fontname="tibo", color=(0.5, 0.2, 0.05))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 130, 310), "Recipe Collection",
                     fontsize=40, fontname="tibo", color=(0.6, 0.25, 0.05))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 100, 400),
                     "15 Signature Dishes", fontsize=18, fontname="tiit",
                     color=(0.4, 0.2, 0.05))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 80, 750), "Gourmet Kitchen Press",
                     fontsize=12, fontname="helv", color=(0.5, 0.3, 0.1))

    # Page 2: Introduction page (no food image)
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 80), "Introduction",
                     fontsize=24, fontname="hebo", color=(0.4, 0.2, 0.05))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(PAGE_W - 72, 95))
    shape.finish(color=(0.6, 0.3, 0.1), width=1.5)
    shape.commit()

    intro_text = (
        "Welcome to our curated collection of 15 signature dishes, each crafted to bring "
        "restaurant-quality flavors into your home kitchen. From the rustic comfort of BBQ Ribs "
        "to the elegant refinement of Lobster Bisque, this collection spans the globe to celebrate "
        "the art of great cooking.\n\n"
        "Each recipe has been carefully tested and refined, providing clear instructions and "
        "professional photography to guide you from raw ingredients to a stunning finished dish. "
        "Whether you are an experienced home cook or just beginning your culinary journey, "
        "these recipes will inspire and delight.\n\n"
        "Take your time, enjoy the process, and savor every bite."
    )
    rect = pymupdf.Rect(72, 120, PAGE_W - 72, PAGE_H - 120)
    page.insert_textbox(rect, intro_text, fontsize=12, fontname="tiro",
                        color=(0.1, 0.1, 0.1))

    # Pages 3-17: One recipe per page (with image), then a text page
    # Place 15 recipe pages distributing across pages 3-17 (one image per page)
    # Then fill remaining pages to reach 20 total
    # Recipes are on pages 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17
    # Plus 3 more pages (18,19,20) for index / notes / back matter

    image_page_indices = []  # track which pages have images

    for i, (food_name, (img_w, img_h), bg_color, accent_color) in enumerate(FOOD_ITEMS):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_num = 3 + i  # pages 3..17
        image_page_indices.append(page_num)

        # Page header
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, 60))
        shape.finish(fill=(0.55, 0.27, 0.07))
        shape.commit()

        page.insert_text(pymupdf.Point(72, 40), food_name,
                         fontsize=20, fontname="hebo", color=(1.0, 0.95, 0.85))
        page.insert_text(pymupdf.Point(PAGE_W - 100, 40), f"Page {page_num}",
                         fontsize=10, fontname="helv", color=(1.0, 0.95, 0.85))

        # Generate and embed the food image
        food_img = make_food_image(img_w, img_h, food_name, bg_color, accent_color)
        img_bytes = io.BytesIO()
        food_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Place image in upper portion of page
        img_rect = pymupdf.Rect(72, 75, PAGE_W - 72, 350)
        page.insert_image(img_rect, stream=img_bytes.getvalue())

        # Recipe description text
        desc = RECIPE_DESCRIPTIONS.get(food_name, "A delicious and satisfying dish.")
        rect = pymupdf.Rect(72, 365, PAGE_W - 72, 580)
        page.insert_textbox(rect, desc, fontsize=11, fontname="tiro",
                            color=(0.1, 0.1, 0.1))

        # Ingredients section
        page.insert_text(pymupdf.Point(72, 595), "Key Ingredients:",
                         fontsize=13, fontname="hebo", color=(0.5, 0.2, 0.05))
        ingredients = [
            "• Fresh, high-quality protein (as specified)",
            "• Seasonal vegetables and aromatics",
            "• Extra virgin olive oil or butter",
            "• Fresh herbs: parsley, thyme, basil",
            "• Sea salt and freshly ground black pepper",
            "• Specialty items per recipe variation",
        ]
        y = 618
        for ing in ingredients:
            page.insert_text(pymupdf.Point(80, y), ing, fontsize=10,
                             fontname="helv", color=(0.2, 0.2, 0.2))
            y += 16

        # Cooking time / difficulty info
        difficulty_map = {
            0: "Easy | 30 min",  1: "Easy | 25 min",
            2: "Easy | 15 min",  3: "Medium | 40 min",
            4: "Medium | 35 min", 5: "Medium | 60 min",
            6: "Medium | 50 min", 7: "Easy | 20 min",
            8: "Hard | 4 hrs",   9: "Medium | 25 min",
            10: "Medium | 30 min", 11: "Medium | 45 min",
            12: "Hard | 90 min",  13: "Medium | 40 min",
            14: "Hard | 60 min",
        }
        time_str = difficulty_map.get(i, "Medium | 45 min")
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(72, 780, PAGE_W - 72, 810))
        shape.finish(fill=(0.93, 0.87, 0.75))
        shape.commit()
        page.insert_text(pymupdf.Point(80, 799), f"⏱  {time_str}",
                         fontsize=10, fontname="helv", color=(0.4, 0.2, 0.05))

    # Page 18: Recipe Index
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 80), "Recipe Index",
                     fontsize=24, fontname="hebo", color=(0.4, 0.2, 0.05))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(PAGE_W - 72, 95))
    shape.finish(color=(0.6, 0.3, 0.1), width=1.5)
    shape.commit()
    y = 120
    for i, (food_name, _, _, _) in enumerate(FOOD_ITEMS):
        page.insert_text(pymupdf.Point(80, y), f"{i + 1:2d}. {food_name}",
                         fontsize=12, fontname="helv", color=(0.1, 0.1, 0.1))
        dots = "." * 50
        page.insert_text(pymupdf.Point(280, y), dots,
                         fontsize=10, fontname="helv", color=(0.6, 0.6, 0.6))
        page.insert_text(pymupdf.Point(490, y), f"pg. {3 + i}",
                         fontsize=12, fontname="helv", color=(0.4, 0.2, 0.05))
        y += 24

    # Page 19: Chef's Notes
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 80), "Chef's Notes",
                     fontsize=24, fontname="hebo", color=(0.4, 0.2, 0.05))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(PAGE_W - 72, 95))
    shape.finish(color=(0.6, 0.3, 0.1), width=1.5)
    shape.commit()
    notes = (
        "Temperature is everything. A meat thermometer is your most valuable kitchen tool. "
        "Never guess on protein doneness — trust the probe.\n\n"
        "Season at every stage. Salt your pasta water aggressively. Season vegetables before "
        "roasting. Taste and adjust before plating.\n\n"
        "High heat = flavor. Whether searing a steak or charring a pizza, high heat creates the "
        "Maillard reaction that develops deep, complex flavors.\n\n"
        "Let it rest. Proteins need resting time after cooking to redistribute juices. "
        "Five minutes for a chicken breast, ten for a roast.\n\n"
        "Fresh > dried for aromatics. Fresh garlic, fresh herbs, and freshly ground spices "
        "make a noticeable difference. Invest in a good pepper grinder.\n\n"
        "Mise en place. Prepare and measure all ingredients before you begin cooking. "
        "This eliminates stress and prevents costly mistakes mid-recipe."
    )
    rect = pymupdf.Rect(72, 120, PAGE_W - 72, PAGE_H - 120)
    page.insert_textbox(rect, notes, fontsize=12, fontname="tiro",
                        color=(0.1, 0.1, 0.1))

    # Page 20: Back matter / colophon
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H))
    shape.finish(fill=(0.55, 0.27, 0.07))
    shape.commit()
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 160, PAGE_H / 2 - 30),
                     "The Home Chef's Recipe Collection",
                     fontsize=18, fontname="tibo", color=(1.0, 0.95, 0.85))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 80, PAGE_H / 2 + 10),
                     "First Edition, 2025",
                     fontsize=14, fontname="tiit", color=(1.0, 0.9, 0.75))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 100, PAGE_H / 2 + 40),
                     "Gourmet Kitchen Press",
                     fontsize=12, fontname="helv", color=(0.9, 0.85, 0.75))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 130, PAGE_H / 2 + 65),
                     "All rights reserved. Printed in the USA.",
                     fontsize=10, fontname="helv", color=(0.85, 0.80, 0.70))

    doc.save(OUTPUT)
    doc.close()

    # Verify
    doc_check = pymupdf.open(OUTPUT)
    page_count = doc_check.page_count
    # Count embedded images across all pages
    total_images = sum(len(doc_check[p].get_images()) for p in range(page_count))
    doc_check.close()

    print(f"Recipe book created: {OUTPUT}")
    print(f"  Pages: {page_count}")
    print(f"  Embedded food images: {total_images}")
    print(f"  Image pages: {image_page_indices}")

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_recipe_book()
