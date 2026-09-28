#!/usr/bin/env python3
"""Post today's queued announcements to X (formerly Twitter).

Reads org/social/queue/*.json and posts every item whose "date" equals today's
date in Japan time. Stateless by design: it runs once a day from GitHub
Actions (see .github/workflows/x-post.yml, decision D0010).

Credentials come only from environment variables (GitHub Actions secrets):
X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.

Usage:
  python3 scripts/x_post.py              # post today's items
  python3 scripts/x_post.py --dry-run    # print what would be posted
  python3 scripts/x_post.py --date 2026-10-05 --dry-run
"""
import argparse
import base64
import datetime
import glob
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

QUEUE_GLOB = "org/social/queue/*.json"
ENDPOINT = "https://api.x.com/2/tweets"
SITE_PREFIX = "https://hclab16k.github.io/health-affiliate-site/"
JST = datetime.timezone(datetime.timedelta(hours=9))
URL_RE = re.compile(r"https?://\S+")


def weighted_length(text):
    """Approximate X's weighted length: URLs count 23, CJK and other
    non-Latin characters count 2, everything else 1."""
    length = 0
    for m in URL_RE.finditer(text):
        length += 23
    rest = URL_RE.sub("", text)
    for ch in rest:
        cp = ord(ch)
        if cp <= 0x10FF or 0x2000 <= cp <= 0x200D or 0x2010 <= cp <= 0x201F or 0x2032 <= cp <= 0x2037:
            length += 1
        else:
            length += 2
    return length


def load_items(date):
    items = []
    for path in sorted(glob.glob(QUEUE_GLOB)):
        with open(path, encoding="utf-8") as f:
            item = json.load(f)
        problems = validate(item)
        if problems:
            raise SystemExit(f"{path}: " + "; ".join(problems))
        if item["date"] == date:
            items.append((path, item))
    return items


def validate(item):
    problems = []
    for key in ("date", "article", "text"):
        if not isinstance(item.get(key), str) or not item[key].strip():
            problems.append(f"missing {key}")
    if problems:
        return problems
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["date"]):
        problems.append("date must be YYYY-MM-DD")
    if SITE_PREFIX not in item["text"]:
        problems.append("text must contain the article URL")
    if weighted_length(item["text"]) > 280:
        problems.append(f"text too long ({weighted_length(item['text'])} > 280)")
    return problems


def pct(s):
    return urllib.parse.quote(s, safe="~")


def oauth_header(method, url, key, key_secret, token, token_secret):
    params = {
        "oauth_consumer_key": key,
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    # JSON body is not part of the signature base string.
    param_str = "&".join(f"{pct(k)}={pct(v)}" for k, v in sorted(params.items()))
    base = "&".join([method.upper(), pct(url), pct(param_str)])
    signing_key = f"{pct(key_secret)}&{pct(token_secret)}"
    digest = hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()
    params["oauth_signature"] = base64.b64encode(digest).decode()
    return "OAuth " + ", ".join(f'{pct(k)}="{pct(v)}"' for k, v in sorted(params.items()))


def post(text, creds):
    body = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", oauth_header("POST", ENDPOINT, *creds))
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", help="override date (YYYY-MM-DD, Japan time)")
    args = ap.parse_args()

    date = args.date or datetime.datetime.now(JST).date().isoformat()
    items = load_items(date)
    print(f"date={date} items={len(items)}")
    if not items:
        return 0

    names = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")
    creds = tuple(os.environ.get(n, "") for n in names)
    if args.dry_run or not all(creds):
        if not args.dry_run:
            print("credentials not set; skipping (dry run)")
        for path, item in items:
            print(f"--- {path} ({weighted_length(item['text'])}/280)\n{item['text']}")
        return 0

    failed = 0
    for path, item in items:
        status, text = post(item["text"], creds)
        print(f"{path}: HTTP {status}")
        if status == 201:
            continue
        if status == 403 and "duplicate" in text.lower():
            print("  already posted (duplicate); skipping")
            continue
        print(f"  error: {text[:500]}")
        failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
