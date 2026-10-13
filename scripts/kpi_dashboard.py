#!/usr/bin/env python3
"""Build org/kpi/snapshot.json and org/kpi/dashboard.html (D0019).

Automatic metrics come from the repository (articles, pages with affiliate
links, owner-inbox, pipeline, X queue). Manual metrics come from
org/kpi/weekly.csv (Search Console / GA4 / ASP), targets from
org/kpi/targets.json. No revenue amounts are read or written.

Usage: python3 scripts/kpi_dashboard.py [--today YYYY-MM-DD]
"""
import argparse
import csv
import datetime as dt
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from x_post import article_has_ad_links  # noqa: E402

KPI = os.path.join(ROOT, "org", "kpi")
JST = dt.timezone(dt.timedelta(hours=9))


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def auto_metrics(today):
    data = json.loads(load("scripts/site_data.json"))
    arts = data["articles"]
    cats = {c["id"]: c["name"] for c in data["categories"]}
    by_cat = {}
    for a in arts:
        k = a.get("category") or "guide"
        by_cat[k] = by_cat.get(k, 0) + 1
    monetized = [a["slug"] for a in arts if article_has_ad_links(f"articles/{a['slug']}.html")]
    if article_has_ad_links("tools.html"):
        monetized.append("tools")
    dates = sorted(a["date"] for a in arts)
    inbox = load("org/owner-inbox.md")
    open_items = len(re.findall(r"^- \[ \]", inbox, re.M))
    active = []
    for p in sorted(glob.glob(os.path.join(ROOT, "org/pipeline/0*/00-brief.md"))):
        m = re.search(r"^- ステータス: (.+)$", open(p, encoding="utf-8").read(), re.M)
        if m and not m.group(1).startswith(("公開済み", "完了", "取り下げ")):
            active.append({"case": os.path.basename(os.path.dirname(p)), "status": m.group(1)[:40]})
    queue = sorted(os.path.basename(p)[:10] for p in glob.glob(os.path.join(ROOT, "org/social/queue/*.json")))
    upcoming = [d for d in queue if d > today]
    return {
        "articles": len(arts),
        "articles_by_category": {cats.get(k, "入門ガイド（カテゴリなし）" if k == "guide" else k): v for k, v in by_cat.items()},
        "article_dates": dates,
        "monetized_pages": len(monetized),
        "monetized_list": monetized,
        "owner_inbox_open": open_items,
        "active_cases": active,
        "x_scheduled_upcoming": len(upcoming),
        "x_last_scheduled": upcoming[-1] if upcoming else None,
    }


