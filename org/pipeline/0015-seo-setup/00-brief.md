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
| 2026-09-29 | 05 | レビュー REVISE（必須: README の robots.txt の説明、リポジトリ直下に混入した SVG） | 採用。robots.txt の記述を訂正、直下の SVG 3点を削除し、cats_real.py は直接実行したときだけ書き出すように。推奨: 更新日が古い5本の `updated` を git 履歴と案件記録から入力（aga・protein=2026-09-28、hair・sleep・fatigue=2026-09-27）、README に参照先と期間の注記。トップの最新記事は「公開日順」に戻す（更新日順だと改訂した古い記事が新記事より上に出るため）。owner-inbox E1 への追記（月次チェックの参照）もこの案件の範囲 | 実態に合わせる |

