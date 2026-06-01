 
import os
import json
import shutil
import uuid
import filecmp
import datetime
import requests


WIT_DIR = "../.wit"
STAGING_DIR = os.path.join(WIT_DIR, "staging")
COMMITS_DIR = os.path.join(WIT_DIR, "commits")
METADATA_FILE = os.path.join(WIT_DIR, "metadata.json")


# ---------- פונקציות עזר ----------

def load_ignore():
    ignore_list = [WIT_DIR]
    if os.path.exists("../.witignore"):
        with open("../.witignore", "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    ignore_list.append(stripped)
    return ignore_list


def is_ignored(path, ignore_list):
    norm_path = os.path.normpath(path)
    for ignore in ignore_list:
        norm_ignore = os.path.normpath(ignore)
        if norm_path == norm_ignore or norm_path.startswith(norm_ignore + os.sep):
            return True
    return False


def are_directories_different(path1, path2):
    if not os.path.exists(path1) or not os.path.exists(path2):
        return True

    comparison = filecmp.dircmp(path1, path2)
    if comparison.diff_files or comparison.left_only or comparison.right_only:
        return True

    for subdir in comparison.common_dirs:
        if are_directories_different(
            os.path.join(path1, subdir),
            os.path.join(path2, subdir)
        ):
            return True

    return False


def has_uncommitted_changes(head_path):
    for root, _, files in os.walk(head_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), head_path)
            work_path = os.path.join("..", rel_path)

            if not os.path.exists(work_path):
                return True

            if not filecmp.cmp(
                os.path.join(head_path, rel_path),
                work_path,
                shallow=False
            ):
                return True
    return False


# ---------- לוגיקה מרכזית ----------

def init_repo():
    if os.path.exists(WIT_DIR):
        return "Repository already initialized"

    os.makedirs(STAGING_DIR, exist_ok=True)
    os.makedirs(COMMITS_DIR, exist_ok=True)

    with open(METADATA_FILE, "w") as f:
        json.dump({"head": None}, f)

    if not os.path.exists("../.witignore"):
        with open("../.witignore", "w") as f:
            f.write(f"{WIT_DIR}/\n.witignore\n")

    return "Initialized empty wit repository"