def weekly_rows():
    with open(os.path.join(KPI, "weekly.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def latest(rows, col):
    for r in reversed(rows):
        v = (r.get(col) or "").strip()
        if v:
            return int(float(v)), r["週の初日"]
    return None, None


def current_phase(targets, today):
    for p in targets["phases"]:
        if today <= p["end"]:
            return p
    return targets["phases"][-1]


# ---------- HTML ----------

def esc(s):
    return html.escape(str(s))


def status(actual, target):
    if actual is None:
        return "nodata", "データ待ち"
    if target == 0:
        return "ok", "目標どおり"
    r = actual / target
    if r >= 1:
        return "ok", "到達"
    if r >= 0.5:
        return "warn", "途中"
    return "low", "これから"


def tile(label, actual, target, unit, note, since=None):
    cls, word = status(actual, target)
    pct = 0 if actual is None or not target else min(100, round(actual / target * 100))
    val = "—" if actual is None else f"{actual:,}"
    sub = f"<span class=\"since\">{esc(since)} 時点</span>" if since else ""
    return f"""<div class="tile {cls}" role="group" aria-label="{esc(label)}">
  <div class="tile-head"><span class="tile-label">{esc(label)}</span><span class="pill {cls}">{word}</span></div>
  <div class="tile-val"><span class="num">{val}</span><span class="unit">{esc(unit)}</span><span class="tgt">目標 {target:,}</span></div>
  <div class="bar" aria-hidden="true"><span style="width:{pct}%"></span></div>
  <div class="tile-note">{esc(note)} {sub}</div>
</div>"""


def articles_chart(dates, phases, today):
    """Cumulative published articles (step line) with phase targets as markers."""
    start = dt.date.fromisoformat(dates[0])
    end = dt.date.fromisoformat(phases[-1]["end"])
    W, H, L, R, T, B = 720, 260, 44, 16, 16, 34
    span = (end - start).days or 1
    ymax = max(phases[-1]["targets"]["articles"], len(dates))
    ymax = ((ymax + 9) // 10) * 10

    def x(d):
        return L + (dt.date.fromisoformat(d) - start).days / span * (W - L - R)

    def y(v):
        return T + (1 - v / ymax) * (H - T - B)

    pts, n = [], 0
    for d in dates:
        if pts:
            pts.append(f"{x(d):.1f},{y(n):.1f}")
        n += 1
        pts.append(f"{x(d):.1f},{y(n):.1f}")
    pts.append(f"{x(min(today, phases[-1]['end'])):.1f},{y(n):.1f}")
    grid = "".join(
        f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="grid"/>'
        f'<text x="{L-8}" y="{y(v)+4:.1f}" class="axis" text-anchor="end">{v}</text>'
        for v in range(0, ymax + 1, ymax // 5 if ymax >= 50 else 10))
    marks = "".join(
        f'<g class="tgtmark"><title>{esc(p["label"])}の目標: {p["targets"]["articles"]}本</title>'
        f'<circle cx="{x(p["end"]):.1f}" cy="{y(p["targets"]["articles"]):.1f}" r="6"/>'
        f'<text x="{x(p["end"]):.1f}" y="{H-12}" class="axis" text-anchor="middle">{esc(p["end"][2:7].replace("-", "/"))}</text></g>'
        for p in phases)
    lx, ly = x(min(today, phases[-1]["end"])), y(n)
    return f"""<svg viewBox="0 0 {W} {H}" role="img" aria-label="公開記事数の累計と目標">
{grid}
<polyline points="{' '.join(pts)}" class="line"/>
<g class="now"><title>{esc(today)} 時点: {n}本</title><circle cx="{lx:.1f}" cy="{ly:.1f}" r="5"/>
<text x="{lx+8:.1f}" y="{ly-8:.1f}" class="label">{n}本</text></g>
{marks}
<text x="{L}" y="{H-12}" class="axis">{esc(dates[0][2:7].replace('-', '/'))}</text>
</svg>"""


def render(snap, rows, targets):
    a, today = snap["auto"], snap["today"]
    ph = current_phase(targets, today)
    t = ph["targets"]
    idx, idx_d = latest(rows, "インデックス登録数")
    imp, imp_d = latest(rows, "検索表示回数(週)")
    ses, ses_d = latest(rows, "セッション(週)")
    clk, clk_d = latest(rows, "ASPクリック(週)")
    prog, prog_d = latest(rows, "提携済みで使える案件数")
    tiles = "".join([
        tile("公開記事数", a["articles"], t["articles"], "本", "サイトの記事（自動で集計）"),
        tile("収益の導線がある記事", a["monetized_pages"], t["monetized_pages"], "ページ", "アフィリエイトリンクが表示されるページ"),
        tile("インデックス登録", idx, t["indexed_pages"], "ページ", "Search Console「ページ」", idx_d),
        tile("検索の表示回数", imp, t["search_impressions_week"], "回/週", "Search Console", imp_d),
        tile("セッション", ses, round(t["sessions_month"] / 4.3), "回/週", "GA4（月の目標を週に換算）", ses_d),
        tile("ASP のクリック", clk, max(1, round(t["asp_clicks_month"] / 4.3)), "回/週", "ASP 管理画面（月の目標を週に換算）", clk_d),
    ])
    cur_attr = ' class="cur"'
    phase_rows = "".join(
        f"<tr{cur_attr if p is ph else ''}><th scope=\"row\">{esc(p['label'])}</th>"
        + "".join(f"<td>{p['targets'][k]:,}</td>" for k in ("articles", "monetized_pages", "indexed_pages", "search_impressions_week", "sessions_month", "asp_clicks_month", "conversions_month"))
        + f"<td class=\"focus\">{esc(p['focus'])}</td></tr>" for p in targets["phases"])
    wk_cols = ["週の初日", "インデックス登録数", "検索表示回数(週)", "検索クリック(週)", "セッション(週)", "うちX流入(週)", "ASPクリック(週)", "発生件数(週)", "承認件数(週)", "提携済みで使える案件数"]
    wk = "".join("<tr>" + "".join(f"<td>{esc(r.get(c) or '—')}</td>" for c in wk_cols) + "</tr>" for r in reversed(rows))
    cats = "".join(f"<li><span>{esc(k)}</span><span class=\"num\">{v}</span></li>" for k, v in sorted(a["articles_by_category"].items(), key=lambda kv: -kv[1]))
    cases = "".join(f"<li><span class=\"case\">{esc(c['case'])}</span><span class=\"st\">{esc(c['status'])}</span></li>" for c in a["active_cases"]) or "<li>なし</li>"
    chart = articles_chart(a["article_dates"], targets["phases"], today)
    return f"""<title>養生帖 KPI ボード</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700&family=Noto+Sans+JP:wght@400;500&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one column of sections; summary tiles first, then trend, then tables. */
:root {{
  --bg: #f5f6f3; --surface: #ffffff; --ink: #1c2420; --muted: #5d6a63; --line: #dfe4df;
  --accent: #2f6b55; --accent-soft: #d6e7df;
  --ok: #2e7d4f; --warn: #a66a00; --low: #8a8f8c; --nodata: #8a8f8c;
  --display: "Zen Kaku Gothic New", "Hiragino Sans", "Noto Sans JP", sans-serif;
  --body: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #121715; --surface: #1a211e; --ink: #e6ece8; --muted: #9aa8a0; --line: #2b3531;
  --accent: #7cc4a5; --accent-soft: #24382f; --ok: #6fcf97; --warn: #e0b04f; --low: #8c9590; --nodata: #8c9590; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #121715; --surface: #1a211e; --ink: #e6ece8; --muted: #9aa8a0; --line: #2b3531;
  --accent: #7cc4a5; --accent-soft: #24382f; --ok: #6fcf97; --warn: #e0b04f; --low: #8c9590; --nodata: #8c9590; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--body); line-height: 1.6; }}
.wrap {{ max-width: 1040px; margin: 0 auto; padding-inline: 16px; padding-block: 24px 48px; display: grid; gap: 28px; }}
h1, h2 {{ font-family: var(--display); text-wrap: balance; margin: 0; }}
h1 {{ font-size: 1.6rem; }}
h2 {{ font-size: 1.1rem; }}
.meta {{ color: var(--muted); font-size: .85rem; display: flex; flex-wrap: wrap; gap: 4px 16px; }}
.phase {{ background: var(--accent-soft); border-radius: 10px; padding: 12px 16px; display: flex; flex-wrap: wrap; gap: 4px 16px; align-items: baseline; }}
.phase b {{ font-family: var(--display); }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
.tile {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 8px; min-width: 0; }}
.tile-head {{ display: flex; justify-content: space-between; gap: 8px; align-items: center; }}
.tile-label {{ font-size: .9rem; color: var(--muted); }}
.pill {{ font-size: .72rem; padding: 2px 8px; border-radius: 99px; border: 1px solid currentColor; white-space: nowrap; }}
.pill.ok {{ color: var(--ok); }} .pill.warn {{ color: var(--warn); }} .pill.low, .pill.nodata {{ color: var(--low); }}
.tile-val {{ display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; }}
.num {{ font-family: var(--mono); font-variant-numeric: tabular-nums; }}
.tile-val .num {{ font-size: 1.8rem; }}
.unit {{ color: var(--muted); font-size: .85rem; }}
.tgt {{ margin-left: auto; color: var(--muted); font-size: .8rem; font-family: var(--mono); }}
.bar {{ height: 6px; background: var(--line); border-radius: 99px; overflow: hidden; }}
.bar span {{ display: block; height: 100%; background: var(--accent); border-radius: 99px; }}
.tile.ok .bar span {{ background: var(--ok); }}
.tile-note {{ font-size: .78rem; color: var(--muted); }}
.since {{ white-space: nowrap; }}
section {{ display: grid; gap: 12px; min-width: 0; }}
.card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px; min-width: 0; }}
svg {{ width: 100%; height: auto; display: block; }}
svg .grid {{ stroke: var(--line); stroke-width: 1; }}
svg .axis {{ fill: var(--muted); font-size: 11px; font-family: var(--mono); }}
svg .label {{ fill: var(--ink); font-size: 12px; font-family: var(--mono); }}
svg .line {{ fill: none; stroke: var(--accent); stroke-width: 2; stroke-linejoin: round; }}
svg .now circle {{ fill: var(--accent); stroke: var(--surface); stroke-width: 2; }}
svg .tgtmark circle {{ fill: var(--surface); stroke: var(--muted); stroke-width: 2; stroke-dasharray: 3 2; }}
.legend {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: .8rem; color: var(--muted); }}
.legend i {{ display: inline-block; width: 18px; height: 2px; background: var(--accent); vertical-align: middle; margin-right: 6px; }}
.legend i.t {{ width: 10px; height: 10px; border-radius: 50%; background: none; border: 2px dashed var(--muted); }}
.scroll {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: .85rem; }}
th, td {{ padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }}
th:first-child, td:first-child, td.focus {{ text-align: left; }}
thead th {{ color: var(--muted); font-weight: 500; }}
td {{ font-family: var(--mono); font-variant-numeric: tabular-nums; }}
td.focus {{ font-family: var(--body); white-space: normal; min-width: 12em; }}
tr.cur th, tr.cur td {{ background: var(--accent-soft); }}
.cols {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }}
ul.list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }}
ul.list li {{ display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px solid var(--line); padding-bottom: 6px; }}
.case {{ font-family: var(--mono); font-size: .85rem; }}
.st {{ color: var(--muted); font-size: .8rem; text-align: right; }}
.foot {{ color: var(--muted); font-size: .78rem; }}
</style>
<main class="wrap">
  <header style="display:grid;gap:8px">
    <h1>男の養生帖 KPI ボード</h1>
    <div class="meta"><span>集計日 {esc(today)}</span><span>目標 月10万円（2027年9月）</span><span>金額は載せていません</span></div>
  </header>
  <div class="phase"><span>いまの期</span><b>{esc(ph['label'])}まで</b><span>重点: {esc(ph['focus'])}</span></div>
  <section aria-labelledby="h-tiles"><h2 id="h-tiles">この期の目標に対して</h2><div class="tiles">{tiles}</div></section>
  <section aria-labelledby="h-trend"><h2 id="h-trend">公開記事数の推移と各期の目標</h2>
    <div class="card">{chart}<div class="legend"><span><i></i>公開記事数（累計）</span><span><i class="t"></i>各期末の目標</span></div></div></section>
  <section aria-labelledby="h-weekly"><h2 id="h-weekly">週ごとの実績（手入力・週次レポート）</h2>
    <div class="card scroll"><table><thead><tr>{''.join(f'<th scope="col">{esc(c)}</th>' for c in wk_cols)}</tr></thead><tbody>{wk}</tbody></table></div></section>
  <section aria-labelledby="h-phases"><h2 id="h-phases">期ごとの目標</h2>
    <div class="card scroll"><table><thead><tr><th scope="col">期</th><th scope="col">記事</th><th scope="col">導線あり</th><th scope="col">インデックス</th><th scope="col">検索表示/週</th><th scope="col">セッション/月</th><th scope="col">ASPクリック/月</th><th scope="col">発生/月</th><th scope="col">重点</th></tr></thead><tbody>{phase_rows}</tbody></table></div></section>
  <section aria-labelledby="h-ops"><h2 id="h-ops">運営の状況</h2>
    <div class="cols">
      <div class="card"><h2 style="font-size:.95rem;margin-bottom:8px">カテゴリ別の記事数</h2><ul class="list">{cats}</ul></div>
      <div class="card"><h2 style="font-size:.95rem;margin-bottom:8px">進行中の案件</h2><ul class="list">{cases}</ul></div>
      <div class="card"><h2 style="font-size:.95rem;margin-bottom:8px">そのほか</h2><ul class="list">
        <li><span>オーナー依頼（未対応）</span><span class="num">{a['owner_inbox_open']}</span></li>
        <li><span>X の予約投稿（これから）</span><span class="num">{a['x_scheduled_upcoming']}</span></li>
        <li><span>最後の予約日</span><span class="num">{esc(a['x_last_scheduled'] or '—')}</span></li>
        <li><span>使える提携案件</span><span class="num">{'—' if prog is None else prog}</span></li></ul></div>
    </div></section>
  <p class="foot">自動の指標はリポジトリから、手入力の指標は weekly.csv（Search Console・GA4・ASP）から集計しています。定義と目標の根拠は org/kpi/README.md。</p>
</main>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.datetime.now(JST).date().isoformat())
    args = ap.parse_args()
    targets = json.loads(load("org/kpi/targets.json"))
    rows = weekly_rows()
    snap = {"today": args.today, "auto": auto_metrics(args.today)}
    with open(os.path.join(KPI, "snapshot.json"), "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(KPI, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(render(snap, rows, targets))
    a = snap["auto"]
    print(f"articles={a['articles']} monetized={a['monetized_pages']} inbox_open={a['owner_inbox_open']} "
          f"active_cases={len(a['active_cases'])} x_upcoming={a['x_scheduled_upcoming']}")


if __name__ == "__main__":
    main()
