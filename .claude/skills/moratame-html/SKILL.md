---
name: moratame-html
description: モラタメLPづくりの工程4・5。承認されたデザインカンプをもとに、テンプレート（template/00000html/dist）から商品概要のHTML・CSS・画像を作り、PC/SPで確認する。moratame-lp から呼ばれる。
---

# 工程4・5: HTMLのコーディングと確認

> **注意:** 99901 サポートミートで1回通した（2026-11-24）。案件を重ねながら、このスキルと requirements.md を直していく。

入力: 承認されたカンプ（Figma と `projects/{案件番号}/design/*.png`）、`blocks.md`、`content.md`
出力: `projects/{案件番号}/dist/`（`{案件番号}.html`、`images/`、`scripts/`、`styles/style.css`）。元の画像は `projects/{案件番号}/source-images/`

**SCSS は使わない。** コンパイルは不要で、CSS を直接書く。Node.js や VS Code の拡張機能は要らない。

## 最初に読むもの

- `.claude/rules/` のルール（文字参照、`<meta charset>` を書かない、案件CSSの書き方、Modern BEM、カンプを見てから実装する）。`projects/` の HTML・CSS を開くと自動で読み込まれる
- テンプレートの部品とクラス名の説明: `template/00000html/README.md`（**SCSS・Live Sass・npm の手順は読み飛ばす**）
- requirements.md の5章（成果物の形）と7章（部品）

## 工程4: コーディング

### 1. テンプレートをコピーする

1. `template/00000html/dist/` を `projects/{案件番号}/dist/` にコピーする。`template/` そのものは編集しない。
2. `dist/00000.html` を `dist/{案件番号}.html` に名前を変える。
3. `dist/` の中のファイル（HTML・CSS・JS）の `00000` を案件番号に置き換える（クラス名の `p00000` も `p{案件番号}` になる）。**前後に数字がない `00000` だけを置き換える**（テンプレートの見本のリンクに `000000000177` のような番号がある）。Python なら `re.sub(r'(?<!\d)00000(?!\d)', '{案件番号}', s)`。
4. `dist/styles/style.css` の最後に、案件専用の区切りのコメントを足す（`.claude/rules/project-css.md` のとおり）。

### 2. 画像を用意する

- **元の画像は `projects/{案件番号}/source-images/` に置き、圧縮したものを `dist/images/` に作る**（下の「圧縮する」）。`dist/images/` に元の画像を直接置かない（ブランドサイトの PNG は1枚 1〜3MB あり、そのまま置くとページが重くなるため）。
- 幅いっぱいの画像は 638px の2倍の **1276px** 幅を基準にする（KV は 1276×1276）。
- Figma で「画像で書き出す」としたフレーム（KV、構成図、バナーなど）は2倍で書き出す。`get_screenshot` は拡大しない（等倍までしか出ない。2026-11 時点の Figma MCP の制約）ので、次の手順にする。2倍の画像を直接得られる方法があれば、それでよい。
  1. `use_figma` で、そのフレームを素材ページに複製し、`rescale(2)` する。名前は `export2x/名前` にする。
  2. **背景が透明なフレームは、複製の塗りに置き場所の背景色を入れる**（入れないと灰色の背景が付いて書き出される。2026-11 時点の `get_screenshot` の動き）。
  3. `get_screenshot` に複製の node ID と `maxDimension`（複製の長い辺）を渡し、返ってきた URL を `curl -fL -o source-images/…` で保存する。
  4. 終わったら `export2x/` の複製を消す。
- 商品写真などは、ブランドサイトの元の画像を使う（できるだけ大きいもの）。画像の配信元が URL で縮小できるもの（Scene7 の `?wid=1276&fmt=jpg&qlt=85` など）なら、1276px 幅で取ってもよい。
- ファイル名は内容が分かる英数字にする（例: `kv.png`、`lineup-box.png`）。

#### 圧縮する

元の画像がそろったら、`tools/compress_images.py` で `dist/images/` に書き出す（Chrome、なければ Edge で動く。Mac・Windows どちらでも、Pillow は要らない）。

