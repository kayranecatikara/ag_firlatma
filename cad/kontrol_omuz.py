#!/usr/bin/env python3
"""DURDURMA OMUZU geometrisini ve boncuk-koni acikligini DOGRULAR.

Kapsulu namluda durduran sey artik capraz pimin yarik ucuna carpmasi degil,
kapsulun halka kenarinin namlu agzindaki ice cikintiya oturmasi. Bu betik:
  1. omuzun gercekten olustugunu (malzeme/bosluk sondalariyla),
  2. boncuklarin koniye carpmadigini (omuz duzleminde VE namlu agzinda),
  3. omuz halka alanini ve tasiyabilecegi kuvveti
kontrol eder.

Kullanim:  freecadcmd cad/kontrol_omuz.py
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
sek = Part.Shape(); sek.read(kyol("cad", "V4_namlu.step"))
ic = lambda x, y, z: sek.isInside(V(x, y, z), 0.01, True)

Rb = P["D_bore"] / 2
Rk = Rb - P["bosluk"] / 2                       # kapsul dis yaricapi
alfa = math.radians(P["ALFA"])
t_om = P["t_omuz"]
R_om = (P["R_pitch"] + P["D_bilye"] / 2 + P["omuz_bosluk"]
        + t_om * math.tan(alfa))
yk = P["y_yuz_dur"]; y_om = yk + t_om; L = P["L_namlu"]

print(f"R_pitch {P['R_pitch']:.1f} · TPU {t_om:.1f} mm · omuz ic R {R_om:.2f} · "
      f"kapsul dis R {Rk:.2f}")
print(f"omuz duzlemi y={yk:.1f}  (TPU halka {yk:.1f}..{y_om:.1f})\n")

T = [("omuz ONUNDE r=20.5 -> malzeme",  0, y_om + 1.0, 20.5, True),
     ("omuz ONUNDE r=18.0 -> bos",      0, y_om + 1.0, 18.0, False),
     ("TPU cebi r=20.5 -> bos",         0, yk + 1.0,   20.5, False),
     ("omuz ARKASI (delik) r=20.5",     0, yk - 5.0,   20.5, False),
     ("agizda r=26 -> malzeme",         0, L - 0.5,    26.0, True)]
ok = True
for ad, x, y, z, bek in T:
    g = ic(x, y, z); ok &= (g == bek)
    print(f"  {ad:34} y={y:6.1f} r={z:5.1f}  "
          f"{'MALZEME' if g else 'BOSLUK '}  {'OK' if g == bek else 'HATA'}")

A = math.pi * (Rk ** 2 - R_om ** 2)
print(f"\n  OMUZ HALKA ALANI  {A:6.0f} mm2   (eski: capraz pim 96 mm2)")
print(f"  PETG 50 MPa  ->   {A * 50:6.0f} N   (eski: 4800 N)")

print("\n  boncuk / koni acikligi:")
for dy, ad in ((0.0, "omuz duzleminde"), (L - yk, "namlu agzinda")):
    r_bon = P["R_pitch"] + P["D_bilye"] / 2 + dy * math.tan(alfa)
    r_koni = R_om + max(dy - t_om, 0.0) * math.tan(alfa)
    pay = r_koni - r_bon
    ok &= pay > 0.5
    print(f"    {ad:18} boncuk {r_bon:5.2f} · koni {r_koni:5.2f} · "
          f"pay {pay:+5.2f} mm  {'OK' if pay > 0.5 else 'CARPIYOR'}")

r_arka = P["R_pitch"] - 0.5 * P["D_bilye"] * math.sin(alfa)
ok &= r_arka >= 9.0
print(f"\n  anti-cakisma: arka boncuk ekseni {r_arka:.2f} mm "
      f"(komsu yuvalar icin >=9.0)  {'OK' if r_arka >= 9.0 else 'CAKISIYOR'}")
print("\nSONUC:", "OMUZ GEOMETRISI DOGRU" if ok else "!!! HATALI !!!")
