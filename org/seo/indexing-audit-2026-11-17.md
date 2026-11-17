# 集客の詰まりの技術診断（インデックス・クロール）2026-11-17

- 担当: 分析部（SEO 責任者、D0012）。依頼: 経営企画（D0021 11/17 追記の火曜枠）
- 対象: 本番 `https://hclab16k.github.io/health-affiliate-site/`（最後の本番反映は 2026-11-10 の pages-build-deployment。11/12 以降のコミットは社内資料で、配信内容は変わっていない）
- 方法: curl・Python（標準ライブラリ、TLS 検証あり）で sitemap の全50 URL を取得して解析し、Playwright（Chromium、モバイル相当の回線・CPU 制限）で5ページを計測した。GitHub Actions は `gh run list/view` で確認した。Google の検索結果（site: 検索）は取得していない。
- 「推定」と書いたものは外から確かめられない推論。Search Console の数字は `org/owner-inbox.md` D13・D15 にあるオーナーの報告（最新は 10/29）だけを使った。

## 0. 結論（先に）

**技術的な「止め」は見つからなかった。** noindex・robots の遮断・canonical の誤り・ソフト404・JS 依存の本文・極端な遅さはない。全ページが200で返り、正規 URL と sitemap が一致し、トップから2クリック以内で全記事に届く。

検索から来ない理由として一番確からしいのは、**技術の問題ではなく、新しい YMYL（健康）サイトを Google が「どこまで登録し、どの順位に置くか」を慎重に決めている段階にあること**（推定）。報告では、sitemap が一度も読まれず（9/28〜10/9「取得できませんでした」、11/5 の再確認は未回答）、登録は URL ごとのリクエストでしか進んでいない（10/29 時点で登録済み21・クロール済み未登録1、約50ページ中）。これと合わせると、**Google がこのサイトを自分から取りに来る頻度（クロールの需要）が低い**と読める（推定）。

コードで直せる小さな問題はある（4章）。ただし、どれも「来ない」の主因になるほどの大きさではない（推定）。11/26 の判断材料には、Search Console の数字（6章）が要る。

## 1. 点検結果の一覧

