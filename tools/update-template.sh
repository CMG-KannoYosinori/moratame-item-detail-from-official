#!/bin/bash
# item-details-template から、テンプレートを取り込み直す（管理者用）。
#
# 使い方:
#   bash tools/update-template.sh <item-details-template のフォルダ>
#
# 取り込み元の 00000html/dist/ と README.md を template/00000html/ に写し、
# template/SOURCE.md のコミットと日付を更新する。ルール（.claude/rules/）は書き直してあるので上書きしない。
set -eu
src="${1:?item-details-template のフォルダを指定してください}"
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$root/template/00000html"

[ -f "$src/00000html/dist/00000.html" ] || { echo "テンプレートが見つかりません: $src/00000html/dist/00000.html" >&2; exit 1; }

commit=$(git -C "$src" log -1 --format='%h')
subject=$(git -C "$src" log -1 --format='%s')
dirty=$(git -C "$src" status --porcelain -- 00000html | head -1)
[ -n "$dirty" ] && echo "注意: 取り込み元の 00000html にコミットしていない変更があります（そのまま写します）"

rm -rf "$dest/dist"
mkdir -p "$dest"
cp -R "$src/00000html/dist" "$dest/dist"
find "$dest" -name .DS_Store -delete
mkdir -p "$dest/dist/images" && touch "$dest/dist/images/.gitkeep"
cp "$src/00000html/README.md" "$dest/README.md"

today=$(date +%Y-%m-%d)
python3 - "$root/template/SOURCE.md" "$commit" "$subject" "$today" <<'EOF'
import re, sys
p, commit, subject, today = sys.argv[1:]
s = open(p, encoding='utf-8').read()
s = re.sub(r'\| コミット \|.*\|', f'| コミット | `{commit}`（{subject}） |', s)
s = re.sub(r'\| 取り込んだ日 \|.*\|', f'| 取り込んだ日 | {today} |', s)
open(p, 'w', encoding='utf-8').write(s)
EOF

echo "取り込みました: $commit $subject"
echo "取り込み元のルールが変わっていないか確かめてください:"
echo "  diff -r \"$src/.claude/rules\" \"$root/.claude/rules\""
