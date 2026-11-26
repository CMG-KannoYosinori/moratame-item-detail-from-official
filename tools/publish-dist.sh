#!/bin/bash
# 最後のコミットから作った配る zip を、Google Drive の 01_エージェント最新版/ に置く（管理者用）。
# 前の版の zip は 01_エージェント最新版/過去の版/ に移す。同じ名前（同じコミット）の zip は上書きする。
#
# 置き場所はリポジトリに書かず、この PC の git の設定に入れておく（アカウント名がパスに入るため）:
#   git config moratame.distDir "$HOME/Library/CloudStorage/GoogleDrive-（会社のアカウント）/共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作/01_エージェント最新版"
#
# 使い方:
#   bash tools/publish-dist.sh   # 手で置く（post-commit のフックからも呼ばれる）。zip がなければ作る
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

dest=$(git config --get moratame.distDir || true)
if [ -z "$dest" ]; then
  echo "置き場所が設定されていません（git config moratame.distDir \"<01_エージェント最新版 のフォルダ>\"）。"
  exit 1
fi
if [ ! -d "$dest" ]; then
  echo "置き場所が見つかりません（Google Drive が開いていない？）: $dest"
  exit 1
fi

# 最後のコミット（HEAD）の zip を置く（--working-tree で作った試しの zip は置かない）
stamp=$(git log -1 --format='%cd' --date=format-local:%Y%m%d%H%M)
name="moratame-lp-${stamp}.zip"
zip="build/$name"
if [ ! -f "$zip" ]; then
  bash tools/make-dist.sh >/dev/null
fi

# 前の版を 過去の版/ へ
for old in "$dest"/moratame-lp-*.zip; do
  [ -e "$old" ] || continue
  [ "$(basename "$old")" = "$name" ] && continue
  mkdir -p "$dest/過去の版"
  mv -f "$old" "$dest/過去の版/"
  echo "前の版を移しました: 過去の版/$(basename "$old")"
done

cp -f "$zip" "$dest/$name"
echo "置きました: $dest/$name"