| # | 項目 | 結果 | 判定 |
|---|---|---|---|
| 1a | ホスト直下 `https://hclab16k.github.io/robots.txt` | 200・`User-agent: * / Allow: / Sitemap: …/health-affiliate-site/sitemap.xml`（最終更新 10/29。オーナーが作った `hclab16k.github.io` リポジトリから配信） | OK |
| 1b | サイト配下 `/health-affiliate-site/robots.txt` | 200・同じ内容。Google はここを読まない（効力なし・害なし） | OK |
| 1c | sitemap.xml | 200・`application/xml`・XML として正しい・名前空間 OK・**50 URL ＝ 記事37＋カテゴリ8＋固定5**（トップ・about・disclosure・privacy・tools）。ローカルの `sitemap.xml` と完全に一致。Googlebot の UA でも 200 | OK |
| 1d | sitemap の lastmod | 46/50 にあり。**トップ・about・disclosure・privacy の4件に無い** | 軽微 |
| 1e | sitemap の URL と正規 URL | 50件すべて「200・リダイレクトなし・`canonical` ＝ `<loc>` ＝ `og:url`」 | OK |
| 2a | meta robots・X-Robots-Tag | 50件とも無し（noindex の混入なし） | OK |
| 2b | title | 重複0。記事は全角33〜41字（検索結果では末尾が少し切れる長さ。致命的ではない） | OK |
| 2c | description | 重複0・欠落0。記事は94〜125字、カテゴリ50〜97字 | OK |
| 2d | hreflang | 無し。`<html lang="ja">`・`og:locale ja_JP`。日本語のみのサイトなので不要 | OK |
| 2e | JSON-LD | 50件すべて JSON として正しい。記事＝Article＋BreadcrumbList（datePublished・dateModified・author・publisher・logo・image あり）、トップ＝WebSite。著者は Organization（「男の養生帖 編集部」） | OK（4-F 参照） |
| 2f | h1 | 50件すべて1つ | OK |
| 2g | 重複 URL | `…/index.html` と `…/`、`…/articles/xxx` と `…/articles/xxx.html` がどれも200（GitHub Pages の仕様）。どれも canonical で正規 URL を指すので害は小さい。ただし**サイト内のリンクが全ページで `index.html` を指している**（4-A） | 軽微 |
| 2h | http→https・末尾スラッシュ | `http://…/` → 301 で https。`/health-affiliate-site` → 301 で末尾 `/` | OK |
| 2i | 404 | 存在しない URL・`org/` 配下は本当の 404 を返す（ソフト404でない）。社内資料は配信されていない | OK |
| 3a | 内部リンクの深さ | トップから1クリック: 18ページ（カテゴリ8・トップの最新記事6・ガイド1 ほか）。2クリック: 31ページ（記事30・tools）。**孤立ページ0** | OK |
| 3b | 被リンク数（サイト内、記事への） | 最少は ed-otc-tadalafil・whitening-japan-vs-overseas・nocturia-night-urination の3（うち記事から2）。最多は fatigue-recovery の16 | 軽微 |
| 3c | カテゴリに載らない記事 | `mens-selfcare-start`（`category: null`）はどのカテゴリページにも無い。今はトップのガイド枠と記事8本から届く | 軽微 |
| 3d | tools.html | トップ・カテゴリから直接のリンクなし。記事3本（hair-damage-care・mens-selfcare-start・oral-care-basics）からのみ。10/29 時点で「未登録」の報告あり | 軽微 |
| 4a | HTML の大きさ | 記事 36〜68KB、トップ 14KB、カテゴリ 5〜10KB。画像は `images/` 全体で 200KB（og.png 39KB、50KB を超える SVG なし） | OK |
| 4b | 応答 | HTML の取得 0.1〜0.5 秒（このサンドボックスのプロキシ経由の値） | OK |
| 4c | 表示速度（Playwright、390×844・遅延150ms・1.6Mbps・CPU 4倍遅く） | FCP/LCP: トップ 1.2秒、ashwagandha 0.84秒、glp1-diet 0.72秒、personal-gym-checklist 0.75秒、category/hair 0.74秒（LCP 要素は本文の段落、カテゴリはサムネイル画像）。CLS はすべて0。目安の 2.5 秒を大きく下回る | OK |
| 4d | 外部スクリプト | Google Fonts の CSS（描画を待たせる）、GA4、**全記事に A8 の `a8linkmgr.js`**（商品リンクの無い記事にも入る）。速度の数値には今のところ響いていない | 参考 |
| 4e | 本文の描画 | 本文は静的 HTML（JS なしで読める）。Google のレンダリングに依存しない | OK |
| 5 | IndexNow | 直近の実行は全22回 success（10/29 の全件送信 43 URL→HTTP 200、11/3 17 URL→200、11/10 11 URL→200、変更なしの回は「No changed pages」）。11/10 以降は本番の更新がないので実行なし。**IndexNow は Bing などへの通知で、Google には効かない** | OK（Google には無関係） |
| 6 | github.io のサブパス・独自ドメインなし | 7章 | 構造上の不利（推定） |

## 2. 詰まりの候補（確からしい順）

1. **Google のクロール需要・品質の判断待ち（新しい YMYL サイト）** — 確からしさ: 高（推定）
   - 根拠: 技術の点検はすべて通る。登録は URL ごとのリクエストでしか進まず（10/9 登録5 → 10/19 登録12 → 10/29 登録21）、melatonin が「クロール済み - インデックス未登録」、表示の大半は1記事から（D0021 背景）。外部からの被リンクは確かめられないが、X の流入0（D0021 11/17 追記）から見ても少ないと推定。
   - 健康の情報は Google が「信頼できる発信元か」を厳しく見る分野。著者が組織名だけで、監修・実名の責任者がいない（D0026 で「人の責任はまだなし」）ことも、判断を遅らせる方向に働きうる（推定。Google は個々の要因を公表しない）。
