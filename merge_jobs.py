import json

# Load local and remote JSON files
with open('jobs_backup.json', 'r') as f:
    local = json.load(f)

with open('jobs.json', 'r') as f:
    remote = json.load(f)

# Merge jobs arrays
all_jobs = {job['id']: job for job in remote['jobs']}  # start with remote
for job in local['jobs']:
    all_jobs[job['id']] = job  # overwrite/add local jobs

# Create merged JSON
merged = {
    "meta": {
        "source": "JobHunter Cache",
        "generated_at": remote['meta'].get('generated_at', local['meta'].get('generated_at')),
        "expires_at": remote['meta'].get('expires_at', local['meta'].get('expires_at')),
        "ttl_hours": remote['meta'].get('ttl_hours', local['meta'].get('ttl_hours', 35))
    },
    "jobs": list(all_jobs.values())
}

# Save merged JSON
with open('jobs.json', 'w') as f:
    json.dump(merged, f, indent=2)

print("[INFO] jobs.json merged successfully")
