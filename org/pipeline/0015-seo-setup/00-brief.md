# 00 発注書: SEO の担当と技術面のセットアップ

- 案件ID: 0015
- ステータス: 進行中
- 起票日: 2026-09-29
- 起票理由: オーナー「SEO対策の担当は？」への回答として提案し、オーナー承認（「Go ahead with SEO setup」）。

## 内容
- 担当の明文化（`org/seo/README.md`、D0012）と、分析部の役割への追記。
- 技術面の自動化（`scripts/build_site.py`）: 全ページに canonical・Open Graph・Twitter カード、記事に Article と BreadcrumbList、トップに WebSite の構造化データ、about・disclosure・privacy に meta description、sitemap に lastmod。共有用の画像 `images/og.png`（猫の2匹、文字なし）。
- 記事の本文・title は変更しない。

## レビューの観点
- 構造化データの内容が記事の実態と一致（公開日・更新日・著者は「男の養生帖 編集部」。資格や医療の専門性を示唆する項目（MedicalWebPage・reviewedBy 等）を入れていない）
- meta description に効能・誇張がない
- OG 画像が特定の商品・効能を示唆しない
- sitemap・canonical の URL が正しい

## 経営判断ログ
| 日付 | 工程 | 論点 | 判断 | 理由 |
|---|---|---|---|---|
| 2026-09-29 | 00 | 構造化データの種類 | Article（著者は Organization）と BreadcrumbList のみ。MedicalWebPage・Person・reviewedBy は使わない | 医療・専門家の監修を示唆しないため（about の「監修は受けていません」と整合） |
