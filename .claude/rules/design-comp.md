---
paths:
  - "projects/**/dist/**/*.{html,css}"
---

# デザインカンプを見てから実装する

HTML や CSS を実装・修正する前に、`projects/{案件番号}/design/` のカンプを開いて内容を確認する。文言、改行、色、余白、角丸、画像の位置はカンプに合わせる。カンプにない要素や文言は足さない。

- SP: `design/{案件番号}-sp.png`（幅 375px が基準。320px でも崩れないようにする）
- PC: `design/{案件番号}-pc.png`（幅 640px。1px のボーダー込み）
- カンプは Figma にもある（`projects/progress.md` に URL と node ID がある）。細かい値は Figma で確かめてよい
- `design/` にカンプがないときは、推測でデザインを足さず、人に確認する
