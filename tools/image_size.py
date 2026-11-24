#!/usr/bin/env python3
"""画像の大きさ（幅×高さ）を調べる。Mac・Windows どちらでも、Python の標準の機能だけで動く。

使い方:
    python3 tools/image_size.py 画像 [画像 ...]      （Windows では python または py）

PNG・JPEG・GIF・WebP・SVG に対応。読めないものは「?」と出す。
"""
import re
import struct
import sys
from pathlib import Path


def size_of(path):
    data = Path(path).read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        kind = data[12:16]
        if kind == b"VP8X":
            return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
        if kind == b"VP8L":
            b = data[21:25]
            return (((b[1] & 0x3F) << 8 | b[0]) + 1, ((b[3] & 0xF) << 10 | b[2] << 2 | (b[1] & 0xC0) >> 6) + 1)
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h)
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    text = data[:4096].decode("utf-8", "ignore")
    if "<svg" in text:
        w = re.search(r'<svg[^>]*\bwidth="([\d.]+)', text)
        h = re.search(r'<svg[^>]*\bheight="([\d.]+)', text)
        if w and h:
            return (float(w.group(1)), float(h.group(1)))
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', text)
        if vb:
            return (float(vb.group(1)), float(vb.group(2)))
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        try:
            s = size_of(p)
        except OSError as e:
            print(f"{p}\t? ({e})")
            continue
        print(f"{p}\t{s[0]:g}x{s[1]:g}" if s else f"{p}\t?")


if __name__ == "__main__":
    main()
