# SEO 監査（0036 スコープ3）— 分析部

- 案件ID: 0036
- 作成: 分析部（analyst）、2026-10-09
- 対象: 公開ページ 34（`index.html`、`about.html`、`disclosure.html`、`privacy.html`、`tools.html`、`category/*.html` 6、`articles/*.html` 22）と `scripts/build_site.py`・`scripts/site_data.json`・`sitemap.xml`・`keywords.csv`・`style.css`・`robots.txt`・`_config.yml`
- 対象外: `articles/blue-light-glasses.html`（0034 で作業中。`site_data.json` にまだ無い。下の T-18 に関係する点だけ書く）
- 編集したファイル: この `seo-audit.md` だけ。git の操作はしていない。

## 0. 前提: 検索のデータがまだ無い

- `org/kpi/monthly.csv` にはヘッダー行しか無い。Search Console のエクスポート（クエリ別・ページ別）も `org/kpi/` に無い。
- そのため、この監査は**リポジトリの中身（HTML・ビルドスクリプト・キーワード表）だけ**で判断している。「表示回数は多いが CTR が低い」「11〜20位」「クリックはあるが成約しない」の洗い出しは**今はできない**。下の「影響」は、ページの作りから見た見込みで、検索の実績で確かめたものではない。
- サイトは 2026-09 に公開したばかりで、記事の多くは公開から2週間以内。`org/seo/README.md` の目安（3か月で順位・CTR からリライトを判断）からみても、実績にもとづくリライト判断はまだ早い。
- 必要なデータは 7章に「オーナーへの依頼の案」として書いた（このファイル以外は編集しない指示なので、`owner-inbox.md` には書いていない。経営企画から転記をお願いしたい）。

## 1. 要点（先に結論）

1. **記事ページに公開日・更新日・書き手が出ていない**（JSON-LD の中にしか無い）。健康分野の記事では、日付と運営者が見えることが信頼の材料になる。`build_site.py` で全記事に自動で入れられる。→ T-1
2. **内部リンクに偏りがある**。`minoxidil-finasteride-guideline` はどの記事からもリンクされていない（入口はカテゴリページと sitemap だけ）。`ashwagandha-japan`・`whitening-japan-vs-overseas` は記事からのリンクが1本ずつ。関連記事が1本だけの記事も4本ある。→ T-2
3. **カード・アンカーに使う短いタイトル（`site_data.json` の `title`）が記事の中身とずれている**ものがある（「スキンケア」「ヘア・スカルプケア」など）。トップ・カテゴリページのリンクの文言がそのまま弱くなっている。→ T-3
4. **title が長い**。全角換算で45字を超えるものが10本（最長64.5字）。主キーワードはほぼ先頭にあるので、致命的ではない。ただし、`keywords.csv` で優先度「高」の検索語が title に入っていない記事がある（疲れ「取れない」、睡眠「質」など）。→ T-4・付録A
5. **FAQPage の構造化データは入れない**ことを勧める。Google の FAQ リッチリザルトは 2023年8月から「よく知られた政府・健康分野の権威あるサイト」に限られていて、当サイトでは表示が見込めない。ページ上の「よくある疑問」の節は読者のためにそのまま残す。→ 4章

## 2. 問題の一覧（優先度順）

影響は「高＝サイト全体または主力記事の評価・クリックに効く見込み／中＝一部のページ、または効果が限られる／低＝整備・予防」。自動化欄の「BS」は `scripts/build_site.py` で自動化できるもの。

