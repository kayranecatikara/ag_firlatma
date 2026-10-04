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
     # AG ARTIK KAPSULDE DEGIL -> baslik merkezi MASIF olmali
     ("baslik merkezi MASIF",   V(0, y0 + L - 2, 0),                  True),
     ("ic bosluk (agirlik) acik", V(0, y0 + L - 25, 0),               False),
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

# --- kutle ve durdurma enerjisi ---
zarf = Part.makeCylinder(Rk, L, V(0, y0, 0), V(0, 1, 0))
ic_hacim = (zarf.Volume - sek.common(zarf).Volume) / 1000.0
m_kap = sek.Volume / 1000.0 * 1.27 * 0.82          # PETG, baski dolulugu
m_pim = 4.41 * 2.70                                 # capraz pim, aluminyum
print(f"\n  kapsul kati {sek.Volume/1000:5.2f} cm3 -> ~{m_kap:.1f} g "
      f"(ic bosluk {ic_hacim:.1f} cm3, agirlik azaltma)")
print(f"  DURACAK KUTLE {m_kap + m_pim:.1f} g (kapsul + capraz pim)")
for v in (17.1, 23.1, 27.7):
    print(f"    v={v:4.1f} m/s -> {0.5*(m_kap+m_pim)/1000*v**2:5.1f} J durdurulacak")

# --- AG ARTIK NAMLUDA: kapsulun onundeki hacim ---
Rb_i = P["D_bore"] / 2
strok = P["STROK"]
V_namlu = math.pi * Rb_i ** 2 * strok / 1000.0
L_ip = 39.2; V_ip = L_ip * 1000 * math.pi / 4 * 0.60 ** 2 / 1000.0
print(f"\n  AG NAMLUDA, KAPSULUN ONUNDE:")
print(f"    kullanilabilir hacim {V_namlu:6.1f} cm3 (O{2*Rb_i:.1f} x {strok:.0f} mm strok)")
print(f"    ag ipi kati hacmi    {V_ip:6.1f} cm3")
print(f"    doluluk              %{V_ip/V_namlu*100:.0f}  (kapsul icindeyken %75 sikisikti)")

print("\nSONUC:", "KAPSUL GEOMETRISI DOGRU" if ok else "!!! HATALI !!!")
