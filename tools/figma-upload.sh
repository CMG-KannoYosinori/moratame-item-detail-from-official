#!/bin/bash
# Figma の upload_assets で受け取った URL に、素材のファイルを送る。
#
# 使い方:
#   bash tools/figma-upload.sh 対応表.tsv
#
# 対応表.tsv は「ファイルのパス<TAB>submitUrl」を1行ずつ書いたもの。
# multipart で送るので、ファイル名が Figma のレイヤー名になる。
# 結果（imageHash と placedOnNodeId）を1行ずつ表示する。
set -u
list="${1:?対応表のファイルを指定してください}"
while IFS=$'\t' read -r file url; do
  [ -z "$file" ] && continue
  case "$file" in
    *.svg) type=image/svg+xml ;;
    *.jpg|*.jpeg) type=image/jpeg ;;
    *.webp) type=image/webp ;;
    *.gif) type=image/gif ;;
    *) type=image/png ;;
  esac
  result=$(curl -s -X POST -F "file=@${file};type=${type}" "$url")
  echo "$(basename "$file") -> ${result}"
done < "$list"
