#!/bin/bash
# 各案件フォルダの feedback/ にあるメモを、このリポジトリの feedback/inbox/ に集める（管理者用）。
#
# 使い方:
#   bash tools/collect-feedback.sh "<Google Drive の 案件 フォルダ>"
#   例: bash tools/collect-feedback.sh ~/Library/CloudStorage/GoogleDrive-（会社のアカウント）/共有ドライブ/design2/MOD_design/モラタメ商品概要LP_AIエージェント制作/02_案件ごとの作業フォルダ
#
# 集めたファイルは「案件フォルダ名__元のファイル名」で inbox/ に写す。
# inbox/ か done/ に同じ名前があるもの（集め済み）は写さない。元のファイルは消さない。
set -eu
src="${1:?案件フォルダが並んでいるフォルダを指定してください}"
root="$(cd "$(dirname "$0")/.." && pwd)"
inbox="$root/feedback/inbox"
done_dir="$root/feedback/done"
mkdir -p "$inbox" "$done_dir"

[ -d "$src" ] || { echo "フォルダが見つかりません: $src" >&2; exit 1; }

new=0; skip=0
for f in "$src"/*/feedback/*.md; do
  [ -e "$f" ] || continue
  [ "$(basename "$f")" = "README.md" ] && continue
  case_dir="$(basename "$(dirname "$(dirname "$f")")")"
  name="${case_dir}__$(basename "$f")"
  if [ -e "$inbox/$name" ] || [ -e "$done_dir/$name" ]; then
    skip=$((skip + 1)); continue
  fi
  cp "$f" "$inbox/$name"
  echo "集めました: $name"
  new=$((new + 1))
done
echo "新しく集めたもの: ${new} 件（集め済みで飛ばしたもの: ${skip} 件）"
