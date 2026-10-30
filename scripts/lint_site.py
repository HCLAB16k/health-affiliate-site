"""Site quality checks run on every PR (D0024 A1).

Catches the mechanical problems reviewers kept finding by hand: a missed build,
citation markers left in key points or body, broken in-page anchors, missing
disclaimer / PR badge, X queue problems. Usage: python3 scripts/lint_site.py
"""
import json
import re
import subprocess
import sys

sys.path.insert(0, "scripts")
from x_post import AD_DOMAINS  # noqa: E402

errors, warnings = [], []


def tracked_articles():
    out = subprocess.run(["git", "ls-files", "articles/*.html"], capture_output=True, text=True).stdout
    return [p for p in out.split() if p]


def check_build_is_current():
    """build_site.py is deterministic, so any file it changes means someone skipped the build."""
    files = subprocess.run(["git", "ls-files", "*.html", "sitemap.xml"], capture_output=True, text=True).stdout.split()
    before = {f: open(f, encoding="utf-8").read() for f in files}
    subprocess.run([sys.executable, "scripts/build_site.py"], check=True, capture_output=True)
    changed = [f for f in files if open(f, encoding="utf-8").read() != before[f]]
    if changed:
        errors.append("build_site.py was not run (these files change when it is): " + ", ".join(changed))


def check_site_data(articles):
    data = json.load(open("scripts/site_data.json", encoding="utf-8"))
    slugs = {a["slug"] for a in data["articles"]}
    for p in articles:
        slug = p.split("/")[-1][:-5]
        if slug not in slugs:
            errors.append(f"{p}: no entry in scripts/site_data.json")


def check_article(p):
    s = open(p, encoding="utf-8").read()
    body = s[s.find("<article>"): s.find("</article>")]
    m = re.search(r'<h2 id="summary-top">.*?(?=<h2)', body, re.S)
    if m:
        if 'class="cite"' in m.group(0) or re.search(r"［\d", m.group(0)):
            errors.append(f"{p}: source numbers inside 先に要点 (D0022)")
        if re.search(r"（→[^）]*。[^）]*）", m.group(0)):
            errors.append(f"{p}: 「。」 inside a →( ) in 先に要点 (style guide)")
    if re.search(r"［\d", body):
        errors.append(f"{p}: bracket citation ［n］ in body; use <sup class=\"cite\"> (D0022)")
    ids = set(re.findall(r'id="([^"]+)"', s))
    for a in set(re.findall(r'href="#([^"]+)"', body)):
        if a not in ids:
            errors.append(f"{p}: link to #{a} but no element has that id")
    n_disc = len(re.findall(r'class="disclaimer"', s))
    if n_disc != 1:
        errors.append(f"{p}: {n_disc} disclaimer blocks (expected 1)")
    has_ads = any(d in href for href in re.findall(r'href="([^"]+)"', body) for d in AD_DOMAINS)
    if has_ads and "pr-badge" not in s:
        errors.append(f"{p}: affiliate links without pr-badge (CLAUDE.md 5)")
    if has_ads and 'rel="nofollow' not in body and "sponsored" not in body:
        errors.append(f"{p}: affiliate links without rel=sponsored/nofollow (CLAUDE.md 7)")


def check_readability(articles):
    for p in articles:
        out = subprocess.run([sys.executable, "scripts/readability.py", p], capture_output=True, text=True).stdout
        m = re.search(r"60字超 (\d+)%", out)
        if m and int(m.group(1)) > 15:
            warnings.append(f"{p}: {m.group(1)}% of sentences over 60 chars (style guide: under 10%)")


def check_x_queue():
    r = subprocess.run([sys.executable, "scripts/x_post.py", "--check"], capture_output=True, text=True)
    if r.returncode:
        errors.append("X queue: " + (r.stdout + r.stderr).strip().splitlines()[-1])


def main():
    articles = tracked_articles()
    check_site_data(articles)
    for p in articles:
        check_article(p)
    check_readability(articles)
    check_x_queue()
    check_build_is_current()
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(articles)} articles, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