| # | 影響 | 対象ページ | 問題 | 具体的な修正案 | 自動化 |
|---|---|---|---|---|---|
| T-1 | 高 | 全記事 22 | 記事の本文に公開日・更新日・書き手が出ていない（`class="date"` などが0件）。Article の JSON-LD には `datePublished`・`dateModified` があるが、ページで見えない。健康分野（YMYL）では日付と運営者が見えることが信頼の材料になり、Google も日付を見える形で出すよう勧めている | h1 の直後に「公開 2026.09.13 ／ 更新 2026.09.29 ／ 文：男の養生帖 編集部（<a href="../about.html">運営者情報</a>）」の1行を入れる。値は `site_data.json` の `date`・`updated` から取る（JSON-LD と必ず一致する） | BS: `cat-nav` と同じやり方で、`<!-- byline:start -->…<!-- byline:end -->` を `</h1>` の直後に毎回入れ直す。`style.css` に `.byline` を足す |
| T-2 | 高 | `minoxidil-finasteride-guideline`（記事からのリンク0本）、`ashwagandha-japan`・`whitening-japan-vs-overseas`（1本）、関連記事が1本だけの `protein-guide`・`winter-vitamin-d`・`whitening-japan-vs-overseas`・`retinoids-japan-vs-overseas` | 記事から記事へのリンクが偏っている。ハブの `mens-selfcare-start` も、10/07以降の新しい記事（ミノキシジル・ホワイトニング・カフェイン・メラトニン・アシュワガンダ）を拾えていない（付録C） | (1) 手で足す（編集部）: aga の「ミノキシジルの内服」（推奨度D）の段落と hair-tonic-review・hair-scalp-care の関連記事 → minoxidil。mens-selfcare-start の髪の節 → minoxidil、口の節 → whitening、睡眠の節 → caffeine・melatonin。sleep-support・fatigue-recovery のサプリの節 → ashwagandha・melatonin。winter-vitamin-d の関連記事 → sleep-support・fatigue-recovery・skincare-antiaging（紫外線）。protein-guide の関連記事 → fatigue-recovery・mens-selfcare-start。(2) 抜けを防ぐ仕組み: 全記事の末尾に「同じカテゴリの記事」を自動で出す | BS: `<!-- related-auto:start/end -->` を参考資料の h2 の前に入れ、同じ `category` の記事（自分以外、新しい順、最大5本）を短いタイトルで並べる。category が null の記事（mens-selfcare-start）は全カテゴリの代表記事を出す。手で選んだ「関連記事」はそのまま残す |
| T-3 | 高 | `site_data.json` の `title`・`desc` → トップ・カテゴリページのカード | カードの見出し（＝リンクの文言）が記事の中身とずれている。`skincare-antiaging` は「スキンケア」、`hair-scalp-care` は「ヘア・スカルプケア」で、説明文の「頭皮ケアの成分と選び方」も、今の記事（抜け毛が増えたときにまず確かめること）とずれている。`aga-selfcare-vs-clinic` の説明文「…を中立に整理」も中身が分かりにくい | `title` の案: skincare-antiaging「30代からの男のスキンケアの基本」、hair-scalp-care「抜け毛が増えたと感じたら」。`desc` は記事の meta description の最初の一文に合わせる（ただし誇張しない）。BreadcrumbList の最後の名前にも、この短いタイトルを使う（T-5） | 一部 BS: カードの `title` が記事の h1 の先頭（「｜」の前まで）とまったく重ならないときに警告を出すチェックを足す |
| T-4 | 高（キーワードのずれ）／中（長さだけ） | 付録A の10本（全角45字超）と、検索語がずれている4本 | (a) 長さ: sleep-support 64.5、minoxidil 59、ashwagandha 58、retinoids 57、hair-damage-care 52、body-odor-sweat 52、caffeine-limits 48.5、fatigue-recovery 47、mens-selfcare-start 47、whitening 46（全角換算）。検索結果では日本語で30〜35字前後から先が切れやすい。(b) ずれ: fatigue-recovery は「疲れが取れない 原因 病気」（高）に対して title に「取れない」「原因」が無い。sleep-support は「睡眠の質を上げるには」（高）に対して「質」が無い。winter-shaving-skin は読者がよく使う「カミソリ負け」が title に無い（本文には1か所ある）。whitening は「セルフ」が後ろの方にあり、切れて見えない | 付録A の案（どれも本文の範囲内の言い方で、効能の言い切り・煽りを含まない）。方針: 主な検索語を最初の30字以内に入れる、全体は40字前後まで、h1 は title と最初の30字をそろえる（h1 は詳しいままでもよい）。編集部が書き換え、レビュー部が誇張の有無を差分で見る | なし（文言は人が決める）。BS で全角換算45字を超える title に警告を出すことはできる |
| T-5 | 中 | 全記事、カテゴリページ 6 | パンくずがページに出ていない（BreadcrumbList の JSON-LD だけある）。JSON-LD の最後の項目名は長い title（最長64.5字）。カテゴリページには BreadcrumbList が無い | 記事: `cat-nav` の下に「男の養生帖 › ヘア・AGA › 抜け毛が増えたと感じたら」の見えるパンくずを出し、JSON-LD の項目名も同じ短いタイトルにする。カテゴリページ: 「男の養生帖 › ヘア・AGA」の BreadcrumbList と見えるパンくず | BS: `seo_block()` の BreadcrumbList の最後の `name` を `a["title"]` にする。`<nav class="breadcrumb" aria-label="パンくず">` を `cat_nav` の直後に入れる関数を足す。カテゴリページの分岐を足す |
| T-6 | 中 | `category/*.html` 6 | (a) 見出しの段が飛んでいる: h1 の次がカードの h3（h2 が無い）。(b) ページが薄い: h1 とリード1文とカードだけ。oral・grooming は2記事、skin・body は3記事。(c) title が「◯◯の記事一覧 \| 男の養生帖」だけで、何が読めるかが分からない | (a) カードの上に `<h2>記事一覧</h2>` を入れる（またはカテゴリページのカード見出しを h2 にする）。(b) `site_data.json` の各カテゴリに `intro`（2〜3文。どの記事から読むとよいか）と `start`（最初に読む記事の slug）を足し、リードの下に「まず読む記事」を1本出す。リードの文も読みやすく直す（hair の「…記事と、…記事です」は長い）。(c) カテゴリに `seo_title` を足す。例: 「ヘア・AGAの記事一覧｜抜け毛・育毛剤・受診の目安 \| 男の養生帖」 | BS: カテゴリページを作る部分（`for c in cats:`）で h2・intro・start・seo_title を出す |
| T-7 | 中 | `keywords.csv` | (a) 22記事のうち12記事が表に無い（hair-tonic-review・winter-shaving-skin・beard-hair-removal・hair-damage-care・mens-bb-cream・oral-care-basics・minoxidil・whitening・body-odor-sweat・melatonin・ashwagandha・caffeine）。(b) 割り当てが合っていない行がある: 「サプリ 飲み合わせ 注意」→ disclosure.html、「機能性表示食品 とは」「男性 グルーミング とは」→ about.html、「レチノール 男性 使い方」→ skincare-antiaging（専門の記事は retinoids）。(c) 「おすすめ」「比較」の購入検討の語（例: メンズ スキンケア おすすめ／高、プロテイン おすすめ 社会人／高）は、順位をつけないサイトの方針と検索の意図が合わない。(d) 対応記事の列の書き方が `articles/x.html` と `x.html` で混ざっている。カテゴリ名もサイトと違う（ヘアケア／疲労回復など） | 付録D の割り当て表で直す。「おすすめ」系の行は消さずに、優先度を「対象外（順位をつけない方針。C02・#27 の入口のサインとして見る）」にする。列を `slug` にそろえ、カテゴリは `site_data.json` の id にそろえる | 一部 BS（または別の小さなスクリプト）: keywords.csv の slug が site_data に無い・記事が keywords.csv に1行も無いときに警告を出す |
| T-8 | 中 | 付録B の長いもの（melatonin・caffeine-limits・sleep-support・aga・whitening・body-odor-sweat など） | meta description がおよそ130〜165字あり、スマホでは70〜90字前後、PC では120字前後で切れる。いくつかは前半が「〜を、厚生労働省の…と…で確認。」のように資料名が先に来ていて、読者の疑問への答えが後ろにある | 最初の50〜60字に「何が分かるか」（読者の疑問と答えの方向）を書き、資料名は後ろにする。全体は100〜120字を目安にする。「出典と確認日つき」「商品の紹介なし」は最後に残してよい（信頼の材料）。retinoids と winter-vitamin-d の書き方（最初の文で事実を言う）が手本になる | なし（文言は人が決める）。BS で140字を超えたら警告を出すことはできる |
| T-9 | 中 | 長い記事（aga・minoxidil・beard・loh・ashwagandha など）、h2 に id の無い記事（aga 6か所、hair-scalp-care・winter-vitamin-d・hair-tonic-review・minoxidil の FAQ の h3 など） | 目次が無い。id の無い h2 にはリンクできない（ページ内リンク・他記事からの節リンク・検索結果の「ページ内の該当箇所」に使えない） | 「先に要点」の下に、h2 の一覧の目次を入れる。id の無い h2 には id を付ける（既存の id は変えない。他記事からリンクされているため） | BS: `<!-- toc:start/end -->` を `id="summary-top"` の節の後（無ければ最初の h2 の前）に入れ、id のある h2 から目次を作る。id の無い h2 は警告を出す（id は人が付ける） |
| T-10 | 中 | 全ページ | 表示速度: Google Fonts の CSS が描画を止める読み込み方で、和文の Zen Kaku Gothic New を本文にも3ウェイト（400・700・900）使っている。和文の Web フォントは容量が大きく、`display=swap` で文字の差し替え（ちらつき・レイアウトのずれ）が起きやすい | 本文（`--font-body`）は端末のフォント（ヒラギノ・游ゴシック・メイリオ）にし、Zen Kaku Gothic New は見出しの 700・900 だけにする。Archivo は使っている太さだけ残す。オーナーの了承が要る見た目の変更なので、経営企画が判断する | 一部 BS: head の Google Fonts の URL は about.html の head から全ページに広がる作りではないので、全ページの置き換えを BS に足すことはできる |
| T-11 | 中（確認が要る） | 記事 20本（A8 のリンクがあるのは protein-guide・mens-bb-cream の2本だけ） | `//statics.a8.net/a8link/a8linkmgr.js` を、商品リンクの無い記事にも同期読み込み（async なし）で入れている。`</body>` の直前なので最初の描画は止めないが、外部への通信が1つ増え、読み込みの完了が遅れる | このスクリプトが何に使われているか（A8 のリンクマネージャーの自動変換を使っているか）をオーナーに確認する。使っていなければ、A8 のリンクがある記事だけに残す。残す記事も、A8 の手順が許す範囲で読み込み方を見直す | BS: 記事に `a8.net` へのリンクがあるかどうかで、このスクリプトを入れる・外すことはできる（確認の後） |
| T-12 | 中〜低 | 全ページ（34ファイルに `href="index.html"` または `href="../index.html"`） | トップの正規 URL は `/`（canonical・sitemap）なのに、ロゴのリンクは `index.html` を指している。canonical でまとまるので大きな問題ではないが、内部リンクは正規 URL にそろえる方がよい | ロゴ・パンくずのトップへのリンクを `./`（記事・カテゴリは `../`）にする | BS: 全ページを回すループで `href="index.html"`→`href="./"`、`href="../index.html"`→`href="../"` に置き換える |
| T-13 | 低 | 全記事（JSON-LD） | Article の `author` が名前だけ（url が無い）。`image` は全記事で共通の `images/og.png`。og:image の幅・高さ・代替テキストが無い | `author` に `"url": SITE + "about.html"` を足す。トップの JSON-LD に Organization（name・url・logo）を足す。`og:image:width`・`og:image:height`・`og:image:alt` を足す。記事ごとの OG 画像（PNG。SVG は SNS で使えない）は後回しでよい | BS: `seo_block()` に足すだけ |
| T-14 | 低 | skincare-antiaging（2か所）、mens-bb-cream（2か所） | リンクの文言が「別記事」だけ | 「レチノール・アダパレン・トレチノインの違い」「化粧品と医薬部外品の見分け方」のように、リンク先の中身が分かる文言にする | なし（編集部。0036 の文体リライトのときに一緒に） |
| T-15 | 低 | `index.html` | (a) 「最新記事」6本だけで、22本のうち古い主力記事（skincare・protein・sleep・aga など）にトップから行くにはカテゴリを経由するしかない。(b) 「このサイトについて」の「分野」がスキンケア・ヘアケア・ボディ・睡眠・季節の栄養のままで、オーラルケア・ヒゲ・脱毛が無い。meta description も「肌・髪・体・睡眠」だけ。(c) カテゴリの見出しが英語の「Categories」だけ。(d) `tools.html` はトップ・ヘッダー・フッターから行けない（記事3本からだけ） | (a) `site_data.json` に `featured`（経営企画が選ぶ4〜6本）を足し、「はじめに読む記事」の節を出す。(b) 分野と description を6カテゴリに合わせる。(c) `<h2>` を「カテゴリ」にし、英語は飾りの span に残す。(d) フッターに「運営者が使っている道具」を足す | BS: (a)(c) はトップを作る部分に足す。(b)(d) は手で（フッターは BS の footer を about.html から取る作りなので about.html を直せばカテゴリページにも広がる） |
| T-16 | 低 | aga-selfcare-vs-clinic | title の最後の【30代から】が h1 に無い（title と h1 の違いはここだけ） | どちらかにそろえる（付録A の案では title 側に残す） | なし |
| T-17 | 低 | サイト全体 | `404.html` が無い（GitHub Pages の既定の画面になり、サイトに戻る道が無い） | トップとカテゴリへのリンクだけの `404.html` を置く。sitemap には入れない | BS: about.html の head・header・footer から作れる |
| T-18 | 低（予防） | `build_site.py`、0034 | git で管理されている `articles/*.html` が `site_data.json` に無いと、`ART[...]` で KeyError になって止まる（理由が分かりにくい）。いま sleep-support の関連記事に、まだ site_data に無い `blue-light-glasses.html` へのリンクがある（0034 の作業中の変更） | 0034 は記事・site_data・sleep-support のリンクを同じ PR でマージする。BS には「site_data に無い記事」をはっきり知らせるチェックを足す | BS: `seo_block()` の前に、記事ファイルと site_data の slug の差を調べて、分かりやすいメッセージで止める |
| T-19 | 低 | `sitemap.xml` | トップ・about・disclosure・privacy に lastmod が無い。ほかは site_data の `updated` と一致していて問題ない | トップの lastmod を「全記事の更新日の最大」にする。固定ページは `pages` に `updated` を足せば入る（今の仕組みで足りる） | BS: トップの行だけ変える |

