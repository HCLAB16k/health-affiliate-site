# 05 レビュー: SEO の担当と技術面のセットアップ（0015）

- 担当: compliance-reviewer
- 審査対象: `git diff origin/main`（コミット fe517f1）。全HTMLの head の `<!-- seo:start -->〜<!-- seo:end -->`、about・disclosure・privacy の meta description、`sitemap.xml`、`images/og.png`、`scripts/build_site.py`、`org/seo/README.md`、D0012、`analyst.md`、`CLAUDE.md` の表1行

## 前工程への質問・異議
- 本案件は 00-brief のみ（01〜04 なし）。異議なし。
- 00-brief の「レビューの観点」に無い変更が差分に含まれている（指摘 #3）。

## 前工程の検証
| 00-brief の主張 | 検証方法 | 結果 |
|---|---|---|
| 記事の本文・title は変更しない | 各HTMLから seo ブロックを取り除いた結果を `origin/main` の同ファイルと文字列比較（python） | 全HTML（記事9・カテゴリ5・index・about・disclosure・privacy）で一致。本文・title・既存 meta description は無変更 |
| 著者は「男の養生帖 編集部」、専門性を示唆する項目なし | 全ページの JSON-LD を `json.loads` し型・キーを確認 | Article 9・BreadcrumbList 9・WebSite 1、すべて妥当な JSON。型は Article / BreadcrumbList / WebSite のみ。MedicalWebPage・reviewedBy・Person・資格・about/mentions 無し。author は Organization「男の養生帖 編集部」で about.html の「運営者：男の養生帖 編集部」「医師・薬剤師などの資格者による監修は受けていません」と整合 |
| sitemap・canonical の URL が正しい | canonical のパスが実在ファイルか、canonical と og:url の一致、canonical 重複の有無を python で確認 | 全ページで実在、canonical と og:url 一致、重複なし。sitemap は index・about・disclosure・privacy・カテゴリ5・記事9の計18件で、`googlef8290cdc0cd76b31.html` は含まれず、当該ファイルは無変更（seo ブロックも無し） |
| og:title/description が title/meta と一致 | python で全ページ照合 | og:title は title と、og:description は meta description と全ページで一致 |
| OG 画像が商品・効能を示唆しない | `images/og.png` を目視 | 黄背景にロシアンブルーと黒猫の2匹、文字なし。商品・体の変化・効能の示唆なし。D0011 のキャラクター規定（本文・商品枠の近くに置かない）は、共有カードの画像でありページ内に置かないため抵触しないと判断 |
| Google の robots.txt の仕様（README の記述の照合） | WebFetch: developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt | 「robots.txt はサイトホストのルートに置く。サブディレクトリでは効かない」。README の説明の前半は正しいが、指摘 #2 のとおり不足がある |

## 経営判断ログの遵守確認
| 判断（00-brief の行） | 遵守 / 不遵守 | 該当箇所 |
|---|---|---|
| Article（著者は Organization）と BreadcrumbList のみ。MedicalWebPage・Person・reviewedBy は使わない（トップは WebSite） | 遵守 | 全ページの JSON-LD（上記） |

## 持ち越し論点の最終判断
なし。

## 第1回審査（2026-09-28）

**判定: REVISE**

法令・捏造・広告主レギュレーションの問題は無い。公開を止める理由は、実態と合わない記述（dateModified、README の robots.txt）と、スコープ外ファイルの混入の3点。いずれも軽い修正で直る。

