# レビュー: X 自動告知の初回9本（D0010）

- 審査日: 2026-09-28（ファイル名の日付は経営企画の指定どおり）
- 審査者: レビュー部（compliance-reviewer）
- 対象: `org/social/queue/*.json` 9ファイル（2026-10-05〜10-13。ブランチ `claude/healthcare-affiliate-ai-org-jyeqv1` のコミット a9df5b0 時点）
- 基準: org/compliance-checklist.md 1章・3章（X 自動告知）・4章・7章、D0010、org/social/README.md、org/departments/marketer.md
- 方法: 各投稿の主張を対象記事のHTML（HTMLコメントを除いて表示される本文）と照合した。外部リンク（`<a href="http…">`）を全記事で数えた。重み付き文字数は `scripts/x_post.py` の `weighted_length` で測った（投稿処理は実行していない）。

## 判定: REVISE（1本だけ要修正。差し戻し先: marketer。残り8本はこのままで可）

法令違反・捏造・効能の示唆・医療広告の問題はない。直す必要があるのは `2026-10-13-site.json` の1か所だけで、サイトの実態より強く書いている（about.html の前回審査 R1 と同じ種類のずれ）。直したら再審査なしでマージしてよい（下の修正案どおりの場合）。修正案と違う文面にするなら再審査に回す。

## 投稿ごとの結果

| 投稿日 | 対象 | 重み | 記事との照合 | #PR | 医療広告 | 判定 |
|---|---|---|---|---|---|---|
| 10-05 | winter-vitamin-d | 226 | 一致（L40・L44〜46・L147）。NHS の記述は原文でも確認 | 不要（リンク0） | 該当なし | PASS |
| 10-06 | retinoids-japan-vs-overseas | 220 | 一致（L44・L78・L80）。2016年は FDA 承認書の原文で確認 | 不要（リンク0） | 該当なし。処方薬は一般名のみ・効能なし | PASS |
| 10-07 | aga-selfcare-vs-clinic | 196 | 一致（1文目は L38 とほぼ同文） | 不要（リンク0） | クリニック名・料金・無料カウンセリングなし。URLは記事トップ | PASS |
| 10-08 | protein-guide | 204 | 一致（L43・46・49・53〜56・59〜61） | **必要・付いている** | 該当なし | PASS（任意の提案あり） |
| 10-09 | hair-scalp-care | 182 | 一致（title・description、本文「本数」「抜け方」「薬用シャンプー」） | 不要（リンク0） | 該当なし | PASS |
| 10-10 | skincare-antiaging | 189 | 一致（L43・L66〜67、4成分とも本文にあり） | 不要（リンク0） | 該当なし | PASS |
| 10-11 | sleep-support | 176 | 一致（L65・まとめ「生活習慣の見直しを基本に」） | 不要（リンク0）※記事側のバッジに注意 | 該当なし | PASS |
| 10-12 | fatigue-recovery | 182 | 一致（description・L65・表） | 不要（リンク0）※記事側のバッジに注意 | 該当なし | PASS（任意の提案あり） |
| 10-13 | site（index.html） | 238 | **「資料にあたりながら」が実態より強い** | 不要（index にリンク・a8linkmgr なし） | 該当なし | **REVISE** |

全9本に共通: 効能・効果の表現、体験談、ランキング、最大級表現、絵文字、#PR 以外のハッシュタグは無い。URL は各記事のトップで、クリニックの記載箇所などへの直リンク（#アンカー）は無い。重み付きはすべて280以内。

### 修正が必要な箇所

**[X1] 2026-10-13-site.json「学会のガイドラインや公的機関の資料にあたりながら中立的に整理するサイトです」（marketer）**
- index.html の description（L8）は「資料に**できるだけ**あたりながら」、L44 は「以前に公開した記事は、更新の際に順次対応します」と条件を付けている。投稿は「できるだけ」を落としている。
- 実態: skincare-antiaging・sleep-support・fatigue-recovery の3本には出典の記載が無い（「出典」「確認日」「学会」「厚生労働省」を Grep して0件）。サイト全体について無条件で言うと事実より強い（2026-09-28 about.html レビュー R1 と同じ）。
- 修正案（重み 248、280以内）:
  > 「男の養生帖」は、30代以降の働く男性に向けて、肌・髪・体・睡眠のセルフケアを、学会のガイドラインや公的機関の資料にできるだけあたりながら中立的に整理するサイトです。商品の区分ごとに「言えること・言えないこと」を分けています。 https://hclab16k.github.io/health-affiliate-site/

### 任意の提案（判定には影響しない）

