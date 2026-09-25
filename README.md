# ジェントルマンズケア（メンズ美容・健康アフィリエイトサイト）

30代以降のビジネスパーソン向け、男性の身だしなみ・アンチエイジングをテーマにしたアフィリエイトサイトです。
全体戦略・デプロイ手順は **`PLAN.md`**、日々の運営は **AI組織**（会社憲章 `CLAUDE.md`、`org/`）で行います。

## AI組織での運営
リサーチ → 商品企画 → プラットフォーム戦略 → 編集 → レビュー の各部署を Claude Code のサブエージェント
（`.claude/agents/`）として独立させ、案件フォルダの書類で引き継ぎます。Claude Code で `/org-cycle` を実行すると
案件を1件、PR作成まで進めます（マージ＝公開の判断はオーナー）。

- `CLAUDE.md` — 会社憲章（目標・分離ルール・部署の分担・守ること）
- `org/goals.md` — 月10万円の逆算と現在地
- `org/owner-inbox.md` — **オーナー（人間）にお願いしたい作業**
- `org/pipeline/` — 案件フォルダとバックログ
- `org/decisions/` — 方針決定の記録
- `org/compliance-checklist.md` — 薬機法・景表法・ステマ・医療広告の審査基準

## このフォルダの中身
- `PLAN.md` — 事業計画・収益化モデル・法規制・デプロイ手順（最初に読む）
- `content-calendar.md` — 90日分の記事公開計画
- `keywords.csv` — ロングテールキーワード案
- `index.html` / `about.html` / `disclosure.html` / `privacy.html` — サイト本体ページ
- `articles/` — 記事5本（スキンケア・ヘアケア・プロテイン・睡眠・疲労回復）
- `style.css` — 全ページ共通デザイン（ネイビー×ゴールドの落ち着いた配色、レスポンシブ対応）
- `robots.txt` / `sitemap.xml` — SEO用設定ファイル

## すぐ試したい場合
`index.html` をダブルクリックすればブラウザでそのまま確認できます（インターネット接続不要）。

## 公開するには
`PLAN.md` の「5. デプロイ方法」を参照。GitHub Pagesで公開中（github.com/HCLAB16k/health-affiliate-site）。

## 重要: 公開前に必ずやること
1. 各記事内の `<!-- ASPリンクをここに挿入 -->` を、A8.net等で取得した実際のアフィリエイトリンクに置き換える（`protein-guide.html` は設置済み）
2. `about.html` の運営者情報をあなたの実情報（または屋号）に更新する
3. 独自ドメインを決めたら `index.html` 等の `<title>` とヘッダーのサイト名を置換する

薬機法・景品表示法・ステマ規制については `disclosure.html` と `PLAN.md` 3章を必ず確認してから記事を追加してください。
