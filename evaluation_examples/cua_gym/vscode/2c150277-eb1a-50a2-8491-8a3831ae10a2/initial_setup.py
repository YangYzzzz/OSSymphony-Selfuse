"""
Initial Setup: Merge conflict resolution across three files in a git repo
Task ID: vscode_git_064
Domain: vs_code

Creates /home/user/project as a git repo with:
- main branch: added ProductManager class in models.py, updated index() return value in views.py,
  added product-related URL patterns in urls.py
- feature/refactor branch: refactored model names in models.py, added new parameter to index() in views.py,
  added feature-related URL patterns in urls.py
- git merge feature/refactor started but not completed (conflict markers present)
- Agent must resolve all three files and complete the merge commit
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_064'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=env
    )
    if check and result.returncode != 0:
        print(f"ERROR running: {cmd}")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout.strip()


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
    # Clean up any existing project dir
    if os.path.exists(PROJECT_DIR):
        run(f'rm -rf "{PROJECT_DIR}"')

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Set up git config
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd):
        return run(f'git {cmd}', cwd=PROJECT_DIR, env=git_env)

    # Initialize git repo with main as default branch
    git('init -b main')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev User"')

    # ---- Create base files (common ancestor) ----

    models_base = '''\
# models.py - Data models for the application

class User:
    """Represents an application user."""
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(username={self.username!r})"


class Post:
    """Represents a blog post."""
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return f"Post(title={self.title!r})"


class Comment:
    """Represents a comment on a post."""
    def __init__(self, text, author):
        self.text = text
        self.author = author

    def __repr__(self):
        return f"Comment(text={self.text!r})"
'''

    views_base = '''\
# views.py - View functions for the application

from models import User, Post, Comment


def index(request):
    """Homepage view."""
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


def user_profile(request, username):
    """User profile view."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template("profile.html", user=user, posts=posts)


def post_detail(request, post_id):
    """Post detail view."""
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).all()
    return render_template("post.html", post=post, comments=comments)
'''

    urls_base = '''\
# urls.py - URL routing configuration

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>/", views.user_profile, name="user-profile"),
    path("post/<int:post_id>/", views.post_detail, name="post-detail"),
]
'''

    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write(models_base)
    with open(os.path.join(PROJECT_DIR, 'views.py'), 'w') as f:
        f.write(views_base)
    with open(os.path.join(PROJECT_DIR, 'urls.py'), 'w') as f:
        f.write(urls_base)

    git('add .')
    git('commit -m "Initial commit: base models, views, and urls"')

    # ---- Create feature/refactor branch from base ----
    git('checkout -b feature/refactor')

    # feature/refactor: refactor model names (rename classes, add docstrings)
    models_feature = '''\
# models.py - Data models for the application

class AppUser:
    """Represents an application user account."""
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_display_name(self):
        return self.username.capitalize()

    def __repr__(self):
        return f"AppUser(username={self.username!r})"


class BlogPost:
    """Represents a blog post entry."""
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def get_summary(self, length=100):
        return self.content[:length] + "..." if len(self.content) > length else self.content

    def __repr__(self):
        return f"BlogPost(title={self.title!r})"


class UserComment:
    """Represents a user comment on a post."""
    def __init__(self, text, author):
        self.text = text
        self.author = author

    def __repr__(self):
        return f"UserComment(text={self.text!r})"
'''

    # feature/refactor: add new parameter to index()
    views_feature = '''\
# views.py - View functions for the application

from models import AppUser, BlogPost, UserComment


def index(request, page=1):
    """Homepage view with pagination support."""
    posts = BlogPost.query.paginate(page=page, per_page=10)
    return render_template("index.html", posts=posts)


def user_profile(request, username):
    """User profile view."""
    user = AppUser.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user).all()
    return render_template("profile.html", user=user, posts=posts)


