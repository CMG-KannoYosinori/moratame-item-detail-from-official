# フィードバックの記録（管理者用）

集めたフィードバックと、その対応。流れは [feedback-flow.md](feedback-flow.md)。この文書は配る zip には入らない。

| 受け取った日 | ファイル | 書いた人 | 要点 | 対応 | 反映した版 | 状態 |
|---|---|---|---|---|---|---|
| 2026-11-27 | `00001_TheFace泡洗顔料__20261125-1858-画像の圧縮.md` | — | 工程4でブランドサイトの PNG をそのまま置き、画像が合計約15MBになった。Mac・Windows の両方で使える圧縮の手段がなかった | `tools/compress_images.py`（Chrome / Edge の canvas で縮小し、WebP にする）を追加。元の画像は `source-images/`、圧縮したものを `dist/images/` に置く。目安は1枚 300KB・合計 3MB。工程5の確認に画像の重さを追加（`moratame-html`・`lp-revise`・requirements・manual）。00001 の画像で 14.9MB → 0.9MB を確認 | 次の commit | 対応済み |
| 2026-11-27 | `00001_TheFace泡洗顔料__20261125-1547-YouTube埋め込みのブロックが抜ける.md` | — | ブランドサイトのトップに YouTube が埋め込まれていたのに、ワイヤーフレームの候補に動画のブロックが出なかった（案件の中では工程2の見直しで追加して解決） | `brand-content`: `iframe`・`video`・YouTube へのリンクを拾い、CM・動画のページも読み、oEmbed で題名を確かめて content.md の「動画」に書く。`lp-wireframe`: 動画があれば `-youtube` のブロックを出す（対象商品の CM・トップの動画はおすすめ）。`figma-comp`: サムネイルと再生ボタンで組む。`moratame-html`: `-youtube` で `?rel=0`、自動再生にしない。requirements 3.1 にも追加 | 次の commit | 対応済み |
