---
name: moratame-html
description: モラタメLPづくりの工程4・5。承認されたデザインカンプをもとに、テンプレート（template/00000html/dist）から商品概要のHTML・CSS・画像を作り、PC/SPで確認する。moratame-lp から呼ばれる。
---

# 工程4・5: HTMLのコーディングと確認

> **注意:** この工程はまだ実案件で通していない（2026-11-24 時点）。1件目を進めながら、このスキルと requirements.md を直していく。

入力: 承認されたカンプ（Figma と `projects/{案件番号}/design/*.png`）、`blocks.md`、`content.md`
出力: `projects/{案件番号}/dist/`（`{案件番号}.html`、`images/`、`scripts/`、`styles/style.css`）

**SCSS は使わない。** コンパイルは不要で、CSS を直接書く。Node.js や VS Code の拡張機能は要らない。

## 最初に読むもの

- `.claude/rules/` のルール（文字参照、`<meta charset>` を書かない、案件CSSの書き方、Modern BEM、カンプを見てから実装する）。`projects/` の HTML・CSS を開くと自動で読み込まれる
- テンプレートの部品とクラス名の説明: `template/00000html/README.md`（**SCSS・Live Sass・npm の手順は読み飛ばす**）
- requirements.md の5章（成果物の形）と7章（部品）

## 工程4: コーディング

### 1. テンプレートをコピーする

1. `template/00000html/dist/` を `projects/{案件番号}/dist/` にコピーする。`template/` そのものは編集しない。
2. `dist/00000.html` を `dist/{案件番号}.html` に名前を変える。
3. `dist/` の中のファイル（HTML・CSS・JS）の `00000` を案件番号に置き換える（クラス名の `p00000` も `p{案件番号}` になる）。置き換えた後、商品URLなど関係ない `00000` が変わっていないか確かめる。
4. `dist/styles/style.css` の最後に、案件専用の区切りのコメントを足す（`.claude/rules/project-css.md` のとおり）。

### 2. 画像を用意する

- 置き場所は `dist/images/`。幅いっぱいの画像は 638px の2倍の **1276px** 幅を基準にする（KV は 1276×1276）。
- Figma で「画像で書き出す」としたフレーム（KV、構成図、バナーなど）は、`get_screenshot` で書き出して大きさを確かめる。必要な大きさにならないときは、人に Figma から2倍で書き出してもらう。
- 商品写真などは、ブランドサイトの元の画像を使う（できるだけ大きいもの）。
- ファイル名は内容が分かる英数字にする（例: `kv.png`、`lineup-box.png`）。

### 3. HTML を書く

- 書くのは `<!-- 商品概要 -->` から `<!--//商品概要 -->` の範囲（CMS に埋め込む部分）。外側はプレビュー用の枠なので触らない。
- カンプの順にブロックを置く。テンプレートの部品（`-mv`、`-delivering-items`、`-section`、`-line-up`、`-item-spec`、`-allergy`、`-accordion-details`、`-banner`、`-cta-x` など）を優先して使い、部品にない見た目だけを案件専用にする。
- 案件専用の要素は `p{案件番号}-project__名前` の Element にする。
- 文字はカンプのとおり。改行もカンプに合わせる。カンプにない要素や文言を足さない。
- 記号は数値文字参照で書く（® → `&#174;`、× → `&#215;`、〜 → `&#12316;` など。`.claude/rules/character-entities.md` に一覧がある）。`<meta charset>` は書かない。ファイルは UTF-8 で保存する。
- リンクには `data-role="none"` を付ける。外部リンクは `target="_blank" rel="noopener"`。
- 送料関係費のご注意は、工程0の配送の条件（通常 / 沖縄以外 / 冷凍便 / 冷蔵便）のものを1つだけ残し、ほかは消す。
- アコーディオンを使わないなら、その HTML と script を消す。
- 画像・CSS・JS のパスは、開発中はローカル（`./images/…`、`./styles/style.css`）にする。公開時の CDN（`https://image.moratame.net/images/detail/{案件番号}/…`）への切り替えは、人がアップロードするときに行う（コメントで両方を残すテンプレートの書き方に従う）。

### 4. CSS を書く

- 案件のスタイルは `dist/styles/style.css` の**最後の区切りより下だけ**に書く。区切りより上（テンプレートの CSS）は編集しない。
- 書けるのは `.p{案件番号}-project` と、その `__` 要素・`--` だけ。ほかの部品を親から直接いじらない。
- 入れ子は使わず平らに書く。SP を基本に書き、PC は同じセレクタのすぐ下に `@media (width >= 640px)` で書く。

## 工程5: 確認

1. **表示:** `python3 tools/wireframe-server.py` を起動し、`http://127.0.0.1:8000/projects/{案件番号}/dist/{案件番号}.html` で開く。
   - Google Chrome があれば headless で幅 640・375・320 のスクリーンショットを撮って見る（`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --window-size=幅,高さ --screenshot=…`）。
   - Chrome がなければ、人に URL を開いてもらい、ブラウザの幅を変えて見てもらう。
2. **カンプとの比較:** `design/{案件番号}-pc.png`・`-sp.png` と並べて、文言・改行・色・余白・角丸・画像の位置を比べる。
3. **ルール:** `<meta charset>` がない、記号が数値文字参照、クラス名の接頭辞、案件のスタイルが style.css の区切りより下だけ、使っていない送料の注意・部品が残っていない、リンクに `data-role="none"`。
4. **表現:** content.md の「表現の注意」で載せないとしたものが入っていない。法令の表示が原文どおり。
5. **リンク:** バナーのリンク先、X 投稿のハッシュタグと文言。
6. 結果を短くまとめ、スクリーンショットと一緒に人に見せる。**人の最終確認を待つ。**

## 終わったら

- projects/progress.md を「完了」にし、公開の前に人がやることを書く:
  - `dist/images/`・`dist/styles/style.css`・（使うなら）`dist/scripts/accordion.2.js` を CDN（`https://image.moratame.net/images/detail/{案件番号}/`）に上げる
  - HTML の画像・CSS・JS のパスを CDN に切り替える
  - `<!-- 商品概要 -->` から `<!--//商品概要 -->` までを CMS に貼る
- 作った `projects/{案件番号}/` を、決められた共有の場所に置くよう人に伝える（git を使っていない場合）。
- このスキルで実際と違ったところ・足りなかったところを、このファイルと requirements.md に反映する（管理者に伝える）。