```sh
python3 tools/compress_images.py projects/{案件番号}/source-images --out projects/{案件番号}/dist/images     # Windows では python
```

- 1276px より広い画像は縮める。**画像は WebP にする**（透明な部分もそのまま保てる）。**1枚 300KB 以下**になるまで品質を下げる（85 → 60）。
- WebP にすると元より重くなる小さな画像（数 KB のアイコンなど）は、元のまま写される。
- 形式が変わると拡張子も変わる（`kv.png` → `kv.webp`）。最後に出る「拡張子が変わったもの」の名前で HTML・CSS を書く。
- 文字の多い図（構成図など）は、圧縮で文字がにじんでいないかをスクリーンショットで見る。にじむときは `--target-kb` を上げて作り直す。
- WebP が使えない場所に出すと言われたときだけ、`--format legacy`（透明な部分がない画像は JPEG、ある画像は PNG）にする。
- 目安は **1枚 300KB 以下、ページ全体で 3MB 以下**。超えたものは「← 目安より重い」と出る。KV などで画質を落としたくないときは、`--target-kb 500` のように目安を上げて作り直してよい（理由を報告に書く）。
- Chrome も Edge もないときは、人に Squoosh（https://squoosh.app/）などで圧縮してもらう。
- 画像を差し替えたときも、元を `source-images/` に置き、その画像だけを同じように書き出す。

### 3. HTML を書く

- 書くのは `<!-- 商品概要 -->` から `<!--//商品概要 -->` の範囲（CMS に埋め込む部分）。外側はプレビュー用の枠なので触らない。
- ブランドの書体（Google Fonts など）は、範囲の中の `<!-- fonts -->` と `<!-- /fonts -->` の間に `<link>` で読み込み、`.p{案件番号} .p{案件番号}-project` に `font-family` を書く。
- カンプの順にブロックを置く。テンプレートの部品（`-mv`、`-delivering-items`、`-section`、`-line-up`、`-item-spec`、`-allergy`、`-accordion-details`、`-banner`、`-cta-x` など）を優先して使い、部品にない見た目だけを案件専用にする。
- **カンプの見た目を変えない。** 部品を使ったブロックは部品の見た目になる（案件の CSS から部品を上書きしないため）。カンプの見た目が部品と違うブロックは、部品を使わず `p{案件番号}-project__名前` の要素でカンプどおりに組む（99901 では、今回お届けする商品・商品ラインナップ・バナーをこうした。開閉は `<details>` と `<summary>` で作り、アコーディオンの JS は使わない）。
- **例外: X投稿のお願い（`-cta-x`、「ご当選された方へ」）は、テンプレートの部品をそのまま使う。** 見本の HTML の構成（リボン画像、吹き出し、「下記のハッシュタグから順に付けて、商品の良さを伝えてくださいね。」、ハッシュタグ、ポストするボタン）と文言を変えない。リボン画像は `https://image.moratame.net/images/detail/12466/images/12466-ribbon.png` を `dist/images/ribbon.png` に写して使う。カンプの B17 が仮の箱のときは、HTML のその部分を2倍で撮ってカンプに貼る。
- ブランドサイトのセクション（特長、シリーズ、シーンなど）は `p{案件番号}-project__名前` の要素で組み、カンプに合わせる。英字の見出しの SVG などは `dist/images/` に置いて `<img>` で使う。
- **YouTube** はテンプレートの `-youtube`（`<div class="p{案件番号}-youtube"><iframe …></iframe></div>`）で埋め込む。
  - `src` は `https://www.youtube.com/embed/{ID}?rel=0`、`title` は content.md の題名（YouTube の題名）にする。テンプレートの `iframe` の `allow` などの属性はそのまま使う。
  - ブランドサイトで自動再生・ミュート・ループになっていても、LP では自動再生にしない（`autoplay`・`mute`・`loop` を付けない）。
  - カンプで動画の周りに見出しや枠があれば、その部分だけ `p{案件番号}-project__名前` で組み、中に `-youtube` を入れる。
