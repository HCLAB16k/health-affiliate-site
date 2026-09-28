# 05 レビュー: SEO の担当と技術面のセットアップ（0015）

- 担当: compliance-reviewer
- 審査対象: `git diff origin/main`（コミット fe517f1。第2回は 01f27d8 を含む）。全HTMLの head の `<!-- seo:start -->〜<!-- seo:end -->`、about・disclosure・privacy の meta description、`sitemap.xml`、`images/og.png`、`scripts/build_site.py`、`org/seo/README.md`、D0012、`analyst.md`、`CLAUDE.md` の表1行

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
| Google の robots.txt の仕様（README の記述の照合） | WebFetch: developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt | 「robots.txt はサイトホストのルートに置く。サブディレクトリでは効かない」。README の説明の前半は正しいが、指摘 #2 のとおり不足があった |

## 経営判断ログの遵守確認
| 判断（00-brief の行） | 遵守 / 不遵守 | 該当箇所 |
|---|---|---|
| Article（著者は Organization）と BreadcrumbList のみ。MedicalWebPage・Person・reviewedBy は使わない（トップは WebSite） | 遵守 | 全ページの JSON-LD（上記。第2回でも再確認） |

## 持ち越し論点の最終判断
なし。

## 第1回審査（2026-09-28）

**判定: REVISE**

法令・捏造・広告主レギュレーションの問題は無い。公開を止める理由は、実態と合わない記述（dateModified、README の robots.txt）と、スコープ外ファイルの混入の3点。いずれも軽い修正で直る。

### 指摘
| # | 観点 | 該当箇所（引用） | 問題 | 修正案 | 差し戻し先 | 重大度（必須/推奨） | 対応（修正側が記入） |
|---|---|---|---|---|---|---|---|
| 1 | 構造化データの実態一致 | 5記事の JSON-LD `"dateModified"` と sitemap の `<lastmod>`。`aga-selfcare-vs-clinic`（09-27）、`protein-guide`（09-13）、`hair-scalp-care`（09-13）、`sleep-support`（09-13）、`fatigue-recovery`（09-13）が「公開日＝更新日」になっている | git 履歴では公開日より後に本文を変えた記録がある。aga は 0008 で OTC 価格表を追加（09-28）、protein は 0007 で商品枠を復活・レビュー修正（09-28）、hair は 0003 で全面書き換え（09-27）、sleep・fatigue は 0002 レビュー修正（09-27）。`site_data.json` の `updated` が入っているのは skincare と oral-care だけで、dateModified が実態より古い。記事ページに更新日の表示は無く、影響は構造化データと sitemap に限る。過小申告のため誤認の害は小さい | 各記事の本文を実際に変えた最終日を編集部が確認し、`scripts/site_data.json` の `updated` に入れて build を再実行する（git の日付は目安。本文変更を伴わない体裁だけのコミットは含めない）。あわせて `org/seo/README.md` 19行目「記事を更新したら `updated` を入れる」を、記事の完了条件に入れることを経営企画が検討する | editor（`updated` の確認）。build は経営企画 | 推奨 | 第2回で確認 |
| 2 | README の記述の正確さ | `org/seo/README.md` 18行目「`robots.txt` は GitHub Pages のプロジェクトサイトではドメイン直下に置けないため、Search Console から sitemap を送信済み。」 | ①リポジトリ直下に `robots.txt`（`Allow: /` と Sitemap 行）が実在し、`/health-affiliate-site/robots.txt` で配信される。読み手が「無い」と誤解する。②Google はホスト直下だけを読むため、この robots.txt は効かない（Google 公式で確認）。この点が書かれていない。「送信済み」は owner-inbox（2026-09-28 の行）で確認できるが、状態が「成功しました」かは確認できていない | 「robots.txt は実在するが Google には読まれず、クロール制御には使えない。sitemap は Search Console から送信済み」の趣旨に直す。断定しすぎない書き方にする | 経営企画 | 必須 | 第2回で確認 |
| 3 | 差分のスコープ | `icon-real.svg`、`real-black.svg`、`real-pair.svg`（リポジトリ直下）、`org/owner-inbox.md` の E1 への追記 | 00-brief・依頼の対象一覧に無い。SVG 3点は `org/brand/cats_real.py` の中間生成物で、リポジトリ直下は `_config.yml` の除外に入っていないためサイトに配信される。参照は無い。owner-inbox の追記は D0012 に沿う内容で問題なし | SVG 3点はコミットから外す（または `org/brand/` に移す）。owner-inbox の追記は 00-brief に明記する | 経営企画 | 必須 | 第2回で確認 |
| 4 | README の実行可能性 | `org/seo/README.md`「出たら C02・#27 の入口のサイン」 | 参照先が README だけでは分からない | 参照先を書く | 経営企画 | 推奨 | 第2回で確認 |
| 5 | README の断定 | 「公開から2週間は…3か月で…」 | 期間の根拠が書かれていない | 「経営企画の目安」と添える | 経営企画 | 推奨 | 第2回で確認 |

### 出典照合の記録
| 記事中の記述 | 出典URL | 照合結果 |
|---|---|---|
| robots.txt はホストのルートに置く。サブディレクトリでは効かない | https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt | 一致 |
| dateModified・lastmod が実態と合うか | `git log -- articles/<slug>.html` と `scripts/site_data.json` の `updated` | 第1回は5記事で不一致（指摘 #1）。第2回で解消 |
| 記事・本文・title・既存 meta description の無変更 | `git show origin/main:<file>` との比較（python） | 全HTMLで一致（第2回の許容差分は下記） |

