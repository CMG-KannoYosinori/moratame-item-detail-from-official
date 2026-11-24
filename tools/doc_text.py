#!/usr/bin/env python3
"""Word（.docx）・Excel（.xlsx）・PowerPoint（.pptx）から文字を取り出す。
Mac・Windows どちらでも、Python の標準の機能だけで動く（修正の依頼を読むときに使う）。

使い方:
    python3 tools/doc_text.py ファイル      （Windows では python または py）

- Word: 段落ごとに1行。変更履歴で足した文字（挿入）は [+…+]、消した文字（削除）は [-…-] で示す。コメントは最後にまとめる。
- Excel: シートごとに、セル番地と値を1行ずつ。
- PowerPoint: スライドごとに文字を出す（図への手書きの書き込みは読めない）。
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def docx(z):
    out = []
    root = ET.fromstring(z.read("word/document.xml"))
    for p in root.iter(W + "p"):
        parts = []
        for el in p.iter():
            if el.tag == W + "t":
                parts.append(el.text or "")
            elif el.tag == W + "delText":
                parts.append("[-" + (el.text or "") + "-]")
            elif el.tag == W + "tab":
                parts.append("\t")
        line = "".join(parts)
        # 挿入（w:ins）の中の文字を示す
        ins = ["".join(t.text or "" for t in i.iter(W + "t")) for i in p.iter(W + "ins")]
        for s in ins:
            if s:
                line = line.replace(s, "[+" + s + "+]", 1)
        out.append(line)
    if "word/comments.xml" in z.namelist():
        out.append("\n--- コメント ---")
        for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
            text = "".join(t.text or "" for t in c.iter(W + "t"))
            out.append(f"{c.get(W + 'author', '')}: {text}")
    return "\n".join(out)


def xlsx(z):
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
            shared.append("".join(t.text or "" for t in si.iter(S + "t")))
    names = {}
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    for i, sh in enumerate(wb.iter(S + "sheet"), 1):
        names[f"xl/worksheets/sheet{i}.xml"] = sh.get("name")
    out = []
    for path in sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
        out.append(f"=== {names.get(path, path)} ===")
        for c in ET.fromstring(z.read(path)).iter(S + "c"):
            v = c.find(S + "v")
            is_ = c.find(S + "is")
            if c.get("t") == "s" and v is not None:
                val = shared[int(v.text)]
            elif is_ is not None:
                val = "".join(t.text or "" for t in is_.iter(S + "t"))
            elif v is not None:
                val = v.text
            else:
                continue
            out.append(f"{c.get('r')}\t{val}")
    return "\n".join(out)


def pptx(z):
    out = []
    slides = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                    key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
    for n in slides:
        out.append(f"=== {n.rsplit('/', 1)[1]} ===")
        for p in ET.fromstring(z.read(n)).iter(A + "p"):
            line = "".join(t.text or "" for t in p.iter(A + "t"))
            if line:
                out.append(line)
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "word/document.xml" in names:
            text = docx(z)
        elif "xl/workbook.xml" in names:
            text = xlsx(z)
        elif any(n.startswith("ppt/slides/") for n in names):
            text = pptx(z)
        else:
            sys.exit("Word・Excel・PowerPoint のファイルではありません")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