def add(path):
    if not os.path.exists(path):
        return "Path does not exist"

    ignore_list = load_ignore()

    def add_single_file(src_path):
        if is_ignored(src_path, ignore_list):
            return
        dest_path = os.path.join(STAGING_DIR, src_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                add_single_file(os.path.join(root, file))
    else:
        add_single_file(path)

    return f"Added {path} to staging area"


def commit(message):
    if not os.listdir(STAGING_DIR):
        return "Nothing to commit (staging is empty)"

    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    head_id = metadata.get("head")
    head_path = os.path.join(COMMITS_DIR, head_id) if head_id else None

    if head_path and not are_directories_different(STAGING_DIR, head_path):
        return "No changes detected since last commit. Commit aborted."

    commit_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    shutil.copytree(STAGING_DIR, commit_path)
    metadata["head"] = commit_id
    metadata[commit_id] = {"message": message, "timestamp": timestamp}
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    return f"Commit {commit_id} created at {timestamp}: {message}"


def status():
    ignore_list = load_ignore()

    staged_files = []
    for root, _, files in os.walk(STAGING_DIR):
        for file in files:
            staged_files.append(
                os.path.relpath(os.path.join(root, file), STAGING_DIR)
            )

    untracked_files = []
    for root, _, files in os.walk(".."):
        if is_ignored(root, ignore_list):
            continue
        for file in files:
            full_path = os.path.join(root, file)
            if not is_ignored(full_path, ignore_list):
                rel = os.path.relpath(full_path, "..")
                if rel not in staged_files:
                    untracked_files.append(rel)

    return staged_files, untracked_files


def checkout(commit_id):
    ignore_list = load_ignore()
    commit_path = os.path.join(COMMITS_DIR, commit_id)

    if not os.path.exists(commit_path):
        return "Unknown commit id"

    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    head_id = metadata.get("head")
    if head_id:
        head_path = os.path.join(COMMITS_DIR, head_id)
        if has_uncommitted_changes(head_path):
            return "Uncommitted changes exist. Checkout blocked."

    for item in os.listdir(".."):
        if item == WIT_DIR or is_ignored(item, ignore_list):
            continue
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

    for item in os.listdir(commit_path):
        src = os.path.join(commit_path, item)
        if os.path.isdir(src):
            shutil.copytree(src, item)
        else:
            shutil.copy2(src, item)

    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    shutil.copytree(commit_path, STAGING_DIR)

    metadata["head"] = commit_id
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    return f"Checked out commit {commit_id}"




def push():
    """
    פקודת push: מוצאת את קבצי הפייתון בקומיט האחרון, שולחת אותם לניתוח בשרת,
    מציגה אזהרות בטרמינל ושומרת את הגרפים הויזואליים כקבצי תמונה.
    """
    # 1. קריאת ה-metadata כדי למצוא את ה-Commit ID האחרון (HEAD)
    if not os.path.exists(METADATA_FILE):
        return "Error: Repository not initialized. Run 'init' first."

    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    head_id = metadata.get("head")
    if not head_id:
        return "Error: Nothing to push. Please commit your changes first."

    # 2. הגדרת נתיב תיקיית הקומיט האחרון
    last_commit_path = os.path.join(COMMITS_DIR, head_id)
    if not os.path.exists(last_commit_path):
        return f"Error: Commit folder for {head_id} not found."

    print(f"Pushing code from last commit ({head_id[:8]}) to CodeGuard CI Server...")

    # 3. סריקה ומציאת כל קבצי הפייתון בקומיט
    py_files_found = []
    for root, _, files in os.walk(last_commit_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, last_commit_path)
                py_files_found.append((full_path, rel_path))

    if not py_files_found:
        return "No Python files found in the last commit to analyze."

    # כתובות השרת המקומי שלנו
    ALERTS_URL = "http://127.0.0.1:8000/alerts"
    ANALYZE_URL = "http://127.0.0.1:8000/analyze"

    # 4. מעבר על כל קובץ ושליחתו לשרת
    for full_path, rel_path in py_files_found:
        print(f"\nAnalyzing file: {rel_path} ...")

        try:
            # א) שליחה לנתיב /alerts לקבלת אזהרות טקסטואליות
            with open(full_path, "rb") as f:
                files_payload = {"file": (rel_path, f, "text/plain")}
                alerts_response = requests.post(ALERTS_URL, files=files_payload)

            if alerts_response.status_code == 200:
                data = alerts_response.json()
                alerts = data.get("alerts", [])
                if alerts:
                    print(f"⚠️  [Alerts for {rel_path}]:")
                    for alert in alerts:
                        print(f"   - {alert}")
                else:
                    print(f"✅ No issues found in {rel_path}!")
            else:
                print(f"❌ Server error on /alerts (Status code: {alerts_response.status_code})")

            # ב) שליחה לנתיב /analyze לקבלת קובץ הגרפים המשולב
            with open(full_path, "rb") as f:
                files_payload = {"file": (rel_path, f, "text/plain")}
                analyze_response = requests.post(ANALYZE_URL, files=files_payload)

            if analyze_response.status_code == 200:
                # יצירת שם לקובץ התמונה שיישמר (למשל: graph_core.py.png)
                output_image_name = f"graph_{rel_path.replace(os.sep, '_')}.png"
                # שמירת זרם הביטים של התמונה מהשרת לקובץ מקומי בדיסק
                with open(output_image_name, "wb") as img_file:
                    img_file.write(analyze_response.content)
                print(f"📊 Visual report saved successfully as '{output_image_name}'")
            else:
                print(f"❌ Server error on /analyze (Status code: {analyze_response.status_code})")

        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to the CodeGuard server. Is it running on http://127.0.0.1:8000 ?"

    return "\n🚀 Push and Code Analysis completed successfully!"
