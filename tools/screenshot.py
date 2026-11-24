#!/usr/bin/env python3
"""HTML を決めた幅で表示して、スクリーンショットを撮る（工程5の確認用）。
Mac・Windows どちらでも、Python の標準の機能と Google Chrome（なければ Microsoft Edge）で動く。

先に tools/wireframe-server.py を起動しておく。

使い方:
    python3 tools/screenshot.py /projects/99901/dist/99901.html          （Windows では python または py）
    python3 tools/screenshot.py /projects/99901/dist/99901.html --widths 375 --out shots

- 幅ごと（標準は 640・375・320）に、縦 1300px ずつの画像に分けて保存する（縦に長い画像は細部が見えないため）。
  保存先は --out（標準は一時フォルダ）。保存したファイルの一覧を表示する。
- Chrome のウィンドウは約500px より狭くできないので、tools/preview.html の iframe で幅を決める。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser():
    for c in CANDIDATES:
        if c and Path(c).is_file():
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    return None


def run(browser, profile, args):
    cmd = [browser, "--headless=new", "--hide-scrollbars", "--disable-gpu", f"--user-data-dir={profile}",
           "--virtual-time-budget=8000"] + args
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)


def main():
    ap = argparse.ArgumentParser(description="HTML を決めた幅で撮る")
    ap.add_argument("src", help="サーバーから見た HTML のパス（例: /projects/99901/dist/99901.html）")
    ap.add_argument("--widths", default="640,375,320")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--segment", type=int, default=1300)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    browser = find_browser()
    if not browser:
        sys.exit("Google Chrome も Microsoft Edge も見つかりません。人にブラウザで開いて見てもらってください。")
    out = Path(a.out or tempfile.mkdtemp(prefix="lp-shot-"))
    out.mkdir(parents=True, exist_ok=True)
    profile = tempfile.mkdtemp(prefix="lp-shot-profile-")
    src = urllib.parse.quote(a.src, safe="/")
    base = f"http://127.0.0.1:{a.port}/tools/preview.html?src={src}"
    saved = []
    try:
        for w in [int(x) for x in a.widths.split(",")]:
            # 1. ページの高さを知る（preview.js が body の data-height に書く）
            dom = run(browser, profile, ["--dump-dom", f"{base}&w={w}"]).stdout
            m = re.search(r'data-height="(\d+)"', dom)
            if not m:
                sys.exit(f"ページの高さが分かりませんでした。サーバー（ポート {a.port}）が起動しているか確かめてください。")
            height = int(m.group(1))
            # 2. 縦 segment ずつ撮る
            win_w = max(w, 520)
            for i, y in enumerate(range(0, height, a.segment)):
                h = min(a.segment, height - y)
                f = out / f"w{w}_{i + 1:02d}.png"
                run(browser, profile, [f"--window-size={win_w},{h}", f"--screenshot={f}", f"{base}&w={w}&y={y}&h={h}"])
                if f.exists():
                    saved.append(f)
            print(f"幅 {w}px: 高さ {height}px")
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    for f in saved:
        print(f)


if __name__ == "__main__":
    main()
