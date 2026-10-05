#!/usr/bin/env python3
"""Kapsulun IKI BLOGA bolunmesini dogrular.

Alt blok ust blogu iter; alt durduktan sonra ust kendi basina gidip
namlu agzindaki omza carpar. Kontrol edilenler:
  - iki parcanin hacmi tam kapsulu veriyor mu (spigot hacmi haric)
  - ITME YUZEYI alani (alt blogun halka yuzu)
  - spigot UST blogun haznesine giriyor mu, cakisma var mi
  - her blogun kutlesi ve durdurma enerjisi

Kullanim:  freecadcmd cad/kontrol_kapsul_bol.py
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
oku = lambda n: (lambda s: (s.read(kyol("cad", n + ".step")), s)[1])(Part.Shape())
tam, alt, ust = oku("V4_kapsul_hazneli"), oku("V4_kapsul_alt"), oku("V4_kapsul_ust")
Rk = P["D_bore"] / 2 - P["bosluk"] / 2
Rh = Rk - P["t_govde"]
y0 = P["arka"]; yb = y0 + P["y_bol_kap"]; L = P["L_kapsul"]

Va, Vu, Vt = alt.Volume / 1000, ust.Volume / 1000, tam.Volume / 1000
rs = Rh - P["spigot_bosluk_kap"]
Vspg = math.pi * (rs ** 2 - (rs - P["t_spigot_kap"]) ** 2) * P["h_spigot_kap"] / 1000
print(f"bolme duzlemi yerel y = {P['y_bol_kap']:.1f} (global {yb:.1f})")
print(f"  ALT blok {Va:6.2f} cm3 -> ~{Va*1.27*0.82:5.1f} g")
print(f"  UST blok {Vu:6.2f} cm3 -> ~{Vu*1.27*0.82:5.1f} g")
print(f"  toplam   {Va+Vu:6.2f} cm3 · tam kapsul {Vt:.2f} + spigot {Vspg:.2f} = "
      f"{Vt+Vspg:.2f}  fark {abs(Va+Vu-Vt-Vspg):.3f} cm3")

# itme yuzeyi: alt blogun yb duzlemindeki kati alani
kutu = Part.makeBox(4 * Rk, 0.2, 4 * Rk, V(-2 * Rk, yb - 0.25, -2 * Rk))
A_itme = alt.common(kutu).Volume / 0.2
print(f"\n  ITME YUZEYI (alt blok, y={yb:.1f})  {A_itme:5.0f} mm2")
print(f"  PETG 50 MPa -> {A_itme*50:.0f} N tasir")

# spigot ust bloga giriyor mu: ust blokta o hacim BOS olmali
ic = lambda v: ust.isInside(v, 0.01, True)
r_test = rs - P["t_spigot_kap"] / 2
sorun = [y for y in (1.0, 3.0, 5.0)
         if ic(V(r_test, yb + y, 0))]
print(f"\n  spigot yolu (r={r_test:.1f}, y={yb:.0f}..{yb+P['h_spigot_kap']:.0f}): "
      f"{'ACIK' if not sorun else 'UST BLOKLA CAKISIYOR!'}")

m_pim = 5.62 * 2.70
print(f"\n  DURDURMA ENERJISI (v = 17.4 m/s)")
print(f"    alt blok + capraz pim {Va*1.27*0.82 + m_pim:5.1f} g -> "
      f"{0.5*(Va*1.27*0.82+m_pim)/1000*17.4**2:5.1f} J  (yarik sonu tamponu durdurur)")
print(f"    UST blok + ag + boncuk {Vu*1.27*0.82 + 9.6 + 24:5.1f} g -> "
      f"{0.5*(Vu*1.27*0.82+9.6+24)/1000*17.4**2:5.1f} J  (namlu omzu durdurur)")
ok = abs(Va + Vu - Vt - Vspg) < 0.05 and A_itme > 300 and not sorun
print("\nSONUC:", "BOLME DOGRU" if ok else "!!! HATALI !!!")