本案件は記事の医学的記述・数値・価格を変えないため、WebFetch での出典照合は robots.txt の仕様1件。記事本体の出典は過去案件のレビューで審査済み。

### チェックリスト結果（第1回）
- 薬機法: OK
- 景品表示法: OK
- ステマ規制（PR表記）: OK（`pr-badge`・`disclaimer` を含む本文は無変更）
- 医療広告ガイドライン（該当時）: 対象外
- 捏造なし: OK
- 広告主レギュレーション: 対象外
- 技術: 一部NG（lastmod、SVG 混入）

### 読者目線の講評
読者に見える変更は共有時のカード表示だけで、本文には影響しない。OG 画像は猫の絵のみで押し売り感は無い。記事ごとに画像が同じなので、クリックされやすさの面では弱い（今後の改善候補。サムネイルに商品・体の変化を描かないルールは守る）。

### 組織への提案（チェックリスト・書式の不足）
- チェックリスト7章に「本文を変えたら `updated` を更新」「直下の画像・SVG は配信される」を追加。
- 構造化データの型を Article（Organization）・BreadcrumbList・WebSite に限り、MedicalWebPage・reviewedBy・Person・資格を入れない、を D0012 か checklist に明記すると、後の変更のレビュー基準になる。

## 第2回審査（2026-09-28）

- 審査対象: 01f27d8「0015: review fixes」を含む `git diff origin/main`

**判定: PASS**

### 前回指摘の確認
| # | 結果 | 確認方法・内容 |
|---|---|---|
| 2（必須） | 解消 | `org/seo/README.md` 18行目を確認。robots.txt が `/health-affiliate-site/robots.txt` として配信されること、Google が読むのはホスト直下だけでクロール制御には使えないこと、sitemap は送信済みで「成功しました」かは月次チェックで確認する、と書かれている。事実と一致し、断定しすぎていない |
| 3（必須） | 解消 | `ls *.svg`（リポジトリ直下）で該当なし。`git diff origin/main --stat` にも直下の SVG は出ない。`org/brand/cats_real.py` は `HERE`（自身のフォルダ）へ書き出す形に変更。`__main__` ガード付きで、直下には出力されない。`org/brand/` の `icon-real.svg` は D0011 に書かれた既存の原図。owner-inbox の追記は 00-brief で明記された（00-brief は 24行に増加） |
| 1（推奨） | 解消 | `site_data.json` に `updated` を追加（aga 09-28、hair 09-27、protein 09-28、sleep 09-27、fatigue 09-27）。値は第1回に挙げた git 履歴の最終本文変更日と一致。python で 9記事すべてについて、JSON-LD の dateModified と sitemap の lastmod が `updated`（無ければ公開日）と一致することを確認。カテゴリの lastmod も所属記事の最大日と一致（5カテゴリ） |
| 4（推奨） | 解消 | README 26行目に C02（`org/pipeline/candidates.md` のフッ素歯磨き粉の候補）と #27（`org/pipeline/backlog.md` の「セール時の紹介ページ」）を明記。candidates.md の C02 と backlog の #27 の内容を確認して一致 |
| 5（推奨） | 解消 | 見出しに「期間は経営企画の目安で、根拠のある基準ではない」を追記 |

### 第2回で新たに確認した点
- seo ブロックを除いた比較で、`origin/main` と差があるのは index と category/{body, hair, rest, skin}.html の5ページ。差分は、記事カードの日付表示「公開 … / 更新 …」の追記と、index・skin でのカード並び（スキンケア記事を公開日順の位置に戻した）だけ。`scripts/build_site.py` の生成物で、カードの「更新」日は `updated` と一致する。記事本文・title・既存 meta description・pr-badge・disclaimer は無変更。指摘 #1 の対応に伴う許容差分と判断する
- 「最新記事」を公開日順に戻す変更（build_site.py の sort）は、SEO の要件に影響しない。sitemap の記事順も公開日順で問題なし
- JSON-LD は引き続き Article・BreadcrumbList・WebSite のみで、author は Organization。og:title/description は title/meta と一致。canonical・og:url は実在ページで一致。sitemap は18件で `googlef8290cdc0cd76b31.html` を含まない。当該ファイルは無変更
- `org/compliance-checklist.md` に `updated` の運用と直下の SVG の注意が1行追加された。内容は妥当
- `README.md` の「更新日の運用」（体裁だけの変更では更新しない）は、実態（ナビ・head の変更は本文変更でない）と整合

### 指摘
なし（必須・推奨とも解消）。

### チェックリスト結果（第2回）
- 薬機法: OK
- 景品表示法: OK
- ステマ規制（PR表記）: OK
- 医療広告ガイドライン（該当時）: 対象外
- 捏造なし: OK
- 広告主レギュレーション: 対象外
- 技術（disclaimer・rel・meta・sitemap・内部リンク）: OK

### 任意の提案（公開を止めない）
- 共有カードの画像が全ページ共通。将来、記事別の画像を作る場合は、チェックリスト6章（体の変化・商品を描かない）に従う。
- 月次チェックで sitemap の状態を確認した結果を、初回だけ `org/seo/README.md` か owner-inbox に記録すると、「送信済み」の記述の裏付けが残る。

<!-- 再審査時は「## 第3回審査」として下に追記する -->
