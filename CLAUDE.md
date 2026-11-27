# moratame-item-detail-from-official

商品のブランドサイトを、モラタメの商品詳細ページ（`tamesu.php?project_id=xxx` の「商品概要」）用のLPに作り直すエージェントのリポジトリ。

## 言葉

**使う人との対話は、いつも日本語にする。** 質問、説明、作業の途中で書く短い報告、考えた内容の要約、エラーの説明も日本語で書く。

- ブランドサイト・エラーの文・ツールの結果が英語でも、日本語に直して伝える。英語のまま引くのは、コマンド、ファイル名、コード、画面のボタンの名前など、そのままでないと困るものだけにする。
- `content.md`・`blocks.md`・`changes.md`・フィードバックのメモなど、Claude が書く文書も日本語で書く（ブランドサイトの英語の商品名やキャッチコピーは、原文のまま載せる）。
- 長い作業の後や、要約から再開したときも日本語を続ける。使う人が英語で話しかけたときだけ、英語で答えてよい。

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
| `lp-feedback` | このツールへのフィードバックを `feedback/` に残す（「フィードバック: 〜」と言われたとき） |
| `feedback-triage` | （管理者用、zip に入らない）集めたフィードバックを整理して直す |

人向けの使い方は [docs/manual.md](docs/manual.md)（簡単マニュアルは [docs/quickstart.md](docs/quickstart.md)、管理者向けは docs/admin-quickstart.md）、修正の流れは [docs/revision-flow.md](docs/revision-flow.md)、フィードバックの流れは [docs/feedback-flow.md](docs/feedback-flow.md)。

### スキルの読み方

スキルとルールに書いてあることは、次の2つに分かれる。

- **決まり（変えない）:** 成果物（content.md・blocks.md・カンプ・HTML・画像など）の中身・名前・置き場所、人の確認（✅）で止まること、表現の扱い（薬機法・景表法など）、`.claude/rules/` のルール。
- **手順（目安）:** そこにたどり着くやり方（道具の呼び方、確かめ方、作業の順番）。今の道具で迷わないように書いたもの。同じ成果物を、より確かに・早く作れるやり方があれば変えてよい。変えたときは、何をなぜ変えたかを人に短く伝える。スキルを直したほうがよさそうなら `lp-feedback` で残す。

道具の制約への回避策には「2026-11 時点」のように時点を書いてある。道具が変わって要らなくなっていれば、使わなくてよい。

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
- ワイヤーフレームは `python3 tools/wireframe-server.py`（Windows では `python`）を起動し、表示された URL（`http://127.0.0.1:8000/...`）で開く。画面で選んだ内容を `blocks.md` に保存できる。
- HTML（`dist/`）も同じサーバーで開く。SP の幅で見るときは `tools/preview.html?src=/projects/{案件番号}/dist/{案件番号}.html&w=375`（Chrome のウィンドウは約500px より狭くできないため）。
- ユーザーは VS Code の Live Server（ポート5500）を使うこともある。Live Server は最初の `</body>` の前にスクリプトを差し込むので、インラインのJSに閉じタグを文字どおり書かない（`<\/body>` と書く）。

## Mac と Windows

使う人には Mac の人も Windows の人もいる。どちらでも動くように、決まった道具を使う。

| すること | 使うもの |
|---|---|
| Python を動かす | Mac は `python3`。Windows は `python`（なければ `py`）。最初に `python3 --version` などで、どれが動くか確かめてから使う |
| コマンド | Bash（Windows の Claude Code では Git Bash）。`cp`・`mkdir -p`・`curl` などはどちらでも使える。Mac だけのコマンド（`sips`、`textutil`、`open` など）は使わない |
| 画像の大きさを調べる | `tools/image_size.py` |
| 画像を縮小・圧縮する | `tools/compress_images.py`（Chrome / Edge で動く。Pillow は要らない） |
| Word・Excel・PowerPoint の文字を読む | `tools/doc_text.py`（Word の変更履歴とコメントも出る） |
| HTML のスクリーンショット | `tools/screenshot.py`（Chrome、なければ Edge を自動で探す。Pillow は要らない） |
| プレビューのサーバー | `tools/wireframe-server.py` |

ファイル名・フォルダ名には、空白と `/ \ : * ? " < > |` を使わない（Windows で使えないため）。案件フォルダの名前は `案件番号_商品名`（決まりは docs/manual.md の「案件フォルダの名前の決まり」）。Claude が作るファイル名（画像など）は、半角の英小文字・数字・`-` にする（例: `product-box.png`）。

## Figma

- Figma の MCP を使う。ファイルの操作の前に `create_session` を呼ぶ。
- `use_figma` の前に Figma のスキル `figma-use` と `figma-generate-design` を読み込む（`get_figma_skill` で `skill://figma/figma-use/SKILL.md` などを読む）。
- ブランドサイトの画像は `upload_assets` で「素材」ページに上げ、カンプでは imageHash やクローンで使う。
