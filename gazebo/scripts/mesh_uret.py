#!/usr/bin/env python3
"""Gazebo gorsel mesh'lerini CAD'den uretir (freecadcmd ile calistir).

Namlu BASKIDA iki parca (01a + 01b) ama simulasyonda TEK govde olarak
gorunmeli; o yuzden baski/ STL'leri kopyalanmaz — mesh'ler dogrudan
cad/V4_*.step'ten, CAD koordinatlarinda, mm biriminde uretilir.
(SDF tarafinda scale 0.001 uygulanir.)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import FreeCAD, Part, Mesh                                    # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

HEDEF = kyol("gazebo", "models", "ag_firlatici", "meshes")
os.makedirs(HEDEF, exist_ok=True)

for kaynak, cikti in (("V4_namlu.step", "namlu.stl"),
                      ("V4_kapsul.step", "kapsul.stl")):
    yol = kyol("cad", kaynak)
    sek = Part.Shape(); sek.read(yol)
    m = Mesh.Mesh(); m.addFacets(sek.tessellate(0.25))
    hed = os.path.join(HEDEF, cikti)
    m.write(hed)
    print(f"{cikti:14} {sek.Volume/1000:8.2f} cm3  {m.CountFacets:7d} ucgen"
          f"  -> {os.path.relpath(hed, kyol())}")