def post_detail(request, post_id):
    """Post detail view."""
    post = BlogPost.query.get_or_404(post_id)
    comments = UserComment.query.filter_by(post=post).all()
    return render_template("post.html", post=post, comments=comments)
'''

    # feature/refactor: add feature-specific URL patterns
    urls_feature = '''\
# urls.py - URL routing configuration

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("page/<int:page>/", views.index, name="index-paged"),
    path("post/<int:post_id>/", views.post_detail, name="post-detail"),
    path("profile/<str:username>/", views.user_profile, name="user-profile"),
]
'''

    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write(models_feature)
    with open(os.path.join(PROJECT_DIR, 'views.py'), 'w') as f:
        f.write(views_feature)
    with open(os.path.join(PROJECT_DIR, 'urls.py'), 'w') as f:
        f.write(urls_feature)

    git('add .')
    git('commit -m "refactor: rename model classes and add pagination to index view"')

    # ---- Go back to main and add main-branch changes ----
    git('checkout main')

    # main: add a new ProductManager class at end of models.py
    models_main = '''\
# models.py - Data models for the application

class User:
    """Represents an application user."""
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(username={self.username!r})"


class Post:
    """Represents a blog post."""
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return f"Post(title={self.title!r})"


class Comment:
    """Represents a comment on a post."""
    def __init__(self, text, author):
        self.text = text
        self.author = author

    def __repr__(self):
        return f"Comment(text={self.text!r})"


class ProductManager:
    """Manages product catalog entries."""
    def __init__(self, name, price, stock=0):
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self):
        return self.stock > 0

    def __repr__(self):
        return f"ProductManager(name={self.name!r}, price={self.price})"
'''

    # main: update index() return value to include featured_posts
    views_main = '''\
# views.py - View functions for the application

from models import User, Post, Comment


def index(request):
    """Homepage view."""
    posts = Post.query.all()
    featured_posts = Post.query.filter_by(featured=True).limit(3).all()
    return render_template("index.html", posts=posts, featured_posts=featured_posts)


def user_profile(request, username):
    """User profile view."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template("profile.html", user=user, posts=posts)


def post_detail(request, post_id):
    """Post detail view."""
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).all()
    return render_template("post.html", post=post, comments=comments)
'''

    # main: add product-related URL patterns
    urls_main = '''\
# urls.py - URL routing configuration

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>/", views.post_detail, name="post-detail"),
    path("products/", views.product_list, name="product-list"),
    path("products/<int:product_id>/", views.product_detail, name="product-detail"),
    path("profile/<str:username>/", views.user_profile, name="user-profile"),
]
'''

    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write(models_main)
    with open(os.path.join(PROJECT_DIR, 'views.py'), 'w') as f:
        f.write(views_main)
    with open(os.path.join(PROJECT_DIR, 'urls.py'), 'w') as f:
        f.write(urls_main)

    git('add .')
    git('commit -m "feat: add ProductManager model and featured posts in index view"')

    # ---- Start the merge (it will fail with conflicts) ----
    merge_result = subprocess.run(
        'git merge feature/refactor',
        shell=True, cwd=PROJECT_DIR, capture_output=True, text=True, env=git_env
    )
    # Merge should exit with non-zero due to conflicts — that's expected
    print(f"Merge result (conflicts expected): {merge_result.returncode}")
    print(f"  stdout: {merge_result.stdout}")
    print(f"  stderr: {merge_result.stderr}")

    # Verify conflict markers exist
    for fname in ['models.py', 'views.py', 'urls.py']:
        fpath = os.path.join(PROJECT_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        if '<<<<<<<' in content:
            print(f"  {fname}: conflict markers present (OK)")
        else:
            print(f"  WARNING: {fname} has no conflict markers!")

    print(f'\nInitial project created at: {PROJECT_DIR}')
    print('Git status:')
    git_status = run('git status', cwd=PROJECT_DIR, env=git_env)
    print(git_status)

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder using DISPLAY=:0')


create_initial()
