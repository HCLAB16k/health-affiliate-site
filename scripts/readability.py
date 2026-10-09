#!/usr/bin/env python3
"""Rough readability numbers for an article (org/style-guide.md 1章).

  python3 scripts/readability.py [--long] articles/foo.html [...]   (--long lists sentences over 60 chars)

Counts body text inside <article> (skips the reference list, tables and the
build-generated parts) and prints: median sentence length, share of sentences
over 60 characters, average paragraph length, lead length, [n] per 1000 chars.
"""
import re
import statistics
import sys


def text(h):
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", h))


def measure(path, show_long=False):
    s = open(path, encoding="utf-8").read()
    body = s[s.find("<article>"): s.find("</article>")]
    body = re.sub(r"<!-- (crumbs|byline|toc|samecat):start -->.*?<!-- \1:end -->", "", body, flags=re.S)
    body = re.sub(r"<table.*?</table>", "", body, flags=re.S)
    body = re.sub(r"<blockquote.*?</blockquote>", "", body, flags=re.S)  # quoted originals are not ours to shorten
    body = re.sub(r'<ol class="refs".*?</ol>|<h2[^>]*>参考資料.*$', "", body, flags=re.S)
    paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S)]
    paras = [p for p in paras if p and not p.startswith("PR/")]
    items = [text(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", body, flags=re.S)]
    sents = [x for t in paras + items for x in re.split(r"(?<=[。！？])", t) if len(x) > 1]  # list items counted on their own
    lens = [len(x) for x in sents]
    allt = "".join(paras + items)
    lead = paras[0] if paras else ""
    print(f"{path}: 文の中央値 {statistics.median(lens):.0f}字 / 60字超 {sum(l > 60 for l in lens) / len(lens):.0%}"
          f" / 段落平均 {statistics.mean(len(p) for p in paras):.0f}字 / リード {len(lead)}字"
          f" / ［n］ {len(re.findall('［', allt)) * 1000 / max(len(allt), 1):.1f}個/1000字")
    if show_long:
        for x in sorted(sents, key=len, reverse=True):
            if len(x) > 60:
                print(f"  {len(x)}字: {x}")


args = [a for a in sys.argv[1:] if a != "--long"]
for p in args:
    measure(p, "--long" in sys.argv)
