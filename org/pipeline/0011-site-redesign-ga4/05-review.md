# 05 レビュー: 0011 サイトデザインの刷新・GA4 導入・HTML骨格

- 担当: compliance-reviewer
- 審査対象: `git diff origin/main` 全体（ブランチ `claude/healthcare-affiliate-ai-org-jyeqv1`、コミット b30cc8e）。`style.css`、全HTML 12ページ（index・about・disclosure・privacy・articles/*.html 8本）、画面の写真 png 3枚（`articles_protein-guide.html-desk.png`・`index.html-desk.png`・`index.html-mob.png`）

## 前工程への質問・異議
- 記事ページの**スマホ幅（390px）の写真が無い**（index のスマホ写真とプロテイン記事のPC写真のみ）。pr-badge・affiliate-box・比較表を 390px 幅で見た確認は CSS を読んだ範囲に留まる。公開後にオーナーか経営企画が実機で1本確認してほしい（下の推奨#4）。

## 前工程の検証
| 00 の主張 | 検証方法 | 結果 |
|---|---|---|
| 記事本文・title・meta description は変えない | `git diff origin/main -U0 -- '*.html'` の変更行をすべて集計した。`<title>` は12ページとも削除行と追加行が同じ文字列（`<head>` 内へ移しただけ）。`description` を含む変更行は0件 | 一致。記事8本の差分は head の骨格・フォント・GA4・ロゴの絵文字除去・フッターの「\|」除去・`</body></html>` のみ |
| 外部読み込みは Google Fonts と GA4 のみ追加 | 追加行を集計（preconnect 2本・fonts.googleapis.com の CSS 1本・googletagmanager の gtag.js と設定スクリプト）が各12回 | 一致。ほかの外部読み込みの追加なし |
| A8 の a8linkmgr はそのまま | 記事8本で a8linkmgr の行は無変更、位置は footer の後・`</body>` の直前（body 内） | 一致 |
| Search Console の確認用メタタグを残す／googlef8290cdc0cd76b31.html は触らない | index.html の `<head>` 内に `google-site-verification` が残存。`git diff --quiet` で googlef ファイル・sitemap.xml・_config.yml は無変更 | 一致 |
| 全ページに DOCTYPE・lang・head・body | 12ページとも1行目が `<!DOCTYPE html>`、`<html lang="ja">`、`<head>`・`</head>`・`<body>`・`</body>` が各1回、最終行 `</html>`。`<meta charset>` が head の先頭 | 一致 |
| GA4 測定ID G-K66FGCJ14H | 12ページの gtag の ID と owner-inbox C1 の回答が一致 | 一致 |

## 経営判断ログの遵守確認
| 判断（00-brief の行） | 遵守 / 不遵守 | 該当箇所 |
|---|---|---|
| 0011 の番号 | 遵守 | フォルダ名 |
| 書体（Shippori Mincho B1・Zen Kaku Gothic New・Manrope） | 遵守 | style.css `--font-*`、各ページの Google Fonts の読み込み |
| ロゴの絵文字「📓」を外し文字ロゴに | 遵守 | 12ページの `.logo`、style.css `.logo::after`（"OTOKO NO YOJOCHO"） |

## 持ち越し論点の最終判断
- **英字ラベル（観点1）**: index のカードの英字ラベルは `SKIN`・`SKIN / JAPAN & US`・`HAIR`・`HAIR / CLINIC`・`BODY`・`SLEEP`・`ENERGY`・`SEASONAL / UK & JAPAN`、hero の `Skin · Hair · Body · Sleep`、見出しの `Articles`。どれも記事の**分野名**で、商品名・CTA の近くには無く、効能（改善・増強・回復）を示す語は無い。許容とする。
  - `ENERGY` だけは単独だと「活力を与える」と読まれうる。ただしすぐ下の見出しは既存の「疲労・エナジーマネジメント」（本案件で変わっていない）で、その英訳にあたるため必須にはしない。気になるなら `FATIGUE`・`DAILY CONDITION` など症状・話題の語に替えるのを推奨（推奨#1）。
  - `HAIR / CLINIC` は特定の医療機関を示さず、カードの説明文（既存）も「受診するか。判断の目安を中立に整理」なので、医療広告の特定性は満たさない。許容。
- index のカードの説明文は**文言が変わっていない**（h3 の先頭の絵文字を外しただけ）。追加された文字列は `<h2>記事</h2>` と CSS の生成テキスト「+ 記事を読む」「OTOKO NO YOJOCHO」、フッターの「男の養生帖」だけ。hero の h1 は `<br>` で3行に分けただけで文言は同じ。

## 第1回審査（2026-09-28）

**判定: REVISE**

法令違反・捏造は無い。表示義務（pr-badge・disclaimer・affiliate-box の提携表示・CTA）はデザイン変更後も読める。記事本文・title・meta description は変わっていない。
差し戻すのは privacy.html の Google Fonts の1文だけ（出典を確認できない断定＋送信される情報の記載漏れ）。直せば再審査は privacy.html の該当段落の確認だけで PASS にできる。

### 指摘
| # | 観点 | 該当箇所（引用） | 問題 | 修正案 | 差し戻し先 | 重大度（必須/推奨） | 対応（修正側が記入） |
|---|---|---|---|---|---|---|---|
| 1 | 事実性（privacy） | privacy.html「ページの表示時に、ご利用のブラウザから Google のサーバーへ接続が行われます（Cookie は使用されません）。」 | ①「Cookie は使用されません」は Google の第三者の挙動についての断定で、出典が無い。Google Fonts の FAQ（fonts.google.com/faq#privacy）は JavaScript で描画されるため、WebFetch でも curl でも本文を取れず**照合できなかった**。②プライバシーの説明として肝心の「何が送られるか」が書かれていない。Google の「Google のサービスを使用するサイトやアプリから収集した情報の Google による使用」ページは、Google のサービスを使うサイトを見るとページの URL や IP アドレスなどが Google に送られると説明している | 例:「当サイトは、文字の表示に Google Fonts（Google LLC）を利用しています。ページの表示時にお使いのブラウザが Google のサーバーからフォントを読み込むため、IP アドレス・ブラウザの種類・閲覧中のページの URL などが Google に送信されます。Google による取り扱いは Google のプライバシーポリシー（https://policies.google.com/privacy）をご確認ください。」Cookie の有無は、原文を確認できた場合だけ出典付きで書く（確認できなければ書かない） | 経営企画（実装者） | 必須 | |
| 2 | privacy の正確さ | privacy.html「これらの情報は、氏名など個人を直接特定する情報を含まない形で集計され」 | 以前の「個人を特定する情報は含まれません」より弱められており、許容範囲。ただし GA4 の読み込み時にも IP アドレスは Google に送られる（上記 Google のページ）ので、「当サイトが受け取る集計データには」と主語をはっきりさせると誤解が少ない。Google のパートナーサイトのページへのリンクも、GA の開示ポリシー（support.google.com/analytics/answer/7318509）が参照先として挙げている | 例:「当サイトが Google アナリティクスで受け取るのは、氏名など個人を直接特定する情報を含まない集計データです。」＋「Google によるデータの使用については『Google のサービスを使用するサイトやアプリから収集した情報の Google による使用』（https://policies.google.com/technologies/partner-sites）をご確認ください。」を追記 | 経営企画（実装者） | 推奨 | |
| 3 | 表示（ラベル） | index.html `<span class="eyebrow">ENERGY</span>` | 上の「持ち越し論点」のとおり単独では活力の付与と読まれうる | `FATIGUE` / `DAILY CONDITION` 等に替える（任意） | 経営企画（実装者） | 推奨 | |
| 4 | 技術（スマホ） | 記事ページ全般（390px 幅の写真なし） | CSS 上は `overflow-wrap: anywhere`・640px 以下で `table.compare { display:block; overflow-x:auto }`・`.pr-badge` は inline-block なので横スクロールは出ない見込みだが、写真で未確認 | 公開後に protein-guide（affiliate-box と比較表がある唯一の収益記事）を 390px で1回確認し、写真を案件フォルダに残す | 経営企画 | 推奨 | |
| 5 | privacy（将来） | privacy.html 全体 | 電気通信事業法の外部送信規律の対象になるかは本サイトの規模・形態では判断が分かれる。現状の記載（送信先 Google LLC・情報の種類・目的・オプトアウト）でおおむね通知・公表の項目は揃っている。AdSense 等を実際に入れる時点で、送信先ごとの一覧にするのを推奨 | 広告タグを追加する案件で見直す（backlog 起票を推奨） | 経営企画 | 推奨 | |

### 出典照合の記録
| 記事中の記述 | 出典URL | 照合結果 |
|---|---|---|
| 「Google アナリティクス オプトアウト アドオン」（https://tools.google.com/dlpage/gaoptout）で停止できる | https://tools.google.com/dlpage/gaoptout （WebFetch、2026-09-28） | 一致。ページ名 "Google Analytics Opt-out Browser Add-on"、「サイト訪問者が自分のデータを Google アナリティクスで使われないようにする」ためのアドオンと説明 |
| GA を使う旨・データの収集と処理の方法を開示する | https://support.google.com/analytics/answer/7318509?hl=ja （WebFetch、2026-09-28） | GA のポリシーは「GA の利用」と「データの収集・処理の方法」の開示を求める。privacy.html は両方を記載しており充足。パートナー向けのプライバシーページへの誘導は推奨#2 |
| Google のサービスを使うサイトでは URL・IP アドレス等がブラウザから Google に送られる（指摘#1・#2 の根拠） | https://policies.google.com/technologies/partner-sites?hl=ja （WebFetch、2026-09-28） | ページ名「Google のサービスを使用するサイトやアプリから収集した情報の Google による使用」。訪問時にページの URL や IP アドレスなどがブラウザから自動的に Google に送信されると説明 |
| Google Fonts は Cookie を使用しない | https://fonts.google.com/faq#privacy （旧 developers.google.com/fonts/faq/privacy から 301） | **取得不可**（JavaScript 描画で本文が取れない。WebFetch・curl とも本文なし。web.archive.org は WebFetch 不可・curl でも取得できず）。→ 指摘#1 |
| GA が収集する情報（閲覧ページ・滞在時間・参照元・おおよその地域・端末） | 上記 GA ヘルプ・partner-sites ページ | 矛盾なし（一般的な GA4 の収集項目の範囲） |

### チェックリスト結果
- 薬機法: OK（本文不変。追加の英字ラベルは分野名で効能をうたわない）
- 景品表示法: OK（ランキング・No.1 等の追加なし。カードの連番 01〜08 は CSS の counter による並び番号で、順位を示す文言は無い）
- ステマ規制（PR表記）: OK（pr-badge は記事の最上部、#2f3e70 の地に白の太字 0.78rem で旧版〔0.75rem〕より大きい。コントラストは約10:1。写真でも本文より先に目に入る。affiliate-box の「当サイトが広告の提携をしている販売サイト…へのリンクです」は #3c4049・0.9rem で読める。CTA は墨地に白の太字ボタン。disclaimer は上下の罫線付きで 0.84rem・#3c4049、写真で読める）
- 医療広告ガイドライン（該当時）: OK（index の `HAIR / CLINIC` は特定性なし。AGA 記事の本文は不変）
- 捏造なし: OK
- 広告主レギュレーション: OK（affiliate-box・リンク・a8linkmgr・計測用 1px 画像に変更なし）
- 技術（disclaimer・rel・meta・sitemap・内部リンク）: OK（disclaimer 8本とも残存、`rel="sponsored nofollow"` 変更なし、meta description 不変、sitemap は新ページが無いので更新不要、内部リンク不変。HTML 骨格は12ページとも妥当。Search Console のメタタグ残存・googlef ファイル無変更）

### 読者目線の講評
- トップは大見出し・余白・罫線で「中立の手引き」の落ち着いた印象になり、30代以上の読者に対して以前の絵文字付きカードより信頼感がある。カードの「01〜08」の連番はランキングに見えないよう、今後「おすすめ順」などの文言を近くに置かないこと。
- 灰色の小さい文字（`--muted` #6b6f78 と地 #f6f4ef のコントラスト約4.6:1）はカード説明文で AA をかろうじて満たす。これ以上薄くしないこと。
- プロテイン記事の写真では、比較表の右端に罫線の無い白地が少し出て見える（描画環境の代替フォントによる可能性）。表示義務には影響しない。

### 組織への提案（チェックリスト・書式の不足）
- チェックリスト 7章に「**共通デザイン変更時は pr-badge・affiliate-box の提携表示・disclaimer の文字サイズとコントラスト、390px 幅の写真（記事ページ1本以上）を審査資料に含める**」を追加することを提案。
- 同 7章に「privacy.html に外部サービス（解析・フォント・広告タグ）を書くときは、送信先・送信される情報・目的・停止方法と、確認できた出典のみを書く」を追加することを提案。
