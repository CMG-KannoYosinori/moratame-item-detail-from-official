#!/usr/bin/env python3
"""画像を縮小・圧縮する（工程4の画像の用意、工程6の差し替え用）。
Mac・Windows どちらでも、Python の標準の機能と Google Chrome（なければ Microsoft Edge）で動く。Pillow は要らない。

使い方:
    python3 tools/compress_images.py projects/99901/source-images/*.png --out projects/99901/dist/images
    python3 tools/compress_images.py kv.png --out dist/images --max-width 1276 --target-kb 300
    python3 tools/compress_images.py kv.png --out dist/images --format legacy   （WebP を使わず JPEG・PNG にする）
    python3 tools/compress_images.py dist/images --report        （圧縮せず、大きさの一覧と合計だけ出す）
（Windows では python または py）

- 幅が --max-width（標準 1276px）より大きい画像は、縦横の比を保って縮める。小さい画像は大きくしない。
- WebP にする（透明な部分もそのまま保てる）。品質を 85 から下げていき、--target-kb（標準 300KB）以下になったところで止める（60 まで）。
- --format legacy のときは、透明な部分がない画像を JPEG、ある画像を PNG にする（WebP が使えない場所に出すとき用。
  Chrome では PNG の色数を減らせないので、透過のある PNG はあまり軽くならない）。
- 形式が変わると拡張子も変わる（kv.png → kv.webp）。最後に「元 → 新」の一覧を出すので、HTML の参照をそれに合わせる。
- 圧縮しても元より重くなるときは、元のファイルをそのまま写す。
- 元のファイルは変えない。--out には元と別のフォルダを指定する。
"""
import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from screenshot import find_browser  # noqa: E402

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}

PAGE = """<!doctype html><html><body><script>
const opt = %(opt)s;
const img = new Image();
img.onload = () => {
  const s = Math.min(1, opt.maxWidth / img.naturalWidth);
  const w = Math.round(img.naturalWidth * s), h = Math.round(img.naturalHeight * s);
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const x = c.getContext('2d'); x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
  x.drawImage(img, 0, 0, w, h);
  const d = x.getImageData(0, 0, w, h).data; let alpha = false;
  for (let i = 3; i < d.length; i += 4) { if (d[i] < 255) { alpha = true; break; } }
  let type, url, q = null;
  if (opt.format === 'legacy' && alpha) {
    type = 'image/png'; url = c.toDataURL(type);
  } else {
    // WebP（透過も保てる）。legacy のときは透過のない画像を JPEG にする
    type = opt.format === 'legacy' ? 'image/jpeg' : 'image/webp';
    for (q = 0.85; ; q = Math.round((q - 0.05) * 100) / 100) {
      url = c.toDataURL(type, q);
      if (url.length * 0.75 <= opt.targetKb * 1024 || q <= 0.6) break;
    }
  }
  const pre = document.createElement('pre'); pre.id = 'out';
  pre.textContent = JSON.stringify({w, h, ow: img.naturalWidth, oh: img.naturalHeight, alpha, type, q, url});
  document.body.appendChild(pre);
};
img.onerror = () => { const p = document.createElement('pre'); p.id = 'out'; p.textContent = '{"error":"load"}'; document.body.appendChild(p); };
img.src = %(src)s;
</script></body></html>"""


def human(n):
    return f"{n / 1024 / 1024:.2f}MB" if n >= 1024 * 1024 else f"{n / 1024:.0f}KB"


def collect(paths):
    files = []
    for p in map(Path, paths):
        if p.is_dir():
            files += sorted(f for f in p.iterdir() if f.suffix.lower() in EXTS)
        elif p.suffix.lower() in EXTS and p.is_file():
            files.append(p)
        else:
            print(f"飛ばしました（画像ではない、または見つからない）: {p}")
    return files


