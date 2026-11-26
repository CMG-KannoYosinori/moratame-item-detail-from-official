# moratame-item-detail-from-official

商品のブランドサイトをもとに、モラタメの商品詳細ページ（`tamesu.php?project_id=xxx` の「商品概要」の部分）の LP を作る AI エージェントです。Claude Code のスキルとして動き、人と対話しながら、ブランドサイトの整理 → ワイヤーフレーム → Figma のデザインカンプ → HTML まで進めます。

このリポジトリはエージェントの開発・管理用です。実際の制作では、管理者がここから配布用の zip を作り、Google Drive で配ります。

## 工程

| 工程 | 内容 | スキル | 人の確認 |
|---|---|---|---|
| 0 | 聞き取り（Figma の URL、案件番号、ブランドサイト、対象商品、配送の条件） | `moratame-lp` | — |
| 1 | ブランドサイトの内容（文言・商品・素材・トンマナ・表現の注意）を整理 | `brand-content` | — |
| 2 | ワイヤーフレームを作り、使うブロックと商品を画面で選んでもらう | `lp-wireframe` | ✅ 選択 |
| 3 | Figma に PC 640px / SP 375px のデザインカンプを作る | `figma-comp` | ✅ 承認 |
| 4・5 | テンプレートから HTML・CSS を作り、確認する | `moratame-html` | ✅ 最終確認 |
| 6 | HTML の後の修正（メーカーからの戻しなど。何回でも） | `lp-revise` | ✅ 修正の確認 |

入口は `moratame-lp` で、各工程のスキルを順に呼び、人の確認が必要なところで止まります。ほかに、フィードバックを残す `lp-feedback` と、管理者がフィードバックを整理する `feedback-triage` があります。

## 必要なもの

Mac・Windows のどちらでも動きます。

- Claude Code（Claude のアプリの Code、または VS Code などの拡張機能）。Windows では Git for Windows も必要（Claude Code がコマンドを動かすのに使う）
- Figma のアカウントと、Claude のアカウントへの Figma の接続（claude.ai のコネクタ）
- Python 3（Mac は最初から入っている。Windows は python.org から入れる）。道具は Python の標準の機能だけで動く
- Google Chrome または Microsoft Edge（HTML の確認でスクリーンショットを撮るのに使う）

Node.js・npm・Pillow などは要りません（CSS は SCSS を使わずに直接書きます）。Mac だけのコマンドは使わず、`tools/` の Python の道具（`image_size.py`・`doc_text.py`・`screenshot.py`）を使います。

## 使い方（管理者）

```sh
git clone <このリポジトリ>
cd moratame-item-detail-from-official
git config core.hooksPath tools/git-hooks   # コミットのたびに配布用の zip を作り直す
git config moratame.distDir "<Drive の 01_エージェント最新版 のフォルダ>"   # できた zip を Drive に自動で置く（docs/admin.md）
```

このフォルダを Claude Code で開き、`/moratame-lp` と入力すると始まります。`projects/` は練習・見本の案件の置き場所です（`99901` サポートミート）。

ワイヤーフレームや HTML のプレビュー:

```sh
python3 tools/wireframe-server.py
# http://127.0.0.1:8000/projects/99901/wireframe/wireframe.html
# http://127.0.0.1:8000/projects/99901/dist/99901.html
# SP の幅: http://127.0.0.1:8000/tools/preview.html?src=/projects/99901/dist/99901.html&w=375
```

## 配布と運用

```
このリポジトリ（管理者の PC）
  ↓ commit（git のフックで build/moratame-lp-{年月日時分}.zip ができる）
  ↓ 自動で置く（tools/publish-dist.sh。前の zip は 過去の版/ へ）
Google Drive: 共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作/
  ├── 01_エージェント最新版/        最新の zip（前のものは 過去の版/ へ）
  └── 02_案件ごとの作業フォルダ/    案件ごとに最新の zip を展開して使う（1案件1フォルダ・1人）
        └── 99902_牛乳石鹸AKA/
```

