#!/usr/bin/env python3
"""KAPSUL ic geometrisini dogrular.

Ilk baskidan gelen sorunlar:
  - boncuk yuvalarinin tabani ag cikis konisine aciliyordu (boncuk dusuyor)
  - hazne ile baslik arasinda basamak vardi (ag takiliyor)
  - kapsul agiz asagi basilinca hazne tavani destek istiyordu

Bu betik: yuva tabani kapali mi, dudak var mi, ip deligi acik mi,
ag gecisi acik mi, hazne hacmi ag icin yetiyor mu — hepsini olcer.

Kullanim:  freecadcmd cad/kontrol_kapsul.py
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
sek = Part.Shape(); sek.read(kyol("cad", "V4_kapsul.step"))
ic = lambda v: sek.isInside(v, 0.01, True)

y0 = P["arka"]                      # kapsul montajda bu y'den basliyor
L = P["L_kapsul"]; a = math.radians(P["ALFA"])
rp, dy, der = P["R_pitch"], P["D_yuva"], P["derinlik"]
Rk = P["D_bore"] / 2 - P["bosluk"] / 2
Rh = Rk - P["t_govde"]
ur = V(1, 0, 0)
eks = V(math.sin(a), math.cos(a), 0)
agiz = V(rp, y0 + L, 0)
taban = agiz - eks * der

print(f"kapsul boyu {L:.0f} · dis R {Rk:.2f} · hazne R {Rh:.2f} · "
      f"R_pitch {rp:.1f} · yuva O{dy:.1f} derinlik {der:.1f}")
print(f"boncuk O{P['D_bilye']:.2f} · dudak daralmasi {P['lip_dar']:.1f} mm · "
      f"ip deligi O{P['d_ip_delik']:.1f}\n")

T = [("yuva ortasi BOS",        agiz - eks * (der / 2),               False),
     # DIKKAT: taban EKSENINDE O3 ip deligi var; taban malzemesini
     # eksenden kacirarak sonda.
     ("yuva TABANI dolu (eksen disi)",
      taban - eks * (P["t_yuva"] / 2) + V(0, 0, 3.0),                 True),
     ("ip deligi acik (eksende)",
      taban - eks * (P["t_yuva"] + 1.5),                              False),
     ("yuva yan cidari dolu",   agiz - eks * (der / 2)
                                + V(0, 0, dy / 2 + P["t_yuva"] / 2),  True),
     ("dudak hizasi DAR",       agiz - eks * 0.3
                                + V(0, 0, (dy - P["lip_dar"]) / 2 + 0.25), True),
     ("ag gecisi (eksen) acik", V(0, y0 + L - 2, 0),                  False),
     ("hazne ortasi acik",      V(0, y0 + L - 25, 0),                 False),
     ("arka blok dolu",         V(0, y0 + 12, 0),                     True)]

ok = True
for ad, v, bek in T:
    g = ic(v); ok &= (g == bek)
    print(f"  {ad:26} ({v.x:6.2f},{v.y:7.2f},{v.z:6.2f})  "
          f"{'DOLU' if g else 'BOS '}  {'OK' if g == bek else 'HATA'}")

# --- boncuk yuvada duruyor mu: dudak boncuktan dar olmali ---
d_lip = dy - P["lip_dar"]
tut = d_lip < P["D_bilye"]
ok &= tut
print(f"\n  dudak capi {d_lip:.2f} < boncuk {P['D_bilye']:.2f} -> "
      f"{'BONCUK TUTULUR' if tut else 'BONCUK DUSER'}")
print(f"  boncugun yuvaya girme derinligi {der - P['lip_boy']:.1f} mm "
      f"(boncuk capi {P['D_bilye']:.2f})")

# --- hazne hacmi: kapsulun ic bosluğu ---
# ic bosluk = kapsulun dis zarfi - gercek kati
zarf = Part.makeCylinder(Rk, L, V(0, y0, 0), V(0, 1, 0))
ic_hacim = (zarf.Volume - sek.common(zarf).Volume) / 1000.0
L_ip = 39.2; A_ip = math.pi / 4 * 0.60 ** 2
V_ip = L_ip * 1000 * A_ip / 1000.0
print(f"\n  KAPSUL IC BOSLUGU   {ic_hacim:6.2f} cm3")
print(f"  ag ipi (39.2 m x O0.60) kati hacmi {V_ip:.2f} cm3")
print(f"  gereken doluluk      %{V_ip / ic_hacim * 100:.0f}  "
      f"({'rahat' if V_ip / ic_hacim < 0.55 else 'sikisik' if V_ip / ic_hacim < 0.75 else 'YETMEZ'})")

print("\nSONUC:", "KAPSUL GEOMETRISI DOGRU" if ok else "!!! HATALI !!!")