## 3. 抜き取り確認で問題が無かったもの

- **canonical**: 34ページすべてに、自分自身の絶対 URL の canonical がある（トップは `/`）。
- **OGP・Twitter カード**: 34ページすべてにある。og:title・og:description は title・meta description と一致。
- **JSON-LD**: 記事22本に Article と BreadcrumbList の2つ、トップに WebSite。`datePublished`・`dateModified` は site_data と一致（protein-guide で突き合わせた: 2026-09-13／2026-09-29）。カテゴリが null の mens-selfcare-start は、パンくずが2段になる分岐が正しく働いている（コードで確認）。
- **sitemap.xml**: トップ、固定ページ3つ、tools、カテゴリ6、記事22のすべてがある。記事とカテゴリの lastmod は site_data から正しく作られている。
- **見出しの順序（記事）**: 22本とも h1 は1つで、h2 より先に h3 が来るところ・段が飛ぶところは無い。
- **ページ内リンク・節リンク**: 記事どうしの `#id` つきリンク約70本で、リンク先の id がすべてあることを確認した（リンク切れ0）。
- **画像**: サムネイルはすべて `alt=""`（隣に見出しの文字があるので飾りの画像として正しい）・`width`・`height`・`loading="lazy"` がある。トップのヒーロー画像は lazy なし（最初に見える位置なので正しい）。記事の本文には内容のある画像が無い（A8 の1×1の計測画像だけ。`alt=""` あり）。
- **広告リンク**: 商品リンク（protein-guide 2本、mens-bb-cream 1本、tools 1本）はすべて `rel="sponsored nofollow"`。
- **h1 と title**: 記事22本のうち21本で完全に一致（違うのは aga の【30代から】だけ、T-16）。
- **title にサイト名が無い（記事）**: Google は検索結果にサイト名を別に出すので、今のままでよい。
- **robots.txt**: `org/seo/README.md` に書いてあるとおり、プロジェクトのサブパスに置いているので効かない。sitemap は Search Console から送信済みなので、手を入れる必要は無い。
- **社内資料の配信**: `_config.yml` で org・scripts・keywords.csv などを除外している。`.sources/` はドットで始まるので Jekyll が配信しない（`.nojekyll` は無い）。