### 指摘
| # | 観点 | 該当箇所（引用） | 問題 | 修正案 | 差し戻し先 | 重大度（必須/推奨） | 対応（修正側が記入） |
|---|---|---|---|---|---|---|---|
| 1 | 構造化データの実態一致 | 5記事の JSON-LD `"dateModified"` と sitemap の `<lastmod>`。`aga-selfcare-vs-clinic`（09-27）、`protein-guide`（09-13）、`hair-scalp-care`（09-13）、`sleep-support`（09-13）、`fatigue-recovery`（09-13）が「公開日＝更新日」になっている | git 履歴では公開日より後に本文を変えた記録がある。aga は 0008 で OTC 価格表を追加（09-28）、protein は 0007 で商品枠を復活・レビュー修正（09-28）、hair は 0003 で全面書き換え（09-27）、sleep・fatigue は 0002 レビュー修正（09-27）。`site_data.json` の `updated` が入っているのは skincare と oral-care だけで、dateModified が実態より古い。なお記事ページに更新日の表示は無く、影響は構造化データと sitemap に限る。過小申告のため誤認の害は小さい | 各記事の本文を実際に変えた最終日を編集部が確認し、`scripts/site_data.json` の `updated` に入れて build を再実行する（git の日付は目安。本文変更を伴わない体裁だけのコミットは含めない）。あわせて `org/seo/README.md` 19行目「記事を更新したら `updated` を入れる」を、記事の完了条件（リライト案件のチェック）に入れることを経営企画が検討する | editor（`updated` の確認）。build は経営企画 | 推奨（公開後の修正でも可。ただし dateModified を載せる以上、直すのが望ましい） | |
| 2 | README の記述の正確さ | `org/seo/README.md` 18行目「`robots.txt` は GitHub Pages のプロジェクトサイトではドメイン直下に置けないため、Search Console から sitemap を送信済み。」 | 事実との差が2点ある。①リポジトリ直下には `robots.txt`（`Allow: /` と Sitemap 行）が実在し、`/health-affiliate-site/robots.txt` で配信される。読み手が「無い」と誤解する。②Google はホスト直下（`https://hclab16k.github.io/robots.txt`）だけを読むため、この robots.txt は効かない（Google 公式で確認）。この点が書かれていない。「送信済み」は owner-inbox（2026-09-28 の行）で確認できるが、サイトマップの状態が「成功しました」かはこのレビューでは確認できていない | 例: 「`robots.txt` はリポジトリ直下にあるが、GitHub Pages のプロジェクトサイトではホストのルートに置けず、Google には読まれない（クロール制御には使えない）。sitemap は Search Console から送信済み（送信日は owner-inbox。状態は月次チェック1で確認）」。断定しすぎない書き方にする | 経営企画（README の書き手）。編集部ではない | 必須 | |
| 3 | 差分のスコープ | `icon-real.svg`、`real-black.svg`、`real-pair.svg`（リポジトリ直下、コミット fe517f1 に含まれる）、`org/owner-inbox.md` の E1 への追記 | 00-brief・依頼の対象一覧に無い。3つの SVG は `org/brand/cats_real.py` が og.png 用に出力した中間生成物とみられ、リポジトリ直下は `_config.yml` の除外に入っていないため**サイトに配信される**。使われている箇所は無い（参照なし）。owner-inbox の追記は D0012 に沿う内容で問題なし | SVG 3点はコミットから外す（または `org/brand/` に移す）。owner-inbox の追記は 00-brief の内容に一行加えて明記する | 経営企画 | 必須（意図しない公開物） | |
| 4 | README の実行可能性 | `org/seo/README.md` 26行目「出たら C02・#27 の入口のサイン」 | 「C02」「#27」は `org/pipeline/candidates.md` と 0012 の書類にあるが、README だけ読むと意味が分からない。実行する人（分析部・オーナー）が迷う | 「C02（candidates.md）・backlog #27（セール時の紹介ページ）」と参照先を書く | 経営企画 | 推奨 | |
| 5 | README の断定 | `org/seo/README.md` 34行目「公開から2週間はインデックスの確認、1〜2か月で表示回数が付くか、3か月で…」 | 「目安」の位置づけは 30行目の見出しにあり、35行目でデータ量の注意も書かれていて、おおむね適切。ただし期間の根拠は書かれていない | 「経営企画の目安（根拠となる公式の基準は無い）」の一言を添えると、断定に読まれない | 経営企画 | 推奨 | |

