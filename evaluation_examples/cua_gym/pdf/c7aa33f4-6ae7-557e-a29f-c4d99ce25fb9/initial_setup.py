"""
Initial Setup: Create article content and images for newspaper layout generator task.
Task ID: pdf_gf3_031
Domain: pdf

Sets up:
- /home/user/content/articles.json with 8 article entries
- /home/user/content/images/ with headline images
- /home/user/scripts/ directory (empty - agent creates the script)
- /home/user/output/ directory (empty - script generates PDF here)
- Opens a text editor with a stub file to orient the agent
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_031'

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


def create_headline_images():
    """Create simple headline images for the articles."""
    from PIL import Image, ImageDraw, ImageFont

    img_dir = f'{WORKDIR}/content/images'
    os.makedirs(img_dir, exist_ok=True)

    image_specs = [
        ('city_council.jpg', (640, 400), '#2E5090', 'City Council Meeting'),
        ('tech_summit.jpg', (640, 400), '#1A7A4C', 'Tech Summit 2026'),
        ('farmers_market.jpg', (640, 400), '#8B4513', 'Local Farmers Market'),
        ('school_expansion.jpg', (640, 400), '#4A0E4E', 'School Expansion'),
        ('marathon.jpg', (640, 400), '#C41E3A', 'Annual Marathon'),
        ('art_gallery.jpg', (640, 400), '#1F4E79', 'Art Gallery Opening'),
        ('solar_farm.jpg', (640, 400), '#2E7D32', 'Solar Farm Project'),
        ('food_festival.jpg', (640, 400), '#E65100', 'Food Festival'),
    ]

    for filename, size, bg_color, label in image_specs:
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)

        # Draw some visual elements to make images look like photos
        w, h = size
        # Gradient overlay
        for y in range(h):
            alpha = int(80 * (y / h))
            draw.line([(0, y), (w, y)], fill=(alpha, alpha, alpha))

        # Add label text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((w - tw) // 2, (h - th) // 2), label, fill='white', font=font)

        # Add decorative borders
        draw.rectangle([5, 5, w - 6, h - 6], outline='white', width=2)

        filepath = os.path.join(img_dir, filename)
        img.save(filepath, quality=85)
        print(f'Created image: {filepath}')


def create_articles_json():
    """Create the articles.json with 8 realistic article entries."""
    content_dir = f'{WORKDIR}/content'
    os.makedirs(content_dir, exist_ok=True)

    articles = [
        {
            "title": "City Council Approves Downtown Revitalization Plan",
            "author": "Sarah Mitchell",
            "body_text": (
                "The Riverside City Council voted unanimously on Tuesday to approve a $45 million "
                "downtown revitalization plan that will transform the historic waterfront district over "
                "the next three years. The ambitious project includes the construction of a new public "
                "plaza, restoration of six heritage buildings dating back to the 1890s, and the creation "
                "of a pedestrian-friendly promenade along the riverbank. Mayor Elena Rodriguez called "
                "the decision 'a turning point for our city's future.' The plan also allocates $8 million "
                "for affordable housing units above commercial spaces, addressing long-standing concerns "
                "about displacement of long-term residents. Local business owners expressed cautious "
                "optimism, with Chamber of Commerce president David Park noting that 'the key will be "
                "maintaining the character of our downtown while welcoming new investment.' Construction "
                "is expected to begin in September, with the first phase focusing on infrastructure "
                "improvements and the public plaza. Environmental assessments have already been completed, "
                "and the project has received preliminary approval from the state historic preservation office."
            ),
            "image_path": "/home/user/content/images/city_council.jpg"
        },
        {
            "title": "Regional Tech Summit Draws Record Attendance",
            "author": "James Chen",
            "body_text": (
                "More than 3,200 technology professionals gathered at the Riverside Convention Center "
                "this week for the 12th annual Pacific Northwest Tech Summit, breaking last year's "
                "attendance record by nearly 400 participants. Keynote speaker Dr. Amara Okafor, chief "
                "scientist at NeuralPath Labs, presented groundbreaking research on adaptive AI systems "
                "that can learn from minimal training data. 'We're entering an era where artificial "
                "intelligence will become truly collaborative,' Dr. Okafor told the audience. The three-day "
                "event featured 85 presentations across eight tracks, including sessions on quantum "
                "computing applications, sustainable technology infrastructure, and the evolving landscape "
                "of cybersecurity. Several local startups showcased their innovations in a dedicated "
                "exhibition hall, with particular interest in GreenGrid Solutions' energy management "
                "platform and DataWeave's privacy-focused analytics toolkit. Industry analysts noted "
                "that the summit's growth reflects the region's emergence as a significant technology hub."
            ),
            "image_path": "/home/user/content/images/tech_summit.jpg"
        },
        {
            "title": "Saturday Farmers Market Celebrates 25th Anniversary",
            "author": "Maria Gonzalez",
            "body_text": (
                "The beloved Riverside Saturday Farmers Market marked its 25th anniversary last weekend "
                "with a special celebration that drew thousands of visitors to Heritage Square. Founded in "
                "2001 by a small group of local farmers, the market has grown from just twelve vendors to "
                "over seventy-five, offering everything from organic produce and artisan cheeses to handmade "
                "soaps and fresh-cut flowers. Market director Patricia Hawkins reflected on the journey: "
                "'What started as a modest gathering has become the heart of our community's weekend ritual.' "
                "The anniversary festivities included live music from the Riverside Community Orchestra, "
                "cooking demonstrations by Chef Thomas Brennan of Harvest Table restaurant, and a special "
                "tribute to the market's founding vendors. Local farms reported strong sales, with several "
                "varieties of heirloom tomatoes and stone fruits selling out before noon. The market operates "
                "year-round, with winter hours from 9 AM to 1 PM and summer hours extending to 3 PM."
            ),
            "image_path": "/home/user/content/images/farmers_market.jpg"
        },
        {
            "title": "School Board Announces $30M Expansion Program",
            "author": "Robert Washington",
            "body_text": (
                "The Riverside Unified School District has unveiled a comprehensive $30 million expansion "
                "program to address rapidly growing enrollment across the district. Superintendent Dr. Linda "
                "Nakamura presented the plan at Monday's school board meeting, outlining construction of a new "
                "elementary school in the Eastgate neighborhood, additions to three existing middle schools, "
                "and a state-of-the-art STEM laboratory wing at Riverside High School. 'Our student population "
                "has increased by 18 percent over the past five years, and we must invest in facilities that "
                "match the quality of our educational programs,' Dr. Nakamura stated. The expansion will be "
                "funded through a combination of state grants, a municipal bond measure approved by voters "
                "last November, and federal infrastructure funds. The new elementary school is projected to "
                "accommodate 600 students and will feature solar panels, a community garden, and a maker space. "
                "Groundbreaking ceremonies are planned for early next year."
            ),
            "image_path": "/home/user/content/images/school_expansion.jpg"
        },
        {
            "title": "Annual River Run Marathon Attracts Elite Runners",
            "author": "Karen O'Brien",
            "body_text": (
                "International distance running stars descended on Riverside this Sunday for the 18th Annual "
                "River Run Marathon, with Kenyan runner Joseph Kipchoge claiming first place with an impressive "
                "time of 2:08:34. Ethiopian athlete Tigist Assefa won the women's division in 2:22:17, setting "
                "a new course record. The race, which follows a scenic route along the river valley and through "
                "downtown, attracted 4,800 registered participants from 23 countries. Race director Michael "
                "Torres was thrilled with the turnout: 'The River Run has established itself as a premier "
                "marathon destination, and this year's field was the strongest we've ever had.' Community "
                "participation was equally impressive, with the accompanying 10K fun run drawing 2,300 runners "
                "and walkers of all ages. Local sponsors contributed over $150,000 in prizes and charitable "
                "donations, with proceeds benefiting the Riverside Youth Athletics Foundation."
            ),
            "image_path": "/home/user/content/images/marathon.jpg"
        },
        {
            "title": "New Contemporary Art Gallery Opens on Main Street",
            "author": "Diana Patel",
            "body_text": (
                "The Meridian Gallery, a bold new contemporary art space, opened its doors on Main Street last "
                "Friday with an inaugural exhibition featuring works by twelve regional artists. Gallery founder "
                "and curator Alexandra Voss has transformed a former warehouse into a striking 4,000 square-foot "
                "exhibition space with soaring ceilings and natural light. The opening show, titled 'Convergence,' "
                "explores themes of community and transformation through painting, sculpture, photography, and "
                "mixed media installations. 'Riverside deserves a gallery that champions emerging voices and "
                "challenges conventional boundaries,' Voss explained. The centerpiece of the exhibition is a "
                "large-scale installation by sculptor Marcus Webb, whose suspended metalwork piece spans the "
                "entire main gallery. The gallery plans to host six exhibitions per year, along with artist talks, "
                "workshops, and a residency program for artists from underrepresented communities."
            ),
            "image_path": "/home/user/content/images/art_gallery.jpg"
        },
        {
            "title": "County Breaks Ground on Solar Energy Farm",
            "author": "Thomas Lee",
            "body_text": (
                "Riverside County officially broke ground on Wednesday on a 200-acre solar energy farm that "
                "officials say will generate enough clean electricity to power approximately 12,000 homes. "
                "Located on former agricultural land east of the city, the $65 million Sunfield Solar project "
                "represents the largest renewable energy investment in the county's history. County Executive "
                "Barbara Chen called it 'a decisive step toward our goal of achieving 100 percent renewable "
                "energy by 2035.' The facility will feature 180,000 photovoltaic panels and an integrated "
                "battery storage system capable of storing 50 megawatt-hours of energy. Construction is "
                "expected to create 350 temporary jobs and 25 permanent positions. The project has been "
                "developed in partnership with GreenVolt Energy and will sell power to the county utility at "
                "rates projected to be 30 percent below current wholesale electricity prices. Environmental "
                "groups have praised the initiative while calling for additional investments in wind energy."
            ),
            "image_path": "/home/user/content/images/solar_farm.jpg"
        },
        {
            "title": "International Food Festival Returns to Riverside Park",
            "author": "Yuki Tanaka",
            "body_text": (
                "The aroma of spices, grilled meats, and freshly baked breads filled the air as the Riverside "
                "International Food Festival returned to Central Park for its 10th edition last weekend. The "
                "two-day celebration of global cuisine featured 48 food vendors representing culinary traditions "
                "from more than 30 countries, alongside live cultural performances and cooking competitions. "
                "Festival organizer Priya Sharma estimated attendance at over 15,000 across both days. 'Food is "
                "the universal language of community,' Sharma said. 'This festival shows how beautifully diverse "
                "our city has become.' Highlights included a Thai street food stall that generated a 45-minute "
                "wait, a live paella cooking demonstration by Spanish chef Carlos Ruiz, and a children's area "
                "where young visitors could try making dumplings and tortillas. The festival's Best Dish award "
                "went to Mama Rosa's Kitchen for their lamb tagine with preserved lemons and olives, while the "
                "People's Choice award was claimed by Seoul Brothers BBQ for their bulgogi tacos."
            ),
            "image_path": "/home/user/content/images/food_festival.jpg"
        }
    ]

    output_path = os.path.join(content_dir, 'articles.json')
    with open(output_path, 'w') as f:
        json.dump(articles, f, indent=2)
    print(f'Created articles.json: {output_path}')


def create_directory_structure():
    """Create the required directory structure."""
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)
    os.makedirs(f'{WORKDIR}/output', exist_ok=True)
    os.makedirs(f'{WORKDIR}/content/images', exist_ok=True)
    print('Directory structure created: scripts/, output/, content/images/')


def create_initial():
    # Create directories
    create_directory_structure()

    # Create article content
    create_articles_json()

    # Create headline images
    create_headline_images()

    # GUI-ready: open the articles.json in a text editor and a file manager
    # so the agent can see the content structure
    launch_gui(f'xdg-open "{WORKDIR}/content/articles.json"', delay_sec=2.0)
    launch_gui(f'nautilus "{WORKDIR}/content"', delay_sec=1.5)
    print('GUI_READY: launched text editor and file manager with DISPLAY=:0')


create_initial()