## 4. 構造化データ: FAQPage・HowTo は入れない

- 当サイトの記事には、ページで見える「よくある疑問」の節がある（aga・minoxidil・hair-tonic-review・body-odor-sweat・winter-vitamin-d・hair-scalp-care）。
- Google は **2023年8月** から、FAQ のリッチリザルトを「よく知られた、権威のある政府・健康分野のサイト」に限って表示している（Google 検索セントラル ブログ 2023-08-08「Changes to HowTo and FAQ rich results」）。開設1か月の個人運営のアフィリエイトサイトが対象になる見込みは低い。HowTo のリッチリザルトは同じ発表で表示されなくなった。
- マークアップを足しても検索結果の見た目は変わらない見込みで、本文を直すたびに JSON-LD もそろえる手間（ずれると「ページに無い内容のマークアップ」になる）だけが増える。**入れない**ことを勧める。
- ページで見える Q&A の節は、読者にも、検索の「ページ内の該当箇所へのリンク」にも役立つので残す。T-9 の id 付けで節に直接リンクできるようにする。
- 実施する前に、Google の構造化データの資料（FAQPage）で今の対象の条件をもう一度確かめること（この判断は 2026-10-09 時点の分析部の理解による。ネットでの再確認はしていない）。
- Article・BreadcrumbList は今の形でよい（T-5・T-13 の小さな改善だけ）。`MedicalWebPage` などの医療系の型は、監修の無いサイトでは使わない（誤解を招く）。

