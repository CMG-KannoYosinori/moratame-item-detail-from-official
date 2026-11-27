# テンプレートの取り込み元

このフォルダは [item-details-template](https://github.com/CMG-KannoYosinori/item-details-template) から、案件で使う部分だけを写したもの。**このリポジトリではここを直接編集しない。** テンプレートを直すときは item-details-template で直し、管理者が取り込み直す。

| 項目 | 内容 |
|---|---|
| 取り込み元 | https://github.com/CMG-KannoYosinori/item-details-template |
| コミット | `713982d`（📝 READMEにClaude用ルールの構成と同期の注意を追記） |
| 取り込んだ日 | 2026-11-24 |

## 写したもの

| このリポジトリ | 取り込み元 | 備考 |
|---|---|---|
| `template/00000html/dist/` | `00000html/dist/` | HTML・CSS（コンパイル済み）・JS |
| `template/00000html/README.md` | `00000html/README.md` | 部品とクラス名の説明として読む。**SCSS・Live Sass の手順はこのリポジトリでは使わない**（CSS だけで運用する） |
| `.claude/rules/` の `character-entities.md`・`html-charset.md` | `.claude/rules/` | 対象のパスだけ変えて写した |
| `.claude/rules/modern-bem.md` | `.claude/rules/` | CSS で運用するこのリポジトリに関係する部分（命名、State、やってはいけないこと）だけを残し、例を案件のクラス名にした（2026-11-27） |
| `.claude/rules/project-css.md`・`design-comp.md` | `.claude/rules/` | CSS で運用する形・SP 375px に書き直した |

`src/`（SCSS）は写していない。案件のスタイルは `dist/styles/style.css` の最後に書く（`.claude/rules/project-css.md`）。

## 取り込み直すとき（管理者）

```sh
bash tools/update-template.sh ~/git-repositories/github-cmg/item-details-template
```

`dist/` と README を写し直し、この表のコミットと日付を更新する。ルール（`.claude/rules/`）は書き直してあるので自動では上書きしない。取り込み元のルールが変わっていたら、差分を見て手で反映する。
