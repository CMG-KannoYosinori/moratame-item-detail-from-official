---
name: figma-comp
description: モラタメLPづくりの工程3。blocks.md で選ばれたブロックを、ブランドサイトの素材とトンマナで、Figma に PC 640px と SP 375px のデザインカンプとして組む。承認後に PNG で書き出す。moratame-lp から呼ばれる。
---

# 工程3: Figma のデザインカンプ

入力: `blocks.md`（使うブロックと並び、商品の区分、メモ）、`content.md`（文言・素材・トンマナ）、工程0で聞いた Figma の URL
出力: Figma の「カンプ」ページに `{案件番号} PC 640`・`{案件番号} SP 375`・`メモ（仮・要確認）`。承認後に `projects/{案件番号}/design/{案件番号}-pc.png`・`-sp.png`

## 決まり（requirements.md 4章）

- **PC:** 幅640px（外枠の1pxボーダー込み。中身は638px）。**SP:** 幅375px（中身は373px）。SP の基準は 375px（テンプレートのルールの 320px より優先）。
- blocks.md で `[x]` のブロックだけを、**blocks.md の順に**組む。商品ラインナップは「対象」→「紹介」の順。対象には商品名の上に「今回試せる商品」のラベル。「載せない」は出さない。
- ブランドサイトの色・書体・写真・あしらいを使う。テンプレートの既存部品（requirements.md 7節）の形を優先する。
- 文字は画像にせず、編集できるテキストで置く（HTMLでもテキストにする前提）。画像として書き出す部分（KV、構成図、バナーなど）は、フレーム名に「画像で書き出す」と書く。
- 各セクションのフレーム名は `B02 リード` のように blocks.md の ID と名前にする（テンプレート部品があれば `（-delivering-items）` のように添える）。
- モラタメのシステムが差し込む部分（今回タメせる商品、送料の注意）はカンプに入れない。

## 手順

### 1. 準備

1. Figma の URL から fileKey を取り、`create_session` を呼ぶ。返ってきた sessionId を以後の Figma ツールすべてに渡す。
2. `get_figma_skill` で `skill://figma/figma-use/SKILL.md` と `skill://figma/figma-generate-design/SKILL.md` を読む。`use_figma` の `skillNames` には `resource:figma-use,resource:figma-generate-design` を渡す。
3. `use_figma` で中身を確かめる（ページ、既存のフレーム、使える書体）。書体は `listAvailableFontsAsync` でブランドの書体（なければ近い Google Fonts）を確かめる。
4. ページを用意する: 1ページ目を「カンプ」、素材用に「素材」ページを作る（既にあれば使う）。

### 2. 素材を Figma に上げる

1. content.md の素材のうち、使うものを `curl` で `/tmp/{案件番号}_assets/` に取る（ブランドサイトに無い画像は使わない。無ければ文字だけで組む）。
2. `upload_assets` を `count`（使う数。60まで）と `currentPageId`（素材ページ）で呼ぶ。
3. 「ファイルのパス<TAB>submitUrl」の対応表を作り、`bash tools/figma-upload.sh 対応表.tsv` で送る（multipart で送るのでファイル名がレイヤー名になる）。
4. 結果の `imageHash`（PNG/JPG）と `placedOnNodeId`（SVG は編集できるベクターになる）を控える。SVG のノードは `use_figma` で `svg/名前` に名前を付けておく。

**載せない表現が入った素材は使わない**（例: ロゴ文字の画像に「健康維持に役立つ」など効果の表現が入っているもの）。代わりにテキストで組み、メモに書く。

### 3. カンプを組む

- [helpers.js](helpers.js) の関数（`T`・`AL`・`IMG`・`svgW`・`svgH`・`triangle`）をスクリプトの先頭に貼り、`H`（imageHash）と `SV`（SVG の node ID）を埋める。
- `build(pc)` 関数を書き、`build(true)` と `build(false)` を**1回の `use_figma` で**呼ぶ。スクリプトの最初に、同じ名前の既存フレーム（`{案件番号} PC 640` など）を消しておく（何度実行しても同じ結果になるように）。
- PC は x=0、SP は x=760、メモは x=1200 に置く。
- 背景色はセクションごとに交互に変え、隣り合うセクションの区切りが分かるようにする。
- 返り値で、フレームの ID・高さ・セクション数を返す。

### 4. 確かめる

1. `use_figma` で、PC と SP のフレームの子（セクション）を数個ずつ `await section.screenshot({ scale: 0.6 })` で撮って見る（画像が返り値と一緒に返ってくる。PC の上から順に、1回に3〜4セクション）。ページ全体を1枚で撮ると縦に長すぎて細部が見えないため、セクションごとに見る。追加のソフトは要らない。
2. 見るところ: 文字の欠け・はみ出し、重なり、記号が絵文字で表示されていないか（▶ など。図形は `triangle()` のように SVG で作る）、書体がブランドの書体か、画像の抜け。
3. 直すところだけを、ノードを ID で探して直す（全体を作り直さない）。直したら、その部分だけもう一度見る。

### 5. メモと報告

- 「メモ（仮・要確認）」のフレームに、仮の値（対象商品・個数など）、画像で書き出す部分、要確認の表現、ブランドサイトに素材がなかったところ、自分で足した要素を書く。
- カンプの URL（`?node-id=` 付き）と、確認してほしいことを短く伝える。修正は会話でも Figma のコメントでもよいと伝える。
- projects/progress.md を更新する（Figma のページと node ID、確認中のこと）。

## 修正を受けたとき

- Figma のコメントは `get_comments` で読む。直したら、そのコメントに返信してよいか確認してから返信する。
- 直したら、該当部分のスクリーンショットで確かめ、何を直したかを伝える。

## 承認されたら

1. `get_screenshot` で PC と SP のフレームを、`maxDimension` にフレームの高さを渡して原寸で取る。返ってきた URL から `curl -fL -o` で `projects/{案件番号}/design/{案件番号}-pc.png`・`{案件番号}-sp.png` に保存する（`.claude/rules/design-comp.md` が読む場所）。
2. projects/progress.md を更新する（工程3 完了、次は工程4）。
