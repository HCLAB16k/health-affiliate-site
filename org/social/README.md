# X（旧Twitter）自動告知の仕組み（D0010）

## 流れ
1. マーケティング部（`marketer`）が投稿文を `org/social/queue/<投稿日>-<slug>.json` に書く。
2. レビュー部が記事と同じ基準で審査（compliance-checklist 3章・4章）。結果は案件フォルダの 05-review.md か `org/reviews/`。
3. PASS 後、経営企画が PR をマージ（D0006・D0010）。
4. GitHub Actions（`.github/workflows/x-post.yml`）が毎日 12:07（日本時間）に `scripts/x_post.py` を実行し、`date` が今日のものを投稿する。

## ファイル形式
```json
{"date": "2026-10-05", "article": "articles/protein-guide.html", "text": "本文 https://hclab16k.github.io/health-affiliate-site/articles/protein-guide.html #PR"}
```
- `text` は記事URLを含むこと、重み付き280以内（日本語1字=2、URL=23）。スクリプトが検証し、違反があると全体を止める。
- 投稿済みのファイルは消さずに残す（履歴）。同じ日付を再利用しない。

## 手動での確認
- GitHub → Actions → 「X post」→ Run workflow（dry_run にチェック、date に日付）で、投稿せずに内容だけ確認できる。
- ローカル: `python3 scripts/x_post.py --date 2026-10-05 --dry-run`

## 秘密情報
- API キーは GitHub の Settings → Secrets and variables → Actions にのみ登録（`X_API_KEY`・`X_API_SECRET`・`X_ACCESS_TOKEN`・`X_ACCESS_SECRET`）。未登録のときスクリプトは投稿せずに終了する。

## 取りこぼし
- 失敗や未設定で投稿されなかったものは、経営企画が新しい日付のファイルとして再投入する（文面は同じでよいが、X の重複拒否を避けるため投稿済みの文面は使わない）。
