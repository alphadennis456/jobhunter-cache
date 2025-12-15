import json
import os
import subprocess
from datetime import datetime, timedelta

# === CONFIG ===
GITHUB_REPO_DIR = r"D:\official office\JobHunter\jobhunter-cache"  # local clone of GitHub repo
GITHUB_REMOTE = "origin"
JSON_FILENAME = "jobs.json"
TTL_HOURS = 35

# === MOCK JOB DATA ===
# Replace this with your real API scraper
jobs = [
    {
        "id": "gh-001",
        "title": "Python Script Developer",
        "company": "Remote",
        "match": 95,
        "location": "Worldwide",
        "type": "Remote",
        "description": "Develop automation scripts in Python. Experience with APIs and data scraping required.",
        "apply_url": "https://example.com/apply/python",
        "posted_at": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "id": "gh-002",
        "title": "Virtual Assistant",
        "company": "Upwork",
        "match": 90,
        "location": "Worldwide",
        "type": "Freelance",
        "description": "Administrative support, email handling, and basic research tasks.",
        "apply_url": "https://example.com/apply/va",
        "posted_at": datetime.now().strftime("%Y-%m-%d")
    }
]

# === METADATA ===
generated_at = datetime.utcnow()
expires_at = generated_at + timedelta(hours=TTL_HOURS)

data = {
    "meta": {
        "source": "JobHunter Cache",
        "generated_at": generated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": expires_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ttl_hours": TTL_HOURS
    },
    "jobs": jobs
}

# === WRITE JSON ===
json_path = os.path.join(GITHUB_REPO_DIR, JSON_FILENAME)
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
print(f"[INFO] {JSON_FILENAME} updated with {len(jobs)} jobs.")

# === GIT PUSH TO GITHUB ===
try:
    os.chdir(GITHUB_REPO_DIR)
    subprocess.run(["git", "add", JSON_FILENAME], check=True)
    subprocess.run(["git", "commit", "-m", f"Update jobs.json ({generated_at.strftime('%Y-%m-%d %H:%M:%S')})"], check=True)
    subprocess.run(["git", "push", GITHUB_REMOTE, "main"], check=True)  # adjust branch if needed
    print("[INFO] jobs.json pushed to GitHub Pages successfully.")
except subprocess.CalledProcessError as e:
    print("[ERROR] Git operation failed:", e)
