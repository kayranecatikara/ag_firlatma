# -*- coding: utf-8 -*-
"""Montaj parcalarini AYRI AYRI STEP olarak disa aktarir.

MONTAJ.step gorsellestirme/oturma kontrolu icindir (parcalar kaynasmis).
Imalat icin asagidaki tekil dosyalari kullanin.
"""
import FreeCAD as App, Part, os

OUT = os.path.dirname(os.path.abspath(__file__))
ADLAR = ["M_namlu", "M_kapsul", "M_bilye", "M_yay", "M_pim_sag", "M_pim_sol"]

for ad in ADLAR:
    yol = os.path.join(OUT, ad + ".brep")
    if not os.path.exists(yol):
        print("atlandi:", ad); continue
    sh = Part.Shape(); sh.read(yol)
    hedef = os.path.join(OUT, ad + ".step")
    sh.exportStep(hedef)
    b = sh.BoundBox
    print(f"{ad:10s} -> {ad}.step  hacim={sh.Volume/1000:7.2f} cm3  "
          f"olcu={b.XLength:.0f}x{b.YLength:.0f}x{b.ZLength:.0f} mm  "
          f"gecerli={sh.isValid()}")
