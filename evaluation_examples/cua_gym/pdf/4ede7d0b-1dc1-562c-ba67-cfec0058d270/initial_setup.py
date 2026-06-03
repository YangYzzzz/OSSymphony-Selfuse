"""
Initial Setup: Split newsletter PDF into sections based on bookmarks
Task ID: pdf_gf2_044
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_044'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/newsletter.pdf'
SECTIONS_DIR = f'{DOCS_DIR}/newsletter_sections'


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
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(SECTIONS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Section 1: Cover Story (pages 1-3) ---
    # Page 1 - Cover Story main page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "THE RIVERSIDE GAZETTE", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(72, 85), "Volume 47, Issue 12  |  March 2025", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 130), "COVER STORY", fontsize=22, fontname="hebo", color=(0.8, 0.1, 0.1))
    page.insert_textbox(
        pymupdf.Rect(72, 160, 540, 750),
        "Local Park Revitalization Project Breaks Ground\n\n"
        "After three years of planning and community fundraising, the Riverside "
        "Memorial Park renovation officially began on Tuesday with a groundbreaking "
        "ceremony attended by over 500 residents.\n\n"
        "Mayor Elena Vasquez presided over the ceremony, calling the $4.2 million "
        "project 'a testament to what our community can achieve when we work together.' "
        "The renovation includes a new amphitheater, upgraded playground facilities, "
        "a community garden spanning 2,500 square feet, and restored walking trails.\n\n"
        "'This park has been the heart of Riverside for over sixty years,' said "
        "Parks Director Marcus Thompson. 'The revitalization will ensure it remains "
        "a vibrant gathering place for generations to come.'\n\n"
        "The project was made possible through a combination of a $2.8 million city bond, "
        "$900,000 in state grants, and $500,000 raised through the community's "
        "'Green Future Fund' campaign launched in 2023.\n\n"
        "Phase 1, which covers the amphitheater and playground, is expected to be "
        "completed by September 2025. The full project timeline extends to March 2026.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 2 - Cover Story continued
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "COVER STORY (continued)", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 80, 540, 750),
        "Community Response Overwhelmingly Positive\n\n"
        "Residents who attended the groundbreaking shared their excitement about the "
        "renovations. 'My kids have been playing here since they were toddlers,' said "
        "Jennifer Park, a mother of three. 'Knowing that the playground will have modern, "
        "accessible equipment makes me so happy.'\n\n"
        "Local business owner David Chen, who operates Chen's Garden Supply on Oak Street, "
        "has pledged to donate plants and materials for the community garden. 'This park "
        "is good for everyone — families, businesses, the whole neighborhood,' he said.\n\n"
        "Sustainability at the Core\n\n"
        "Environmental consultant Dr. Sarah Whitfield, who advised on the project design, "
        "emphasized the sustainability features incorporated into the plan. Solar-powered "
        "lighting will reduce energy costs by an estimated 40%, while native plantings will "
        "decrease water usage by 60% compared to the current landscaping.\n\n"
        "A new rainwater collection system will irrigate the community garden, and recycled "
        "materials will be used for park benches and pathway surfaces. 'We wanted this to "
        "be a model for green urban spaces,' said Dr. Whitfield.\n\n"
        "The amphitheater will seat 350 people and host free summer concerts, theater "
        "performances, and community meetings throughout the year.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 3 - Cover Story photos/sidebar
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "COVER STORY — Project Timeline", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    timeline = [
        ("March 2025", "Groundbreaking ceremony, site preparation begins"),
        ("April–June 2025", "Foundation work for amphitheater and playground"),
        ("July–Sept 2025", "Phase 1 completion: amphitheater and playground open"),
        ("Oct–Dec 2025", "Community garden construction and trail restoration"),
        ("Jan–March 2026", "Final landscaping, lighting installation, grand opening"),
    ]
    y = 100
    for date, desc in timeline:
        page.insert_text(pymupdf.Point(90, y), date, fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
        page.insert_textbox(pymupdf.Rect(90, y + 5, 540, y + 40), desc, fontsize=10, fontname="tiro", color=(0, 0, 0))
        y += 55

    page.insert_textbox(
        pymupdf.Rect(72, 420, 540, 750),
        "Budget Breakdown\n\n"
        "Amphitheater Construction: $1,200,000\n"
        "Playground Equipment & Installation: $850,000\n"
        "Community Garden Infrastructure: $400,000\n"
        "Trail Restoration & Landscaping: $650,000\n"
        "Solar Lighting & Utilities: $550,000\n"
        "Project Management & Contingency: $550,000\n"
        "Total Project Cost: $4,200,000\n\n"
        "For more information about the revitalization project, visit "
        "www.riversideparks.gov/renewal or attend the next public forum on April 3rd.",
        fontsize=11, fontname="tiro", color=(0, 0, 0),
    )

    # --- Section 2: Tech Review (pages 4-6) ---
    # Page 4
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "TECH REVIEW", fontsize=22, fontname="hebo", color=(0, 0.4, 0.2))
    page.insert_textbox(
        pymupdf.Rect(72, 90, 540, 750),
        "Smart Home Hub Roundup: Which System Deserves Your Investment?\n\n"
        "By Alex Rivera, Technology Correspondent\n\n"
        "The smart home market has exploded in 2025, with three major platforms vying "
        "for dominance. We tested the latest offerings from AppleHome Pro, Google Nest "
        "Hub Max 3, and Amazon Echo Universe over a six-week period in typical household "
        "settings.\n\n"
        "AppleHome Pro ($349)\n\n"
        "Apple's flagship hub excels in privacy and ecosystem integration. Setup took "
        "just 12 minutes, and the device seamlessly connected with all 23 HomeKit "
        "accessories in our test home. Voice recognition accuracy reached 97.3%, the "
        "highest among all three platforms.\n\n"
        "The 8-inch Liquid Retina display is gorgeous, and the new spatial audio with "
        "Dolby Atmos support makes it a capable bedside speaker. However, cross-platform "
        "compatibility remains limited — only 340 third-party brands are supported "
        "versus over 800 for competitors.\n\n"
        "Rating: 8.5/10",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 5
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "TECH REVIEW (continued)", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 80, 540, 750),
        "Google Nest Hub Max 3 ($279)\n\n"
        "Google's offering brings its AI prowess front and center. The built-in Gemini "
        "assistant handles complex, multi-step commands with impressive accuracy. Ask it "
        "to 'dim the living room lights, start relaxing music, and set the thermostat to "
        "68 degrees' and it executes all three without hesitation.\n\n"
        "The 10-inch display doubles as a capable tablet for recipes, video calls, and "
        "YouTube streaming. Integration with 850+ smart home brands makes it the most "
        "versatile option. Battery life in portable mode lasts approximately 4.5 hours.\n\n"
        "Rating: 9.0/10\n\n"
        "Amazon Echo Universe ($229)\n\n"
        "Amazon's budget-friendly option punches above its weight. Alexa has matured "
        "significantly, with improved natural language understanding and the new 'Routines "
        "Plus' feature that learns your daily patterns and automates accordingly.\n\n"
        "The device includes a built-in Zigbee and Thread hub, eliminating the need for "
        "separate bridges for most smart accessories. The 7-inch display is adequate, "
        "though noticeably lower resolution than competitors.\n\n"
        "Rating: 8.0/10\n\n"
        "Our Pick: Google Nest Hub Max 3 offers the best balance of AI intelligence, "
        "display quality, and third-party compatibility.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 6
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "TECH REVIEW — Comparison Chart", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    # Draw comparison table
    headers = ["Feature", "AppleHome Pro", "Nest Hub Max 3", "Echo Universe"]
    rows = [
        ["Price", "$349", "$279", "$229"],
        ["Display", '8" Retina', '10" HD', '7" Standard'],
        ["Voice Accuracy", "97.3%", "95.1%", "93.8%"],
        ["Brands Supported", "340+", "850+", "780+"],
        ["Setup Time", "12 min", "15 min", "10 min"],
        ["Privacy Score", "A+", "B+", "B"],
        ["Overall Rating", "8.5/10", "9.0/10", "8.0/10"],
    ]
    y_start = 90
    col_widths = [130, 120, 130, 120]
    x_positions = [72]
    for w in col_widths[:-1]:
        x_positions.append(x_positions[-1] + w)
    for ci, hdr in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[ci] + 5, y_start + 15), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(72, y_start, 572, y_start + 22))
    shape.finish(fill=(0.1, 0.2, 0.5), color=(0, 0, 0), width=0.5)
    shape.commit()
    # Re-draw header text on top
    for ci, hdr in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[ci] + 5, y_start + 15), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))
    y = y_start + 22
    for ri, row in enumerate(rows):
        fill_color = (0.95, 0.95, 0.95) if ri % 2 == 0 else (1, 1, 1)
        shape2 = page.new_shape()
        shape2.draw_rect(pymupdf.Rect(72, y, 572, y + 20))
        shape2.finish(fill=fill_color, color=(0.8, 0.8, 0.8), width=0.3)
        shape2.commit()
        for ci, val in enumerate(row):
            page.insert_text(pymupdf.Point(x_positions[ci] + 5, y + 14), val, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 20

    page.insert_textbox(
        pymupdf.Rect(72, y + 40, 540, 750),
        "Quick Tips for Smart Home Setup\n\n"
        "1. Start with a strong Wi-Fi mesh network — most issues stem from connectivity.\n"
        "2. Choose one ecosystem and stick with it for the best experience.\n"
        "3. Update firmware on all devices regularly for security patches.\n"
        "4. Use guest networks to isolate IoT devices from personal computers.\n"
        "5. Consider Thread/Matter-compatible devices for future-proofing.\n\n"
        "Next month: We review the latest robot vacuum cleaners from Roborock, iRobot, "
        "and Ecovacs.",
        fontsize=11, fontname="tiro", color=(0, 0, 0),
    )

    # --- Section 3: Community News (pages 7-9) ---
    # Page 7
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "COMMUNITY NEWS", fontsize=22, fontname="hebo", color=(0.6, 0.3, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 90, 540, 750),
        "Riverside High School Robotics Team Advances to Nationals\n\n"
        "The Riverside High School 'Circuit Breakers' robotics team earned a spot at "
        "the National FIRST Robotics Championship after a dominant performance at the "
        "Pacific Northwest Regional competition last weekend.\n\n"
        "Led by team captain Priya Sharma and mentor Coach Robert Lin, the 18-member "
        "team designed a robot capable of autonomously sorting and stacking colored blocks "
        "with 98% accuracy — the highest score at regionals.\n\n"
        "'These students have been working after school and weekends since September,' "
        "said Principal Diane Foster. 'Their dedication and creativity represent the "
        "best of what our school community has to offer.'\n\n"
        "The nationals will be held in Houston, Texas from April 17-20. The team is "
        "seeking sponsors to help cover $15,000 in travel and competition costs. "
        "Donations can be made at www.riversiderobotics.org.\n\n"
        "Local Farmer's Market Expands to Year-Round Schedule\n\n"
        "Beginning April 1st, the Riverside Farmer's Market will operate every Saturday "
        "from 8 AM to 1 PM throughout the year, expanding from its previous April-October "
        "seasonal schedule.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 8
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "COMMUNITY NEWS (continued)", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 80, 540, 750),
        "Market manager Lisa Yamamoto says the expansion is possible thanks to the new "
        "covered pavilion completed last fall. 'Rain or shine, our vendors will be here "
        "with fresh, locally-grown produce and artisan goods,' she said.\n\n"
        "The market currently hosts 45 vendors, including 12 certified organic farms, "
        "8 bakeries, and various artisan food producers. A new winter vendor application "
        "period opens March 15th.\n\n"
        "Library Announces Summer Reading Program\n\n"
        "The Riverside Public Library has unveiled its 2025 Summer Reading Program, "
        "'Explore the Unknown,' running June 1 through August 15. Open to all ages, "
        "the program features:\n\n"
        "- Children (ages 5-12): Read 20 books to earn a new backpack and book voucher\n"
        "- Teens (ages 13-17): Complete reading challenges for prize drawings\n"
        "- Adults: Join monthly book clubs and author meet-and-greets\n\n"
        "Head Librarian Thomas Garcia expects over 2,000 participants this year. "
        "'Reading is the foundation of lifelong learning,' he said. 'Our goal is to "
        "make every resident excited about picking up a book this summer.'\n\n"
        "Registration opens May 1st at all three library branches or online at "
        "www.riversidelibrary.org/summer.",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 9
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "COMMUNITY NEWS — Upcoming Events", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    events = [
        ("March 22", "Spring Cleanup Day — Meet at City Hall, 9 AM. Bags and gloves provided."),
        ("March 28", "Riverside Symphony Concert — 'Beethoven & Beyond' at Lincoln Center, 7 PM."),
        ("April 3", "Park Revitalization Public Forum — Community Center, 6:30 PM."),
        ("April 5", "Annual Easter Egg Hunt — Riverside Memorial Park, 10 AM. Ages 2-10."),
        ("April 12", "Earth Day Festival — Downtown plaza, 11 AM-4 PM. Live music, workshops."),
        ("April 17-20", "Robotics Nationals Watch Party — Riverside High cafeteria, schedule TBD."),
        ("May 1", "Summer Reading Program Registration Opens — All library branches."),
        ("May 10", "Mother's Day Brunch Fundraiser — Elks Lodge, 10 AM-1 PM. $25/person."),
    ]
    y = 90
    for date, desc in events:
        page.insert_text(pymupdf.Point(80, y), date, fontsize=11, fontname="hebo", color=(0.6, 0.3, 0))
        page.insert_textbox(pymupdf.Rect(170, y - 12, 540, y + 25), desc, fontsize=10, fontname="tiro", color=(0, 0, 0))
        y += 45

    page.insert_textbox(
        pymupdf.Rect(72, y + 20, 540, 750),
        "Community Spotlight: Volunteer of the Month\n\n"
        "Congratulations to Margaret 'Peggy' O'Brien, named March Volunteer of the Month "
        "for her 15 years of service at the Riverside Food Bank. Peggy coordinates weekly "
        "food distributions serving 200+ families and has organized three successful "
        "holiday food drives.\n\n"
        "'Peggy's tireless dedication has made an immeasurable impact on families facing "
        "food insecurity in our community,' said Food Bank Director James Wright. "
        "'She embodies the spirit of Riverside.'",
        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Section 4: Classifieds (pages 10-12) ---
    # Page 10
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "CLASSIFIEDS", fontsize=22, fontname="hebo", color=(0.4, 0, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 90, 540, 750),
        "EMPLOYMENT\n\n"
        "RIVERSIDE GENERAL HOSPITAL — Seeking RNs for ER and ICU departments. "
        "Full-time, competitive salary, full benefits. BSN required. Apply at "
        "riversidegeneral.org/careers. EOE.\n\n"
        "CHEN'S GARDEN SUPPLY — Part-time sales associate needed. Garden knowledge "
        "preferred. $18/hour + employee discount. Contact David at 555-0142.\n\n"
        "RIVERSIDE SCHOOL DISTRICT — Hiring substitute teachers for all grade levels. "
        "Bachelor's degree required. $175/day. Apply at rsd.edu/employment.\n\n"
        "SUNSET CAFE — Experienced barista wanted. Morning shifts, 5:30 AM-12 PM. "
        "$16/hour + tips. Apply in person at 428 Main Street.\n\n"
        "REAL ESTATE\n\n"
        "FOR SALE — 3BR/2BA ranch on Elm Street. Updated kitchen, hardwood floors, "
        "fenced yard. $425,000. Open house Sat 1-4 PM. Call RE/MAX: 555-0198.\n\n"
        "FOR RENT — 2BR apartment downtown. W/D in unit, parking included. $1,650/mo. "
        "No pets. Available April 1. Contact: apartments@riversidemgmt.com.\n\n"
        "FOR SALE — Commercial lot on Highway 9, 0.75 acres, zoned C-2. Ideal for "
        "retail or office. $280,000. Broker: 555-0234.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
    )

    # Page 11
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "CLASSIFIEDS (continued)", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 80, 540, 750),
        "SERVICES\n\n"
        "PETERSON PLUMBING — Licensed, bonded, insured. Residential & commercial. "
        "24/7 emergency service. Free estimates. Call 555-0167.\n\n"
        "MARIA'S CLEANING SERVICE — Residential and office cleaning. Weekly, bi-weekly, "
        "or one-time deep clean. References available. 555-0289.\n\n"
        "RIVERSIDE TREE CARE — Pruning, removal, stump grinding. ISA certified arborist "
        "on staff. Free consultation. 555-0312.\n\n"
        "TAX PREPARATION — CPA with 20 years experience. Individual and small business "
        "returns. Competitive rates. Johnson & Associates: 555-0178.\n\n"
        "FOR SALE — ITEMS\n\n"
        "MOVING SALE — Sectional sofa (beige, excellent condition) $400. Dining table "
        "with 6 chairs $350. Washer/dryer set $500. King bed frame $200. Call 555-0456.\n\n"
        "BABY ITEMS — Crib, changing table, stroller, car seat. All gently used. "
        "$300 for the lot. Text 555-0523.\n\n"
        "2019 HONDA CIVIC EX — 42,000 miles, one owner, regular maintenance records. "
        "Silver, sunroof, heated seats. $19,500 OBO. 555-0634.\n\n"
        "PIANO — Yamaha upright, excellent condition, recently tuned. Includes bench. "
        "$1,800. Must pick up. 555-0789.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
    )

    # Page 12
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "CLASSIFIEDS (continued)", fontsize=14, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_textbox(
        pymupdf.Rect(72, 80, 540, 450),
        "PETS\n\n"
        "FREE TO GOOD HOME — 2-year-old tabby cat, neutered, vaccinated, indoor only. "
        "Very affectionate. Owner relocating overseas. 555-0891.\n\n"
        "DOG WALKING — Reliable, experienced dog walker. $20/30-min walk, $30/hour walk. "
        "Serving downtown and Oak Hill areas. Sarah: 555-0445.\n\n"
        "LOST — Golden Retriever, male, answers to 'Buddy'. Last seen near Riverside "
        "Park on March 10. Wearing blue collar. REWARD. 555-0667.\n\n"
        "WANTED\n\n"
        "LOOKING FOR — Reliable used pickup truck, 2015 or newer, under $20,000. "
        "Call Mike at 555-0533.\n\n"
        "SEEKING — Experienced piano teacher for 8-year-old beginner. Willing to travel "
        "to your studio or our home. 555-0712.\n\n"
        "ROOMMATE WANTED — Professional seeking quiet roommate for 2BR house near "
        "downtown. $800/mo including utilities. Available May 1. 555-0488.",
        fontsize=10, fontname="tiro", color=(0, 0, 0),
    )

    # Footer on page 12
    page.insert_text(pymupdf.Point(72, 700), "To place a classified ad, contact:", fontsize=10, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 715), "classifieds@riversidegazette.com  |  555-0100  |  $15/week (up to 30 words)", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(200, 750), "THE RIVERSIDE GAZETTE  |  Page 12", fontsize=8, fontname="helv", color=(0.6, 0.6, 0.6))

    # --- Set Table of Contents (Bookmarks) ---
    toc = [
        [1, "Cover Story", 1],
        [1, "Tech Review", 4],
        [1, "Community News", 7],
        [1, "Classifieds", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    print(f'Page count: {verify_doc.page_count}')
    print(f'TOC: {verify_doc.get_toc()}')
    verify_doc.close()

    # Verify sections dir is empty
    print(f'Sections dir contents: {os.listdir(SECTIONS_DIR)}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
