import json
import os
from datetime import datetime, timedelta
import subprocess

# Files
CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_FILE = os.path.join(CACHE_DIR, "jobs.json")
NEW_JOBS_FILE = os.path.join(CACHE_DIR, "new_jobs.json")

# Config
TTL_HOURS = 35

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] {file_path} updated with {len(data.get('jobs', []))} jobs.")

def merge_jobs(existing, new):
    if existing is None:
        return new
    existing_ids = {job["id"] for job in existing.get("jobs", [])}
    added = 0
    for job in new.get("jobs", []):
        if job["id"] not in existing_ids:
            existing["jobs"].append(job)
            added += 1
    return existing, added

def update_meta(data):
    now = datetime.utcnow()
    data["meta"] = {
        "source": "JobHunter Cache",
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": (now + timedelta(hours=TTL_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ttl_hours": TTL_HOURS
    }

def git_commit_push():
    try:
        subprocess.run(["git", "add", "jobs.json"], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Auto-update jobs.json ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"],
            check=True
        )
        subprocess.run(["git", "pull", "--rebase"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[INFO] GitHub push complete.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git operation failed: {e}")

def main():
    new_jobs = load_json(NEW_JOBS_FILE)
    if not new_jobs:
        print("[INFO] No new jobs found. Exiting.")
        return

    existing_jobs = load_json(JOBS_FILE)
    merged, added_count = merge_jobs(existing_jobs, new_jobs)
    update_meta(merged)

    save_json(JOBS_FILE, merged)
    print(f"[INFO] {added_count} new jobs merged.")
    git_commit_push()

if __name__ == "__main__":
    main()