2. **sitemap を Google が読んでいない（読まれていない状態が続いている）** — 確からしさ: 中（11/5 以降の状態が未確認）
   - ファイル側は正常（1c）。ホスト直下の robots.txt にも 10/29 から `Sitemap:` がある。それでも「取得できませんでした」なら、Search Console 側でこのプロパティを後回しにしている（＝1と同じ根っこ）と推定。sitemap が読まれないと、新記事が見つかるのは内部リンク経由のクロールか手動リクエストだけになる。
   - 10/30 以降の新記事5本（personal-gym-checklist・aga-clinic-cost-guide・medical-hair-removal-cost・gym-after-course・aga-oral-treatment-timeline。収益の柱の D0026 分野）は、登録状況の報告がない。**登録されていなければ、高単価分野の入口がまだ検索に存在しない**。
3. **登録されても順位が付かない（狙う語の競合・需要）** — 確からしさ: 中（推定。技術の範囲外）
   - 登録21ページで3か月の表示234（10/29 時点）は、登録されたページの多くが表示圏外（おおむね100位より下）にいることを示す（推定）。`org/seo/serp-2026-10-30.md`・`serp-2026-11-02.md` の競合調査の続きで見る。
4. **サイト内の小さな技術の不整合** — 確からしさ: 低（主因ではない）
   - 内部リンクが非正規の `index.html` を指す（85本／48ページ）、lastmod の欠け4件、tools.html とガイド記事の導線の弱さ。直すのは安い（4章）が、直しても流入が目に見えて変わるとは考えにくい。
5. **github.io のサブパス配信** — 確からしさ: 低〜中（推定。今週は手を打てない）
   - 7章。

## 3. 「ではない」と言えるもの（外から確かめた）

- noindex・X-Robots-Tag・robots.txt の Disallow による遮断ではない。
- canonical が別 URL を指して登録を譲っているのではない（50件すべて自己参照）。
- リダイレクトの連鎖・ソフト404・5xx ではない。
- 本文が JS で描かれていて Google に読めない、ではない。
- 表示が遅い（Core Web Vitals）、ではない（4c）。
- sitemap の書式・URL 数・場所の誤りではない（1c・1e）。
- 社内資料（org/ 等）が配信されて品質を下げている、ではない（404）。

## 4. 経営企画が今週できる対策（コードで直せるもの）

記事 HTML と scripts は本診断では編集していない。以下は修正案。優先度は「主因への効き」ではなく「安くて害がない順」。

### A. 内部リンクを正規 URL（`./`・`../`）に揃える — 小
- 現状: ロゴ（全48ページのヘッダー）とパンくず（記事37本）が `index.html` / `../index.html` を指す。canonical は `…/health-affiliate-site/` なので、内部リンクと canonical が食い違う。
- 修正案:
  - `scripts/build_site.py` 218行: `crumbs = '<a href="../index.html">男の養生帖</a>'` → `crumbs = '<a href="../">男の養生帖</a>'`
  - ヘッダーのロゴは各 HTML に直書き（例 `index.html` 42行 `href="index.html"`、`articles/*.html`・`category/*.html` の40〜42行 `href="../index.html"`）。記事を1本ずつ直す代わりに、`scripts/build_site.py` 25〜29行の `write()` で書き出し前に置換する:
    `text = text.replace('href="../index.html"', 'href="../"').replace('href="index.html"', 'href="./"')`
    （配信する全 HTML（about・disclosure・privacy・tools を含む）は 256〜272行のループで `write()` を通るので、これ1か所で全ページに効く。build 後に `grep -rn 'index.html"' --include=*.html . | grep -v '^./org/'` で残りが0か確認）
- 注意: ローカルでファイルを直接開いたときは `../` がフォルダ一覧になる（配信上は問題なし）。

