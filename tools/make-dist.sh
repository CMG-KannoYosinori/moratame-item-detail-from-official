#!/bin/bash
# スタッフに配る zip を作る（管理者用）。
#
# 使い方:
#   bash tools/make-dist.sh                 # コミット済みの内容（HEAD）から作る（配るときはこちら）
#   bash tools/make-dist.sh --working-tree  # コミットしていない変更も含めて試しに作る
#
# 管理者の案件（projects/ の中身）、.git、管理者向けの文書・ルール・道具は入れない。
# できた zip は build/ に置く。
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

date=$(date +%Y%m%d)
if [ "${1:-}" = "--working-tree" ]; then
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
fi
name="moratame-lp-${date}"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# HEAD の内容を取り出す
git archive --format=tar --prefix="${name}/" "$ref" | tar -x -C "$work"
dir="$work/$name"

# 配らないもの
rm -rf "$dir/projects" "$dir/build"
rm -f "$dir/.gitignore" \
      "$dir/.claude/rules/git-commit.md" \
      "$dir/docs/admin.md" "$dir/docs/team-rollout.md" \
      "$dir/tools/make-dist.sh" "$dir/tools/update-template.sh"
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

# 版の番号
cat > "$dir/VERSION" <<EOF
${date} (${commit})
EOF

mkdir -p "$root/build"
out="$root/build/${name}.zip"
rm -f "$out"
(cd "$work" && zip -qr -X "$out" "$name" -x '*.DS_Store')
echo "作りました: $out"
echo "版: ${date} (${commit})"