1. **protein（10-08）の「#PR」を冒頭に置く（marketer）**。今の位置（末尾、URLの後）でも、短い文で単独のハッシュタグなので「広告の表示が埋もれている」とは言いにくく、違反とは判断しない。ただし冒頭のほうが一目で分かり、X の表示でも本文より先に読まれる。例: `#PR ホエイ・ソイ・カゼインは、…まとめました。 https://…/protein-guide.html`。消費者庁のステマ運用基準の原文は、この環境では caa.go.jp が 403 で取得できず（.sources/README.md 144行の記録どおり）、位置の要件は原文で確認していない。
2. **fatigue（10-12）「疲れが気になる方向けのサプリに使われる」→「使われることがある」（marketer）**。記事に出典が無く、チェックリスト1章「傾向は出典が無ければ配合例がある程度に弱める」に寄せる。記事の description と同じ言い回しなので必須にはしない。sleep（10-11）の「サプリに使われる」も同じ。
3. **skincare の URL に `antiaging` が出る**。記事に OG／Twitter Card のタグが無いので（全記事で `og:`・`twitter:` が0件）、X ではカードではなく URL の文字列が見える可能性が高い。チェックリスト1章は「アンチエイジング」の語を使わないとしている。英語のスラッグで効能をうたう文ではないので今回は可とするが、URL を変えるならリダイレクトと sitemap の対応が必要（経営企画・editor の判断）。
4. **OG タグを足すなら再審査に回す**（editor）。カードには title・description・画像が出るので、投稿文と同じ基準で見る必要がある（例: sleep-support の description「睡眠の質を意識した」）。

## 記事側の指摘（投稿文の外。今回の判定には含めない）

**[A1] sleep-support.html・fatigue-recovery.html の pr-badge が「PR / 本記事はアフィリエイト広告を含みます」のまま（editor）**
- 両記事とも affiliate-box はHTMLコメントの中で、表示されるアフィリエイトリンクは0件。チェックリスト7章では、リンクが描画されない記事は「PR / 当サイトはアフィリエイト広告を利用しています」（hair・skincare・aga・retinoids・winter は変更済み）。
- 投稿（#PR なし）から来た読者が「本記事は広告を含みます」を見ると、投稿で広告を隠したように見えかねない。広告の表示が多すぎても違反にはならないので法的リスクは無いが、投稿日（10-11・10-12）より前に「利用しています」に揃えるのが望ましい。直さない場合は、代わりに両投稿に「#PR」を付けてもよい（過剰な表示は問題にならない）。

## マーケティング部の申し送りへの判断

### (a) a8linkmgr.js がリンクを自動でアフィリエイトリンクに変える可能性と #PR
- **A8 の公開情報**（`.sources/a8_help_linkmanager.txt`、`.sources/a8_campaign_linkmanager.txt`、2026-09-28 取得）:
  - 「あなたのサイトや記事に貼っている広告主サイトへのリンクを、自動でアフィリエイトリンクに変換してくれる機能です」（リンクマネージャー対応プログラム特集）
  - 対象は「プログラム詳細画面にリンクマネージャーのアイコンがついているもの」。サイトごと・プログラムごとに置換の許可／ブロックを設定できる。機能は管理画面で ON にして使う（ヘルプ「リンクマネージャーの使い方」）。
  - 提携していないプログラムでも変換されるのかは、公開ページには書かれていない（未確認）。ON／OFF の状態は管理画面でしか確認できない。
- **当サイトの実態**: 記事8本と index.html で、外部への `<a href="http…">` は protein-guide の A8 リンク2件だけ（ほかの外部 href は Google Fonts の `<link>` で、変換の対象になるリンクではない）。出典の URL は文字として書かれていて、リンクになっていない。index.html は a8linkmgr を読み込んでいない。
- **結論: 今の9本では #PR の要否は変わらない**。変換されうる「広告主サイトへのリンク」が protein 以外に存在しないため、a8linkmgr が表示時にアフィリエイトリンクを作ることはない。protein はもともと #PR 付き。
- **ただし運用上の穴が2つある**（経営企画）:
  1. 投稿文はマージ時点の記事に合わせて書かれ、投稿は最大2週間後。その間に記事へアフィリエイトリンクを戻す（sleep・fatigue・skincare の affiliate-box 復活など）と、#PR の無い告知が出る。**対策案**: `scripts/x_post.py` の投稿前に対象記事の HTML を読み、HTMLコメント外に `cta-btn` か外部の `<a href="http…">` があるのに text に「#PR」が無ければ、その投稿を止める。スクリプトを直さない場合は、affiliate-box を戻す案件のゲートに「キューにある同じ記事の投稿に #PR を足す」を加える。
  2. 今後、記事に広告主の公式サイトへの通常リンク（出典としてのリンクを含む）を置くと、リンクマネージャーの置換が ON なら表示時にアフィリエイトリンクになりうる。marketer の判断基準（「cta-btn がHTMLコメントの外にあるか」）だけでは拾えない。**対策案**: marketer.md の基準を「HTMLコメント外に cta-btn、または外部サイトへの `<a>` がある記事は #PR」に広げる。あわせて、オーナーに管理画面で自動置換の ON／OFF と許可中のプログラムを確認してもらう（owner-inbox、推測で埋めない）。
- 補足: A8 のヘルプは タグを `<head>` の上のほうに置くよう案内しているが、当サイトは `</body>` の直前に置いている。置換の動作に影響しうるが、変換対象のリンクが無い今は実害なし。