### B. sitemap の lastmod を全 URL に付ける — 小
- `scripts/build_site.py` 275行の `urls = [(SITE, None), (SITE + "about.html", None), …]`: トップは「最新記事の公開日・更新日の最大値」、about・disclosure・privacy は `scripts/site_data.json` の `pages` と同じ形で `updated` を持たせて渡す（391行の tools と同じ）。
- 効果は小さい（Google は lastmod を「正確なときだけ」使う）。**体裁だけの変更で `updated` を動かさない**運用（README「更新日の運用」）を続けることの方が大事。

### C. tools.html と mens-selfcare-start への導線 — 小
- `index.html` 43〜47行の `site-nav`、またはトップの本文に tools.html へのリンクを1本足す（10/29 時点で未登録、オーナーは「収益ページ、最優先」と記録）。
- `mens-selfcare-start` は `category: null` のためカテゴリページに出ない。トップのガイド枠から外れると記事経由でしか届かなくなる。今は害なし。トップのガイド枠を残すことだけ守る。

### D. 被リンクの少ない記事への内部リンク — 中（編集部の作業）
- サイト内の被リンクが3本しかない ed-otc-tadalafil・whitening-japan-vs-overseas・nocturia-night-urination と、D0026 の新記事（gym-after-course・medical-hair-removal-cost・personal-gym-checklist は記事からの被リンク3〜5本）へ、関連する既存記事の該当節からリンクを足す。D0025 の「疑問系 → 比較ページ」の送客とも同じ作業。記事 HTML の編集なので、通常の案件（レビューつき）で行う。

### E. org/seo/README.md の記述を直す — 小
- 18行は「Google が読むのはホスト直下の robots.txt だけなので、クロール制御には使えない」とあるが、10/29 からホスト直下に robots.txt がある（オーナーの `hclab16k.github.io` リポジトリ）。「ホスト直下の robots.txt は `hclab16k.github.io` リポジトリで管理、Sitemap 行あり」に更新する。

### F. 信頼の情報を構造化データにも載せる（任意）— 小
- Article の `author` は Organization のみ。`publisher`/`author` に `url`（about.html）を足す（`scripts/build_site.py` 142行以降 `seo_block`）。about.html に「記事の作り方・出典の方針・誤りの連絡先」がそろっているかを確認する。実名の責任者・監修は D0026 で保留中なので、ここでは書かない（捏造しない）。

### やらないこと
- 同じ URL の「インデックス登録をリクエスト」の連打、`sitemap.xml?v=3` などの再送信の繰り返し（効果が確かめられず、作業だけ増える）。
- 記事の量産で入口を増やすこと（D0021 の理由のとおり、登録が追いつかない段階では逆効果になりうる）。

## 5. GitHub Actions（IndexNow）の詳細

- `.github/workflows/indexnow.yml` は pages-build-deployment の完了ごとに、変わった `*.html` を `api.indexnow.org` に送る。`gh run list` で全22回 success（10/29 の手動全件送信を含む）。ログ上の応答はすべて HTTP 200。
- 鍵ファイル `…/health-affiliate-site/85426c61f7f008ceeccb62379df9b5e8.txt` は200で配信。鍵の置き場所がサブパスでも、送る URL がすべてその配下なので仕様上問題ない。
- **Google は IndexNow を使わない**。このワークフローは Bing（と提携先）向け。Bing の状況は Bing Webmaster Tools でしか確かめられない（6章の任意項目）。
- GitHub Pages の設定 API（`repos/…/pages`）はこの環境のプロキシで許可されず、確かめていない。

## 6. オーナーに Search Console で確かめてもらう項目（11/26 の判断の前に）

プロパティは URL プレフィックス `https://hclab16k.github.io/health-affiliate-site/`（HTML ファイル方式）。スクショでよい。

1. **「ページ」レポート（インデックス作成 → ページ）**
   - 「登録済み」と「未登録」の件数（10/29: 21・1 からの変化）
   - 「未登録」の**理由別の件数**: 特に「検出 - インデックス未登録」「クロール済み - インデックス未登録」「代替ページ（適切な canonical タグあり）」「重複しています」「ページにリダイレクトがあります」「見つかりませんでした（404）」
   - 「代替ページ」に `…/index.html` や拡張子なしの URL が出ていれば正常（4-A で減らせる）。記事の `.html` が出ていたら知らせてほしい
