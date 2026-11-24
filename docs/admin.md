# 管理者向けの手順

スタッフに配るフォルダ（zip）の作り方と、テンプレート・スキルの更新のしかた。この文書は配る zip には入らない。

## 役割

| 担当 | すること |
|---|---|
| 管理者 | このリポジトリを git で管理する。スキル・ルール・テンプレート・マニュアルを直す。zip を作って配る。スタッフからの困りごとを集めて直す |
| スタッフ | zip を解凍したフォルダを Claude のアプリで開き、対話で LP を作る。終わった案件を共有の場所に置く |

## zip を作って配る

1. 直したものをコミットする（zip は最後のコミットの内容から作る）。
2. 次を実行する。

   ```sh
   bash tools/make-dist.sh
   ```

   `build/moratame-lp-{日付}.zip` ができる。中のフォルダ名も `moratame-lp-{日付}` になる。
3. 配る前に試す。
   - zip を解凍し、そのフォルダを Claude のアプリの Code で開く。
   - `/moratame-lp` と入力し、工程0の質問が出ることを確かめる。
   - `VERSION` に日付とコミットが入っていることを確かめる。
4. 共有の場所に置き、スタッフに知らせる。知らせる内容: 版（`VERSION`）、変わったこと、**古いフォルダの `projects` を新しいフォルダに移すこと**（[manual.md](manual.md) の「新しい版に入れ替える」）。

### zip に入らないもの

- `projects/` の中身（管理者の案件）。代わりに空の `projects/progress.md` が入る
- `.git`、`.gitignore`、`build/`
- `.claude/rules/git-commit.md`（スタッフは git を使わない）
- `docs/admin.md`（この文書）、`docs/team-rollout.md`
- `tools/make-dist.sh`、`tools/update-template.sh`

入れるものを変えたいときは `tools/make-dist.sh` を直す。

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

## スタッフの作業を集める

- スタッフの作業はスタッフの PC にしか残らない。案件が終わったら `projects/{案件番号}/` をフォルダごと共有の場所に置いてもらう。
- スタッフがつまずいたことを集め、スキル・マニュアルに反映して、次の版で配る。
- スタッフから「どの版を使っているか」を聞くときは、フォルダの `VERSION` を見てもらう。

## スタッフの PC に必要なもの

- Claude のアプリ（Code が使えるプラン）と、Figma をつないだ Claude のアカウント
- Figma の編集できるアカウント（Figma のプランによっては、Claude から Figma を操作できる回数に上限がある）
- Mac の Python 3（最初に使うときに「コマンドライン・デベロッパ・ツール」のインストールを求められることがある。その場合は入れてもらう）
- Google Chrome（あれば、HTML の確認で Claude が画面を撮れる。なくても、ブラウザで開いて目で確認すれば進められる）