### (b) X の健康食品の PR 投稿に関するポリシー
- **確認できたもの**: X 広告ポリシー「Health care」（`.sources/x_ads_policy_healthcare.txt`、https://business.x.com/en/help/ads-policies/ads-content-policies/healthcare.html 、2026-09-28 取得）。
  - 冒頭: 「This policy applies to monetization on X and X's paid advertising products.」→ 対象は X の広告商品（プロモ投稿）と収益化。**当社の自動告知はオーガニック投稿（広告費を払わない）なので、この広告ポリシーの直接の対象ではない**。
  - 対象には「Health and wellness supplements」「Informational sites or blogs focusing on prescription drugs」「Medical and cosmetic services」「Telemedicine」が含まれる。
  - Japan の項: 「Healthcare products and supplements are permitted subject to restrictions.」「Ads must not refer to the benefits or effects of a medical device, product or service.」「Advertising should comply with applicable medical related regulations.」
  - → 将来プロモ投稿（有料広告）に使う、または X の収益化プログラムに参加する場合はこのポリシーが適用される。効能に触れない当社の投稿ルール（D0010）は Japan の条件と方向が同じだが、retinoids（処方薬を扱う情報記事）・aga（医療機関・オンライン診療を扱う記事）は「事前の認可が必要」「処方薬の情報サイト」に当たりうるので、**有料で出す前に必ず再審査**すること。4章の「有料広告から クリニック記載箇所へ直接誘導すると限定解除要件①を満たさない」とも関係する。
- **確認できなかったもの**: help.x.com の「Paid partnerships policy」（オーガニック投稿での有償提携の開示ルール）と「Automation rules」は、curl・WebFetch とも HTTP 403 で**取得不可**（.sources/README.md に記録）。したがって、「自サイトの記事（アフィリエイトリンクを含む）への告知が X の定める有償提携に当たるか」「X 所定の開示方法（ラベル等）が必要か」は未確認。
- **結論**: 確認できた範囲では、今回の9本を止める X 側のルールは見当たらない。国内法（ステマ規制）にもとづく「#PR」の付与（D0010）で開示している。未確認の2つのポリシーは、オーナーに X のヘルプセンターで確認してもらうよう owner-inbox に積むことを勧める（とくに有償提携の開示方法と、自動化アカウントのラベル設定。後者は D0010 で既にオーナー作業）。

## 事実性（出典で照合したもの）
- NHS「Vitamin D」（WebFetch、2026-09-28）: 「Everyone … should consider taking a daily supplement containing 10 micrograms of vitamin D during the autumn and winter.」「Do not take more than 100 micrograms (4,000 IU) of vitamin D a day」、Page last reviewed 03 August 2020。10-05 の投稿（NHS は秋冬のサプリを「検討」するよう勧める、共通の耐容上限量）と一致。記事の注2どおり見直し予定日は過ぎている。
- FDA 承認書 NDA 020380/S-010（WebFetch で PDF の日付、`.sources/fda_differin_otc_ltr_2016.txt` L22「provides for the over-the-counter use」・L216 署名日 07/08/2016）: 10-06 の「米国では2016年から市販薬」と一致。
- 日本皮膚科学会 ガイドライン一覧（WebFetch、2026-09-28）: 「男性型および女性型脱毛症診療ガイドライン（2017年版）」の掲載を確認。10-07 の「日本皮膚科学会の診療ガイドライン」と一致。
- 日本の食事摂取基準（2025年版）の内容は 0004 審査で照合済みのため今回は再照合していない。

## 前工程の検証
- marketer の「#PR は cta-btn がHTMLコメントの外にある記事だけ」→ Grep で確認。コメント外の `cta-btn` は protein-guide（L75・L82）のみで、#PR が付いているのも protein だけ。一致。
- marketer の「医療広告の該当は aga のみ」→ クリニックを扱う記事は aga-selfcare-vs-clinic のみ（「掲載基準」節 L228〜、現時点では個別の医療機関を載せていない）。一致。

## 参照ファイル（原文）
- `.sources/a8_help_linkmanager.txt`、`.sources/a8_campaign_linkmanager.txt`、`.sources/a8_help_faq_sns.txt`、`.sources/x_ads_policy_healthcare.txt`（2026-09-28 取得、TLS 検証あり）

## 経営企画の対応（2026-09-28）
- 要修正の 10-13 site: 修正案どおりの文面に差し替え（重み付き 248）。レビューの指示により再審査なしでマージ。
- sleep-support・fatigue-recovery の pr-badge を「PR / 当サイトはアフィリエイト広告を利用しています」に修正（checklist 7章の既定の文言。backlog #18 実施）。
- 申し送り①: `scripts/x_post.py` に、投稿時に対象記事のコメント外の `cta-btn`・外部リンクを確認し、#PR が無ければ全体を止める検証を追加（9本すべて dry-run で通過を確認。protein のみ広告リンクありと判定）。
- 申し送り②: marketer の判断基準を拡張（`org/departments/marketer.md`）。オーナー依頼 D4（A8 リンクマネージャーの設定）・D5（X の自動化ルール・ラベル）を追加。
- 任意の提案（#PR の位置、「使われることがある」、OG タグ）は見送り。OG タグは将来の案件で扱う。
