# 部署一覧と呼び方（D0024 で改定、2026-10-30）

| 部署 | 定義 | 呼び方 | いつ |
|---|---|---|---|
| 経営企画 | CLAUDE.md | メインセッション | 常時 |
| リサーチ部 | `.claude/agents/researcher.md` | subagent `researcher` | 案件ごと・木曜（トレンド＋競合の新着） |
| 商品企画部 | `.claude/agents/merchandiser.md` | subagent `merchandiser` | 収益案件（収益・提携部の下） |
| プラットフォーム戦略部 | `.claude/agents/channel-strategist.md` | subagent `channel-strategist` | 媒体・X の設計 |
| 編集部 | `.claude/agents/editor.md` | subagent `editor` | 案件ごと |
| **事実確認部** | `org/departments/fact-checker.md` | general-purpose に定義を読ませる | 編集部の後・レビュー部の前（毎案件） |
| レビュー部 | `.claude/agents/compliance-reviewer.md` | subagent `compliance-reviewer` | 公開前に毎回 |
| 分析部 | `.claude/agents/analyst.md` ＋ `org/departments/analyst-serp.md` | subagent `analyst`（競合分析は general-purpose） | 月曜 KPI、月1 競合分析 |
| **収益・提携部** | `org/departments/partnerships.md` | general-purpose | 水曜（週報）・収益案件 |
| **保守部** | `org/departments/maintenance.md` | general-purpose | 火曜（更新枠） |
| **読者体験部** | `org/departments/ux-auditor.md` | general-purpose | 月1回 |
| マーケティング部 | `org/departments/marketer.md` | general-purpose | X の予約・効果測定 |

## 案件の流れ（D0024 で追加した工程は太字）
起票 → リサーチ → （商品企画 → 媒体）→ 編集 → **readability 実測と `python3 scripts/lint_site.py`（経営企画）** → **事実確認** → レビュー → 修正 → PASS → site_data・build → PR（**CI の Site lint が通ること**）→ マージ → **公開後確認**

## 公開後確認（D0024 A3。経営企画、マージの後に必須）
1. 本番 URL で、依頼範囲の**全件**が反映されたことを確かめる（変更した文言・数値を本番の HTML で検索。1件の確認で済ませない）。
2. 反映待ちの間は「公開済み」と報告しない。デプロイの完了を待ってから報告する。
3. スマホ幅（390px）のスクリーンショットで表示崩れが無いことを見る（新記事・見た目を変えた案件）。
4. 依頼の範囲とやった範囲が違う場合（例: 要点だけ直して本文は未）は、報告で必ずその差を書く。

## 週のリズム
- 月: KPI 更新（分析部）、月初は競合・検索結果の分析
- 火: 新記事1本＋保守1件（保守部が選ぶ）
- 水: 収益・提携の週報（オーナーへの依頼を週1回にまとめる）
- 木: 週次トレンド（リサーチ部、競合の新着を含む）
- 月1: 読者体験の巡回
