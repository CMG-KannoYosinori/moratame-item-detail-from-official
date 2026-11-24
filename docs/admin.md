# 管理者向けの手順

スタッフに配るフォルダ（zip）の作り方と、テンプレート・スキルの更新のしかた。この文書は配る zip には入らない。

## Google Drive のフォルダ

```
共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作
├── 01_エージェント最新版/      管理者が最新の zip を置く（最新の1つだけ）
│   └── 過去の版/       前の zip を移しておく（なければ作る）
└── 02_案件ごとの作業フォルダ/  スタッフ・管理者が案件ごとに作る作業フォルダ（1案件1フォルダ、1案件1人）
```

- このリポジトリ（git）は Drive に置かない。手元の PC に置く（git の中身が Drive の同期で壊れることがあるため）。
- 管理者自身の実際の案件も、スタッフと同じく `02_案件ごとの作業フォルダ/` で配った版を使って作る（スタッフと同じ条件で使い、問題に気づくため）。このリポジトリの `projects/` は練習・見本用。

## 役割

| 担当 | すること |
|---|---|
| 管理者 | このリポジトリを git で管理する。スキル・ルール・テンプレート・マニュアルを直す。zip を作って配る。スタッフからの困りごとを集めて直す |
| スタッフ | 案件ごとに、`01_エージェント最新版/` の最新の zip を `02_案件ごとの作業フォルダ/` に展開してフォルダ名を変え、Claude のアプリで開いて対話で LP を作る |

## zip を作って配る

1. 直したものをコミットする。**コミットのたびに、配る zip が自動で作り直される**（`build/moratame-lp-{日付}.zip`。中のフォルダ名も `moratame-lp-{日付}`）。zip は最後のコミットの内容から作られ、同じ日のものは上書きされる。
   - 自動で作られないときは、手で `bash tools/make-dist.sh` を実行する。
   - コミットしていない変更も含めて試しに作るときは `bash tools/make-dist.sh --working-tree`。
2. 配る前に試す。
   - zip を解凍し、そのフォルダを Claude のアプリの Code で開く。
   - `/moratame-lp` と入力し、工程0の質問が出ることを確かめる。
   - `VERSION` に日付とコミットが入っていることを確かめる。
3. Google Drive の `01_エージェント最新版/` に置く（Finder で `build/moratame-lp-{日付}.zip` をコピーする）。前の zip は `01_エージェント最新版/過去の版/` に移し、`01_エージェント最新版/` には最新の1つだけを置く。
4. スタッフに知らせる。知らせる内容: 版（`VERSION`）と変わったこと。**作業中の案件は、そのフォルダの版のまま続けてよい**。新しい案件から新しい版を使う。

### zip に入らないもの

- `projects/` の中身（管理者の案件）。代わりに空の `projects/progress.md` が入る
- `.git`、`.gitignore`、`build/`、`README.md`（リポジトリの説明。スタッフ向けは manual.md）
- `.claude/rules/git-commit.md`（スタッフは git を使わない）
- `docs/admin.md`（この文書）、`docs/team-rollout.md`、`docs/feedback-log.md`
- `feedback/`（このリポジトリで集めたフィードバック。zip には空の `feedback/` が入る）、`.claude/skills/feedback-triage/`
- `tools/make-dist.sh`、`tools/update-template.sh`、`tools/collect-feedback.sh`、`tools/git-hooks/`

入れるものを変えたいときは `tools/make-dist.sh` を直す。

### 自動で作る設定

コミットのたびに zip を作るのは、git のフック（`tools/git-hooks/post-commit`）。このリポジトリを clone し直したときは、一度だけ次を実行して有効にする。

```sh
git config core.hooksPath tools/git-hooks
```

止めたいときは `git config --unset core.hooksPath`。フックは zip には入らない。

## テンプレートを取り込み直す

item-details-template が更新されたら:

```sh
bash tools/update-template.sh ~/git-repositories/github-cmg/item-details-template
```

- `template/00000html/dist/` と README が写し直され、[template/SOURCE.md](../template/SOURCE.md) のコミットと日付が更新される。
- ルール（`.claude/rules/`）は CSS で運用する形に書き直してあるので、自動では上書きしない。最後に表示される `diff -r …` で取り込み元のルールとの差を見て、必要なところを手で直す。
- 取り込み直しても、すでに作った案件（`projects/{案件番号}/dist/`）は古いテンプレートのまま。
- 直したらコミットして、zip を作り直して配る。

## スキルやマニュアルを直す

| 直したいもの | 場所 |
|---|---|
| 工程の進め方 | `.claude/skills/{スキル名}/SKILL.md` |
| コーディングのルール | `.claude/rules/` |
| ワイヤーフレームの見た目と動き | `tools/wireframe/` |
| スタッフ向けの使い方 | `docs/manual.md` |
| 要件・決まりごと | `docs/requirements.md` |
| チームで使うまでのプラン | `docs/team-rollout.md` |

Claude に頼んで直してもらってよい（このリポジトリを開いた会話なら、プランの更新やコミットのルールも効く）。

## フィードバックを整理する

流れは [feedback-flow.md](feedback-flow.md)。

1. 各案件フォルダの `feedback/` から、このリポジトリの `feedback/inbox/` に集める。

   ```sh
   bash tools/collect-feedback.sh "$HOME/Library/CloudStorage/GoogleDrive-（会社のアカウント）/共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作/02_案件ごとの作業フォルダ"
   ```

   ファイル名の前に案件フォルダ名が付く。集め済みのものは飛ばすので、何度実行してもよい。
2. Claude に「フィードバックを整理して」と頼む（スキル `feedback-triage`。zip には入らない）。
3. 一覧と対応案を見て、直すものを決める。
4. 直したら [feedback-log.md](feedback-log.md) に記録され、メモは `feedback/done/` に移る。`commit` すると zip が作り直されるので、変わったことと一緒に配る。

## スタッフの作業

- スタッフの作業は Google Drive の `02_案件ごとの作業フォルダ/` にそのまま残る。集める作業は要らない。
- スタッフから「どの版を使っているか」を聞くときは、案件フォルダの `VERSION` を見てもらう。

## スタッフの PC に必要なもの

- Claude のアプリ（Code が使えるプラン）と、Figma をつないだ Claude のアカウント
- Google Drive for desktop（Finder で `共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作` が見えること）
- Figma の編集できるアカウント（Figma のプランによっては、Claude から Figma を操作できる回数に上限がある）
- Mac の Python 3（最初に使うときに「コマンドライン・デベロッパ・ツール」のインストールを求められることがある。その場合は入れてもらう）
- Google Chrome（あれば、HTML の確認で Claude が画面を撮れる。なくても、ブラウザで開いて目で確認すれば進められる）
