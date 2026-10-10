#!/usr/bin/env python3
"""Rebuild activities.json from every GitHub repo whose name starts with the prefix
in settings.json (default "vu23560") and has GitHub Pages turned on.

Run by .github/workflows/update-activities.yml every hour.
It only writes activities.json when the list of activities has changed.
"""
import json
import os
import re
import sys
import urllib.request
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SETTINGS = os.path.join(ROOT, "settings.json")
OUT = os.path.join(ROOT, "activities.json")

owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "teacherfrances")
home_repo = os.environ.get("GITHUB_REPOSITORY", owner + "/vu23560").split("/")[-1]
token = os.environ.get("GITHUB_TOKEN", "")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


settings = load(SETTINGS, {})
prefix = (settings.get("prefix") or "vu23560").lower()
hidden = {h.lower() for h in settings.get("hide", [])}
old = load(OUT, {"items": []})
old_titles = {i["repo"]: i.get("title", "") for i in old.get("items", [])}


def get(url, api=True):
    req = urllib.request.Request(url, headers={"User-Agent": "vu23560-homepage"})
    if api:
        req.add_header("Accept", "application/vnd.github+json")
        if token:
            req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def list_repos():
    repos, page = [], 1
    while True:
        data = json.loads(get("https://api.github.com/users/%s/repos?per_page=100&page=%d" % (owner, page)))
        repos += data
        if len(data) < 100:
            return repos
        page += 1


def kind(name):
    n = name.lower()
    for key, words in [
        ("deck", ["deck", "slides"]),
        ("jeopardy", ["jeopardy", "board"]),
        ("escape", ["escape"]),
        ("seek", ["seek", "findit", "hunt"]),
        ("phone", ["phone"]),
        ("email", ["email", "inbox"]),
        ("quiz", ["quiz"]),
        ("speak", ["record", "sayit", "pronun", "speak"]),
        ("revision", ["revision", "revise", "review"]),
    ]:
        if any(w in n for w in words):
            return key
    return "other"


def lesson(name):
    m = re.search(r"lesson[_\- ]?(\d+)", name, re.I)
    return int(m.group(1)) if m else 0


def page_title(url, repo):
    try:
        html = get(url, api=False)
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        if m and m.group(1).strip():
            return unescape(re.sub(r"\s+", " ", m.group(1)).strip())
    except Exception as e:
        print("  could not read title for", repo, e)
    return old_titles.get(repo) or repo


def main():
    items = []
    for r in list_repos():
        name = r["name"]
        if not name.lower().startswith(prefix) or name.lower() == home_repo.lower():
            continue
        if name.lower() in hidden:
            continue
        if not r.get("has_pages") or r.get("private") or r.get("archived"):
            continue
        url = "https://%s.github.io/%s/" % (owner.lower(), name)
        items.append({
            "repo": name,
            "url": url,
            "lesson": lesson(name),
            "type": kind(name),
            "title": page_title(url, name),
            "created": r["created_at"][:10],
        })
        print("found", name)
    order = ["deck", "revision", "jeopardy", "escape", "seek", "phone", "email", "quiz", "speak", "other"]
    items.sort(key=lambda i: (i["lesson"] or 999, order.index(i["type"]), i["repo"].lower()))
    if items == old.get("items"):
        print("No change.")
        return
    from datetime import date
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"updated": date.today().isoformat(), "items": items}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Wrote", len(items), "activities.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Update failed:", e)
        sys.exit(1)