2. **「サイトマップ」**: `sitemap.xml`（と 10/4 の `sitemap.xml?v=2`）の状態・最終読み込み日時・検出されたページ数。10/29 にホスト直下の robots.txt に Sitemap 行を入れてから変わったか
3. **URL 検査（「インデックス登録をリクエスト」は押さなくてよい。結果のスクショ）**
   - `articles/personal-gym-checklist.html`（10/30〜11/10 の D0026 新記事の代表）
   - `articles/aga-oral-treatment-timeline.html`（11/10 公開の最新記事）
   - `tools.html`（10/29 未登録）
   - `articles/melatonin-japan-vs-us.html`（「クロール済み - 未登録」だったもの）
   - `articles/ashwagandha-japan.html`（表示の大半を集めていた記事。比較の基準として）
   - 見る欄: 「URL は Google に登録されています／いません」、理由、**検出元（サイトマップ／参照元ページ）**、前回のクロール日時、ユーザーが指定した canonical と Google が選んだ canonical
   - 未登録だった新記事5本（personal-gym-checklist・aga-clinic-cost-guide・medical-hair-removal-cost・gym-after-course・aga-oral-treatment-timeline）は、このときに「インデックス登録をリクエスト」してよい（1日の上限内で）
4. **設定 → クロールの統計情報**: 過去90日の合計クロールリクエスト数、平均応答時間、ホストの状態（robots.txt の取得・DNS・サーバー接続に問題なし、になっているか）
5. **検索パフォーマンス（過去3か月）**: 合計の表示・クリック、表示のあるページ数、上位10クエリ（D0021 戻す条件②の判定用）
6. **手動による対策・セキュリティの問題**: 「問題は検出されませんでした」か（念のため）
7. （任意）Bing Webmaster Tools に登録済みなら、インデックス済み URL 数（IndexNow の効き目の確認）

## 7. github.io のサブパス配信・独自ドメインなしの不利（一般論、短く）

- `github.io` は Public Suffix List に載っており、Google は `hclab16k.github.io` を1つのサイトとして扱う（推定ではなく公開情報。どのように評価に効くかは非公表）。不利は主に3つ（推定）:
  1. **評価の積み上げが移せない**: 後で独自ドメインへ移ると、301 を張れない（GitHub Pages は任意の 301 を出せない。独自ドメイン設定時だけ自動で転送される）ので、それまでの評価の引き継ぎが不確か。移るなら早いほど損が小さい。
  2. **ドメインプロパティが使えない**: Search Console は URL プレフィックスのみ。ホスト直下（robots.txt・トップ）は別リポジトリ `hclab16k.github.io` の管理になる（現状、トップは英語の空のページで、このサイトへのリンクもない）。
  3. **信頼の見え方**: 無料の共有ホストの下層フォルダにある健康サイトは、読者・リンク元から「事業者の運営」と見られにくい（推定）。
- D0026 で独自ドメインは保留（12末に再検討）。本診断の範囲では「今週の主因」ではないが、12末の再検討では上の1を判断材料にしてほしい。

## 8. 前工程の検証・限界

- D0021 背景の「インデックスは約12ページ」は 10/19 の報告値。10/29 の報告では登録済み21で、D0021 の記述は少し古い（数字は本書2章で更新）。
- `org/seo/README.md` 18行の robots.txt の記述が現状と食い違う（4-E）。
- 計測はこのサンドボックスのプロキシ経由で、実際の利用者の回線・Google の取得とは異なる。トップの load イベントだけ 24 秒かかったが、FCP/LCP は 1.2 秒で、GA のビーコンがプロキシで待たされた計測上の現象と推定（他ページは 1.0〜1.6 秒）。
- 外部の被リンク数、Google の登録状況・順位は外からは確かめていない（site: 検索は自動取得しない方針）。
