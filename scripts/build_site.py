#!/usr/bin/env python3
"""Rebuild the site's navigation from scripts/site_data.json.

Generates / updates:
  - category/<id>.html        one page per category, listing its articles
  - index.html                the "Categories" panel and the "latest articles" cards
  - every page                the small category bar under the header (<nav class="cat-nav">)
  - sitemap.xml               adds category pages

Run after adding an article or changing a category:
  python3 scripts/build_site.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://hclab16k.github.io/health-affiliate-site/"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


data = json.loads(read("scripts/site_data.json"))
cats = data["categories"]
arts = sorted(data["articles"], key=lambda a: a.get("updated") or a["date"], reverse=True)
by_cat = {c["id"]: [a for a in arts if a["category"] == c["id"]] for c in cats}


def fmt_date(d):
    return d.replace("-", ".")


def cat_nav(prefix, current=None):
    links = "".join(
        f'<a href="{prefix}category/{c["id"]}.html"' + (' aria-current="page"' if c["id"] == current else "") + f'>{c["name"]}</a>'
        for c in cats)
    return f'<nav class="cat-nav" aria-label="カテゴリ"><div class="inner">{links}</div></nav>'


def card(a, prefix):
    return (
        f'        <a class="card" href="{prefix}articles/{a["slug"]}.html">\n'
        f'          <div class="thumb"><img src="{prefix}images/thumbs/{a["slug"]}.svg" alt="" width="400" height="300" loading="lazy"><span class="tag">{a["tag"]}</span></div>\n'
        f'          <span class="date">公開 {fmt_date(a["date"])}' + (f' / 更新 {fmt_date(a["updated"])}' if a.get("updated") else '') + '</span>\n'
        f'          <h3>{a["title"]}</h3>\n'
        f'          <p>{a["desc"]}</p>\n'
        f'          <span class="more">+ 記事を読む</span>\n'
        f'        </a>\n'
    )


# ---------- index.html ----------
index = read("index.html")
panel = (
    '      <div class="panel">\n'
    '        <h2 id="topics-title"><span>Categories</span></h2>\n'
    '        <ul>\n'
    + "".join(
        f'          <li><a href="category/{c["id"]}.html">{c["name"]}<span class="count">{len(by_cat[c["id"]])}</span></a></li>\n'
        for c in cats
    )
    + '        </ul>\n'
    '      </div>\n'
)
index, n = re.subn(r'      <div class="panel">\n.*?      </div>\n(?=    </div>\n  </section>)', panel, index, count=1, flags=re.S)
assert n == 1, "panel not found"
latest = (
    '  <section class="articles">\n'
    '    <div class="wrap">\n'
    '      <h2 class="section-title"><span>最新記事</span></h2>\n'
    '      <div class="category-grid">\n'
    + "".join(card(a, "") for a in arts[: data["latest_count"]])
    + '      </div>\n'
    '      <p class="all-cats">カテゴリから探す：'
    + " / ".join(f'<a href="category/{c["id"]}.html">{c["name"]}</a>' for c in cats)
    + '</p>\n'
    '    </div>\n'
    '  </section>\n'
)
index, n = re.subn(r'  <section class="articles">\n.*?  </section>\n', latest, index, count=1, flags=re.S)
assert n == 1, "articles section not found"
write("index.html", index)

# ---------- category pages ----------
head_src = read("about.html")
head = head_src[: head_src.index("<body>")]
head = re.sub(r'(href|src)="(?!https?:|//|#)([^"]+)"', r'\1="../\2"', head)
header = head_src[head_src.index("<header"): head_src.index("</header>") + len("</header>")]
header = re.sub(r'href="(?!https?:|//|#)([^"]+)"', r'href="../\1"', header)
footer = head_src[head_src.index("<footer"): head_src.index("</footer>") + len("</footer>")]
footer = re.sub(r'href="(?!https?:|//|#)([^"]+)"', r'href="../\1"', footer)

for c in cats:
    h = re.sub(r"<title>.*?</title>", f"<title>{c['name']}の記事一覧 | 男の養生帖</title>", head)
    h = h.replace('<meta name="viewport"', f'<meta name="description" content="{c["lead"]}">\n<meta name="viewport"', 1)
    items = "".join(card(a, "../") for a in by_cat[c["id"]])
    page = (
        h + "<body>\n\n" + header + "\n\n"
        '<main class="category-page">\n'
        '  <div class="wrap">\n'
        f'    <span class="eyebrow">{c["label"]}</span>\n'
        f'    <h1>{c["name"]}</h1>\n'
        f'    <p class="lead">{c["lead"]}</p>\n'
        '    <div class="category-grid">\n'
        + items +
        '    </div>\n'
        '  </div>\n'
        '</main>\n\n' + footer + "\n\n</body>\n</html>\n"
    )
    write(f"category/{c['id']}.html", page)

# ---------- SEO head block (canonical, Open Graph, Twitter card, JSON-LD) ----------
import html as _html
import json as _json

STATIC_DESC = {
    "about.html": "「男の養生帖」の運営者情報。記事の作り方（一次情報の確認、AIの利用、監修なし）、広告の扱い、お問い合わせ先。",
    "disclosure.html": "「男の養生帖」の広告表記・掲載基準・免責事項。アフィリエイト広告の利用、記事内の表示、掲載の基準。",
    "privacy.html": "「男の養生帖」のプライバシーポリシー。個人情報、アクセス解析（Google アナリティクス）、Web フォント、アフィリエイトプログラムの扱い。",
}
ART = {a["slug"]: a for a in data["articles"]}
CATN = {c["id"]: c["name"] for c in cats}
PUBLISHER = {"@type": "Organization", "name": "男の養生帖", "logo": {"@type": "ImageObject", "url": SITE + "icon-512.png"}}


def page_url(f):
    return SITE if f == "index.html" else SITE + f


def seo_block(f, s):
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    m = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    desc = m.group(1) if m else _html.escape(STATIC_DESC[f], quote=True)
    url = page_url(f)
    is_article = f.startswith("articles/")
    lines = ["<!-- seo:start -->"]
    if not m:
        lines.append(f'<meta name="description" content="{desc}">')
    lines += [
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:site_name" content="男の養生帖">',
        '<meta property="og:locale" content="ja_JP">',
        f'<meta property="og:type" content="{"article" if is_article else "website"}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{SITE}images/og.png">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    ld = None
    if is_article:
        a = ART[f[len("articles/"):-len(".html")]]
        ld = [{
            "@context": "https://schema.org", "@type": "Article", "headline": _html.unescape(title),
            "description": _html.unescape(desc), "inLanguage": "ja", "mainEntityOfPage": url,
            "datePublished": a["date"], "dateModified": a.get("updated") or a["date"],
            "author": {"@type": "Organization", "name": "男の養生帖 編集部"}, "publisher": PUBLISHER,
            "image": SITE + "images/og.png",
        }, {
            "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "男の養生帖", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": CATN[a["category"]], "item": f"{SITE}category/{a['category']}.html"},
                {"@type": "ListItem", "position": 3, "name": _html.unescape(title), "item": url},
            ]}]
    elif f == "index.html":
        ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "男の養生帖", "url": SITE, "inLanguage": "ja"}]
    if ld:
        for obj in ld:
            lines.append('<script type="application/ld+json">' + _json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>")
    lines.append("<!-- seo:end -->")
    return "\n".join(lines)


# ---------- category bar on every page ----------
files = subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT).decode().split()
files = sorted(set(files) | {f"category/{c['id']}.html" for c in cats})
for f in files:
    if f.startswith("google"):
        continue
    s = read(f)
    prefix = "../" if "/" in f else ""
    current = f[len("category/"):-len(".html")] if f.startswith("category/") else None
    nav = cat_nav(prefix, current)
    s = re.sub(r'\n?<nav class="cat-nav".*?</nav>', "", s, flags=re.S)
    s = s.replace("</header>", "</header>\n" + nav, 1)
    s = re.sub(r"\n?<!-- seo:start -->.*?<!-- seo:end -->", "", s, flags=re.S)
    s = s.replace("</head>", seo_block(f, s) + "\n</head>", 1)
    write(f, s)

# ---------- sitemap ----------
urls = [(SITE, None), (SITE + "about.html", None), (SITE + "disclosure.html", None), (SITE + "privacy.html", None)]
urls += [(f"{SITE}category/{c['id']}.html", max([a.get("updated") or a["date"] for a in by_cat[c["id"]]] or [None])) for c in cats]
urls += [(f"{SITE}articles/{a['slug']}.html", a.get("updated") or a["date"]) for a in sorted(data["articles"], key=lambda a: a["date"])]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc, lm in urls:
    sm += f"  <url><loc>{loc}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>\n"
sm += "</urlset>\n"
write("sitemap.xml", sm)
print("categories:", {c["id"]: len(by_cat[c["id"]]) for c in cats}, "latest:", [a["slug"] for a in arts[: data["latest_count"]]])
