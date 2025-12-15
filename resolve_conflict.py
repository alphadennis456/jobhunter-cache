import re
import json

file_path = "jobs.json"

# Read the conflicted JSON file
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove Git conflict markers
# Keep only the bottom (local) part after =======
pattern = r"<<<<<<< HEAD.*?=======\n(.*?)>>>>>>>.*"
resolved_content = re.sub(pattern, r"\1", content, flags=re.DOTALL).strip()

# Try to parse JSON to validate
try:
    data = json.loads(resolved_content)
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    exit(1)

# Write back the cleaned JSON
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"[INFO] Conflicts resolved and jobs.json updated successfully.")
