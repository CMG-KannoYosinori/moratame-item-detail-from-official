# moratame-item-detail-from-official

商品のブランドサイトを、モラタメの商品詳細ページ（`tamesu.php?project_id=xxx` の「商品概要」）用のLPに作り直すエージェントのリポジトリ。

## スキル

作業は `.claude/skills/` のスキルで進める。入口は **`moratame-lp`**（新しい案件も、途中の案件の続きも）。

| スキル | 工程 |
|---|---|
| `moratame-lp` | 進行役。工程0の聞き取りと、各工程のスキルの呼び出し、人の確認での停止 |
| `brand-content` | 工程1: コンテンツ整理 |
| `lp-wireframe` | 工程2: ワイヤーフレームとブロックの選択 |
| `figma-comp` | 工程3: Figma のデザインカンプ |
| `moratame-html` | 工程4・5: HTML と確認 |
| `lp-revise` | 工程6: HTML を作った後の修正（メーカーからの戻しなど。何回でも） |

人向けの使い方は [docs/manual.md](docs/manual.md)、修正の流れは [docs/revision-flow.md](docs/revision-flow.md)。

## まず読むもの

- [docs/requirements.md](docs/requirements.md) — 要件と工程（工程0〜5）。作業の決まりはすべてここにある
- [projects/progress.md](projects/progress.md) — 案件ごとの進み具合。**作業を始める前に読み、工程が進んだら更新する**
- [docs/team-rollout.md](docs/team-rollout.md) — チームで使うまでのプラン。よりよい案が出たら更新する（管理者の手元だけにある）
- [docs/admin.md](docs/admin.md) — 管理者向け（配る zip の作り方、テンプレートの取り込み直し。管理者の手元だけにある）

## 工程（詳しくは requirements.md の2章）

| 工程 | 内容 | 人の確認 |
|---|---|---|
| 0 | 聞き取り（FigmaのURL、案件番号、ブランドサイト、対象商品、配送の条件）。**FigmaのURLは毎回聞く** | — |
| 1 | ブランドサイトの内容を `projects/{案件番号}/wireframe/content.md` に整理 | — |
| 2 | `wireframe.html` と `blocks.md` を作る。人が画面で選んで保存し、対話で見直す | ✅ |
| 3 | Figma に PC 640px / SP 375px のカンプを作る | ✅ 承認 |
| 4 | テンプレートからHTMLを作る | — |
| 5 | 確認 | ✅ |
| 6 | 修正対応（メーカーからの戻しなど。何回でも）。受け取ったファイルと直す前の版を `revisions/round-N/` に残し、blocks.md・カンプ・HTML をそろえて直し、`changes.md` に記録 | ✅ |

## 決まりごと

- 作業フォルダは `projects/{案件番号}/`。テンプレートは `template/00000html/dist/`（item-details-template から写したもの。**編集しない**。取り込み元は `template/SOURCE.md`）。
- SCSS は使わず CSS だけで運用する。案件のスタイルは `dist/styles/style.css` の最後の区切りより下に書く（`.claude/rules/project-css.md`）。
- コーディングのルールは `.claude/rules/`。SP の基準は 375px。
- ブランドサイトを基準にする。過去のモラタメのページは形式の参考だけ。
- 薬機法・景表法に関わる表現は言い換えない。体への働きをうたう表現は人に確認する。
- このフォルダは、管理者の手元では git で管理し、スタッフには zip で配る。**git で管理されていない（`.git` がない）ときは、コミットや push の話をしない。** git で管理されているときのコミットは `.claude/rules/git-commit.md` に従う（ユーザーが `commit` と言ったときだけ）。

## プレビュー

- ワイヤーフレームの見た目と動きは共通の `tools/wireframe/`（`wireframe.js`・`wireframe.css`・`frame.css`）が受け持つ。新しい案件は `tools/wireframe/template.html` と `blocks.template.md` から作る。
- ワイヤーフレームは `python3 tools/wireframe-server.py` を起動し、表示された URL（`http://127.0.0.1:8000/...`）で開く。画面で選んだ内容を `blocks.md` に保存できる。
- HTML（`dist/`）も同じサーバーで開く。SP の幅で見るときは `tools/preview.html?src=/projects/{案件番号}/dist/{案件番号}.html&w=375`（Chrome のウィンドウは約500px より狭くできないため）。
- ユーザーは VS Code の Live Server（ポート5500）を使うこともある。Live Server は最初の `</body>` の前にスクリプトを差し込むので、インラインのJSに閉じタグを文字どおり書かない（`<\/body>` と書く）。

## Figma

- Figma の MCP を使う。ファイルの操作の前に `create_session` を呼ぶ。
- `use_figma` の前に Figma のスキル `figma-use` と `figma-generate-design` を読み込む（`get_figma_skill` で `skill://figma/figma-use/SKILL.md` などを読む）。
- ブランドサイトの画像は `upload_assets` で「素材」ページに上げ、カンプでは imageHash やクローンで使う。
