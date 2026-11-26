#!/bin/bash
# スタッフに配る zip を作る（管理者用）。
#
# 使い方:
#   bash tools/make-dist.sh                 # コミット済みの内容（HEAD）から作る（配るときはこちら）
#   bash tools/make-dist.sh --working-tree  # コミットしていない変更も含めて試しに作る
#
# 管理者の案件（projects/ の中身）、.git、管理者向けの文書・ルール・道具は入れない。
# できた zip は build/moratame-lp-{年月日時分}.zip（コミットした日時の12桁）。build/ には新しい5つだけ残す。
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if [ "${1:-}" = "--working-tree" ]; then
  stamp=$(date +%Y%m%d%H%M)
  # 今の作業中のファイルから一時的なツリーを作る（インデックスやコミットは変えない）
  tmpidx=$(mktemp)
  GIT_INDEX_FILE="$tmpidx" git read-tree HEAD
  GIT_INDEX_FILE="$tmpidx" git add -A
  ref=$(GIT_INDEX_FILE="$tmpidx" git write-tree)
  rm -f "$tmpidx"
  commit="$(git log -1 --format='%h') + 作業中の変更（試し）"
else
  if [ -n "$(git status --porcelain)" ]; then
    echo "注意: コミットしていない変更があります。zip には HEAD（最後のコミット）の内容だけが入ります。"
  fi
  ref=HEAD
  commit=$(git log -1 --format='%h')
  # 版の番号はコミットした日時（年月日時分の12桁）。同じコミットから作り直すと同じ名前になる
  stamp=$(git log -1 --format='%cd' --date=format-local:%Y%m%d%H%M)
fi
name="moratame-lp-${stamp}"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# HEAD の内容を取り出す
git archive --format=tar --prefix="${name}/" "$ref" | tar -x -C "$work"
dir="$work/$name"

# 配らないもの
rm -rf "$dir/projects" "$dir/build" "$dir/feedback" "$dir/.claude/skills/feedback-triage"
rm -f "$dir/.gitignore" "$dir/README.md" \
      "$dir/.claude/rules/git-commit.md" \
      "$dir/docs/admin.md" "$dir/docs/admin-quickstart.md" "$dir/docs/team-rollout.md" "$dir/docs/feedback-log.md" \
      "$dir/tools/make-dist.sh" "$dir/tools/publish-dist.sh" "$dir/tools/update-template.sh" "$dir/tools/collect-feedback.sh"
rm -rf "$dir/tools/git-hooks"

# スタッフの作業場所（空）と進み具合の記録
mkdir -p "$dir/projects"
cat > "$dir/projects/progress.md" <<'EOF'
# 進み具合

この PC での案件の進み具合。工程が進んだら、この表と各案件の節を更新する。

| 案件番号 | 商品 | 工程 | 状態 |
|---|---|---|---|

（まだ案件はありません）
EOF

# フィードバックの置き場所（空）
mkdir -p "$dir/feedback"
cat > "$dir/feedback/README.md" <<'EOF'
# フィードバック

Claude に「フィードバック: 〇〇」と言うと、ここにメモが1件できます。流れは docs/feedback-flow.md を見てください。
EOF

# 版の番号
cat > "$dir/VERSION" <<EOF
${stamp} (${commit})
EOF

mkdir -p "$root/build"
out="$root/build/${name}.zip"
rm -f "$out"
# zip の一番上にフォルダを作らない（Mac のダブルクリックも Windows の「すべて展開」も、zip の名前のフォルダを1つ作って展開するため。
# 一番上にフォルダがあると、Windows ではフォルダが二重になる）
(cd "$dir" && zip -qr -X "$out" . -x '*.DS_Store')
echo "作りました: $out"
echo "版: ${stamp} (${commit})"

# build/ には新しい5つだけ残す
ls -1 "$root/build"/moratame-lp-*.zip 2>/dev/null | sort | sed -e :a -e '$d;N;2,5ba' -e 'P;D' | while read -r f; do rm -f "$f"; done