- 案件専用の要素は `p{案件番号}-project__名前` の Element にする。
- 文字はカンプのとおり。改行もカンプに合わせる。カンプにない要素や文言を足さない。
- 記号は数値文字参照で書く（® → `&#174;`、× → `&#215;`、〜 → `&#12316;` など。`.claude/rules/character-entities.md` に一覧がある）。`<meta charset>` は書かない。ファイルは UTF-8 で保存する。
- リンクには `data-role="none"` を付ける。外部リンクは `target="_blank" rel="noopener"`。
- 送料関係費のご注意は、工程0の配送の条件（通常 / 沖縄以外 / 冷凍便 / 冷蔵便）のものを1つだけ残し、ほかは消す。
- アコーディオン（`-accordion-details`）を使わないなら、その HTML と script を消し、`dist/scripts/` も消す。
- 画像・CSS・JS のパスは、開発中はローカル（`./images/…`、`./styles/style.css`）にする。公開時の CDN（`https://image.moratame.net/images/detail/{案件番号}/…`）への切り替えは、人がアップロードするときに行う（コメントで両方を残すテンプレートの書き方に従う）。

### 4. CSS を書く

- 書く前に `.claude/rules/project-css.md` と `modern-bem.md` を読み、そのとおりに書く（案件のスタイルは `dist/styles/style.css` の最後の区切りより下だけ）。

## 工程5: 確認

1. **表示:** `python3 tools/wireframe-server.py`（Windows では `python`）を起動し、`http://127.0.0.1:8000/projects/{案件番号}/dist/{案件番号}.html` で開く（このサーバーは `charset=utf-8` を付けて返すので、`<meta charset>` がなくても文字化けしない）。
   - スクリーンショットは `tools/screenshot.py` で撮る（Chrome、なければ Edge を自動で探す。Mac・Windows どちらでも動き、Pillow も要らない）。
     ```sh
     python3 tools/screenshot.py /projects/{案件番号}/dist/{案件番号}.html            # Windows では python
     ```
     幅 640・375・320 で、縦 1300px ずつの画像に分けて保存し、ファイルの一覧を出すので、Read で見る。SP の幅は `tools/preview.html` の iframe で決めている（Chrome のウィンドウは約500px より狭くできないため）。
   - 横にはみ出していないかは、`w=320` で右端が切れていないかで見る。
   - Chrome がなければ、人に URL を開いてもらい、ブラウザの幅を変えて見てもらう。
2. **カンプとの比較:** `design/{案件番号}-pc.png`・`-sp.png` と並べて、文言・改行・色・余白・角丸・画像の位置を比べる。
3. **画像の重さ:** `python3 tools/compress_images.py projects/{案件番号}/dist/images --report` で、1枚 300KB・合計 3MB の目安を超えていないかを見る。使っていない画像が `dist/images/` に残っていないかも見る。
4. **ルール:** `<meta charset>` がない、記号が数値文字参照、クラス名の接頭辞、案件のスタイルが style.css の区切りより下だけ、使っていない送料の注意・部品が残っていない、リンクに `data-role="none"`。
5. **表現:** content.md の「表現の注意」で載せないとしたものが入っていない。法令の表示が原文どおり。
6. **リンク:** バナーのリンク先、X 投稿のハッシュタグと文言、YouTube の ID（content.md と同じか。スクリーンショットで動画のサムネイルが出ているか）。
7. 結果を短くまとめ、スクリーンショットと画像の重さ（合計）と一緒に人に見せる。**人の最終確認を待つ。**

## 終わったら

- projects/progress.md を「完了」にし、公開の前に人がやることを書く:
  - `dist/images/`・`dist/styles/style.css`・（使うなら）`dist/scripts/accordion.2.js` を CDN（`https://image.moratame.net/images/detail/{案件番号}/`）に上げる
  - HTML の画像・CSS・JS のパスを CDN に切り替える
  - `<!-- 商品概要 -->` から `<!--//商品概要 -->` までを CMS に貼る
- 作った `projects/{案件番号}/` を、決められた共有の場所に置くよう人に伝える（git を使っていない場合）。
- このスキルで実際と違ったところ・足りなかったところを、このファイルと requirements.md に反映する（管理者に伝える）。
