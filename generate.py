#!/usr/bin/env python3
"""Build a PLDMNGR catalog from the official PS5SX2 GitHub release."""

import json
import os
import urllib.request
from datetime import datetime, timezone

OWNER = "Swordpdf"
REPO = "PS5SX2"
API = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
OUTPUT = "payloads.json"

def get_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "barelynotlegal-PS5SX2-PLDMNGR",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def describe(filename):
    lower = filename.lower()
    if "installer" in lower:
        return "PS5SX2 installer and updater payload. Use to install or update the PS5SX2 app."
    if "no-data-mount" in lower:
        return "PS5SX2 helper payload for ShadowMountPlus 1.7-beta5fix1 or newer (without the /data mount variant)."
    if "helper" in lower or "helper" in lower.replace(" ", ""):
        return "PS5SX2 helper payload. Check the official release notes for the matching ShadowMountPlus version."
    return "Official PS5SX2 payload."

def main():
    release = get_json(API)
    tag = release.get("tag_name") or "latest"
    published = release.get("published_at") or release.get("created_at")
    if published:
        last_update = datetime.fromisoformat(published.replace("Z", "+00:00")).date().isoformat()
    else:
        last_update = datetime.now(timezone.utc).date().isoformat()

    entries = []
    for asset in release.get("assets", []):
        filename = asset.get("name", "")
        if not filename.lower().endswith(".elf"):
            continue
        url = asset.get("browser_download_url")
        if not url:
            continue
        entries.append({
            "name": "PS5SX2 - " + filename.removesuffix(".elf"),
            "filename": filename,
            "url": url,
            "source": f"https://github.com/{OWNER}/{REPO}/releases",
            "source_direct": url,
            "description": describe(filename),
            "last_update": last_update,
            "version": tag,
            "category": "Emulators",
        })

    if not entries:
        raise RuntimeError("No .elf assets found in the latest PS5SX2 release; refusing to publish an empty catalog.")

    with open(OUTPUT, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2, ensure_ascii=False)
        file.write("\n")

    print(f"Generated {OUTPUT} with {len(entries)} PS5SX2 payload(s) from {tag}")

if __name__ == "__main__":
    main()