## 5. カニバリ（同じ検索語を複数の記事が取り合う）の判断

詳しくは付録D。今の実績データが無いので「起きている」とは断定しない。**起きうる組み合わせ**と、どちらを本命にするかの割り当てだけを決めておく。

| 検索語の群 | 取り合いうる記事 | 本命 | もう一方の扱い |
|---|---|---|---|
| 育毛剤・発毛剤の区分の違い | hair-scalp-care（#categories）、aga-selfcare-vs-clinic（区分の比較表）、hair-tonic-review（#category） | hair-scalp-care | aga は「受診か市販薬か」、hair-tonic は「使っていて変わらないとき」に絞り、区分の説明は短くして本命へリンク（すでに一部リンクあり） |
| ミノキシジル内服 | minoxidil-finasteride-guideline、aga-selfcare-vs-clinic（推奨度Dの段落） | minoxidil | aga の該当段落から minoxidil へリンクする（今は無い。T-2） |
| 男のスキンケアの始め方 | skincare-antiaging、mens-selfcare-start | skincare-antiaging | mens-selfcare-start は「何から始めるか（分野全体）」。keywords.csv の「30代 男性 スキンケア 始め方」は skincare、「メンズ 美容 何から」は mens-selfcare-start のまま |
| レチノールの使い方・区分 | skincare-antiaging、retinoids-japan-vs-overseas | retinoids | keywords.csv の「レチノール 男性 使い方」を retinoids に移す |
| カフェインと睡眠 | sleep-support（#caffeine-alcohol）、caffeine-limits | caffeine-limits（量）、sleep-support（睡眠全体） | sleep-support の節から caffeine-limits へのリンクはある。問題なし |
| 疲れ・やる気が出ない | fatigue-recovery、loh-testosterone | fatigue-recovery | loh は「男性更年期 検査・何科」に絞る（すでにそうなっている） |

## 6. title・meta 以外で、0036 の文体リライトと一緒にやると効率がよいもの

- T-14（「別記事」のリンク文言）、T-9（id の無い h2）、T-2（手で足す内部リンク）は、編集部が既存記事を数本ずつリライトするときに、同じ差分でやるのがよい。
- リライトで本文を変えたら、`site_data.json` の `updated` を更新する（`org/seo/README.md` の「更新日の運用」）。title だけ、内部リンクだけの変更で `updated` を動かすかどうかは、経営企画が決める（README は「体裁だけの変更では更新しない」）。

