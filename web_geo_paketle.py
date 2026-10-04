#!/usr/bin/env python3
"""web/geo/*.stl dosyalarini TEK bir web/geo.json icinde paketler.

Neden: yayin ortami .stl uzantisini servis etmiyor. Ayrica ikili STL her
ucgende normali de tasiyor (50 bayt); normaller tarayicida hesaplanabildigi
icin atiliyor ve koordinatlar parca sinir kutusuna gore int16'ya
nicemleniyor (~0.001 mm cozunurluk). Sonuc: ~4x kucuk, metin-guvenli.

Kullanim:  python3 web_geo_paketle.py
"""
import os, sys, json, struct, base64
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsim.yollar import kyol                                  # noqa: E402

GEO = kyol("web", "geo")


def stl_oku(yol):
    d = open(yol, "rb").read()
    n = struct.unpack("<I", d[80:84])[0]
    if 84 + n * 50 != len(d):
        raise SystemExit(f"{yol}: STL boyutu tutmuyor")
    ham = np.frombuffer(d[84:], dtype=np.uint8).reshape(n, 50)
    # her ucgen: 12 bayt normal (atilir) + 36 bayt 3 kose + 2 bayt oznitelik
    kose = ham[:, 12:48].copy().view(np.float32).reshape(n * 3, 3)
    return kose


paketler, toplam_ucgen = {}, 0
for ad in sorted(os.listdir(GEO)):
    if not ad.endswith(".stl"):
        continue
    v = stl_oku(os.path.join(GEO, ad))
    mn, mx = v.min(axis=0), v.max(axis=0)
    mrk = (mn + mx) / 2.0
    yari = np.maximum((mx - mn) / 2.0, 1e-6)
    q = np.clip(np.round((v - mrk) / yari * 32767.0), -32767, 32767).astype("<i2")
    paketler[ad[:-4]] = {
        "merkez": [round(float(x), 4) for x in mrk],
        "yari": [round(float(x), 4) for x in yari],
        "ucgen": v.shape[0] // 3,
        "b64": base64.b64encode(q.tobytes()).decode("ascii"),
    }
    toplam_ucgen += v.shape[0] // 3

idx = json.load(open(os.path.join(GEO, "_index.json")))
cikti = {
    "_not": "int16 nicemlenmis kose koordinatlari; v = merkez + q/32767*yari",
    "olcu": idx["olcu"],
    "boncuk": idx["boncuk"],
    "mesh": paketler,
}
yol = kyol("web", "geo.json")
json.dump(cikti, open(yol, "w"), separators=(",", ":"))
kb = os.path.getsize(yol) / 1024
eski = sum(os.path.getsize(os.path.join(GEO, f))
           for f in os.listdir(GEO) if f.endswith(".stl")) / 1024
print(f"{len(paketler)} parca · {toplam_ucgen} ucgen")
print(f"STL toplami {eski:.0f} kB  ->  geo.json {kb:.0f} kB "
      f"({eski/kb:.1f}x kucuk)")
