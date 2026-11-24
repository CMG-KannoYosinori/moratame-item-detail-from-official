---
paths:
  - "projects/**/*.html"
---

# 埋め込み用 HTML に charset は書かない

`projects/{案件番号}/dist/*.html` は、Shift-JIS の CMS と UTF-8 の CMS の両方に埋め込むローカルファイルである。文字コードの宣言は埋め込み先（HTTP ヘッダ、または親テンプレートの `head`）が持つ。このファイルには `<meta charset>` を書かない。

`charset=utf-8` を書いておくと、Shift-JIS で配信されたときにブラウザがバイト列を UTF-8 と解釈し、日本語が文字化けする。

- ファイル自体は UTF-8 で保存する
- Shift-JIS にない記号（`®` `×` など）は数値文字参照のままにする
- ローカルプレビューで文字化けするときは HTML に宣言を足さず、プレビューサーバの `Content-Type` に `charset=utf-8` を付ける
