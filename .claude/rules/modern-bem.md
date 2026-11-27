---
paths:
  - "projects/**/*.{html,css}"
---

# Modern BEM（このリポジトリで使う部分）

> item-details-template の Modern BEM 規約から、CSS だけで運用するこのリポジトリに関係する部分を残した（SCSS のディレクトリ構成などは省いた）。案件のスタイルの置き場所と書き方は `project-css.md` に従う。

## 命名

クラス名は kebab-case。案件では、ページ全体を1つの Block（`.p{案件番号}-project`）とみなし、案件専用の要素はその Element にする。

| 要素 | 決まり | 例 |
| :-- | :-- | :-- |
| Block | コンポーネント名 | `.p15403-project` |
| Element | Block 名 + `__` | `.p15403-project__feature` |
| Modifier | Block / Element + `--`。静的な見た目の違い（大きさ、色、レイアウト） | `.p15403-project__point--wide` |
| State | `is-*` か `data-*`。動的な状態（開閉、有効・無効など。JS で付け外しする） | `.is-open`、`[data-disabled='true']` |

## やってはいけないこと

**孫要素を作らない。** DOM の入れ子をクラス名に写さない。Element は常に Block に直接属する。

```css
/* 悪い */
.p15403 .p15403-project__list__item {}

/* 良い */
.p15403 .p15403-project__list {}
.p15403 .p15403-project__item {}
```

**親から別の部品を直接いじらない。** テンプレートの部品（`-button`、`-line-up` など）を、案件の Block から上書きしない。余白や配置は、部品を包む案件の Element に持たせる。

```css
/* 悪い */
.p15403 .p15403-project .p15403-button { margin-top: 16px; }

/* 良い */
.p15403 .p15403-project__action { margin-top: 16px; }
```

```html
<div class="p15403-project__action"><a class="p15403-button" …>…</a></div>
```

**Block のルートに、置かれる場所しだいのスタイル（外側の margin、絶対配置）を持たせない。** 配置は親の Element が受け持つ。
