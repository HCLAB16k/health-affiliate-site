# D0012: SEO の担当を明確にし、技術面を自動化する

- 日付: 2026-09-29
- ステータス: 採用
- 決定者: オーナー（「Go ahead with SEO setup」）／経営企画の提案
- 関連: `org/seo/README.md`、案件0015

## 決定
- SEO 全体の責任者は分析部。各工程の SEO 関連の担当は `org/seo/README.md` の表のとおり。
- 技術面（canonical・OGP・Twitter カード・構造化データ・sitemap の lastmod）は `scripts/build_site.py` で全ページに自動で付ける。
- 月次チェックはオーナーが Search Console の数値を共有し、分析部が読む。

## 理由
- 各部署に SEO の作業が分散して責任者がいなかった。技術面は手作業だと記事を足すたびに漏れる。