指摘 #1〜#5 以外の確認結果（問題なし）:
- seo ブロックは冪等（再実行時に正規表現で置換される）。og:title・description は `html.escape` 済みで、JSON-LD 側は `unescape` して二重エスケープを防いでいる。
- about・disclosure・privacy の追加 meta description は、本文の見出し（運営者・記事の作り方・広告・お問い合わせ、広告表記・掲載基準・免責、個人情報・アクセス解析・Web フォント・アフィリエイト）と一致し、効能表現・最大級表現・断定を含まない。about の「AIの利用、監修なし」は about.html 66〜67行と一致。
- index の og:description「学会のガイドラインや公的機関の資料にできるだけあたりながら、中立的に整理する」は、index の既存 meta description と同一。og に独自の誇張は無い。
- BreadcrumbList の中間項目（カテゴリ名・URL）は `category/<id>.html` で実在。
- `CLAUDE.md` の表の変更（分析部に「SEO の責任者、D0012」）は D0012・analyst.md と整合。`analyst.md` の追記は、抜き取り確認を求めるにとどまり、他部署の権限を侵さない。
- publisher.logo は `icon-512.png`（実在）。

### 出典照合の記録
| 記事中の記述 | 出典URL | 照合結果 |
|---|---|---|
| robots.txt はホストのルートに置く。サブディレクトリでは効かない（README 18行目の前提） | https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt | 一致（指摘 #2 のとおり、README に不足あり） |
| dateModified・lastmod が実態と合うか | `git log -- articles/<slug>.html` と `scripts/site_data.json` の `updated` | 5記事で不一致（指摘 #1） |
| 記事・本文・title・既存 meta description の無変更 | `git show origin/main:<file>` との比較（python） | 全HTMLで一致 |

本案件は記事の医学的記述・数値・価格を変えないため、WebFetch での出典照合は上記1件（robots.txt の仕様）。記事本体の出典は過去案件のレビューで審査済み。

### チェックリスト結果
- 薬機法: OK（効能表現なし。JSON-LD に医療の型・監修の示唆なし）
- 景品表示法: OK
- ステマ規制（PR表記）: OK（`pr-badge`・`disclaimer` を含む本文は無変更）
- 医療広告ガイドライン（該当時）: 対象外（クリニック名・料金の追加なし。og・meta description にクリニック名なし）
- 捏造なし: OK
- 広告主レギュレーション: 対象外（商品・リンクの変更なし。rel 属性も無変更）
- 技術（disclaimer・rel・meta・sitemap・内部リンク）: 一部NG（sitemap の lastmod が5記事で実態より古い、配信対象の SVG 3点が混入）

### 読者目線の講評
読者に見える変更は共有時のカード表示だけで、本文には影響しない。OG 画像は猫の絵のみで、記事の内容を語らず、押し売り感も無い。一方、共有カードで記事ごとに画像が同じになるため、クリックされやすさの面では弱い。今後の改善候補（各記事のサムネイルを流用する等）だが、サムネイルに商品・体の変化を描かないルール（チェックリスト6章）を守る前提で、今回は任意。

### 組織への提案（チェックリスト・書式の不足）
- チェックリスト7章に「`site_data.json` の `updated` を、本文を変えた記事で更新する（構造化データ・sitemap に出る）」を追加する提案。
- チェックリスト7章に「リポジトリ直下に置く画像・SVG は配信される。中間生成物は `org/` 配下に置く」を追加する提案。
- 構造化データは今後も Article（Organization）・BreadcrumbList・WebSite に限り、MedicalWebPage・reviewedBy・Person・資格を入れない、を D0012 か checklist に明記すると、後の変更時にレビューの基準になる。

### 再審査の条件
- #2・#3 が必須。#1・#4・#5 は推奨（#1 は対応すれば sitemap の lastmod も直る。対応しない場合は理由を「対応」欄に書く）。
- 修正後は seo ブロックが再生成されるため、差分が head と sitemap に限られることを再確認する。

<!-- 再審査時は「## 第2回審査」として下に追記する -->
