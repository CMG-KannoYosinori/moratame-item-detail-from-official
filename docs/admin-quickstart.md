# 簡単マニュアル（管理者向け）

管理者の操作の順番です。くわしい説明は [admin.md](admin.md)、フィードバックの流れは [feedback-flow.md](feedback-flow.md)。この文書は配る zip には入りません。

Google Drive の場所: `共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作`

## 1. 最初の1回だけ

```sh
git clone <このリポジトリ>
cd moratame-item-detail-from-official
git config core.hooksPath tools/git-hooks   # コミットのたびに配る zip を作り直す
```

リポジトリは手元の PC に置きます（Google Drive には置かない）。

## 2. スキルやマニュアルを直す

1. このリポジトリを Claude Code で開き、直したいことを言葉で頼む（例:「工程2の候補に〇〇も出して」）。
2. 直ったら `commit` と入力する。意味ごとにコミットされ、`build/moratame-lp-日付.zip` が自動で作り直される。

## 3. 新しい版を配る

1. 試す: `build/moratame-lp-日付.zip` を解凍し、Claude のアプリの Code で開いて `/moratame-lp` と入力。工程0の質問が出て、`VERSION` に日付とコミットが入っていれば OK。
2. 置く: Drive の `01_エージェント最新版/` にある前の zip を `過去の版/` に移し、新しい zip を置く（最新の1つだけにする）。
3. 知らせる: 版（`VERSION`）と変わったことをスタッフに伝える。作業中の案件は前の版のまま続けてよい、と添える。

zip が自動で作られなかったときは `bash tools/make-dist.sh`。

## 4. フィードバックを集めて直す

1. 「フィードバックを集めて」と頼む。各案件の `feedback/` のメモが `feedback/inbox/` に入る（集め済みは飛ばす）。自分で実行するときは:

   ```sh
   bash tools/collect-feedback.sh "$HOME/Library/CloudStorage/GoogleDrive-（会社のアカウント）/共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作/02_案件ごとの作業フォルダ"
   ```
2. 「フィードバックを整理して」と頼む。一覧と対応案が出る。
3. 直すものを決めて伝える（「全部おすすめどおりで」でもよい）。Claude が直し、`docs/feedback-log.md` に記録して、メモを `feedback/done/` に移す。
4. `commit` → 3 の手順で配る。Claude が作る知らせの文の案を使う。

## 5. テンプレートを取り込み直す

item-details-template が更新されたら:

```sh
bash tools/update-template.sh ~/git-repositories/github-cmg/item-details-template
```

表示される差分を見て、`.claude/rules/` に必要な直しがあれば頼む。`commit` → 3 の手順で配る。

## 6. 自分で案件を作るとき

スタッフと同じく、Drive の `02_案件ごとの作業フォルダ/` に最新の zip を展開して作る（[quickstart.md](quickstart.md)）。このリポジトリの `projects/` は練習・見本用。