def compress(browser, work, f, opt):
    data = base64.b64encode(f.read_bytes()).decode()
    src = json.dumps(f"data:{MIME[f.suffix.lower()]};base64,{data}")
    page = work / "page.html"
    page.write_text(PAGE % {"opt": json.dumps(opt), "src": src}, encoding="utf-8")
    cmd = [browser, "--headless=new", "--disable-gpu", f"--user-data-dir={work / 'profile'}",
           "--virtual-time-budget=20000", "--dump-dom", page.as_uri()]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180).stdout
    m = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
    if not m:
        return None
    r = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
    return None if "error" in r else r


def main():
    ap = argparse.ArgumentParser(description="画像を縮小・圧縮する（Chrome / Edge）")
    ap.add_argument("inputs", nargs="+", help="画像のファイル、または画像の入ったフォルダ")
    ap.add_argument("--out", help="書き出すフォルダ（元とは別のフォルダ）")
    ap.add_argument("--max-width", type=int, default=1276)
    ap.add_argument("--target-kb", type=int, default=300)
    ap.add_argument("--format", choices=["webp", "legacy"], default="webp", help="webp（標準）か、JPEG・PNG にする legacy")
    ap.add_argument("--report", action="store_true", help="圧縮せず、大きさの一覧と合計だけ出す")
    a = ap.parse_args()

    files = collect(a.inputs)
    if not files:
        sys.exit("画像がありません。")

    if a.report:
        total = 0
        for f in files:
            n = f.stat().st_size
            total += n
            mark = "  ← 目安より重い" if n > a.target_kb * 1024 else ""
            print(f"{f.name}\t{human(n)}{mark}")
        print(f"合計 {len(files)} 枚 {human(total)}")
        return

    if not a.out:
        sys.exit("--out に書き出すフォルダを指定してください（元のファイルは変えません）。")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if any(f.parent.resolve() == out.resolve() for f in files):
        sys.exit("--out が元の画像と同じフォルダです。元を残すため、別のフォルダを指定してください。")
    browser = find_browser()
    if not browser:
        sys.exit("Google Chrome も Microsoft Edge も見つかりません。人にウェブの道具（Squoosh など）で圧縮してもらってください。")

    opt = {"maxWidth": a.max_width, "targetKb": a.target_kb, "format": a.format}
    ext_of = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
    work = Path(tempfile.mkdtemp(prefix="lp-compress-"))
    rows, renamed, before_total, after_total = [], [], 0, 0
    try:
        for f in files:
            before = f.stat().st_size
            r = compress(browser, work, f, opt)
            if r is None:
                print(f"圧縮できませんでした（元のまま写します）: {f.name}")
                shutil.copy2(f, out / f.name)
                rows.append((f.name, f.name, before, before, "失敗・元のまま"))
                before_total += before
                after_total += before
                continue
            blob = base64.b64decode(r["url"].split(",", 1)[1])
            name = f.stem + ext_of[r["type"]]
            note = f'{r["ow"]}×{r["oh"]} → {r["w"]}×{r["h"]}'
            note += f'、品質{round(r["q"] * 100)}' if r["q"] else ""
            note += "、透過あり" if r["alpha"] else ""
            if len(blob) >= before and r["w"] == r["ow"]:
                name, blob, note = f.name, f.read_bytes(), "元のほうが軽いので元のまま"
            (out / name).write_bytes(blob)
            if name != f.name:
                renamed.append((f.name, name))
            rows.append((f.name, name, before, len(blob), note))
            before_total += before
            after_total += len(blob)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print("元\t新\t元の重さ\t新の重さ\t内容")
    for src, dst, b, n, note in rows:
        mark = "  ← 目安より重い" if n > a.target_kb * 1024 else ""
        print(f"{src}\t{dst}\t{human(b)}\t{human(n)}{mark}\t{note}")
    print(f"合計 {len(rows)} 枚: {human(before_total)} → {human(after_total)}")
    if renamed:
        print("\n拡張子が変わったもの（HTML・CSS の参照を直す）:")
        for s, d in renamed:
            print(f"  {s} → {d}")


if __name__ == "__main__":
    main()
