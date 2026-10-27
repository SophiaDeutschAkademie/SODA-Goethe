#!/usr/bin/env python3
"""fonts/pretendard-soda.woff neu erzeugen (Teilmenge von Pretendard mit allen Zeichen aus template.html und data/).

python3 digital-src/make-font.py PretendardVariable.ttf
PretendardVariable.ttf: https://github.com/orioncactus/pretendard (packages/pretendard/dist/public/variable/)
Lizenz: SIL Open Font License 1.1 (fonts/Pretendard-OFL.txt)
"""
import glob
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
chars = set()
for p in [os.path.join(HERE, "template.html")] + glob.glob(os.path.join(HERE, "data", "mt*.json")):
    chars |= set(open(p, encoding="utf-8").read())
base = set(range(0x20, 0x7F)) | set(range(0xA0, 0x180)) | set(range(0x2010, 0x2028)) | set(range(0x2030, 0x203B))
base |= {0x20AC, 0x2190, 0x2191, 0x2192, 0x2193, 0x2605, 0x2713, 0x2717, 0x00B7}
cps = sorted(base | {ord(c) for c in chars if ord(c) >= 0x20})
font = TTFont(src)
opts = subset.Options()
opts.flavor = "woff"
opts.layout_features = ["kern", "liga", "calt", "locl", "tnum", "case", "ccmp", "mark", "mkmk"]
opts.name_IDs = ["*"]
opts.notdef_outline = True
s = subset.Subsetter(opts)
s.populate(unicodes=cps)
s.subset(font)
font.flavor = "woff"
out = os.path.join(HERE, "fonts", "pretendard-soda.woff")
font.save(out)
print(out, os.path.getsize(out), "Bytes,", len(cps), "Zeichen")