## 7. 判断に必要なデータ（オーナーへの依頼の案。経営企画が `org/owner-inbox.md` に転記）

このファイル以外を編集しない指示のため、ここに案として書く。

1. **Search Console「ページ」**: 登録済みのページ数と、未登録のページと理由（特に「クロール済み - インデックス未登録」「検出 - インデックス未登録」）。スクショでよい。
2. **サイトマップの状態**（D13 の続き）: 「成功しました」になったか、検出された URL の数（今は35あるはず）。
3. **検索パフォーマンス（過去28日）**: 合計クリック・表示回数・平均 CTR・平均掲載順位、ページ別の上位10、クエリ別の上位10。表示回数が付いていなければ「0」とそのまま教えてほしい（それ自体が判断材料になる）。
4. **A8 のリンクマネージャー（a8linkmgr.js）を使っているか**（T-11）。使っているなら、何のための設定か。
5. **（任意）PageSpeed Insights** の結果（トップと記事1本、スマホ）。https://pagespeed.web.dev/ に URL を入れるだけで、ログインは要らない。T-10 のフォントの判断に使う。

データが届いたら、分析部が「表示回数は多いが CTR が低い／11〜20位／クリックはあるが成約しない」を洗い出して、`org/kpi/report-2026-10.md` に書く。それまでは、付録A・B の title・meta の案は「実績の裏付けの無い、作りからの改善」として扱う。

---

## 付録A: title の一覧（全角換算。半角英数字は0.5で数えた。手で数えたので±1字の誤差がありうる）

「主KW」は `keywords.csv` の優先度の高い語（無い記事は記事の主題）。位置は title の何字目から始まるか。案は、主な検索語を先頭に置き、記事の本文にある内容だけで書いたもの（効能の言い切り・「必ず」「最強」などの煽りは使っていない）。採用するかどうかは編集部が決め、レビュー部が確認する。

