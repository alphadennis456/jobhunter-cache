import json
import os
from datetime import datetime, timedelta
import subprocess

# --- Config ---
CACHE_FILE = "jobs.json"
NEW_JOBS_FILE = "new_jobs.json"  # temporary file with new jobs fetched
GIT_REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Load existing jobs ---
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            jobs_data = json.load(f)
        except json.JSONDecodeError:
            print("[WARN] jobs.json corrupted. Starting fresh.")
            jobs_data = {"meta": {}, "jobs": []}
else:
    jobs_data = {"meta": {}, "jobs": []}

existing_ids = {job["id"] for job in jobs_data.get("jobs", [])}

# --- Load new jobs ---
if os.path.exists(NEW_JOBS_FILE):
    with open(NEW_JOBS_FILE, "r", encoding="utf-8") as f:
        new_data = json.load(f)
else:
    print(f"[INFO] {NEW_JOBS_FILE} not found. Nothing to update.")
    exit(0)

# --- Merge new jobs ---
added_count = 0
for job in new_data.get("jobs", []):
    if job["id"] not in existing_ids:
        jobs_data["jobs"].append(job)
        added_count += 1

# --- Update metadata ---
now = datetime.utcnow()
jobs_data["meta"] = {
    "source": "JobHunter Cache",
    "generated_at": now.isoformat() + "Z",
    "expires_at": (now + timedelta(hours=35)).isoformat() + "Z",
    "ttl_hours": 35
}

# --- Save updated cache ---
with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(jobs_data, f, indent=4)

print(f"[INFO] jobs.json updated with {added_count} new jobs.")

# --- Git commit & push ---
try:
    subprocess.run(["git", "add", CACHE_FILE], cwd=GIT_REPO_DIR, check=True)
    commit_msg = f"Auto-update jobs.json ({now.strftime('%Y-%m-%d %H:%M:%S')})"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=GIT_REPO_DIR, check=True)
    subprocess.run(["git", "pull", "--rebase"], cwd=GIT_REPO_DIR, check=True)
    subprocess.run(["git", "push"], cwd=GIT_REPO_DIR, check=True)
    print("[INFO] GitHub push complete.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Git operation failed: {e}")
