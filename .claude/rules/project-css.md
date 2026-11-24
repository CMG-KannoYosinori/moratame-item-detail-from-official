---
paths:
  - "projects/**/*.{html,css}"
---

# 案件の CSS は style.css の最後に Modern BEM で書く

このリポジトリでは SCSS を使わず、CSS だけで運用する（コンパイルしない）。

`projects/{案件番号}/dist/styles/style.css` は、テンプレートのコンパイル済み CSS をそのまま写したもの。**その中身は書き換えない。** 案件だけのスタイルは、ファイルの最後に次の区切りのコメントを置き、その下に書く。

```css
/* ==========================================================================
   案件専用（{案件番号}）ここから。この区切りより上はテンプレートの CSS なので編集しない
   ========================================================================== */
```

- 書いてよいのは `.p{案件番号}-project` と、その Element（`.p{案件番号}-project__名前`）・Modifier だけ。
- テンプレートの部品（`.p{案件番号}-line-up` など）を案件の見た目のために上書きしない。親から子の部品を直接いじらない（`.p{案件番号}-project .p{案件番号}-button` は不可）。余白や配置は `project__` の Element に持たせる。
- 孫要素（`__a__b`）は作らない。要素名はフラットにする（`.p{案件番号}-project__point-title`）。
- 入れ子（CSS Nesting）は使わず、平らに書く。
- SP を基本に書き、PC はテンプレートと同じ書き方の `@media (width >= 640px)` で、同じセレクタのすぐ下に書く（ファイルの最後にまとめない）。

```css
.p15403-project__feature {
  padding: 20px 12px 8px;
}

@media (width >= 640px) {
  .p15403-project__feature {
    padding: 28px 24px 12px;
  }
}

.p15403-project__feature-heading {
  text-align: center;
}
```

くわしい規約は `modern-bem.md` を参照。
