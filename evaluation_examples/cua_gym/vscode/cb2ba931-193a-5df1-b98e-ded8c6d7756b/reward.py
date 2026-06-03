"""
Reward Script: Next.js Blog with TypeScript, Tailwind, API Routes, and VSCode Config
Task ID: vscode_gf4_024
Domain: vscode
Scoring:
  Component 1: package.json with required dependencies (0.2)
  Component 2: app/blog/page.tsx fetching from /api/posts (0.2)
  Component 3: app/api/posts/route.ts returning 5+ post objects (0.2)
  Component 4: components/PostCard.tsx with TS interface and Tailwind (0.2)
  Component 5: .vscode/settings.json with Tailwind CSS config (0.2)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'nextjs-blog')
TASK_ID = 'vscode_gf4_024'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json with next, react, react-dom, tailwindcss (0.2 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        # Collect all dependencies (both deps and devDeps)
        all_deps = {}
        all_deps.update(pkg.get('dependencies', {}))
        all_deps.update(pkg.get('devDependencies', {}))

        required = ['next', 'react', 'react-dom', 'tailwindcss']
        found = [dep for dep in required if dep in all_deps]

        if len(found) == len(required):
            print(f"PASS: Component 1 — package.json has all required deps: {found} (0.2 pts)")
            total_score += 0.2
        else:
            missing = [dep for dep in required if dep not in all_deps]
            print(f"FAIL: Component 1 — package.json missing deps: {missing}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — package.json not found at {pkg_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: app/blog/page.tsx exists and fetches from /api/posts (0.2 points)
    try:
        blog_page_path = os.path.join(PROJECT_DIR, 'app', 'blog', 'page.tsx')
        with open(blog_page_path, 'r') as f:
            blog_content = f.read()

        # Must be a React component (has export default function/const) and fetch from /api/posts
        has_export = bool(re.search(r'export\s+default', blog_content))
        has_api_fetch = bool(re.search(r'/api/posts', blog_content))

        if has_export and has_api_fetch:
            print(f"PASS: Component 2 — app/blog/page.tsx exports default component and fetches /api/posts (0.2 pts)")
            total_score += 0.2
        else:
            reasons = []
            if not has_export:
                reasons.append("no default export")
            if not has_api_fetch:
                reasons.append("no /api/posts fetch reference")
            print(f"FAIL: Component 2 — app/blog/page.tsx issues: {', '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — app/blog/page.tsx not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: app/api/posts/route.ts returns JSON array of 5+ post objects (0.2 points)
    try:
        route_path = os.path.join(PROJECT_DIR, 'app', 'api', 'posts', 'route.ts')
        with open(route_path, 'r') as f:
            route_content = f.read()

        # Must export a GET handler
        has_get_export = bool(re.search(r'export\s+(async\s+)?function\s+GET', route_content))

        # Must have at least 5 post objects with id, title, excerpt, date fields
        # Count distinct id values to verify 5+ posts
        id_matches = re.findall(r'id\s*:\s*(\d+)', route_content)
        has_5_posts = len(set(id_matches)) >= 5

        # Check for required fields in post objects
        has_title_field = bool(re.search(r'title\s*:', route_content))
        has_excerpt_field = bool(re.search(r'excerpt\s*:', route_content))
        has_date_field = bool(re.search(r'date\s*:', route_content))
        has_required_fields = has_title_field and has_excerpt_field and has_date_field

        if has_get_export and has_5_posts and has_required_fields:
            print(f"PASS: Component 3 — route.ts has GET export, {len(set(id_matches))} posts with required fields (0.2 pts)")
            total_score += 0.2
        else:
            reasons = []
            if not has_get_export:
                reasons.append("no GET export")
            if not has_5_posts:
                reasons.append(f"only {len(set(id_matches))} unique post ids (need 5+)")
            if not has_required_fields:
                reasons.append("missing title/excerpt/date fields")
            print(f"FAIL: Component 3 — route.ts issues: {', '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — app/api/posts/route.ts not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: components/PostCard.tsx with TypeScript interface and Tailwind classes (0.2 points)
    try:
        postcard_path = os.path.join(PROJECT_DIR, 'components', 'PostCard.tsx')
        with open(postcard_path, 'r') as f:
            postcard_content = f.read()

        # Must have a TypeScript interface or type definition for props
        has_ts_interface = bool(re.search(r'(interface\s+\w+|type\s+\w+\s*=)', postcard_content))

        # Must have Tailwind CSS class names (className with typical tailwind patterns)
        has_tailwind = bool(re.search(r'className\s*=\s*["\'].*?(text-|bg-|p-|m-|flex|grid|rounded|border|shadow|font-)', postcard_content))

        # Must display title, excerpt, and date (referenced in JSX)
        has_title = bool(re.search(r'\btitle\b', postcard_content))
        has_excerpt = bool(re.search(r'\bexcerpt\b', postcard_content))
        has_date = bool(re.search(r'\bdate\b', postcard_content))
        has_props = has_title and has_excerpt and has_date

        if has_ts_interface and has_tailwind and has_props:
            print(f"PASS: Component 4 — PostCard.tsx has TS interface, Tailwind classes, and displays title/excerpt/date (0.2 pts)")
            total_score += 0.2
        else:
            reasons = []
            if not has_ts_interface:
                reasons.append("no TypeScript interface/type")
            if not has_tailwind:
                reasons.append("no Tailwind CSS classes")
            if not has_props:
                reasons.append("missing title/excerpt/date props usage")
            print(f"FAIL: Component 4 — PostCard.tsx issues: {', '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — components/PostCard.tsx not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/settings.json with Tailwind CSS IntelliSense config (0.2 points)
    try:
        vscode_settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        with open(vscode_settings_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        settings = json.loads(cleaned)

        # Check for any tailwindCSS-related settings
        tailwind_keys = [k for k in settings.keys() if 'tailwind' in k.lower()]
        # Also check files.associations for tailwindcss
        files_assoc = settings.get('files.associations', {})
        has_tailwind_assoc = any('tailwind' in str(v).lower() for v in files_assoc.values())

        if len(tailwind_keys) > 0 or has_tailwind_assoc:
            print(f"PASS: Component 5 — .vscode/settings.json has Tailwind config keys: {tailwind_keys} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — .vscode/settings.json has no Tailwind CSS settings")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point artifacts
    final_score = round(final_score, 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
