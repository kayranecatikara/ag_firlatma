#!/usr/bin/env python3
"""Bant ankraj geometrisini ve boncuk-koni acikligini DOGRULAR.

Konfig degisince (strok, L0, ALFA, L_kapsul, r_bant...) ankraj deligi koniyle
cakisabilir ya da boncuklar ankraja carpabilir. Bu betik onu yakalar.

Kullanim:  freecadcmd cad/kontrol_ankraj.py
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
sek = Part.Shape(); sek.read(kyol("cad", "V4_namlu.step"))
ya = P["y_ankraj"]; y0 = ya - P["bilezik_geri"]; rb = P["r_bant"]
kw = P["kulak_w"]; db = P["d_bant_delik"]; Rb = P["D_bore"] / 2
ic = lambda x, y, z: sek.isInside(V(x, y, z), 0.01, True)

print(f"namlu {P['L_namlu']:.1f} · strok {P['STROK']:.0f} · L0 {P['L0']:.1f} · "
      f"kapsul {P['L_kapsul']:.1f} · ALFA {P['ALFA']:.0f}d")
print(f"ankraj y={ya:.2f}, bilezik {y0:.2f}..{ya:.2f}, r_bant={rb}, delik O{db}\n")

# DIKKAT: sondalar enine pim deliginin DISINDA bir y'de olmali, yoksa
# dogru geometride bile "bosluk" okur. Pim deligi y_pim +/- (dp/2).
dp = P["d_pim_ankraj"] + P["pim_bosluk"]
y_pim = ya - P["pim_geri"]
y_s = y0 + 3.0                                  # pim deliginden uzak kesit
T = [("bant deligi ekseni",            0, y_s,  rb,       False),
     ("bant deligi (arka agiz)",       0, y0 + 1.0, rb,   False),
     ("delik ic kenari r=6",           0, y_s,  rb - 6.0, False),
     ("delik DISI r=7.6 -> malzeme",   0, y_s,  rb - 7.6, True),
     ("kulak yan cidari x=9",          9, y_s,  rb,       True),
     ("kulak disi x=12",              12, y_s,  rb,       False),
     ("karsi kenar deligi",            0, y_s, -rb,       False),
     ("pim deligi, sag yan duvar",   kw - 2.0, y_pim,  rb, False),
     ("pim deligi, sol yan duvar", -(kw - 2.0), y_pim,  rb, False),
     ("pim ARKASINDA malzeme",       kw - 2.0, y_pim - 4.0, rb, True),
     ("pim ONUNDE malzeme",          kw - 2.0, y_pim + 4.0, rb, True),
     ("pim hizasi, kulak disinda",   kw - 2.0, y_pim, rb + 9.0, True)]

ok = True
for ad, x, y, z, bek in T:
    g = ic(x, y, z); ok &= (g == bek)
    print(f"  {ad:30} ({x:5.1f},{y:7.2f},{z:6.1f}) "
          f"{'MALZEME' if g else 'BOSLUK '}  {'OK' if g == bek else 'HATA'}")

# --- boncuk konisi ankraji vuruyor mu ---
a = math.radians(P["ALFA"])
bos = ya - P["y_yuz_dur"]                       # kapsul agzindan ankraja
r_bon = P["R_pitch"] + bos * math.tan(a)        # boncuk yaricapi ankraj duzleminde
r_koni = Rb + bos * math.tan(a)                 # koni yaricapi ayni duzlemde
pay = (rb - db / 2) - r_koni
print(f"\n  enine pim: O{P['d_pim_ankraj']:.0f} celik, delik O{dp:.1f}, "
      f"y={y_pim:.2f} (on yuzden {P['pim_geri']:.0f} mm geride)")
print(f"  pim arkasinda malzeme: {y_pim - y0:.1f} mm (bant bu yonde ceker)")
print(f"\n  kapsul agzi -> ankraj bosluk  {bos:6.2f} mm")
print(f"  boncuk yaricapi (ankrajda)    {r_bon:6.2f} mm")
print(f"  koni  yaricapi (ankrajda)     {r_koni:6.2f} mm")
print(f"  ankraj deliginin ic kenari    {rb - db / 2:6.2f} mm")
print(f"  PAY                           {pay:6.2f} mm  "
      f"{'OK' if pay > 0 else 'CAKISMA! r_bant buyutulmeli'}")
ok &= pay > 0
print("\nSONUC:", "ANKRAJ GEOMETRISI DOGRU" if ok else "!!! GEOMETRI HATALI !!!")
