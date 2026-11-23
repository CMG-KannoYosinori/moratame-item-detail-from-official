# テンプレート（サブモジュール）の扱い方

このリポジトリでは、モラタメのHTMLテンプレートを **Gitのサブモジュール** として持っています。この文書は、サブモジュールで困らないための手順をまとめたものです。

## 1. どうなっているか

| 項目 | 内容 |
|---|---|
| 置き場所 | `references/moratame/item-details-template/` |
| 元のリポジトリ | https://github.com/CMG-KannoYosinori/item-details-template |
| 使っているブランチ | `main` |
| 設定ファイル | リポジトリ直下の `.gitmodules` |

このリポジトリに保存しているのは、テンプレートの **ファイルではなく「どのバージョン（コミット）を使うか」の記録だけ** です。ファイル本体と履歴は、テンプレートのリポジトリ側にあります。

```
moratame-item-detail-from-official      ← このリポジトリ
├── .gitmodules                          ← テンプレートのURLと置き場所
└── references/moratame/
    └── item-details-template/           ← 中身は別のリポジトリ（コミット番号だけを記録）
```

いま使っているバージョンは、次のコマンドで確認できます。

```sh
git submodule status
```

### 大事なこと

- テンプレートのリポジトリが更新されても、**このリポジトリには自動では反映されません**。取り込む操作をして、コミットするまでは前のバージョンのままです（[4. テンプレートの更新を取り込む](#4-テンプレートの更新を取り込む)）。
- テンプレートの中身は **このリポジトリでは編集しません**。直すときはテンプレートのリポジトリで直します（[5. テンプレートを直したいとき](#5-テンプレートを直したいとき)）。

## 2. 最初に clone するとき

`--recursive` を付けて clone します。

```sh
git clone --recursive <このリポジトリのURL>
```

付け忘れると、`references/moratame/item-details-template/` が空のフォルダになります。そのときは、clone したフォルダで次を実行します。

```sh
git submodule update --init
```

### 接続先（SSH）の設定について

`.gitmodules` のURLは、次のようにSSHの別名（`github.com-excrie`）を使っています。

```
git@github.com-excrie:CMG-KannoYosinori/item-details-template.git
```

この別名は、作成者のPCの `~/.ssh/config` に書いてある設定です。ほかのPCや人が clone すると、別名が見つからず失敗します。その場合は、自分のPCだけでURLを置き換えてから取得します（`.gitmodules` は書き換えません）。

```sh
git config submodule.references/moratame/item-details-template.url \
  git@github.com:CMG-KannoYosinori/item-details-template.git
git submodule update --init
```

## 3. ふだんの `pull`

このリポジトリで `git pull` すると、ほかの人が「テンプレートのバージョンを上げた」記録だけが取り込まれます。テンプレートのファイルを、記録されたバージョンに合わせるには、続けて次を実行します。

```sh
git submodule update
```

毎回打つのが面倒な場合は、一度だけ次を設定します。以降は `pull` のたびに自動で合わせてくれます。

```sh
git config submodule.recurse true
```

## 4. テンプレートの更新を取り込む

テンプレートのリポジトリの `main` が更新され、その内容を使いたいときの手順です。

```sh
# 1. テンプレートの main の最新版を取得する
git submodule update --remote references/moratame/item-details-template

# 2. 何が変わったかを見る
git diff --submodule=log

# 3. 新しいバージョンを使うことを記録する
git add references/moratame/item-details-template
git commit -m "⬆️ テンプレートを最新版に更新"
```

- 手順3のコミットをするまでは、ほかのPCや人からは古いバージョンのままに見えます。
- **すでに作った案件には影響しません。** 案件は、テンプレートの `00000html/` を `projects/{案件番号}/` にコピーして作るため、コピーした時点の内容で固定されます。新しいテンプレートを既存の案件に反映したいときは、案件ごとに手で直します。

## 5. テンプレートを直したいとき

テンプレートの直しは、テンプレートのリポジトリへのコミットになります。おすすめは、テンプレートのリポジトリを別の場所に clone して直す方法です。

1. テンプレートのリポジトリで直して、`main` に push する
2. このリポジトリで [4. テンプレートの更新を取り込む](#4-テンプレートの更新を取り込む) をする

サブモジュールのフォルダの中で直接直すこともできます。その場合は、先にブランチに切り替えてから直してください。`git submodule update` の後は、どのブランチにもいない状態（detached HEAD）になっていて、そのままコミットすると行方不明になりやすいためです。

```sh
cd references/moratame/item-details-template
git switch main
git pull
# 直してコミットする
git push
cd -
git add references/moratame/item-details-template
git commit -m "⬆️ テンプレートの修正を反映"
```

## 6. 困ったとき

| 症状 | 原因と対処 |
|---|---|
| テンプレートのフォルダが空 | `--recursive` なしで clone した。`git submodule update --init` を実行する |
| clone や update で `Could not resolve hostname github.com-excrie` | SSHの別名がないPC。[接続先（SSH）の設定について](#接続先sshの設定について) の手順でURLを置き換える |
| `git status` にテンプレートが ` m` と出る | テンプレートのフォルダ内に、コミットしていない変更がある。中に入って `git status` で確かめる。不要なら `git restore .` で戻す |
| `git status` にテンプレートが ` M`（新しいコミット）と出る | テンプレートのバージョンが記録と違う。使うなら [4.](#4-テンプレートの更新を取り込む) の手順3でコミット、戻すなら `git submodule update` |
| `update --remote` が「上書きされる」と言って止まる | テンプレートのフォルダ内の未コミットの変更と、取り込む更新がぶつかった。変更をテンプレートのリポジトリでコミットするか、`git restore .` で戻してからやり直す |
| フォルダ内でコミットしたはずの変更が消えた | detached HEAD のままコミットした。フォルダ内で `git reflog` を見てコミットを探し、`git switch main` の後に `git cherry-pick <番号>` で拾う |

## 7. 現在の注意点

テンプレートのフォルダ内の `.vscode/settings.json` に、コミットしていない変更（ポート5505、整形の設定）が残っています。この変更をどう扱うかを決めておかないと、`update --remote` で止まることがあります。

- **残す場合：** テンプレートのリポジトリでコミットして push する
- **要らない場合：** フォルダ内で `git restore .vscode/settings.json` で戻す
