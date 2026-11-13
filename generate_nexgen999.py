#!/usr/bin/env python3
"""Build a PLDMNGR-compatible catalog from nexgen999's upstream payload list."""
import json
import re
import urllib.request
from pathlib import PurePosixPath

UPSTREAM = "https://raw.githubusercontent.com/nexgen999/PS5_Payload_Manager_Updater/main/payloads.json"
SOURCE = "https://github.com/nexgen999/PS5_Payload_Manager_Updater"
OUTPUT = "payloads-nexgen999.json"

request = urllib.request.Request(UPSTREAM, headers={"User-Agent": "PLDMNGR-catalog-builder"})
with urllib.request.urlopen(request, timeout=30) as response:
    raw = response.read().decode("utf-8")

# Upstream currently omits commas after some version values before checksum.
raw = re.sub(r'("version"\s*:\s*"[^"]*")\s*\n(\s*"checksum")', r'\1,\n\2', raw)
upstream = json.loads(raw)

items = []
for item in upstream["payloads"]:
    url = item["url"]
    category = PurePosixPath(url.split("/main/", 1)[-1]).parent.name
    items.append({
        "name": item["name"],
        "filename": item["filename"],
        "url": url,
        "source": SOURCE,
        "source_direct": url,
        "description": item.get("description", ""),
        "version": item.get("version", ""),
        "category": category,
        "checksum": item.get("checksum", "")
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Wrote {len(items)} payloads to {OUTPUT}")