- スタッフは git を使いません。案件を始めるたびに最新の zip を展開し、フォルダを Claude のアプリで開いて使います（[docs/manual.md](docs/manual.md)）。
- 配布用の zip には、`projects/` の中身、`.git`、管理者向けの文書・スキル・道具は入りません（`tools/make-dist.sh`）。
- 使った人のフィードバックは各案件フォルダの `feedback/` に残り、管理者が `tools/collect-feedback.sh` で集めて整理します（[docs/feedback-flow.md](docs/feedback-flow.md)）。

操作の順番は [docs/admin-quickstart.md](docs/admin-quickstart.md)、くわしい手順は [docs/admin.md](docs/admin.md)。

## フォルダ構成

```
.
├── CLAUDE.md                 Claude Code が最初に読む案内
├── .claude/
│   ├── skills/               工程ごとのスキル
│   └── rules/                コーディングのルール（文字参照、charset、案件の CSS、Modern BEM、カンプの確認、コミット）
├── docs/
│   ├── requirements.md       要件と工程の決まり（作業の正）
│   ├── quickstart.md         使う人向けの簡単マニュアル（操作の順番だけ）
│   ├── manual.md             使う人向けのマニュアル
│   ├── revision-flow.md      修正の流れ（工程6）
│   ├── feedback-flow.md      フィードバックの流れ
│   ├── admin-quickstart.md   管理者向けの簡単マニュアル（配布しない）
│   ├── admin.md              管理者向けの手順（配布しない）
│   ├── team-rollout.md       チームで使うまでのプラン（配布しない）
│   └── feedback-log.md       フィードバックの記録（配布しない）
├── template/                 HTML テンプレート（item-details-template から写したもの。編集しない）
├── tools/
│   ├── wireframe/            ワイヤーフレームのひな形と共通の CSS・JS
│   ├── wireframe-server.py   プレビューと blocks.md への保存をするローカルサーバー
│   ├── preview.html          HTML を決めた幅（375px など）で表示する
│   ├── screenshot.py         HTML を幅ごと・縦に分けて撮る（Chrome / Edge）
│   ├── image_size.py         画像の大きさを調べる
│   ├── doc_text.py           Word・Excel・PowerPoint の文字を取り出す
│   ├── figma-upload.sh       素材を Figma に上げる
│   ├── make-dist.sh          配布用の zip を作る（配布しない）
│   ├── publish-dist.sh       できた zip を Google Drive に置く（配布しない）
│   ├── collect-feedback.sh   各案件フォルダのフィードバックを集める（配布しない）
│   ├── update-template.sh    テンプレートを取り込み直す（配布しない）
│   └── git-hooks/            コミットのたびに zip を作るフック（配布しない）
├── projects/                 案件（このリポジトリでは練習・見本）と進み具合 progress.md
└── feedback/                 集めたフィードバック（inbox/ と done/）
```

1つの案件の中身:

```
projects/{案件番号}/
├── wireframe/   content.md（ブランドサイトの整理）、blocks.md（選んだブロックと商品）、wireframe.html
├── design/      承認したカンプの PNG（PC・SP）
├── dist/        納品物（{案件番号}.html、images/、styles/style.css）
├── changes.md   修正の記録
└── revisions/   修正の回ごとの受け取ったファイル（request/）と直す前の版（before/）
```

## テンプレート

[item-details-template](https://github.com/CMG-KannoYosinori/item-details-template) の `00000html/dist/` を `template/` に写して使っています。取り込み元のコミットは [template/SOURCE.md](template/SOURCE.md) にあります。テンプレートが更新されたら、管理者が次で取り込み直します。

```sh
bash tools/update-template.sh <item-details-template のフォルダ>
```

案件のスタイルは、`dist/styles/style.css` の最後の区切りより下に、`.p{案件番号} .p{案件番号}-project__名前` の形で書きます（[.claude/rules/project-css.md](.claude/rules/project-css.md)）。

## コミット

gitmoji を付け、意味ごとに分けてコミットします（[.claude/rules/git-commit.md](.claude/rules/git-commit.md)）。Claude Code では `commit` と入力すると、このルールでコミットします。
