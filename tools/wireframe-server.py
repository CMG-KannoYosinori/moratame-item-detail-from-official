#!/usr/bin/env python3
"""ワイヤーフレームを表示し、画面で選んだ結果を blocks.md に保存するローカルサーバー。

使い方（リポジトリのどこからでも）:
    python3 tools/wireframe-server.py          # ポート 8000
    python3 tools/wireframe-server.py 8010     # ポートを指定

- リポジトリ全体を http://127.0.0.1:{ポート}/ で配信する（自分のPCからだけ見られる）。
- 書き込めるのは、すでにある projects/{案件番号}/wireframe/blocks.md だけ。
- Python の標準ライブラリだけで動く（インストール不要）。
"""

import functools
import http.server
import os
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = (ROOT / "projects").resolve()
WRITABLE = re.compile(r"^/projects/[A-Za-z0-9_-]+/wireframe/blocks\.md$")
MAX_BYTES = 512 * 1024


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 常に最新のファイルを返す。ページ側はこのヘッダーで「保存できるサーバー」か判断する。
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Wireframe-Save", "1")
        super().end_headers()

    def _host_ok(self):
        # ほかのサイトから名前を偽って届くリクエスト（DNS rebinding）を断る
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        return host in ("127.0.0.1", "localhost")

    def do_GET(self):
        if not self._host_ok():
            return self.send_error(403, "Forbidden host")
        return super().do_GET()

    def do_HEAD(self):
        if not self._host_ok():
            return self.send_error(403, "Forbidden host")
        return super().do_HEAD()

    def do_PUT(self):
        if not self._host_ok():
            return self.send_error(403, "Forbidden host")
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if not WRITABLE.match(path):
            return self.send_error(403, "Only projects/*/wireframe/blocks.md can be saved")
        target = (ROOT / path.lstrip("/")).resolve()
        if PROJECTS not in target.parents or not target.is_file():
            return self.send_error(404, "blocks.md not found")

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BYTES:
            return self.send_error(413, "Body is empty or too large")
        try:
            text = self.rfile.read(length).decode("utf-8")
        except UnicodeDecodeError:
            return self.send_error(400, "Body must be UTF-8")

        # 途中で失敗しても元のファイルが壊れないよう、一時ファイルに書いてから置き換える
        fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".blocks-", suffix=".md")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            os.replace(tmp, target)
        except OSError:
            if os.path.exists(tmp):
                os.remove(tmp)
            return self.send_error(500, "Could not write blocks.md")

        self.send_response(204)
        self.end_headers()
        print(f"保存しました: {target.relative_to(ROOT)}", flush=True)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=str(ROOT))
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError:
        sys.exit(f"ポート {port} は使用中です。別の番号を指定してください（例: python3 tools/wireframe-server.py {port + 1}）")

    print(f"ワイヤーフレームのサーバーを起動しました（止めるときは Ctrl+C）: http://127.0.0.1:{port}/")
    for wf in sorted(PROJECTS.glob("*/wireframe/wireframe.html")):
        print(f"  http://127.0.0.1:{port}/{wf.relative_to(ROOT).as_posix()}")
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n停止しました")


if __name__ == "__main__":
    main()
