#!/usr/bin/env python3
"""ESNEK BANTIN YOLU acik mi — namluda cakisan parca var mi?

v2.1'de namlunun disina eklenen durdurma takozu (Ro..Ro+12) tam bandin
gectigi yarıcapta (z = r_bant) duruyordu ve bandi engelliyordu. Bu betik
bandin capraz pimden agiz ankrajina kadarki yolunu ornekleyip namlu
katisiyla kesisip kesismedigine bakar.

Kullanim:  freecadcmd cad/kontrol_bant_yolu.py
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
sek = Part.Shape(); sek.read(kyol("cad", "V4_namlu.step"))

rb = P["r_bant"]
d_ger = P["bant_OD"] / math.sqrt(P["lam"])        # gergin bantta cap kuculur
y0 = P["y_capraz0"]                                # kurulu capraz pim
y1 = P["y_ankraj"] - P["pim_geri"]                 # agiz ankraj pimi
print(f"bant yarıcapi z = +-{rb:.1f} mm · gergin cap {d_ger:.1f} mm")
print(f"yol: y {y0:.1f} .. {y1:.1f} (kurulu capraz pimden agiz pimine)\n")

carp = []
N = 120
for s in (+1, -1):
    for i in range(N + 1):
        y = y0 + (y1 - y0) * i / N
        for dz in (-d_ger / 2 + 0.3, 0.0, d_ger / 2 - 0.3):
            for dx in (-d_ger / 2 + 0.3, 0.0, d_ger / 2 - 0.3):
                pt = V(dx, y, s * rb + dz)
                if sek.isInside(pt, 0.01, True):
                    carp.append((s, round(y, 1), round(s * rb + dz, 1)))
if carp:
    ys = sorted({c[1] for c in carp})
    print(f"  !!! BANT {len(carp)} noktada MALZEMEYE GIRIYOR")
    print(f"      y araligi {ys[0]:.1f} .. {ys[-1]:.1f}")
    print(f"      ornek: {carp[:4]}")
else:
    print("  bant yolu boyunca namlu katisiyla KESISME YOK")

# bandin agiz ankraj deligine hizalandigini da dogrula
db = P["d_bant_delik"]
print(f"\n  agiz ankraj deligi: z = +-{rb:.1f}, O{db:.1f} -> bant O{P['bant_OD']:.1f} "
      f"{'gecer' if db > P['bant_OD'] else 'GECMEZ'}")
print("\nSONUC:", "BANT YOLU ACIK" if not carp else "!!! BANT ENGELLENIYOR !!!")