| 記事 | 今の長さ | 主KW と位置 | h1 と同じか | 判定 | title の案（長さ） |
|---|---|---|---|---|---|
| sleep-support | 64.5 | 「睡眠」1字目。「睡眠の質」（高）は無い | 同じ | 長い・語がずれている | 睡眠の質が気になったら｜厚労省「睡眠ガイド2023」の目安と受診の目安（約34） |
| minoxidil-finasteride-guideline | 59 | 「ミノキシジル」1字目 | 同じ | 長い | ミノキシジル内服・外用フィナステリドの位置づけ｜日本のガイドラインと海外の安全性情報（約42） |
| ashwagandha-japan | 58 | 「アシュワガンダ」1字目 | 同じ | 長い | アシュワガンダはなぜ日本で規制されているのか｜「専ら医薬品」の理由と海外の評価（約39） |
| retinoids-japan-vs-overseas | 57 | 「レチノール アダパレン 違い」1字目 | 同じ | 長い | レチノール・アダパレン・トレチノインの違い｜日米の区分を公的資料で整理（約35） |
| hair-damage-care | 52 | 「髪 パサつき」1字目 | 同じ | 長い | 男の髪のパサつき・傷みの原因と手入れ｜洗い流さないトリートメントの使い方（約36） |
| body-odor-sweat | 52 | 「体臭・汗」1字目 | 同じ | 長い | 体臭・汗が気になり始めたら｜においの原因と毎日の手入れ、皮膚科に相談する目安（約38） |
| caffeine-limits | 48.5 | 「カフェイン 1日」1字目 | 同じ | やや長い | カフェインは1日どこまで？｜「400mg」の条件の違いと飲み物の含有量、寝る前の目安（約39） |
| fatigue-recovery | 47 | 「疲れが取れない 原因」（高）が無い | 同じ | 語がずれている | 疲れが取れない・だるさが続くとき｜考えられる原因と受診の目安（約30） |
| mens-selfcare-start | 47 | 「メンズ 美容 何から」1字目 | 同じ | やや長い | メンズ美容、何から始める？30代からのセルフケア｜分野別にまず確かめること（約36） |
| whitening-japan-vs-overseas | 46 | 「ホワイトニング」1字目。「セルフ」は42字目 | 同じ | 語の位置 | ホワイトニング、歯科とセルフサロンの違い｜海外（EU・英米）と日本の制度（約35） |
| loh-testosterone | 44.5 | 「男性更年期 検査」1字目、「何科」17字目 | 同じ | 可 | 今のままでよい |
| beard-hair-removal | 44 | 「ヒゲ脱毛」1字目 | 同じ | 可（短くできる） | ヒゲ脱毛、医療・エステ・家庭用の違い｜回数・リスク・契約の確認点（約32） |
| aga-selfcare-vs-clinic | 43.5 | 「AGA 市販薬 クリニック 違い」1字目 | 【30代から】だけ違う | 可 | AGAのセルフケアとクリニックの違い｜市販薬・育毛剤・受診の目安【30代から】（約36。h1 は【】を除いてそろえる） |
| hair-scalp-care | 43 | 「抜け毛 増えた 30代 男性」1字目 | 同じ | 可 | 今のままでよい |
| protein-guide | 42.5 | 「ホエイ ソイ 違い」1字目 | 同じ | 可（短くできる） | ホエイとソイの違いとプロテインの選び方｜1日の量・腎臓の注意・表示の見方（約36） |
| hair-tonic-review | 42.5 | 「育毛剤 効果がない」1字目 | 同じ | 可 | 今のままでよい |
| skincare-antiaging | 42 | 「スキンケア」8字目。「メンズ」は無い | 同じ | 可（短くできる） | 30代からの男のスキンケアの基本｜洗顔・保湿・日焼け止めと成分の見方（約33） |
| mens-bb-cream | 42 | 「メンズBBクリーム」1字目 | 同じ | 後半が検索語でない | メンズBBクリームを選ぶ前に｜表示の確かめ方・落とし方・肌に合わないとき（約35） |
| winter-shaving-skin | 41 | 「ひげ剃り 肌荒れ」1字目。「カミソリ負け」が無い | 同じ | 語の追加 | 冬のひげ剃りと肌荒れ（カミソリ負け）｜剃り方・刃の交換・皮膚科の目安（約33。本文で「カミソリ負け」という呼び名と、記事で扱う症状の対応を1文で書くことが条件） |
| oral-care-basics | 39 | 「口臭ケア」1字目 | 同じ | 可 | 今のままでよい |
| winter-vitamin-d | 37 | 「ビタミンD 冬 不足」1字目 | 同じ | 可 | 今のままでよい |
| index.html | 22.5 | サイト名が先頭 | h1 は「30代からの、根拠で選ぶセルフケア」 | 可 | 今のままでよい（トップはサイト名の検索が主） |
| category/*.html | 15〜18 | 「◯◯の記事一覧」 | h1 はカテゴリ名だけ | 何が読めるか分からない | T-6 の seo_title（例: ヘア・AGAの記事一覧｜抜け毛・育毛剤・受診の目安 \| 男の養生帖） |
| tools.html | 34.5 | — | 同じ（サイト名を除く） | 可 | 今のままでよい |
| about / disclosure / privacy | 11〜22 | — | 同じ | 可 | 今のままでよい |

## 付録B: meta description（字数は目で数えた概数）

| ページ | 概数 | 所見 |
|---|---|---|
| caffeine-limits | 約165 | 長い。前半が機関名の羅列。案の方向: 「カフェインは1日どこまでか。米国・欧州・カナダが示す400mgの条件の違いと、日本の扱い、飲み物の含有量、寝る何時間前までかを公的資料で整理。」から始める |
| melatonin-japan-vs-us | 約155 | 長い。最初の文はよい。後半（時差ぼけ・個人輸入）を短くする |
| sleep-support | 約150 | 長い。「睡眠の質を上げるには何から見直すか」で始まっているのはよい（ただし title 側に「質」が無い、T-4） |
| aga-selfcare-vs-clinic | 約140 | 「30代以上の方へ」から始まり、答えの方向（判断の目安）が後ろ。最後の文は削れる |
| whitening-japan-vs-overseas | 約140 | 「歯科とセルフサロンの違い」を前に出す |
| body-odor-sweat | 約135 | やや長い |
| hair-tonic-review | 約135 | やや長い。最初の文はよい |
| winter-vitamin-d | 約135 | 最初の文で事実を言っている。手本 |
| hair-damage-care | 約130 | やや長い |
| minoxidil-finasteride-guideline | 約130 | やや長い |
| retinoids-japan-vs-overseas | 約125 | 最初の文で答えを言っている。手本 |
| loh-testosterone・hair-scalp-care・winter-shaving-skin | 約125 | 可 |
| skincare-antiaging・mens-selfcare-start・beard-hair-removal・ashwagandha-japan | 約115〜120 | 可 |
| fatigue-recovery・protein-guide | 約105 | 可 |
| mens-bb-cream・oral-care-basics | 約90〜95 | 可 |
| index.html | 約85 | 「肌・髪・体・睡眠」に口・ヒゲが無い（T-15） |
| category/*.html | 約50〜100 | リードと同じ文。hair は「…記事と、…記事です」で読みにくい（T-6） |
| about / disclosure / privacy / tools | 約55〜80 | 可 |

## 付録C: 記事どうしの内部リンク（記事本文からのリンク。カテゴリページ・トップからのものは除く）

| 記事 | リンクしている記事の数（重複なし） | リンク元 |
|---|---|---|
| minoxidil-finasteride-guideline | **0** | なし |
| ashwagandha-japan | 1 | loh |
| whitening-japan-vs-overseas | 1 | oral-care-basics |
| melatonin-japan-vs-us | 2 | sleep-support、caffeine-limits |
| body-odor-sweat | 2 | oral-care-basics、mens-selfcare-start |
| caffeine-limits | 3 | sleep-support、fatigue-recovery、melatonin |
| hair-damage-care | 3 | hair-scalp-care、hair-tonic-review、mens-selfcare-start |
| protein-guide | 3 | winter-vitamin-d、fatigue-recovery、mens-selfcare-start |
| retinoids-japan-vs-overseas | 3 | skincare-antiaging、mens-selfcare-start、oral-care-basics |
| mens-bb-cream | 3 | beard-hair-removal、winter-shaving-skin、mens-selfcare-start |
| winter-shaving-skin | 3 | skincare-antiaging、beard-hair-removal、mens-selfcare-start |
| hair-tonic-review | 4 | aga、minoxidil、hair-scalp-care、mens-selfcare-start |
| oral-care-basics | 4 | skincare-antiaging、whitening、body-odor-sweat、mens-selfcare-start |
| mens-selfcare-start | 4 | body-odor-sweat、fatigue-recovery、loh、sleep-support（ほかにトップのヒーローから常にリンクあり） |
| beard-hair-removal | 4 | skincare-antiaging、mens-bb-cream、winter-shaving-skin、mens-selfcare-start |
| aga-selfcare-vs-clinic | 4 | hair-scalp-care、hair-tonic-review、minoxidil、mens-selfcare-start |
| winter-vitamin-d | 5 | skincare-antiaging、protein-guide、fatigue-recovery、sleep-support、mens-selfcare-start |
| loh-testosterone | 6 | fatigue-recovery、sleep-support、melatonin、ashwagandha、mens-selfcare-start ほか |
| hair-scalp-care・skincare-antiaging・sleep-support・fatigue-recovery | 5〜7 | 多い |

関連記事（「関連記事」の節）の本数が1本だけ: protein-guide、winter-vitamin-d、whitening-japan-vs-overseas、retinoids-japan-vs-overseas。

## 付録D: keywords.csv の割り当ての直し方（案）

| 直すこと | 行・記事 | 案 |
|---|---|---|
| 割り当て先の誤り | 「レチノール 男性 使い方」→ skincare-antiaging | retinoids-japan-vs-overseas に移す |
| 割り当て先の誤り | 「サプリ 飲み合わせ 注意」→ disclosure.html | 答える記事が無い。「未対応（候補）」にする。部分的に答えているのは winter-vitamin-d（相互作用の注意）・fatigue-recovery |
| 割り当て先の誤り | 「機能性表示食品 とは」→ about.html | fatigue-recovery（#ffc）・sleep-support に移す |
| 割り当て先の誤り | 「男性 グルーミング とは」→ about.html、「デキる男 身だしなみ 習慣」→ index.html | mens-selfcare-start に移すか「対象外」にする（「デキる男」は当サイトの言葉の基準に合うかレビュー部に確認） |
| 方針と意図が合わない | 「メンズ スキンケア おすすめ」「プロテイン おすすめ 社会人」「ソイプロテイン おすすめ」「スカルプシャンプー メンズ おすすめ」「髭剃り後 保湿 おすすめ」「育毛剤 メンズ 比較」 | 優先度を「対象外（順位をつけない方針）」にする。Search Console のクエリに出てきたら、C02・#27 の入口のサインとして見る（`org/seo/README.md` 月次チェック4） |
| 行が無い記事 | 12記事（T-7） | 各記事の `01-research.md`・`03-channel.md` の主キーワードを1〜3行ずつ転記する（分析部が次の月次で行う。転記だけなので、新しい判断はしない） |
| 書き方のばらつき | 対応記事の列が `articles/x.html` と `x.html`、カテゴリ名が site と違う | 対応記事は slug だけ、カテゴリは site_data の id（skin・hair・body・rest・oral・grooming・null）にそろえる |

## 前工程への質問・異議

- 経営企画へ: T-10（本文のフォントを端末のフォントにする）は見た目が変わるため、オーナーに見せてから決めることを勧める。
- 経営企画へ: T-11 の a8linkmgr.js は、収益に関係する可能性があるので、オーナーの確認（7章の4）を待ってから外す。
- 0034 の担当へ: sleep-support に、blue-light-glasses へのリンクがすでにある。0034 の記事と site_data の追加と同じ PR でマージしないと、リンク切れになる（T-18）。

## 前工程の検証

- `org/seo/README.md` の「技術面（自動で入るもの）」の記載（全ページに canonical・OGP・Twitter カード、記事に Article・BreadcrumbList、トップに WebSite、sitemap に記事とカテゴリの lastmod）を、34ページの grep と protein-guide・index・about・category/hair の通読で確かめた。**記載どおり**。ただし README に書かれていない欠け（見えるパンくず・記事の見える日付が無い）を T-1・T-5 に挙げた。
- 00-brief のスコープ3にある「Search Console の状況（オーナーのスクショ待ち）」: `org/kpi/` にデータは無く、`owner-inbox.md` の D13（サイトマップの状態の再確認）も未完了。実績データが無いことを前提に書いた（0章・7章）。
